from datetime import datetime
import operator
from random import shuffle
import time

from base.bot import HeuristicBot, A, G, H
from base.player import Player
from base.score import Score
from base.state import State
from base.heuristic import HeuristicScore
from base.action import Action
import math
from typing import Type


class NegamaxAlphaBetaIDS(HeuristicBot[A, G, H]):
    """
    A configurable MiniMax Alpha-Beta with depth limit player implemented using Negamax: https://www.wikiwand.com/en/Negamax
    
    Attributes
    -----------
    visited_nodes: int
        Counts how many game tree nodes have been visited by the algorithm
    explored_level: int
        Which was the maximal tree level explored in the last run
    explored_all: bool
        Whether the algorithm explored the whole tree
    pruned: int
        Counts how many times alpha/beta were used to prune the search tree
    move_timeout: int
        How much time we have for the move.
    heuristic: Heuristic
        A heuristic to estimate the state value.
    reorder_actions: bool
        Whether the algorithm should try to reorder actions.
    prune_branches: bool
        Whether the algorithm should use alpha/beta pruning
    """
    move_timeout: float
    reorder_actions: bool
    prune_branches: bool
    visited_nodes: int = 0
    explored_level: int = 0
    explored_all: bool = False
    pruned: int = 0

    def name(self) -> str:
        if self.prune_branches:
            return f"NegamaxAlphaBetaIDS_{self.heuristic_constructor.__name__}"
        else:
            return f"NegamaxIDS_{self.heuristic_constructor.__name__}"

    def __init__(self, heuristic_constructor: Type[H], move_timeout: float, reorder_actions: bool = True,
                 prune_branches: bool = True):
        super().__init__(heuristic_constructor)
        self.move_timeout = move_timeout
        self.reorder_actions = reorder_actions
        self.prune_branches = prune_branches

    def _choose_action(self, state: State) -> None:
        self.best_action = None
        self.pruned = 0
        self.visited_nodes = 0
        self.explored_level = 0
        self.explored_all = False

        start = datetime.now()

        def any_time_left() -> bool:
            return (datetime.now() - start).total_seconds() < self.move_timeout

        current_level = 1
        while not self.explored_all and any_time_left():
            self.explored_all = True
            self.best_action = self._alpha_beta(
                state, current_level, HeuristicScore.worst_possible(), HeuristicScore.best_possible(), self.player,
                self.best_action)[0]
            self.explored_level = current_level
            current_level += 1

    def _alpha_beta(self, state: State, depth: int, alpha: HeuristicScore, beta: HeuristicScore, player: Player,
                    last_winner: A | None = None) -> tuple[A | None, HeuristicScore]:
        self.visited_nodes += 1

        if self.game.is_terminal_state(state):
            return None, self.heuristic(state, player)
        
        if depth == 0:
            self.explored_all = False
            return None, self.heuristic(state, player)

        best_score = HeuristicScore.worst_possible()
        best_action = None
        possible_actions = self.game.actions_for(state, player)
        actions = self._reorder_actions(possible_actions, last_winner)

        for action in actions:
            new_state = self.game.take_action(state, action)
            
            _, temp_score = self._alpha_beta(
                new_state, depth - 1, -beta, -alpha, player.opponent(), None)
            
            temp_score = -temp_score

            if temp_score > best_score:
                best_score = temp_score
                best_action = action

            if self.prune_branches and best_score > alpha:
                alpha = best_score

            if self.prune_branches and best_score >= beta:
                self.pruned += 1
                break

        return best_action, best_score

    def _reorder_actions(self, actions: list[A], last_winner: A | None):
        if not self.reorder_actions:
            return actions
        if last_winner is None:
            return actions
        shuffle(actions)

        try:
            idx = actions.index(last_winner)
            actions[0], actions[idx] = actions[idx], actions[0]
        except ValueError:
            pass

        return actions

    def metric(self) -> str | None:
        if self.explored_all:
            return f"Explored the whole tree ({self.explored_level} levels):\n\t- visited {self.visited_nodes} nodes\n\t- pruned {self.pruned} branches"
        return f"Explored {self.explored_level} level of the tree:\n\t- visited {self.visited_nodes} nodes\n\t- pruned {self.pruned} branches"
