import unittest

import astroid

from pygolf.rules import RangeForToComprehensionFor
from pygolf.unparser import Unparser


class TestFormatToFString(unittest.TestCase):
    range_for_to_comprehension_for = RangeForToComprehensionFor()
    astroid.MANAGER.register_transform(
        range_for_to_comprehension_for.on_node,
        range_for_to_comprehension_for.transform,
        range_for_to_comprehension_for.predicate,
    )

    def test_rule(self):
        unparser = Unparser()

        node = astroid.extract_node("for i in range(2, 10, 5):print('hello world')")
        self.assertEqual(unparser.unparse(node), "for i in'|'*2:print('hello world')")

        node = astroid.extract_node("for i in range(n):print('hello world')")
        self.assertEqual(
            unparser.unparse(node), "for i in range(n):print('hello world')"
        )
