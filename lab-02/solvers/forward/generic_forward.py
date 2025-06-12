from typing import Iterable

from problems import StripsState
from problems.action import StripsAction
from problems.problem import StripsProblem
from solvers.solver import Solver
from utils.node import Node
from utils.searchmonitor import SearchTree
from utils.queues import Queue


class ForwardUninformedSearch(Solver):
    """
    The basic forward search exploring the states without any extra information/heuristic.
    The order of the search may be controlled by providing a queue in the constructor.
    """

    def __init__(self, problem: StripsProblem, queue: Queue):
        super().__init__(problem)
        self.problem = problem
        self.start = problem.init_state
        self.frontier = queue
        self.visited = {self.start}
        self.root = Node(self.start)
        self.tree = SearchTree(self.root, lambda s: self._generator(s))
        self.closed = 0
        self.opened = 0

    def metric(self) -> str:
        return f"closed: {self.closed} # opened: {self.opened}"

    def search_tree(self) -> SearchTree:
        return self.tree

    def solve(self) -> list[StripsAction] | None:
        node = self.search()

        if node is None:
            return None

        path = node.path()

        if len(path) == 0:
            return []

        actions: list[StripsAction] = [n.action for n in path[1:]]
        return actions

    def search(self) -> Node | None:
        self.closed, self.opened = 0, 0
        self.frontier.push(self.root)
        while not self.frontier.is_empty():
            parent = self.frontier.pop()
            self.closed += 1
            self.update_metric()
            for child_node in self.tree.expand(parent):
                if self.problem.satisfies_goals(child_node.state):
                    return child_node
                if child_node.state not in self.visited:
                    self.opened += 1
                    self.update_metric()
                    self.frontier.push(child_node)
                    self.visited.add(child_node.state)
        return None

    def _generator(self, state: StripsState) -> Iterable[tuple[StripsAction, StripsState]]:
        for action in self.problem.actions(state):
            new_state = self.problem.take_action(state, action)
            yield action, new_state