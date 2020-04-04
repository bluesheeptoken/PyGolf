import unittest

import astroid

from pygolf.rules import RenameAssignName
from pygolf.unparser import Unparser


class TestRenameAssign(unittest.TestCase):
    def test_rule(self):
        rename_rule = RenameAssignName("long_name", "very_short_name")

        astroid.MANAGER.register_transform(
            rename_rule.on_node, rename_rule.transform, rename_rule.predicate,
        )

        node = astroid.extract_node("long_name,short_name=l")

        unparser = Unparser()

        self.assertEqual("very_short_name,short_name=l", unparser.unparse(node))
