from __future__ import annotations
from dataclasses import dataclass
import logging
from typing import Generic, NamedTuple

import numpy as np
from gym.core import ActType, ObsType
from src.action_selection_rules.greedy import GreedyActionSelection
from src.policies.action_value_policy import ActionValuePolicy
from src.algorithms.algorithm import Algorithm
from src.action_selection_rules.generic import ActionSelectionRule
from src.wrappers.discrete_env_wrapper import DiscreteEnvironment
from collections import defaultdict
import random
from src.algorithms.q_learning.dynaq import DynaEntry, DynaMemory, DynaModel
import math


class DynaQPlus(Algorithm[ObsType, ActType, ActionValuePolicy]):
    """
        A DynaQ+ algorithm.
        Stores experience in memory to later replay it and reinforce the learning.
        The exploration is encouraged by an additional reward given to the action
        that haven't be tried for a long time.

        Private Attributes:
            _alpha: float
                The learning rate for the Q-Learning algorithm
            _gamma: float
                The discount factor (tells how much future rewards are discounted)
            _action_selection_rule: ActionSelectionRule[ActType]
                The selection rule used to explore the action space.
            _planning_steps: int
                How many steps of learning are performed using the memory/model.
            _kappa: float
                Size of the bonus factor used to reward exploration.
            _step: int
                Track how many steps has been taken so far.
    """
    def __init__(self, alpha: float, gamma: float, planning_steps: int, kappa: float, action_selection_rule: ActionSelectionRule[ActType]) -> None:
        self._alpha = alpha
        self._gamma = gamma
        self._action_selection_rule = action_selection_rule
        self._planning_steps = planning_steps
        self._kappa = kappa
        self._step = 0
        
    def name(self) -> str:
        return f"DynaQPlus(alpha={self._alpha}, n={self._planning_steps}, kappa={self._kappa},  {self._action_selection_rule.name()})"

    def run(self, n_episodes: int, env: DiscreteEnvironment[ObsType, ActType]):
        model: DynaModel = dict()
        tau = defaultdict(lambda: np.full(env.n_actions, self._step))
        action_value_estimates = defaultdict(lambda: np.zeros(env.n_actions))
        for i in range(n_episodes):
            logging.info(f'Starting episode {i}')
            self._run_episode(env, action_value_estimates, model, tau)
        return ActionValuePolicy(
            action_value_estimates,
            self._action_selection_rule
        )
                
    def _run_episode(self, 
                    env: DiscreteEnvironment[ObsType, ActType], 
                    action_value_estimates: dict[ObsType, np.ndarray[np._ShapeType, float]], 
                    model: DynaModel, 
                    tau: dict[ObsType, np.ndarray]):
        from_observation, _ = env.reset(seed=42, return_info=False)
        is_done = False
        while not is_done:
            logging.debug(env.render('ansi'))
            
            action = self._action_selection_rule(action_value_estimates[from_observation])
            
            to_observation, reward, is_done, _ = env.step(action)
            
            if to_observation not in action_value_estimates:
                action_value_estimates[to_observation] = np.zeros(env.n_actions)
            
            expected_reward = self._calculate_expected_reward(
                previous_observation=from_observation,
                action=action,
                next_observation=to_observation,
                reward=reward,
                action_value_estimates=action_value_estimates
            )
            
            action_value_estimates[from_observation][action] = expected_reward
            
            self._update_tau(tau, from_observation, action)
            
            self._update_model(model, env, from_observation, action, to_observation, reward, is_done)
            
            self._planning(model, tau, action_value_estimates)
            
            from_observation = to_observation
        
        logging.debug('---------------------------------')

    def _update_tau(self, 
                    tau: dict[ObsType, np.ndarray],
                    observation: ObsType, action: ActType):
        
        self._step += 1
        
        for obs_key in tau:
            tau[obs_key] += 1
        
        tau[observation][action] = 0

    def _update_model(self, 
                    model: DynaModel, 
                    env: DiscreteEnvironment[ObsType, ActType], 
                    from_observation: ObsType, action: ActType, 
                    to_observation: ObsType, 
                    reward: float, 
                    is_done: bool):
        
        entry = DynaEntry(to_observation, reward, is_done)
        
        if from_observation in model:
            model[from_observation][action] = entry
        else:
            action_dict = {}
            for a in env.actions():
                if a == action:
                    action_dict[a] = entry
                else:
                    action_dict[a] = DynaEntry(from_observation, 0, False)
            model[from_observation] = action_dict

    def _sample_model(self, model: DynaModel) -> DynaMemory:
        from_observation = random.choice(list(model.keys()))
        action = random.choice(list(model[from_observation].keys()))
        entry = model[from_observation][action]
        
        return DynaMemory(from_observation, action, entry.next_observation, entry.reward, entry.is_done)

    def _planning(self, 
                model: DynaModel, 
                tau: dict[ObsType, np.ndarray], 
                action_value_estimates: dict[ObsType, np.ndarray[np._ShapeType, float]]):
        
        for _ in range(self._planning_steps):
            memory = self._sample_model(model)
            
            if memory.next_observation not in action_value_estimates:
                action_value_estimates[memory.next_observation] = np.zeros(len(action_value_estimates[list(action_value_estimates.keys())[0]]))
            
            bonus = self._kappa * math.sqrt(tau[memory.from_observation][memory.action])
            adjusted_reward = memory.reward + bonus
            
            expected_reward = self._calculate_expected_reward(
                previous_observation=memory.from_observation,
                action=memory.action,
                next_observation=memory.next_observation,
                reward=adjusted_reward,
                action_value_estimates=action_value_estimates
            )
            
            action_value_estimates[memory.from_observation][memory.action] = expected_reward

    def _calculate_expected_reward(self, 
                                previous_observation: ObsType, 
                                action: ActType, 
                                next_observation: ObsType, 
                                reward: float, 
                                action_value_estimates: dict[ObsType, np.ndarray[np._ShapeType, float]]) -> float:
        
        if next_observation not in action_value_estimates:
            action_value_estimates[next_observation] = np.zeros(len(action_value_estimates[list(action_value_estimates.keys())[0]]))
        
        greedy_selector = GreedyActionSelection()
        greedy_action_next = greedy_selector(action_value_estimates[next_observation])
        
        td_target = reward + self._gamma * action_value_estimates[next_observation][greedy_action_next]
        
        td_error = td_target - action_value_estimates[previous_observation][action]
        
        updated_q = action_value_estimates[previous_observation][action] + self._alpha * td_error
        
        return updated_q