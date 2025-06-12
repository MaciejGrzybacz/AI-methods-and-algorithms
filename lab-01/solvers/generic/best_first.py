from typing import Callable, Optional
from base.problem import Problem
from base.state import State
from solvers.utils import PriorityQueue
from tree import Node, Tree


class BestFirstSearch:
    """
    Type of search that have access to problem definition and to heuristic, that allows it estimate
    which nodes should be searched.
    """

    def __init__(self, problem: Problem, eval_fun: Callable[[Node], float]):
        self.problem = problem
        self.start: State = problem.initial
        self.root = Node(self.start)
        self.frontier: PriorityQueue = PriorityQueue(eval_fun)
        self.visited = {self.start: float(self.root.cost)}
        self.tree = Tree(self.root)

    def solve(self) -> Node | None:
        if self.problem.is_goal(self.start):
            return self.root
            
        self.frontier.push(self.root)

        while not self.frontier.is_empty():
            node = self.frontier.pop()

            if self.problem.is_goal(node.state):
                return node
            
            for child in self.tree.expand(self.problem, node):
                if child.state not in self.visited or child.cost < self.visited[child.state]:
                    self.visited[child.state] = child.cost
                    self.frontier.push(child)
                    
        return None