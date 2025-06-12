import math

from base.heuristic import Heuristic
from games.tic_tac_toe.game import TicTacToeGame
from games.tic_tac_toe.pieces import TicTacToeState


class EmptyTicTacToeHeuristic(Heuristic[TicTacToeState]):
    """A dummy heuristics — always returns 0"""

    game: TicTacToeGame

    def __init__(self, game: TicTacToeGame) -> None:
        self.game = game
        super().__init__(game)

    def value(self, state: TicTacToeState) -> float:
        return 0
    

class NaiveTicTacToeHeuristic(Heuristic[TicTacToeState]):
    """A naive heuristics — use lines exisisting on the board.
       Length of each line is taken to the power of itself (https://www.wikiwand.com/en/Tetration)
       This way the longest lines dominate over the other.
       Then we some the resulting number for our lines
       and substract sum of the opponents' lines.
       """
    game: TicTacToeGame

    def __init__(self, game: TicTacToeGame) -> None:
        self.game = game
        super().__init__(game)

    def value(self, state: TicTacToeState) -> float:
        return sum(l.sign * math.pow(l.length, l.length) for l in state.all_lines())

