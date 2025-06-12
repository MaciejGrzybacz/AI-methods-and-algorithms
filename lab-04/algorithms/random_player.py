from random import choice

from base.bot import Bot
from base.state import State


class RandomPlayer(Bot):
    """Chooses a random action."""
    def __init__(self):
        super().__init__()

    def _choose_action(self, state: State) -> None:
        self.best_action = choice(
            self.game.actions_for(state, self.player))
