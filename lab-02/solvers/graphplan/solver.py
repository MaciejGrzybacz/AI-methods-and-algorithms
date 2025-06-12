from collections.abc import Iterator

from problems import StripsAction, StripsProblem
from solvers.graphplan.graph.graph import LayeredGraph
from solvers.graphplan.graph.graph_layer import GraphLayer
from solvers.graphplan.graph.action_node_label import ActionNodeLabel
from solvers.graphplan.graph.action import Action
from solvers.graphplan.graph.literal_node_label import LiteralNodeLabel
from solvers.graphplan.graph.literal import Literal
from solvers.solver import Solver
from utils.list_utils import pairs


class GraphPlan(Solver):
    """
    A STRIPS solver using the GraphPlan algorithm.

    Attributes:
        graph: a layered graph data structure used by the algorithm
    """
    graph: LayeredGraph

    def __init__(self, problem: StripsProblem):
        """
        Initializes the planning graph.

        Parameters:
            problem: the problem to be solved by the algorithm
        """
        self.graph = LayeredGraph(problem.init_state)
        super().__init__(problem)

    def solve(self) -> list[StripsAction] | None:
        """
        The main algorithm loop:
            1. Checks whether the graph reached a fixed point.
                   - if so, the problem is unsolvable and None is returned
            2. Then we check whether we are able to build a valid plan based on the current graph.
                   - if so, we return the plan
            3. We expand the graph and repeat the loop
        The `update_metric` is used just to update the user interface.


        Returns:
            None if the problem is unsolvable.
            Otherwise, a valid plan is returned.
        """
        while True:
            if self.graph.reached_fixed_point():
                return None
            solution = self.extract_solution()
            if solution is not None:
                return solution
            self.expand_graph()
            self.update_metric()

    def metric(self) -> str:
        """
        Returns:
            a short summary of the current algorithm state
        """
        n_layers = self.graph.number_of_layers()
        n_literals = sum(len(l.literals_nodes) for l in self.graph.layers)
        n_actions = sum(len(l.actions_nodes) for l in self.graph.layers)
        return f"{n_layers} layers # {n_literals} literals # {n_actions} actions"

    def expand_graph(self) -> None:
        """
        Expands the graph with a new layer in three steps:
            1. Add a new layer based on the available actions and the last layer.
            2. Identifies which actions exclude each other
            3. Identifies which literals exclude each other
        """
        layer = self._expand_graph_layers()
        self._update_action_mutexes(layer)
        self._update_literal_mutexes(layer)

    def _expand_graph_layers(self) -> GraphLayer:
        """
        Creates a new graph layer based ont the available actions and the last layer.

        Returns:
            a newly created layer
        """
        prev_layer = self.graph.last_layer()
        new_layer = self.graph.add_layer()

        for literal_label in prev_layer.literals_nodes:
            new_layer.transfer_literal(literal_label)

        true_literals = frozenset(
            label.literal.proposition for label in prev_layer.literals_nodes if label.literal.true
        )

        for action in self.problem.actions(true_literals):
            action_label = new_layer.action_label_for(action)

            action_node = new_layer.add_action(action_label)

            action_node.parents = [prev_layer.literal_label_for_literal(Literal(req, True)) for req in action.requires]

            effects_literals = ([Literal(eff, True) for eff in action.adds] +
                                [Literal(eff, False) for eff in action.removes])

            for effect_literal in effects_literals:
                literal_label = new_layer.literal_label_for_literal(effect_literal)
                literal_node = new_layer.add_literal(literal_label)

                action_node.children.append(literal_label)
                literal_node.parents.append(action_label)

        return new_layer

    def _update_action_mutexes(self, layer: GraphLayer) -> None:
        """
        Adds relevant action mutexes to the layer.

        Parameters:
            layer: the current graph layer
        """
        for a1, a2 in pairs(list(layer.actions_nodes)):
            if self._are_action_nodes_exclusive(a1, a2):
                layer.add_action_mutex(a1.action, a2.action)

    def _are_action_nodes_exclusive(self,
                                    al1: ActionNodeLabel,
                                    al2: ActionNodeLabel) -> bool:
        """
        Tells whether the two actions belonging to the same layer are exclusive.

        Parameters:
            al1: label of the first action node
            al2: label of the second action node

        Returns:
            true if the two action nodes are exclusive
        """
        action1 = al1.action
        action2 = al2.action

        if (action1.requires_true & action2.requires_false) or (action2.requires_true & action1.requires_false):
            return True

        if action1.adds_false & action2.requires_true or action2.adds_false & action1.requires_true:
            return True

        if action1.adds_true & action2.requires_false or action2.adds_true & action1.requires_false:
            return True

        action_node1 = self.graph.get_action_node(al1)
        action_node2 = self.graph.get_action_node(al2)

        for parent_label1 in action_node1.parents:
            for parent_label2 in action_node2.parents:
                if self.graph.contains_literal_mutex(parent_label1, parent_label2):
                    return True

        return False

    def _update_literal_mutexes(self, layer: GraphLayer) -> None:
        """
        Adds relevant literal mutexes to the layer.

        Parameters:
            layer: the current graph layer
        """
        for l1, l2 in pairs(list(layer.literals_nodes)):
            if self._are_literal_nodes_exclusive(l1, l2):
                layer.add_literal_mutex(l1.literal, l2.literal)

    def _are_literal_nodes_exclusive(self,
                                     ll1: LiteralNodeLabel,
                                     ll2: LiteralNodeLabel) -> bool:
        """
        Tells whether the two literals belonging to the same layer are exclusive.

        Parameters:
            ll1: label of the first literal node
            ll2: label of the second literal node

        Returns:
            true if the two literals cannot be true at the same time
        """
        literal1 = ll1.literal
        literal2 = ll2.literal

        if literal1.proposition == literal2.proposition and literal1.true != literal2.true:
            return True

        literal_node1 = self.graph.get_literal_node(ll1)
        literal_node2 = self.graph.get_literal_node(ll2)

        for parent1 in literal_node1.parents:
            for parent2 in literal_node2.parents:
                if not self.graph.contains_action_mutex(parent1, parent2):
                    return False

        return True

    def extract_solution(self) -> list[StripsAction] | None:
        """
        Tries to extract the solution from the graph.
        It starts with the last layer and tries to satisfy all the problem goals.
        Finally, if there is a solution, it translates it to plain STRIPS actions.

        Returns:
            None if there is no solution found, otherwise list of the actions.
        """
        goals = [Literal(g, True) for g in self.problem.goals]
        plan = next(self._extract_solution(goals, self.graph.last_layer()), None)
        if plan is None:
            return None
        return [a.action.strips_action() for a in plan if not a.is_transfer]

    def _extract_solution(self, goals: list[Literal], layer: GraphLayer) -> Iterator[list[ActionNodeLabel]]:
        """
        Finds possible plans that can satisfy given literals at the given layer.
        It does so-called goal regression (backward planning).

        Parameters:
            goals: list of literals to be satisfied
            layer: currently analyzed layer

        Returns:
            an iterator over possible sets of actions satisfying the goals
        """
        if not self._are_goals_reachable(goals, layer):
            return

        if self.graph.is_first_layer(layer):
            yield []
            return

        for action_set in self._possible_action_sets(goals, layer):
            sub_goals = [parent.literal for action in action_set for parent in
                         self.graph.get_action_node(action).parents]

            prev_layer = self.graph.previous_layer(layer)
            for sub_plan in self._extract_solution(sub_goals, prev_layer):
                yield sub_plan + action_set

    def _are_goals_reachable(self, goals: list[Literal], layer: GraphLayer) -> bool:
        """
        Checks whether the goals may be reached in the given layer.

        Parameters:
            goals: list of literals to be satisfied
            layer: currently analyzed layer

        Returns:
            true if there is a chance to satisfy the goals
        """
        layer_literals = layer.literals()

        if any(goal not in layer_literals for goal in goals):
            return False

        for goal1, goal2 in pairs(goals):
            if layer.contains_literal_mutex(goal1, goal2):
                return False

        return True

    def _possible_action_sets(self, goals: list[Literal], layer: GraphLayer) -> Iterator[list[ActionNodeLabel]]:
        """
        Finds possible actions' sets that satisfy given literals at the given layer.
        It's an entry point of method `_find_possible_actions`.

        Parameters:
            goals: list of literals to be satisfied
            layer: currently analyzed layer

        Returns:
            list of actions that satisfy the goals starting from the previous layer
        """
        init_goals = [layer.literal_label_for_literal(g) for g in goals]
        init_satisfied_goals: frozenset[LiteralNodeLabel] = frozenset()
        init_conflicting_actions: frozenset[Action] = frozenset()
        yield from self._find_possible_actions(init_goals, init_conflicting_actions, init_satisfied_goals, layer)

    def _find_possible_actions(self,
                               goals_left: list[LiteralNodeLabel],
                               conflicting_actions: frozenset[Action],
                               satisfied: frozenset[LiteralNodeLabel],
                               layer: GraphLayer) -> Iterator[list[ActionNodeLabel]]:
        """
        Finds possible actions' sets that satisfy given literals at the given layer.
        It's a recursive function, calling itself and remembering already made choices.

        Parameters:
            goals_left: list of the literals left to be satisfied
            conflicting_actions: actions that would conflict with already chosen actions
            satisfied: literals already satisfied by the actions found previously
            layer: currently analyzed layer

        Returns:
            list of actions that satisfy the goals starting from the previous layer
        """
        goals_left = [goal for goal in goals_left if goal not in satisfied]

        if not goals_left:
            yield []
            return

        goal_node = self.graph.get_literal_node(goals_left[0])
        for parent_action_label in goal_node.parents:
            parent_action = parent_action_label.action

            if parent_action in conflicting_actions:
                continue

            new_satisfied = satisfied.union(self.graph.get_action_node(parent_action_label).children)
            new_conflicting_actions = conflicting_actions.union(layer.conflicting_actions(parent_action))

            for sub_plan in self._find_possible_actions(goals_left[1:], new_conflicting_actions, new_satisfied, layer):
                yield [parent_action_label] + sub_plan
