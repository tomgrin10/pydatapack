import enum
from typing import Union

import typeguard

from pydatapack.mc import internal, TargetType

__all__ = ['gamemode', 'GamemodeType']


class GamemodeType(enum.Enum):
    survival = enum.auto()
    creative = enum.auto()
    adventure = enum.auto()
    spectator = enum.auto()
    _value = enum.auto()

    @internal.generic_command(ignore_args=['self'], replace_name='')
    def __call__(self, mode: 'GamemodeType', target: Union[TargetType, str] = None):
        assert typeguard.check_argument_types()


gamemode = GamemodeType._value
