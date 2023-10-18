import subprocess
import os
import utils
import logic


def evaluate_board(process, board):
    #board_string = utils.board_to_site_format(board)
    board_string = board
    print(board_string)
    process.stdin.write(board_string + "\n")
    process.stdin.flush()

    stdout = process.stdout.readline()

    evaluation = int(stdout.split(" ")[1])
    print(evaluation)
    return evaluation

directory = os.path.join("MoveGenerator", "connect4", "c4solver")

def pick_move(process, board):
    current_player = logic.player
    valid_boards, valid_columns = utils.possibleMoves(board, current_player)
    best_move = -1
    best_evaluation = -1000000
    for i in range(len(valid_boards)):
        print(valid_boards[i])
        board = utils.board_to_site_format(valid_boards[i])
        print(board)
        evaluation = -evaluate_board(process, board)
        if evaluation > best_evaluation:
            best_evaluation = evaluation
            best_move = valid_columns[i]
    return best_move, evaluation
    

class Player:
    def __init__(self):
        self.process = subprocess.Popen([directory, "-", "w"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    def make_move(self, board, events, size, player):
        print(board)
        return pick_move(self.process, board)
