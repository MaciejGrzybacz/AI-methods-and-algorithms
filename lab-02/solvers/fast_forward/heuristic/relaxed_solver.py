from collections.abc import Iterator

from problems import StripsAction, StripsProblem, StripsState
from solvers.fast_forward.generic_best_first_search import Heuristic
from solvers.fast_forward.heuristic.graph.action_node_label import ActionNodeLabel
from solvers.fast_forward.heuristic.graph.graph import LayeredGraph
from solvers.fast_forward.heuristic.graph.graph_layer import GraphLayer
from solvers.fast_forward.heuristic.graph.literal import Literal
from solvers.fast_forward.heuristic.graph.literal_node_label import LiteralNodeLabel


class RelaxedGraphPlan(Heuristic):
    """
    A heuristic calculator for the STRIPS problems.
    It is based on the graphplan algorithm solving a relaxed problem
    without the DEL actions.

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
        self.problem = problem

    def __call__(self, state: StripsState) -> int | None:
        """
        The main algorithm loop:
            1. Checks whether the graph reached a fixed point.
                   - if so, the problem is unsolvable and None is returned
            2. Then we check whether we are able to build a valid plan based on the current graph.
                   - if so, we return length of the plan
            3. We expand the graph and repeat the loop

        Returns:
            None if the problem is unsolvable.
            Otherwise, a valid plan is returned.
        """
        self.graph = LayeredGraph(state)
        while True:
            if self.graph.reached_fixed_point():
                return None
            solution = self.extract_solution()
            if solution is not None:
                return len(solution)
            self.expand_graph()


    def expand_graph(self) -> None:
        """
        Expands the graph with a new layer in three steps:
            1. Add a new layer based on the available actions and the last layer.
            2. Identifies which actions exclude each other
            3. Identifies which literals exclude each other
        """
        prev_layer = self.graph.last_layer()
        new_layer = self.graph.add_layer()

        for literal_label in prev_layer.literals_nodes:
            new_layer.transfer_literal(literal_label)

        true_literals = frozenset(
            label.literal for label in prev_layer.literals_nodes
        )

        for action in self.problem.actions(true_literals):
            action_label = new_layer.action_label_for(action)

            action_node = new_layer.add_action(action_label)

            action_node.parents = [prev_layer.literal_label_for(req) for req in action.requires]

            effects_literals = (eff for eff in action.adds)

            for effect_literal in effects_literals:
                literal_label = new_layer.literal_label_for(effect_literal)
                literal_node = new_layer.add_literal(literal_label)

                action_node.children.append(literal_label)
                literal_node.parents.append(action_label)

        return new_layer


    def extract_solution(self) -> list[StripsAction] | None:
        """
        Tries to extract the solution from the graph.
        It starts with the last layer and tries to satisfy all the problem goals.
        Finally, if there is a solution, it translates it to plain STRIPS actions.

        Returns:
            None if there is no solution found, otherwise list of the actions.
        """
        goals = list(self.problem.goals)
        plan = next(self._extract_solution(goals, self.graph.last_layer()), None)
        if plan is None:
            return None
        return [a.action for a in plan if not a.is_transfer]

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
        init_goals = [layer.literal_label_for(g) for g in goals]
        init_satisfied_goals: frozenset[LiteralNodeLabel] = frozenset()
        yield from self._find_possible_actions(init_goals, init_satisfied_goals, layer)

    def _find_possible_actions(self,
                               goals_left: list[LiteralNodeLabel],
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

            new_satisfied = satisfied.union(self.graph.get_action_node(parent_action_label).children)

            for sub_plan in self._find_possible_actions(goals_left[1:], new_satisfied, layer):
                yield [parent_action_label] + sub_plan