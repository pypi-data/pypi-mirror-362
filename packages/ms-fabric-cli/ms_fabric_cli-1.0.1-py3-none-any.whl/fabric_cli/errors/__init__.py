# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

from .common import CommonErrors
from .config import ConfigErrors
from .labels import LabelsErrors
from .mkdir import MkdirErrors
from .start_stop import StartStopErrors
from .auth import AuthErrors

class ErrorMessages:
    Common = CommonErrors
    Config = ConfigErrors
    Labels = LabelsErrors
    Mkdir = MkdirErrors
    StartStop = StartStopErrors
    Auth = AuthErrors
    # Add more error classes as needed
