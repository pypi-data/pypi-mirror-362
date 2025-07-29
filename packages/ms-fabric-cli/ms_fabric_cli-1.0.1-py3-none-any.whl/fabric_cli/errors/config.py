# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

class ConfigErrors:
    @staticmethod
    def invalid_capacity(capacityName: str) -> str:
        return f"'{capacityName}' is not a valid capacity. Please provide a valid capacity name"

    @staticmethod
    def invalid_configuration_value(invalidValue: str, configurationKey: str, allowedValues: list[str]) -> str:
        return f"'{invalidValue}' is not a valid value for '{configurationKey}'. Allowed values are: {allowedValues}"

    @staticmethod
    def unknown_configuration_key(configurationKey: str) -> str:
        return f"'{configurationKey}' is not a recognized configuration key. Please check the available configuration keys"
