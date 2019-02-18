import ast
import inspect
import types
from typing import *

import mcpack

import pydatapack.mc.commands as mc


def parse_module_to_datapack(datapack: mcpack.DataPack, namespace_name: str, module):
    func_tuples = _parse_module(module, namespace_name)
    for name, func in func_tuples:
        datapack[f"{namespace_name}:{name}"] = func


def _parse_module(module, namespace_name: str) -> List[Tuple[str, mcpack.Function]]:
    source = inspect.getsource(module)
    file = inspect.getfile(module)
    compile(source, file, "exec")
    ast_obj = ast.parse(source, file)
    return Simplifier(module, namespace_name).visit(ast_obj)


class CommandNode(ast.Str):
    pass


class Simplifier(ast.NodeVisitor):
    """
    Simplifies the whole tree so it would be easier to read later.
    """
    def __init__(self, module, namespace_name):
        self._module = module
        self._ns_name = namespace_name

        self._globals = self._module.__dict__
        self._locals = {}

    def _eval(self, node):
        try:
            code = compile(ast.Expression(node), inspect.getfile(self._module), "eval")
        except TypeError:
            exec(compile(ast.Interactive([node]), inspect.getfile(self._module), "single"), self._globals, self._locals)
        else:
            return eval(code, self._globals, self._locals)

    def visit_Import(self, node: ast.Import):
        self._eval(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        self._eval(node)

    def generic_visit(self, node):
        """Called if no explicit visitor function exists for a node."""
        def helper():
            for field, value in ast.iter_fields(node):
                if isinstance(value, list):
                    for item in value:
                        if isinstance(item, ast.AST):
                            ret = self.visit(item)
                            if ret:
                                yield ret
                elif isinstance(value, ast.AST):
                    ret = self.visit(value)
                    if ret:
                        yield ret

        ret_list = list(helper())
        if ret_list:
            if isinstance(ret_list[0], str):
                return ''.join(ret_list)
            if isinstance(ret_list[0], tuple):
                return ret_list

    def visit_Module(self, node: ast.Module) -> List[Tuple[str, mcpack.Function]]:
        return self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Tuple[str, mcpack.Function]:
        self._locals = {}

        func_str = ""
        docstring = ast.get_docstring(node)
        if docstring:
            func_str = '\n'.join(f'# {line}' for line in docstring.split('\n')) + '\n\n'

        commands = self.generic_visit(node)
        if commands:
            func_str += commands

        return node.name, mcpack.Function(func_str.strip() + '\n')

    def visit_Call(self, node: ast.Call):
        func = self._eval(node.func)
        if inspect.getmodule(func) == self._module:
            # Replace function node with function pointer
            return f"function {self._ns_name}:{func.__name__}\n"

        self._eval(node)
        if mc._commands:
            return mc._commands.pop()

    def visit_Assign(self, node: ast.Assign):
        self._eval(node)
        if mc._commands:
            return mc._commands.pop()

    def visit_With(self, node: ast.With):
        self._eval(node)
        if mc._commands:
            return mc._commands.pop()

    def visit_Delete(self, node: ast.Delete):
        self._eval(node)
        if mc._commands:
            return mc._commands.pop()


