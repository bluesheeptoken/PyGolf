from typing import *

import astroid as ast
from astroid.node_classes import NodeNG

from pygolf.abstract_optimizer.abstract_optimizer import AbstractOptimizer
from pygolf.name_finder import NameFinder
from pygolf.rules.astroid_rule import AstroidRule
from pygolf.rules.format_to_f_string import FormatToFString
from pygolf.unparser import Unparser


def generate_rules(ast: "NodeNG") -> List[AstroidRule]:
    name_finder = NameFinder()
    optimizer = AbstractOptimizer(name_finder)
    optimizer.visit(ast)
    rules = optimizer.generate_optimizations_rules()
    return rules


def read_ast(file_path):
    with open(file_path) as f:
        return ast.parse("".join(f.readlines()))


def _apply_rules(rules: List[AstroidRule]) -> None:
    for rule in rules:
        ast.MANAGER.register_transform(rule.on_node, rule.transform, rule.predicate)


class Pygolfer:
    def reduce(self, file_path):
        old_ast = read_ast(file_path)
        rules = generate_rules(old_ast)
        _apply_rules(rules)
        new_ast = read_ast(file_path)

        unparser = Unparser()
        return unparser.unparse(new_ast)
