# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

import webbrowser
from argparse import Namespace
from typing import Optional

from fabric_cli.core import fab_constant, fab_logger, fab_state_config
from fabric_cli.core.fab_auth import FabAuth
from fabric_cli.core.fab_types import uri_mapping
from fabric_cli.core.hiearchy.fab_hiearchy import FabricElement, Item, Workspace
from fabric_cli.utils import fab_ui as utils_ui

COMMAND = "open"


def exec_command(args: Namespace, context: FabricElement) -> None:
    if isinstance(context, Workspace):
        _open_workspace(context)
    elif isinstance(context, Item):
        _open_item(context)


# Workspaces
def _open_workspace(workspace: Workspace) -> None:
    workspace_id = workspace.id
    experience = _get_ux_experience()

    if workspace_id:
        url = f"{fab_constant.WEB_URI}/{workspace_id}/list?experience={experience}"
        _open_in_browser(url, workspace.name)


# Items
def _open_item(item: Item) -> None:
    workspace_id = item.workspace.id
    item_id = item.id
    experience = _get_ux_experience()

    if workspace_id and item_id:
        url = f"{fab_constant.WEB_URI}/{workspace_id}/{uri_mapping.get(item.item_type, '')}/{item_id}/?experience={experience}"
        _open_in_browser(url, item.name)


# Utils
def _open_in_browser(url: str, name: str) -> None:
    utils_ui.print_grey(f"Opening '{name}' in the web browser...")
    utils_ui.print_done(f"{url}")

    if FabAuth()._get_auth_property(fab_constant.IDENTITY_TYPE) != "user":
        fab_logger.log_error(
            "Only supported with user authentication", COMMAND)
        return
    else:
        claims = FabAuth().get_token_claims(
            fab_constant.SCOPE_FABRIC_DEFAULT, ["upn", "tid"]
        )

        # Rename the "tid" key to "ctid" for the query parameter
        if claims and "tid" in claims:
            claims["ctid"] = claims.pop("tid")

        url = _add_claims_as_query_param(url, claims)

        webbrowser.open_new(url)


def _add_claims_as_query_param(url: str, claims: Optional[dict[str, str]]) -> str:
    if claims:
        for key, value in claims.items():
            separator = "&" if "?" in url else "?"
            url = f"{url}{separator}{key}={value}"

    return url


def _get_ux_experience() -> str:
    if (
        fab_state_config.get_config(fab_constant.FAB_DEFAULT_OPEN_EXPERIENCE)
        == "powerbi"
    ):
        return fab_constant.FAB_DEFAULT_OPEN_EXPERIENCE_POWERBI
    else:
        return fab_constant.FAB_DEFAULT_OPEN_EXPERIENCE_FABRIC
