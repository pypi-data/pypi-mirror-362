# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

import json
from argparse import Namespace
from typing import Any, Optional

from fabric_cli.client import fab_api_azure as azure_api
from fabric_cli.client import fab_api_client as fabric_api
from fabric_cli.core import fab_constant as constant
from fabric_cli.core.fab_exceptions import FabricCLIError
from fabric_cli.utils import fab_ui as utils_ui


def delete_resource(
    args: Namespace,
    bypass_confirmation: bool | None,
    debug: Optional[bool] = True,
    operation: Optional[str] = "delete",
) -> bool:
    if not bypass_confirmation:
        if utils_ui.prompt_confirm():
            return _do_delete_resource(args, operation=operation)
        else:
            if debug:
                utils_ui.print_warning(f"Resource {operation} cancelled")
            return False
    else:
        if debug:
            utils_ui.print_warning(f"Executing force {operation}...")
        return _do_delete_resource(args, debug=debug, operation=operation)


def start_resource(
    args: Namespace, bypass_confirmation: bool | None, debug: Optional[bool] = True
) -> bool:
    if not bypass_confirmation:
        if utils_ui.prompt_confirm():
            return _do_start_resource(args, debug)
        else:
            if debug:
                utils_ui.print_warning("Resource start cancelled")
            return False
    else:
        if debug:
            utils_ui.print_warning("Executing force start...")
        return _do_start_resource(args, debug)


def stop_resource(
    args: Namespace, bypass_confirmation: bool | None, debug: Optional[bool] = True
) -> bool:
    if not bypass_confirmation:
        if utils_ui.prompt_confirm():
            return _do_stop_resource(args, debug)
        else:
            if debug:
                utils_ui.print_warning("Resource stop cancelled")
            return False
    else:
        if debug:
            utils_ui.print_warning("Executing force stop...")
        return _do_stop_resource(args, debug)


def assign_resource(
    args: Namespace,
    payload: str,
    bypass_confirmation: bool | None,
    debug: Optional[bool] = True,
) -> bool:
    if not bypass_confirmation:
        if utils_ui.prompt_confirm():
            return _do_assign_resource(args, payload, debug)
        else:
            if debug:
                utils_ui.print_warning("Resource assignment cancelled")
            return False
    else:
        if debug:
            utils_ui.print_warning("Executing force assignment...")
        return _do_assign_resource(args, payload, debug)


def unassign_resource(
    args: Namespace,
    bypass_confirmation: bool | None,
    payload: Optional[str] = None,
    debug: Optional[bool] = True,
) -> bool:
    if not bypass_confirmation:
        if utils_ui.prompt_confirm():
            return _do_unassign_resource(args, payload, debug)
        else:
            if debug:
                utils_ui.print_warning("Resource unassignment cancelled")
            return False
    else:
        if debug:
            utils_ui.print_warning("Executing force unassignment...")
        return _do_unassign_resource(args, payload, debug)


def get_api_version(resource_uri: str) -> Any:
    # Resource URI format Option A: /subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/{namespace}/{resource_type}/{resource_name}
    # Resource URI format Option B: /subscriptions/{subscription_id}/providers/{namespace}/{resource_type}
    ru_parts = resource_uri.lstrip("/").split("/")
    subscription_id = ru_parts[1]
    namespace = ru_parts[3] if ru_parts[2] == "providers" else ru_parts[5]
    resource_type = ru_parts[4] if ru_parts[2] == "providers" else ru_parts[6]
    # Hardcoded api version for capacities for performance reasons
    if namespace == "Microsoft.Fabric" and resource_type == "capacities":
        return "2023-11-01"

    args = Namespace()
    args.subscription_id = subscription_id
    args.provider_namespace = namespace

    response = azure_api.get_provider_azure(args)
    if response.status_code == 200:
        json_response = json.loads(response.text)
        for rt in json_response["resourceTypes"]:
            if rt["resourceType"].lower() == resource_type.lower():
                return rt["apiVersions"][0]

    raise FabricCLIError(
        f"Resource type '{args.resource_type}' not found in provider '{args.provider_namespace}'",
        status_code=constant.ERROR_NOT_SUPPORTED,
    )


# Utils
def _do_delete_resource(
    args: Namespace, debug: Optional[bool] = True, operation: Optional[str] = "delete"
) -> bool:
    if debug:
        if operation is not None:
            utils_ui.print_grey(f"{_to_gerund_capitalized(operation)} '{args.name}'...")
    response = fabric_api.do_request(args)

    if response.status_code == 200:
        if debug:
            utils_ui.print_done(f"'{args.name}' {operation}d")
        return True
    elif response.status_code in [201, 202]:
        if debug:
            utils_ui.print_done(f"'{args.name}' is being {operation}d")
        return True

    return False


def _do_start_resource(args: Namespace, debug: Optional[bool] = True) -> bool:
    if debug:
        utils_ui.print_grey(f"Starting '{args.name}'...")
    response = fabric_api.do_request(args)

    if response.status_code == 200:
        if debug:
            utils_ui.print_done(f"'{args.name}' started")
        return True
    elif response.status_code in [201, 202]:
        if debug:
            utils_ui.print_done(f"'{args.name}' is starting")
        return True

    return False


def _do_stop_resource(args: Namespace, debug: Optional[bool] = True) -> bool:
    if debug:
        utils_ui.print_grey(f"Stopping '{args.name}'...")
    response = fabric_api.do_request(args)

    if response.status_code == 200:
        if debug:
            utils_ui.print_done(f"'{args.name}' stopped")
        return True
    elif response.status_code in [201, 202]:
        if debug:
            utils_ui.print_done(f"'{args.name}' is stopping")

    return False


def _do_assign_resource(
    args: Namespace, payload: str, debug: Optional[bool] = True
) -> bool:
    if debug:
        utils_ui.print_grey(f"Assigning '{args.name}'...")
    response = fabric_api.do_request(args, data=payload)

    if response.status_code == 200:
        if debug:
            utils_ui.print_done(f"'{args.name}' assigned")
        return True
    elif response.status_code in [201, 202]:
        if debug:
            utils_ui.print_done(f"'{args.name}' is being assigned")
        return True

    return False


def _do_unassign_resource(
    args: Namespace, payload: Optional[str] = None, debug: Optional[bool] = True
) -> bool:
    if debug:
        utils_ui.print_grey(f"Unassigning '{args.name}'...")
    response = fabric_api.do_request(args, data=payload)

    if response.status_code == 200:
        if debug:
            utils_ui.print_done(f"'{args.name}' unassigned")
        return True
    elif response.status_code in [201, 202]:
        if debug:
            utils_ui.print_done(f"'{args.name}' is being unassigned")
        return True

    return False


def _to_gerund_capitalized(operation: str) -> str:
    if operation.endswith("e") and not operation.endswith("ee"):
        result = f"{operation[:-1]}ing"
    else:
        result = f"{operation}ing"
    return result.capitalize()
