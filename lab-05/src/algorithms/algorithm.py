from abc import ABC, abstractmethod
import gym
from typing import Generic, TypeVar
from gym.core import ObsType, ActType

        
PolicyType = TypeVar("PolicyType")
class Algorithm(Generic[ObsType, ActType, PolicyType],ABC):
    """
    Abstract base class for reinforcement learning algorithms.
    There are three parameters of this class:
    - `ObsType`: what the agent observes (a state)
    - `ActType`: what are the actions the agent can take
    - `PolicyType`: what type of policy the algorithm produces

    """
    def __init__(self) -> None:
        ...

    @abstractmethod
    def run(self, n_episodes: int, env: gym.Env[ObsType, ActType]) -> PolicyType:
        """
        Runs the reinforcement learning algorithm for given number of episodes.

        Args:
            n_episodes: how many episodes should algorithm play
            env: the environment the algorithm acts in

        Returns:
            a trained policy
        """
    
    @abstractmethod
    def name(self) -> str:
        """ Returns the name of the algorithm for the display purposes """
    