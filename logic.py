from copy import deepcopy
import math
from time import sleep

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
    if checkWin(player, currentBoardLayout) :
        newGame()
        return
    changeTurn()

def newGame(rows = 6, columns = 7) :
    sleep(5)
    global currentBoardLayout 

    global player
    player = 1
    currentBoardLayout = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0]
    ]

def checkWin(player, boardState) :
    for row in boardState :
        for column in range(0, columns - 3) : #horizontal check
            if row[column] == player and row[column + 1] == player and row[column + 2] == player and row[column + 3] == player :
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
    return False
        

    




