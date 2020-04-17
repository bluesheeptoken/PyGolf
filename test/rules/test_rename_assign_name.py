import unittest
from test.rules.helper import register_rule

import astroid

from pygolf.rules import RenameAssignName
from pygolf.unparser import Unparser


class TestRenameAssign(unittest.TestCase):
    def test_rule(self):
        unparser = Unparser()

        with register_rule(RenameAssignName("long_name", "very_short_name")):
            node = astroid.extract_node("long_name,short_name=l")
            self.assertEqual("very_short_name,short_name=l", unparser.unparse(node))
