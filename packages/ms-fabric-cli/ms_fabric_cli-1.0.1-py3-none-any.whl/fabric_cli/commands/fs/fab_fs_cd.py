# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

from argparse import Namespace

from fabric_cli.core.fab_context import Context
from fabric_cli.core.hiearchy.fab_hiearchy import FabricElement, Tenant
from fabric_cli.utils import fab_ui as utils_ui


def exec_command(args: Namespace, context: FabricElement) -> None:
    _change_context(context)


def _change_context(context: FabricElement) -> None:
    Context().context = context
    if isinstance(context, Tenant):
        utils_ui.print_done("Switched to root")
    else:
        utils_ui.print_done(f"Switched to '{context.name}'")
