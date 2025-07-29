import json
from argparse import Namespace
from typing import Optional

from fabric_cli.client import fab_api_item as item_api
from fabric_cli.core.hiearchy.fab_hiearchy import VirtualItem
from fabric_cli.utils import fab_cmd_get_utils as utils_get
from fabric_cli.utils import fab_mem_store as utils_mem_store
from fabric_cli.utils import fab_util as utils


def exec(
    virtual_item: VirtualItem, args: Namespace, debug: Optional[bool] = True
) -> dict:
    item_name = utils.get_item_name_from_eds_name(virtual_item.name)
    args.item_id = utils_mem_store.get_item_id(virtual_item.workspace, item_name)

    args.ws_id = virtual_item.workspace.id
    args.id = virtual_item.id
    response = item_api.get_item_external_data_share(args)

    virtual_item_def = {}
    if response.status_code == 200:
        virtual_item_def = json.loads(response.text)
        utils_get.query_and_export(virtual_item_def, args, virtual_item.name, debug)

    return virtual_item_def
