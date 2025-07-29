# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

import json
import re
from argparse import Namespace
from typing import Optional

from fabric_cli.client import fab_api_item as item_api
from fabric_cli.commands.fs.export import fab_fs_export_item as export_item
from fabric_cli.core import fab_constant, fab_state_config
from fabric_cli.core.fab_commands import Command
from fabric_cli.core.fab_exceptions import FabricCLIError
from fabric_cli.core.fab_types import ItemType, format_mapping
from fabric_cli.core.hiearchy.fab_hiearchy import FabricElement, Item, OneLakeItem


# General utils
def process_nargs(arg: str | list[str]) -> str:
    if isinstance(arg, list):
        return " ".join(arg).strip("\"'")
    return arg


def remove_dot_suffix(path: str, dot_string_to_rm: str = ".Shortcut") -> str:
    return path.replace(dot_string_to_rm, "").replace(dot_string_to_rm.lower(), "")


def obtain_id_names_for_onelake(
    from_context: OneLakeItem, to_context: OneLakeItem
) -> tuple:
    from_path_id, from_path_name = extract_paths(from_context)
    to_path_id, to_path_name = extract_paths(to_context)

    return from_path_id, from_path_name, to_path_id, to_path_name


def extract_paths(context: FabricElement) -> tuple:
    path_id = context.path_id.lstrip("/")
    path_name = context.path.lstrip("/")
    return path_id, path_name


def get_dict_from_params(params: str | list[str], max_depth: int = 2) -> dict:
    """
    Convert args to dict with a specified max nested level.
    Example:
    args.params = "key1.key2=value2,key1.key3=value3,key4=value4" -> {"key1": {"key2": "value2", "key3": "value3"}, "key4": "value4"}
    """

    params_dict: dict = {}
    # Split the params using a regular expression that matches a comma that is not inside a pair of quotes, brackets or braces
    # Example key1.key2=hello,key2={"hello":"testing","bye":2},key3=[1,2,3],key4={"key5":"value5"}
    # Result ['key1.key2=hello', 'key2={"hello":"testing","bye":2}', 'key3=[1,2,3]', 'key4={"key5":"value5"}']
    # Example key1.key2=hello
    # Result ['key1.key=hello']
    # TODO fix this to support key=value, key=value with spaces
    pattern = r"((?:[\w\.]+=.+?)(?=(?:,[\w\.]+=)|$))"

    if params:
        if isinstance(params, list):
            norm_params = " ".join(params)
        else:
            norm_params = params

        # Remove from multiline
        norm_params = norm_params.replace("\\", "").strip()

        matches = re.findall(pattern, norm_params)
        if not matches:
            raise FabricCLIError(
                f"Invalid parameter format: {norm_params}",
                fab_constant.ERROR_INVALID_INPUT,
            )

        params_dict = {}
        for param in matches:
            key, value = param.split("=", 1)
            params_dict = merge_dicts(
                params_dict, get_dict_from_parameter(key, value, max_depth)
            )

    return params_dict


def get_dict_from_parameter(
    param: str, value: str, max_depth: int = 2, current_depth: int = 1
) -> dict:
    """
    Convert args to dict with a specified max nested level.
    Example:
    param = key1.key2 and max_depth=2 -> {"key1": {"key2": value}}
    param = key1.key2 and max_depth=1 -> {"key1.key2": value}
    param = key1.key2.key3 and max_depth=2 -> {"key1": {"key2.key3": value}}
    """
    if max_depth != -1 and current_depth >= max_depth:
        return {param: value}

    if "." in param:
        key, rest = param.split(".", 1)
        return {key: get_dict_from_parameter(rest, value, max_depth, current_depth + 1)}
    else:
        clean_value = value.replace("'", "").replace('"', "")
        return {param: clean_value}


def merge_dicts(dict1: dict, dict2: dict) -> dict:
    """
    Merge two dictionaries.
    """
    if not dict1:
        return dict2
    if not dict2:
        return dict1

    for key, value in dict2.items():
        if key in dict1 and isinstance(value, dict):
            dict1[key] = merge_dicts(dict1[key], value)
        else:
            dict1[key] = value

    return dict1


def remove_keys_from_dict(_dict: dict, keys: list) -> dict:
    for key in keys:
        if key in _dict.keys():
            del _dict[key]
    return _dict


def sort_items_by_config(ws_items: list[Item]) -> list[Item]:
    if (
        fab_state_config.get_config(fab_constant.FAB_OUTPUT_ITEM_SORT_CRITERIA)
        == "bytype"
    ):
        return sorted(
            ws_items,
            key=lambda item: (str(item.item_type.name), item.short_name.lower()),
        )
    return sorted(ws_items, key=lambda item: item.short_name.lower())


# Item utils
def get_item_with_definition(
    item: Item,
    args: Namespace,
    decode: Optional[bool] = True,
    obtain_definition: bool = True,
) -> dict:

    args.force = True
    args.ws_id = item.workspace.id
    args.id = item.id
    args.item_uri = format_mapping.get(item.item_type, "items")

    if not obtain_definition:
        response = item_api.get_item(args, item_uri=True)
        item_def = json.loads(response.text)
    else:
        try:
            # Obtain item + definition
            item.check_command_support(Command.FS_EXPORT)
            item_def = export_item.export_single_item(
                item, args, do_export=False, decode=decode, item_uri=True
            )
        except FabricCLIError as e:
            # Fallback
            if e.status_code == fab_constant.ERROR_UNSUPPORTED_COMMAND:
                # Obtain item
                response = item_api.get_item(args, item_uri=True)
                item_def = json.loads(response.text)
            else:
                raise e

    return item_def


def get_capacity_settings(
    params: dict = {},
) -> tuple:

    az_subscription_id = params.get(
        "subscriptionid",
        fab_state_config.get_config(fab_constant.FAB_DEFAULT_AZ_SUBSCRIPTION_ID),
    )
    az_resource_group = params.get(
        "resourcegroup",
        fab_state_config.get_config(fab_constant.FAB_DEFAULT_AZ_RESOURCE_GROUP),
    )
    az_default_location = params.get(
        "location", fab_state_config.get_config(fab_constant.FAB_DEFAULT_AZ_LOCATION)
    )
    az_default_admin = params.get(
        "admin", fab_state_config.get_config(fab_constant.FAB_DEFAULT_AZ_ADMIN)
    )
    sku = params.get("sku", "F2")

    if not az_subscription_id:
        raise FabricCLIError(
            "Azure subscription ID is not set. Pass it with -P subscriptionId=<subscription_id> or set it with 'config set default_az_subscription_id <subscription_id>'",
            fab_constant.ERROR_INVALID_INPUT,
        )
    if not az_resource_group:
        raise FabricCLIError(
            "Azure resource group is not set. Pass it with -P resourceGroup=<resource_group> or set it with 'config set default_az_resource_group <resource_group>'",
            fab_constant.ERROR_INVALID_INPUT,
        )
    if not az_default_location:
        raise FabricCLIError(
            "Azure default location is not set. Pass it with -P location=<location> or set it with 'config set default_az_location <location>'",
            fab_constant.ERROR_INVALID_INPUT,
        )
    if not az_default_admin:
        raise FabricCLIError(
            "Azure default admin is not set. Pass it with -P admin=<admin> or set it with 'config set default_az_admin <admin>'",
            fab_constant.ERROR_INVALID_INPUT,
        )

    return (
        az_default_admin,
        az_default_location,
        az_subscription_id,
        az_resource_group,
        sku,
    )


def get_external_data_share_name(item_name: str, eds_id: str) -> str:
    return item_name + "_" + eds_id.split("-")[0]


def get_item_name_from_eds_name(eds_name) -> str:
    parts = eds_name.split("_")
    item_name = "_".join(parts[:-1])
    return item_name


def item_types_supporting_external_data_shares() -> list:
    return [ItemType.LAKEHOUSE, ItemType.KQL_DATABASE, ItemType.WAREHOUSE]


def replace_bypath_to_byconnection() -> bool:
    return True
