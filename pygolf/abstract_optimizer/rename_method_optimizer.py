from typing import *

import astroid as ast

from pygolf.abstract_optimizer.optimizer import Optimizer
from pygolf.name_finder import NameFinder
from pygolf.rules import *

_builtin_methods = __builtins__.keys()  # type: ignore


class RenameMethodOptimizer(Optimizer):
    def __init__(self, name_finder: NameFinder) -> None:
        self.standard_methods: Dict[str, int] = {
            f: 0 for f in _builtin_methods if f.islower()
        }
        self.name_finder: NameFinder = name_finder

    def add_name(self, name: str) -> None:
        if name in self.standard_methods:
            self.standard_methods[name] += 1

    def generate_rules(self) -> List[AstroidRule]:
        rules: List[AstroidRule] = []
        for method, count in self.standard_methods.items():
            next_name: str = self.name_finder.next_name()

            length_not_renamed: int = len(method) * count

            length_renamed: int = len(next_name) * count + len(f"{next_name}={method}")

            if length_renamed < length_not_renamed:
                self.name_finder.pop_next_name()
                rules.append(RenameCall(method, next_name))

                rules.append(DefineRenameCall(method, next_name))

        return rules

    def visit_Call(self, node: ast.Call) -> None:
        self.add_name(node.func.name)


if __name__ == "__main__":
    print(_builtin_methods)
