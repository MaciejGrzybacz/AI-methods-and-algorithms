from datetime import datetime
from base.action import Action
from base.game import Game
from base.bot import Bot, HeuristicBot
from base.player import Player
from base.state import State
import stopit
import random
from typing import Generic, Optional, TypeVar

TPlayer = TypeVar('TPlayer', bound=Bot)
TOpponent = TypeVar('TOpponent', bound=Bot)
TState = TypeVar('TState', bound=State)
TAction = TypeVar('TAction', bound=Action)


class Match(Generic[TPlayer, TOpponent]):

    def __init__(self, game: Game,
                       o: TPlayer, 
                       x: TOpponent, 
                       move_timeout = 1,
                       print_progress = False):
        self.game = game
        self.current_state = self.game.initial_state()
        self.current_player = Player.MAX
        o.setup(self.game, Player.MAX)
        x.setup(self.game, Player.MIN)
        self._players = { Player.MAX: o, Player.MIN: x }
        self._players_names = { Player.MAX: "O", Player.MIN: "X" }
        self._move_timeout = move_timeout + 1
        self._print_progress = print_progress
        self.states = [self.current_state]


    def print_progress(self, msg: str):
        if self._print_progress:
            print(msg)    

    def play(self) -> TPlayer | TOpponent | None:
        while not self._is_match_end():
            self.print_progress(self.game.to_ascii(self.current_state))
            self.print_progress(f"{self._players_names[self.current_player]}'s turn. ({self._players[self.current_player].name()})")
            for player, bot in self._players.items():
                if isinstance(bot, HeuristicBot):
                    self.print_progress(f"- heuristic for '{self._players_names[player]}': {bot.heuristic(self.current_state, player)}")
            self.current_state = self._next_move(self._players[self.current_player])
            self.print_progress("====================")
            self.current_player = self.current_player.opponent()
            self.states.append(self.current_state)
        self.print_progress(self.game.to_ascii(self.current_state))
        return self.winner()

    def _next_move(self, player: TPlayer | TOpponent) -> TState:
        start = datetime.now()
        with stopit.ThreadingTimeout(self._move_timeout) as to_ctx_mgr:
            assert to_ctx_mgr.state == to_ctx_mgr.EXECUTING
            _ = player._choose_action(self.current_state)
        self.print_progress(f"Move took {(datetime.now() - start).total_seconds()}s. Time out: {to_ctx_mgr.state == to_ctx_mgr.TIMED_OUT}")
        metric = player.metric()
        if metric is not None:
            self.print_progress(metric)
        
        action = player.best_action
        available_actions = self.game.actions_for(self.current_state, player.player)
        if action == None:
            self.print_progress(f"Bot {player.name()} failed to choose an action, will chose a random one")
            action = random.choice(available_actions)
        elif action not in available_actions:
            self.print_progress(f"Bot {player.name()} chose an illegal action {action}, will be overriden with a random one")
            action = random.choice(available_actions)
            
        return self.game.take_action(self.current_state,  action)

    def _is_match_end(self) -> bool:
        return self.game.is_terminal_state(self.current_state)

    def _is_tie(self) -> bool:
        return self.game.is_tie(self.current_state)

    def to_gif(self, name: str | None):
        object_names = [o.name() for o in [
            self.game, *self._players.values()]]
        img_name = f"{'_'.join(object_names)}.gif" if name is None else f"{name}.gif"
        imgs = [self.game.to_image(state) for state in self.states]
        if all(imgs):
            imgs[0].save(img_name, save_all=True, append_images=imgs[1:],
                         format='GIF', optimize=False, duration=500, loop=1)


    def winner(self) -> TPlayer | TOpponent | None:
        if self._is_match_end() and not self._is_tie():
            return self._players[self.current_player.opponent()]
