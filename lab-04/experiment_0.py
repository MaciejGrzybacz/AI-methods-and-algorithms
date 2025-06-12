from algorithms import *
from games import *
from games.tic_tac_toe.heuristics import *
from tournament.tournament import run_tournament


if __name__ == "__main__":
    '''A primitive benchmark of primitve algorithms'''
    move_timeout = 3
    game = ConnectFour()
    run_tournament([game], 
                   [RandomPlayer(),
                    NearSighted(),
                    HeuristicPlayer(EmptyTicTacToeHeuristic),
                    HeuristicPlayer(NaiveTicTacToeHeuristic)],
                    matches=8)
    
