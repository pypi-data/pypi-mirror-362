# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

import json
from argparse import Namespace

from fabric_cli.client import fab_api_workspace as api_workspaces
from fabric_cli.core import fab_constant, fab_logger
from fabric_cli.core.fab_exceptions import FabricCLIError
from fabric_cli.core.hiearchy.fab_hiearchy import FabricElement, Workspace
from fabric_cli.utils import fab_ui as utils_ui


def exec_command(args: Namespace, context: FabricElement) -> None:
    if isinstance(context, Workspace):
        _set_acls_workspace(context, args)


# Workspaces
def _set_acls_workspace(workspace: Workspace, args: Namespace) -> None:
    if args.force or utils_ui.prompt_confirm():
        args.ws_id = workspace.id
        identity = args.identity

        response = api_workspaces.acl_list_from_workspace(args)

        if response.status_code in (200, 201):
            ws_acls = response.text
            if ws_acls:
                if identity in ws_acls:
                    fab_logger.log_warning(
                        "The provided principal already has a role assigned in the workspace"
                    )
                    if args.force or utils_ui.prompt_confirm("Overwrite?"):
                        args.id = identity
                        payload = json.dumps({"role": args.role})
                        response = api_workspaces.acl_update_to_workspace(args, payload)

                        if response.status_code in (200, 201):
                            utils_ui.print_done("ACL updated")

                    return

        types_to_try = ["User", "ServicePrincipal", "Group", "ServicePrincipalProfile"]
        success = False

        utils_ui.print_grey(f"Adding ACL to '{workspace.name}'...")

        for principal_type in types_to_try:
            payload = json.dumps(
                {
                    "principal": {"id": identity, "type": principal_type},
                    "role": args.role,
                }
            )

            try:
                response = api_workspaces.acl_add_to_workspace(args, payload)
                if response.status_code in (200, 201):
                    utils_ui.print_done("ACL set")
                    success = True
                    break
            except Exception as e:
                pass

        if not success:
            raise FabricCLIError(
                f"'{identity}' identity not found", fab_constant.ERROR_NOT_FOUND
            )
