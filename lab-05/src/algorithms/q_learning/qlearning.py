from __future__ import annotations
import logging
from typing import Callable, Generic, Tuple

import numpy as np
from gym.core import ActType, ObsType
from src.action_selection_rules.greedy import GreedyActionSelection
from src.policies.action_value_policy import ActionValuePolicy
from src.algorithms.algorithm import Algorithm
from src.action_selection_rules.generic import ActionSelectionRule
from src.wrappers.discrete_env_wrapper import DiscreteEnvironment
from collections import defaultdict


class QLearning(Algorithm[ObsType, ActType, ActionValuePolicy]):
    """
    A basic Q-Learning algorithm

    Private Attributes:
        _alpha: float
            The learning rate for the Q-Learning algorithm
        _gamma: float
            The discount factor (tells how much future rewards are discounted)
        _action_selection_rule: ActionSelectionRule[ActType]
            The selection rule used to explore the action space.
    """
    _alpha: float
    _gamma: float
    _action_selection_rule: ActionSelectionRule[ActType]

    def __init__(self, alpha: float, gamma: float, action_selection_rule: ActionSelectionRule[ActType]) -> None:
        self._alpha = alpha
        self._gamma = gamma
        self._action_selection_rule = action_selection_rule

    def name(self) -> str:
        return f"QLearning(alpha={self._alpha}, {self._action_selection_rule.name()})"

    def run(self, n_episodes: int, env: DiscreteEnvironment[ObsType, ActType]) -> ActionValuePolicy[ObsType, ActType]:
        action_value_estimates = defaultdict(lambda: np.zeros(env.n_actions))
        for i in range(n_episodes):
            logging.info(f'Starting episode {i}')
            self._run_episode(env, action_value_estimates)
        return ActionValuePolicy(
            action_value_estimates,
            self._action_selection_rule
        )

    def _run_episode(self,
                     env: DiscreteEnvironment[ObsType, ActType],
                     action_value_estimates: dict[ObsType, np.ndarray[np._ShapeType, float]]):
        """
        Runs a single episode of the algorithm.
        """

        # initial observation (e.g. position on the grid)
        from_observation, _ = env.reset(seed=42)
        # whether the episode has finished
        is_done = False

        while not is_done:
            logging.debug(env.render('ansi'))

            action = self._action_selection_rule(action_value_estimates[from_observation])

            to_observation, reward, is_done, _ = env.step(action)

            if to_observation not in action_value_estimates:
                action_value_estimates[to_observation] = np.zeros(env.action_space.n)

            expected_reward = self._calculate_expected_reward(
                previous_observation=from_observation,
                action=action,
                next_observation=to_observation,
                reward=reward,
                action_value_estimates=action_value_estimates
            )

            current_qvalues = action_value_estimates[from_observation]
            current_qvalues[action] = expected_reward

            from_observation = to_observation

        logging.debug('---------------------------------')

    def _calculate_expected_reward(self,
                                   previous_observation: ObsType,
                                   action: ActType,
                                   next_observation: ObsType,
                                   reward: float,
                                   action_value_estimates: dict[ObsType, np.ndarray[np._ShapeType, float]]) -> float:
        """ Updates the expected reward of taking an action in the given state. """

        if next_observation not in action_value_estimates:
            action_value_estimates[next_observation] = np.zeros(self.env.action_space.n)

        greedy_selector = GreedyActionSelection()
        greedy_action_next = greedy_selector(action_value_estimates[next_observation])

        td_target = reward + self._gamma * action_value_estimates[next_observation][greedy_action_next]

        td_error = td_target - action_value_estimates[previous_observation][action]

        updated_q = action_value_estimates[previous_observation][action] + self._alpha * td_error

        return updated_q
