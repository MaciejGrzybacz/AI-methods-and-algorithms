from algorithms import *
from games import *
from games.tic_tac_toe.heuristics import *
from match import Match

if __name__ == "__main__":
    '''Iterative deepening goes over the same nodes many times.
       Maybe setting the depth limit is smarter?'''
    move_timeout = 5
    game = ConnectFour()

    match = Match(game=game,
                  o=NegamaxAlphaBetaDepth(NaiveTicTacToeHeuristic, 6),
                  x=NegamaxAlphaBetaIDS(NaiveTicTacToeHeuristic, move_timeout),
                  move_timeout=move_timeout,
                  print_progress=True)

    match.play()
    match.to_gif("experiment_3")
