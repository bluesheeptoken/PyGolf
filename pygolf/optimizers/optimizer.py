import abc
from typing import Iterator

from astroid.node_classes import NodeNG


class Optimizer(metaclass=abc.ABCMeta):
    def visit(self, node: NodeNG):
        if hasattr(self, f"visit_{node.__class__.__name__}"):
            method = getattr(self, f"visit_{node.__class__.__name__}")
            method(node)

    @abc.abstractmethod
    def generate_rules(self) -> Iterator:
        raise NotImplementedError
