from typing import *

import astroid as ast
from astroid.node_classes import NodeNG

from pygolf.errors.python_2_code_detected import Python2CodeDetected


class Unparser:
    def __init__(self, should_remove_spaces_between_keywords: bool = True) -> None:
        self.sep: str = " "
        self.should_remove_spaces_between_keywords = should_remove_spaces_between_keywords

    def unparse(self, node: NodeNG, indent: int = 0) -> str:
        method = getattr(self, "unparse_" + node.__class__.__name__)
        return method(node, indent)  # type: ignore

    def unparse_alias_import(self, node: List[Tuple[str, Optional[str]]]) -> str:
        import_name, alias = node
        if alias is None:
            return import_name

        return f"{import_name} as {alias}"

    def unparse_block(self, block: List[NodeNG], indent: int = 0) -> str:
        if self.has_block(block):
            return "\n" + "\n".join(map(lambda x: self.unparse(x, indent + 1), block))
        return ";".join(map(self.unparse, block))

    def unparse_comprehension_generators(self, generators: List[ast.Comprehension], indent: int = 0) -> str:
        stmnt = ""

        for i, generator in enumerate(generators):
            stmnt += self.unparse(generator)
            if i != len(generators) - 1:
                stmnt += self.space_before_kw(generator)

        return stmnt

    def unparse_for(self, for_node: Union[ast.AsyncFor, ast.For], is_async: bool, indent: int = 0) -> str:
        for_stmnt = (
            f"{self.sep*indent}{'async ' if is_async else ''}"
            f"for {self.unparse(for_node.target)} in{self.space_after_kw(for_node.iter)}"
            f"{self.unparse(for_node.iter)}:{self.unparse_block(for_node.body, indent)}"
        )

        if for_node.orelse:
            for_stmnt += f"\n{self.sep*indent}else:{self.unparse_block(for_node.orelse, indent)}"

        return for_stmnt

    def unparse_function_def(
        self, node: Union[ast.AsyncFunctionDef, ast.FunctionDef], is_async: bool, indent: int = 0,
    ) -> str:
        if node.decorators is not None:
            stmt = self.unparse(node.decorators, indent) + "\n"
        else:
            stmt = ""
        stmt += (
            f"{self.sep*indent}{'async ' if is_async else ''}def "
            f"{node.name}({self.unparse(node.args)}):{self.unparse_block(node.body, indent)}"
        )

        return stmt

    def unparse_with(self, node: Union[ast.AsyncWith, ast.With], is_async: bool, indent: int = 0) -> str:
        return (
            f"{self.sep*indent}{'async ' if is_async else ''}with "
            f"{','.join(map(self.unparse_with_item, node.items))}:" + self.unparse_block(node.body, indent)
        )

    def unparse_with_item(self, node: List[Tuple[NodeNG, Optional[ast.AssignName]]]) -> str:
        item, alias = node
        if alias is None:
            return self.unparse(item)
        return f"{self.unparse(item)} as {self.unparse(alias)}"

    def unparse_AnnAssign(self, node: ast.AnnAssign, indent: int = 0) -> str:
        if node.value is not None:
            name = node.target.name if hasattr(node.target, "name") else node.target.attrname
            return f"{self.sep*indent}{name}={self.unparse(node.value)}"  # ignore annotation
        return f"{self.sep*indent}{node.target.name}"

    def unparse_Arguments(self, node: ast.Arguments, indent: int = 0) -> str:
        number_non_default_args = len(node.args) - len(node.defaults)
        return ",".join(
            self.unparse(arg)
            if i < number_non_default_args
            else f"{self.unparse(arg)}={self.unparse(node.defaults[i-number_non_default_args])}"
            for i, arg in enumerate(node.args)
        )

    def unparse_Assert(self, node: ast.Assert, indent: int = 0) -> str:
        if node.fail is not None:
            return f"{self.sep*indent}assert {self.unparse(node.test)},{self.unparse(node.fail)}"
        return f"{self.sep*indent}assert {self.unparse(node.test)}"

    def unparse_Assign(self, node: ast.Assign, indent: int = 0) -> str:
        if (
            isinstance(node.targets[0], ast.Tuple)
            and len(node.targets[0].elts) == 1
            and isinstance(node.targets[0].elts[0], ast.Starred)
        ):
            return f"{self.sep*indent}{self.unparse(node.targets[0])},={self.unparse(node.value)}"
        return f"{self.sep*indent}{'='.join(map(self.unparse, node.targets))}={self.unparse(node.value)}"

    def unparse_AssignAttr(self, node: ast.AssignAttr, indent: int = 0) -> str:
        return f"{self.sep*indent}{self.unparse(node.expr)}.{node.attrname}"

    def unparse_AssignName(self, node: ast.AssignName, indent: int = 0) -> str:
        return f"{self.sep*indent}{node.name}"

    def unparse_AsyncFor(self, node: ast.AsyncFor, indent: int = 0) -> str:
        return self.unparse_for(node, True, indent)

    def unparse_AsyncFunctionDef(self, node: ast.AsyncFunctionDef, indent: int = 0) -> str:
        return self.unparse_function_def(node, True, indent)

    def unparse_AsyncWith(self, node: ast.AsyncWith, indent: int = 0) -> str:
        return self.unparse_with(node, True, indent)

    def unparse_Attribute(self, node: ast.Attribute, indent: int = 0) -> str:
        return f"{self.sep*indent}{self.unparse(node.expr)}.{node.attrname}"

    def unparse_AugAssign(self, node: ast.AugAssign, indent: int = 0) -> str:
        return f"{self.sep*indent}{self.unparse(node.target)}{node.op}{self.unparse(node.value)}"

    def unparse_Await(self, node: ast.Await, indent: int = 0) -> str:
        return f"{self.sep*indent}await"

    def unparse_BinOp(self, node: ast.BinOp, indent: int = 0) -> str:
        operators_level = {
            "|": 0,
            "^": 1,
            "&": 2,
            "<<": 3,
            ">>": 3,
            "+": 4,
            "-": 4,
            "*": 5,
            "//": 5,
            "/": 5,
            "%": 5,
            "**": 6,
        }

        stmnt = ""

        def unparse_child(node: ast.BinOp, child_node: NodeNG, already_have_parenthesis=False) -> str:
            if (
                not already_have_parenthesis
                and isinstance(child_node, ast.BinOp)
                and operators_level[node.op] > operators_level[child_node.op]
            ):
                return f"({self.unparse(child_node)})"
            return f"{self.unparse(child_node)}"

        stmnt += unparse_child(node, node.left)
        stmnt += node.op

        if (
            (
                (isinstance(node.left, ast.Const) and isinstance(node.left.value, str))
                or (
                    not isinstance(node.left, ast.BinOp) and not isinstance(node.left, ast.Const)
                )  # Possibly a string is returned, in doubt we have to put parenthesis
                or (isinstance(node.right, ast.Compare))
            )
            and operators_level[node.op] > 4
            and (isinstance(node.right, ast.BinOp) or isinstance(node.right, ast.Compare))
        ):
            stmnt += f"({unparse_child(node, node.right, already_have_parenthesis=True)})"
        else:
            stmnt += unparse_child(node, node.right)

        return stmnt

    def unparse_BoolOp(self, node: ast.BoolOp, indent: int = 0) -> str:
        stmnt = ""

        for i, target in enumerate(node.values):
            if i == 0:
                stmnt += f"{self.unparse(target)}{self.space_before_kw(target)}{node.op}"
            else:
                stmnt += f"{self.space_after_kw(target)}{self.unparse(target)}"
                if i != len(node.values) - 1:
                    stmnt += f"{self.space_before_kw(target)}{node.op}"

        return stmnt

    def unparse_Break(self, node: ast.Break, indent: int = 0) -> str:
        return f"{self.sep*indent}break"

    def unparse_Call(self, node: ast.Call, indent: int = 0) -> str:
        args: List[NodeNG] = []
        if node.args is not None:
            args += node.args
        if node.keywords is not None:
            args += node.keywords
        return f"{self.unparse(node.func)}({','.join(map(self.unparse, args))})"

    def unparse_ClassDef(self, node: ast.ClassDef, indent: int = 0) -> str:
        if node.decorators is not None:
            stmnt = self.unparse(node.decorators, indent) + "\n"
        else:
            stmnt = ""

        stmnt += f"{self.sep*indent}class {node.name}"

        if node.bases:
            stmnt += f"({','.join(map(self.unparse, node.bases))})"

        stmnt += ":"

        return stmnt + self.unparse_block(node.body, indent)

    def unparse_Compare(self, node: ast.Compare, indent: int = 0) -> str:
        stmnt = self.unparse(node.left)

        for op, arg in node.ops:
            if op in ("in", "not in", "is", "is not"):
                stmnt += f" {op}{self.space_after_kw(arg)}{self.unparse(arg)}"
            else:
                stmnt += op + self.unparse(arg)

        return stmnt

    def unparse_Comprehension(self, node: ast.Comprehension, indent: int = 0) -> str:
        stmnt = (
            f"for {self.unparse(node.target)}"
            f"{self.space_before_kw(node.target)}"
            f"in{self.space_after_kw(node.iter)}{self.unparse(node.iter)}"
        )
        if stmnt is not None:
            for i, if_stmnt in enumerate(node.ifs):
                if i == 0:
                    stmnt += self.space_before_kw(node.iter)
                else:
                    stmnt += self.space_after_kw(node.ifs[i - 1])
                stmnt += f"if{self.space_after_kw(if_stmnt)}{self.unparse(if_stmnt)}"
        return stmnt

    def unparse_Const(self, node: ast.Const, indent: int = 0) -> str:
        if "str" in node.pytype():
            quotes = "'''" if "\n" in node.value else "'"
            return f"{quotes}{node.value}{quotes}"
        return str(node.value)

    def unparse_Continue(self, node: ast.Continue, indent: int = 0) -> str:
        return f"{self.sep*indent}continue"

    def unparse_Decorators(self, node: ast.Decorators, indent: int = 0) -> str:
        return "\n".join(f"{self.sep*indent}@{self.unparse(decorator)}" for decorator in node.nodes)

    def unparse_DelAttr(self, node: ast.DelAttr, indent: int = 0) -> str:
        return f"{self.unparse(node.expr)}.{node.attrname}"

    def unparse_DelName(self, node: ast.DelName, indent: int = 0) -> str:
        return node.name  # type: ignore

    def unparse_Delete(self, node: ast.Delete, indent: int = 0) -> str:
        return f"{self.sep*indent}del {','.join(map(self.unparse, node.targets))}"

    def unparse_Dict(self, node: ast.Dict, indent: int = 0) -> str:
        dict_values = ",".join(self.unparse(key) + ":" + self.unparse(value) for key, value in node.items)
        return f"{self.sep*indent}{{{dict_values}}}"

    def unparse_DictComp(self, node: ast.DictComp, indent: int = 0) -> str:
        return (
            f"{self.sep*indent}{{{self.unparse(node.key)}:{self.unparse(node.value)}"
            f"{self.space_before_kw(node.value)}"
            f"{self.unparse_comprehension_generators(node.generators)}}}"
        )

    def unparse_DictUnpack(self, node: ast.DictUnpack, indent: int = 0) -> str:
        return f"{self.sep*indent}**"

    def unparse_Ellipsis(self, node: ast.Ellipsis, indent: int = 0) -> str:
        return f"{self.sep*indent}..."

    def unparse_EmptyNode(self, node: ast.EmptyNode, indent: int = 0) -> str:
        pass

    def unparse_ExceptHandler(self, node: ast.ExceptHandler, indent: int = 0) -> str:
        stmnt = f"{self.sep*indent}except {self.unparse(node.type)}"
        if node.name is not None:
            stmnt += f" as {self.unparse(node.name)}"
        return f"{stmnt}:{self.unparse_block(node.body, indent)}"

    def unparse_Exec(self, node: ast.Exec, indent: int = 0) -> str:
        raise Python2CodeDetected(node.__class__.__name__)

    def unparse_Expr(self, node: ast.Expr, indent: int = 0) -> str:
        return f"{self.sep*indent}{self.unparse(node.value)}"

    def unparse_ExtSlice(self, node: ast.ExtSlice, indent: int = 0) -> str:
        return ",".join(map(self.unparse, node.dims))

    def unparse_For(self, node: ast.For, indent: int = 0) -> str:
        return self.unparse_for(node, False, indent)

    def unparse_FormattedValue(self, node: ast.FormattedValue, indent: int = 0) -> str:
        unparsed_node = self.unparse(node.value).replace("'", '"')
        spec = node.format_spec.values[0] if node.format_spec is not None else None
        if spec is not None and spec.value != "''":
            unparsed_spec = self.unparse(spec).strip("'")
            return f"{{{unparsed_node}:{unparsed_spec}}}"
        return f"{{{unparsed_node}}}"

    def unparse_FunctionDef(self, node: ast.FunctionDef, indent: int = 0) -> str:
        return self.unparse_function_def(node, False, indent)

    def unparse_GeneratorExp(self, node: ast.GeneratorExp, indent: int = 0) -> str:
        return (
            f"{self.sep*indent}({self.unparse(node.elt)}{self.space_before_kw(node.elt)}"
            f"{self.unparse_comprehension_generators(node.generators)})"
        )

    def unparse_Global(self, node: ast.Global, indent: int = 0) -> str:
        return f"{self.sep*indent}global {','.join(node.names)}"

    def unparse_If(self, node: ast.If, indent: int = 0) -> str:
        stmnt = (
            f"{self.sep*indent}if{self.space_after_kw(node.test)}{self.unparse(node.test)}:"
            f"{self.unparse_block(node.body, indent)}"
        )
        if node.orelse:
            stmnt += f"\n{self.sep*indent}else:{self.unparse_block(node.orelse, indent)}"
        return stmnt

    def unparse_IfExp(self, node: ast.IfExp, indent: int = 0) -> str:
        return (
            f"{self.sep*indent}{self.unparse(node.body)}{self.space_before_kw(node.body)}"
            f"if{self.space_after_kw(node.test)}{self.unparse(node.test)}"
            f"{self.space_after_kw(node.test)}else"
            f"{self.space_after_kw(node.orelse)}{self.unparse(node.orelse)}"
        )

    def unparse_Import(self, node: ast.Import, indent: int = 0) -> str:
        return f"{self.sep*indent}import {','.join(map(self.unparse_alias_import, node.names))}"

    def unparse_ImportFrom(self, node: ast.ImportFrom, indent: int = 0) -> str:
        return (
            f"{self.sep*indent}from "
            f"{'.'*node.level if node.level is not None else ''}{node.modname} "
            f"import {','.join(map(self.unparse_alias_import, node.names))}"
        )

    def unparse_Index(self, node: ast.Index, indent: int = 0) -> str:
        return self.unparse(node.value)

    def unparse_JoinedStr(self, node: ast.JoinedStr, indent: int = 0) -> str:
        unparsed_values: List[str] = list(map(lambda x: self.unparse(x).strip("'"), node.values))
        quotes = "'''" if any("\n" in x for x in unparsed_values) else "'"
        return f"{self.sep*indent}f{quotes}{''.join(unparsed_values)}{quotes}"

    def unparse_Keyword(self, node: ast.Keyword, indent: int = 0) -> str:
        return f"{node.arg}={self.unparse(node.value)}"

    def unparse_Lambda(self, node: ast.Lambda, indent: int = 0) -> str:
        return f"{self.sep*indent}lambda {self.unparse(node.args)}:{self.unparse(node.body)}"

    def unparse_List(self, node: ast.List, indent: int = 0) -> str:
        return f"{self.sep*indent}[{','.join(map(self.unparse, node.elts))}]"

    def unparse_ListComp(self, node: ast.ListComp, indent: int = 0) -> str:
        return (
            f"{self.sep*indent}[{self.unparse(node.elt)}{self.space_before_kw(node.elt)}"
            f"{self.unparse_comprehension_generators(node.generators)}]"
        )

    def unparse_Module(self, node: ast.Module, indent: int = 0) -> str:
        separator = "\n" if self.has_block(node.body) else ";"
        return separator.join(map(self.unparse, node.body))

    def unparse_Name(self, node: ast.Name, indent: int = 0) -> str:
        return node.name  # type: ignore

    def unparse_Nonlocal(self, node: ast.Nonlocal, indent: int = 0) -> str:
        return f"{self.sep*indent}nonlocal {','.join(node.names)}"

    def unparse_Pass(self, node: ast.Pass, indent: int = 0) -> str:
        return "pass"

    def unparse_Print(self, node: ast.Print, indent: int = 0) -> str:
        raise Python2CodeDetected(node.__class__.__name__)

    def unparse_Raise(self, node: ast.Raise, indent: int = 0) -> str:
        stmnt = "raise"
        if node.exc is not None:
            stmnt += f" {self.unparse(node.exc)}"
        if node.cause is not None:
            if node.exc is None:
                stmnt += " "
            else:
                stmnt += self.space_before_kw(node.exc)
            stmnt += f"from {self.unparse(node.cause)}"
        return stmnt

    def unparse_Repr(self, node: ast.Repr, indent: int = 0) -> str:
        raise Python2CodeDetected(node.__class__.__name__)

    def unparse_Return(self, node: ast.Return, indent: int = 0) -> str:
        if node.value is not None:
            return f"{self.sep*indent}return{self.space_after_kw(node.value)}{self.unparse(node.value)}"
        return f"{self.sep*indent}return"

    def unparse_Set(self, node: ast.Set, indent: int = 0) -> str:
        return f"{self.sep*indent}{{{','.join(map(self.unparse, node.elts))}}}"

    def unparse_SetComp(self, node: ast.SetComp, indent: int = 0) -> str:
        return (
            f"{self.sep*indent}{{{self.unparse(node.elt)}{self.space_before_kw(node.elt)}"
            f"{self.unparse_comprehension_generators(node.generators)}}}"
        )

    def unparse_Slice(self, node: ast.Slice, indent: int = 0) -> str:
        stmnt = ""

        if node.lower is not None:
            stmnt += self.unparse(node.lower)
        stmnt += ":"

        if node.upper is not None:
            stmnt += self.unparse(node.upper)
        if node.step is not None:
            stmnt += ":" + self.unparse(node.step)

        return stmnt

    def unparse_Starred(self, node: ast.Starred, indent: int = 0) -> str:
        return f"*{self.unparse(node.value)}"

    def unparse_Subscript(self, node: ast.Subscript, indent: int = 0) -> str:
        return f"{self.sep*indent}{self.unparse(node.value)}[{self.unparse(node.slice)}]"

    def unparse_TryExcept(self, node: ast.TryExcept, indent: int = 0) -> str:
        stmnt = f"{self.sep*indent}try:{self.unparse_block(node.body)}\n"
        stmnt += "\n".join(map(lambda handler: self.unparse(handler, indent), node.handlers))
        if node.orelse:
            return f"{stmnt}\nelse:{self.unparse_block(node.orelse)}"
        return stmnt

    def unparse_TryFinally(self, node: ast.TryFinally, indent: int = 0) -> str:
        stmnt = f"{self.sep*indent}try:{self.unparse_block(node.body)}"
        if node.finalbody:
            return f"{stmnt}\n{self.sep*indent}finally:{self.unparse_block(node.finalbody)}"
        return stmnt

    def unparse_Tuple(self, node: ast.Tuple, indent: int = 0) -> str:
        core: str = f"{self.sep*indent}{','.join(map(self.unparse, node.elts))}"
        if isinstance(node.parent, ast.Compare):
            return f"({core})"
        return self.sep * indent + core

    def unparse_UnaryOp(self, node: ast.UnaryOp, indent: int = 0) -> str:
        return (
            f"{self.sep*indent}{node.op}"
            f"{' ' if node.op == 'not' and not self._can_follow_reserved_keywords(node.operand) else ''}"
            f"{self.unparse(node.operand)}"
        )

    def unparse_Unknown(self, node: ast.Unknown, indent: int = 0) -> str:
        pass

    def unparse_While(self, node: ast.While, indent: int = 0) -> str:
        stmnt = f"{self.sep*indent}while {self.unparse(node.test)}:" + self.unparse_block(node.body, indent)

        if node.orelse:
            stmnt += f"\n{self.sep*indent}else:{self.unparse_block(node.orelse, indent)}"

        return stmnt

    def unparse_With(self, node: ast.With, indent: int = 0) -> str:
        return self.unparse_with(node, False, indent)

    def unparse_Yield(self, node: ast.Yield, indent: int = 0) -> str:
        return f"{self.sep*indent}yield {self.unparse(node.value)}"

    def unparse_YieldFrom(self, node: ast.YieldFrom, indent: int = 0) -> str:
        return f"{self.sep*indent}yield from {self.unparse(node.value)}"

    def space_after_kw(self, node):
        return "" if self._can_follow_reserved_keywords(node) else " "

    def space_before_kw(self, node):
        return "" if self._can_be_before_reserved_keywords(node) else " "

    def _can_follow_reserved_keywords(self, node):
        if not self.should_remove_spaces_between_keywords:
            return False
        unparsed = self.unparse(node)
        return isinstance(unparsed, str) and unparsed[0] in "'\"({["

    def _can_be_before_reserved_keywords(self, node):
        if not self.should_remove_spaces_between_keywords:
            return False
        unparsed = self.unparse(node)
        return isinstance(unparsed, str) and unparsed[-1] in "'\")}]0123456789"

    def has_block(self, block):
        def is_block(node):
            return node.__class__ in [
                ast.AsyncFor,
                ast.AsyncFunctionDef,
                ast.AsyncWith,
                ast.ClassDef,
                ast.FunctionDef,
                ast.For,
                ast.If,
                ast.TryExcept,
                ast.TryFinally,
                ast.With,
                ast.While,
            ]

        return any(is_block(node) for node in block)
