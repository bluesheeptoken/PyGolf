from typing import Iterator

from astroid.node_classes import NodeNG

from pygolf.name_finder import NameFinder
from pygolf.optimizers.batch_optimizer import BatchOptimizer
from pygolf.rules import AstroidRule

from .phase import Phase


class RenamePhase(Phase):
    def generate_rules(self, ast: NodeNG) -> Iterator[AstroidRule]:
        name_finder = NameFinder()
        optimizer = BatchOptimizer(name_finder)
        optimizer.visit(ast)
        yield from optimizer.generate_optimizations_rules()
