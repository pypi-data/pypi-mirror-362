# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

from fabric_cli.core.fab_auth import FabAuth
from fabric_cli.core.fab_types import FabricElementType
from fabric_cli.core.hiearchy.fab_element import FabricElement
from fabric_cli.core.hiearchy.fab_tenant import Tenant
from fabric_cli.utils import fab_ui as utils_ui


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@singleton
class Context:
    def __init__(self):
        # Initialize the context
        self._context: FabricElement = None
        self._command: str = None

    @property
    def context(self) -> FabricElement:
        if self._context is None:
            self.load_context()
        return self._context

    @context.setter
    def context(self, context: FabricElement) -> None:
        self._context = context

    @property
    def command(self) -> str:
        return self._command

    @command.setter
    def command(self, command: str) -> None:
        self._command = command

    def load_context(self) -> None:
        self.context = FabAuth().get_tenant()

    def reset_context(self) -> None:
        self.context = self.context.tenant

    def print_context(self) -> None:
        utils_ui.print_grey(str(self.context))

    # Tenant

    def get_tenant(self) -> Tenant:
        assert isinstance(self.context.tenant, Tenant)
        return self.context.tenant

    def get_tenant_id(self) -> str:
        return self.get_tenant().id
