from typing import *

import astroid as ast

from pygolf.name_finder import NameFinder
from pygolf.optimizers.optimizer import Optimizer
from pygolf.rules import *

_builtin_methods = __builtins__.keys()  # type: ignore


class RenameMethodOptimizer(Optimizer):
    def __init__(self, name_finder: NameFinder) -> None:
        self.standard_methods: Dict[str, int] = {f: 0 for f in _builtin_methods if f.islower()}
        self.name_finder: NameFinder = name_finder

    def add_name(self, name: str) -> None:
        if name in self.standard_methods:
            self.standard_methods[name] += 1

    def generate_rules(self) -> Iterator[AstroidRule]:

        for method, count in self.standard_methods.items():
            next_name: str = self.name_finder.next_name()

            length_not_renamed: int = len(method) * count

            length_renamed: int = len(next_name) * count + len(f"{next_name}={method}")

            if length_renamed < length_not_renamed:
                self.name_finder.pop_next_name()
                yield RenameCall(method, next_name)

                yield DefineRenameCall(method, next_name)

    def visit_Call(self, node: ast.Call) -> None:
        if isinstance(node.func, ast.Name):
            self.add_name(node.func.name)


if __name__ == "__main__":
    print(_builtin_methods)
