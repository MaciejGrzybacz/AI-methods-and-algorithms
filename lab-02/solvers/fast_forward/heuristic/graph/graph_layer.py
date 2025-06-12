import dataclasses
from dataclasses import dataclass, field

from problems import StripsState, StripsProposition, StripsAction
from solvers.fast_forward.heuristic.graph.action_node import ActionNode
from solvers.fast_forward.heuristic.graph.action_node_label import ActionNodeLabel

from solvers.fast_forward.heuristic.graph.literal_node import LiteralNode
from solvers.fast_forward.heuristic.graph.literal_node_label import LiteralNodeLabel
from solvers.fast_forward.heuristic.graph.literal import Literal

"""
A layer is just a dictionary mapping labels to nodes.
"""
LiteralLayer = dict[LiteralNodeLabel, LiteralNode]
ActionLayer = dict[ActionNodeLabel, ActionNode]


@dataclass
class GraphLayer:
    """
    A single layer of a graph.
    Every layer has two sub-layers: layer of actions and layer of literals created by the actions.
    Every node contains information about its relation to the other nodes,
    1. action nodes store:
        - `parents` (labels of the literals from the previous layer)
        - `children` (labels of the literals from the same layer)
    2.literal nodes store:
        - `parents` (labels of the action from the same layer)

    Every node has a `label`, its key and unique identifier.

    | previous layer |       current layer         |
    ---------------------------------------------
       literal <------- actions <------- literals
                parents    |      parents     ^
                           |-------->---------|
                                children
    Attributes:
        index: int
            The index of the layer, 0 corresponds to the first layer.
        literals_nodes: LiteralLayer
            A layer of the literal nodes.
        actions_nodes: ActionLayer
            A layer of the action nodes.
    """
    index: int = field(compare=False, default=0)
    literals_nodes: LiteralLayer = field(default_factory=dict)
    actions_nodes: ActionLayer = field(default_factory=dict)

    @staticmethod
    def from_state(state: StripsState, index: int) -> 'GraphLayer':
        """
        Creates a new layer including literals true at the given state.
        Parameters:
            state: StripsState
        """
        literal_nodes = {LiteralNodeLabel(literal, index): LiteralNode() for literal in state}
        return GraphLayer(index=index, literals_nodes=literal_nodes)

    def __str__(self):
        header = f"layer: {self.index}"
        actions = f"actions: {','.join(str(a) for a in self.actions_nodes)}"
        literals = f"literals: {','.join(str(l) for l in self.literals_nodes)}"
        return "\n".join([header, actions, literals])

    def literals(self) -> frozenset[Literal]:
        """
        Returns:
            all the literals included in the layer.
        """
        return frozenset(label.literal for label in self.literals_nodes)

    def transfer_literal(self, prev_label: LiteralNodeLabel):
        """
        Transfers a literal node (from a previous layer) to this layer.
        This method automatically adds a "transfer action" connecting
        the new literal node to the previous layer.

        Parameters:
            prev_label: a label from the previous layer.
        """
        new_label = dataclasses.replace(prev_label, layer_index=self.index)

        action_label = ActionNodeLabel.create_transfer_label(new_label)
        action_node = ActionNode(parents=[prev_label],
                                 children=[new_label])

        label_node = self.literals_nodes.get(new_label, LiteralNode(parents=[action_label]))
        self.literals_nodes[new_label] = label_node
        self.actions_nodes[action_label] = action_node

    def add_literal(self, label: LiteralNodeLabel) -> LiteralNode:
        """
        Creates a new literal node with the given label.
        If the node already exists, it will be returned instead.

        Parameters:
            label: a label for the new node.
        Returns:
            a literal node (either new or existing one).
        """
        node = self.literals_nodes.get(label, LiteralNode())
        self.literals_nodes[label] = node
        return node

    def literal_label_for(self, proposition: StripsProposition) -> LiteralNodeLabel:
        """
        Creates a new label for the given STRIPS proposition.
        If the node already exists, it will be returned instead.

        Parameters:
            proposition: A proposition stated in the literal.
        Returns:
            a literal label corresponding to the proposition.
        """
        return LiteralNodeLabel(proposition, self.index)

    def add_action(self, label: ActionNodeLabel) -> ActionNode:
        """
        Creates a new action node with the given label.
        If the node already exists, it will be returned instead.

        Parameters:
            label: a label for the new node.
        Returns:
            an action node (new or existing one).
        """
        node = self.actions_nodes.get(label, ActionNode())
        self.actions_nodes[label] = node
        return node

    def action_label_for(self, strips_action: StripsAction) -> ActionNodeLabel:
        """
        Creates a new action label for the given STRIPS action.

        Parameters:
            strips_action: A STRIPS action.
        Returns:
            an action label corresponding this action.
        """
        return ActionNodeLabel(strips_action,
                               layer_index=self.index)
