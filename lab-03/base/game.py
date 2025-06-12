from base.player import Player
from base.score import Score
from base.state import State
from base.action import Action
from typing import TypeVar, Generic
from abc import ABC, abstractmethod
from PIL.Image import Image

S = TypeVar('S', bound=State)
A = TypeVar('A', bound=Action)
G = TypeVar('G', bound='Game')

class Game(ABC, Generic[S, A]):

    @abstractmethod
    def initial_state(self) -> S:
        """Returns an initial state"""

    @abstractmethod
    def actions_for(self, state: S, player: Player) -> list[A]:
        """Generates actions to take from the given state"""

    @abstractmethod
    def take_action(self, state: S, action: A) -> S:
        """Returns new state resulting from taking given action"""

    def reward(self, state: S, player: Player) -> Score:
        """Returns reward for a terminal state. Fails if the state is not terminal"""
        assert self.is_terminal_state(state), "Asking for a reward of a non-terminal state!"
        return self.value_for_terminal(state).for_player(player)
    
    @abstractmethod
    def value_for_terminal(self, state: S) -> Score:
        """Returns value of a terminal state for the max player"""

    @abstractmethod
    def is_terminal_state(self, state: S) -> bool:
        """Returns if given state is a terminal state"""

    def name(self) -> str:
        """Returns short name of the game, optional"""
        return type(self).__name__
    
    def to_ascii(self, state: S) -> str:
        """Converts state to its text representation."""

    def to_image(self, state: S, size: tuple[int, int] = (800, 900)) -> Image | None:
        """Converts state to its image representation."""

    def is_tie(self, state: S) -> bool:
        return (self.is_terminal_state(state)
                and self.value_for_terminal(state) == 0)
