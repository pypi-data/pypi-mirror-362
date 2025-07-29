# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

import json

from fabric_cli.core import fab_constant
from fabric_cli.core.fab_exceptions import FabricCLIError
from fabric_cli.utils import fab_ui as utils_ui


def load_json_from_path(file_path: str) -> dict:
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            return data

    except FileNotFoundError:
        utils_ui.print(f"The file at {file_path} was not found")
        raise FabricCLIError(
            f"The file at {file_path} was not found", fab_constant.ERROR_NOT_FOUND
        )

    except json.JSONDecodeError:
        utils_ui.print(f"The file at {file_path} is not a valid JSON file")
        raise FabricCLIError(
            f"The file at {file_path} is not a valid JSON file",
            fab_constant.ERROR_INVALID_JSON,
        )
