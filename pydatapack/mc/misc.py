import enum
import typing

from pydatapack import utils
import pydatapack.mc.commands as commands
from typeguard import check_argument_types

__all__ = ["target"]


class _target():
    def __init__(self, char: str, kwargs: dict = None):
        self.char = char

        self.kwargs = kwargs or {}

    def __str__(self):
        ret = f"@{self.char}"
        if self.kwargs:
            ret += f"[{', '.join(f'{name}={commands._default_parser(value)}' for name, value in self.kwargs.items() if value is not None)}]"
        return ret

    def __call__(self, **kwargs):
        return _target(self.char, kwargs)


class _target_entities(_target):
    @utils.return_call(_target.__call__)
    def __call__(self, *, x: float = None, y: float = None, z: float = None,
                 distance: float = None, dx: float = None, dy: float = None,
                 dz: float = None, scores: dict = None, tag: str = None,
                 team: typing.Union[str, bool] = None, limit: int = None, sort: 'target.sorting' = None,
                 level: int = None, gamemode: 'commands._gamemode' = None, name: str = None,
                 x_rotation: float = None, y_rotation: float = None, type: str = None,
                 advancements: dict = None, nbt: dict = None):
        assert check_argument_types()


class _target_players(_target):
    @utils.return_call(_target.__call__)
    def __call__(self, *, x: float = None, y: float = None, z: float = None,
                 distance: float = None, dx: float = None, dy: float = None,
                 dz: float = None, scores: dict = None, tag: str = None,
                 team: typing.Union[str, bool] = None, limit: int = None, sort: 'target.sorting' = None,
                 level: int = None, gamemode: 'commands._gamemode' = None, name: str = None,
                 x_rotation: float = None, y_rotation: float = None, advancements: dict = None,
                 nbt: dict = None):
        assert check_argument_types()


class _target_one(_target):
    @utils.return_call(_target.__call__)
    def __call__(self, *, x: float = None, y: float = None, z: float = None,
                 distance: float = None, dx: float = None, dy: float = None,
                 dz: float = None, scores: dict = None, tag: str = None,
                 team: typing.Union[str, bool] = None, level: int = None, gamemode: 'commands._gamemode' = None,
                 name: str = None, x_rotation: float = None, y_rotation: float = None,
                 type: str = None, advancements: dict = None, nbt: dict = None):
        assert check_argument_types()


class target:
    class sorting(enum.Enum):
        arbitrary = enum.auto()
        nearest = enum.auto()
        furthest = enum.auto()
        random = enum.auto()

    players = _target_players('a')
    entities = _target_entities('e')
    random = _target_players('r')
    near = _target_players('p')
    me = _target_one('s')

