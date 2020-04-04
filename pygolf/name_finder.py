import string
from typing import List, Set


class NameFinder:
    def __init__(self):
        self.names: List[str] = list(string.ascii_lowercase + string.ascii_uppercase)
        self.current_index: int = 0
        self.already_used_names: Set[str] = set()
        self.next_name_index: int = 0

    def next_name(self) -> str:
        if self.next_name_index > self.current_index:
            return self.names[self.next_name_index]
        next_name = self.names[self.next_name_index]
        while next_name in self.already_used_names:
            self.next_name_index += 1
            next_name = self.names[self.next_name_index]
        return next_name

    def pop_next_name(self) -> str:
        next_name = self.next_name()
        self.next_name_index += 1
        self.current_index = self.next_name_index
        return next_name

    def next_k_names(self, k: int) -> List[str]:
        initial_index = self.current_index
        next_names: List[str] = []
        while len(next_names) < k:
            next_names.append(self.pop_next_name())
        self.current_index = initial_index
        return next_names

    def add_potential_used_name(self, name: str) -> bool:
        if len(name) == 1:
            self.already_used_names.add(name)
            return True
        return False
