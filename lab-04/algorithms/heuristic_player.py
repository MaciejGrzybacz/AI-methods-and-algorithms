from typing import List, Tuple, Type

from base.action import Action
from base.bot import Bot, G, A, H, HeuristicBot
from base.score import Score
from base.state import State
from random import shuffle


class HeuristicPlayer(HeuristicBot[G,A,H]):
    """
    This player chooses the action maximising the given heuristic.
    """
    def __init__(self, heuristic_constructor: Type[H]):
        super().__init__(heuristic_constructor)


    def _choose_action(self, state: State) -> None:
        actions = self.game.actions_for(state, self.player)
        # scored_actions = [(score, action), ...]
        scored_actions = ([ (self.heuristic(self.game.take_action(state, a), self.player), a) for a in actions ])
        shuffle(scored_actions) # shuffle the states to make the player a bit less predicatable
        self.best_action = max(scored_actions, key=lambda s: s[0])[1]