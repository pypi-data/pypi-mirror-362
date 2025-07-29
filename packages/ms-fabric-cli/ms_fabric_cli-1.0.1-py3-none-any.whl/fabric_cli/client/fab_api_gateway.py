# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

from argparse import Namespace
from typing import Optional

from fabric_cli.client import fab_api_client as fabric_api
from fabric_cli.client import fab_api_utils as api_utils
from fabric_cli.client.fab_api_client import ApiResponse


def create_gateway(args: Namespace, payload: str) -> ApiResponse:
    """https://learn.microsoft.com/en-us/rest/api/fabric/core/gateways/create-gateway?tabs=HTTP"""
    args.uri = "gateways"
    args.method = "post"

    return fabric_api.do_request(args, data=payload)


def get_gateway(args: Namespace) -> ApiResponse:
    """https://learn.microsoft.com/en-us/rest/api/fabric/core/gateways/get-gateway?tabs=HTTP"""
    args.uri = f"gateways/{args.id}"
    args.method = "get"

    return fabric_api.do_request(args)


def update_gateway(args: Namespace, payload: str) -> ApiResponse:
    """https://learn.microsoft.com/en-us/rest/api/fabric/core/gateways/update-gateway?tabs=HTTP"""
    args.uri = f"gateways/{args.id}"
    args.method = "patch"

    return fabric_api.do_request(args, data=payload)


def delete_gateway(
    args: Namespace, bypass_confirmation: Optional[bool] = False
) -> bool:
    """https://learn.microsoft.com/en-us/rest/api/fabric/core/gateways/delete-gateway?tabs=HTTP"""
    args.uri = f"gateways/{args.id}"
    args.method = "delete"

    return api_utils.delete_resource(args, bypass_confirmation)


def list_gateways(args: Namespace) -> ApiResponse:
    """https://learn.microsoft.com/en-us/rest/api/fabric/core/gateways/list-gateways?tabs=HTTP"""
    args.uri = "gateways"
    args.method = "get"

    return fabric_api.do_request(args)


# Members


# def update_gateway_member(args: Namespace, payload: str) -> ApiResponse:
#     """https://learn.microsoft.com/en-us/rest/api/fabric/core/gateways/update-gateway-member?tabs=HTTP"""
#     args.uri = f"gateways/{args.id}/members/{args.member_id}"
#     args.method = "patch"

#     return fabric_api.do_request(args, data=payload)


# def list_gateway_members(args: Namespace) -> ApiResponse:
#     """https://learn.microsoft.com/en-us/rest/api/fabric/core/gateways/list-gateway-members?tabs=HTTP"""
#     args.uri = f"gateways/{args.id}/members"
#     args.method = "get"

#     return fabric_api.do_request(args)


# def delete_gateway_member(
#     args: Namespace, bypass_confirmation: Optional[bool] = False
# ) -> bool:
#     """https://learn.microsoft.com/en-us/rest/api/fabric/core/gateways/delete-gateway-member?tabs=HTTP"""
#     args.uri = f"gateways/{args.id}/members/{args.member_id}"
#     args.method = "delete"

#     return api_utils.delete_resource(args, bypass_confirmation)


# ACLs


def acl_list_from_gateway(args: Namespace) -> ApiResponse:
    """https://learn.microsoft.com/en-us/rest/api/fabric/core/gateways/list-gateway-role-assignments?tabs=HTTP"""
    args.uri = f"gateways/{args.gw_id}/roleAssignments"
    args.method = "get"

    return fabric_api.do_request(args)


# def acl_delete_from_gateway(args: Namespace) -> ApiResponse:
#     """https://learn.microsoft.com/en-us/rest/api/fabric/core/gateways/delete-gateway-role-assignment?tabs=HTTP"""
#     args.uri = f"gateways/{args.gw_id}/roleAssignments/{args.id}"
#     args.method = "delete"

#     return fabric_api.do_request(args)


# def acl_add_for_gateway(args: Namespace, payload: str) -> ApiResponse:
#     """https://learn.microsoft.com/en-us/rest/api/fabric/core/gateways/add-gateway-role-assignment?tabs=HTTP"""
#     args.uri = f"gateways/{args.gw_id}/roleAssignments"
#     args.method = "post"

#     return fabric_api.do_request(args, data=payload)


# def acl_update_for_gateway(args: Namespace, payload: str) -> ApiResponse:
#     """https://learn.microsoft.com/en-us/rest/api/fabric/core/gateways/update-gateway-role-assignment?tabs=HTTP"""
#     args.uri = f"gateways/{args.gw_id}/roleAssignments/{args.id}"
#     args.method = "patch"

#     return fabric_api.do_request(args, data=payload)


# def acl_get_for_gateway(args: Namespace) -> ApiResponse:
#     """https://learn.microsoft.com/en-us/rest/api/fabric/core/gateways/get-gateway-role-assignment?tabs=HTTP"""
#     args.uri = f"gateways/{args.gw_id}/roleAssignments/{args.id}"
#     args.method = "get"

#     return fabric_api.do_request(args)
