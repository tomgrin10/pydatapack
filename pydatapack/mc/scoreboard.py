from typing import *

import typeguard

import pydatapack.mc.target as target
import pydatapack.mc.internal as internal


__all__ = []


class Objective:
    def __init__(self, name: str):
        self.name = name

    @internal.generic_command(ignore=['self'])
    def add(self, criteria: str, display_name: Optional[str] = None):
        assert typeguard.check_argument_types()

    @internal.generic_command(ignore=['self'])
    def remove(self, name: str, criteria: str, display_name: Optional[str] = None):
        assert typeguard.check_argument_types()

    @staticmethod
    @internal.generic_command()
    def list():
        pass


class players:
    pass
