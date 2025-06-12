from dataclasses import dataclass
from typing import Generic
import numpy as np
from gym.core import ObsType, ActType

from src.action_selection_rules.generic import ActionCandidate, ActionSelectionRule


@dataclass
class ActionValuePolicy(Generic[ObsType, ActType]):
    """
    A policy that chooses actions based on the action values (Q-values).

    Attributes:
        action_value_estimates: dict[ObsType, np.ndarray]
            The estimated action values represented as a dictionary.
            Keys are the observation and values are Q-values for every possible action.
        selection_rule: ActionSelectionRule
            The selection rule that determines which action is chosen based on the Q-values.
            After the training, the greedy rule is a most likely to be used.
    """
    action_value_estimates: dict[ObsType, np.ndarray]
    selection_rule: ActionSelectionRule

    def select_action(self, from_observation: ObsType) -> ActType:
        return self.selection_rule(self.action_value_estimates[from_observation])

    def __repr__(self) -> str:
        return f'{type(self).__name__} with {repr(self.selection_rule)}'
