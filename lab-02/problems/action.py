from __future__ import annotations
from dataclasses import dataclass
from problems.state import StripsProposition, StripsPropositionSchema


@dataclass(frozen=True)
class StripsAction:
    """
    A class that represents a grounded action in a STRIPS domain.

    Attributes:
        name: str
            the full (unique) name of the action
        requires: frozenset[StripsProposition]
            propositions that have to be true for the action to be performed
        adds: frozenset[StripsProposition]
            propositions that become true after performing the action
        removes: frozenset[StripsProposition]
            propositions that become false before performing the action
    """
    name: str
    requires: frozenset[StripsProposition]
    adds: frozenset[StripsProposition]
    removes: frozenset[StripsProposition]

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True)
class StripsActionSchema:
    """
    An ungrounded STRIP action, a schema.

    Attributes:
         name: str
            the unique name of the action schema
        arity: int
            how many arguments the action takes
        requires_schemas: frozenset[StripsPropositionSchema]
            schemas of the propositions that have to be true for the action to be performed
        adds_schemas: frozenset[StripsPropositionSchema]
            schemas of the propositions that become true after performing the action
        removes_schemas: frozenset[StripsPropositionSchema]
            schemas of the propositions that become true after performing the action
    Methods:
        ground(*args: str) -> StripsAction:
            grounds the schema with given objects, yielding an action
    """
    name: str
    arity: int
    requires_schemas: frozenset[StripsPropositionSchema]
    adds_schemas: frozenset[StripsPropositionSchema]
    removes_schemas: frozenset[StripsPropositionSchema]

    def ground(self, *args: str) -> StripsAction:
        """
        Grounds the schema with given objects, yielding an action.

        Parameters:
            args: the objects that are supposed to replace variables in the schema components
                order of the objects should correspond the numbers representing the variables
        Return:
            a grounded action

        """
        name = self.name + "(" + ", ".join(args) + ")"
        preconditions = frozenset(pt.ground(*args) for pt in self.requires_schemas)
        positive_effects = frozenset(pet.ground(*args) for pet in self.adds_schemas)
        negative_effects = frozenset(net.ground(*args) for net in self.removes_schemas)
        return StripsAction(name, preconditions, positive_effects, negative_effects)
