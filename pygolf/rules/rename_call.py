import astroid as ast
from astroid.node_classes import NodeNG

from .astroid_rule import AstroidRule
from .version import Version


class RenameCall(AstroidRule):
    def __init__(self, old_name: str, new_name: str) -> None:
        self.new_name: str = new_name
        self.old_name: str = old_name

    on_node = ast.Call

    def transform(self, node: ast.Call) -> ast.Call:
        new_call = ast.Call(parent=node.parent)
        new_name = ast.Name(self.new_name, parent=new_call.parent)
        new_call.postinit(func=new_name, args=node.args, keywords=node.keywords)
        return new_call

    def predicate(self, node: NodeNG) -> bool:
        return isinstance(node, ast.Call) and node.func.name == self.old_name

    def since(self) -> Version:
        return Version.min_version()

    def __repr__(self) -> str:
        return f"RenameCall(old_name:{self.old_name}, new_name:{self.new_name})"
