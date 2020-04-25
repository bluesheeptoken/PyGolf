from unittest import TestCase

import astroid

from pygolf.name_finder import NameFinder
from pygolf.optimizers.assign_name_optimizer import AssignNameOptimizer
from pygolf.rules import RenameAssignName, RenameName


class TestAssignNameOptimizer(TestCase):
    def test_visit_assign_name(self):
        assign_name_optimizer = AssignNameOptimizer(NameFinder())
        assign_name = astroid.extract_node("a=5").targets[0]

        assign_name_optimizer.visit(assign_name)
        self.assertEqual(assign_name_optimizer.names, ["a"])

    def test_generate_rules(self):
        assign_name_optimizer = AssignNameOptimizer(NameFinder())
        next_name = assign_name_optimizer.name_finder.next_name()
        assign_name_optimizer.visit(astroid.extract_node("long_name=3").targets[0])
        assign_name_optimizer.visit(astroid.extract_node("a=3").targets[0])
        rules = list(assign_name_optimizer.generate_rules())
        self.assertEqual(rules, [RenameAssignName("long_name", next_name), RenameName("long_name", next_name)])
