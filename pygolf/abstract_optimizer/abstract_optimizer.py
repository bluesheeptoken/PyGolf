from typing import *

from astroid.node_classes import NodeNG

from pygolf.abstract_optimizer.assign_name_optimizer import AssignNameOptimizer
from pygolf.abstract_optimizer.optimizer import Optimizer
from pygolf.helper import walker
from pygolf.name_finder import NameFinder
from pygolf.rules import AstroidRule


class AbstractOptimizer:
    def __init__(self, name_finder: NameFinder):
        self.name_finder: NameFinder = name_finder
        self.optimizers: List[Optimizer] = [AssignNameOptimizer(name_finder)]

    def generate_optimizations_rules(self) -> List[AstroidRule]:
        rules: List[AstroidRule] = []
        for optimizer in self.optimizers:
            rules += optimizer.generate_rules()
        return rules

    def visit(self, node: NodeNG) -> None:
        for child in walker.walk(node):
            for optimizer in self.optimizers:
                optimizer.visit(child)
