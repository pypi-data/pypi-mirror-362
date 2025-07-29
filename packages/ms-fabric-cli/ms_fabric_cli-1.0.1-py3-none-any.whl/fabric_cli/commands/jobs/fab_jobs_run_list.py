# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

import json
from argparse import Namespace

from fabric_cli.client import fab_api_jobs as jobs_api
from fabric_cli.core.hiearchy.fab_hiearchy import Item
from fabric_cli.utils import fab_ui as utils_ui


def exec_command(args: Namespace, context: Item) -> None:
    if args.schedule:
        response = jobs_api.list_item_schedules(args)
    else:
        response = jobs_api.list_item_runs(args)

    if response.status_code == 200:
        data = json.loads(response.text)

        if data["value"]:
            _keys = (
                data["value"][0].keys()
                if isinstance(data["value"], list)
                else data["value"].keys()
            )
            utils_ui.print_entries_unix_style(data["value"], _keys, header=True)
        else:
            if args.schedule:
                utils_ui.print_done("No schedules found")
            else:
                utils_ui.print_done("No runs found")
