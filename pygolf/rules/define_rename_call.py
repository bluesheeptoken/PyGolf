import astroid as ast

from ..helper import walker
from .astroid_rule import AstroidRule


class DefineRenameCall(AstroidRule):
    def __init__(self, old_name: str, new_name: str) -> None:
        self.new_name: str = new_name
        self.old_name: str = old_name

    on_node = ast.Module

    def transform(self, node: ast.Module) -> ast.Module:
        new_node = node
        new_assign = ast.Assign()
        new_assign.postinit(
            targets=[ast.AssignName(name=self.new_name, parent=new_assign)],
            value=ast.Name(name=self.old_name, parent=new_assign),
        )
        new_node.body = [new_assign] + node.body
        return new_node

    def predicate(self, node: ast.Module) -> bool:
        for node in walker.walk(node):
            if (
                isinstance(node, ast.Assign)
                and any(n.name == self.new_name for n in node.targets)
                and isinstance(node.value, ast.Name)
                and node.value.name == self.old_name
            ):
                return False
        return True

    def __repr__(self) -> str:
        return f"DefineRenameCall(old_name:{self.old_name}, new_name:{self.new_name})"
