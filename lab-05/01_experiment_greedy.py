"""
This experiment shows that greedy selection rule may get stuck on a suboptimal solution.
A more exploration driven rule may find better solutions with time.

The test environment is stored in src/environments/grid_pathfinding/benchmarks/7_bait.txt
The letter "S" marks the initial position.
The letter "B" marks the "bait", a goal node with a low reward (only 10), compared to the real goal "G" (rewarded with 100).
Every step costs -1.
Walls "#" cannot be passed.

The resulting plot shows the accumulated reward — the slope indicates an average reward for a single episode
"""
import logging
from src.action_selection_rules.greedy import GreedyActionSelection
from src.action_selection_rules.epsilon_greedy import EpsilonGreedyActionSelection
from src.action_selection_rules.epsilon_greedy_with_epsilon_decay import EpsilonGreedyActionSelectionWithDecayEpsilon
from src.algorithms.q_learning.qlearning import QLearning
from src.utils.comparator import Comparator
from src.wrappers.discrete_env_wrapper import DiscreteEnvironment
from src.wrappers.named_env_wrapper import NamedEnv
from src.wrappers.stats_wrapper import PlotType

import gym
import src.enviroments.grid_pathfinding as gp
from pathlib import Path

def grid_pathinding_benchmark(n_episodes: int):
    cmp = Comparator()
    policies = cmp.compare_algorithms(
        algorithms=[
            QLearning(.1, 1, GreedyActionSelection()),
            QLearning(.1, 1, EpsilonGreedyActionSelection(.10)),
            QLearning(.1, 1, EpsilonGreedyActionSelection(.20)),
            QLearning(.1, 1, EpsilonGreedyActionSelection(.30)),
            QLearning(.1, 1, EpsilonGreedyActionSelectionWithDecayEpsilon(0.99, 0.99)),
            QLearning(.1, 1, EpsilonGreedyActionSelectionWithDecayEpsilon(0.99, 0.9999))
        ],
        envs=[
            NamedEnv(f"Grid pathfinding: 13_bait.txt", DiscreteEnvironment(
                gym.make("custom/gridpathfinding-v0",
                         file=f"{Path(gp.__file__).parent}/benchmarks/7_bait.txt")))
            ],
        get_algorithm_label=lambda a:a.name(),
        n_episodes=n_episodes,
        plot_types=[PlotType.CumulatedReward])
    cmp.compare_policies(policies, 1000)


if __name__ == '__main__':
    # NOTE: change logging level to logging.DEBUG if you want to observe the experiment visually
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s\n%(message)s')
    grid_pathinding_benchmark(10000)
