import random
import utils
player = 1

currentBoardLayout = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0]
]

rows = len(currentBoardLayout)
columns = len(currentBoardLayout[0])

def changeTurn () :
    global player

    if player == 1 :
        player = 2
    else :
        player = 1
def AddChecker(position) :

    if currentBoardLayout[position[1]][position[0]] > 0 :
        return

    if not (len(currentBoardLayout) == position[1] + 1 or currentBoardLayout[position[1] + 1][position[0]] > 0): 
        return

    currentBoardLayout[position[1]][position[0]] = player
    
    changeTurn()

def newGame(game_length=0, rows = 6, columns = 7) :
    global currentBoardLayout 

    global player
    player = 1
    currentBoardLayout = utils.site_to_board_format(generate_random_position(game_length))

def generate_random_position(game_length):
    board = ""
    col_count = [0 for x in range(7)]
    while True:
        if len(board) == game_length:
            matrix_board = utils.site_to_board_format(board)
            if checkWin(matrix_board, 1) or checkWin(matrix_board, 2):
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

def checkWin(boardState, player) :
    for row in range(0, rows) :
            for column in range(0, columns - 3) : #horizontal check
                if boardState[row][column] == player and boardState[row][column + 1] == player and boardState[row][column + 2] == player and boardState[row][column + 3] == player :
                    return True
    
    for row in range(0, rows - 3) : #vertical check
        for column in range(0, columns) :
            if boardState[row][column] == player and boardState[row + 1][column] == player and boardState[row + 2][column] == player and boardState[row + 3][column] == player :
                return True

    for row in range(0, rows - 3) : #diagonal left check
        for column in range(0, columns - 3) :
            if boardState[row][column] == player and boardState[row + 1][column + 1] == player and boardState[row + 2][column + 2] == player and boardState[row + 3][column + 3] == player :
                return True

    for row in range(0, rows - 3) : #diagonal right check
        for column in range(3, columns) :
            if boardState[row][column] == player and boardState[row + 1][column - 1] == player and boardState[row + 2][column - 2] == player and boardState[row + 3][column - 3] == player :
                return True

def winPositions(boardState) :
    for player in range(1,3):
        for row in range(0, rows) :
            for column in range(0, columns - 3) : #horizontal check
                if boardState[row][column] == player and boardState[row][column + 1] == player and boardState[row][column + 2] == player and boardState[row][column + 3] == player :
                    return (row, column), (row, column + 1), (row, column + 2), (row, column + 3)
    
        for row in range(0, rows - 3) : #vertical check
            for column in range(0, columns) :
                if boardState[row][column] == player and boardState[row + 1][column] == player and boardState[row + 2][column] == player and boardState[row + 3][column] == player :
                    return (row, column), (row + 1, column), (row + 2, column), (row + 3, column)
    
        for row in range(0, rows - 3) : #diagonal left check
            for column in range(0, columns - 3) :
                if boardState[row][column] == player and boardState[row + 1][column + 1] == player and boardState[row + 2][column + 2] == player and boardState[row + 3][column + 3] == player :
                    return (row, column), (row + 1, column + 1), (row + 2, column + 2), (row + 3, column + 3), 
    
        for row in range(0, rows - 3) : #diagonal right check
            for column in range(3, columns) :
                if boardState[row][column] == player and boardState[row + 1][column - 1] == player and boardState[row + 2][column - 2] == player and boardState[row + 3][column - 3] == player :
                    return (row, column), (row + 1, column - 1), (row + 2, column - 2), (row + 3, column - 3), 
    return 0, 0, 0, 0

def check_draw(boardState):
    for row in range(0, rows):
        for column in range(0, columns):
            if boardState[row][column] == 0:
                return False
    return True
