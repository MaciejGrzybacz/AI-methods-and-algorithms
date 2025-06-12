from __future__ import annotations
from dataclasses import dataclass
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


class MonteCarlo(Bot):
    """
    A MonteCarlo player.
    Plays the game randomly as long as possible and then chooses a move that statistically was the best.
    
    Attributes:
    -----------
    timeout: float
        How much time we have to make a move
    total_rollouts: int
        Counts how many times the game was simulated
    action_values: Dict[Action, ActionStatistics]
        Stores statistics about available actions
    """
    timeout: float
    total_rollouts: int
    action_values: Dict[Action, ActionStatistics] 

    def __init__(self, move_timeout: float = 1):
        self.timeout = move_timeout 
        self.total_rollouts = 0
        super().__init__()

    def _choose_action(self, from_state: State) -> None:
        """An entry method, resets some attributes,
           calls other methods and finally chooses an action
           with the highest average reward"""
        self.start = datetime.now()
        self.total_rollouts = 0
        self.action_values = self._evaluate_actions(from_state)
        self.best_action = max(self.action_values, key=lambda a: self.action_values[a].average_reward())

    def _any_time_left(self) -> bool:
        """Check whether is a time for anoter rollout"""
        return (datetime.now() - self.start).total_seconds() < self.timeout
    
    def _evaluate_actions(self, from_state: State) -> Dict[Action, ActionStatistics]:
        """
        Main loop of the MonteCarlo method

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
        # 1) create initial dictionary of statistics for every available action 
        # 2) create a loop going as long as there is time left [1]
        #   - choose a random action and use to get the next state
        #   - perform a random rollout [2] from this state and check its reward 
        #   - update statistics with the result of the rollout [3]
        #   - increment self.total_rollouts
        # 3) return the dictionary
        #
        # [1] method `self._any_time_left`
        # [2] method `self._rollout`
        # [3] method `add_reward`
        
        actions = self.game.actions_for(from_state, self.player)
        action_stats = {action: ActionStatistics() for action in actions}

        while self._any_time_left():
            action = random.choice(actions)
            next_state = self.game.take_action(from_state, action)
            terminal_state = self._rollout(next_state)
            reward = self.game.reward(terminal_state, self.player)
            action_stats[action].add_reward(reward)
            self.total_rollouts += 1

        return action_stats

    def _rollout(self, from_state: State) -> State:
        """A random game simulation

        Parameters
        ----------
        from_state: State
            a state the simulation starts from

        Returns
        -------
        State:
            a terminal state, the simulation ends in
        """

        # TODO:
        # 1) perform the random game simulation until the game ends (reaches the terminal state)
        # - start with the `self.player.opponent()` as the player
        # - remember to flip the player after each move
        # return the terminal state!
        
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
            response += f"  - {action} -> {stats.average_reward}.\n"
        return response