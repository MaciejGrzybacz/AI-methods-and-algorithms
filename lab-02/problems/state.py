from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class StripsPredicate:
    """
    A STRIPS predicate.

    Attributes:
        name: str
            A (unique) name of the predicate.
        arity: int
            How many argument this predicate takes.
    """
    name: str
    arity: int


@dataclass(frozen=True)
class StripsProposition:
    """
    A grounded STRIPS proposition.

    Attributes:
        predicate: StripsPredicate
            What predicate defines this STRIPS proposition, e.g. "on_table/2"
        args: tuple[str, ...]
            Arguments passed to the predicate to make, e.g. '("a", "b")
        
        Together they makey on_table("a", "b").
    """
    predicate: StripsPredicate
    args: tuple[str, ...]

    def __str__(self) -> str:
        return self.predicate.name + "(" + ", ".join(self.args) + ")"


"""
A STRIPS state is just a set of grounded STRIPS propositions.
"""
StripsState = frozenset[StripsProposition]


@dataclass(frozen=True)
class StripsPropositionSchema:
    """
    An ungrounded proposition, i.e., a schema of STRIPS proposition.
    The variables in the schema are represented by numbers, i.e.
    - "on_table(1,2)" has two variables.
    The variables are shared by various propositions schemata inside an action.

    Attributes:
         predicate: StripsPredicate
            What predicate defines this schema, e.g. "on_table/2"
         args: tuple[int, ...]
            the variables in the schema, e.g. [1,2].

    Methods:
        can_be_grounded(*objects: str | None) -> bool
            Whether the schema could be grounded given objects.
            A schema can be grounded, if the provided collection of objects
            contains objects (not `None`) at indices included in `self.args`
        ground(*objects: str | None) -> StripsProposition
            Grounds the schema to produce a STRIPS proposition.
            Basically, it replaces `self.args` with objects at corresponding indices.
    """
    predicate: StripsPredicate
    args: tuple[int, ...]

    def can_be_grounded(self, *objects: str | None) -> bool:
        """
            Whether the schema could be grounded given objects.
            A schema can be grounded, if the provided collection of objects
            contains objects (not `None`) at indices included in `self.args`
        """
        if len(self.args) == 0:
            return True

        assert len(objects) > max(self.args), \
            f"tried to use predicate {self.predicate} with incorrect number of arguments {objects}, {self.args}: {len(objects)} > {max(self.args)}"
        return all(objects[arg] is not None for arg in self.args)

    def ground(self, *objects: str | None) -> StripsProposition:
        """
        Grounds the schema to produce a STRIPS proposition.
        Basically, it replaces `self.args` with objects at corresponding indices.
        """
        if len(self.args) == 0:
            return StripsProposition(self.predicate, tuple())
        assert len(objects) > max(self.args), \
            f"tried to use predicate {self.predicate} with incorrect number of arguments {objects}, {self.args}: {len(objects)} > {max(self.args)}"
        built_args = tuple(objects[a] for a in self.args)
        return StripsProposition(self.predicate, built_args)
