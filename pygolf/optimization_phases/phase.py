import abc
from typing import List

from astroid.node_classes import NodeNG

from pygolf.rules import AstroidRule


class Phase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def generate_rules(self, ast: NodeNG) -> List[AstroidRule]:
        raise NotImplementedError
