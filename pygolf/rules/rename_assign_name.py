import astroid as ast

from .astroid_rule import AstroidRule
from .version import Version


class RenameAssignName(AstroidRule):
    def __init__(self, old_name: str, new_name: str) -> None:
        self.new_name: str = new_name
        self.old_name: str = old_name

    on_node = ast.AssignName

    def transform(self, node: on_node) -> ast.AssignName:
        return ast.AssignName(
            lineno=node.lineno,
            col_offset=node.col_offset,
            parent=node.parent,
            name=self.new_name,
        )

    def predicate(self, node: on_node) -> bool:
        return node.name == self.old_name

    def since(self) -> Version:
        return Version.min_version()
