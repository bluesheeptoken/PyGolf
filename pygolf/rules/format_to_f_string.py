import astroid
import re


def create_const_node(value):
    return astroid.Const(value)

def create_format_spec_node(node, value, format_spec):
    specifications = astroid.JoinedStr(
        lineno=node.lineno,
        col_offset=node.col_offset,
        parent=node.parent,
    )

    formatted_value_node = astroid.FormattedValue(
        lineno=node.lineno,
        col_offset=node.col_offset,
        parent=node.parent
    )
    if format_spec:
        specifications.postinit(values=[astroid.Const(format_spec.replace(':', ''))])
    else:
        specifications.postinit(values=[astroid.Const("''")])

    formatted_value_node.postinit(
        value=astroid.Const(value.name),
        format_spec=specifications
    )

    return formatted_value_node


class FormatToFString:
    on_node = astroid.Call

    def transform(node):
        f_string_node = astroid.JoinedStr(
            lineno=node.lineno,
            col_offset=node.col_offset,
            parent=node.parent,
        )
        formatted_value_node = astroid.FormattedValue(
            lineno=node.lineno,
            col_offset=node.col_offset,
            parent=node.parent,
        )

        joined_node = astroid.extract_node("f'The best {language} version is {version:.2f}'")
        constants = re.split("{[^{]*}", node.func.expr.value)
        specs = re.findall("(?<={)[^{]*(?=})", node.func.expr.value)

        values = []
        for i, const in enumerate(constants):
            values.append(astroid.Const(const))
            if i != len(constants) - 1:
                formatted_node = create_format_spec_node(node, node.args[i], specs[i])

                values.append(formatted_node)

        f_string_node.postinit(values=values)

        return f_string_node

    def predicate(node):
        return isinstance(node.func, astroid.Attribute) and node.func.attrname == "format"

