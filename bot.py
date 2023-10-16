import logic
import time
import utils 
from threading import Thread
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

def init(board) :
    global playerNumber
    global aiNumber
    game_length = utils.get_game_length(board)
    if game_length % 2 == 0:
        playerNumber = 2
        aiNumber = 1
    else:
        playerNumber = 1
        aiNumber = 2

def analyseBoard(boardState, depth) :
    if logic.checkWin(boardState, aiNumber):
        return 1000 + depth
    if logic.checkWin(boardState, playerNumber):
        return -1000 - depth
    if logic.check_draw(boardState):
        return 0
    playerScore = 0
    aiScore = 0

    for r in range(len(boardState)):
        for c in range(len(boardState[0])):
            if boardState[r][c] == playerNumber:
                playerScore += scoreMatrix[r][c]
            elif boardState[r][c] == aiNumber:
                aiScore+= scoreMatrix[r][c]

    return aiScore - playerScore


def isTerminalNode(boardState) :
    return len(utils.possibleMoves(boardState, 1)) == 0 or logic.checkWin(boardState, playerNumber) or logic.checkWin(boardState, aiNumber) or logic.check_draw(boardState)

def minimax(boardState, depth, alpha, beta, maximizingPlayer) :
    global callCount
    callCount += 1
    if isTerminalNode(boardState) or depth == 0:
        return analyseBoard(boardState, depth), -1

    if maximizingPlayer :
        value = -10000
        bestCol = -1
        layouts, columns = utils.possibleMoves(boardState, aiNumber)
        for num in range(0, len(columns)) :
            boardValue, move = minimax(layouts[num], depth - 1, alpha, beta, False)
            
            if boardValue > value :
                value = boardValue
                bestCol = columns[num]
            if value >= beta:
                break
            if alpha < value:
                alpha = value
            
        return value, bestCol
    else :
        value = 10000
        bestCol = -1
        layouts, columns = utils.possibleMoves(boardState, playerNumber)
        for num in range(0, len(columns)) :
            boardValue, move = minimax(layouts[num], depth - 1, alpha, beta, True)
            
            if boardValue < value :
                value = boardValue
                bestCol = columns[num]
            if value <= alpha:
                break
            if beta > value:
                beta = value
            
        return value, bestCol

def getBestMove(boardState, depth):
    global callCount
    callCount = 0
    t = time.time()
    value, column = minimax(boardState, depth, -10000, 10000, True)
    #print(f"Completed {depth} depth in {round(time.time() - t, 6)} seconds at {callCount} positions searched!")
    return value, column, callCount

class Player():
    def __init__(self):
        self.thread = None
        self.results = None

    def _calculate_move(self, board, time_limit):
        init(board)
        move = None
        max_depth = 25
        t1 = time.time()
        for depth in range(2, max_depth + 1):
            analysis, move = minimax(board, depth, -10000, 10000, True)
            if analysis >= 1000 or time.time() - t1 > time_limit:
                break
        #if depth == max_depth or analysis >= 1000:
            #time.sleep(1.5)
        self.results = move, depth
    def make_move(self, board, events, size, time_limit):
        if self.thread is None:
            self.thread = Thread(target=self._calculate_move, args=(board, time_limit))
            self.thread.start()
            return -1, -1
        if self.results is None:
            return -1, -1
        else:
            move, depth = self.results
            self.thread.join()
            self.thread = None
            self.results = None
            return move, depth