import astroid as ast

from pygolf.rules.format_to_f_string import FormatToFString
from pygolf.unparser import Unparser


class Pygolfer:
    def __init__(self):
        self.ast = None
        self.rules = [FormatToFString]
        for rule in self.rules:
            ast.MANAGER.register_transform(rule.on_node, rule.transform, rule.predicate)

    def feed(self, file_path):
        with open(file_path) as f:
            self.ast = ast.parse("".join(f.readlines()))

    def reduce(self, file_path):
        self.feed(file_path)
        unparser = Unparser()
        return unparser.unparse(self.ast)
