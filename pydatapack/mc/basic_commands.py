import enum
from typing import *

import typeguard

from . import internal
from . import TargetType

__all__ = ['advancement', 'Bossbar', 'execute', 'msg', 'whisper', 'tell', 'say', 'summon', 'tp']


class advancement:
    class method(enum.Enum):
        only = enum.auto()
        until = enum.auto()
        from_ = enum.auto()
        through = enum.auto()
        everything = enum.auto()

    @staticmethod
    @internal.generic_command()
    def grant(target: Union[TargetType, str], method: method, advancement: Optional[str] = None, criterion: Optional[str] = None):
        assert typeguard.check_argument_types()

    @staticmethod
    @internal.generic_command()
    def revoke(target: Union[TargetType, str], method: method, advancement: Optional[str] = None, criterion: Optional[str] = None):
        assert typeguard.check_argument_types()


class Bossbar:
    def __init__(self, id: str):
        self.id = id

    @staticmethod
    @internal.generic_command()
    def list():
        pass

    @internal.generic_command(ignore_args=["self"], replace_name="{__name__} {self.id}", arg_parsers={"name": internal.json_parser})
    def add(self, name: str):
        assert typeguard.check_argument_types()
        self._name = name
        self._color = "white"
        self._style = "progress"
        self._value = 0
        self._max = 100
        self._visible = True
        self._players = None

    @internal.generic_command(ignore_args=["self"], replace_name="{__name__} {self.id}")
    def _set(self, setting: str, value: Any):
        assert typeguard.check_argument_types()
        setattr(self, f"_{setting}", value)

    def _get(self, setting: str):
        assert typeguard.check_argument_types()
        value = getattr(self, f"_{setting}")
        if value:
            return value
        else:
            internal.commands.append(f"bossbar get {self.id} {setting}")

    @internal.generic_command(ignore_args=["self"], replace_name="remove {self.id}")
    def remove(self):
        pass

    @property
    def name(self) -> str:
        try:
            return self._name
        except AttributeError:
            raise internal.InvalidCommandError("There is no 'bossbar get <id> name' command.")

    @name.setter
    def name(self, name: str):
        self._set("name", name)

    @property
    def color(self) -> str:
        try:
            return self._color
        except AttributeError:
            raise internal.InvalidCommandError("There is no 'bossbar get <id> color' command.")

    @color.setter
    def color(self, color: str):
        self._set("color", color)

    @property
    def style(self) -> str:
        try:
            return self._style
        except AttributeError:
            raise internal.InvalidCommandError("There is no 'bossbar get <id> style' command.")

    @style.setter
    def style(self, style: str):
        self._set("style", style)

    @property
    def value(self) -> int:
        return self._get("value")

    @value.setter
    def value(self, value: int):
        self._set("value", value)

    @property
    def max(self) -> int:
        return self._get("max")

    @max.setter
    def max(self, max: int):
        self._set("max", max)

    @property
    def visible(self) -> bool:
        return self._get("visible")

    @visible.setter
    def visible(self, visible: bool):
        self._set("visible", visible)

    @property
    def players(self) -> str:
        return self._get("players")

    @players.setter
    def players(self, players: str):
        self._set("players", players)


class execute:
    @staticmethod
    @internal.generic_command()
    def at(target: Union[TargetType, str]):
        assert typeguard.check_argument_types()

    @staticmethod
    @internal.generic_command()
    def as_(target: Union[TargetType, str]):
        assert typeguard.check_argument_types()


@internal.generic_command()
def msg(target: Union[TargetType, str], msg: str):
    assert typeguard.check_argument_types()
whisper = msg
tell = msg


@internal.generic_command()
def say(msg: str):
    assert typeguard.check_argument_types()


@internal.generic_command()
def summon(entity: str):
    assert typeguard.check_argument_types()


@internal.generic_command()
def tp(*args):
    assert typeguard.check_argument_types()
