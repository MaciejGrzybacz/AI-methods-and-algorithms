from dataclasses import dataclass

from problems import StripsState
from solvers.graphplan.graph.action import Action
from solvers.graphplan.graph.literal_node_label import LiteralNodeLabel


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
        """
            Creates a new label for an action transferring given literal to the next layer.

            Parameters:
                literal_label: a label of a literal in the *new* graph layer,
            Returns:
                a new action label with `is_transfer` set to `True`
                     and a single-element set of requirements/effects.
        """
        literal = literal_label.literal
        propositions = StripsState({literal.proposition})
        true_set = propositions if literal.true else StripsState()
        false_set = propositions - true_set

        action = Action(f"transfer_{literal}",
                        requires_true=true_set,
                        requires_false=false_set,
                        adds_true=true_set,
                        adds_false=false_set)

        return ActionNodeLabel(action,
                               layer_index=literal_label.layer_index,
                               is_transfer=True)

    def __str__(self):
        return str(self.action)
