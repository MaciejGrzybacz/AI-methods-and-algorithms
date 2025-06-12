from __future__ import annotations
from typing import Iterator

from problems.action import StripsAction, StripsActionSchema
from problems.state import StripsState
from problems.unifier import StrictUnifier


class StripsProblem:
    """
    A STRIPS problem in all its glory.
    It can be used as a basic state-space generator.

    Attributes:
        name: str
            The name of the problem.
        objects: frozenset[str]
            All objects involved in the problem instance.
        action_schemas: list[StripsActionSchema]
            Action schemas defined in the problem domain.
        init_state:
            The initial state of the problem.
        goals:
            The state to be reached by the plan.

    Methods:
        actions(state: StripsState) -> Iterator[StripsAction]:
            Yields grounded action that can be performed in the given state.
        take_action(state: StripsState, action: StripsAction) -> StripsState:
            Performs action in the state, yielding a new state.
         satisfies_goals(state: StripsState) -> bool:
            Checks if the given state satisfies the problem goals.
    """
    name: str
    objects: frozenset[str]
    action_schemas: list[StripsActionSchema]
    init_state: StripsState
    goals: StripsState

    def __init__(self, name: str,
                 objects: frozenset[str],
                 actions_schemas: list[StripsActionSchema],
                 init_state: StripsState,
                 goals: StripsState):
        super().__init__()
        self.objects = objects
        self.name = name
        self.action_schemas = actions_schemas
        self.init_state = init_state
        self.goals = goals

    def actions(self, state: StripsState) -> Iterator[StripsAction]:
        """Yields grounded actions feasible in the given state.

        Parameters:
            state: a state considered when checking actions requirements.
        Returns:
            grounded actions
        """
        unifier = StrictUnifier(state, self.objects)
        for schema in self.action_schemas:
            for values in unifier.matches(list(schema.requires_schemas)):
                yield schema.ground(*values)

    def take_action(self, state: StripsState, action: StripsAction) -> StripsState:
        """Performs action in the state, yielding a new state."""
        return state.difference(action.removes).union(action.adds)

    def satisfies_goals(self, state: StripsState) -> bool:
        """Checks whether the given state satisfies the problem goals."""
        return self.goals.issubset(state)
