import operator
from math import inf

from base.bot import G, A, Bot
from base.player import Player
from base.score import Score
from base.state import State
from base.action import Action


class Negamax(Bot[G, A]):
    """
    A MiniMax player implemented using Negamax: https://www.wikiwand.com/en/Negamax
    
    Attributes:
    -----------
    visited_nodes: int
        Counts how many game tree nodes have been visited by the algorithm
    """
    visited_nodes: int

    def __init__(self):
        self.visited_nodes = 0
        super().__init__()

    def _choose_action(self, state: State) -> None:
        self.visited_nodes = 0
        self.best_action = self._negamax(state, self.player)[0]

    def _negamax(self, state: State, player: Player) -> tuple[A | None, Score]:
        """ Negamax function following https://www.wikiwand.com/en/Negamax#Negamax_base_algorithm

        Player acts like the `color` parameter from the wikipedia article, but its logic is already included
        in the reward method of the Game class.
        
        Parameters
        ----------
        state: State
            the current state in the game
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

        if self.game.is_terminal_state(state):
            return None, self.game.reward(state, player)

        best_score = Score.LOST
        best_action = None
        possible_actions = self.game.actions_for(state, player)

        for action in possible_actions:
            temp_score = -self._negamax(self.game.take_action(state, action), player.opponent())[1]

            if temp_score > best_score:
                best_score = temp_score
                best_action = action

        return best_action, best_score

    def metric(self) -> str | None:
        return f"Visited {self.visited_nodes} nodes in the game tree."