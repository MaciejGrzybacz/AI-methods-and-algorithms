from typing import Callable, Iterable

from problems import StripsState, StripsProblem, StripsAction
from solvers.solver import Solver
from utils.queues import PriorityQueue
from utils.node import Node
from utils.searchmonitor import SearchTree

Heuristic = Callable[[Node], float | None]


class GenericBestFirstSearch(Solver):
    """
    Type of search that have access to problem definition and to heuristic,
    that allows it estimate which nodes should be searched.
    Compared to the uninformed search, it uses a priority queue,
    sorting nodes according the given function.
    """

    def __init__(self, problem: StripsProblem, eval_fun: Heuristic):
        """
        Initializes the search with.

        Parameters:
            problem: the problem to be solved, used to generate the search tree.
            eval_fun: function used to evaluate search three nodes and guide the search
                      lower the value, the better is the state
        """
        super().__init__(problem)
        self.problem = problem
        self.start: StripsState = problem.init_state
        self.root = Node(self.start)
        self.frontier: PriorityQueue = PriorityQueue(eval_fun)
        self.visited = {self.start: float(self.root.cost)}
        self.tree = SearchTree(self.root, generator=self._generator)
        self.closed = 0
        self.opened = 0

    def search_tree(self) -> SearchTree:
        return self.tree

    def metric(self) -> str:
        return f"closed {self.closed} # opened {self.opened}"

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
            if self.problem.satisfies_goals(parent.state):
                return parent
            for child_node in self.tree.expand(parent):
                state = child_node.state
                if state not in self.visited or child_node.cost < self.visited[state]:
                    self.opened += 1
                    self.visited[state] = child_node.cost
                    self.frontier.push(child_node)
                    self.update_metric()
        return None

    def _generator(self, state: StripsState) -> Iterable[tuple[StripsAction, StripsState]]:
        for action in self.problem.actions(state):
            yield action, self.problem.take_action(state, action)