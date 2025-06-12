from algorithms import *
from games import *
from games.tic_tac_toe.heuristics import *
from games.tic_tac_toe.symmetry_breaking import SymmetryBreakingWrapper
from match import Match

if __name__ == "__main__":
    '''Testing if symmtery breaking makes sense'''
    move_timeout = 5
    game = TicTacToe()
    
    match = Match(game = SymmetryBreakingWrapper(game),
                  o = Negamax(),
                  x = HeuristicPlayer(NaiveTicTacToeHeuristic),
                  move_timeout = move_timeout,
                  print_progress = True)
    
    match.play()
    match.to_gif("experiment_2")
