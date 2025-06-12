from dataclasses import dataclass

from problems import StripsState
from solvers.fast_forward.heuristic.graph.literal_node_label import LiteralNodeLabel
from solvers.fast_forward.heuristic.graph.action import Action



@dataclass(frozen=True)
class ActionNodeLabel:
    """
    A label of a node representing an action in the graph plan.

    Attributes:
        action: Action
            An action corresponding to the node.
        layer_index: int
            The index of the layer that the node belongs to.
        is_transfer: bool
            Whether the action is a dummy action used just to transfer literal to the next layer.
    """
    action: Action
    layer_index: int
    is_transfer: bool = False

    @staticmethod
    def create_transfer_label(literal_label: LiteralNodeLabel) -> 'ActionNodeLabel':
        literal = literal_label.literal
        propositions = StripsState({literal})

        action = Action(f"transfer_{literal}",
                        requires=propositions,
                        adds=propositions,
                        removes=frozenset())

        return ActionNodeLabel(action,
                               layer_index=literal_label.layer_index,
                               is_transfer=True)

    def __str__(self):
        return str(self.action)
