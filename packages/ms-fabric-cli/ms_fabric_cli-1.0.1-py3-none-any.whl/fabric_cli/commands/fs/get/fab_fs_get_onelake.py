import json
import os
from argparse import Namespace
from typing import Optional

from fabric_cli.client import fab_api_onelake as onelake_api
from fabric_cli.client import fab_api_shortcuts as shortcut_api
from fabric_cli.core.hiearchy.fab_hiearchy import OneLakeItem
from fabric_cli.utils import fab_cmd_get_utils as utils_get
from fabric_cli.utils import fab_util as utils


# OneLake - File and Folder
def onelake_resource(
    context: OneLakeItem, args: Namespace, debug: Optional[bool] = True
) -> dict:
    third_part = context.local_path
    workspace_id = context.workspace.id
    item_id = context.item.id

    args.directory = f"{workspace_id}/?recursive=false&resource=filesystem&directory={item_id}/{third_part}&getShortcutMetadata=true"
    response = onelake_api.list_tables_files_recursive(args)

    onelake_def = json.loads(response.text)
    onelake_def.pop("ContinuationToken", None)
    utils_get.query_and_export(onelake_def, args, third_part, debug)

    return onelake_def


# OneLake - Shortcut
def onelake_shortcut(
    shortcut: OneLakeItem, args: Namespace, debug: Optional[bool] = True
) -> dict:
    args.ws_id = shortcut.workspace.id
    args.id = shortcut.item.id
    args.path, name = os.path.split(shortcut.local_path.rstrip("/"))

    # Remove .Shortcut extension
    args.name = utils.remove_dot_suffix(name)

    # Obtain shortcut metadata
    response = shortcut_api.get_shortcut(args)

    shortcut_def = json.loads(response.text)
    utils_get.query_and_export(shortcut_def, args, shortcut.full_name, debug)

    return shortcut_def
