import inspect
from base.game import Game
from base.heuristic import Heuristic
from base.player import Player
from base.state import State
from base.action import Action
from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar

G = TypeVar('G', bound=Game)
H = TypeVar('H', bound=Heuristic)
A = TypeVar('A', bound=Action)
B = TypeVar('B', bound='Bot')


class Bot(ABC, Generic[G, A]):
    game: G
    player: Player    
    _best_action: A | None

    def __init__(self):
        self.game = None
        self.player = None
        self._best_action = None

    @property
    def best_action(self) -> A | None:
        return self._best_action

    @best_action.setter
    def best_action(self, a: A | None) -> None:
        assert not a or isinstance(
            a, Action), f"Invalid action type '{type(a)}'"
        self._best_action = a

    def choose_action(self, state: State) -> None:
        assert self.game is not None and self.player is not None, "Bot is not setup to game. Call `setup` method first."
        self._choose_action(state)

    @abstractmethod
    def _choose_action(self, state: State) -> None:
        """
        Finds the optimal action for the state and assigns it to the `best_action` property.
        """

    def metric(self) -> str | None:
        """
        Returns a metric, how much work the bot has done. It's optional.
        """
        return None
    
    def name(self) -> str:
        """
        Returns a metric, how much work the bot has done. It's optional.
        """
        return type(self).__name__

    def setup(self: B, game: G, player: Player) -> B:
        """
        Configures Bot so it would be possible to use it in game.        
        """
        self.game = game
        self.player = player
        self.best_action = None # clears action in case Bot was reused
        return self


class HeuristicBot(Bot[G, A], ABC, Generic[A, G, H]):
    def __init__(self, heuristic: Type[H]):
        super().__init__()
        self.heuristic_constructor = heuristic

    def setup(self: B, game: G, player: Player) -> B:
        self.heuristic = self.heuristic_constructor(game)
        super().setup(game, player)

    def name(self) -> str:
        """
        Returns a metric, how much work the bot has done. It's optional.
        """
        return f"{type(self).__name__}_{self.heuristic_constructor.__name__}"
        
