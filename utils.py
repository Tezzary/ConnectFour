import random
import logic
import torch

test_board = [
    [1, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 0, 0],
    [2, 2, 0, 1, 0, 0, 2],
    [1, 1, 1, 2, 0, 0, 1],
    [2, 2, 2, 1, 0, 1, 2]
    ]

def board_to_site_format(board):
    current_player = 1
    running_text = ""
    game_length = get_game_length(board)
    indexes_used = []
    while True:
        if len(running_text) == game_length:
            break
        for x in range(7):
            for y in range(6):
                temp = 5 - y
                index_exists = 7 * temp + x in indexes_used
                if index_exists:
                    continue
                if board[temp][x] == current_player:
                    current_player = 2 if current_player == 1 else 1
                    running_text += str(x + 1)
                    indexes_used.append(7 * temp + x)
                else:
                    break

    return running_text

def board_to_tensor(board):
    if type(board) == str:
        board = site_to_board_format(board)

    move_count = get_game_length(board)
    if move_count % 2 == 0:
        current_player = 1
    else:
        current_player = 2
    tensor = torch.zeros(42, dtype=torch.float)
    for y in range(6):
        for x in range(7):
            index = 7 * y + x
            if board[y][x] == current_player:
                tensor[index] = 1
            elif board[y][x] == 0:
                tensor[index] = 0
            else:
                tensor[index] = -1
    return tensor

def site_to_board_format(site_format):
    board = [[0 for x in range(7)] for y in range(6)]
    current_player = 1
    for char in site_format:
        column = int(char) - 1
        for y in range(6):
            temp = 5 - y
            if board[temp][column] == 0:
                board[temp][column] = current_player
                current_player = 2 if current_player == 1 else 1
                break
    return board

def get_game_length(board):
    return sum([1 for x in range(7) for y in range(6) if board[y][x] != 0])

def generate_random_position():
    board = ""
    game_length = random.randrange(0, 42)
    col_count = [0 for x in range(7)]
    while True:
        if len(board) == game_length:
            matrix_board = site_to_board_format(board)
            if logic.checkWin(matrix_board, 1) or logic.checkWin(matrix_board, 2):
                board = ""
                col_count = [0 for x in range(7)]
                #game_length = random.randrange(0, 42)
            else:
                break
        col = random.randrange(0, 7)
        if col_count[col] == 6:
            continue
        col_count[col] += 1
        board += str(col + 1)
    return board

if __name__ == "__main__":
    print(test_board)
    print(board_to_site_format(test_board))
    print(site_to_board_format(board_to_site_format(test_board)))