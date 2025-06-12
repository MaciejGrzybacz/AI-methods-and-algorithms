from base.bot import Bot, G, A
from base.score import Score
from base.state import State


class NearSighted(Bot[G, A]):
    """A nearsighted bot looking two moves ahead and avoids loosing.
       It's like minimax without heuristic with depth limit = 2
    """

    def __init__(self):
        super().__init__()

    def _choose_action(self, state: State) -> None:
        def is_losing_state(s: State) -> bool:
            return self.game.is_terminal_state(s) and self.game.reward(s, self.player) == Score.LOST

        def is_winning_state(s: State) -> bool:
            return self.game.is_terminal_state(s) and self.game.reward(s, self.player) == Score.WON

        def worst_case(s: State) -> Score:
            opponent_actions = self.game.actions_for(s, self.player.opponent())
            opponent_states = [self.game.take_action(s, a) for a in opponent_actions]
            if any(is_losing_state(s) for s in opponent_states):
                return Score.LOST
            if all(is_winning_state(s) for s in opponent_states):
                return Score.WON
            return Score.TIE

        current_actions = self.game.actions_for(state, self.player)
        states = {self.game.take_action(state, a): a for a in current_actions}

        # if we can win in a single move, let's do this move!
        winning_states = {s: a for s, a in states.items() if is_winning_state(s)}
        if len(winning_states) > 0:
            self.best_action = list(winning_states.values())[0]

        # let's ignore actions that lead to a losing state
        states = {s: a for s, a in states.items() if not is_losing_state(s)}
        if len(states) == 0:
            # all actions lead to a losing state... let's do anything...
            self.best_action = current_actions[0]

        # for every state, let's check what is the worst thing our opponent can do to harm us
        worst_cases = {worst_case(s): a for s, a in states.items()}
        if Score.WON in worst_cases:
            # in this state opponent has to lose!
            self.best_action = worst_cases[Score.WON]
        if Score.TIE in worst_cases:
            # in this state opponent cannot win
            self.best_action = worst_cases[Score.TIE]

        # we have to lose :(
        return current_actions[0]
