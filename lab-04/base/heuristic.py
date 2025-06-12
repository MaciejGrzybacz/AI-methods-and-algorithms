from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from base.player import Player
from base.state import State
from base.game import Game, Score
import math
from typing import NamedTuple, TypeVar, Generic, Any

S = TypeVar('S', bound=State)
G = TypeVar('G', bound=Game)



class HeuristicScore(NamedTuple):
    """
    A thin wrapper over the heuristic results.
    It is a named tuple of shape (Score, float).
    Thanks to that heuristic scores are first compared by the score,
    and only later by the heuristic value.
    """
    score: Score
    value: float

    def __neg__(self):
        '''So programmer can write `-score` as it was a number'''
        return HeuristicScore(-self.score, -self.value)
    
    @staticmethod
    def best_possible() -> HeuristicScore:
        '''The best possible score one can achieve'''
        return HeuristicScore(Score.WON, math.inf)
    
    @staticmethod
    def worst_possible() -> HeuristicScore:
        '''The worst possible score one can achieve'''
        return HeuristicScore(Score.LOST, -math.inf)


class Heuristic(ABC, Generic[S]):

    def __init__(self, game: Game[S, Any]) -> None:
        """Creates a heuristic for the given game"""
        self.game = game

    def __call__(self, state: S, player: Player) -> HeuristicScore:
        return HeuristicScore(self.game.reward(state, player) if self.game.is_terminal_state(state) else Score.TIE, 
                              self.value(state) * player)

    @abstractmethod
    def value(self, state: S) -> float:
        """Calculates value for a given state depending on the chances to win from that state
           Should be calculated from the max_player perspective.
           Should give MAX value when the MAX Player is expected to win, MIN value
        """