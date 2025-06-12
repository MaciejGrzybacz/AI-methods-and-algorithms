from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np
from PIL import Image, ImageFont

from base.game import Game
from base.player import Player
from base.score import Score
from games.tic_tac_toe.pieces import TicTacToeAction, TicTacToeLine, TicTacToeSign, TicTacToeState
from utils.pil_utils import GridDrawer


class TicTacToeGame(Game[TicTacToeState, TicTacToeAction], ABC):

    @property
    @abstractmethod
    def board_size(self) -> int:
        """Height/width of the game board"""

    @property
    @abstractmethod
    def win_length(self) -> int:
        """How long has to be the line to win"""

    @property
    @abstractmethod
    def loose_length(self) -> int:
        """How long has to be the line to loose"""

    def initial_state(self) -> TicTacToeState:
        return TicTacToeState.empty(self.board_size, TicTacToeSign.from_player(Player.MAX))

    def take_action(self, state: TicTacToeState, action: TicTacToeAction) -> TicTacToeState:
        return state.take_action(action)

    def is_terminal_state(self, state: TicTacToeState) -> bool:
        return (TicTacToeSign.BLANK not in state.board) or (self.current_score(state)[0] != Score.TIE)

    def value_for_terminal(self, state: TicTacToeState):
        return self.current_score(state)[0]

    def current_score(self, state: TicTacToeState) -> tuple[Score, TicTacToeLine | None]:
        lines = state.all_lines()
        if len(lines) == 0:
            return Score.TIE, None

        max_line = max(lines, key=lambda l: l.length)
        max_length = max_line.length

        if max_length < min(self.win_length, self.loose_length):
            return Score.TIE, None

        player = max_line.sign.to_player()
        score = Score.WON.for_player(player)

        if self.loose_length <= max_length < self.win_length:
            score = Score.LOST.for_player(player)
        if self.win_length < self.loose_length <= max_length:
            score = Score.LOST.for_player(player)

        return score, max_line

    def actions_for(self, state: TicTacToeState, player: Player) -> list[TicTacToeAction]:
        sign = TicTacToeSign.from_player(player)

        if sign != state.current_sign:
            return []

        return [TicTacToeAction(sign, index) for index in np.ndindex(state.board.shape)
                if state.board[index] == TicTacToeSign.BLANK]

    def to_ascii(self, state: TicTacToeState) -> str:
        width = (self.board_size * 2 + 1)
        line = '-' * (self.board_size * 2 + 1)
        is_terminal = self.is_terminal_state(state)
        score, _ = self.current_score(state)
        header = self._header(state, is_terminal, score)
        padding = ' ' * (((width - len(header)) // 2) - 1)
        ascii = ' ' + padding + '|' + header + '|' + padding
        ascii += '\n' + line + '\n'

        actions = set() if is_terminal else set(
            (a.x, a.y) for a in self.actions_for(state, state.current_sign.to_player()))
        n_actions = len(actions)
        n_empty_fields = 0 if is_terminal else np.count_nonzero(state.board == TicTacToeSign.BLANK)
        print_question_marks = n_actions < n_empty_fields

        def get_text(xy: tuple[int, int], number: int) -> str:
            if print_question_marks and xy in actions:
                return "?"
            return str(TicTacToeSign(number))

        for y, row in enumerate(state.board):
            ascii += ' '
            ascii += ' '.join([get_text((x, y), c) for x, c in enumerate(row)])
            ascii += '\n'
        ascii += line + '\n'
        return ascii

    def to_image(self, state: TicTacToeState, size: tuple[int, int] = (800, 900)) -> Image.Image:
        background_color = (255, 233, 208)
        image = Image.new("RGB", size, background_color)
        grid_drawer = GridDrawer(image, state.board)
        grid_drawer.draw_grid()
        head_font = ImageFont.truetype("assets/arial.ttf", size=int(grid_drawer.header_height * 0.8))
        font = ImageFont.truetype("assets/arial.ttf", size=int(grid_drawer.cell_height * 0.8))
        colors = {TicTacToeSign.X: (229, 68, 109), TicTacToeSign.O: (46, 134, 171), TicTacToeSign.BLANK: (146, 98, 137)}
        line_colors = {TicTacToeSign.X: (242, 151, 159), TicTacToeSign.O: (151, 184, 190),
                       TicTacToeSign.BLANK: (146, 98, 137)}

        is_terminal = self.is_terminal_state(state)
        score, line = self.current_score(state)
        header = self._header(state, is_terminal, score)
        current_sign = TicTacToeSign.from_player(self._get_winner(score) if is_terminal else state.current_sign)
        actions = self.actions_for(state, state.current_sign.to_player())
        n_empty_fields = np.count_nonzero(state.board == TicTacToeSign.BLANK)
        player_color = colors[current_sign]
        line_color = line_colors[current_sign]

        grid_drawer.draw_header_text(header, fill=player_color, font=head_font)
        for y, row in enumerate(state.board):
            for x, cell in enumerate(row):
                sign = TicTacToeSign(cell)
                if sign != TicTacToeSign.BLANK:
                    grid_drawer.draw_text(str(sign), (x, y), fill=colors[sign], font=font)
        if line:
            grid_drawer.line_through((line.coord_start[1], line.coord_start[0]),
                                     (line.coord_end[1], line.coord_end[0]),
                                     fill=line_color,
                                     width=int(grid_drawer.cell_height * 0.2))
        if not is_terminal and len(actions) < n_empty_fields:
            for a in actions:
                grid_drawer.draw_text('?', (a.x, a.y), fill=line_color, font=font)
        return image

    def _get_winner(self, score: Score) -> Player | None:
        if score == Score.WON:
            return Player.MAX
        elif score == score.LOST:
            return Player.MIN
        else:
            return None

    def _header(self, state: TicTacToeState, is_terminal: True, score: Score) -> str:
        if is_terminal:
            winner = self._get_winner(score)
            if winner is None:
                return "> TIE! <"
            else:
                sign = TicTacToeSign.from_player(winner)
                return f"> '{sign}' WON! <"
        else:
            return f"{state.current_sign}'s turn"


class TicTacToeGameLogic(TicTacToeGame):
    _board_size: int
    _win_length: int
    _loose_length: int

    def __init__(self, board_size: int, win_length: int, loose_length: int | None = None):
        loose_length = loose_length if loose_length is not None else board_size + 1
        assert win_length <= board_size or loose_length <= board_size, \
            "board should be big enough to win the game"
        assert win_length > 1 and loose_length > 1, \
            "this would not make sense..."
        assert win_length != loose_length, \
            "you can't loose and win at the same time"
        self._board_size = board_size
        self._win_length = win_length
        self._loose_length = loose_length
        super().__init__()

    @property
    def board_size(self) -> int:
        return self._board_size

    @property
    def win_length(self) -> int:
        return self._win_length

    @property
    def loose_length(self) -> int:
        return self._loose_length
