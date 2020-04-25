import unittest
from test.rules.helper_testkit import register_rule

import astroid

from pygolf.rules import *
from pygolf.unparser import Unparser

unparser = Unparser()


class TestComprehensionForAssignToMapAssign(unittest.TestCase):
    def test_rule(self):
        with register_rule(ComprehensionForAssignToMapAssign()) as transformer:
            node = transformer.visit(astroid.parse("x,y=[int(j) for j in input().split()]"))
            unparsed = unparser.unparse(node)
            self.assertEqual(unparsed, "x,y=map(int,input().split())")

            node = transformer.visit(astroid.parse("x,y=[f(j, 1) for j in input().split()]"))
            unparsed = unparser.unparse(node)
            self.assertEqual(unparsed, "x,y=[f(j,1)for j in input().split()]")


class TestDefineRenameCall(unittest.TestCase):
    def test_rule(self):
        with register_rule(DefineRenameCall("method_name", "new_method_name")) as transformer:
            node = transformer.visit(astroid.parse(""))
            unparsed = unparser.unparse(node)
            self.assertEqual(unparsed, "new_method_name=method_name")

            node = transformer.visit(astroid.parse(unparsed))
            unparsed = unparser.unparse(node)
            self.assertEqual(unparsed, "new_method_name=method_name")


class TestFormatToFString(unittest.TestCase):
    def test_rule(self):
        with register_rule(FormatToFString()) as transformer:
            node = transformer.visit(astroid.parse("'The best {} version is {:.2f} !'.format(language, version)"))
            self.assertEqual(
                "f'The best {language} version is {version:.2f} !'", unparser.unparse(node),
            )


class TestListAppend(unittest.TestCase):
    def test_rule(self):
        with register_rule(ListAppend()) as transformer:
            node = transformer.visit(astroid.parse("l.append(2)"))
            self.assertEqual("l+=[2]", unparser.unparse(node))


class TestRangeForToComprehensionFor(unittest.TestCase):
    def test_rule(self):
        with register_rule(RangeForToComprehensionFor()) as transformer:

            node = transformer.visit(astroid.parse("for i in range(2, 10, 5):print('hello world')"))
            self.assertEqual(unparser.unparse(node), "for i in range(2,10,5):print('hello world')")

            node = transformer.visit(astroid.parse("for i in range(1,n):print('hello world')"))
            self.assertEqual(unparser.unparse(node), "for i in'|'*(n-1):print('hello world')")

            node = transformer.visit(astroid.parse("for i in range(n):print('hello world')"))
            self.assertEqual(unparser.unparse(node), "for i in'|'*n:print('hello world')")


class TestRenameAssign(unittest.TestCase):
    def test_rule(self):
        with register_rule(RenameAssignName("long_name", "very_short_name")) as transformer:
            node = transformer.visit(astroid.parse("long_name,short_name=l"))
            self.assertEqual("very_short_name,short_name=l", unparser.unparse(node))


class TestRenameCall(unittest.TestCase):
    def test_rule(self):
        with register_rule(RenameCall("method_name", "new_method_name")) as transformer:
            node = transformer.visit(astroid.parse("method_name(2)"))
            self.assertEqual("new_method_name(2)", unparser.unparse(node))


class TestRenameName(unittest.TestCase):
    def test_rule(self):
        with register_rule(RenameName("long_name", "very_short_name")) as transformer:
            node = transformer.visit(astroid.parse("print(long_name)"))
            self.assertEqual("print(very_short_name)", unparser.unparse(node))
