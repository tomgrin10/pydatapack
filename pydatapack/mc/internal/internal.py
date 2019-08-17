import functools
from typing import List, Callable, Any, Dict, Optional

from ... import utils as utils
from .parsers import default_parser

__all__ = ['commands', 'generic_command', 'class_options']

commands: List[str] = []


DEFAULT_IGNORE_ARGS = ['self']


def generic_command(replace_name: Optional[str] = None,
                    default_parser: Callable[[Any], str] = default_parser,
                    arg_parsers: Optional[Dict[str, Callable[[Any], str]]] = None,
                    ignore_args: Optional[List[str]] = None,
                    add_class_name: bool = True):
    """
    Decorator that creates command out of function definition.
    :param replace_name: String to replace name of the command, function arguments are injected into it via format().
    :param default_parser: Generic parser to use for parsing arguments instead of default parser.
                           The default value is used as the default parser.
    :param arg_parsers: Mapping of arguments to their parsers.
    :param ignore_args: List of arguments to ignore.
    :param add_class_name: If to add the class name before the command or not.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return_value = func(*args, **kwargs)

            # Resolve parameters
            nonlocal ignore_args
            ignore_args = (ignore_args or []) + DEFAULT_IGNORE_ARGS

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

            if add_class_name:
                class_ = utils.get_defining_class(func)
                if class_:
                    command += utils.pascal_to_snake_case(class_.__name__).strip('_').replace('_', '-') + ' '

            # Set command name
            final_name = func.__name__.strip('_').replace('_', '-')
            if replace_name is not None:
                final_name = replace_name.format(__name__=final_name, **unparsed_kwargs)
            if final_name:
                command += final_name + ' '

            default_arg_parser = utils.get_arg_default(generic_command, "default_parser")
            final_kwargs = {}
            for key, value in unparsed_kwargs.items():
                # Ignore argument
                if ignore_args and key in ignore_args:
                    continue

                manual_arg_parser = arg_parsers[key] if arg_parsers and arg_parsers.get(key) else lambda x: None
                final_kwargs[key] = manual_arg_parser(value) or default_parser(value) or default_arg_parser(value)

            # Set arguments
            command += ' '.join(final_kwargs.values())

            commands.append(command.strip())
            return return_value

        return wrapper
    return decorator


def class_options(replace_name: Optional[str] = None):
    def decorator(orig_class):
        if replace_name:
            orig_class.__name__ = replace_name

        return orig_class
    return decorator
