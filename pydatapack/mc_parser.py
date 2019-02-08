import ast
from typing import *


def format_arg(arg: Any) -> str:
    if isinstance(arg, str):
        return arg


def construct_command(obj: ast.Call) -> str:
    return f"{obj.func.__name__} {' '.join(format_arg(arg) for arg in obj.args)}"
