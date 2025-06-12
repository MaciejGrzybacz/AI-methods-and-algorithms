"""
This experiment shows that adding Memory and Planning improves performance of the learning algorithm.

The test environments are stored in src/environments/grid_pathfinding/benchmarks/{4,16,25}.txt

The resulting plot shows the accumulated reward — the slope indicates an average reward for a single episode
"""

import logging
from src.action_selection_rules.epsilon_greedy_with_epsilon_decay import EpsilonGreedyActionSelectionWithDecayEpsilon
from src.algorithms.q_learning.qlearning import QLearning
from src.algorithms.q_learning.dynaq import DynaQ
from src.algorithms.q_learning.dynaq_plus import DynaQPlus
from src.utils.comparator import Comparator
from src.wrappers.discrete_env_wrapper import DiscreteEnvironment
from src.wrappers.named_env_wrapper import NamedEnv
from src.wrappers.stats_wrapper import PlotType

import gym
from src.action_selection_rules.epsilon_greedy import EpsilonGreedyActionSelection
import src.enviroments.grid_pathfinding as gp
from pathlib import Path

def grid_pathinding_benchmark(n_episodes: int):
    cmp = Comparator()
    policies = cmp.compare_algorithms(
        algorithms=[
            QLearning(.1, 1, EpsilonGreedyActionSelection(.1)),
            QLearning(.1, 1, EpsilonGreedyActionSelectionWithDecayEpsilon(0.99, 0.99)),
            DynaQ(.1, 1, 50, EpsilonGreedyActionSelection(.1)),
            DynaQPlus(.1, 1, 50, 0.001, EpsilonGreedyActionSelection(.1))
        ],
        envs=[
            NamedEnv(f"Grid pathfinding: {problem_size}", DiscreteEnvironment(
                gym.make("custom/gridpathfinding-v0",
                         file=f"{Path(gp.__file__).parent}/benchmarks/{problem_size}.txt")
            )) for problem_size in ["4", "16", "25"]],
        get_algorithm_label=lambda a:a.name(),
        n_episodes=n_episodes,
        plot_types=[PlotType.CumulatedReward])
    cmp.compare_policies(policies, 100)


if __name__ == '__main__':
    # NOTE: change logging level to logging.DEBUG if you want to observe the experiment visually
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s\n%(message)s')
    grid_pathinding_benchmark(1000)
