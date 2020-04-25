from typing import List

import astroid as ast
from astroid.node_classes import NodeNG

from pygolf.optimization_phases import all_phases
from pygolf.rules import AstroidRule
from pygolf.unparser import Unparser


class Pygolfer:
    def shorten(self, code: str) -> str:
        module: NodeNG = ast.parse(code)
        unparser: Unparser = Unparser()
        rules: List[AstroidRule] = []

        for phase in all_phases:
            for rule in phase.generate_rules(module):
                ast.MANAGER.register_transform(rule.on_node, rule.transform, rule.predicate)
                rules.append(rule)

            module = ast.parse(unparser.unparse(module))

        for rule in rules:
            ast.MANAGER.unregister_transform(rule.on_node, rule.transform, rule.predicate)
        return unparser.unparse(module)
