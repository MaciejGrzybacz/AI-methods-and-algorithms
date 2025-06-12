import operator

from base.bot import HeuristicBot, A, G, H
from base.heuristic import HeuristicScore
from base.player import Player
from base.score import Score
from base.state import State
from base.action import Action
import math
from typing import Type


class NegamaxAlphaBetaDepth(HeuristicBot[A, G, H]):
    """
    A MiniMax Alpha-Beta with depth limit player implemented using Negamax: https://www.wikiwand.com/en/Negamax
    
    Attributes
    -----------
    visited_nodes: int
        Counts how many game tree nodes have been visited by the algorithm
    pruned: int
        Counts how many times alpha/beta were used to prune the search tree
    max_depth: int
        Search limit for the algorithm
    heuristic: Heuristic
        A heuristic to estimate the state value.
    """
    visited_nodes: int
    pruned: int
    max_depth: int

    def name(self) -> str:
        return f"{type(self).__name__}_{self.max_depth}"

    def __init__(self, heuristic_constructor: Type[H], max_depth: int, ):
        super().__init__(heuristic_constructor)
        self.visited_nodes = 0
        self.pruned = 0
        self.max_depth = max_depth

    def _choose_action(self, state: State) -> None:
        self.visited_nodes = 0
        self.best_action = self._alpha_beta(
            state, self.max_depth, HeuristicScore.worst_possible(), HeuristicScore.best_possible(), self.player)[0]

    def _alpha_beta(self, state: State, depth: int, alpha: HeuristicScore, beta: HeuristicScore, player: Player) \
            -> tuple[A | None, HeuristicScore]:
        """ Negamax function following https://www.chessprogramming.org/Alpha-Beta#Outside_the_Bounds

        Player acts like the `color` parameter from the article, but its logic is already included
        in the reward method of the Game class.
        It has a depth limit to prevent algorithm from breaking the timelimit.
        """
        self.visited_nodes += 1  # to track the progress...

        if self.game.is_terminal_state(state) or depth == 0:
            return None, self.heuristic(state, player)

        best_score = HeuristicScore.worst_possible()
        best_action = None
        possible_actions = self.game.actions_for(state, player)

        for action in possible_actions:
            new_state = self.game.take_action(state, action)
            _, temp_score = self._alpha_beta(
                new_state, depth - 1, -beta, -alpha, player.opponent())
            temp_score = -temp_score

            if temp_score > best_score:
                best_score = temp_score
                best_action = action

            if best_score > alpha:
                alpha = best_score

            if best_score >= beta:
                self.pruned += 1
                break

        return best_action, best_score

    def metric(self) -> str | None:
        return f"Visited {self.visited_nodes} nodes in the game tree. Pruned {self.pruned} branches."