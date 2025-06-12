from algorithms import *
from games import *
from games.tic_tac_toe.heuristics import *
from games.tic_tac_toe.symmetry_breaking import SymmetryBreakingWrapper
from tournament.tournament import run_tournament

if __name__ == '__main__':
    matches = 4
    move_timeout = 3
    games: list[Game] = [SymmetryBreakingWrapper(ConnectFour())]
    bots = [    
        NegamaxAlphaBetaIDS(NaiveTicTacToeHeuristic, move_timeout),
        NegamaxAlphaBetaDepth(NaiveTicTacToeHeuristic, 6),
        HeuristicPlayer(NaiveTicTacToeHeuristic),
    ]

    run_tournament(games, bots, matches, move_timeout)
