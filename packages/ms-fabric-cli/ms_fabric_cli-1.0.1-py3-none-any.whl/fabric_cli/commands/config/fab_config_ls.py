# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

from argparse import Namespace

from fabric_cli.core import fab_constant, fab_state_config
from fabric_cli.utils import fab_ui as utils_ui


def exec_command(args: Namespace) -> None:
    configs = fab_state_config.list_configs()

    all_configs = [
        {"setting": key, "value": configs.get(key, "")}
        for key in fab_constant.CONFIG_KEYS
    ]

    columns = ["setting", "value"]
    utils_ui.print_entries_unix_style(all_configs, columns, header=True)
