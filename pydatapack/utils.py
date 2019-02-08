import collections
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