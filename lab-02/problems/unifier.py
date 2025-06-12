from collections import defaultdict
from dataclasses import dataclass
from typing import Iterator

from problems.state import StripsPropositionSchema, StripsState, StripsProposition
from utils.list_utils import split
from utils.queues import Queue, LIFO


def unify(fact: StripsProposition, schema: StripsPropositionSchema,
          grounding: list[str | None]) -> list[str | None] | None:
    """
    Unifies a strips proposition with a schema given a current list of objects.

    Parameters:
        fact: A grounded strips proposition
        schema: A schema of a proposition.
        grounding: A list of objects with `None` marking still ungrounded variables.

    Returns:
        An updated grounding.
    """
    if fact.predicate != schema.predicate:
        return None

    new_grounding = grounding.copy()
    for i, o in zip(schema.args, fact.args):
        if grounding[i] is not None and grounding[i] != o:
            return None
        new_grounding[i] = o
    return new_grounding


def _new_empty_grounding(schemas) -> list[None]:
    """
    Creates a new grounding with enough variables to cover all the provided schemas.

    Parameters:
        schemas: a list of schemas that are supposed to be grounded.
    Returns:
        a new grounding containing enough None elements.
    """
    max_pos_args = max(max(sch.args + (-1,)) for sch in schemas) if len(schemas) > 0 else -1
    num_args = max_pos_args + 1
    empty_grounding = [None] * num_args
    return empty_grounding


def _create_predicates_to_propositions(state: StripsState):
    predicates_to_propositions = defaultdict(list)
    for p in state:
        predicates_to_propositions[p.predicate].append(p)
    return predicates_to_propositions


@dataclass
class StrictUnifier:
    """
    Class designed to find a grounding (set of objects)
    that make the provided schemas true in the given state.

    Attributes:
        state: StripsState
            A state that should unify with the schemas.
        objects: frozenset[str]
            All objects in the corresponding problem.

    Methods:
        matches(schemas: list[StripsPropositionSchema]) -> Iterator[list[str]]:
            Yields all possible groundings, that make the schemas true in the given state.
            Grounding is just list of objects (strings) that can be used to ground the schemas.
    """
    state: StripsState
    objects: frozenset[str]

    def matches(self,
                schemas: list[StripsPropositionSchema]) -> Iterator[list[str]]:
        """
        Yields all possible groundings, that make the provided schemas true in the given state.
        The grounding may be later used to ground the schemas leading to actions.
        """
        assert len(schemas) > 0, \
            "cannot match empty set of schemas"
        empty_grounding = _new_empty_grounding(schemas)
        predicates_to_propositions = _create_predicates_to_propositions(self.state)

        sorted_pos_schemas = sorted(schemas, key=lambda s: len(predicates_to_propositions[s.predicate]))

        candidates: Queue[tuple[list[str | None], list[StripsPropositionSchema]]] = LIFO()
        candidates.push((empty_grounding, sorted_pos_schemas))
        while not candidates.is_empty():
            cand_grounding, cand_schemas = candidates.pop()
            grnd_schemas, left_schemas = split(cand_schemas, lambda x: x.can_be_grounded(*cand_grounding))

            if any(pos_schema.ground(*cand_grounding) not in self.state for pos_schema in grnd_schemas):
                continue

            if len(left_schemas) > 0:
                first_schema, *new_schemas = left_schemas
                for p in predicates_to_propositions[first_schema.predicate]:
                    new_grounding = unify(p, first_schema, cand_grounding)
                    if new_grounding is not None:
                        candidates.push((new_grounding, new_schemas))
                continue

            if None in cand_grounding:
                for obj in self.objects:
                    new_grounding = cand_grounding.copy()
                    new_grounding[new_grounding.index(None)] = obj
                    candidates.push((new_grounding, left_schemas))
                continue

            yield cand_grounding
