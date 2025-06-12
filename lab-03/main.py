from algorithms import *
from games import *
from games.tic_tac_toe.heuristics import *
from games.tic_tac_toe.symmetry_breaking import SymmetryBreakingWrapper
from match import Match

if __name__ == "__main__":
    move_timeout = 5
    game = ConnectThree()
    wrapped_game = SymmetryBreakingWrapper(game)
    game_heuristic = NaiveTicTacToeHeuristic
    
    match = Match(game = wrapped_game,
                  x = NegamaxAlphaBetaIDS(game_heuristic, move_timeout),
                  o = NegamaxAlphaBetaDepth(NaiveTicTacToeHeuristic, 6),
                  move_timeout = move_timeout,
                  print_progress = True)
    
    match.play()
    match.to_gif()
