from base.heuristic import Heuristic
from problems.blocks_world.blocks_world_problem import BlocksWorldProblem, BlocksWorldState


class BlocksWorldNaiveHeuristic(Heuristic):

    def __init__(self, problem: BlocksWorldProblem) -> None:
        super().__init__(problem)
        self.expected_columns = self._calculate_expected_columns(problem.goal)
        self.expected_fundaments = self._calculate_expected_fundaments(
            problem.goal)

    def _calculate_expected_columns(self, goal: BlocksWorldState) -> dict[str, int]:
        return {block: col_idx for col_idx, col in enumerate(goal.columns) for block in col}

    def _calculate_expected_fundaments(self, goal: BlocksWorldState) -> dict[str, list[str]]:
        return {block: col[:i] for col in goal.columns for i, block in enumerate(col)}

    def __call__(self, state: BlocksWorldState) -> int:
        misplaced = 0
        misaligned = 0

        for col_idx, col in enumerate(state.columns):
            for i, block in enumerate(col):
                expected_col = self.expected_columns[block]
                if expected_col != col_idx:
                    misplaced += 1
                elif col[:i] != self.expected_fundaments[block]:
                    misaligned += 1

        return misplaced + 2 * misaligned
