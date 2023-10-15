import logic
import time
import utils 
import model
from threading import Thread
playerNumber = 1
aiNumber = 2

callCount = 0

agent = model.Agent()
agent.load("agentv7-1.2l.pt")

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
    board_length = utils.get_game_length(boardState)
    if board_length % 2 == 0:
        current_player = 1
    else:
        current_player = 2

    evaluation = agent.evaluate(utils.board_to_tensor(boardState)).item()
    if current_player == aiNumber:
        return evaluation
    else:
        return -evaluation


def isTerminalNode(boardState) :
    return len(utils.possibleMoves(boardState, 1)) == 0 or logic.checkWin(boardState, playerNumber) or logic.checkWin(boardState, aiNumber)

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