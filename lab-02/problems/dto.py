from __future__ import annotations
from dataclasses import dataclass
from dataclass_wizard import YAMLWizard
import re

"""
This file defines the data transfer objects used to serialize and deserialize
the STRIPS problem to/from YAML. 
"""


@dataclass
class StripsInstanceDTO(YAMLWizard):
    name: str | None
    objects: list[str]
    init: list[str]
    goal: list[str]


@dataclass
class StripsDomainActionDTO(YAMLWizard):
    schema: str
    requires: list[str]
    adds: list[str]
    removes: list[str]


@dataclass
class StripsDomainDTO(YAMLWizard):
    name: str
    predicates: list[str]
    actions: list[StripsDomainActionDTO]


@dataclass
class StripsPropositionDTO:
    name: str
    args: list[str]

    @staticmethod
    def from_string(raw_predicate: str) -> StripsPropositionDTO:
        pattern = r'''^(\w+)\(([^)]*)\)'''
        match = re.match(pattern, raw_predicate)
        try:
            name, input = match.group(1, 2)
            args = [a.strip() for a in input.split(',') if len(a.strip()) > 0]
            return StripsPropositionDTO(name, args)
        except:
            raise Exception(f"{raw_predicate} is not valid representation of a predicate/proposition")
