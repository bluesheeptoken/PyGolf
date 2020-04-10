from typing import List

from astroid.node_classes import NodeNG

from pygolf.rules import AstroidRule, FormatToFString

from .phase import Phase


class AlwaysApplyPhase(Phase):
    def generate_rules(self, ast: NodeNG) -> List[AstroidRule]:
        return [FormatToFString()]
