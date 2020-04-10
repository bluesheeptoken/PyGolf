from typing import List

from astroid.node_classes import NodeNG

from pygolf.abstract_optimizer.abstract_optimizer import AbstractOptimizer
from pygolf.name_finder import NameFinder
from pygolf.rules import AstroidRule

from .phase import Phase


class RenamePhase(Phase):
    def generate_rules(self, ast: NodeNG) -> List[AstroidRule]:
        name_finder = NameFinder()
        optimizer = AbstractOptimizer(name_finder)
        optimizer.visit(ast)
        rules = optimizer.generate_optimizations_rules()
        return rules
