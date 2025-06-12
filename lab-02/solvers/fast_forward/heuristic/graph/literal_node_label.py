from dataclasses import dataclass

from solvers.fast_forward.heuristic.graph.literal import Literal


@dataclass(frozen=True)
class LiteralNodeLabel:
    """
    Literal represents a possibly negated STRIPS proposition.

    Attributes:
        literal: Literal
            A proposition forming the literal.
        layer_index: int
            Index of the layer the literal belongs to
    """
    literal: Literal
    layer_index: int

    def __str__(self):
        return str(self.literal)
