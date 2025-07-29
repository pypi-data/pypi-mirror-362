# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

import json
from argparse import Namespace

from fabric_cli.client import fab_api_jobs as jobs_api
from fabric_cli.core import fab_constant
from fabric_cli.core.fab_exceptions import FabricCLIError
from fabric_cli.core.hiearchy.fab_hiearchy import Item
from fabric_cli.utils import fab_ui as utils_ui

"""
This function is used to execute the command for creating or updating a job schedule.

Examples of CronScheduleConfig:
{
  "startDateTime": "2024-04-28T00:00:00",
  "endDateTime": "2024-04-30T23:59:00",
  "localTimeZoneId": "Central Standard Time",
  "type": "Cron",
  "interval": 10
}
Example of DailyScheduleConfig
{
    "startDateTime": "2024-04-28T00:00:00",
    "endDateTime": "2024-04-30T23:59:00",
    "localTimeZoneId": "UTC",
    "type": "Daily",
    "times": ["00:00", "12:00"]
}
Example of WeeklyScheduleConfig
{
    "startDateTime": "2024-04-28T00:00:00",
    "endDateTime": "2024-04-30T23:59:00",
    "localTimeZoneId": "UTC",
    "type": "Weekly",
    "times": 10,
    "days": ["Monday", "Tuesday"]
}
"""


def exec_command(args: Namespace, context: Item) -> None:
    utils_ui.print_grey(f"Creating job schedule for '{args.item}'...")

    # Build the payload
    _configuration = json.loads(args.configuration)
    # Check if the _configuration already contains the schedule and enabled keys
    if "enabled" in _configuration and "configuration" in _configuration:
        payload = args.configuration
    else:
        # If the configuration only provides the schedule, add the enabled key
        payload = json.dumps({"configuration": _configuration, "enabled": args.enable})

    # Catch the special case for the EntityConflict => Cannot create a schedule for a job that is already scheduled
    try:
        response = jobs_api.create_item_schedule(args, payload)

        if response.status_code == 201:
            content = json.loads(response.text)
            instance_id = content["id"]

            utils_ui.print_done(f"Job schedule '{instance_id}' created")
    except FabricCLIError as e:
        if e.status_code == "EntityConflict":
            raise FabricCLIError(
                "Only one schedule per item is supported",
                fab_constant.ERROR_NOT_SUPPORTED,
            )
        else:
            raise e
