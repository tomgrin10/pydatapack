from enum import Enum

import mc_parser
import core


class target:
    @staticmethod
    def _generic(char, **kwargs):
        if not kwargs:
            return f"@{char}"
        else:
            return f"@{char}[]"  # TODO

    @staticmethod
    def all(**kwargs):
        return target._generic('a', **kwargs)

    @staticmethod
    def enemy(**kwargs):
        return target._generic('e', **kwargs)

    @staticmethod
    def random(**kwargs):
        return target._generic('r', **kwargs)

    @staticmethod
    def near(**kwargs):
        return target._generic('p', **kwargs)

    @staticmethod
    def me(**kwargs):
        return target._generic('s', **kwargs)


def _generic_command(func):
    def decorator(*args, **kwargs):
        command = f"{func.__name__}"
        if args or kwargs:
            command += f" {' '.join(mc_parser.format_arg(arg) for arg in (list(args) + list(kwargs.values())) if arg is not None)}"
        return core.CommandNode(command.strip())
    return decorator


@_generic_command
def say(msg: str):
    pass


@_generic_command
def gamemode(mode: str, player: str = None):
    pass

