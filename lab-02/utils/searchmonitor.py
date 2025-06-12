from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Callable, Iterable, Iterator
from problems import StripsState, StripsAction
from utils.node import Node

class SearchTree:
    """
    This class represents the search tree expanded by a state space search algorithm.

    Attributes:
    ===========
    root: Node
        root of the utils
        set up in the __init__
    generator:
        a function generating successors for a give state

    Methods:
    ========
    expand(problem, node: Node) -> Iterator[Node]:
        allows to iterate over all the possible children of the given node
    """

    def __init__(self, root: Node, generator: Callable[[StripsState], Iterable[tuple[StripsAction, StripsState]]]):
        super().__init__()
        self.root = root
        self.generator = generator

    def expand(self, node: Node) -> Iterator[Node]:
        for action, state in self.generator(node.state):
            child_node = Node(
                state=state,
                parent=node,
                cost=node.cost + 1,
                action=action
            )
            yield child_node
