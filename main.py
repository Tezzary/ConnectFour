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
botPlaysFirst = True

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
        analysis = move = okayMoves = callCount = None
        upperBound = 25
        for depth in range(2, upperBound + 1):
            analysis, move, okayMoves, callCount = bot.getBestMove(logic.currentBoardLayout, depth)
            #print(f"{forced} {depth}")
            if okayMoves < 2 or analysis >= 1000 or time.time() - t1 > 3:
                for row in range(len(logic.currentBoardLayout)):
                    logic.AddChecker((move, row))
                break
            #print("placed")

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
        if okayMoves < 2:
            text += " My move was forced!"
        text += f"{okayMoves}"
        t2 = time.time()
        print(f"{text} After searching at a {depth} depth for {round(t2 - t1, 2)} seconds with {callCount} positions searched!")
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

