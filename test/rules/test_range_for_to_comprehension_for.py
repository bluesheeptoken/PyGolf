import unittest
from test.rules.helper import register_rule

import astroid

from pygolf.rules import RangeForToComprehensionFor
from pygolf.unparser import Unparser


class TestFormatToFString(unittest.TestCase):
    def test_rule(self):
        unparser = Unparser()

        with register_rule(RangeForToComprehensionFor()) as transformer:

            node = transformer.visit(
                astroid.parse("for i in range(2, 10, 5):print('hello world')")
            )
            self.assertEqual(
                unparser.unparse(node), "for i in'|'*2:print('hello world')"
            )

            node = transformer.visit(
                astroid.parse("for i in range(n):print('hello world')")
            )
            self.assertEqual(
                unparser.unparse(node), "for i in range(n):print('hello world')"
            )
