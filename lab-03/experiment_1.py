from algorithms import *
from games import *
from games.tic_tac_toe.heuristics import *
from match import Match

if __name__ == "__main__":
    '''A Negamax vs HeuristicPlayer'''
    move_timeout = 5
    game = TicTacToe()

    match = Match(game=game,
                  o=NegamaxAlphaBeta(),
                  x=HeuristicPlayer(NaiveTicTacToeHeuristic),
                  move_timeout=move_timeout,
                  print_progress=True)

    match.play()
    match.to_gif("experiment_1")
