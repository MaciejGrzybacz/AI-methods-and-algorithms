import random
from gym.core import ActType
import numpy as np

from src.action_selection_rules.generic import ActionCandidate, ActionSelectionRule


class GreedyActionSelection(ActionSelectionRule[ActType]):
    """
    A greedy selection rule. Always selects an action with the highest reward.
    """
    def _select_action(self, action_rewards: list[ActionCandidate[ActType]]) -> ActType:
        """
        Selects the action with the highest reward.

        Args:
            action_rewards: a list of actions and their corresponding rewards

        Returns:
            an action with the highest reward. In case there are several actions with
            the highest reward, ties are broken randomly..
        """
        rewards = np.array([a.reward for a in action_rewards])
        maxs = np.flatnonzero(rewards == np.max(rewards))
        best = random.choice(maxs)
        return action_rewards[best].action
    
    def name(self) -> str:
        return "Greedy"
