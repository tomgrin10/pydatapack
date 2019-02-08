import ast
import inspect
import types
from pathlib import Path
from typing import *

import mcpack

import mc_parser
import test


def parse_module_to_datapack(datapack: mcpack.DataPack, namespace_name: str, module):
    func_tuples = _parse_module(module, namespace_name)
    for name, func in func_tuples:
        datapack[f"{namespace_name}:{name}"] = func


def _parse_module(module, namespace_name: str) -> List[Tuple[str, mcpack.Function]]:
    source = inspect.getsource(module)
    file = inspect.getfile(module)
    compile(source, file, "exec")
    ast_obj = ast.parse(source, file)
    Simplifier(module).visit(ast_obj)
    return MCParser(namespace_name).visit(ast_obj)


class CommandNode(ast.AST):
    def __init__(self, command):
        self.data = command


class Simplifier(ast.NodeTransformer):
    """
    Simplifies the whole tree so it would be easier to read later.
    """
    def __init__(self, module):
        self._module = module

        self._globals = self._module.__dict__

    def _eval(self, node):
        return eval(compile(ast.Expression(node), "ast", "eval"), self._globals, {})

    def _exec(self, node):
        exec(compile(ast.Interactive([node]), "ast", "single"), self._globals, {})

    def visit_Call(self, node):
        self.generic_visit(node)
        # Replace function node with function pointer
        node.func = self._eval(node.func)
        # If call to function outside module evaluate
        if inspect.getmodule(node.func) != self._module:
            return node.func(*(self._eval(arg) for arg in node.args))

        return node


class MCParser(ast.NodeVisitor):
    def __init__(self, namespace_name: str):
        self._ns_name = namespace_name

    def generic_visit(self, node):
        """Called if no explicit visitor function exists for a node."""
        def helper():
            for field, value in ast.iter_fields(node):
                if isinstance(value, list):
                    for item in value:
                        if isinstance(item, ast.AST):
                            yield self.visit(item)
                elif isinstance(value, ast.AST):
                    yield self.visit(value)

        for ret in helper():
            if isinstance(ret, types.GeneratorType):
                yield from ret
            elif ret:
                yield ret

    def visit_Module(self, node: ast.Module) -> List[Tuple[str, mcpack.Function]]:
        return list(self.generic_visit(node))

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Tuple[str, mcpack.Function]:
        """Returns a tuple containing the function name and list of mc commands"""
        func_str = ""

        docstring = ast.get_docstring(node)
        if docstring:
            func_str += '\n'.join(f'# {line}' for line in docstring.split('\n')) + '\n\n'

        commands = self.generic_visit(node)
        if commands:
            func_str += ('\n'.join(commands))

        return node.name, mcpack.Function(func_str)

    def visit_CommandNode(self, node: CommandNode):
        return node.data

    def visit_Call(self, node):
        return f"function {self._ns_name}:{node.func.__name__}"


if __name__ == "__main__":
    pack = mcpack.DataPack("Pack", "Description")
    parse_module_to_datapack(pack, "pack", test)

    pack.dump(
        Path.home() / r"AppData\Roaming\.minecraft\saves\Superflat Testing\datapacks",
        overwrite=True)



