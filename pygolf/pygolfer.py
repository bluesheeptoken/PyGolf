from typing import *

import astroid as ast
from astroid.node_classes import NodeNG

from pygolf.optimization_phases import all_phases
from pygolf.rules import AstroidRule, FormatToFString
from pygolf.unparser import Unparser


def _apply_rules(rules: List[AstroidRule]) -> None:
    for rule in rules:
        ast.MANAGER.register_transform(rule.on_node, rule.transform, rule.predicate)


def base_rules() -> List[AstroidRule]:
    return [FormatToFString()]


class Pygolfer:
    def shorten(self, code: str) -> str:
        module: NodeNG = ast.parse(code)
        unparser: Unparser = Unparser()

        for phase in all_phases:
            rules = phase.generate_rules(module)
            _apply_rules(rules)
            module = ast.parse(unparser.unparse(module))

        return unparser.unparse(module)
