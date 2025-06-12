from dataclasses import dataclass, field

from solvers.fast_forward.heuristic.graph.literal_node_label import LiteralNodeLabel


@dataclass
class ActionNode:
    """
    A node stores information about the literal related to the given action.

    Attributes:
         parents: list[LiteralNodeLabel]
            The list of literal nodes that made the action possible.
         children: list[LiteralNodeLabel]
            The list of literal nodes added by the action.
    """
    parents: list[LiteralNodeLabel] = field(default_factory=list)
    children: list[LiteralNodeLabel] = field(default_factory=list)
