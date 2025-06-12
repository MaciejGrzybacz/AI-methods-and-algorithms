from problems.n_puzzle import NPuzzleState

from problems.n_puzzle.heuristics.n_puzzle_abstract_heuristic import NPuzzleAbstractHeuristic


class NPuzzleManhattanHeuristic(NPuzzleAbstractHeuristic):

    def __call__(self, state: NPuzzleState) -> float:
        current_positions = self.positions(state)
        manhattan_distance = 0

        for tile, (current_x, current_y) in current_positions.items():
            if tile == 0:  # Skip empty tile
                continue
            goal_x, goal_y = self.goal_coords[tile]
            manhattan_distance += abs(current_x - goal_x) + abs(current_y - goal_y)

        return float(manhattan_distance)
