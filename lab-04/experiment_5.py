from algorithms import *
from games import *
from games.tic_tac_toe.heuristics import *
from match import Match

if __name__ == "__main__":
    '''A duel between to best algorithms in their classes: MCTS and NegamaxAlphaBetaIDS'''
    move_timeout = 5
    game = ConnectFour()
    
    match = Match(game = game,
                  o = NegamaxAlphaBetaIDS(NaiveTicTacToeHeuristic, move_timeout),
                  x = MCTS(move_timeout),
                  move_timeout = move_timeout,
                  print_progress = True)
    
    match.play()
    match.to_gif("experiment_5")
