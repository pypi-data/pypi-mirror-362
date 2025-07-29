# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

from typing import Union

from fabric_cli.core.fab_types import FabricElementType
from fabric_cli.core.hiearchy.fab_element import FabricElement
from fabric_cli.core.hiearchy.fab_tenant import Tenant
from fabric_cli.core.hiearchy.fab_workspace import Workspace


class Folder(FabricElement):

    # The parent of a folder is either a workspace or another folder
    def __init__(self, name, id, parent: Union[Workspace, 'Folder']):
        super().__init__(name, id, FabricElementType.FOLDER, parent)

    def __eq__(self, value) -> bool:
        if not isinstance(value, Folder):
            return False
        return super().__eq__(value)

    @property
    def parent(self) -> Union[Workspace, 'Folder']:
        _parent = super().parent
        assert isinstance(_parent, Workspace) or isinstance(_parent, Folder)
        return _parent

    @property
    def path(self) -> str:
        return self.parent.path + "/" + self.name

    @property
    def tenant(self) -> Tenant:
        return self.parent.tenant

    @property
    def workspace(self) -> Workspace:
        if isinstance(self.parent, Workspace):
            return self.parent
        elif isinstance(self.parent, Folder):
            return self.parent.workspace
