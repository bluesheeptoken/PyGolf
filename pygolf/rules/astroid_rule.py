import abc

from astroid.node_classes import NodeNG

from pygolf.rules.version import Version


class AstroidRule(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def transform(self, node: NodeNG) -> NodeNG:
        raise NotImplementedError

    @abc.abstractmethod
    def predicate(self, node: NodeNG) -> NodeNG:
        raise NotImplementedError

    @abc.abstractmethod
    def since(self) -> Version:
        raise NotImplementedError

    on_node = None
