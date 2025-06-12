from typing import Union
from local_search.algorithms.hill_climbing.hill_climbing import HillClimbing

from local_search.problems.base.state import State
from local_search.problems.base.problem import Problem


class BestChoiceHillClimbing(HillClimbing):
    """
    Implementation of hill climbing local search.

    The most known version of hill climbing.
    Algorithm works, by checking all the available moves
    and selecting the best one that improves the current state.
    """

    def _climb_the_hill(self, model: Problem, state: State) -> Union[State, None]:
        best_neighbor = None
        best_improvement = 0

        for neighbor in self._get_neighbours(model, state):
            improvement = model.improvement(neighbor, state)

            if improvement > best_improvement:
                best_improvement = improvement
                best_neighbor = neighbor

        return best_neighbor if best_neighbor else state