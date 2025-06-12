from problems.n_puzzle import NPuzzleState
from problems.n_puzzle.heuristics.n_puzzle_abstract_heuristic import NPuzzleAbstractHeuristic


class NPuzzleTilesOutOfPlaceHeuristic(NPuzzleAbstractHeuristic):

    def __call__(self, state: NPuzzleState) -> float:
        current_positions = self.positions(state)
        tiles_out_of_place = 0

        for tile, position in current_positions.items():
            if tile == 0:
                continue
            if position != self.goal_coords[tile]:
                tiles_out_of_place += 1

        return float(tiles_out_of_place)
