from typing import Optional, Union

import typeguard

from pydatapack.mc import TargetType
from .. import internal

__all__ = ['Objective', 'Score']


@internal.class_options(replace_name="scoreboard objectives")
class Objective:
    def __init__(self, name: str):
        self.name = name

    @internal.generic_command(replace_name="{__name__} {self.name}")
    def add(self, criteria: str, display_name: Optional[str] = None):
        assert typeguard.check_argument_types()

    @internal.generic_command(replace_name="{__name__} {self.name}",
                              arg_parsers={"display_name": internal.json_parser})
    def remove(self, name: str, criteria: str, display_name: Optional[str] = None):
        assert typeguard.check_argument_types()

    @internal.generic_command(replace_name="{__name__} {slot} {self.name}")
    def setdisplay(self, slot: str):
        assert typeguard.check_argument_types()

    @internal.generic_command(replace_name="modify {self.name} displayname")
    def modify_display_name(self, display_name: str):
        assert typeguard.check_argument_types()

    @staticmethod
    @internal.generic_command(replace_name="scoreboard objectives {__name__}")
    def list():
        pass


@internal.class_options(replace_name="scoreboard players")
class Score:
    MAX_VALUE = 2_147_483_647
    MIN_VALUE = -2_147_483_648

    def __init__(self, entity: Union[TargetType, str], objective: Union[str, Objective]):
        assert typeguard.check_argument_types()

        self.entity = entity
        self.objective = objective

    @internal.generic_command(replace_name="{__name__} {self.entity} {self.objective}")
    def set(self, score: int):
        assert typeguard.check_argument_types()
        if not (self.MIN_VALUE <= score <= self.MAX_VALUE):
            raise internal.BadArgumentsError(f"amount needs to be between between {self.MIN_VALUE:n} and {self.MAX_VALUE:n},"
                                             f" inclusive.\n"
                                             f"Received: {score}")

    @internal.generic_command(replace_name="{__name__} {self.entity} {self.objective}")
    def add(self, amount: int):
        assert typeguard.check_argument_types()
        if not (0 <= amount <= self.MAX_VALUE):
            raise internal.BadArgumentsError(f"amount needs to be between between 0 and {self.MAX_VALUE:n}, inclusive.\n"
                                             f"Received: {amount}")

    __iadd__ = add

    @internal.generic_command(replace_name="{__name__} {self.entity} {self.objective}")
    def remove(self, amount: int):
        assert typeguard.check_argument_types()
        if not (0 <= amount <= self.MAX_VALUE):
            raise internal.BadArgumentsError(f"amount needs to be between between 0 and {self.MAX_VALUE:n}, inclusive.\n"
                                             f"Received: {amount}")

    subtract = remove
    __isub__ = remove

    @internal.generic_command(replace_name="{")
    def _operation(self, operation):
        pass

    @staticmethod
    @internal.generic_command(add_class_name=False,
                              replace_name="scoreboard players list")
    def list_tracked_entities():
        assert typeguard.check_argument_types()

    @staticmethod
    @internal.generic_command(add_class_name=False,
                              replace_name="scoreboard players list")
    def list_scores(entity: Union[TargetType, str]):
        assert typeguard.check_argument_types()
