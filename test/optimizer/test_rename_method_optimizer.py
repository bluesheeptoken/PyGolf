from unittest import TestCase

import astroid

from pygolf.name_finder import NameFinder
from pygolf.optimizers.rename_method_optimizer import RenameMethodOptimizer
from pygolf.rules import DefineRenameCall, RenameCall


class TestRenameMethodOptimizer(TestCase):
    def test_generate_rules(self):
        rename_method_optimizer = RenameMethodOptimizer(NameFinder())
        next_name = rename_method_optimizer.name_finder.next_name()
        rename_method_optimizer.visit(astroid.extract_node("print(2)"))
        rename_method_optimizer.visit(astroid.extract_node("print(2)"))
        rename_method_optimizer.visit(astroid.extract_node("print(2)"))
        rename_method_optimizer.visit(astroid.extract_node("print(2)"))
        rename_method_optimizer.visit(astroid.extract_node("print(2)"))
        rename_method_optimizer.visit(astroid.extract_node("input()"))
        rules = list(rename_method_optimizer.generate_rules())
        self.assertEqual(rules, [RenameCall("print", next_name), DefineRenameCall("print", next_name)])
