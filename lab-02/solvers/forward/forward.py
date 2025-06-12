from typing import Callable

from problems import StripsProblem
from solvers.solver import Solver
from solvers.forward.generic_forward import ForwardUninformedSearch
from utils.queues import FIFO, LIFO


class ForwardBFS(Solver):
    """A basic forward solver exploring states in the breadth-first manner"""
    def __init__(self, problem: StripsProblem):
        super().__init__(problem)
        self.search = ForwardUninformedSearch(problem, FIFO())

    def solve(self):
        return self.search.solve()

    def metric(self) -> str:
        return self.search.metric()

    def register_callback(self, callback: Callable[[str], None]) -> None:
        self.search.register_callback(callback)


class ForwardDFS(Solver):
    """A basic forward solver exploring states in the depth-first manner"""
    def __init__(self, problem: StripsProblem):
        super().__init__(problem)
        self.search = ForwardUninformedSearch(problem, LIFO())

    def solve(self):
        return self.search.solve()

    def metric(self) -> str:
        return self.search.metric()

    def register_callback(self, callback: Callable[[str], None]) -> None:
        self.search.register_callback(callback)