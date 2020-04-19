from typing import *

import astroid as ast

from pygolf.abstract_optimizer.optimizer import Optimizer
from pygolf.name_finder import NameFinder
from pygolf.rules import AstroidRule, RenameAssignName, RenameName


class AssignNameOptimizer(Optimizer):
    def __init__(self, name_finder: NameFinder) -> None:
        self.names: List[str] = []
        self.name_finder: NameFinder = name_finder

    def add_name(self, name: str) -> None:
        self.names.append(name)

    def generate_rules(self) -> List[AstroidRule]:
        rules: List[AstroidRule] = []
        for name in self.names:
            self.name_finder.remove_used_name(name)
        for name in self.names:
            next_name: str = self.name_finder.next_name()
            if len(next_name) < len(name):
                self.name_finder.pop_next_name()
                rules.append(RenameAssignName(name, next_name))
                rules.append(RenameName(name, next_name))
        return rules

    def visit_AssignName(self, node: ast.AssignName) -> None:
        self.add_name(node.name)
