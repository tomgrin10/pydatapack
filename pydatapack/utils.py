import collections
import inspect
import re
from typing import *


class defaultdict(collections.defaultdict):
    def __missing__(self, key):
        try:
            super().__missing__(key)
        except:
            ret = self[key] = self.default_factory(key)
            return ret


def extension(cls: Union[type, Sequence[type]], name: str = None):
    def decorator(func: Callable):
        nonlocal cls
        if isinstance(cls, type):
            cls = (cls,)

        for c in cls:
            setattr(c, name or func.__name__, func)

    return decorator


def get_arg_default(func, arg_name):
    return inspect.signature(func).parameters[arg_name].default


def get_arg_annotation(func, arg_name):
    ret = inspect.signature(func).parameters[arg_name].annotation
    if ret == inspect.Parameter.empty:
        return None
    return ret


def get_defining_class(method):
    if inspect.ismethod(method):
        for cls in inspect.getmro(method.__self__.__class__):
            if cls.__dict__.get(method.__name__) is method and inspect.isclass(cls):
                return cls
    if inspect.isfunction(method):
        cls = getattr(inspect.getmodule(method),
                      method.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0])
        if inspect.isclass(cls):
            return cls


def pascal_to_snake_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def return_call(to_call):
    def decorator(func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            return to_call(*args, **kwargs)
        return wrapper
    return decorator


