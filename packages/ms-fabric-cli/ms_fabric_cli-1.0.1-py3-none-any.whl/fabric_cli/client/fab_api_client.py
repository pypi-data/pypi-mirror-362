# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

import json
import platform
import time
from argparse import Namespace

import requests
from requests.adapters import HTTPAdapter, Retry
from requests.structures import CaseInsensitiveDict

from fabric_cli.core import fab_constant, fab_logger
from fabric_cli.core.fab_auth import FabAuth
from fabric_cli.core.fab_context import Context as FabContext
from fabric_cli.core.fab_exceptions import (
    AzureAPIError,
    FabricAPIError,
    FabricCLIError,
    OnelakeAPIError,
)
from fabric_cli.errors import ErrorMessages
from fabric_cli.utils import fab_files as files_utils
from fabric_cli.utils import fab_ui as utils_ui
from fabric_cli.utils import fab_error_parser as utils_errors


class ApiResponse:
    def __init__(self, status_code: int, text: str, headers: CaseInsensitiveDict[str]):
        self.status_code = status_code
        self.text = text
        self.headers = headers

    def append_text(self, text: str, total_pages: int = 0):
        try:
            original_text = json.loads(self.text)
            new_text = json.loads(text)

            for key, value in original_text.items():
                if isinstance(value, list) and key in new_text:
                    original_text[key].extend(new_text[key])

            original_text.pop("continuationToken", None)
            original_text.pop("continuationUri", None)
            original_text["total_pages"] = total_pages + 1

            self.text = json.dumps(original_text)
        except json.JSONDecodeError as e:
            raise FabricCLIError(
                ErrorMessages.Common.json_decode_error(str(e)),
                fab_constant.ERROR_INVALID_JSON,
            )

    def json(self):
        return json.loads(self.text)


def do_request(
    args,
    json=None,
    data=None,
    files=None,
    timeout_sec=240,
    continuation_token=None,
) -> ApiResponse:
    json_file = getattr(args, "json_file", None)
    audience_value = getattr(args, "audience", None)
    headers_value = getattr(args, "headers", None)
    method = getattr(args, "method", "get")
    wait = getattr(args, "wait", True)  # Operations are synchronous by default
    raw_response = getattr(args, "raw_response", False)
    request_params = getattr(args, "request_params", {})
    uri = args.uri.split("?")[0]
    # Get query parameters from URI and add them to request_params extracted from args
    _params_from_uri = args.uri.split("?")[1] if len(args.uri.split("?")) > 1 else None
    if _params_from_uri:
        _params = _params_from_uri.split("&")
        for _param in _params:
            _key, _value = _param.split("=")
            request_params[_key] = _value

    if json_file is not None:
        json = files_utils.load_json_from_path(json_file)

    # Get endpoint and token, and set continuation token if present (pbi and storage audience)
    if audience_value == "storage":
        scope = fab_constant.SCOPE_ONELAKE_DEFAULT
        url = fab_constant.API_ENDPOINT_ONELAKE
    elif audience_value == "azure":
        scope = fab_constant.SCOPE_AZURE_DEFAULT
        url = fab_constant.API_ENDPOINT_AZURE
    elif audience_value == "powerbi":
        scope = fab_constant.SCOPE_FABRIC_DEFAULT
        url = fab_constant.API_ENDPOINT_POWER_BI
    else:
        scope = fab_constant.SCOPE_FABRIC_DEFAULT
        url = f"{fab_constant.API_ENDPOINT_FABRIC}/{fab_constant.API_VERSION_FABRIC}"

    if continuation_token:
        request_params["continuationToken"] = continuation_token

    # Build url
    url = f"https://{url}/{uri}"
    if request_params:
        url += f"?{requests.compat.urlencode(request_params)}"

    # Get token
    token = FabAuth().get_access_token(scope)

    # Build headers
    ctxt_cmd = FabContext().command
    headers = {
        "Authorization": "Bearer " + str(token),
        "User-Agent": f"{fab_constant.API_USER_AGENT}/{fab_constant.FAB_VERSION} ({ctxt_cmd}; {platform.system()}; {platform.machine()}; {platform.release()})",
    }

    if files is None:
        headers["Content-Type"] = "application/json"

    if headers_value is not None:
        if isinstance(args.headers, dict):
            headers.update(args.headers)
        else:
            raise FabricCLIError(
                ErrorMessages.Common.invalid_headers_format(),
                fab_constant.ERROR_INVALID_OPERATION,
            )

    try:
        session = requests.Session()
        retries_count = 3
        retries = Retry(
            total=retries_count, backoff_factor=1, status_forcelist=[502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retries)
        session.mount("https://", adapter)

        request_params = {
            "headers": headers,
            "timeout": timeout_sec,
        }

        if files is not None:
            request_params["files"] = files
        elif json is not None:
            request_params["json"] = json
        elif data is not None:
            request_params["data"] = data

        for attempt in range(retries_count + 1):

            fab_logger.log_debug_http_request(
                method, url, headers, timeout_sec, attempt, json, data, files
            )
            start_time = time.time()
            response = session.request(method=method, url=url, **request_params)
            fab_logger.log_debug_http_response(
                response.status_code, response.headers, response.text, start_time
            )

            if raw_response:
                return ApiResponse(
                    status_code=response.status_code,
                    text=response.text,
                    headers=response.headers,
                )

            match response.status_code:
                case 401:
                    raise FabricCLIError(
                        ErrorMessages.Common.unauthorized(),
                        fab_constant.ERROR_UNAUTHORIZED,
                    )
                case 403:
                    raise FabricCLIError(
                        ErrorMessages.Common.forbidden(),
                        fab_constant.ERROR_FORBIDDEN,
                    )
                case 404:
                    raise FabricCLIError(
                        ErrorMessages.Common.resource_not_found(),
                        fab_constant.ERROR_NOT_FOUND,
                    )
                case 429:
                    retry_after = int(response.headers["Retry-After"])
                    utils_ui.print_info(
                        f"Rate limit exceeded. {attempt}º retrying attemp in {retry_after} seconds"
                    )
                    time.sleep(retry_after)
                    continue
                # We handle 202 status code in a different way for Fabric and Azure APIs
                # if the Location header is present, we ignore it if it is the Get Item Job Instance API url returned by the Run On Demand Item Job API
                case 202 if (
                    wait
                    and scope == fab_constant.SCOPE_FABRIC_DEFAULT
                    and "/jobs/instances/" not in response.headers.get("Location", "")
                ):
                    api_response = ApiResponse(
                        status_code=response.status_code,
                        text=response.text,
                        headers=response.headers,
                    )
                    fab_logger.log_debug(f"Operation started. Polling for result...")
                    return _handle_fab_long_running_op(api_response)
                case 201 | 202 if wait and scope == fab_constant.SCOPE_AZURE_DEFAULT:
                    # Track Azure API asynchronous operations
                    api_response = ApiResponse(
                        status_code=response.status_code,
                        text=response.text,
                        headers=response.headers,
                    )
                    fab_logger.log_debug(f"Operation started. Polling for result...")
                    return _handle_azure_async_op(api_response)
                case c if c in [200, 201, 202, 204]:
                    api_response = ApiResponse(
                        status_code=response.status_code,
                        text=response.text,
                        headers=response.headers,
                    )
                    return _handle_successful_response(args, api_response)
                case _:
                    if fab_constant.API_ENDPOINT_FABRIC in url:
                        raise FabricAPIError(response.text)
                    elif fab_constant.API_ENDPOINT_ONELAKE in url:
                        raise OnelakeAPIError(response.text)
                    elif fab_constant.API_ENDPOINT_AZURE in url:
                        raise AzureAPIError(response.text)
                    raise FabricCLIError(
                        ErrorMessages.Common.unexpected_error_response(
                            response.status_code,
                            response.text,
                        ),
                        utils_errors.map_http_status_code_to_error_code(
                            response.status_code
                        ),
                    )

        raise FabricCLIError(
            ErrorMessages.Common.max_retries_exceeded(retries_count),
            fab_constant.ERROR_MAX_RETRIES_EXCEEDED,
        )

    except requests.RequestException as ex:
        fab_logger.log_debug_http_request_exception(ex)
        # TODO handle specific error code
        raise FabricCLIError(
            ErrorMessages.Common.unexpected_error(str(ex)),
            fab_constant.ERROR_UNEXPECTED_ERROR,
        ) from ex


# Utils


def _handle_successful_response(args: Namespace, response: ApiResponse) -> ApiResponse:
    if fab_constant.DEBUG:
        _print_response_details(response)

    _continuation_token = None

    # In ADLS Gen2 / Onelake, check for x-ms-continuation token in response headers
    if "x-ms-continuation" in response.headers:
        # utils_ui.print_info(
        #     f"Continuation token found for Onelake. Fetching next page of results..."
        # )
        _continuation_token = response.headers["x-ms-continuation"]
    # In Fabric, check for continuation token in response text
    elif response.text != "" and response.text != "null":
        if "continuationToken" in response.text:
            _text = json.loads(response.text)
            if _text and "continuationToken" in _text:
                _continuation_token = _text["continuationToken"]
                # utils_ui.print_info(
                #     f"Continuation token found for Fabric. Fetching next page of results..."
                # )

    if _continuation_token:
        _response = do_request(args, continuation_token=_continuation_token)
    if _continuation_token and _response.status_code == 200:
        response.status_code = 200
        response.append_text(_response.text)

    return response


def _print_response_details(response: ApiResponse) -> None:
    response_details = dict(
        {
            "status_code": response.status_code,
            "response": response.text,
            "headers": dict(response.headers),
        }
    )

    try:
        response_details["response"] = dict(json.loads(response.text))
    except json.JSONDecodeError:
        pass

    fab_logger.log_debug(json.dumps(dict(response_details), indent=4))


def _handle_fab_long_running_op(response: ApiResponse, max_attempts=10) -> ApiResponse:
    # Poll for the result of a long running operation
    # https://learn.microsoft.com/en-us/rest/api/fabric/articles/long-running-operation
    if response.headers.get("x-ms-operation-id") is None:
        if not response.headers.get("Location"):
            return response
        uri = response.headers["Location"]
        # Match the URI with the fab_constant.API_ENDPOINT_FABRIC and remove it and all previous characters from the URI
        # The default endpoint is "api.fabric.microsoft.com" but it can be different in some cases (e.g. "msit.fabric.microsoft.com")
        _endpoint = fab_constant.API_ENDPOINT_FABRIC.replace("api.", "")
        if not _endpoint in uri:
            return response
        _api_version = fab_constant.API_VERSION_FABRIC
        uri = uri[uri.find(_endpoint) + len(f"{_endpoint}/{_api_version}") :]
    else:
        uri = f"operations/{response.headers['x-ms-operation-id']}"
    # ignore Retry-After header for now and use exponential backoff
    # interval = int(response.headers.get("Retry-After", "15"))
    return _poll_operation(
        "fabric", uri, response, fab_constant.SCOPE_FABRIC_DEFAULT, True, max_attempts
    )


def _handle_azure_async_op(response: ApiResponse, max_attempts=10) -> ApiResponse:
    # First check for the Azure-AsyncOperation header
    uri = response.headers.get("Azure-AsyncOperation")
    if uri is None:
        # Check fot the Location header
        uri = response.headers.get("Location")
        check_status = False
    else:
        check_status = True

    # If no header is found or the URI doesn't match the expected pattern, raise an error
    if uri is None or not fab_constant.API_ENDPOINT_AZURE in uri:
        raise AzureAPIError(response.text)

    # Match the URI with the fab_constant.API_ENDPOINT_AZURE and remove it and all previous characters from the URI
    uri = uri[
        uri.find(fab_constant.API_ENDPOINT_AZURE)
        + len(fab_constant.API_ENDPOINT_AZURE) :
    ]
    # ignore Retry-After header for now and use exponential backoff
    # interval = int(response.headers.get("Retry-After", "15"))
    return _poll_operation(
        "azure",
        uri,
        response,
        fab_constant.SCOPE_AZURE_DEFAULT,
        check_status,
        max_attempts,
    )


def _poll_operation(
    audience, uri, original_response: ApiResponse, scope, check_status, max_attempts
) -> ApiResponse:
    attempts = 0
    args = Namespace()
    args.uri = uri
    args.audience = audience
    args.method = "get"
    args.wait = False
    args.params = {}
    while attempts < max_attempts:
        response = do_request(args)
        interval = (2**attempts - 1) / 2 if attempts > 0 else 0

        if response.status_code == 200:
            if check_status:
                result_json = response.json()
                status = result_json.get("status")
                #
                if status == "Succeeded" or status == "Completed":
                    fab_logger.log_progress(status)
                    if scope == fab_constant.SCOPE_AZURE_DEFAULT:
                        original_response.status_code = 200
                        return original_response
                    elif scope == fab_constant.SCOPE_FABRIC_DEFAULT:
                        return _fetch_operation_result(
                            args, uri, response, original_response
                        )
                elif status == "Failed":
                    fab_logger.log_progress(status)
                    raise FabricCLIError(
                        ErrorMessages.Common.operation_failed(
                            str(result_json.get("error"))
                        ),
                        fab_constant.ERROR_OPERATION_FAILED,
                    )
                elif status == "Cancelled":
                    fab_logger.log_progress(status)
                    raise FabricCLIError(
                        ErrorMessages.Common.operation_cancelled(
                            str(result_json.get("error"))
                        ),
                        fab_constant.ERROR_OPERATION_CANCELLED,
                    )
                else:
                    # Any other status is considered running
                    _log_operation_progress(result_json)
                    time.sleep(interval)
                    attempts += 1
            else:
                original_response.status_code = 200
                return original_response
        elif not check_status and response.status_code in [202, 201]:
            time.sleep(interval)
            attempts += 1
        else:
            raise FabricCLIError(
                ErrorMessages.Common.unexpected_error_response(
                    response.status_code,
                    response.text,
                ),
                utils_errors.map_http_status_code_to_error_code(response.status_code),
            )
    return original_response


def _fetch_operation_result(
    args: Namespace, uri: str, response: ApiResponse, original_response: ApiResponse
) -> ApiResponse:
    # If it is an Operation API, fetch the result
    if "operations/" in uri:
        try:
            args.uri = f"{uri}/result"
            args.method = "get"
            return do_request(args)
        except FabricAPIError as e:
            if e.status_code != "OperationHasNoResult":
                raise e
            original_response.status_code = 200
            return original_response
    else:
        # If it is not an Operation API (e.g. Job Instance), return the response
        return response


def _log_operation_progress(result_json: dict) -> None:
    # Common behaviour for Azure and Fabric REST APIs
    status = result_json.get("status")
    percentage_complete = result_json.get("percentageComplete")
    if percentage_complete is None:
        # But sometimes is missing in the response
        fab_logger.log_progress(status)
    else:
        fab_logger.log_progress(status, percentage_complete)


def check_token_expired(response: ApiResponse) -> bool:
    if response.status_code == 401:
        try:
            _text = json.loads(response.text)
            if _text.get("errorCode", "") == "TokenExpired":
                return True
        except json.JSONDecodeError:
            pass
    return False
