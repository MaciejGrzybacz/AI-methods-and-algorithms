from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable

from rich.panel import Panel

from base.bot import Bot
from base.game import Game
from match import Match


@dataclass
class CompetitionParams:
    n_matches: int
    move_timeout: int


@dataclass
class BotResults:
    bot_name: Bot
    victories: int


@dataclass
class CompetitionResults:
    player: BotResults
    opponent: BotResults
    matches_played: int

    def winner_results(self):
        if self.player.victories > self.opponent.victories:
            return self.player
        if self.player.victories < self.opponent.victories:
            return self.opponent

    def __rich__(self):
        pv, ov = self.player.victories, self.opponent.victories
        border_style = "yellow"
        if pv > ov:
            border_style = "green"
        if ov > pv:
            border_style = "red"
        return Panel(
            f"{self.player.bot_name}: {self.player.victories}\n"
            f"{self.opponent.bot_name}: {self.opponent.victories}\n"
            f"Total matches: {self.matches_played}",
            title=f'{self.player.bot_name} vs {self.opponent.bot_name}',
            border_style=border_style
        )


def run_competition(
        bot_a: Bot | tuple[Bot, str],
        bot_b: Bot | tuple[Bot, str],
        game: Game, params: CompetitionParams) -> CompetitionResults:
    bot_names = dict(assign_names_to_bots([bot_a, bot_b]))
    victories = defaultdict(int)
    bot_a = bot_a[0] if isinstance(bot_a, tuple) else bot_a
    bot_b = bot_b[0] if isinstance(bot_b, tuple) else bot_b
    print(f"> {game.name()}: {bot_a.name()} vs {bot_b.name()}")
    for i in range(params.n_matches):
        match = Match(game, bot_a, bot_b, move_timeout=params.move_timeout)
        winner = match.play()
        if winner:
            print(f"- {i+1}/{params.n_matches}: {winner.name()} won!")
            victories[winner] += 1
        else:
            print(f"- {i+1}/{params.n_matches}: tie")
        bot_a, bot_b = bot_b, bot_a
        
    return CompetitionResults(*[BotResults(
        name,
        victories[bot]
    ) for bot, name in bot_names.items()
    ], matches_played=params.n_matches)


def assign_names_to_bots(bots: Iterable[Bot | tuple[Bot, str]]) -> list[tuple[Bot, str]]:
    return [b if isinstance(b, tuple) else (b, b.name())
            for b in bots
            ]
