from base.heuristic import Heuristic
from base.problem import Problem
from base.solver import HeuristicSolver
from solvers.generic.best_first import BestFirstSearch
from tree.tree import Tree
from tree.node import Node


class AStar(HeuristicSolver):
    def __init__(self, problem: Problem, heuristic: Heuristic):
        super().__init__(problem, heuristic)
        self.search = BestFirstSearch(problem, lambda node: node.cost + heuristic(node.state))

    def solve(self) -> Node | None:
        return self.search.solve()

    def search_tree(self) -> Tree:
        return self.search.tree
        
        