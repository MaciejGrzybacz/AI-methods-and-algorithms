from dataclasses import dataclass
from gym.core import ActType
import random
from src.action_selection_rules.epsilon_greedy import EpsilonGreedyActionSelection

from src.action_selection_rules.generic import ActionCandidate, ActionSelectionRule

@dataclass
class EpsilonGreedyActionSelectionWithDecayEpsilon(ActionSelectionRule[ActType]):
    """
        This selection policy behave as greedy with chance equal `1 - epsilon`.
        Otherwise, it chooses a random action.
        The main twist is that the epsilon decays with time, so the selection
        is more exploring in the beginning, then becomes more and more greedy.

        Attributes:
            epsilon: The current probability that action will be chosen randomly.
            decay_step: How quickly the epsilon decays.
            init_epsilon: The initial epsilon value (before the decay).
    """
    epsilon: float
    decay_step: float
    init_epsilon: float

    def __init__(self, epsilon: float, decay_step: float):
        self.epsilon = epsilon
        self.decay_step = decay_step
        self.init_epsilon = epsilon

    def _select_action(self, action_rewards: list[ActionCandidate[ActType]]) -> ActType:
        """ Chooses an action according to the Epsilon Greedy rule.
            Then decreases the epsilon
        """
        epsilon_greedy_action_selection = EpsilonGreedyActionSelection[ActType](self.epsilon)
        action = epsilon_greedy_action_selection(action_rewards)
        self.epsilon *= self.decay_step
        return action
    
    def name(self) -> str:
        return f"EpsilonGreedyDecay({self.init_epsilon}, {self.decay_step})"
    