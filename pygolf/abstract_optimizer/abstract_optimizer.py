from typing import *

import astroid as ast
from astroid.node_classes import NodeNG

from pygolf.abstract_optimizer.assign_name_optimizer import AssignNameOptimizer
from pygolf.errors.python_2_code_detected import Python2CodeDetected
from pygolf.name_finder import NameFinder
from pygolf.rules import AstroidRule


class AbstractOptimizer:
    def __init__(self, name_finder: NameFinder):
        self.name_finder: NameFinder = name_finder
        self.assign_name_optimizer: AssignNameOptimizer = AssignNameOptimizer()

    def generate_optimizations_rules(self) -> List[AstroidRule]:
        return self.assign_name_optimizer.generate_rules(self.name_finder)

    def visit(self, node: Optional[NodeNG]) -> None:
        if node is not None:
            method = getattr(self, "visit_" + node.__class__.__name__)
            return method(node)

    def visit_list(self, nodes: Optional[List[NodeNG]]) -> None:
        if nodes is not None:
            for node in nodes:
                self.visit(node)

    def visit_for(self, node: Union[ast.AsyncFor, ast.For]) -> None:
        self.visit(node.target)
        self.visit(node.iter)  # mypy ignore
        self.visit_list(node.body)
        self.visit_list(node.orelse)

    def visit_function_def(
        self, node: Union[ast.AsyncFunctionDef, ast.FunctionDef]
    ) -> None:
        # Optimize node.name
        self.visit_list(node.body)
        self.visit(node.args)
        self.visit_list(node.decorators)

    def visit_with(self, node: Union[ast.AsyncWith, ast.With]):
        for item in node.items:
            self.visit_list(item)
        self.visit_list(node.body)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        self.visit(node.target)
        self.visit(node.value)

    def visit_Arguments(self, node: ast.Arguments) -> None:
        self.visit_list(node.args)
        self.visit_list(node.defaults)

    def visit_Assert(self, node: ast.Assert) -> None:
        self.visit(node.fail)
        self.visit(node.test)

    def visit_Assign(self, node: ast.Assign) -> None:
        self.visit_list(node.targets)
        self.visit(node.value)

    def visit_AssignAttr(self, node: ast.AssignAttr) -> None:
        # Optimize node.attrname
        self.visit(node.expr)

    def visit_AssignName(self, node: ast.AssignName) -> None:
        self.assign_name_optimizer.add_name(node.name)

    def visit_AsyncFor(self, node: ast.AsyncFor) -> None:
        self.visit_for(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        return self.visit_function_def(node)

    def visit_AsyncWith(self, node: ast.AsyncWith) -> None:
        return self.visit_with(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        # optimize node.attrname
        self.visit(node.expr)

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        self.visit(node.target)
        self.visit(node.value)

    def visit_Await(self, node: ast.Await) -> None:
        self.visit(node.value)

    def visit_BinOp(self, node: ast.BinOp) -> None:
        self.visit(node.left)
        self.visit(node.right)

    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        self.visit_list(node.values)

    def visit_Break(self, node: ast.Break) -> None:
        pass

    def visit_Call(self, node: ast.Call) -> None:
        self.visit(node.func)
        self.visit_list(node.args)
        self.visit_list(node.keywords)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        # optimize node.name
        self.visit_list(node.bases)
        self.visit_list(node.body)

    def visit_Compare(self, node: ast.Compare) -> None:
        self.visit(node.left)
        self.visit_list(list(map(lambda x: x[1], node.ops)))

    def visit_Comprehension(self, node: ast.Comprehension) -> None:
        self.visit(node.target)
        self.visit(node.iter)
        self.visit_list(node.ifs)

    def visit_Const(self, node: ast.Const) -> None:
        pass

    def visit_Continue(self, node: ast.Continue) -> None:
        pass

    def visit_Decorators(self, node: ast.Decorators) -> None:
        self.visit_list(node.nodes)

    def visit_DelAttr(self, node: ast.DelAttr) -> None:
        # optimize node.attrname
        self.visit(node.expr)

    def visit_DelName(self, node: ast.DelName) -> None:
        # optimize node.name
        pass

    def visit_Delete(self, node: ast.Delete) -> None:
        self.visit_list(node.targets)

    def visit_Dict(self, node: ast.Dict) -> None:
        for item in node.items:
            self.visit(item[0])
            self.visit(item[1])

    def visit_DictComp(self, node: ast.DictComp) -> None:
        self.visit(node.key)
        self.visit(node.value)
        self.visit_list(node.generators)

    def visit_DictUnpack(self, node: ast.DictUnpack) -> None:
        pass

    def visit_Ellipsis(self, node: ast.Ellipsis) -> None:
        pass

    def visit_EmptyNode(self, node: ast.EmptyNode) -> None:
        pass

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        self.visit_list(node.body)
        self.visit(node.type)
        self.visit(node.name)

    def visit_Exec(self, node: ast.Exec) -> None:
        raise Python2CodeDetected(node.__class__.__name__)

    def visit_Expr(self, node: ast.Expr) -> None:
        self.visit(node.value)

    def visit_ExtSlice(self, node: ast.ExtSlice) -> None:
        self.visit(node.dims)

    def visit_For(self, node: ast.For) -> None:
        return self.visit_for(node)

    def visit_FormattedValue(self, node: ast.FormattedValue) -> None:
        self.visit(node.value)
        self.visit(node.format_spec)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        return self.visit_function_def(node)

    def visit_GeneratorExp(self, node: ast.GeneratorExp) -> None:
        self.visit(node.elt)
        self.visit_list(node.generators)

    def visit_Global(self, node: ast.Global) -> None:
        self.visit_list(node.names)

    def visit_If(self, node: ast.If) -> None:
        self.visit(node.test)
        self.visit_list(node.body)
        self.visit_list(node.orelse)

    def visit_IfExp(self, node: ast.IfExp) -> None:
        self.visit(node.test)
        self.visit(node.body)
        self.visit(node.orelse)

    def visit_Import(self, node: ast.Import) -> None:
        pass

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        pass

    def visit_Index(self, node: ast.Index) -> None:
        return self.visit(node.value)

    def visit_JoinedStr(self, node: ast.JoinedStr) -> None:
        self.visit_list(node.values)

    def visit_Keyword(self, node: ast.Keyword) -> None:
        self.visit(node.value)

    def visit_Lambda(self, node: ast.Lambda) -> None:
        self.visit(node.args)
        self.visit(node.body)

    def visit_List(self, node: ast.List) -> None:
        self.visit_list(node.elts)

    def visit_ListComp(self, node: ast.ListComp) -> None:
        self.visit(node.elt)
        self.visit_list(node.generators)

    def visit_Module(self, node: ast.Module) -> None:
        self.visit_list(node.body)

    def visit_Name(self, node: ast.Name) -> None:
        pass

    def visit_Nonlocal(self, node: ast.Nonlocal) -> None:
        self.visit_list(node.names)

    def visit_Pass(self, node: ast.Pass) -> None:
        pass

    def visit_Print(self, node: ast.Print) -> None:
        raise Python2CodeDetected(node.__class__.__name__)

    def visit_Raise(self, node: ast.Raise) -> None:
        self.visit(node.exc)
        self.visit(node.cause)

    def visit_Repr(self, node: ast.Repr) -> None:
        raise Python2CodeDetected(node.__class__.__name__)

    def visit_Return(self, node: ast.Return) -> None:
        self.visit(node.value)

    def visit_Set(self, node: ast.Set) -> None:
        self.visit_list(node.elts)

    def visit_SetComp(self, node: ast.SetComp) -> None:
        self.visit(node.elt)
        self.visit_list(node.generators)

    def visit_Slice(self, node: ast.Slice) -> None:
        self.visit(node.lower)
        self.visit(node.upper)
        self.visit(node.step)

    def visit_Starred(self, node: ast.Starred) -> None:
        self.visit(node.value)

    def visit_Subscript(self, node: ast.Subscript) -> None:
        self.visit(node.value)
        self.visit(node.slice)

    def visit_TryExcept(self, node: ast.TryExcept) -> None:
        self.visit_list(node.body)
        self.visit_list(node.handlers)
        self.visit_list(node.orelse)

    def visit_TryFinally(self, node: ast.TryFinally) -> None:
        self.visit_list(node.body)
        self.visit_list(node.finalbody)

    def visit_Tuple(self, node: ast.Tuple) -> None:
        self.visit_list(node.elts)

    def visit_UnaryOp(self, node: ast.UnaryOp) -> None:
        self.visit(node.operand)

    def visit_Unknown(self, node: ast.Unknown) -> None:
        pass

    def visit_While(self, node: ast.While) -> None:
        self.visit(node.test)
        self.visit_list(node.body)
        self.visit_list(node.orelse)

    def visit_With(self, node: ast.With) -> None:
        return self.visit_with(node)

    def visit_Yield(self, node: ast.Yield) -> None:
        self.visit(node.value)

    def visit_YieldFrom(self, node: ast.YieldFrom) -> None:
        self.visit(node.value)
