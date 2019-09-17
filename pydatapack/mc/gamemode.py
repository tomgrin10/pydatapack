import enum
from typing import Union

import typeguard

from pydatapack.mc import internal, _target

__all__ = ['gamemode', 'GamemodeEnum']


class GamemodeEnum(enum.Enum):
    survival = enum.auto()
    creative = enum.auto()
    adventure = enum.auto()
    spectator = enum.auto()
    _value = enum.auto()

    @internal.generic_command(ignore_args=['self'], replace_name='')
    def __call__(self, mode: 'GamemodeEnum', target: Union[_target, str] = None):
        assert typeguard.check_argument_types()


gamemode = GamemodeEnum._value
