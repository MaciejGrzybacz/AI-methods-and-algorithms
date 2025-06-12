from algorithms import *
from games import *
from games.tic_tac_toe.heuristics import *
from match import Match

if __name__ == "__main__":
    '''Is alpha-beta pruning really useful?'''
    move_timeout = 5
    game = ConnectFour()

    match = Match(game=game,
                  o=NegamaxAlphaBetaIDS(NaiveTicTacToeHeuristic, move_timeout, prune_branches=False),
                  x=NegamaxAlphaBetaIDS(NaiveTicTacToeHeuristic, move_timeout),
                  move_timeout=move_timeout,
                  print_progress=True)

    match.play()
    match.to_gif("experiment_4")
