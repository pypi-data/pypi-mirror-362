# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

from fabric_cli.core import fab_constant, fab_state_config
from fabric_cli.core.fab_types import VirtualItemContainerType
from fabric_cli.core.hiearchy.fab_hiearchy import Item, Workspace
from fabric_cli.utils import fab_mem_store as utils_mem_store
from fabric_cli.utils import fab_ui as utils_ui
from fabric_cli.utils import fab_util as utils


def exec(workspace: Workspace, args):
    show_details = bool(args.long)
    show_all = bool(args.all)
    ws_items: list[Item] = utils_mem_store.get_workspace_items(workspace)

    if ws_items:
        sorted_items = utils.sort_items_by_config(ws_items)
        sorted_items_dict = [
            {"name": item.name, "id": item.id} for item in sorted_items
        ]

        columns = ["name", "id"] if show_details else ["name"]
        utils_ui.print_entries_unix_style(
            sorted_items_dict, columns, header=show_details
        )

    if show_all or fab_state_config.get_config(fab_constant.FAB_SHOW_HIDDEN) == "true":
        utils_ui.print_grey("------------------------------")
        sorted_vic = sorted(VirtualItemContainerType, key=lambda vic: vic.value)
        for vic in sorted_vic:
            utils_ui.print_grey(vic.value)
