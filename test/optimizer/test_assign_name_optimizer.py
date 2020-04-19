from unittest import TestCase, mock

import astroid

from pygolf.optimizers.assign_name_optimizer import AssignNameOptimizer


class TestAssignNameOptimizer(TestCase):
    def test_visit_assign_name(self):
        with mock.patch("pygolf.name_finder.NameFinder") as mock_name_finder:
            assign_name = astroid.extract_node("a=5").targets[0]
            assign_name_optimizer = AssignNameOptimizer(mock_name_finder)
            assign_name_optimizer.visit(assign_name)
            self.assertEqual(assign_name_optimizer.names, ["a"])
