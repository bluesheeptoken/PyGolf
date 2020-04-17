import unittest
from test.rules.helper import register_rule

import astroid

from pygolf.rules import DefineRenameCall
from pygolf.unparser import Unparser


class TestDefineRenameCall(unittest.TestCase):
    def test_rule(self):
        unparser = Unparser()

        with register_rule(DefineRenameCall("method_name", "new_method_name")):
            node = astroid.parse("")
            unparsed = unparser.unparse(node)
            self.assertEqual(unparsed, "new_method_name=method_name")

            node = astroid.parse(unparsed)
            unparsed = unparser.unparse(node)
            self.assertEqual(unparsed, "new_method_name=method_name")
