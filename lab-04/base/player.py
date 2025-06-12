from __future__ import annotations
from enum import IntEnum


class Player(IntEnum):
    MIN = -1
    MAX = 1

    def opponent(self) -> Player:
        return Player(self.value * -1)

