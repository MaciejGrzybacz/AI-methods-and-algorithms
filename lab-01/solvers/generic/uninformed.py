from base.solver import P
from solvers.utils import Queue
from tree import Node, Tree


class UninformedSearch:
    """
    Type of search, that have access only to problem definition.    
    """

    def __init__(self, problem: P, queue: Queue):
        self.problem = problem
        self.start = problem.initial
        self.frontier = queue
        self.visited = {self.start}
        # using a set instead of a dictionary as it was in BestFirstSearch, 
        # because we don't have an evaluation funtion and there is no need for a dictionary.
        self.root = Node(self.start)
        self.tree = Tree(self.root)

    def solve(self):
        if self.problem.is_goal(self.start):
            return self.root
        self.frontier.push(self.root)

        while not self.frontier.is_empty():
            node = self.frontier.pop()

            if self.problem.is_goal(node.state):
                return node
            
            for child in self.tree.expand(self.problem, node):
                if child.state not in self.visited:
                    self.visited.add(child.state)
                    self.frontier.push(child)
                    
        return None