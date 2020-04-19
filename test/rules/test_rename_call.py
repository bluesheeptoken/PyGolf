import unittest
from test.rules.helper import register_rule

import astroid

from pygolf.rules import RenameCall
from pygolf.unparser import Unparser


class TestRenameCall(unittest.TestCase):
    def test_rule(self):
        unparser = Unparser()

        with register_rule(RenameCall("method_name", "new_method_name")) as transformer:
            node = transformer.visit(astroid.parse("method_name(2)"))
            self.assertEqual("new_method_name(2)", unparser.unparse(node))
