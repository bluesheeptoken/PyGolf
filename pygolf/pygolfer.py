import astroid as ast
from astroid.node_classes import NodeNG

from pygolf.optimization_phases import all_phases
from pygolf.unparser import Unparser


class Pygolfer:
    def shorten(self, code: str) -> str:
        module: NodeNG = ast.parse(code)
        unparser: Unparser = Unparser()

        for phase in all_phases:
            for rule in phase.generate_rules(module):
                ast.MANAGER.register_transform(
                    rule.on_node, rule.transform, rule.predicate
                )

            module = ast.parse(unparser.unparse(module))

        return unparser.unparse(module)
