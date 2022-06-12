import logic
from copy import deepcopy

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

def init(playerNum, aiNum) :
    playerNumber = playerNum
    aiNumber = aiNum

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
    for row in range(0, logic.rows) :
        for column in range(0, logic.columns) :
            if boardState[row][column] == 0 and (row == logic.rows - 1 or boardState[row + 1][column] != 0) :
                layoutsCount = len(layouts)
                copiedBoard = deepcopy(boardState)
                copiedBoard[row][column] = player
                layouts.append(copiedBoard)
                columns.append(column)

    return layouts, columns

def isTerminalNode(boardState) :
    return logic.checkWin(boardState, 1) or logic.checkWin(boardState, 2) or len(possibleMoves(boardState, 1)) == 0

def minimax(boardState, depth, maximizingPlayer) :
    global callCount
    callCount += 1
    if isTerminalNode(boardState) or depth == 0:
        return analyseBoard(boardState), -1

    if maximizingPlayer :
        value = -10
        bestCol = -1
        layouts, columns = possibleMoves(boardState, aiNumber)
        for num in range(0, len(columns)) :
            boardValue, move = minimax(layouts[num], depth - 1, False)
            if boardValue > value :
                value = boardValue
                bestCol = columns[num]
        return value, bestCol
    else :
        value = 10
        bestCol = -1
        layouts, columns = possibleMoves(boardState, playerNumber)
        for num in range(0, len(columns)) :
            boardValue, move = minimax(layouts[num], depth - 1, True)
            if boardValue < value :
                value = boardValue
                bestCol = columns[num]
        return value, bestCol

def getBestMove(boardState, depth):
    global callCount
    callCount = 0
    value, column = minimax(boardState, depth, True)
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