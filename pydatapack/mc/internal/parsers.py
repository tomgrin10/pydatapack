import enum
import json

from pydatapack import utils as utils

__all__ = ['json_parser', 'default_parser']


def json_parser(arg) -> str:
    return json.dumps(arg)


def default_parser(arg) -> str:
    if isinstance(arg, enum.Enum):
        return utils.pascal_to_snake_case(arg.name).strip('_').replace('_', '-')
    if isinstance(arg, bool):
        return str(arg).lower()

    return str(arg)