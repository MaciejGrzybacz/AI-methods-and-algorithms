from dataclasses import dataclass

from problems import StripsState, StripsAction


@dataclass(frozen=True, order=True)
class Action:
    """
    A grounded STRIPS action as represented in the graph plan.
    The only difference between this and the normal StripsAction class is that
    it can also specify, what has to be false (`requires_false`) for the action to be doable.

    Attributes:
        name: str
            The name of the action.
        requires_true: bool
            What propositions are required to be true in a state to take this action.
        requires_false: bool
            What propositions are required to be false in a state to take this action.
        adds_true: bool
            What propositions are required to be true in a state to take this action.
        adds_false: bool
            What propositions are required to be true in a state to take this action.
    """
    name: str
    requires_true: StripsState
    requires_false: StripsState
    adds_true: StripsState
    adds_false: StripsState

    def strips_action(self) -> StripsAction | None:
        return StripsAction(self.name, self.requires_true, self.adds_true, self.adds_false)

    def __str__(self):
        return self.name
