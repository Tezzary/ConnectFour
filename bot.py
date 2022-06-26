import logic
from copy import deepcopy, copy
playerNumber = 1
aiNumber = 2

callCount = 0

scoreMatrix = [
    [1, 2, 3, 4, 3, 2, 1],
    [1, 2, 3.5, 4.5, 3.5, 2, 1],
    [1, 3, 4, 5, 4, 3, 1],
    [1, 3, 4, 5, 4, 3, 1],
    [1, 2, 3.5, 4.5, 3.5, 2, 1],
    [1, 2, 3, 4, 3, 2, 1]
    ]

def init(botplaysFirst) :
    global playerNumber
    global aiNumber
    if botplaysFirst:
        playerNumber = 2
        aiNumber = 1
    else:
        playerNumber = 1
        aiNumber = 2

def analyseBoard(boardState) :
    if logic.checkWin(boardState, aiNumber):
        return 1000
    if logic.checkWin(boardState, playerNumber):
        return -1000
    playerScore = 0
    aiScore = 0
    for r in range(len(boardState)):
        for c in range(len(boardState[0])):
            if boardState[r][c] == playerNumber:
                playerScore += scoreMatrix[r][c]
            elif boardState[r][c] == aiNumber:
                aiScore+= scoreMatrix[r][c]

    return aiScore - playerScore


def possibleMoves(boardState, player) :

    layouts = []
    columns = []
    for row in range(6) :
        for column in range(7) :
            if boardState[row][column] == 0 and (row == logic.rows - 1 or boardState[row + 1][column] != 0) :
                copiedBoard = []
                for r in boardState:
                    copiedBoard.append(r.copy())
                copiedBoard[row][column] = player
                layouts.append(copiedBoard)
                columns.append(column)

    return layouts, columns

def isTerminalNode(boardState) :
    return len(possibleMoves(boardState, 1)) == 0

def minimax(boardState, depth, alpha, beta, maximizingPlayer) :
    global callCount
    callCount += 1
    if isTerminalNode(boardState) or depth == 0:
        return analyseBoard(boardState), -1

    if maximizingPlayer :
        value = -10000
        bestCol = -1
        layouts, columns = possibleMoves(boardState, aiNumber)
        for num in range(0, len(columns)) :
            if logic.checkWin(layouts[num], playerNumber):
                return -1000, -1
        for num in range(0, len(columns)) :
            boardValue, move = minimax(layouts[num], depth - 1, alpha, beta, False)
            
            if boardValue > value :
                value = boardValue
                bestCol = columns[num]
            if value >= beta or value >= 10000:
                break
            if alpha < value:
                alpha = value
        return value, bestCol
    else :
        value = 10000
        bestCol = -1
        layouts, columns = possibleMoves(boardState, playerNumber)
        for num in range(0, len(columns)) :
            if logic.checkWin(layouts[num], aiNumber):
                return 1000, -1
        for num in range(0, len(columns)) :
            boardValue, move = minimax(layouts[num], depth - 1, alpha, beta, True)
            if boardValue < value :
                value = boardValue
                bestCol = columns[num]
            if value <= alpha or value <= -10000:
                break
            if beta > value:
                beta = value
        return value, bestCol

def getBestMove(boardState, timeOut):
    global callCount
    callCount = 0
    value, column = minimax(boardState, depth, -10000, 10000, True)
    print(callCount)
    return value, column

if __name__ == "__main__":
    print(possibleMoves([
    [0, 2, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0],
    [0, 2, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0],
    [0, 1, 2, 2, 2, 1, 0],
    [1, 2, 1, 1, 1, 2, 0]
    ], 2)[0])