import time
from abc import ABC, abstractmethod
from collections.abc import Callable

from problems import StripsProblem, StripsAction


class Solver(ABC):
    """
    Abstract base class for solvers, handling all the extra logic
    required to monitor solving process...

    The main thing left to be implements is the "solve" method.
    """
    problem: StripsProblem
    update_interval: float
    last_update_time: float
    callback: Callable[[str], None]

    def __init__(self, problem: StripsProblem, update_interval: float = 0.033) -> None:
        super().__init__()
        self.problem = problem
        self.update_interval = update_interval
        self.callback = lambda _: None
        self.last_update_time = time.time()

    def register_callback(self, callback: Callable[[str], None]) -> None:
        self.callback = callback

    def update_metric(self) -> None:
        if time.time() - self.last_update_time > self.update_interval:
            self.callback(self.metric())
            self.last_update_time = time.time()

    @abstractmethod
    def metric(self) -> str:
        """Returns information about the search process, e.g., how much has is explored"""

    @abstractmethod
    def solve(self) -> list[StripsAction] | None:
        """
        Solves the problem providing a sequence of actions

        Returns:
            None if no solution was found, otherwise a plan is returned.
        """
