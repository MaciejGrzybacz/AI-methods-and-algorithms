from problems import StripsState
from solvers.fast_forward.heuristic.graph.graph_layer import GraphLayer
from solvers.fast_forward.heuristic.graph.literal_node_label import LiteralNodeLabel
from solvers.fast_forward.heuristic.graph.literal import Literal

from solvers.fast_forward.heuristic.graph.action_node import ActionNode
from solvers.fast_forward.heuristic.graph.action_node_label import ActionNodeLabel
from solvers.fast_forward.heuristic.graph.literal_node import LiteralNode


class LayeredGraph:
    """
    A layered graph structure used by the Graphplan algorithm.

    Attributes:
        layers: a list of layers in the graph.
    """
    layers: list[GraphLayer]

    def __init__(self, init_state: StripsState):
        """
        Parameters:
            init_state: a STRIPS used to initialize the first layer of the graph
        """
        self.layers = [GraphLayer.from_state(init_state, 0)]

    def number_of_layers(self) -> int:
        """
        Returns:
            the number of layers in the graph.
        """
        return len(self.layers)

    def is_last_layer(self, layer: GraphLayer) -> bool:
        """
        Parameters:
            layer: a layer included in the graph
        Returns:
            true if the provided layer is the last layer in the graph
        """
        return layer.index == len(self.layers) - 1

    def is_first_layer(self, layer: GraphLayer) -> bool:
        """
        Parameters:
            layer: a layer included in the graph
        Returns:
            true if the provided layer is the first layer in the graph
        """
        return layer.index == 0

    def last_layer(self) -> GraphLayer:
        """
        Returns:
            the last layer in the graph.
        """
        return self.layers[-1]

    def next_layer(self, layer: GraphLayer) -> GraphLayer | None:
        """
        Parameters:
            layer: a layer included in the graph
        Returns:
            None, if the provided layer is the last in the graph.
            Otherwise, the layer's successor is returned.
        """
        if layer.index < len(self.layers) - 1:
            return self.layers[layer.index + 1]
        return None

    def previous_layer(self, layer: GraphLayer) -> GraphLayer | None:
        """
        Parameters:
            layer: a layer included in the graph
        Returns:
            None, if the provided layer is the first in the graph.
            Otherwise, the layer's predecessor is returned.
        """
        if layer.index > 0:
            return self.layers[layer.index - 1]
        return None

    def add_layer(self) -> GraphLayer:
        """
        Creates a new layer in the graph and adds it as the last in the graph.

        Returns:
            a newly created layer.
        """
        layer = GraphLayer(len(self.layers))
        self.layers.append(layer)
        return layer

    def reachable_facts(self, layer_index: int = -1) -> frozenset[Literal]:
        """
        Parameters:
            layer_index: the index of a layer in the graph.
        Returns:
            all literals true in the layer at the provided index.
        """
        return self.layers[layer_index].literals()

    def get_literal_node(self, label: LiteralNodeLabel) -> LiteralNode:
        """
        Parameters:
            label: a literal node label belonging to the graph.
        Returns:
            a node corresponding to the label
        """
        return self.layers[label.layer_index].literals_nodes[label]

    def get_action_node(self, label: ActionNodeLabel) -> ActionNode:
        """
        Parameters:
            label: an action node label belonging to the graph.
        Returns:
            a node corresponding to the label
        """
        return self.layers[label.layer_index].actions_nodes[label]

    def reached_fixed_point(self):
        """
        Returns:
            true if the two last layers in the graph are exactly the same.
            It indicates that the graph stopped expanding.
        """
        if len(self.layers) < 2:
            return False

        return self.layers[-2] == self.layers[-1]
