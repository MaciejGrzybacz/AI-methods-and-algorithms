from algorithms import *
from games import *
from games.tic_tac_toe.heuristics import *
from tournament.tournament import run_tournament


if __name__ == "__main__":
    '''A benchmark of sampling based algorithms'''
    move_timeout = 1
    game = ConnectFour()
    run_tournament([game], 
                   [
                    MCTS(move_timeout),
                    MonteCarlo(move_timeout),
                    UCB(move_timeout)
                    ],
                    matches=4)
    
