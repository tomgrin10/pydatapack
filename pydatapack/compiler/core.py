import ast
import inspect
import itertools
from typing import *

import mcpack

from ..mc import internal


def parse_module_to_datapack(datapack: mcpack.DataPack, namespace_name: str, module):
    func_tuples = _parse_functions_from_module(module, namespace_name)
    for name, func in func_tuples:
        datapack[f"{namespace_name}:{name}"] = func


def _parse_functions_from_module(module, namespace_name: str) -> List[Tuple[str, mcpack.Function]]:
    source = inspect.getsource(module)
    file = inspect.getfile(module)
    compile(source, file, "exec")
    ast_obj = ast.parse(source, file)
    return MCParser(module, namespace_name).visit(ast_obj)


class MCParser(ast.NodeVisitor):
    def __init__(self, module, namespace_name):
        self._module = module
        self._namespace_name = namespace_name

        self._globals = self._module.__dict__
        self._locals = {}

    def _eval(self, node: ast.AST):
        try:
            code = compile(ast.Expression(node), inspect.getfile(self._module), "eval")
        except TypeError:
            exec(compile(ast.Interactive([node]), inspect.getfile(self._module), "single"), self._globals, self._locals)
        else:
            return eval(code, self._globals, self._locals)

    def _eval_and_get_commands(self, node: ast.AST, commands_join_str: str = '\n') -> str:
        """
        Evaluate node and return commands string generated by it.
        :param node: Node to evaluate.
        :param commands_join_str: String to place between commands.
        :return: A string containing a concatenation of gotten commands.
        """
        old_commands_count = len(internal.commands)
        self._eval(node)
        commands_str = commands_join_str.join(internal.commands[old_commands_count:])
        internal.commands = internal.commands[:old_commands_count]

        return commands_str

    def visit_Import(self, node: ast.Import):
        self._eval(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        self._eval(node)

    def generic_visit(self, node: Union[ast.AST, Sequence[ast.AST]]):
        """
        Called if no explicit visitor function exists for a node.
        """
        def helper():
            nodes = [node] if isinstance(node, ast.AST) else node

            for n in nodes:
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
        # If call to another function from module
        # example: function pack:bar
        if inspect.getmodule(func) == self._module:
            return f"function {self._namespace_name}:{func.__name__}\n"

        return self._eval_and_get_commands(node)

    def visit_Assign(self, node: ast.Assign):
        return self._eval_and_get_commands(node)

    def visit_With(self, node: ast.With):
        initial = ""
        # Evaluate 'with' expression items (not body)
        for item in node.items:
            initial += self._eval_and_get_commands(item.context_expr) + ' '
        initial += "run "

        return '\n'.join(initial + command for command in self.generic_visit(node.body).strip().split('\n')) + '\n'

    def visit_Delete(self, node: ast.Delete):
        return self._eval_and_get_commands(node)


