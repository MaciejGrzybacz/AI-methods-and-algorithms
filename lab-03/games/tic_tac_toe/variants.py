from typing import List
from base.player import Player
from games.tic_tac_toe.game import TicTacToeGame, TicTacToeGameLogic
from games.tic_tac_toe.pieces import TicTacToeAction, TicTacToeSign, TicTacToeState


class TicTacToeVariant(TicTacToeGame):
    logic: TicTacToeGameLogic

    def __init__(self, logic: TicTacToeGameLogic) -> None:
        self.logic = logic
        super().__init__()

    @property
    def board_size(self) -> int:
        return self.logic.board_size

    @property
    def win_length(self) -> int:
        return self.logic.win_length

    @property
    def loose_length(self) -> int:
        return self.logic.loose_length

    def actions_for(self, state: TicTacToeState, player: Player):
        return self.logic.actions_for(state, player)


class ConnectVariant(TicTacToeVariant):

    def actions_for(self, state: TicTacToeState, player: Player) -> list[TicTacToeAction]:
        actions = super().actions_for(state, player)

        def is_on_bottom(y: int, x: int) -> bool:
            if y == self.board_size - 1:
                return True
            return state.board[y + 1, x] != TicTacToeSign.BLANK

        return [a for a in actions if is_on_bottom(a.y, a.x)]


class TicTacToe(TicTacToeVariant):

    def __init__(self):
        super().__init__(TicTacToeGameLogic(3, 3))


class Gomoku(TicTacToeVariant):

    def __init__(self):
        super().__init__(TicTacToeGameLogic(15, 5))


class GomokuSmall(TicTacToeVariant):

    def __init__(self):
        super().__init__(TicTacToeGameLogic(8, 4))


class GomokuTiny(TicTacToeVariant):

    def __init__(self):
        super().__init__(TicTacToeGameLogic(5, 4))


class Iieshimoku(TicTacToeVariant):

    def __init__(self):
        super().__init__(TicTacToeGameLogic(15, 5, 4))


class IieshimokuSmall(TicTacToeVariant):

    def __init__(self):
        super().__init__(TicTacToeGameLogic(8, 4, 3))


class IieshimokuTiny(TicTacToeVariant):

    def __init__(self):
        super().__init__(TicTacToeGameLogic(5, 4, 3))


class ConnectFive(ConnectVariant):

    def __init__(self):
        super().__init__(TicTacToeGameLogic(9, 5))


class ConnectFour(ConnectVariant):

    def __init__(self):
        super().__init__(TicTacToeGameLogic(7, 4))


class ConnectThree(ConnectVariant):

    def __init__(self):
        super().__init__(TicTacToeGameLogic(5, 3))
