from base.heuristic import Heuristic
from base.solver import HeuristicSolver
from solvers.generic.best_first import BestFirstSearch
from tree.node import Node
from tree.tree import Tree


class Greedy(HeuristicSolver):
    def __init__(self, problem, heuristic):
        super().__init__(problem, heuristic)
        self.search = BestFirstSearch(problem, lambda node: heuristic(node.state))

    def solve(self) -> Node | None:
        return self.search.solve()
        
    def search_tree(self) -> Tree:
        return self.search.tree    