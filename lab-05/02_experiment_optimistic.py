"""
This experiment shows that QLearning is too optimistic.
Double-QLearning fixes this bias.

The test environment is stored in src/environments/grid_pathfinding/benchmarks/16_minefield.txt
The letter "*" marks mines, stepping on the mine ends the game with reward -100.

The resulting plot shows the accumulated reward — the slope indicates an average reward for a single episode
"""

import logging
from src.algorithms.q_learning.qlearning import QLearning
from src.algorithms.q_learning.dynaq import DynaQ
from src.algorithms.q_learning.dynaq_plus import DynaQPlus
from src.algorithms.q_learning.double_q import DoubleQLearning
from src.utils.comparator import Comparator
from src.wrappers.discrete_env_wrapper import DiscreteEnvironment
from src.wrappers.named_env_wrapper import NamedEnv
from src.wrappers.stats_wrapper import PlotType
import src.enviroments
import gym
from src.action_selection_rules.epsilon_greedy import EpsilonGreedyActionSelection
import src.enviroments.grid_pathfinding as gp
from pathlib import Path

def minefield_benchmark(n_episodes: int):
    cmp = Comparator()
    policies = cmp.compare_algorithms(
        algorithms=[
            QLearning(.1, 1, EpsilonGreedyActionSelection(.1)),
            DoubleQLearning(.1, 1, EpsilonGreedyActionSelection(.1))
        ],
        envs=[
            NamedEnv(f"Grid pathfinding: Minefield", DiscreteEnvironment(gym.make(
            "custom/gridpathfinding-v0",
            file=f"{Path(gp.__file__).parent}/benchmarks/16_minefield.txt",
            )))
        ],
        get_algorithm_label=lambda a: a.name(),
        n_episodes=n_episodes,
        plot_types=[PlotType.CumulatedReward])
    cmp.compare_policies(policies, 100)

if __name__ == '__main__':
    # NOTE: change logging level to logging.DEBUG if you want to observe the experiment visually
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s\n%(message)s')
    minefield_benchmark(4000)
