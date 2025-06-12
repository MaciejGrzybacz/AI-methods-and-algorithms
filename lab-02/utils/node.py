from __future__ import annotations
from dataclasses import dataclass
from problems import StripsState, StripsAction


@dataclass
class Node:
    state: StripsState
    parent: Node | None = None
    action: StripsAction | None = None
    cost: float = 0

    def __lt__(self, other):
        return self.cost < other.cost

    def __str__(self) -> str:
        return str(self.state)

    def __repr__(self) -> str:
        return f"<{str(self.parent)} --{self.action}--> {str(self.state)}. cost: {self.cost}>"

    def path(self) -> list[Node]:
        node: Node | None = self 
        path: list[Node] = []
        while node:
            path.append(node)
            node = node.parent
        return path[::-1]


