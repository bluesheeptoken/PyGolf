import unittest

import astroid

from pygolf.rules import RenameName
from pygolf.unparser import Unparser


class TestRenameAssign(unittest.TestCase):
    def test_rule(self):
        rename_rule = RenameName("long_name", "very_short_name")

        astroid.MANAGER.register_transform(
            rename_rule.on_node, rename_rule.transform, rename_rule.predicate,
        )

        node = astroid.extract_node("print(long_name)")

        unparser = Unparser()

        self.assertEqual("print(very_short_name)", unparser.unparse(node))
