import math
from typing import *

import astroid as ast

from ..helper import walker
from .astroid_rule import AstroidRule
from .version import Version


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

        arguments: List[int] = list(map(lambda const: const.value, range_method.args))  # type: ignore
        start = 0
        step = 1

        if len(arguments) == 1:
            end = arguments[0]
        elif len(arguments) == 2:
            start, end = arguments
        else:
            start, end, step = arguments

        nb_iterations = math.ceil((end - start) / step)
        return _create_for_node(node, ast.extract_node(f"'|'*{nb_iterations}"))

    def predicate(self, node: ast.For) -> bool:
        is_range_for: bool = isinstance(
            node.iter, ast.Call
        ) and node.iter.func.name == "range"

        if not is_range_for:
            return False

        all_const: bool = all(isinstance(arg, ast.Const) for arg in node.iter.args)

        if not all_const:
            return False

        target_is_used: bool = False
        target: str = node.target.name
        for node0 in walker.walk(node):
            if isinstance(node0, ast.Name) and node0.name == target:
                target_is_used = True
                break

        return not target_is_used

    def since(self) -> Version:
        return Version.min_version()

    def __repr__(self) -> str:
        return "RangeForToComprehensionFor"
