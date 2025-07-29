# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

from argparse import Namespace
from typing import Optional

from fabric_cli.commands.fs.mv import fab_fs_mv_item as mv_item
from fabric_cli.commands.fs.mv import fab_fs_mv_onelake as mv_onelake
from fabric_cli.core import fab_constant
from fabric_cli.core.fab_exceptions import FabricCLIError
from fabric_cli.core.hiearchy.fab_hiearchy import (
    FabricElement,
    Item,
    OneLakeItem,
    Workspace,
)
from fabric_cli.utils import fab_ui as utils_ui


def exec_command(
    args: Namespace, from_context: FabricElement, to_context: FabricElement
) -> None:
    args.from_path = from_context.path
    args.to_path = to_context.path

    if from_context.type == to_context.type:
        if isinstance(from_context, Workspace) and isinstance(to_context, Workspace):
            _check_for_sensitivity_label_warning(args)
            _move_workspace_items_if_types_match(from_context, to_context, args)
        elif isinstance(from_context, Item) and isinstance(to_context, Item):
            _check_for_sensitivity_label_warning(args)
            _move_item_if_types_match(from_context, to_context, args)
        elif isinstance(from_context, OneLakeItem) and isinstance(
            to_context, OneLakeItem
        ):
            mv_onelake.move_onelake_file(from_context, to_context, args)
    else:
        raise FabricCLIError(
            fab_constant.WARNING_INVALID_PATHS, fab_constant.ERROR_INVALID_INPUT
        )


# Workspace Items (not workspace itself, multi-item selection)
def _move_workspace_items_if_types_match(
    from_context: Workspace,
    to_context: Workspace,
    args: Namespace,
    delete_from_item: Optional[bool] = True,
) -> None:
    wstype_from = from_context.ws_type
    wstype_to = to_context.ws_type

    if wstype_from == wstype_to:
        mv_item.move_bulk_items(
            from_context, to_context, args, delete_from_item=delete_from_item
        )
    else:
        raise FabricCLIError(
            fab_constant.WARNING_DIFFERENT_ITEM_TYPES, fab_constant.ERROR_INVALID_INPUT
        )


# Items
def _move_item_if_types_match(
    from_context: Item,
    to_context: Item,
    args: Namespace,
    delete_from_item: Optional[bool] = True,
) -> None:
    if from_context.item_type == to_context.item_type:
        mv_item.move_single_item(
            from_context, to_context, args, delete_from_item=delete_from_item
        )
    else:
        raise FabricCLIError(
            fab_constant.WARNING_DIFFERENT_ITEM_TYPES, fab_constant.ERROR_INVALID_INPUT
        )

def _check_for_sensitivity_label_warning(args: Namespace) -> None:
    if args.force:
        utils_ui.print_warning("Item definition is moved without its sensitivity label")
