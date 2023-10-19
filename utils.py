import random
import torch

test_board = [[0, 0, 0, 0, 2, 0, 0], 
              [0, 0, 0, 0, 2, 0, 0], 
              [0, 0, 0, 0, 2, 0, 0], 
              [0, 0, 0, 0, 1, 1, 0], 
              [1, 0, 0, 1, 1, 2, 0], 
              [2, 1, 0, 2, 1, 2, 0]]

def board_to_site_format(board):
    current_player = 1
    running_text = ""
    game_length = get_game_length(board)
    indexes_used = []
    indexes_tried = [[] for x in range(42)]
    while True:
        placed = False
        print(running_text)
        if len(running_text) == game_length:
            break
        
        for x in range(7):
            for y in range(6):
                temp = 5 - y
                index = 7 * temp + x
                if index in indexes_tried[len(running_text)]:
                    break
                index_exists = index in indexes_used
                if index_exists:
                    continue
                
                if board[temp][x] == current_player:
                    current_player = 2 if current_player == 1 else 1
                    running_text += str(x + 1)
                    indexes_used.append(index)
                    for i in range(len(running_text), 42):
                        indexes_tried[i] = []
                    indexes_tried[len(running_text) - 1].append(index)
                    placed = True
                else:
                    break
        if placed == False:
            try:
                indexes_used.pop()
            except:
                print(board)
            current_player = 1 if current_player == 2 else 2
            running_text = running_text[:-1]

    return running_text

def possibleMoves(boardState, player) :

    layouts = []
    columns = []
    for row in range(6) :
        for column in range(7) :
            if boardState[row][column] == 0 and (row == 6 - 1 or boardState[row + 1][column] != 0) :
                copiedBoard = []
                for r in boardState:
                    copiedBoard.append(r.copy())
                copiedBoard[row][column] = player
                layouts.append(copiedBoard)
                columns.append(column)

    return layouts, columns

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


if __name__ == "__main__":
    print(test_board)
    print(board_to_site_format(test_board))
    print(site_to_board_format(board_to_site_format(test_board)))