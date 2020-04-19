from typing import *

from astroid.node_classes import NodeNG

from pygolf.helper import walker
from pygolf.name_finder import NameFinder
from pygolf.rules import AstroidRule

from .assign_name_optimizer import AssignNameOptimizer
from .optimizer import Optimizer
from .rename_method_optimizer import RenameMethodOptimizer


class BatchOptimizer:
    def __init__(self, name_finder: NameFinder):
        self.name_finder: NameFinder = name_finder
        self.optimizers: List[Optimizer] = [
            AssignNameOptimizer(name_finder),
            RenameMethodOptimizer(name_finder),
        ]

    def generate_optimizations_rules(self) -> Iterator[AstroidRule]:
        for optimizer in self.optimizers:
            yield from optimizer.generate_rules()

    def visit(self, node: NodeNG) -> None:
        for child in walker.walk(node):
            for optimizer in self.optimizers:
                optimizer.visit(child)
