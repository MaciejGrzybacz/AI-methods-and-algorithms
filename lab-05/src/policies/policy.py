from abc import ABC, abstractmethod
from gym.core import ObsType, ActType
from typing import Generic


class Policy(ABC, Generic[ObsType, ActType]):
    """
    Represents a policy — how the agent should behave given an observation.
    A good policy is an expected result of the reinforcement learning process.
    """
    @abstractmethod
    def select_action(self, from_observation: ObsType) -> ActType:
        """
        Selects an action given the observation.
        Args:
            from_observation: what the agent observes.

        Returns:
            what action will the agent take given the observation.
        """
