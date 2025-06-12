from __future__ import annotations
from dataclasses import dataclass
import math
from typing import Dict
from base.action import Action
from base.bot import Bot, G
from base.score import Score
from base.state import State
from datetime import datetime
import random


@dataclass
class ActionStatistics:
    """A small class to track the action statistics.

    Attributes
    ----------
    visits: int
        How many times the action was tried
    accumulated_reward: int
        What was the total reward got by the action.

    Static Methods:
    ---------------
    add_reward(reward: Score) -> None:
        writes down a reward into the statistics
    average_reward() -> float:
        returns an average reward
    """
    visits: int = 0
    accumulated_reward: int = 0

    def add_reward(self, reward: Score):
        self.visits += 1
        self.accumulated_reward += reward

    def average_reward(self) -> float:
        return self.accumulated_reward / self.visits


class UCB(Bot):
    """
    An Upper Confidence Bound player.
    Samples the moves according to the UCB formula, performing random simulations.
    A smarter version of the MonteCarlo player.
    
    For UCB, check: https://www.wikiwand.com/en/Monte_Carlo_tree_search#Exploration_and_exploitation

    Attributes:
    -----------
    timeout: float
        How much time we have to make a move
    total_rollouts: int
        Counts how many times the game was simulated
    action_values: Dict[Action, ActionStatistics]
        Stores statistics about available actions.
    """
    timeout: float
    total_rollouts: int
    action_values: Dict[Action, ActionStatistics]

    def __init__(self, move_timeout: float = 1):
        self.timeout = move_timeout
        self.total_rollouts = 0
        super().__init__()

    def _choose_action(self, from_state: State) -> None:
        '''An entry method, resets some attributes, 
           calls other methods and finally chooses an action
           with the highest average reward'''
        self.start = datetime.now()
        self.total_rollouts = 0
        self.action_values = self._evaluate_actions(from_state)
        self.best_action = max(self.action_values.keys(), key=lambda a: self.action_values[a].average_reward())

    def _any_time_left(self) -> bool:
        """Check whether is a time for another rollout"""
        return (datetime.now() - self.start).total_seconds() < self.timeout

    def _evaluate_actions(self, from_state: State) -> Dict[Action, ActionStatistics]:
        """Main loop of the UCB method

        Parameters
        ----------
        from_state: State
            a current game state

        Returns
        -------
        Dict[Action, ActionStatistics]
            a dictionary storing statistics for every available action
        """

        # TODO:
        # 1) you may start with copying code from the `monte_carlo.py` 
        # 2) change the way the first action is chosen
        #       a) if there is an action, that has not been tried yet, choose it
        #       b) if all actions have been tried, just try one according to the UCB[1]
        #
        # [1] method `self._ucb`
        
        actions = self.game.actions_for(from_state, self.player)
        action_stats = {action: ActionStatistics() for action in actions}

        while self._any_time_left():
            unvisited_actions = [action for action, stats in action_stats.items() if stats.visits == 0]
            
            if unvisited_actions:
                action = random.choice(unvisited_actions)
            else:
                action = max(action_stats.keys(), key=lambda a: self._ucb(action_stats[a]))
                
            next_state = self.game.take_action(from_state, action)
            terminal_state = self._rollout(next_state)
            reward = self.game.reward(terminal_state, self.player)
            action_stats[action].add_reward(reward)
            self.total_rollouts += 1

        return action_stats

    def _ucb(self, action_statistics: ActionStatistics, c=1.4) -> float:
        """An UCB function: https://www.wikiwand.com/en/Monte_Carlo_tree_search#Exploration_and_exploitation"""
        # TODO:
        # 1) implement the UCB formula using `action_statistics` and `self.total_rollouts`
        # - you can assume that the action has been tried at least once
        
        exploitation_term = action_statistics.average_reward()
        exploration_term = c * math.sqrt(math.log(self.total_rollouts) / action_statistics.visits)

        return exploitation_term + exploration_term

    def _rollout(self, from_state: State) -> State:
        """A random game simulation

        Parameters
        ----------
        from_state: State
            a state the simulation starts from

        Returns
        -------
        State:
            a terminal state, the simulation ands in
        """

        # TODO: copy from monte_carlo.py :)
        
        state = from_state
        player = self.player.opponent()
        
        while not self.game.is_terminal_state(state):
            actions = self.game.actions_for(state, player)
            
            if not actions:
                break
            
            action = random.choice(actions)
            state = self.game.take_action(state, action)
            player = player.opponent()
            
        return state

    def metric(self) -> str | None:
        response = f"Has performed {self.total_rollouts} rollouts\n"
        for action, stats in self.action_values.items():
            response += f"  - {action} -> {stats.average_reward()}.\n"
        return response