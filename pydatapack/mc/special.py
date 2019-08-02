from pydatapack.mc import internal


__all__ = ['command_unsafe']


def command_unsafe(command_str: str):
    internal.commands.append(command_str)
