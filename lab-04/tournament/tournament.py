from itertools import combinations
from base.bot import Bot
from base.game import Game
from games.tic_tac_toe.heuristics import EmptyTicTacToeHeuristic, NaiveTicTacToeHeuristic
from tournament.run_competition import CompetitionParams, CompetitionResults, run_competition
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from itertools import chain
from games import *
from algorithms import *
from games.tic_tac_toe.symmetry_breaking import SymmetryBreakingWrapper

def print_summary(console: Console, game_name: str, competitions_results: list[CompetitionResults]):
    print_score_table(console, game_name, competitions_results)
    print_detailed_summary(console, competitions_results)


def print_score_table(console: Console, game_name: str, competitions_results: list[CompetitionResults]):
    bot_names = [(result.player.bot_name, result.opponent.bot_name) for result in competitions_results]
    bot_match_victories = {name: 0 for name in chain(*bot_names)}
    for result in competitions_results:
        winner_results = result.winner_results()
        if winner_results:
            name = winner_results.bot_name
            bot_match_victories[name] += 1
    ranking = sorted(bot_match_victories.items(), key=lambda x: x[1], reverse=True)
    score_table = '\n'.join([f'{bot_name}: {victories_count}' for (bot_name, victories_count) in ranking])
    console.print(Panel(
        score_table,
        title=f'Score table: {game_name}',
        style='blue'
    ))


def print_detailed_summary(console: Console, competitions_results: list[CompetitionResults]):
    console.print(Columns(competitions_results))

def run_tournament(games: list[Game],
                   bots: list[Bot],
                   matches: int = 4, 
                   move_timeout: float = 3):
    console = Console()
    params = CompetitionParams(matches, move_timeout)
    for game in games:
        results = [run_competition(bot_a_type, bot_b_type, game, params)
                   for bot_a_type, bot_b_type in combinations(bots, 2)]
        print_summary(console, game.name(), results)
