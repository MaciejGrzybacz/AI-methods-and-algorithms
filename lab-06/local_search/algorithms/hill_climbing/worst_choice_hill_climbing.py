from typing import Union
from local_search.algorithms.hill_climbing.hill_climbing import HillClimbing
from local_search.problems.base.state import State
from local_search.problems.base.problem import Problem


class WorstChoiceHillClimbing(HillClimbing):
    """
    Implementation of hill climbing local search.

    Pretty exotic version of hill climbing. Algorithm works, by checking all the available moves
    and selecting the worst one that improves the current state.
    """

    def _climb_the_hill(self, model: Problem, state: State) -> Union[State, None]:
        worst_improvement = float('inf')
        worst_improving_neighbor = None

        for neighbor in self._get_neighbours(model, state):
            improvement = model.improvement(neighbor, state)

            if 0 < improvement < worst_improvement:
                worst_improvement = improvement
                worst_improving_neighbor = neighbor

        return worst_improving_neighbor if worst_improving_neighbor else state
