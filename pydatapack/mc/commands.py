import enum as _enum
import typing as _t

from contextlib import contextmanager
import json as _json
from typeguard import check_argument_types

import pydatapack.utils as _utils
from .misc import _target


_commands: _t.List[str] = []


class CommandError(Exception):
    pass


def _to_json(arg) -> str:
    return _json.dumps(arg)


def _default_parser(arg) -> str:
    if isinstance(arg, _enum.Enum):
        return _utils.pascal_to_snake_case(arg.name).strip('_').replace('_', '-')
    if isinstance(arg, bool):
        return str(arg).lower()

    return str(arg)


def _generic_command(name: str = None,
                     generic: _t.Callable[[_t.Any], str] = _default_parser,
                     arg_parsers: _t.Dict[str, _t.Callable[[_t.Any], str]] = None,
                     ignore: _t.List[str] = None):
    """
    Decorator that creates command out of function definition.
    :param generic: Generic parser to use for parsing arguments instead of default parser
                    The default value is used as the default parser
    :param arg_parsers: Mapping of arguments to their parsers.
    :param ignore: List of arguments to ignore.
    :return:
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            unparsed_kwargs = {}
            if args or kwargs:
                arg_names = func.__code__.co_varnames
                # update with args
                unparsed_kwargs = {key: value for key, value in zip(arg_names[:len(args)], args) if value is not None}
                # update with kwargs
                unparsed_kwargs.update(dict(
                    sorted(
                        {k: v for k, v in kwargs.items() if v is not None}.items(),
                        key=lambda items: arg_names[len(args):].index(items[0]))))

            command = ""

            class_ = _utils.get_defining_class(func)
            if class_:
                command += _utils.pascal_to_snake_case(class_.__name__).strip('_').replace('_', '-') + ' '

            # Set command name
            final_name = func.__name__.strip('_').replace('_', '-')
            if name is not None:
                final_name = name.format(__name__=final_name, **unparsed_kwargs)
            if final_name:
                command += final_name + ' '

            default_arg_parser = _utils.get_arg_default(_generic_command, "generic")
            final_kwargs = {}
            for key, value in unparsed_kwargs.items():
                # Ignore argument
                if ignore and key in ignore:
                    continue

                manual_arg_parser = arg_parsers[key] if arg_parsers and arg_parsers.get(key) else lambda x: None
                final_kwargs[key] = manual_arg_parser(value) or generic(value) or default_arg_parser(value)

            # Set arguments
            command += ' '.join(final_kwargs.values())

            _commands.append(command.strip() + '\n')
            return func(*args, **kwargs)

        return wrapper
    return decorator


class advancement:
    class method(_enum.Enum):
        only = _enum.auto()
        until = _enum.auto()
        from_ = _enum.auto()
        through = _enum.auto()
        everything = _enum.auto()

    @staticmethod
    @_generic_command()
    def grant(target: _t.Union[_target, str], method: method, advancement: _t.Optional[str] = None, criterion: _t.Optional[str] = None):
        assert check_argument_types()

    @staticmethod
    @_generic_command()
    def revoke(target: _t.Union[_target, str], method: method, advancement: _t.Optional[str] = None, criterion: _t.Optional[str] = None):
        assert check_argument_types()


class Bossbar:
    def __init__(self, id: str, name: str = None):
        """
        :param name: If this is supplied the 'bossbar add' command is called.
        """
        self.id: str = id
        if name is not None:
            self._name = name
            self._color = "white"
            self._style = "progress"
            self._value = 0
            self._max = 100
            self._visible = True
            self._players = None
            self._add(name)

    @staticmethod
    @_generic_command()
    def list():
        pass

    @_generic_command(ignore=["self"], name="{__name__} {self.id}", arg_parsers={"name": _to_json})
    def _add(self, name: str):
        assert check_argument_types()

    @_generic_command(ignore=["self"], name="{__name__} {self.id}")
    def _set(self, setting: str, value: _t.Any):
        assert check_argument_types()
        setattr(self, f"_{setting}", value)

    def _get(self, setting: str):
        assert check_argument_types()
        value = getattr(self, f"_{setting}")
        if value:
            return value
        else:
            _commands.append(f"bossbar get {self.id} {setting}")

    @_generic_command(ignore=["self"], name="remove {self.id}")
    def __del__(self):
        pass

    @property
    def name(self) -> str:
        try:
            return self._name
        except AttributeError:
            raise CommandError("There is no 'bossbar get <id> name' command.")

    @name.setter
    def name(self, name: str):
        self._set("name", name)

    @property
    def color(self) -> str:
        try:
            return self._color
        except AttributeError:
            raise CommandError("There is no 'bossbar get <id> color' command.")

    @color.setter
    def color(self, color: str):
        self._set("color", color)

    @property
    def style(self) -> str:
        try:
            return self._style
        except AttributeError:
            raise CommandError("There is no 'bossbar get <id> style' command.")

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
    @contextmanager
    @_generic_command()
    def at(target: _t.Union[_target, str]):
        global _commands
        prev_commands = _commands
        _commands = []
        yield
        execute_str = prev_commands.pop().strip()
        prev_commands.append(''.join(f'{execute_str} run {command}' for command in _commands))
        _commands = prev_commands


class _gamemode(_enum.Enum):
    survival = _enum.auto()
    creative = _enum.auto()
    adventure = _enum.auto()
    spectator = _enum.auto()
    _value = _enum.auto()

    @_generic_command(ignore=['self'], name='')
    def __call__(self, mode: '_gamemode', target: _t.Union[_target, str] = None):
        assert check_argument_types()

gamemode = _gamemode._value


@_generic_command()
def msg(target: _t.Union[_target, str], msg: str):
    assert check_argument_types()
whisper = msg
tell = msg


@_generic_command()
def say(msg: str):
    assert check_argument_types()


@_generic_command()
def summon(entity: str):
    assert check_argument_types()


@_generic_command()
def tp(*args):
    assert check_argument_types()


