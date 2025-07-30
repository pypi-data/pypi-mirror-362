from .exec import ExecStatus as ExecStatus
from typing_extensions import TypeAlias

__all__ = ['ExecCommandsResult', 'ExecSingleCommandResult', 'DeviceToCommandToCommandOutputDict', 'DeviceToSingleCommandOutputDict', 'ExecStatus', 'ExecFailedError']

DeviceToCommandToCommandOutputDict: TypeAlias
ExecCommandsResult: TypeAlias
DeviceToSingleCommandOutputDict: TypeAlias
ExecSingleCommandResult: TypeAlias
ExecFailedError: TypeAlias
