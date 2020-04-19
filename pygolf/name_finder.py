import string
from typing import Set

from pygolf.errors.no_names_left import NoNamesLeftException


class NameFinder:
    def __init__(self) -> None:
        self.names: Set[str] = set(string.ascii_lowercase + string.ascii_uppercase)

    def next_name(self) -> str:
        if self.names:
            return next(iter(self.names))
        else:
            raise NoNamesLeftException

    def pop_next_name(self) -> str:
        if self.names:
            return self.names.pop()
        else:
            raise NoNamesLeftException

    def remove_used_name(self, name: str) -> None:
        if len(name) == 1:
            self.names.remove(name)
