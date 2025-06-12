from base import Heuristic
from problems.grid_pathfinding.grid_pathfinding import GridPathfinding
from problems.grid_pathfinding.grid import GridCoord


class GridDiagonalHeuristic(Heuristic[GridCoord]):
 
    def __init__(self, problem: GridPathfinding):
        self.problem = problem

    def __call__(self, state: GridCoord) -> float:
        # I am assuming that vertical/horizontal cost is 1
        man_dist = max(abs(state.x - self.problem.goal.x), abs(state.y - self.problem.goal.y))
        diag_dist = (self.problem.diagonal_weight - 1) * min(abs(state.x - self.problem.goal.x), abs(state.y - self.problem.goal.y))
        
        return  man_dist + diag_dist
