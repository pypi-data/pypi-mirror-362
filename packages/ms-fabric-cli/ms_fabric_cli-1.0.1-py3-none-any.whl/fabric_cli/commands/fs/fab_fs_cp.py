# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

from argparse import Namespace

from fabric_cli.commands.fs.cp import fab_fs_cp_item as cp_item
from fabric_cli.commands.fs.cp import fab_fs_cp_onelake as cp_onelake
from fabric_cli.core import fab_constant
from fabric_cli.core.fab_exceptions import FabricCLIError
from fabric_cli.core.hiearchy.fab_hiearchy import (
    FabricElement,
    Item,
    LocalPath,
    OneLakeItem,
    Workspace,
)
from fabric_cli.utils import fab_ui as utils_ui


def exec_command(
    args: Namespace, from_context: FabricElement, to_context: FabricElement
) -> None:
    args.from_path, args.to_path = from_context.path, to_context.path

    # Workspaces
    if isinstance(from_context, Workspace) and isinstance(to_context, Workspace):
        _check_for_sensitivity_label_warning(args)
        cp_item.cp_bulk_items(args, from_context, to_context)

    # Items
    elif isinstance(from_context, Item) and isinstance(to_context, Item):
        _check_for_sensitivity_label_warning(args)
        cp_item.cp_single_item(args, from_context, to_context)

    # OneLake to OneLake
    elif isinstance(from_context, OneLakeItem) and isinstance(to_context, OneLakeItem):
        cp_onelake.copy_onelake_2_onelake(from_context, to_context, args)

    # Local to OneLake
    elif isinstance(from_context, LocalPath) and isinstance(to_context, OneLakeItem):
        cp_onelake.copy_local_2_onelake(from_context, to_context, args)

    # OneLake to Local
    elif isinstance(from_context, OneLakeItem) and isinstance(to_context, LocalPath):
        cp_onelake.copy_onelake_2_local(from_context, to_context, args)

    # Source and target items must be same types
    elif from_context.type != to_context.type:
        raise FabricCLIError(
            fab_constant.WARNING_INVALID_PATHS, fab_constant.ERROR_INVALID_INPUT
        )

    else:
        raise FabricCLIError(
            fab_constant.WARNING_INVALID_PATHS, fab_constant.ERROR_NOT_SUPPORTED
        )

def _check_for_sensitivity_label_warning(args: Namespace) -> None:
    if args.force:
        utils_ui.print_warning("Item definition is copied without its sensitivity label")
