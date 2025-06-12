from dataclasses import dataclass
from gym.core import ActType
import random

from src.action_selection_rules.generic import ActionCandidate, ActionSelectionRule
from src.action_selection_rules.greedy import GreedyActionSelection


@dataclass
class EpsilonGreedyActionSelection(ActionSelectionRule[ActType]):
    """
    This selection policy behave as greedy with chance equal `1 - epsilon`.
    Otherwise, it chooses a random action.
    The idea is to boost the exploration.

    Attributes:
        epsilon: The probability that action will be chosen randomly.
    """
    epsilon: float

    def __init__(self, epsilon: float) -> None:
        """ Initializes selection rule with an epsilon value."""
        self.epsilon = epsilon
        self._greedy_policy = GreedyActionSelection[ActType]()

    def _select_action(self, action_rewards: list[ActionCandidate[ActType]]) -> ActType:
        """
        Selects an action with the highest reward with probability `1 - epsilon`.
        A random action is chosen with probability `epsilon`.
        """
        if random.random() > self.epsilon:
            return self._greedy_policy(action_rewards)
        return random.choice([c for c in action_rewards]).action
    
    def name(self) -> str:
        return f"EpsilonGreedy({self.epsilon})"