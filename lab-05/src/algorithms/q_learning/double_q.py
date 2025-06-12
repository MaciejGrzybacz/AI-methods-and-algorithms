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
import random

class DoubleQLearning(Algorithm[ObsType, ActType, ActionValuePolicy]):
    """
        A Double Q-Learning algorithm.
        Uses two Q-values sets to interplay as a learner and a critic.

        Private Attributes:
            _alpha: float
                The learning rate for the Q-Learning algorithm
            _gamma: float
                The discount factor (tells how much future rewards are discounted)
            _action_selection_rule: ActionSelectionRule[ActType]
                The selection rule used to explore the action space.
    """
    def __init__(self, alpha: float, gamma: float, action_selection_rule: ActionSelectionRule[ActType]) -> None:
        self._alpha = alpha
        self._gamma = gamma
        self._action_selection_rule = action_selection_rule

    def name(self) -> str:
        return f"DoubleQLearning(alpha={self._alpha}, {self._action_selection_rule.name()})"       
    
    def run(self, n_episodes: int, env: DiscreteEnvironment[ObsType, ActType]):
        action_value_estimates_a = defaultdict(lambda: np.zeros(env.n_actions))
        action_value_estimates_b = defaultdict(lambda: np.zeros(env.n_actions))
        for i in range(n_episodes):
            logging.info(f'Starting episode {i}')
            self._run_episode(env, action_value_estimates_a, action_value_estimates_b)
        return ActionValuePolicy(
            action_value_estimates_a,
            self._action_selection_rule
        )

    
    def _run_episode(self, 
                    env: DiscreteEnvironment[ObsType, ActType], 
                    action_value_estimates_a: dict[ObsType, np.ndarray[np._ShapeType, float]], 
                    action_value_estimates_b: dict[ObsType, np.ndarray[np._ShapeType, float]]):
        """ Trains algorithm on a single episode."""
        from_observation, _ = env.reset(seed=42, return_info=False)
        is_done = False
        while not is_done:
            logging.debug(env.render('ansi'))
            
            combined_estimates = (action_value_estimates_a[from_observation] + 
                                action_value_estimates_b[from_observation]) / 2
            action = self._action_selection_rule(combined_estimates)
            
            to_observation, reward, is_done, _ = env.step(action)
            
            if to_observation not in action_value_estimates_a:
                action_value_estimates_a[to_observation] = np.zeros(env.n_actions)
            if to_observation not in action_value_estimates_b:
                action_value_estimates_b[to_observation] = np.zeros(env.n_actions)
            
            if random.random() > 0.5:
                expected_reward = self._calculate_expected_reward(
                    previous_observation=from_observation,
                    action=action,
                    next_observation=to_observation,
                    reward=reward,
                    learner=action_value_estimates_a,
                    critic=action_value_estimates_b
                )
                action_value_estimates_a[from_observation][action] = expected_reward
            else:
                expected_reward = self._calculate_expected_reward(
                    previous_observation=from_observation,
                    action=action,
                    next_observation=to_observation,
                    reward=reward,
                    learner=action_value_estimates_b,
                    critic=action_value_estimates_a
                )
                action_value_estimates_b[from_observation][action] = expected_reward
            
            from_observation = to_observation
        
        logging.debug('---------------------------------')
    
    def _calculate_expected_reward(self, 
                                previous_observation: ObsType, 
                                action: ActType,
                                next_observation: ObsType, 
                                reward: float, 
                                learner: dict[ObsType, np.ndarray[np._ShapeType, float]],
                                critic: dict[ObsType, np.ndarray[np._ShapeType, float]]) -> float:
        greedy_selector = GreedyActionSelection()
        greedy_action_next = greedy_selector(learner[next_observation])
        
        td_target = reward + self._gamma * critic[next_observation][greedy_action_next]
        
        td_error = td_target - learner[previous_observation][action]
        
        updated_q = learner[previous_observation][action] + self._alpha * td_error
        
        return updated_q