import math
import operator

from base.bot import Bot, G, A
from base.player import Player
from base.score import Score
from base.state import State


class NegamaxAlphaBeta(Bot[G, A]):
    """
    A MiniMax Alpha-Beta player implemented using Negamax: https://www.wikiwand.com/en/Negamax
    
    Attributes:
    -----------
    visited_nodes: int
        Counts how many game tree nodes have been visited by the algorithm
    pruned: int
        Counts how many times alpha/beta were used to prune the search tree
    """
    visited_nodes: int
    pruned: int

    def __init__(self):
        self.visited_nodes = 0
        self.pruned = 0
        super().__init__()

    def _choose_action(self, state: State) -> None:
        self.visited_nodes = 0
        self.pruned = 0
        self.best_action = self._alpha_beta(
            state, Score.LOST, Score.WON, self.player)[0]

    def _alpha_beta(self, state: State, alpha: Score, beta: Score, player: Player) -> tuple[A | None, Score]:
        """ Negamax function following https://www.chessprogramming.org/Alpha-Beta#Outside_the_Bounds

        Player acts like the `color` parameter from the article, but its logic is already included
        in the reward method of the Game class.
        
        Parameters
        ----------
        state: State
            the current state in the game
        alpha: Score
            current lower bound for the final score
        beta: Score
            current upper bound for the final score
        player: Player
            the player that is supposed to move at the given state    
        
        Returns
        -------
        tuple[Action | None, Score]:
            - the first tuple element is the action, that player would choose at the state;
            it should be equal None if the state is terminal and there is no action to make
            - the second tuple element is the score got by the player by following the action
        """
        self.visited_nodes += 1

        best_score = Score.LOST
        best_action = None
        possible_actions = self.game.actions_for(state, player)

        for action in possible_actions:
            score = -self._alpha_beta(self.game.take_action(state, action), -beta, -alpha, player.opponent())[1]

            if score > best_score:
                best_score = score
                best_action = action

            if score > alpha:
                alpha = score

            if alpha >= beta:
                self.pruned += 1
                break

        return best_action, best_score

    def metric(self) -> str | None:
        return f"Visited {self.visited_nodes} nodes in the game tree. Pruned {self.pruned} branches."
