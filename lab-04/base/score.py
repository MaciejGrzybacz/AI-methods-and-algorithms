from __future__ import annotations
from enum import IntEnum

from base.player import Player


class Score(IntEnum):
    WON  = 1
    TIE  = 0
    LOST = -1

    def for_player(self, player: Player) -> Score:
        return Score(player.value * self.value)
    
    def __neg__(self):
        return Score(-self.value)