player = 1

currentBoardLayout = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0]
]
def changeTurn () :
    global player

    if player == 1 :
        player = 2
    else :
        player = 1
def AddChecker(position) :
    if len(currentBoardLayout) == position[1] + 1 or currentBoardLayout[position[1] + 1][position[0]] > 0: 
        currentBoardLayout[position[1]][position[0]] = player
        changeTurn()


