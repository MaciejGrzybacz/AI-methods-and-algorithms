from dataclasses import dataclass
from typing import AbstractSet, Iterable
from problems import StripsProblem, StripsState, StripsProposition, StripsAction


@dataclass(eq=True, frozen=True)
class StripsValidationReport:
    """
    A report of the validation of a Strips problem.

    Attributes:
        states: tuple[StripsState, ...]
            The successive states as they are visited following the plan.
        plan: tuple[StripsAction, ...]
            The plan that was validated.
        missing_requirements: tuple[tuple[StripsProposition, ...], ...]
            This collection contains unsatisfied requirements for each action in the plan.
            Optimally, it is a tuple of empty tuples.
        missing_goals: tuple[StripsProposition, ...]
            This collection contains goals yet to be satisfied after executing the plan.

    Properties:
        is_valid: bool
            Whether the plan is valid.
    """
    states: tuple[StripsState, ...]
    plan: tuple[StripsAction, ...]
    missing_requirements: tuple[tuple[StripsProposition, ...], ...]
    missing_goals: tuple[StripsProposition, ...]

    def __str__(self) -> str:
        separator = "====\n>"
        output: list[str] = [f"====\nSTATE 0:\n{self._state_str(self.states[0])}"]
        for i, (action, state, missing) in enumerate(zip(self.plan, self.states[1:], self.missing_requirements)):
            line = f"{separator} ACTION [{i}] {action.name} — "
            if len(missing) == 0:
                line += "SUCCESSFUL"
            else:
                line += "UNSATISFIED PRECONDITIONS:\n"
                line += "\n".join([f"\t- {p}" for p in missing])

            line += f"\n====\nSTATE {i + 1}:\n{self._state_str(state)}"
            output.append(line)

        if self.missing_goals:
            line = f"{separator} UNSATISFIED GOALS:\n"
            for goal in self.missing_goals:
                line += f"\t- {goal}"
            output.append(line)
        else:
            output.append(f"{separator} SATISFIED ALL GOALS")
        if self.is_valid:
            output.append(f"> THE PLAN (LENGTH={len(self.plan)}) IS VALID")
        else:
            output.append(f"> INVALID PLAN")
        return "\n".join(output)

    def _state_str(self, state: StripsState) -> str:
        state_lines = sorted([str(f) for f in state])
        return "\n".join(state_lines)

    @property
    def is_valid(self) -> bool:
        """
        Returns true, if the plan is valid. Otherwise, returns false.
        """
        if len(self.missing_goals) > 0:
            return False
        if len(sum(self.missing_requirements, tuple())) > 0:
            return False
        return True


class StripsPlanValidator:
    """
    A naive validator for STRIPS plans.

    Attributes:
        problem: StripsProblem
            The STRIPS problem involved in the plan.

    Methods:
        validate(plan: Iterable[StripsAction]) -> StripsValidationReport:
            Validates the STRIPS plan, returning a report.
    """
    problem: StripsProblem

    def __init__(self, problem: StripsProblem) -> None:
        self.problem = problem

    def validate(self, plan: Iterable[StripsAction]) -> StripsValidationReport:
        """
        Validates the STRIPS plan, returning a report.
        Parameters:
            plan: a STRIPS plan to be validated.
        Returns:
             a report with errors detected in the plan.
        """
        def missing_propositions(state: StripsState, propositions: AbstractSet[StripsProposition]) \
                -> list[StripsProposition]:
            return [precondition for precondition in propositions if precondition not in state]

        state = self.problem.init_state
        states = [state]
        missing_requirements: list[list[StripsProposition]] = list()
        for action in plan:
            missing_requirements.append(missing_propositions(state, action.requires))
            state = self.problem.take_action(state, action)
            states.append(state)
        missing_goals = missing_propositions(state, self.problem.goals)
        return StripsValidationReport(tuple(states),
                                      tuple(plan),
                                      tuple(tuple(mr) for mr in missing_requirements),
                                      tuple(missing_goals))
