from dataclasses import dataclass

from solvers.graphplan.graph.literal import Literal


@dataclass(frozen=True)
class LiteralNodeLabel:
    """
    A label of a node representing a literal in the graph plan.

    Attributes:
        literal: Literal
            A literal corresponding to the node.
        layer_index: int
            The index of the layer that the literal belongs to.
    """
    literal: Literal
    layer_index: int

    def __str__(self):
        return str(self.literal)
