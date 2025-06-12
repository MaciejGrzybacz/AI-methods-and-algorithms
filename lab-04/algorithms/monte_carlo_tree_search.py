from __future__ import annotations
from time import sleep
from datetime import datetime
from base.bot import A, Bot, G
from base.player import Player
from base.score import Score
from base.state import State
from base.action import Action
import math
from typing import Generic, Optional, List, Tuple
from dataclasses import dataclass, field
import random


@dataclass
class Node(Generic[A]):
    """A node in the Monte Carlo Tree

    Attributes
    ----------
    game_state: State
        Game state corresponding to the node.
    player: Player
        Which player is expected to move at the given state.
    visits: int
        How many times the action was tried
    accumulated_reward: int
        What was the total reward got by the action.
    parent: Node | None
        A parent node used to propagate the rewards
    action: Action | None
        Which action was used to generate the node
    children: List[Node]
        Contains all the nodes children

    Static Methods:
    ---------------
    is_lead() -> bool:
        checks whether the node is a leaf
    add_reward(reward: Score) -> None:
        writes down a reward into the statistics
    average_reward() -> float:
        returns an average reward
    """

    game_state: State
    player: Player

    accumulated_reward: int = 0
    visits: int = 0

    parent: Optional[Node] = None
    action: Optional[A] = None
    children: List[Node[A]] = field(default_factory=list)

    def is_leaf(self):
        return len(self.children) == 0

    def add_reward(self, reward: Score):
        self.visits += 1
        self.accumulated_reward += reward

    def average_reward(self) -> float:
        return self.accumulated_reward / self.visits


class MCTS(Bot[G, A]):
    """
    A Monte Carlo Tree Search player.
    For details, check https://www.wikiwand.com/en/Monte_Carlo_tree_search

    Attributes:
    -----------
    timeout: float
        How much time we have to make a move
    root: Node | None
        The root node of the Monte Carlo Tree
    use_cache: bool
        Whether the algorithm should reuse results from the previous move.
    """
    timeout: float
    root: Node | None
    use_cache: bool

    def __init__(self, move_timeout: float = 1, use_cache=True):
        super().__init__()
        self.timeout = move_timeout
        self.use_cache = use_cache
        self.root: Optional[Node[A]] = None

    def _any_time_left(self) -> bool:
        """Check whether is a time for another rollout"""
        return (datetime.now() - self.start).total_seconds() < self.timeout

    def _choose_action(self, state: State) -> None:
        self.root = self._find_root(state)
        self.best_action = None
        self.start = datetime.now()
        self._mcts(self.root)

        # TODO:
        # set the best action to a root child, that has been visited most often
        self.best_action = max(self.root.children, key=lambda child: child.visits).action

    def _mcts(self, root: Node):
        """Main MCTS loop updating the search tree via self.root"""
        while self._any_time_left():
            select_node = self._select(root)
            expanded_node = self._expand(select_node)
            reward = self._rollout(expanded_node)
            self._propagate(reward, expanded_node)

    def _find_root(self, state: State) -> Node:
        """Restores root based on the previous move.

        Parameters:
        ----------
        state: State
            the current game state

        Returns:
        --------
        Node
            a new root node
        """
        if not self.use_cache or self.root is None:
            return Node(game_state=state, player=self.player)

        # The code below works, but always return a new root.
        # We can reuse the node from the old tree (self.root is not cleared after the move).
        # 1) if the game is played first time, the self.root is None, create a new root as it's done now
        # 2) otherwise:
        #   - find a node in the tree (starting from self.root) with a `game_state` equal to `state` and return it
        stack: list[Node] = [self.root]
        while stack:
            n = stack.pop()
            if n.game_state == state:
                n.parent = None
                return n
            stack.extend(n.children)

        return Node(game_state=state, player=self.player)

    def _select(self, node: Node) -> Node:
        """
        The selection phase of the MCTS

        Parameters:
        -----------
        node: Node
            the parent node, we want to explore

        Returns
        -------
        Node
            the most promising child to be explored
        """

        # TODO:
        # 1) if node is a leaf, just return it
        # 2) otherwise:
        #   - if there is an unvisited child, return it
        #   - otherwise: choose node maximising the `_ucb` method
        while not node.is_leaf():
            unvisited = [ch for ch in node.children if ch.visits == 0]
            if unvisited:
                node = random.choice(unvisited)
            else:
                node = max(node.children, key=self._ucb)
        return node

    def _expand(self, node: Node) -> Node:
        """
        The expansion phase of the MCTS

        Parameters:
        -----------
        node: Node
            the parent node, we want to expand

        Returns
        -------
        Node
            new node in the tree
        """

        # 1) if node.game_state is terminal, just return the node
        # 2) otherwise:
        #   - add children to the node based on the available actions:
        #       - set correctly parent, player, game_state and action attributes
        #   - return a random child

        if self.game.is_terminal_state(node.game_state):
            return node

        possible_actions = self.game.actions_for(node.game_state, node.player)

        for action in possible_actions:
            new_state = self.game.take_action(node.game_state, action)
            new_player = node.player.opponent()
            new_node = Node(game_state=new_state, player=new_player, parent=node, action=action)
            node.children.append(new_node)

        if node.children:
            return random.choice(node.children)
        else:
            return node

    def _rollout(self, node: Node) -> Score:
        """
        The simulation phase of the MCTS

        Parameters:
        -----------
        node: Node
            the child node corresponding to the action, we want to check

        Returns
        -------
        Score
            a reward received after the simulation...
        """
        # TODO:
        # 1) perform the random game simulation until the game ends
        # - start with the `node.game_state` and `node.player`
        # - remember to flip the player after each move
        # - return the reward!
        #
        # tip. when calculating the reward for the terminal state,
        #      remember from whom is the simulation performed,
        #      for player owning the parent node!    

        current_state = node.game_state
        current_player = node.player

        while not self.game.is_terminal_state(current_state):
            actions = self.game.actions_for(current_state, current_player)
            if not actions:
                break

            action = random.choice(actions)
            current_state = self.game.take_action(current_state, action)
            current_player = current_player.opponent()

        return self.game.reward(current_state, self.player)

    def _propagate(self, reward: Score, node: Node) -> None:
        """
        The propagation phase of the MCTS

        Parameters:
        -----------
        reward:
            what reward the node received due to the simulation
        node: Node
            the currently updated node
        """

        # 1) add reward to the current node (`add_reward` method)
        # 2) propagate reward to the parent node
        #   - remember that the parent has a different view on the score ;)
        cur, r = node, reward
        while cur is not None:
            cur.visits += 1
            cur.accumulated_reward += r
            r = -r
            cur = cur.parent

    @staticmethod
    def _ucb(child: Node, c=1.4) -> float:
        # 1) implement the UCB formula using information in child node
        # - you can assume that the child has been tried at least once
        # - you can assume that the child has a parent node

        exploitation_term = child.average_reward()
        exploration_term = c * math.sqrt(math.log(child.parent.visits) / child.visits)

        return exploitation_term + exploration_term

    def metric(self) -> str | None:
        response = f"Has performed {self.root.visits} rollouts.\n"
        for ch in self.root.children:
            response += f"  - {ch.action} -> {ch.accumulated_reward}/{ch.visits}.\n"
        return response
