from __future__ import annotations

import enum
import typing

from typeguard import check_argument_types

from pydatapack import utils
from . import GamemodeEnum
from . import internal

__all__ = ["target", "TargetType"]


class TargetType:
    def __init__(self, char: str, kwargs: dict = None):
        self.character = char

        self._kwargs = kwargs or {}

    def __str__(self):
        ret = f"@{self.character}"
        if self._kwargs:
            ret += f"[{', '.join(f'{name}={internal.default_parser(value)}' for name, value in self._kwargs.items() if value is not None)}]"
        return ret

    def __call__(self, **kwargs):
        return TargetType(self.character, kwargs)


class _TargetEntitiesType(TargetType):
    @utils.call_and_return(TargetType.__call__)
    def __call__(self, *, x: float = None, y: float = None, z: float = None,
                 distance: float = None, dx: float = None, dy: float = None,
                 dz: float = None, scores: dict = None, tag: str = None,
                 team: typing.Union[str, bool] = None, limit: int = None, sort: 'target.sort' = None,
                 level: int = None, gamemode: GamemodeEnum = None, name: str = None,
                 x_rotation: float = None, y_rotation: float = None, type: str = None,
                 advancements: dict = None, nbt: dict = None):
        assert check_argument_types()


class _TargetPlayersType(TargetType):
    @utils.call_and_return(TargetType.__call__)
    def __call__(self, *, x: float = None, y: float = None, z: float = None,
                 distance: float = None, dx: float = None, dy: float = None,
                 dz: float = None, scores: dict = None, tag: str = None,
                 team: typing.Union[str, bool] = None, limit: int = None, sort: 'target.sort' = None,
                 level: int = None, gamemode: GamemodeEnum = None, name: str = None,
                 x_rotation: float = None, y_rotation: float = None, advancements: dict = None,
                 nbt: dict = None):
        assert check_argument_types()


class _TargetSingleType(TargetType):
    @utils.call_and_return(TargetType.__call__)
    def __call__(self, *, x: float = None, y: float = None, z: float = None,
                 distance: float = None, dx: float = None, dy: float = None,
                 dz: float = None, scores: dict = None, tag: str = None,
                 team: typing.Union[str, bool] = None, level: int = None, gamemode: GamemodeEnum = None,
                 name: str = None, x_rotation: float = None, y_rotation: float = None,
                 type: str = None, advancements: dict = None, nbt: dict = None):
        assert check_argument_types()


class target:
    class sort(enum.Enum):
        arbitrary = enum.auto()
        nearest = enum.auto()
        furthest = enum.auto()
        random = enum.auto()

    players = _TargetPlayersType('a')
    entities = _TargetEntitiesType('e')
    random = _TargetPlayersType('r')
    near = _TargetPlayersType('p')
    me = _TargetSingleType('s')

