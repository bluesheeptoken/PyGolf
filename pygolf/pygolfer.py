from typing import *

import astroid as ast
from astroid.node_classes import NodeNG

from pygolf.abstract_optimizer.abstract_optimizer import AbstractOptimizer
from pygolf.name_finder import NameFinder
from pygolf.rules import AstroidRule, FormatToFString
from pygolf.unparser import Unparser


def generate_rules(ast: NodeNG) -> List[AstroidRule]:
    name_finder = NameFinder()
    optimizer = AbstractOptimizer(name_finder)
    optimizer.visit(ast)
    rules = optimizer.generate_optimizations_rules()
    return rules


def _apply_rules(rules: List[AstroidRule]) -> None:
    for rule in rules:
        ast.MANAGER.register_transform(rule.on_node, rule.transform, rule.predicate)


def base_rules() -> List[AstroidRule]:
    return [FormatToFString()]


class Pygolfer:
    def reduce(self, code: str) -> str:
        old_ast: NodeNG = ast.parse(code)
        rules: List[AstroidRule] = generate_rules(old_ast)
        _apply_rules(rules)
        new_ast: NodeNG = ast.parse(code)

        unparser: Unparser = Unparser()
        return unparser.unparse(new_ast)
