import dataclasses
from dataclasses import dataclass, field

from problems import StripsState, StripsProposition, StripsAction
from solvers.graphplan.graph.action import Action
from solvers.graphplan.graph.action_node import ActionNode
from solvers.graphplan.graph.action_node_label import ActionNodeLabel
from solvers.graphplan.graph.literal import Literal
from solvers.graphplan.graph.literal_node import LiteralNode
from solvers.graphplan.graph.literal_node_label import LiteralNodeLabel

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

    Additionally, every layer contains information, whether the two actions/literals are exclusive.

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
    _literals_mutexes: dict[Literal, set[Literal]] = field(default_factory=dict)
    _actions_mutexes: dict[Action, set[Action]] = field(default_factory=dict)

    @staticmethod
    def from_state(state: StripsState, index: int) -> 'GraphLayer':
        """
        Creates a new layer including literals true at the given state.
        Parameters:
            state: StripsState
        """
        literals = {Literal(fact, True) for fact in state}
        literal_nodes = {LiteralNodeLabel(literal, index): LiteralNode() for literal in literals}
        _literals_mutexes = {literal: set() for literal in literals}
        return GraphLayer(index=index, literals_nodes=literal_nodes, _literals_mutexes=_literals_mutexes)

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
        self._literals_mutexes[new_label.literal] = set()
        self._actions_mutexes[action_label.action] = set()

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
        self._literals_mutexes[label.literal] = set()
        return node

    def literal_label_for_proposition(self, proposition: StripsProposition, true: bool) -> LiteralNodeLabel:
        """
        Creates a new label for the given STRIPS proposition.
        If the node already exists, it will be returned instead.

        Parameters:
            proposition: A proposition stated in the literal.
            true: Whether the proposition is true in the layer.
        Returns:
            a literal label corresponding to the proposition.
        """
        literal = Literal(proposition, true)
        return LiteralNodeLabel(literal, self.index)

    def literal_label_for_literal(self, literal: Literal) -> LiteralNodeLabel:
        """
        Creates a new label for the given literal.

        Parameters:
            literal: A literal supposed to be true in the layer.
        Returns:
            a literal label corresponding to the literal.
        """
        return LiteralNodeLabel(literal, self.index)

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
        self._actions_mutexes[label.action] = set()
        return node

    def action_label_for(self, strips_action: StripsAction) -> ActionNodeLabel:
        """
        Creates a new action label for the given STRIPS action.

        Parameters:
            strips_action: A STRIPS action.
        Returns:
            an action label corresponding this action.
        """
        action = Action(strips_action.name,
                        requires_true=strips_action.requires,
                        requires_false=frozenset(),
                        adds_true=strips_action.adds,
                        adds_false=strips_action.removes)
        return ActionNodeLabel(action,
                               layer_index=self.index)

    def add_literal_mutex(self, l1: Literal, l2: Literal) -> None:
        """
        States that the two literals cannot be true at the same time.

        Parameters:
            l1: a literal belonging to the layer.
            l2: another literal belonging to the layer.
        """
        self._literals_mutexes[l1].add(l2)
        self._literals_mutexes[l2].add(l1)

    def add_action_mutex(self, a1: Action, a2: Action) -> None:
        """
        States that two actions cannot be performed together.

        Parameters:
            a1: an action belonging to the layer.
            a2: another action belonging to the layer.
        """
        self._actions_mutexes[a1].add(a2)
        self._actions_mutexes[a2].add(a1)

    def contains_literal_mutex(self, l1: Literal, l2: Literal) -> bool:
        """
        Checks whether the two literals cannot be true at the same time.

        Parameters:
            l1: a literal belonging to the layer.
            l2: another literal belonging to the layer.
        Returns:
            true if the literals cannot be true at the same time.
        """
        return l2 in self._literals_mutexes[l1]

    def contains_action_mutex(self, a1: Action, a2: Action) -> bool:
        """
        Checks whether the two actions cannot be performed together.

        Parameters:
            a1: an action belonging to the layer.
            a2: another action belonging to the layer.
        Returns:
            true if the actions exclude each other.
        """
        return a2 in self._actions_mutexes[a1]

    def conflicting_literals(self, l: Literal) -> set[Literal]:
        """
        Returns all literals that cannot held true together with the given literal.

        Parameters:
            l: a literal belonging to the layer.
        Returns:
            all literal that cannot be true at the same time as the literal.
        """
        return self._literals_mutexes[l]

    def conflicting_actions(self, a: Action) -> set[Action]:
        """
        Returns all actions that cannot be performed together with the given action.

        Parameters:
            a: an action belonging to the layer.
        Returns:
            all actions that cannot be performed together with the given action.
        """
        return self._actions_mutexes[a]
