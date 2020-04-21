import astroid as ast

from ..helper import walker
from .astroid_rule import AstroidRule


def _create_for_node(old_for_node: ast.For, new_iter: ast.BinOp) -> ast.For:
    new_for_node = ast.For(
        lineno=old_for_node.lineno,
        col_offset=old_for_node.col_offset,
        parent=old_for_node.parent,
    )

    new_iter.parent = new_for_node

    new_for_node.postinit(
        target=old_for_node.target,
        iter=new_iter,
        body=old_for_node.body,
        orelse=old_for_node.orelse,
    )

    return new_for_node


class RangeForToComprehensionFor(AstroidRule):
    on_node = ast.For

    def transform(self, node: ast.For) -> ast.For:
        range_method: ast.Call = node.iter

        if len(range_method.args) == 1:
            end = range_method.args[0]
            return _create_for_node(node, ast.extract_node(f"'|'*{end.as_string()}"))
        if len(range_method.args) == 2:
            start, end = range_method.args
            return _create_for_node(
                node, ast.extract_node(f"'|'*({end.as_string()}-{start.as_string()})")
            )

        return node  # No optimization here

    def predicate(self, node: ast.For) -> bool:
        is_range_for: bool = isinstance(
            node.iter, ast.Call
        ) and node.iter.func.name == "range"

        if not is_range_for:
            return False

        target_is_used: bool = False
        target: str = node.target.name
        for node0 in walker.walk(node):
            if isinstance(node0, ast.Name) and node0.name == target:
                target_is_used = True
                break

        return not target_is_used

    def __repr__(self) -> str:
        return "RangeForToComprehensionFor"
