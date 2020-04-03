from typing import *

from ..name_finder import NameFinder
from ..rules.astroid_rule import AstroidRule
from ..rules.rename_assign_name import RenameAssignName
from ..rules.rename_name import RenameName


class AssignNameOptimizer:
    def __init__(self):
        self.names: List[str] = []

    def add_name(self, name: str) -> None:
        self.names.append(name)

    def generate_rules(self, name_finder: NameFinder) -> List[AstroidRule]:
        rules: List[AstroidRule] = []
        for name in self.names:
            name_finder.add_potential_used_name(name)
        for name in self.names:
            next_name: str = name_finder.next_name()
            print(next_name)
            if len(next_name) < len(name):
                name_finder.pop_next_name()
                rules.append(RenameAssignName(name, next_name))
                rules.append(RenameName(name, next_name))
        return rules
