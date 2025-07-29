# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.


from typing import Optional, Tuple
from requests import Response


class CommonErrors:

    @staticmethod
    def invalid_element_type(element_type: str) -> str:
        return f"'{element_type}' is not a valid Fabric element type"

    @staticmethod
    def invalid_workspace_type(workspace_type: str) -> str:
        return f"'{workspace_type}' is not a valid Fabric workspace type"

    @staticmethod
    def invalid_item_type(item_type: str) -> str:
        return f"'{item_type}' is not a valid Fabric item type"

    @staticmethod
    def invalid_virtual_workspace_type(vws_type: str) -> str:
        return f"'{vws_type}' is not a valid Fabric virtual workspace type"

    @staticmethod
    def invalid_virtual_item_container_type(vic_type: str) -> str:
        return f"'{vic_type}' is not a valid Fabric virtual item container type"

    @staticmethod
    def file_or_directory_not_exists() -> str:
        return "The specified file or directory does not exist"

    @staticmethod
    def invalid_json_format() -> str:
        return "Invalid JSON format"

    @staticmethod
    def type_not_supported(type_name: str) -> str:
        return f"The type '{type_name}' is not supported"

    @staticmethod
    def invalid_path(path: Optional[str] = None) -> str:
        return (
            f"The path '{path}' is invalid" if path else "The specified path is invalid"
        )

    @staticmethod
    def invalid_guid(parameter_name: str) -> str:
        return f"The parameter '{parameter_name}' must be a valid GUID"

    @staticmethod
    def unauthorized() -> str:
        return "Access is unauthorized"

    @staticmethod
    def forbidden() -> str:
        return "Access is forbidden. You do not have permission to access this resource"

    @staticmethod
    def max_retries_exceeded(retries_count: int) -> str:
        return f"Maximum retries ({retries_count}) exceeded. The operation could not be completed"

    @staticmethod
    def unexpected_error_response(http_status_code: int, message: str) -> str:
        return f"An unexpected error occurred with status code: {http_status_code} and message: {message}"

    @staticmethod
    def unexpected_error(error: str) -> str:
        return f"An unexpected error occurred: {error}"

    @staticmethod
    def operation_failed(error: str) -> str:
        return f"The operation failed: {error}"

    @staticmethod
    def operation_cancelled(error: str) -> str:
        return f"The operation was cancelled: {error}"

    @staticmethod
    def invalid_headers_format() -> str:
        return "The headers format is invalid"

    @staticmethod
    def invalid_json_content(content: str, error: Optional[str]) -> str:
        base_msg = f"The JSON content is invalid: {content}"
        return f"{base_msg}. Error: {error}" if error else f"{base_msg}"

    @staticmethod
    def unexpected_response(status_code: int, response_text: str) -> str:
        return f"Received an unexpected response with status code {status_code}: {response_text}"

    @staticmethod
    def resource_not_found(resource: Optional[dict] = None) -> str:
        return (
            f"The {resource['type']} '{resource['name']}' could not be found"
            if resource
            else "The requested resource could not be found"
        )

    @staticmethod
    def identity_not_found(identity: str) -> str:
        return f"The identity '{identity}' could not be found"

    @staticmethod
    def json_decode_error(error: str) -> str:
        return f"Failed to decode JSON: {error}"

    @staticmethod
    def traversing_not_supported(path: str) -> str:
        return f"Traversing into '{path}' is not supported"

    @staticmethod
    def personal_workspace_not_found() -> str:
        return "The personal workspace could not be found"

    @staticmethod
    def personal_workspace_user_auth_only() -> str:
        return "The personal workspace is only available with user authentication"

    @staticmethod
    def folder_not_found(folder: str, item_name: str, valid_folders: str) -> str:
        return f"The folder '{folder}' could not be found in item '{item_name}'. Valid folders are: {valid_folders}"

    @staticmethod
    def path_not_found(path: str) -> str:
        return f"The path '{path}' could not be found"

    @staticmethod
    def item_not_supported_in_context(item_type: str, context_type: str) -> str:
        return f"The item type '{item_type}' is not supported in the context '{context_type}'"

    @staticmethod
    def item_not_supported(item_type: str) -> str:
        return f"The item type '{item_type}' is not supported"
