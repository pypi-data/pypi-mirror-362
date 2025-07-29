# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

from argparse import Namespace

from fabric_cli.commands.fs.export import fab_fs_export_item as export_item
from fabric_cli.core.hiearchy.fab_hiearchy import FabricElement, Item, Workspace
from fabric_cli.utils import fab_util as utils
from fabric_cli.utils import fab_ui as utils_ui


def exec_command(args: Namespace, context: FabricElement) -> None:
    args.output = utils.process_nargs(args.output)

    if isinstance(context, Workspace):
        _check_for_sensitivity_label_warning(args)
        export_item.export_bulk_items(context, args)
    elif isinstance(context, Item):
        _check_for_sensitivity_label_warning(args)
        export_item.export_single_item(context, args)

def _check_for_sensitivity_label_warning(args: Namespace) -> None:
    if args.force:
        utils_ui.print_warning("Item definition is exported without its sensitivity label")
