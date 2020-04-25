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

    def since(self) -> Version:
        return Version.min_version()

    on_node = None
