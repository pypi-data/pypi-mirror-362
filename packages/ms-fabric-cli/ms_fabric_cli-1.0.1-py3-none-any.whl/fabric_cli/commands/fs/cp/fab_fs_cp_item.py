# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

from argparse import Namespace

from fabric_cli.commands.fs import fab_fs_mv as fs_mv
from fabric_cli.core.hiearchy.fab_hiearchy import Item, Workspace


def cp_bulk_items(
    args: Namespace, from_context: Workspace, to_context: Workspace
) -> None:
    fs_mv._move_workspace_items_if_types_match(
        from_context, to_context, args, delete_from_item=False
    )


def cp_single_item(args: Namespace, from_context: Item, to_context: Item) -> None:
    fs_mv._move_item_if_types_match(
        from_context, to_context, args, delete_from_item=False
    )
