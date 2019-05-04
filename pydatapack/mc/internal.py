import enum
import json
from typing import List, Callable, Any, Dict

from pydatapack import utils as utils


commands: List[str] = []


class CommandError(Exception):
    pass


def to_json(arg) -> str:
    return json.dumps(arg)


def default_parser(arg) -> str:
    if isinstance(arg, enum.Enum):
        return utils.pascal_to_snake_case(arg.name).strip('_').replace('_', '-')
    if isinstance(arg, bool):
        return str(arg).lower()

    return str(arg)


def generic_command(name: str = None,
                    generic: Callable[[Any], str] = default_parser,
                    arg_parsers: Dict[str, Callable[[Any], str]] = None,
                    ignore: List[str] = None):
    """
    Decorator that creates command out of function definition.
    :param name: Name of the command.
    :param generic: Generic parser to use for parsing arguments instead of default parser
                    The default value is used as the default parser
    :param arg_parsers: Mapping of arguments to their parsers.
    :param ignore: List of arguments to ignore.
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

            class_ = utils.get_defining_class(func)
            if class_:
                command += utils.pascal_to_snake_case(class_.__name__).strip('_').replace('_', '-') + ' '

            # Set command name
            final_name = func.__name__.strip('_').replace('_', '-')
            if name is not None:
                final_name = name.format(__name__=final_name, **unparsed_kwargs)
            if final_name:
                command += final_name + ' '

            default_arg_parser = utils.get_arg_default(generic_command, "generic")
            final_kwargs = {}
            for key, value in unparsed_kwargs.items():
                # Ignore argument
                if ignore and key in ignore:
                    continue

                manual_arg_parser = arg_parsers[key] if arg_parsers and arg_parsers.get(key) else lambda x: None
                final_kwargs[key] = manual_arg_parser(value) or generic(value) or default_arg_parser(value)

            # Set arguments
            command += ' '.join(final_kwargs.values())

            commands.append(command.strip())
            return func(*args, **kwargs)

        return wrapper
    return decorator
