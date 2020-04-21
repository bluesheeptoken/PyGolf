import astroid as ast
from astroid.node_classes import NodeNG

from .astroid_rule import AstroidRule


class RenameAssignName(AstroidRule):
    def __init__(self, old_name: str, new_name: str) -> None:
        self.new_name: str = new_name
        self.old_name: str = old_name

    on_node = ast.AssignName

    def transform(self, node: ast.AssignName) -> ast.AssignName:
        return ast.AssignName(
            lineno=node.lineno,
            col_offset=node.col_offset,
            parent=node.parent,
            name=self.new_name,
        )

    def predicate(self, node: NodeNG) -> bool:
        return isinstance(node, ast.AssignName) and node.name == self.old_name

    def __repr__(self) -> str:
        return f"RenameAssignName(old_name:{self.old_name}, new_name:{self.new_name})"
