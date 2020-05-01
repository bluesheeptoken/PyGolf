import unittest

from astroid import extract_node, parse

from pygolf.unparser import Unparser


class TestUnparser(unittest.TestCase):

    unparser = Unparser()

    def test_unparse_for(self):
        async_for = extract_node("async for thing in things:pass")

        self.assertEqual(self.unparser.unparse_for(async_for, True), "async for thing in things:pass")

        for_def = extract_node(
            """
for thing in things:
    pass
"""
        )

        self.assertEqual(self.unparser.unparse_for(for_def, False), "for thing in things:pass")

    def test_unparse_function_def(self):
        async_function_def = extract_node(
            """
@test
async def func(things):
    async for thing in things:pass
"""
        )
        self.assertEqual(
            self.unparser.unparse_function_def(async_function_def, True),
            "@test\nasync def func(things):\n async for thing in things:pass",
        )

        function_def = extract_node("def func(a, b=2):pass")
        self.assertEqual(
            self.unparser.unparse_function_def(function_def, False), "def func(a,b=2):pass",
        )

    def test_unparse_with(self):
        async_with_node = extract_node("async with open('foo') as bar:pass")

        self.assertEqual(
            self.unparser.unparse_with(async_with_node, True), "async with open('foo') as bar:pass",
        )

        with_node = extract_node("with open('foo') as bar, foo:pass")

        self.assertEqual(
            self.unparser.unparse_with(with_node, False), "with open('foo') as bar,foo:pass",
        )

    # def test_unparse_AnnAssign(self):
    #     node = extract_node("a: int = 1")
    #     self.assertEqual(self.unparser.unparse_AnnAssign(node), "a=1")

    def test_unparse_Arguments(self):
        node = extract_node("def f(foo, bar=None): pass").args
        self.assertEqual(self.unparser.unparse_Arguments(node), "foo,bar=None")

    def test_unparse_Assert(self):
        assert_with_message = extract_node("assert True, 'message'")
        self.assertEqual(self.unparser.unparse_Assert(assert_with_message), "assert True,'message'")

        assert_without_message = extract_node("assert True")
        self.assertEqual(self.unparser.unparse_Assert(assert_without_message), "assert True")

    def test_unparse_Assign(self):
        assign_several = extract_node("*a, b = 2, 3, 5")
        self.assertEqual(self.unparser.unparse_Assign(assign_several), "*a,b=2,3,5")

        assign_single_starred = extract_node("*a, = 2, 3, 5")
        self.assertEqual(self.unparser.unparse_Assign(assign_single_starred), "*a,=2,3,5")

        assign_single_not_starred = extract_node("a = 2")
        self.assertEqual(self.unparser.unparse_Assign(assign_single_not_starred), "a=2")

        multiple_targets = extract_node("a = b = 2")
        self.assertEqual(self.unparser.unparse_Assign(multiple_targets), "a=b=2")

    def test_unparse_AssignAttr(self):
        node = extract_node("self.attribute = 2")
        self.assertEqual(self.unparser.unparse_Assign(node), "self.attribute=2")

    def test_unparse_AssignName(self):
        node = extract_node("a = 2")
        self.assertEqual(self.unparser.unparse_Assign(node), "a=2")

    def test_unparse_Attribute(self):
        node = extract_node("snake.colour")

        self.assertEqual(self.unparser.unparse_Attribute(node), "snake.colour")

    def test_unparse_AugAssign(self):
        node = extract_node("a *= 2")

        self.assertEqual(self.unparser.unparse_AugAssign(node), "a*=2")

    def test_unparse_BinOp(self):
        self.assertEqual(self.unparser.unparse_BinOp(extract_node("4*(a + 2)")), "4*(a+2)")

        self.assertEqual(self.unparser.unparse_BinOp(extract_node("(1 + 2) + 3")), "1+2+3")

        self.assertEqual(self.unparser.unparse_BinOp(extract_node("(1 + 2) * 3")), "(1+2)*3")

        self.assertEqual(self.unparser.unparse_BinOp(extract_node("'a'*(5//n)")), "'a'*(5//n)")

        self.assertEqual(
            self.unparser.unparse_BinOp(extract_node("might_generate_string()*(5//n)")), "might_generate_string()*(5//n)",
        )

        self.assertEqual(self.unparser.unparse_BinOp(extract_node("a**(2/3)")), "a**(2/3)")

    def test_unparse_BoolOP(self):
        node = parse("True and '' and False").body[0].value

        self.assertEqual(self.unparser.unparse_BoolOp(node), "True and''and False")

    def test_unparse_Call(self):
        node = extract_node("f(a, b=2, c=3)")

        self.assertEqual(self.unparser.unparse_Call(node), "f(a,b=2,c=3)")

    def test_unparse_ClassDef(self):
        node = extract_node(
            """
@test
class A(B,C):
    @dec
    def __init__(self):
        pass"""
        )

        self.assertEqual(
            self.unparser.unparse_ClassDef(node),
            """@test
class A(B,C):
 @dec
 def __init__(self):pass""",
        )

    def test_unparse_Compare(self):
        node = extract_node("a <= 2 > b")

        self.assertEqual(self.unparser.unparse_Compare(node), "a<=2>b")

        self.assertEqual(
            self.unparser.unparse_Compare(extract_node("3 not in (1, 2, 3)")), "3 not in(1,2,3)",
        )

    def test_unparse_Comprehension(self):
        node = extract_node("[i for i in range(10) if i < 5 if i > 8]").generators[0]

        self.assertEqual(self.unparser.unparse_Comprehension(node), "for i in range(10)if i<5 if i>8")

    def test_unparse_Const(self):
        const = extract_node("2")

        self.assertEqual(self.unparser.unparse_Const(const), "2")

        string_const = extract_node("a='golf'").value

        self.assertEqual(self.unparser.unparse_Const(string_const), "'golf'")

        long_string_const = extract_node(
            """a='''go
lf'''"""
        ).value

        self.assertEqual(
            self.unparser.unparse_Const(long_string_const),
            """'''go
lf'''""",
        )

    def test_unparse_Decorators(self):
        node = extract_node("@property\n@decoratorsWithArguments(2, a=3)\ndef f():pass").decorators
        self.assertEqual(
            self.unparser.unparse_Decorators(node), "@property\n@decoratorsWithArguments(2,a=3)",
        )

    def test_unparse_Delete(self):
        node = extract_node("del a, self.b")
        self.assertEqual(self.unparser.unparse_Delete(node), "del a,self.b")

    def test_unparse_Dict(self):
        node = extract_node("{1: 1, 'a': 'b'}")
        self.assertEqual(self.unparser.unparse_Dict(node), "{1:1,'a':'b'}")

    def test_unparse_DictComp(self):
        node = extract_node("{k: 2 for k, _ in things if k < 5 for things in meta_things}")
        self.assertEqual(
            self.unparser.unparse_DictComp(node), "{k:2for k,_ in things if k<5for things in meta_things}",
        )

    def test_unparse_ExceptHandler(self):
        node = extract_node(
            """
try:
    f()
except Exception as error:
    pass
"""
        ).handlers[0]
        self.assertEqual(self.unparser.unparse_ExceptHandler(node), "except Exception as error:pass")

    def test_unparse_JoinedStr(self):
        node = extract_node('f"You reduced your code by {percent_characters:.2f} !"')

        self.assertEqual(
            self.unparser.unparse_JoinedStr(node), "f'You reduced your code by {percent_characters:.2f} !'",
        )

        node = extract_node(
            """f'''long
string'''"""
        )

        self.assertEqual(
            self.unparser.unparse_JoinedStr(node),
            """f'''long
string'''""",
        )

        node = extract_node("""f"{'2'}\"""")

        self.assertEqual(self.unparser.unparse_JoinedStr(node), """f'{"2"}'""")

    def test_unparse_GeneratorExp(self):
        node = extract_node("(thing for thing in things for things in range(10) for x in y if thing)")

        self.assertEqual(
            self.unparser.unparse_GeneratorExp(node), "(thing for thing in things for things in range(10)for x in y if thing)",
        )

    def test_unparse_Global(self):
        node = extract_node("global a, b")

        self.assertEqual(self.unparser.unparse_Global(node), "global a,b")

    def test_unparse_If(self):
        if_node = extract_node("if condition:pass")

        self.assertEqual(self.unparser.unparse_If(if_node), "if condition:pass")

        if_else_node = extract_node(
            """if {}:pass
else:pass"""
        )

        self.assertEqual(
            self.unparser.unparse_If(if_else_node),
            """if{}:pass
else:pass""",
        )

    def test_unparse_IfExp(self):
        node = extract_node("5 if {} else 2")

        self.assertEqual(self.unparser.unparse_IfExp(node), "5if{}else 2")

    def test_unparse_Import(self):
        node = extract_node("import foo as foo, bar")

        self.assertEqual(self.unparser.unparse_Import(node), "import foo as foo,bar")

    def test_unparse_ImportFrom(self):
        node = extract_node("from ...module import foo as foo, bar as bar")

        self.assertEqual(
            self.unparser.unparse_ImportFrom(node), "from ...module import foo as foo,bar as bar",
        )

    def test_unparse_Lambda(self):
        node = extract_node("lambda x, y: (x, y)")

        self.assertEqual(self.unparser.unparse_Lambda(node), "lambda x,y:x,y")

    def test_unparse_List(self):
        node = extract_node("[2, 3, 5]")

        self.assertEqual(self.unparser.unparse_List(node), "[2,3,5]")

    def test_unparse_ListComp(self):
        node = extract_node("[2 for x in range(10)]")

        self.assertEqual(self.unparser.unparse_ListComp(node), "[2for x in range(10)]")

    def test_unparse_Module(self):
        node = parse("print(2)")
        self.assertEqual(
            self.unparser.unparse(node), "print(2)",
        )

    def test_unparse_Nonlocal(self):
        node = extract_node("nonlocal a, b")

        self.assertEqual(self.unparser.unparse_Nonlocal(node), "nonlocal a,b")

    def test_unparse_Raise(self):
        raise_none = extract_node("raise")

        self.assertEqual(self.unparser.unparse_Raise(raise_none), "raise")

        raise_call = extract_node("raise Exception('So bad') from x")

        self.assertEqual(self.unparser.unparse_Raise(raise_call), "raise Exception('So bad')from x")

    def test_unparse_Return(self):
        node = extract_node("return []")

        self.assertEqual(self.unparser.unparse_Return(node), "return[]")

    def test_unparse_Set(self):
        node = extract_node("{2, 3, 5}")

        self.assertEqual(self.unparser.unparse_Set(node), "{2,3,5}")

    def test_unparse_SetComp(self):
        node = extract_node("{2 for x in range(10)}")

        self.assertEqual(self.unparser.unparse_SetComp(node), "{2for x in range(10)}")

    def test_unparse_Slice(self):
        slice_1 = extract_node("l[1:]")

        self.assertEqual(self.unparser.unparse_Subscript(slice_1), "l[1:]")

        slice_2 = extract_node("l[1::5]")

        self.assertEqual(self.unparser.unparse_Subscript(slice_2), "l[1::5]")

        slice_3 = extract_node("l[1:2:3]")

        self.assertEqual(self.unparser.unparse_Subscript(slice_3), "l[1:2:3]")

        slice_4 = extract_node("l[:1:3]")

        self.assertEqual(self.unparser.unparse_Subscript(slice_4), "l[:1:3]")

    def test_unparse_Subscript(self):
        complex_slice = extract_node("l[1:3:5, 3]")

        self.assertEqual(self.unparser.unparse_Subscript(complex_slice), "l[1:3:5,3]")

        simple_slice = extract_node("l[1::5]")

        self.assertEqual(self.unparser.unparse_Subscript(simple_slice), "l[1::5]")

    def test_unparse_TryExcept(self):
        node = extract_node(
            """
try:pass
except Exception1 as e:pass
except Exception2 as e:pass
else:pass"""
        )

        self.assertEqual(
            self.unparser.unparse_TryExcept(node),
            """try:pass
except Exception1 as e:pass
except Exception2 as e:pass
else:pass""",
        )

    def test_unparse_TryFinally(self):
        node = extract_node("try:pass\nfinally:pass")

        self.assertEqual(self.unparser.unparse_TryFinally(node), "try:pass\nfinally:pass")

    def test_unparse_UnaryOp(self):
        node = extract_node("-3")

        self.assertEqual(self.unparser.unparse_UnaryOp(node), "-3")

        node = extract_node("not []")

        self.assertEqual(self.unparser.unparse_UnaryOp(node), "not[]")

        node = extract_node("not a")

        self.assertEqual(self.unparser.unparse_UnaryOp(node), "not a")

    def test_unparse_While(self):
        while_else = extract_node(
            """while True:pass
else:pass
"""
        )

        self.assertEqual(
            self.unparser.unparse_While(while_else),
            """while True:pass
else:pass""",
        )

        node_while = extract_node("while True:pass")

        self.assertEqual(self.unparser.unparse_While(node_while), "while True:pass")

    def test_unparse_Yield(self):
        node = extract_node("yield True")

        self.assertEqual(self.unparser.unparse_Yield(node), "yield True")

    def test_unparse_YieldFrom(self):
        node = extract_node("yield from True")

        self.assertEqual(self.unparser.unparse_YieldFrom(node), "yield from True")
