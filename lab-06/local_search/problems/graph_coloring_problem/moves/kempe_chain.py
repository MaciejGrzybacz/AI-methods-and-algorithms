import random
from typing import Generator, Set, Dict, List

from local_search.problems.base.moves import Move
from local_search.problems.graph_coloring_problem.models.vertex import Vertex
from local_search.problems.graph_coloring_problem.moves.move_generator import (
    GraphColoringMoveGenerator,
)
from local_search.problems.graph_coloring_problem.state import GraphColoringState
import copy


class KempeChainMove(Move[GraphColoringState]):
    def __init__(
        self,
        graph: Dict[int, Set[int]],
        from_state: GraphColoringState,
        idx: int,
        color: int,
    ):
        super().__init__(from_state)
        self.idx = idx
        self.color = color
        self.graph = graph
        self.old_color = self.state.coloring[idx].color

    def _kempe_chain(self, coloring: List[Vertex]):
        """This method is supposed to fix the `coloring` using the kempe chain method"""
        # TODO: do the kempe chain thing
        # - self.idx is index of the node beginning the chain
        # - self.color is the new color of the node (already set in the `make` method)
        # - self.old_color is the old color of the node
        # - self.graph[c] are the neighbors of the node c, just a list of adjacent vertices (`Vertex` class)
        # - coloring is a list of vertices (also `Vertex` class, has index and color)
        #   your task is to modify this coloring to make it again a correct graph coloring
        #
        # Debrief:
        # The color of the node with index `self.idx`` has changed!
        # Now you have to fix all the possible conflicts in a BFS fashion
        # by changing colors of nodes (via `coloring`):
        # - with self.color to self.old_color
        # - with self.old_color to self.color
        #
        # Remember, the BFS start at `self.idx` and should explore the graph
        # as long as the explored nodes are colored with self.old_color or self.color.

        visited = set()
        queue = [self.idx]
        visited.add(self.idx)

        while queue:
            current_idx = queue.pop(0)

            for neighbor_idx in self.graph[current_idx]:
                if neighbor_idx not in visited:
                    neighbor_color = coloring[neighbor_idx].color

                    if neighbor_color == self.old_color or neighbor_color == self.color:
                        visited.add(neighbor_idx)
                        queue.append(neighbor_idx)

                        if neighbor_color == self.old_color:
                            coloring[neighbor_idx].color = self.color
                        elif neighbor_color == self.color:
                            coloring[neighbor_idx].color = self.old_color

    def make(self) -> GraphColoringState:
        """This method changes color of a single node and starts of the kempe chain"""
        new_coloring = copy.deepcopy(self.state.coloring)
        new_coloring[self.idx].color = self.color
        self._kempe_chain(new_coloring)
        return GraphColoringState(coloring=new_coloring)


class KempeChain(GraphColoringMoveGenerator):
    def random_moves(
        self, state: GraphColoringState
    ) -> Generator[KempeChainMove, None, None]:
        while True:
            idx = random.randrange(self.n_vertices)
            available_colors = self.get_available_colors(idx, state)
            yield KempeChainMove(
                self.graph,
                state,
                idx=random.randrange(self.n_vertices),
                color=random.choice(available_colors),
            )

    def available_moves(
        self, state: GraphColoringState
    ) -> Generator[KempeChainMove, None, None]:
        for idx in range(self.n_vertices):
            for color in self.get_available_colors(idx, state):
                if state.coloring[idx].color == color:
                    continue
                yield KempeChainMove(self.graph, state, idx, color)