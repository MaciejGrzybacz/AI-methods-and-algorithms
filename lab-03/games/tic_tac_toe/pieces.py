from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, IntEnum

import numpy as np
import numpy.typing as npt

from base.action import Action
from base.player import Player
from base.state import State


class TicTacToeSign(IntEnum):
    O = 1
    X = -1
    BLANK = 0

    def opposite(self) -> TicTacToeSign:
        return TicTacToeSign(-1 * self)

    @staticmethod
    def from_player(player: Player | None) -> TicTacToeSign:
        if player is None:
            return TicTacToeSign.BLANK

        return {
            Player.MAX: TicTacToeSign.O,
            Player.MIN: TicTacToeSign.X
        }[player]

    def to_player(self) -> Player:
        return {
            TicTacToeSign.O: Player.MAX,
            TicTacToeSign.X: Player.MIN
        }[self]

    def __str__(self) -> str:
        return {
            TicTacToeSign.BLANK: "_",
            TicTacToeSign.O: "O",
            TicTacToeSign.X: "X"
        }[self]


class TicTacToeLineDirection(Enum):
    HORIZONTAL = 0
    VERTICAL = 1
    DIAG_UP = 2
    DIAG_DOWN = 3


@dataclass(frozen=True, eq=True)
class TicTacToeLine:
    sign: TicTacToeSign
    coords: frozenset[tuple[int, int]]
    direction: TicTacToeLineDirection

    @property
    def coord_start(self) -> tuple[int, int]:
        return min(self.coords)

    @property
    def coord_end(self) -> tuple[int, int]:
        return max(self.coords)

    @property
    def length(self):
        return len(self.coords)

    @staticmethod
    def point_line(sign: TicTacToeSign, coord: tuple[int, int], direction: TicTacToeLineDirection) -> TicTacToeLine:
        return TicTacToeLine(sign, frozenset([coord]), direction)

    def add_points(self, coords: list[tuple[int, int]]) -> TicTacToeLine:
        return TicTacToeLine(self.sign, frozenset.union(self.coords, coords), self.direction)

    def __str__(self) -> str:
        return f"{self.sign} - {self.direction}: ({self.coord_start[1], self.coord_start[0]}) - ({self.coord_end[1], self.coord_end[0]})"


@dataclass(frozen=True, eq=True)
class TicTacToeAction(Action):
    sign: TicTacToeSign
    coord: tuple[int, int]

    @property
    def x(self) -> int:
        return self.coord[1]

    @property
    def y(self) -> int:
        return self.coord[0]

    def __str__(self) -> str:
        return f"{self.coord} <- {self.sign}"


@dataclass(frozen=True)
class TicTacToeState(State):
    board: npt.NDArray[np.int_]
    current_sign: TicTacToeSign
    lines: dict[TicTacToeLineDirection, dict[tuple[int, int], TicTacToeLine]]

    def take_action(self, action: TicTacToeAction) -> TicTacToeState:
        def _neighbors(coord: tuple[int, int]):
            shifts = [
                (TicTacToeLineDirection.HORIZONTAL, [(0, -1), (0, 1)]),
                (TicTacToeLineDirection.VERTICAL, [(-1, 0), (1, 0)]),
                (TicTacToeLineDirection.DIAG_UP, [(-1, -1), (1, 1)]),
                (TicTacToeLineDirection.DIAG_DOWN, [(-1, 1), (1, -1)]),
            ]

            def apply_diff(diff) -> tuple[int, int]:
                return coord[0] + diff[0], coord[1] + diff[1]

            def inside(diff) -> bool:
                return (0 <= coord[0] + diff[0] <= self.board.shape[0]
                        and 0 <= coord[1] + diff[1] <= self.board.shape[1])

            for dir, diffs in shifts:
                neighbors = [apply_diff(d) for d in diffs if inside(d)]
                yield dir, neighbors

        lines = {TicTacToeLineDirection.HORIZONTAL: self.lines[TicTacToeLineDirection.HORIZONTAL].copy(),
                 TicTacToeLineDirection.VERTICAL: self.lines[TicTacToeLineDirection.VERTICAL].copy(),
                 TicTacToeLineDirection.DIAG_DOWN: self.lines[TicTacToeLineDirection.DIAG_DOWN].copy(),
                 TicTacToeLineDirection.DIAG_UP: self.lines[TicTacToeLineDirection.DIAG_UP].copy()}
        board = self.board.copy()
        board[action.coord] = action.sign

        neighbors = list(_neighbors(action.coord))
        for dir, coords in neighbors:
            dir_lines = lines[dir]
            n_lines = [dir_lines[c] for c in coords if c in dir_lines]
            n_lines = [l for l in n_lines if l.sign == action.sign]

            if len(n_lines) == 0:
                dir_lines[action.coord] = TicTacToeLine.point_line(action.sign, action.coord, dir)
            elif len(n_lines) == 1:
                new_line = n_lines[0].add_points([action.coord])
                for coord in new_line.coords:
                    dir_lines[coord] = new_line
            elif len(n_lines) == 2:
                new_line = n_lines[0].add_points(list(n_lines[1].coords) + [action.coord])
                for coord in new_line.coords:
                    dir_lines[coord] = new_line
        return TicTacToeState(board, self.current_sign.opposite(), lines)

    def all_lines(self) -> set[TicTacToeLine]:
        return set().union(*[set(coords_to_lines.values()) for coords_to_lines in self.lines.values()])

    @staticmethod
    def empty(size: int, sign: TicTacToeSign) -> TicTacToeState:
        board = np.full((size, size), TicTacToeSign.BLANK)
        return TicTacToeState(board, sign, {TicTacToeLineDirection.HORIZONTAL: {},
                                            TicTacToeLineDirection.VERTICAL: {},
                                            TicTacToeLineDirection.DIAG_DOWN: {},
                                            TicTacToeLineDirection.DIAG_UP: {}})

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TicTacToeState):
            return False
        return np.array_equal(self.board, other.board) \
            and self.current_sign == other.current_sign

    def __hash__(self) -> int:
        return hash((self.current_sign, self.board.tobytes()))
