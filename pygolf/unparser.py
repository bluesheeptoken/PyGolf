from astroid import *
from pygolf.errors.should_be_reduced_exception import ShouldBeReducedException
from pygolf.errors.python_2_code_detected import Python2CodeDetected


class Unparser():
    def __init__(self):
        self.sep = ' '

    def unparse(self, node, indent=0):
        method = getattr(self, "unparse_" + node.__class__.__name__)
        return method(node, indent)

    def unparse_alias_import(self, node):
        import_name, alias = node
        if alias is None:
            return import_name
        return f"{import_name} as {alias}"

    def unparse_block(self, block, indent=0):
        if self.has_block(block):
            return '\n' + '\n'.join(map(lambda x: self.unparse(x, indent+1), block))
        return ';'.join(map(self.unparse, block))

    def unparse_comprehension_generators(self, generators, indent=0):
        statement = ''

        for i, generator in enumerate(generators):
            statement += self.unparse(generator)
            if i != len(generators) - 1:
                statement += self.space_before_kw(generator)

        return statement

    def unparse_for(self, for_node, is_async, indent=0):
        for_statement = f"{self.sep*indent}{'async ' if is_async else ''}" \
            + f"for {self.unparse(for_node.target)} in{self.space_after_kw(for_node.iter)}" \
            + f"{self.unparse(for_node.iter)}:{self.unparse_block(for_node.body, indent)}"

        if for_node.orelse:
            for_statement += f"\n{self.sep*indent}else:{self.unparse_block(for_node.orelse, indent)}"

        return for_statement

    def unparse_function_def(self, node, is_async, indent=0):
        if node.decorators is not None:
            statement = self.unparse(node.decorators, indent) + '\n'
        else:
            statement = ""
        statement += f"{self.sep*indent}{'async ' if is_async else ''}def "
        statement += f"{node.name}({self.unparse(node.args)}):{self.unparse_block(node.body, indent)}"

        return statement

    def unparse_with(self, node, is_async, indent=0):
        return f"{self.sep*indent}{'async ' if is_async else ''}with " \
            + f"{','.join(map(self.unparse_with_item, node.items))}:" \
            + self.unparse_block(node.body, indent)

    def unparse_with_item(self, node):
        item, alias = node
        if alias is None:
            return self.unparse(item)
        return f"{self.unparse(item)} as {self.unparse(alias)}"

    def unparse_AnnAssign(self, node, indent=0):
        raise ShouldBeReducedException(node.__class__.__name__)

    def unparse_Arguments(self, node, indent=0):
        number_non_default_args = len(node.args) - len(node.defaults)
        return ','.join(
            self.unparse(arg)
            if i < number_non_default_args
            else f"{self.unparse(arg)}={self.unparse(node.defaults[i-number_non_default_args])}"
            for i, arg in enumerate(node.args)
        )

    def unparse_Assert(self, node, indent=0):
        if node.fail is not None:
            return f"{self.sep*indent}assert {self.unparse(node.test)},{self.unparse(node.fail)}"
        return f"{self.sep*indent}assert {self.unparse(node.test)}"

    def unparse_Assign(self, node, indent=0):
        if isinstance(node.targets[0], Tuple) and \
            len(node.targets[0].elts) == 1 and \
            isinstance(node.targets[0].elts[0], Starred):
            return f"{self.sep*indent}{self.unparse(node.targets[0])},={self.unparse(node.value)}"
        return f"{self.sep*indent}{'='.join(map(self.unparse, node.targets))}={self.unparse(node.value)}"

    def unparse_AssignAttr(self, node, indent=0):
        return f"{self.sep*indent}{self.unparse(node.expr)}.{node.attrname}"

    def unparse_AssignName(self, node, indent=0):
        return f"{self.sep*indent}{node.name}"

    def unparse_AsyncFor(self, node, indent=0):
        return self.unparse_for(node, True, indent)

    def unparse_AsyncFunctionDef(self, node, indent=0):
        return self.unparse_function_def(node, True, indent)

    def unparse_AsyncWith(self, node, indent=0):
        return self.unparse_with(node, True, indent)

    def unparse_Attribute(self, node, indent=0):
        return f"{self.sep*indent}{self.unparse(node.expr)}.{node.attrname}"

    def unparse_AugAssign(self, node, indent=0):
        return f"{self.sep*indent}{self.unparse(node.target)}{node.op}{self.unparse(node.value)}"

    def unparse_Await(self, node, indent=0):
        return f"{self.sep*indent}await"

    def unparse_BinOp(self, node, indent=0):
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
            "*": 5,
            "%": 5
        }

        statement = ""

        def unparse_child(parent_node, child_node):
            if isinstance(child_node, BinOp) and operators_level[parent_node.op] > operators_level[child_node.op]:
                return f"({self.unparse(child_node)})"
            else:
                return f"{self.unparse(child_node)}"

        statement += unparse_child(node, node.left)
        statement += node.op
        statement += unparse_child(node, node.right)

        return statement

    def unparse_BoolOp(self, node, indent=0):
        statement = ""

        for i, target in enumerate(node.values):
            if i == 0:
                statement += f"{self.unparse(target)}{self.space_before_kw(target)}{node.op}"
            else:
                statement += f"{self.space_after_kw(target)}{self.unparse(target)}"
                if i != len(node.values) - 1:
                    statement += f"{self.space_before_kw(target)}{node.op}"

        return statement

    def unparse_Break(self, node, indent=0):
        return f"{self.sep*indent}break"

    def unparse_Call(self, node, indent=0):
        args = []
        if node.args is not None:
            args += node.args
        if node.keywords is not None:
            args += node.keywords
        return f"{self.unparse(node.func)}({','.join(map(self.unparse, args))})"

    def unparse_ClassDef(self, node, indent=0):
        if node.decorators is not None:
            statement = self.unparse(node.decorators, indent) + '\n'
        else:
            statement = ""

        statement += f"{self.sep*indent}class {node.name}"

        if node.bases:
            statement += f"({','.join(map(self.unparse, node.bases))})"

        statement += ":"

        return statement + self.unparse_block(node.body, indent)


    def unparse_Compare(self, node, indent=0):
        statement = self.unparse(node.left)
        last_arg = node.left
        for op, arg in node.ops:
            if op in ('in', 'not in', 'is', 'is not'):
                statement += f" {op}{self.space_after_kw(arg)}{self.unparse(arg)}"
            else:
                statement += op + self.unparse(arg)

        return statement

    def unparse_Comprehension(self, node, indent=0):
        statement = f"for {self.unparse(node.target)}" \
                    + f"{self.space_before_kw(node.target)}" \
                    + f"in{self.space_after_kw(node.iter)}{self.unparse(node.iter)}"
        if statement is not None:
            for i, if_statement in enumerate(node.ifs):
                if i == 0:
                    statement += self.space_before_kw(node.iter)
                else:
                    statement += self.space_after_kw(node.ifs[i-1])
                statement += f"if{self.space_after_kw(if_statement)}{self.unparse(if_statement)}"
        return statement

    def unparse_Const(self, node, indent=0):
        return f"'{node.value}'" if "str" in node.pytype() else str(node.value)

    def unparse_Continue(self, node, indent=0):
        return f"{self.sep*indent}continue"

    def unparse_Decorators(self, node, indent=0):
        return '\n'.join(f"{self.sep*indent}@{self.unparse(decorator)}" for decorator in node.nodes)

    def unparse_DelAttr(self, node, indent=0):
        return f"{self.unparse(node.expr)}.{node.attrname}"

    def unparse_DelName(self, node, indent=0):
        return node.name

    def unparse_Delete(self, node, indent=0):
        return f"{self.sep*indent}del {','.join(map(self.unparse, node.targets))}"

    def unparse_Dict(self, node, indent=0):
        dict_values = ','.join(
            self.unparse(key) + ':' + self.unparse(value)
            for key, value in node.items
        )
        return f"{self.sep*indent}{{{dict_values}}}"

    def unparse_DictComp(self, node, indent=0):
        return f"{self.sep*indent}{{{self.unparse(node.key)}:{self.unparse(node.value)}" \
            + f"{self.space_before_kw(node.value)}{self.unparse_comprehension_generators(node.generators)}}}"

    def unparse_DictUnpack(self, node, indent=0):
        return f"{self.sep*indent}**"

    def unparse_Ellipsis(self, node, indent=0):
        return f"{self.sep*indent}..."

    def unparse_EmptyNode(self, node, indent=0):
        pass

    def unparse_ExceptHandler(self, node, indent=0):
        statement = f"{self.sep*indent}except {self.unparse(node.type)}"
        if node.name is not None:
            statement += f" as {self.unparse(node.name)}"
        return f"{statement}:{self.unparse_block(node.body, indent)}"

    def unparse_Exec(self, node, indent=0):
        raise Python2CodeDetected(node.__class__.__name__)

    def unparse_Expr(self, node, indent=0):
        return f"{self.sep*indent}{self.unparse(node.value)}"

    def unparse_ExtSlice(self, node, indent=0):
        return ','.join(map(self.unparse, node.dims))

    def unparse_For(self, node, indent=0):
        return self.unparse_for(node, False, indent)

    def unparse_FormattedValue(self, node, indent=0):
        unparsed_node = self.unparse(node.value).strip("'")
        spec = node.format_spec.values[0]

        if spec is not None and spec.value != "''":
            unparsed_spec = self.unparse(spec).strip("'")
            return f"{{{unparsed_node}:{unparsed_spec}}}"
        return f"{{{unparsed_node}}}"

    def unparse_FunctionDef(self, node, indent=0):
        return self.unparse_function_def(node, False, indent)

    def unparse_GeneratorExp(self, node, indent=0):
        return f"{self.sep*indent}({self.unparse(node.elt)}{self.space_before_kw(node.elt)}" + \
            f"{self.unparse_comprehension_generators(node.generators)})"

    def unparse_Global(self, node, indent=0):
        return f"{self.sep*indent}global {','.join(node.names)}"

    def unparse_If(self, node, indent=0):
        statement = f"{self.sep*indent}if{self.space_after_kw(node.test)}{self.unparse(node.test)}:" \
            + f"{self.unparse_block(node.body, indent)}"
        if node.orelse:
            statement += f"\n{self.sep*indent}else:{self.unparse_block(node.orelse, indent)}"
        return statement

    def unparse_IfExp(self, node, indent=0):
        return f"{self.sep*indent}{self.unparse(node.body)}{self.space_before_kw(node.body)}" \
            + f"if{self.space_after_kw(node.test)}{self.unparse(node.test)}" \
            + f"{self.space_after_kw(node.test)}else" \
            + f"{self.space_after_kw(node.orelse)}{self.unparse(node.orelse)}"

    def unparse_Import(self, node, indent=0):
        return f"{self.sep*indent}import {','.join(map(self.unparse_alias_import, node.names))}"

    def unparse_ImportFrom(self, node, indent=0):
        return f"{self.sep*indent}from {'.'*node.level}{node.modname} " \
            + f"import {','.join(map(self.unparse_alias_import, node.names))}"

    def unparse_Index(self, node, indent=0):
        return self.unparse(node.value)

    def unparse_JoinedStr(self, node, indent=0):
        unparsed_values = map(lambda x: self.unparse(x).strip("'"), node.values)
        return f"{self.sep*indent}f'{''.join(unparsed_values)}'"

    def unparse_Keyword(self, node, indent=0):
        return f"{node.arg}={self.unparse(node.value)}"

    def unparse_Lambda(self, node, indent=0):
        return f"{self.sep*indent}lambda {self.unparse(node.args)}:{self.unparse(node.body)}"

    def unparse_List(self, node, indent=0):
        return f"{self.sep*indent}[{','.join(map(self.unparse, node.elts))}]"

    def unparse_ListComp(self, node, indent=0):
        return f"{self.sep*indent}[{self.unparse(node.elt)}{self.space_before_kw(node.elt)}" \
            + f"{self.unparse_comprehension_generators(node.generators)}]"

    def unparse_Module(self, node, indent=0):
        separator = "\n" if self.has_block(node.body) else ";"
        return separator.join(map(self.unparse, node.body))

    def unparse_Name(self, node, indent=0):
        return node.name

    def unparse_Nonlocal(self, node, indent=0):
        return f"{self.sep*indent}nonlocal {','.join(node.names)}"

    def unparse_Pass(self, node, indent=0):
        return "pass"

    def unparse_Print(self, node, indent=0):
        raise Python2CodeDetected(node.__class__.__name__)

    def unparse_Raise(self, node, indent=0):
        statement ="raise"
        if node.exc is not None:
            statement += f" {self.unparse(node.exc)}"
        if node.cause is not None:
            if node.exc is None:
                statement += " "
            else:
                statement += self.space_before_kw(node.exc)
            statement += f"from {self.unparse(node.cause)}"
        return statement

    def unparse_Repr(self, node, indent=0):
        raise Python2CodeDetected(node.__class__.__name__)

    def unparse_Return(self, node, indent=0):
        return f"{self.sep*indent}return{self.space_after_kw(node.value)}{self.unparse(node.value)}"

    def unparse_Set(self, node, indent=0):
        return f"{self.sep*indent}{{{','.join(map(self.unparse, node.elts))}}}"

    def unparse_SetComp(self, node, indent=0):
        return f"{self.sep*indent}{{{self.unparse(node.elt)}{self.space_before_kw(node.elt)}" \
            + f"{self.unparse_comprehension_generators(node.generators)}}}"

    def unparse_Slice(self, node, indent=0):
        statement = ""

        if node.lower is not None:
            statement += self.unparse(node.lower)
        statement += ":"

        if node.upper is not None:
            statement += self.unparse(node.upper)
        if node.step is not None:
            statement += ":" + self.unparse(node.step)

        return statement

    def unparse_Starred(self, node, indent=0):
        return f"*{self.unparse(node.value)}"

    def unparse_Subscript(self, node, indent=0):
        return f"{self.sep*indent}{self.unparse(node.value)}[{self.unparse(node.slice)}]"

    def unparse_TryExcept(self, node, indent=0):
        statement = f"{self.sep*indent}try:{self.unparse_block(node.body)}\n"
        statement += '\n'.join(map(self.unparse, node.handlers))
        if node.orelse:
            return f"{statement}\nelse:{self.unparse_block(node.orelse)}"
        return statement

    def unparse_TryFinally(self, node, indent=0):
        statement = f"{self.sep*indent}try:{self.unparse_block(node.body)}"
        if node.finalbody:
            return f"{statement}\nfinally:{self.unparse_block(node.finalbody)}"
        return statement

    def unparse_Tuple(self, node, indent=0):
        if isinstance(node.parent, Compare):
            return f"({self.sep*indent}{','.join(map(self.unparse, node.elts))})"
        return self.sep*indent + ",".join(map(self.unparse, node.elts))

    def unparse_UnaryOp(self, node, indent=0):
        return f"{self.sep*indent}{node.op}{self.unparse(node.operand)}"

    def unparse_Unknown(self, node, indent=0):
        pass

    def unparse_While(self, node, indent=0):
        statement = f"{self.sep*indent}while {self.unparse(node.test)}:" \
            + self.unparse_block(node.body, indent)

        if node.orelse:
            statement += f"\n{self.sep*indent}else:{self.unparse_block(node.orelse, indent)}"

        return statement

    def unparse_With(self, node, indent=0):
        return self.unparse_with(node, False, indent)

    def unparse_Yield(self, node, indent=0):
        return f"{self.sep*indent}yield {self.unparse(node.value)}"

    def unparse_YieldFrom(self, node, indent=0):
        return f"{self.sep*indent}yield from {self.unparse(node.value)}"

    def space_after_kw(self, node):
        return '' if self._can_follow_reserved_keywords(node) else ' '

    def space_before_kw(self, node):
        return '' if self._can_be_before_reserved_keywords(node) else ' '

    def _can_follow_reserved_keywords(self, node):
        unparsed = self.unparse(node)
        return isinstance(unparsed, str) and unparsed[0] in "'\"({["

    def _can_be_before_reserved_keywords(self, node):
        unparsed = self.unparse(node)
        return isinstance(unparsed, str) and unparsed[-1] in "'\")}]0123456789"

    def has_block(self, block):
        def is_block(node):
            return node.__class__ in [
                AsyncFor,
                AsyncFunctionDef,
                AsyncWith,
                ClassDef,
                FunctionDef,
                For,
                If,
                With,
                While,
            ]
        return any(is_block(node) for node in block)
