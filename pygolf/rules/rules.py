import re
from typing import *

import astroid as ast

from pygolf.rules.astroid_rule import AstroidRule
from pygolf.rules.node_creator_helper import create_for_node_with_new_iter, create_format_spec_node
from pygolf.rules.version import Version

from ..helper import walker


class AnnAssignToAssign(AstroidRule):
    on_node = ast.AnnAssign

    def transform(self, node: ast.AnnAssign) -> ast.Assign:
        assign_node = ast.Assign(lineno=node.lineno, col_offset=node.col_offset, parent=node.parent)
        assign_node.postinit(targets=[node.target], value=node.value)
        return assign_node

    def predicate(self, node: ast.AnnAssign) -> bool:
        return True

    def __repr__(self) -> str:
        return f"AnnAssignToAssign"


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


class FormatToFString(AstroidRule):
    on_node = ast.Call

    def transform(self, node: ast.Call) -> ast.JoinedStr:
        f_string_node = ast.JoinedStr(lineno=node.lineno, col_offset=node.col_offset, parent=node.parent,)

        constants: List[str] = re.split("{[^{]*}", node.func.expr.value)
        specs = re.findall("(?<={)[^{]*(?=})", node.func.expr.value)

        values = []
        for i, const in enumerate(constants):
            values.append(ast.Const(const))
            if i != len(constants) - 1:
                formatted_node = create_format_spec_node(node, node.args[i], specs[i])

                values.append(formatted_node)

        f_string_node.postinit(values=values)

        return f_string_node

    def predicate(self, node: ast.Call) -> bool:
        return isinstance(node.func, ast.Attribute) and node.func.attrname == "format"

    def since(self) -> Version:
        return Version("3.6")

    def __repr__(self) -> str:
        return "FormatToFString"


class RangeForToComprehensionFor(AstroidRule):
    on_node = ast.For

    def transform(self, node: ast.For) -> ast.For:
        range_method: ast.Call = node.iter

        if len(range_method.args) == 1:
            end = range_method.args[0]
            return create_for_node_with_new_iter(node, ast.extract_node(f"'|'*{end.as_string()}"))
        if len(range_method.args) == 2:
            start, end = range_method.args
            return create_for_node_with_new_iter(node, ast.extract_node(f"'|'*({end.as_string()}-{start.as_string()})"))

        return node  # No optimization here

    def predicate(self, node: ast.For) -> bool:
        is_range_for: bool = isinstance(node.iter, ast.Call) and node.iter.func.name == "range"

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


class RenameAssignName(AstroidRule):
    def __init__(self, old_name: str, new_name: str) -> None:
        self.new_name: str = new_name
        self.old_name: str = old_name

    on_node = ast.AssignName

    def transform(self, node: ast.AssignName) -> ast.AssignName:
        return ast.AssignName(lineno=node.lineno, col_offset=node.col_offset, parent=node.parent, name=self.new_name,)

    def predicate(self, node: ast.AssignName) -> bool:
        return node.name == self.old_name  # type:ignore

    def __repr__(self) -> str:
        return f"RenameAssignName(old_name:{self.old_name}, new_name:{self.new_name})"


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

    def predicate(self, node: ast.Call) -> bool:
        return isinstance(node.func, ast.Name) and node.func.name == self.old_name

    def __repr__(self) -> str:
        return f"RenameCall(old_name:{self.old_name}, new_name:{self.new_name})"


class RenameName(AstroidRule):
    def __init__(self, old_name: str, new_name: str) -> None:
        self.new_name: str = new_name
        self.old_name: str = old_name

    on_node = ast.Name

    def transform(self, node: ast.Name) -> ast.Name:
        return ast.Name(lineno=node.lineno, col_offset=node.col_offset, parent=node.parent, name=self.new_name,)

    def predicate(self, node: ast.Name) -> bool:
        return node.name == self.old_name  # type:ignore

    def __repr__(self) -> str:
        return f"RenameName(old_name:{self.old_name}, new_name:{self.new_name})"