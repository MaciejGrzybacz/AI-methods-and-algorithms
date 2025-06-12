from dataclasses import dataclass
from typing import Generic, Tuple, overload
from gym.core import ActType
import numpy as np
from abc import abstractmethod, ABC


@dataclass
class ActionCandidate(Generic[ActType]):
    """
    Represents a candidate action

    Attributes:
        action: the action under consideration
        reward: an expected reward of taking the action
    """
    action: ActType
    reward: float


class ActionSelectionRule(ABC, Generic[ActType]):
    """
    Represents a rule to select an action based on a list of candidates.
    """
    @overload
    def __call__(self, action_rewards: list[ActionCandidate[ActType]]) -> ActType:
        ...

    @overload
    def __call__(self, action_rewards: np.ndarray[Tuple[int], float]) -> ActType:
        ...

    def __call__(self, action_rewards: list[ActionCandidate[ActType]] | np.ndarray) -> ActType:
        """ A wrapper that allows to call the selection rule with both list and numpy array as an argument"""
        if isinstance(action_rewards, np.ndarray):
            action_rewards = [ActionCandidate(
                action, reward) for action, reward in enumerate(action_rewards)]
        return self._select_action(action_rewards)

    @abstractmethod
    def _select_action(self, action_rewards: list[ActionCandidate[ActType]]) -> ActType:
        """ An abstract method to select an action based on a list of candidates """

    @abstractmethod
    def name(self) -> str:
        """ Returns the name of the selection rule """