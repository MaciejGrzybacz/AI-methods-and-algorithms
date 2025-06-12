from dataclasses import dataclass, field

from solvers.fast_forward.heuristic.graph.action_node_label import ActionNodeLabel


@dataclass
class LiteralNode:
    """
    A literal node stores information about the actions that lead to the corresponding literal.

    Attributes:
         parents: list[ActionNodeLabel]
            The list of nodes that are responsible for adding this literal to its layer.
    """
    parents: list[ActionNodeLabel] = field(default_factory=list)
