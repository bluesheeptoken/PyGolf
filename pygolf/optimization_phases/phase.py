import abc
from typing import Iterator

from astroid.node_classes import NodeNG

from pygolf.rules import AstroidRule


class Phase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def generate_rules(self, ast: NodeNG) -> Iterator[AstroidRule]:
        raise NotImplementedError
