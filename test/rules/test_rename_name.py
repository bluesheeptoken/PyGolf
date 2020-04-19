import unittest
from test.rules.helper import register_rule

import astroid

from pygolf.rules import RenameName
from pygolf.unparser import Unparser


class TestRenameAssign(unittest.TestCase):
    def test_rule(self):
        unparser = Unparser()

        with register_rule(RenameName("long_name", "very_short_name")) as transformer:
            node = transformer.visit(astroid.parse("print(long_name)"))
            self.assertEqual("print(very_short_name)", unparser.unparse(node))
