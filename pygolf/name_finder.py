import string
from typing import List, Set

from pygolf.errors.no_names_left import NoNamesLeftException


class NameFinder:
    def __init__(self) -> None:
        self.names: List[str] = list(string.ascii_lowercase + string.ascii_uppercase)
        self.forbidden_names: Set[str] = set()

    def next_name(self) -> str:
        self._remove_forbidden_names()
        if self.names:
            return self.names[-1]
        else:
            raise NoNamesLeftException

    def pop_next_name(self) -> str:
        self._remove_forbidden_names()
        if self.names:
            return self.names.pop()
        else:
            raise NoNamesLeftException

    def _remove_forbidden_names(self):
        while self.names and self.names[-1] in self.forbidden_names:
            self.names.pop()

    def remove_used_name(self, name: str) -> None:
        if len(name) == 1:
            self.forbidden_names.add(name)
