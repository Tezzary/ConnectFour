import math
import pygame
import logic
import time
import bot
import platform

pygame.init()

size = 0

os = platform.system()

if os == "Darwin":
    size = 140
else:
    size = 160
screen = pygame.display.set_mode((size * 7, size * 6))

gameOver = False

botEnabled = True
botPlaysFirst = False

if botEnabled:
    bot.init(botPlaysFirst)

def RenderCheckers(checkers) :
    screen.fill((0, 0, 255))
    for y, row in enumerate(checkers) :
        for x, checker in enumerate(row) :

            pygame.draw.circle(screen, (0, 0, 0), (size / 2 + x * size, size / 2 + y * size), size * 0.45)

            color = (255, 0, 0)
           # print(checker)
            if checker == 0 :
                continue
            if checker == 2 :
                color = (255, 255, 0)

            pygame.draw.circle(screen, color, (size / 2 + x * size, size / 2 + y * size), size * 0.45)

def Clicked() :
    closest = [math.inf, 0, 0]
    mousePos = pygame.mouse.get_pos()
    for x in range(7) :
        deltaX = size / 2 + x * size - mousePos[0]
        for y in range(6) :
            deltaY = size / 2 + y * size - mousePos[1]

            dist = math.sqrt(deltaX ** 2 + deltaY ** 2)

            if dist < closest[0] :
                closest[0] = dist
                closest[1] = x
                closest[2] = y
    logic.AddChecker((closest[1], closest[2]))

while not gameOver :

    if (logic.player == 2 and not botPlaysFirst or logic.player == 1 and botPlaysFirst) and botEnabled:
        t1 = time.time()
        depth = 9
        print(len(bot.possibleMoves(logic.currentBoardLayout, 2)[0]))
        if len(bot.possibleMoves(logic.currentBoardLayout, 2)[0]) == 6:
            depth = 11
        elif len(bot.possibleMoves(logic.currentBoardLayout, 2)[0]) == 5:
            depth = 13
        elif len(bot.possibleMoves(logic.currentBoardLayout, 2)[0]) == 4:
            depth = 15
        elif len(bot.possibleMoves(logic.currentBoardLayout, 2)[0]) == 3:
            depth = 18
        elif len(bot.possibleMoves(logic.currentBoardLayout, 2)[0]) == 2 or len(bot.possibleMoves(logic.currentBoardLayout, 2)[0]) == 1:
            depth = 25
        analysis, move = bot.getBestMove(logic.currentBoardLayout, depth)

        if analysis == 10000:
            text = "This should be a draw!"
        elif analysis >= 1000:
            text = "I have a guaranteed win!"
        elif analysis <= -1000:
            text = "If you play perfectly you have a guaranteed win!"
        elif analysis > 0:
            text = f"I think I'm winning by {analysis}!"
        elif analysis < 0:
            text = f"I think I'm losing by {analysis * -1}!"
        else:
            text = f"I think we are equal!"
        
        for row in range(len(logic.currentBoardLayout)):
            logic.AddChecker((move, row))
        t2 = time.time()
        print(f"{text} After searching at a {depth} depth for {round(t2 - t1, 2)} seconds")
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            gameOver = True
        elif event.type == pygame.MOUSEBUTTONDOWN :
            Clicked()
       # elif event.type == pygame.KEYDOWN :
        #    logic.newGame()
    
    RenderCheckers(logic.currentBoardLayout)

    pygame.display.update()

    if logic.checkWin(logic.currentBoardLayout, 1) or logic.checkWin(logic.currentBoardLayout, 2):
        pos1, pos2, pos3, pos4 = logic.winPositions(logic.currentBoardLayout)
        pygame.draw.circle(screen, (255, 255, 255), (size / 2 + pos1[1] * size, size / 2 + pos1[0] * size), size * 0.45)
        pygame.draw.circle(screen, (255, 255, 255), (size / 2 + pos2[1] * size, size / 2 + pos2[0] * size), size * 0.45)
        pygame.draw.circle(screen, (255, 255, 255), (size / 2 + pos3[1] * size, size / 2 + pos3[0] * size), size * 0.45)
        pygame.draw.circle(screen, (255, 255, 255), (size / 2 + pos4[1] * size, size / 2 + pos4[0] * size), size * 0.45)
        pygame.display.update()
        time.sleep(5)
        logic.newGame()

    time.sleep(0.1)

    
pygame.quit()

