from typing import Optional

import astroid as ast


def create_for_node_with_new_iter(old_for_node: ast.For, new_iter: ast.BinOp) -> ast.For:
    new_for_node = ast.For(lineno=old_for_node.lineno, col_offset=old_for_node.col_offset, parent=old_for_node.parent,)

    new_iter.parent = new_for_node

    new_for_node.postinit(
        target=old_for_node.target, iter=new_iter, body=old_for_node.body, orelse=old_for_node.orelse,
    )

    return new_for_node


def create_format_spec_node(node: ast.Call, value: ast.Name, format_spec: str) -> ast.FormattedValue:
    formatted_value_node = ast.FormattedValue(lineno=node.lineno, col_offset=node.col_offset, parent=node.parent)
    specifications: Optional[ast.JoinedStr]
    if format_spec:
        specifications = ast.JoinedStr(lineno=node.lineno, col_offset=node.col_offset, parent=node.parent,)
        specifications.postinit(values=[ast.Const(format_spec.replace(":", ""))])
    else:
        specifications = None

    formatted_value_node.postinit(value=ast.Name(value.name), format_spec=specifications)

    return formatted_value_node
