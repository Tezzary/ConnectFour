import math
import logic
from copy import deepcopy


def min() :
    d
def max() :
    d
def analyseBoard(boardState,) :
    if logic.checkWin(1, boardState):
        return math.inf
    elif logic.checkWin(2, boardState):
        return -math.inf



def possibleMoves(boardState, player) :

    layouts = []
    moves = []
    for row in range(0, logic.rows) :
        for column in range(0, logic.columns) :
            if boardState[row][column] != 0 and row == logic.rows - 1 or boardState[row + 1][column] != 0 :
                layoutsCount = len(layouts)
                layouts[layoutsCount] = deepcopy(boardState)
                moves[len(moves)] = column

    return layouts, moves

def minimax(boardState, depth, maximizingPlayer) :
    children, moves = possibleMoves(boardState, maximizingPlayer)
    if depth == 0 or children == None:
        return analyseBoard(boardState)
    
    

    if maximizingPlayer:
        value = -math.inf
        bestPosition = -1
        bestMove = -1
        for i, child in enumerate(children) :
            childValue, position = minimax(child, depth - 1, False)
            if childValue > value :
                value = childValue
        return value, bestPosition

    else :
        value = math.inf
        bestPosition = -1
        bestMove = -1
        for i, child in enumerate(children):
            childValue, move = minimax(child, depth - 1, True)
            if childValue < value :
                value = childValue
                bestMove = moves[i]
        return value, bestMove
    
def calculateBestMove(boardState, searchDepth) :
    minimax