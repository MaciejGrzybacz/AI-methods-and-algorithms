"""
This experiment shows memory in a dynamic environment may be misleading.
DynaQPlus knows it has to update the memory :)

The test environment is stored in src/environments/grid_pathfinding/benchmarks/13_dynamic.txt
The letter "D" marks walls that will disappear after the 1/3 of the simulation passed (line `open_after=int(n_episodes / 3)))`)

The resulting plot shows the accumulated reward — the slope indicates an average reward for a single episode
"""

import logging
import random
from src.action_selection_rules.epsilon_greedy_with_epsilon_decay import EpsilonGreedyActionSelectionWithDecayEpsilon
from src.algorithms.q_learning.qlearning import QLearning
from src.algorithms.q_learning.dynaq import DynaQ
from src.algorithms.q_learning.dynaq_plus import DynaQPlus
from src.utils.comparator import Comparator
from src.wrappers.discrete_env_wrapper import DiscreteEnvironment
from src.wrappers.stats_wrapper import PlotType
import src.enviroments
import gym
from src.action_selection_rules.epsilon_greedy import EpsilonGreedyActionSelection
import src.enviroments.grid_pathfinding as gp
from pathlib import Path

def dynamic_pathinding_benchmark(n_episodes: int):
    cmp = Comparator()
    policies = cmp.compare_algorithms(
        algorithms=[
            DynaQPlus(.1, 1, 50, 0.01, EpsilonGreedyActionSelectionWithDecayEpsilon(0.99, 0.99)),
            DynaQ(.1, 1, 50, EpsilonGreedyActionSelectionWithDecayEpsilon(0.99, 0.99)),
            QLearning(.1, 1, EpsilonGreedyActionSelectionWithDecayEpsilon(0.99, 0.99)),
            QLearning(.1, 1, EpsilonGreedyActionSelection(0.05)),
            ],
        envs=[
            DiscreteEnvironment(gym.make(
            "custom/gridpathfinding-v0",
            file=f"{Path(gp.__file__).parent}/benchmarks/13_dynamic.txt",
            open_after=int(n_episodes / 3)))
        ],
        get_algorithm_label=lambda a: a.name(), n_episodes=n_episodes,
        plot_types=[PlotType.CumulatedReward])
    cmp.compare_policies(policies, 100)

if __name__ == '__main__':
    # NOTE: change logging level to logging.DEBUG if you want to observe the experiment visually
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s\n%(message)s')
    dynamic_pathinding_benchmark(2000)
