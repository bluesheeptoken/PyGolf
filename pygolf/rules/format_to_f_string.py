import re
from typing import *

import astroid as ast

from .astroid_rule import AstroidRule
from .version import Version


def create_format_spec_node(
    node: ast.Call, value: ast.Name, format_spec: str
) -> ast.FormattedValue:
    specifications = ast.JoinedStr(
        lineno=node.lineno, col_offset=node.col_offset, parent=node.parent,
    )

    formatted_value_node = ast.FormattedValue(
        lineno=node.lineno, col_offset=node.col_offset, parent=node.parent
    )
    if format_spec:
        specifications.postinit(values=[ast.Const(format_spec.replace(":", ""))])
    else:
        specifications.postinit(values=[ast.Const("''")])

    formatted_value_node.postinit(
        value=ast.Const(value.name), format_spec=specifications
    )

    return formatted_value_node


class FormatToFString(AstroidRule):
    on_node = ast.Call

    def transform(self) -> ast.JoinedStr:
        f_string_node = ast.JoinedStr(
            lineno=self.lineno, col_offset=self.col_offset, parent=self.parent,
        )

        constants: List[str] = re.split("{[^{]*}", self.func.expr.value)
        specs = re.findall("(?<={)[^{]*(?=})", self.func.expr.value)

        values = []
        for i, const in enumerate(constants):
            values.append(ast.Const(const))
            if i != len(constants) - 1:
                formatted_node = create_format_spec_node(self, self.args[i], specs[i])

                values.append(formatted_node)

        f_string_node.postinit(values=values)

        return f_string_node

    def predicate(self) -> bool:
        return isinstance(self.func, ast.Attribute) and self.func.attrname == "format"

    def since(self) -> Version:
        return Version("3.6")
