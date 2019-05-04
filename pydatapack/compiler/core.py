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
    return MCParser(module, namespace_name).visit(ast_obj)


class MCParser(ast.NodeVisitor):
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
            nonlocal node
            if isinstance(node, ast.AST):
                node = [node]

            for n in node:
                for field, value in ast.iter_fields(n):
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

        n = len(mc.internal.commands)
        self._eval(node)
        if len(mc.internal.commands) > n:
            return mc.internal.commands.pop() + '\n'

    def visit_Assign(self, node: ast.Assign):
        n = len(mc.internal.commands)
        self._eval(node)
        if len(mc.internal.commands) > n:
            return mc.internal.commands.pop() + '\n'

    def visit_With(self, node: ast.With):
        initial = ""
        for item in node.items:
            n = len(mc.internal.commands)
            self._eval(item.context_expr)
            if len(mc.internal.commands) > n:
                initial += mc.internal.commands.pop() + ' '
        initial += "run "

        return '\n'.join(initial + command for command in self.generic_visit(node.body).strip().split('\n')) + '\n'

    def visit_Delete(self, node: ast.Delete):
        n = len(mc.internal.commands)
        self._eval(node)
        if len(mc.internal.commands) > n:
            return mc.internal.commands.pop() + '\n'


