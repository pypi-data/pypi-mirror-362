# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

import os
import re
import sys

from fabric_cli.utils import fab_ui as utils_ui

# Define a regular expression for valid domains with wildcards
VALID_DOMAIN_REGEX = re.compile(
    r"^([\w-]+\.)?(fabric\.microsoft\.com|dfs\.fabric\.microsoft\.com|powerbi\.com|management\.[\w-]+\.[\w-]+)$"
)


def _validate_and_get_env_variable(env_var_name: str, default_value: str) -> str:
    value = os.environ.get(env_var_name, default_value)
    value = value.split("/")[0]  # Extract the domain part (before any path)

    if not VALID_DOMAIN_REGEX.match(value):
        utils_ui.print_error(f"Invalid domain for '{env_var_name}'")
        sys.exit(1)
    return value


# Endpoints
API_ENDPOINT_FABRIC = _validate_and_get_env_variable(
    "FAB_API_ENDPOINT_FABRIC", "api.fabric.microsoft.com"
)
API_VERSION_FABRIC = "v1"
API_ENDPOINT_ONELAKE = _validate_and_get_env_variable(
    "FAB_API_ENDPOINT_ONELAKE", "onelake.dfs.fabric.microsoft.com"
)
API_ENDPOINT_AZURE = _validate_and_get_env_variable(
    "FAB_API_ENDPOINT_AZURE", "management.azure.com"
)
API_ENDPOINT_POWER_BI = (
    _validate_and_get_env_variable("FAB_API_ENDPOINT_POWER_BI", "api.powerbi.com")
    + "/v1.0/myorg"
)

API_USER_AGENT = "ms-fabric-cli"
API_USER_AGENT_TEST = "ms-fabric-cli-test"
WEB_URI = "https://app.powerbi.com/groups"

# Versioning
FAB_VERSION = "1.0.1"  # change pyproject.toml version too, this must be aligned

# Scopes
SCOPE_FABRIC_DEFAULT = ["https://analysis.windows.net/powerbi/api/.default"]
SCOPE_ONELAKE_DEFAULT = ["https://storage.azure.com/.default"]
SCOPE_AZURE_DEFAULT = ["https://management.azure.com/.default"]

FABRIC_TOKEN_AUDIENCE = ["https://analysis.windows.net/powerbi/api"]
ONELAKE_TOKEN_AUDIENCE = ["https://storage.azure.com"]
AZURE_TOKEN_AUDIENCE = ["https://management.azure.com"]

# Auth
AUTH_DEFAULT_AUTHORITY = "https://login.microsoftonline.com/common"
AUTH_DEFAULT_CLIENT_ID = "5814bfb4-2705-4994-b8d6-39aabeb5eaeb"
AUTH_TENANT_AUTHORITY = "https://login.microsoftonline.com/"

# Env variables
FAB_TOKEN = "fab_token"
FAB_TOKEN_ONELAKE = "fab_token_onelake"
FAB_TOKEN_AZURE = "fab_token_azure"
FAB_SPN_CLIENT_ID = "fab_spn_client_id"
FAB_SPN_CLIENT_SECRET = "fab_spn_client_secret"
FAB_SPN_CERT_PATH = "fab_spn_cert_path"
FAB_SPN_CERT_PASSWORD = "fab_spn_cert_password"
FAB_SPN_FEDERATED_TOKEN = "fab_spn_federated_token"
FAB_TENANT_ID = "fab_tenant_id"

FAB_REFRESH_TOKEN = "fab_refresh_token"
IDENTITY_TYPE = "identity_type"
FAB_AUTH_MODE = "fab_auth_mode"  # Kept for backward compatibility
FAB_AUTHORITY = "fab_authority"

AUTH_KEYS = {
    FAB_TENANT_ID: [],
    IDENTITY_TYPE: ["user", "service_principal", "managed_identity"],
}

# Other constants
FAB_CAPACITY_NAME_NONE = "none"
FAB_DEFAULT_OPEN_EXPERIENCE_FABRIC = "fabric-developer"
FAB_DEFAULT_OPEN_EXPERIENCE_POWERBI = "power-bi"
FAB_DEFAULT_CAPACITY_ID = "fab_default_capacity_id"
FAB_MODE_INTERACTIVE = "interactive"
FAB_MODE_COMMANDLINE = "command_line"

# CLI settings
FAB_MODE = "mode"
FAB_CACHE_ENABLED = "cache_enabled"
FAB_DEBUG_ENABLED = "debug_enabled"
FAB_ENCRYPTION_FALLBACK_ENABLED = "encryption_fallback_enabled"
FAB_SHOW_HIDDEN = "show_hidden"
FAB_LOCAL_DEFINITION_LABELS = "local_definition_labels"
# FAB_LOCAL_COMMAND_YAML = "local_command_yaml"
FAB_DEFAULT_OPEN_EXPERIENCE = "default_open_experience"
FAB_DEFAULT_CAPACITY = "default_capacity"
FAB_DEFAULT_AZ_SUBSCRIPTION_ID = "default_az_subscription_id"
FAB_DEFAULT_AZ_RESOURCE_GROUP = "default_az_resource_group"
FAB_DEFAULT_AZ_LOCATION = "default_az_location"
FAB_DEFAULT_AZ_ADMIN = "default_az_admin"
FAB_JOB_CANCEL_ONTIMEOUT = "job_cancel_ontimeout"
FAB_OUTPUT_ITEM_SORT_CRITERIA = "output_item_sort_criteria"
# FAB_OUTPUT = "output"

CONFIG_KEYS = {
    FAB_CACHE_ENABLED: ["false", "true"],
    FAB_DEBUG_ENABLED: ["false", "true"],
    FAB_ENCRYPTION_FALLBACK_ENABLED: ["false", "true"],
    FAB_JOB_CANCEL_ONTIMEOUT: ["false", "true"],
    FAB_LOCAL_DEFINITION_LABELS: [],
    FAB_MODE: [FAB_MODE_INTERACTIVE, FAB_MODE_COMMANDLINE],
    FAB_OUTPUT_ITEM_SORT_CRITERIA: ["byname", "bytype"],
    FAB_SHOW_HIDDEN: ["false", "true"],
    # FAB_LOCAL_COMMAND_YAML: [],
    FAB_DEFAULT_AZ_SUBSCRIPTION_ID: [],
    FAB_DEFAULT_AZ_RESOURCE_GROUP: [],
    FAB_DEFAULT_AZ_LOCATION: [],
    FAB_DEFAULT_AZ_ADMIN: [],
    FAB_DEFAULT_CAPACITY: [],
    FAB_DEFAULT_OPEN_EXPERIENCE: ["fabric", "powerbi"],
    # Add more keys and their respective allowed values as needed
}

CONFIG_DEFAULT_VALUES = {
    FAB_MODE: FAB_MODE_COMMANDLINE,
    FAB_CACHE_ENABLED: "true",
    FAB_JOB_CANCEL_ONTIMEOUT: "true",
    FAB_DEBUG_ENABLED: "false",
    FAB_SHOW_HIDDEN: "false",
    FAB_ENCRYPTION_FALLBACK_ENABLED: "false",
    FAB_DEFAULT_OPEN_EXPERIENCE: "fabric",
    FAB_OUTPUT_ITEM_SORT_CRITERIA: "byname",
}

# Command descriptions
COMMAND_AUTH_DESCRIPTION = "Authenticate fab with Fabric."
COMMAND_FS_DESCRIPTION = "Workspace, item and file system operations."
COMMAND_JOBS_DESCRIPTION = "Manage tasks and jobs."
COMMAND_TABLES_DESCRIPTION = "Manage tables."
COMMAND_SHORTCUTS_DESCRIPTION = "Manage shorcuts."
COMMAND_ACLS_DESCRIPTION = "Manage permissions [admin]."
COMMAND_CONFIG_DESCRIPTION = "Manage configuration settings."
COMMAND_API_DESCRIPTION = "Make an authenticated API request."
COMMAND_EXTENSIONS_DESCRIPTION = "Manage extensions."
COMMAND_LABELS_DESCRIPTION = "Manage sensitivity labels [admin]."
COMMAND_CAPACITIES_DESCRIPTION = "(tenant) Manage capacities [admin]."
COMMAND_CONNECTIONS_DESCRIPTION = "(tenant) Manage connections."
COMMAND_DOMAINS_DESCRIPTION = "(tenant) Manage domains [admin]."
COMMAND_EXTERNAL_DATA_SHARES_DESCRIPTION = (
    "(tenant) Manage external data shares [admin]."
)
COMMAND_GATEWAYS_DESCRIPTION = "(tenant) Manage gateways."
COMMAND_FOLDERS_DESCRIPTION = "(workspace) Manage folders."
COMMAND_MANAGED_IDENTITIES_DESCRIPTION = "(workspace) Manage managed identities."
COMMAND_MANAGED_PRIVATE_ENDPOINTS_DESCRIPTION = (
    "(workspace) Manage managed private endpoints."
)
COMMAND_SPARK_POOLS_DESCRIPTION = "(workspace) Manage Apache Spark pools."
COMMAND_VARIABLES_DESCRIPTION = "(workspace) Manage variables."
COMMAND_DESCRIBE_DESCRIPTION = "Show commands supported by each Fabric element or path."

# Info
INFO_EXISTS_TRUE = "true"
INFO_EXISTS_FALSE = "false"
INFO_FEATURE_NOT_SUPPORTED = "Feature is not supported"

# Warnings
WARNING_INVALID_WORKSPACE_NAME = "Invalid workspace name"
WARNING_INVALID_ITEM_NAME = "Invalid item name"
WARNING_NOT_SUPPORTED_ITEM = "Not supported in this item type"
WARNING_DIFFERENT_ITEM_TYPES = "Different item types, review"
WARNING_INVALID_PATHS = (
    "Source and destination must be of the same type. Check your paths"
)
WARNING_INVALID_SPECIAL_CHARACTERS = (
    "Special caracters not supported for this item type"
)
WARNING_INVALID_LS_ONELAKE = "No more subdirectories supported for this item"
WARNING_INVALID_JSON_FORMAT = "Invalid JSON format"
WARNING_MKDIR_INVALID_ONELAKE = "Invalid paths. Only supported within /Files"
WARNING_OPERATION_NO_RESULT = "Long Running Operation returned no result"
WARNING_FABRIC_ADMIN_ROLE = "Requires Fabric admin role"
WARNING_ONELAKE_RBAC_ENABLED = "Requires data access roles enabled"
WARNING_NON_FABRIC_CAPACITY = "Not a Fabric capacity"
WARNING_ONLY_SUPPORTED_WITHIN_LAKEHOUSE = "Only supported within Lakehouse"
WARNING_ONLY_SUPPORTED_WITHIN_FILES_AND_TABLES = (
    "Only supported within Files/ and Tables/"
)

# Error codes

ERROR_ALREADY_EXISTS = "AlreadyExists"
ERROR_ALREADY_RUNNING = "AlreadyRunning"
ERROR_AUTHENTICATION_FAILED = "AuthenticationFailed"
ERROR_BAD_REQUEST = "BadRequest"
ERROR_CONFLICT = "Conflict"
ERROR_DUPLICATE_GATEWAY_NAME = "DuplicateGatewayName"
ERROR_ENCRYPTION_FAILED = "EncryptionFailed"
ERROR_FORBIDDEN = "Forbidden"
ERROR_INVALID_ACCESS_MODE = "InvalidAccessMode"
ERROR_INVALID_CERTIFICATE = "InvalidCertificate"
ERROR_INVALID_CERTIFICATE_PATH = "InvalidCertificatePath"
ERROR_INVALID_DEFINITION_PAYLOAD = "InvalidDefinitionPayload"
ERROR_INVALID_ELEMENT_TYPE = "InvalidElementType"
ERROR_INVALID_ENTRIES_FORMAT = "InvalidEntriesFormat"
ERROR_INVALID_FORMAT = "InvalidFormat"
ERROR_INVALID_GUID = "InvalidGuid"
ERROR_INVALID_INPUT = "InvalidInput"
ERROR_INVALID_ITEM_TYPE = "InvalidItemType"
ERROR_INVALID_JSON = "InvalidJson"
ERROR_INVALID_OPERATION = "InvalidOperation"
ERROR_INVALID_PATH = "InvalidPath"
ERROR_INVALID_PROPERTY = "InvalidProperty"
ERROR_INVALID_DETLA_TABLE = "InvalidDeltaTable"
ERROR_INVALID_WORKSPACE_TYPE = "InvalidWorkspaceType"
ERROR_INTERNAL_SERVER_ERROR = "InternalServerError"
ERROR_UNSUPPORTED_ITEM_TYPE = "UnsupportedItemType"
ERROR_UNSUPPORTED_COMMAND = "UnsupportedCommand"
ERROR_UNEXPECTED_ERROR = "UnexpectedError"
ERROR_ITEM_DISPLAY_NAME_ALREADY_IN_USE = "ItemDisplayNameAlreadyInUse"
ERROR_MAX_RETRIES_EXCEEDED = "MaxRetriesExceeded"
ERROR_NOT_FOUND = "NotFound"
ERROR_NOT_RUNNABLE = "NotRunnable"
ERROR_NOT_RUNNING = "NotRunning"
ERROR_NOT_SUPPORTED = "NotSupported"
ERROR_OPERATION_CANCELLED = "LongRunningOperationCancelled"
ERROR_OPERATION_FAILED = "LongRunningOperationFailed"
ERROR_UNAUTHORIZED = "Unauthorized"

# Exit codes
EXIT_CODE_SUCCESS = 0
EXIT_CODE_ERROR = 1
EXIT_CODE_CANCELLED_OR_MISUSE_BUILTINS = 2
EXIT_CODE_AUTHORIZATION_REQUIRED = 4

# Contextual commands
OS_COMMANDS = {
    "rm": {"windows": "del", "unix": "rm"},
    "ls": {"windows": "dir", "unix": "ls"},
    "mv": {"windows": "move", "unix": "mv"},
    "cp": {"windows": "copy", "unix": "cp"},
    "ln": {
        "windows": "mklink",
        "unix": "ln",
    },
    "clear": {
        "windows": "cls",
        "unix": "clear",
    },
}

# DEBUG
DEBUG = False


# Platform metadata
ITEM_METADATA_PROPERTIES = {
    "id",
    "type",
    "displayName",
    "description",
    "workspaceId",
    "folderId",
}
