from problems import (StripsProblem, StripsActionSchema, StripsPredicate, StripsProposition, StripsPropositionSchema,
                      StripsState)
from problems.dto import StripsDomainDTO, StripsInstanceDTO, StripsPropositionDTO

"""
This file contains code related to building a STRIPS problem from YAML files.
"""


class StripsProblemBuilder:
    domain_raw: str
    instance_raw: str

    def __init__(self, domain_raw: str, instance_raw: str) -> None:
        self.domain_raw = domain_raw
        self.instance_raw = instance_raw

    def build(self) -> StripsProblem:
        domain_dto = StripsDomainDTO.from_yaml(self.domain_raw)
        instance_dto = StripsInstanceDTO.from_yaml(self.instance_raw)

        name = f"{domain_dto.name} - {instance_dto.name}"

        predicates = StripsProblemBuilder.get_predicates(domain_dto)
        actions = StripsProblemBuilder.get_actions(domain_dto, predicates)
        objects = StripsProblemBuilder.get_objects(instance_dto)
        init_state = StripsProblemBuilder.get_state(instance_dto.init, objects, predicates)
        goal_state = StripsProblemBuilder.get_state(instance_dto.goal, objects, predicates)
        return StripsProblem(name, objects, list(actions.values()), init_state, goal_state)

    @staticmethod
    def get_predicates(domain: StripsDomainDTO) -> dict[str, StripsPredicate]:
        predicates_definitions = domain.predicates
        assert len(predicates_definitions) > 0, "the STRIPS domain should define at least one predicate"
        predicates: dict[str, StripsPredicate] = dict()
        for predicate_definition in predicates_definitions:
            predicate_dto = StripsPropositionDTO.from_string(predicate_definition)
            predicate_name = predicate_dto.name
            assert predicate_name not in predicates, f"a predicate name '{predicate_name}' is duplicated"
            predicate = StripsPredicate(predicate_name, len(predicate_dto.args))
            predicates[predicate_name] = predicate
        return predicates

    @staticmethod
    def get_actions(domain: StripsDomainDTO, domain_predicates: dict[str, StripsPredicate]) \
            -> dict[str, StripsActionSchema]:
        actions_definitions = domain.actions
        assert len(actions_definitions) > 0, "the STRIPS domain should define at least one action"
        action_schemas: dict[str, StripsActionSchema] = dict()
        for action_definition in actions_definitions:
            action_predicate = StripsPropositionDTO.from_string(action_definition.schema)
            action_name = action_predicate.name
            assert action_name not in action_schemas, f"action name {action_name} is duplicated"
            action_arity = len(action_predicate.args)
            left_args = set(action_predicate.args)

            def init_proposition_schemas(definitions: list[str]) -> frozenset[StripsPropositionSchema]:
                templates: list[StripsPropositionSchema] = []
                for definition in definitions:
                    definition_predicate = StripsPropositionDTO.from_string(definition)
                    predicate_name: str = definition_predicate.name
                    assert predicate_name in domain_predicates, f"action {action_name} is using an unknown predicate {predicate_name}"
                    predicate = domain_predicates[predicate_name]
                    predicate_args: list[str] = definition_predicate.args
                    assert len(
                        predicate_args) == predicate.arity, f"action {action_name} uses predicate '{predicate_name}/{predicate.arity}' with incorrect number of arguments"
                    assert all([pa in action_predicate.args for pa in
                                predicate_args]), f"action {action_name} calls '{definition} with unknown argument"
                    predicate_args_indexes = [action_predicate.args.index(pa) for pa in predicate_args]
                    left_args.difference_update(predicate_args)
                    templates.append(StripsPropositionSchema(predicate, tuple(predicate_args_indexes)))
                return frozenset(templates)

            action_requires_schemas = init_proposition_schemas(action_definition.requires)
            action_pos_effects_schemas = init_proposition_schemas(action_definition.adds)
            action_neg_effects_schemas = init_proposition_schemas(action_definition.removes)

            assert len(action_pos_effects_schemas.intersection(action_neg_effects_schemas)) == 0, \
                (f"the negative and positive effects should not share elements: {action_name}\n"
                 f"{action_pos_effects_schemas.intersection(action_neg_effects_schemas)}")
            assert len(left_args) == 0, \
                f'action "{action_name}" has arguments unused in its body: {",".join(left_args)}'
            action_schemas[action_name] = StripsActionSchema(action_name,
                                                             action_arity,
                                                             action_requires_schemas,
                                                             action_pos_effects_schemas,
                                                             action_neg_effects_schemas)
        return action_schemas

    @staticmethod
    def get_objects(instance: StripsInstanceDTO) -> frozenset[str]:
        assert len(instance.objects) > 0, f"problem instance should have at least single object"
        assert len(set(instance.objects)) == len(instance.objects), f"problem instance contains duplicate objects"
        return frozenset(instance.objects)

    @staticmethod
    def get_state(propositions: list[str], instance_objects: frozenset[str],
                  domain_predicates: dict[str, StripsPredicate]) -> StripsState:
        true_propositions: list[StripsProposition] = []
        for proposition in propositions:
            proposition_predicate = StripsPropositionDTO.from_string(proposition)
            assert proposition_predicate.name in domain_predicates, f"instance definition uses an unknown predicate: '{proposition_predicate.name}'"
            predicate = domain_predicates[proposition_predicate.name]
            assert all([pa in instance_objects for pa in
                        proposition_predicate.args]), f"instance definition uses predicate with unknown object as argument: {proposition}"
            assert len(
                proposition_predicate.args) == predicate.arity, f"instance definition states predicate '{proposition_predicate.name}' with incorrect number of arguments"
            true_propositions.append(StripsProposition(predicate, tuple(proposition_predicate.args)))
        return StripsState(frozenset(true_propositions))
