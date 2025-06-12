from typing import Callable

from problems import StripsAction, StripsProblem
from solvers.fast_forward.generic_best_first_search import GenericBestFirstSearch, Heuristic
from solvers.fast_forward.heuristic.relaxed_solver import RelaxedGraphPlan
from solvers.solver import Solver
from utils.node import Node


class FastForward(Solver):
    """
    FastForward is a greedy algorithm exploring the search space
    according to the heuristic based on the relaxed problem
    (missing the "del" effects).
    """

    def __init__(self, problem: StripsProblem):
        """Initializes the FastForward solver"""
        super().__init__(problem)
        self.heuristics = RelaxedGraphPlan(problem)
        self.search = GenericBestFirstSearch(problem, self.evaluation_function)

    def evaluation_function(self, node: Node) -> float:
        h_value = self.heuristics(node.state)
        if h_value is None:
            return float('inf')
        return h_value

    def solve(self) -> list[StripsAction] | None:
        return self.search.solve()

    def metric(self) -> str:
        return self.search.metric()

    def register_callback(self, callback: Callable[[str], None]) -> None:
        self.search.register_callback(callback)


class NotSoFastForward(Solver):
    """
       NotSoFastForward(tm) is just an A* search using the same heuristic as FastForward
    """

    def __init__(self, problem: StripsProblem):
        """Initializes the NotSoFastForward solver"""
        super().__init__(problem)
        self.heuristics = RelaxedGraphPlan(problem)
        self.search = GenericBestFirstSearch(problem, self.evaluation_function)

    def evaluation_function(self, node: Node) -> float:
        h_value = self.heuristics(node.state)
        if h_value is None:
            return float('inf')
        return node.cost + h_value

    def solve(self) -> list[StripsAction] | None:
        return self.search.solve()

    def register_callback(self, callback: Callable[[str], None]) -> None:
        self.search.register_callback(callback)

    def metric(self) -> str:
        return self.search.metric()
