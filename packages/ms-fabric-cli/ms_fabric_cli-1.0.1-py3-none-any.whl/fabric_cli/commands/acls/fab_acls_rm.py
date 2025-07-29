# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

import json
from argparse import Namespace

from fabric_cli.client import fab_api_workspace as api_workspaces
from fabric_cli.core import fab_constant as constant
from fabric_cli.core.fab_exceptions import FabricCLIError
from fabric_cli.core.hiearchy.fab_hiearchy import FabricElement, Workspace
from fabric_cli.utils import fab_ui as utils_ui


def exec_command(args: Namespace, context: FabricElement) -> None:
    if isinstance(context, Workspace):
        _rm_acls_workspace(context, args)


# Workspaces
def _rm_acls_workspace(workspace: Workspace, args: Namespace) -> None:
    if args.force or utils_ui.prompt_confirm():
        identity = args.identity
        args.ws_id = workspace.id

        response = api_workspaces.acl_list_from_workspace(args)

        data = json.loads(response.text)
        is_valid_identity, matching_identity_id = _validate_identity(identity, data)

        if is_valid_identity:
            utils_ui.print_grey(f"Deleting ACL from '{workspace.name}'...")
            args.id = matching_identity_id

            response = api_workspaces.acl_delete_from_workspace(args)

            if response.status_code == 200:
                utils_ui.print_done(f"ACL removed")
        else:
            raise FabricCLIError(
                f"'{identity}' identity not found", constant.ERROR_NOT_FOUND
            )


# Utils
def _validate_identity(identity: str, data: dict) -> tuple[bool, str]:
    for item in data["value"]:
        upn = item["principal"].get("userDetails", {}).get("userPrincipalName")
        spn_client_id = (
            item["principal"].get("servicePrincipalDetails", {}).get("aadAppId")
        )
        group_name = item["principal"].get("displayName", {})
        object_id = item["principal"].get("id", {})

        if (
            upn == identity
            or spn_client_id == identity
            or object_id == identity
            or group_name == identity
        ):
            return True, item["id"]
    return False, ""
