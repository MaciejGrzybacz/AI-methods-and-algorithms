from typing import Dict, List, Set, Tuple
from base.player import Player
from games.tic_tac_toe.game import TicTacToeGame
from games.tic_tac_toe.pieces import TicTacToeAction, TicTacToeSign, TicTacToeState
from numpy.typing import NDArray
import numpy as np

class SymmetryBreakingWrapper(TicTacToeGame):
    game: TicTacToeGame  

    def __init__(self, game: TicTacToeGame, stop_breaking_after_filling: int = 3):
        self.game = game
        self.stop_breaking_after = stop_breaking_after_filling
        super().__init__()

    @property
    def win_length(self) -> int:
        return self.game.win_length
    
    @property
    def loose_length(self) -> int:
        return self.game.loose_length
    
    @property
    def board_size(self) -> int:
        return self.game.board_size
    
    def name(self) -> str:
        return f"SB_{self.game.name()}"

    def actions_for(self, state: TicTacToeState, player: Player) -> List[TicTacToeAction]:
        actions = self.game.actions_for(state, player)
        if np.count_nonzero(state.board) > self.stop_breaking_after:
            return actions
        return self.break_symmetry(state, actions)
    
    def break_symmetry(self, state: TicTacToeState, actions: List[TicTacToeAction]) -> List[TicTacToeAction]:

        def to_tuple(board: NDArray) -> Tuple[int, ...]:
            return tuple(board.ravel())
        
        def all_versions(board: NDArray) -> Set[Tuple[int, ...]]:
            transformations = [
                lambda a: a,
                lambda a: np.rot90(a, 1),
                lambda a: np.rot90(a, 2),
                lambda a: np.rot90(a, 3),
                lambda a: np.fliplr(a),
                lambda a: np.flipud(a),
                lambda a: np.rot90(np.fliplr(a)),
                lambda a: np.fliplr(np.rot90(a))
            ]

            return set(to_tuple(t(board)) for t in transformations)
        
        known_states : Set[Tuple[int, ...]] = set()
        unique_actions : List[actions] = []

        candidate = state.board.copy()
        for a in actions:
            candidate[a.coord] = a.sign
            candidate_tuple = to_tuple(candidate)
            if candidate_tuple not in known_states:
                known_states.update(all_versions(candidate))
                unique_actions.append(a)
            candidate[a.coord] = TicTacToeSign.BLANK
        
        return unique_actions


    