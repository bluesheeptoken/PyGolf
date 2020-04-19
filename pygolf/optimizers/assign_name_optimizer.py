from typing import *

import astroid as ast

from pygolf.name_finder import NameFinder
from pygolf.optimizers.optimizer import Optimizer
from pygolf.rules import AstroidRule, RenameAssignName, RenameName


class AssignNameOptimizer(Optimizer):
    def __init__(self, name_finder: NameFinder) -> None:
        self.names: List[str] = []
        self.name_finder: NameFinder = name_finder

    def add_name(self, name: str) -> None:
        self.names.append(name)

    def generate_rules(self) -> Iterator[AstroidRule]:
        for name in self.names:
            self.name_finder.remove_used_name(name)
        for name in self.names:
            next_name: str = self.name_finder.next_name()
            if len(next_name) < len(name):
                self.name_finder.pop_next_name()
                yield RenameAssignName(name, next_name)
                yield RenameName(name, next_name)

    def visit_AssignName(self, node: ast.AssignName) -> None:
        self.add_name(node.name)
