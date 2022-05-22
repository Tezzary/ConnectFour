import math
import pygame
import logic
import time
pygame.init()

size = 160
screen = pygame.display.set_mode((size * 7, size * 6))

gameOver = False

def RenderCheckers(checkers) :
    screen.fill((0,0,0))
    for y, row in enumerate(checkers) :
        for x, checker in enumerate(row) :
            color = (0, 0, 255)
           # print(checker)
            if checker == 0 :
                continue
            if checker == 2 :
                color = (255, 0, 0)
                #print(f"{x} {y} {row} {checker} {time.process_time()}", flush=True)

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

    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            gameOver = True
        elif event.type == pygame.MOUSEBUTTONDOWN :
            Clicked()
    
    RenderCheckers(logic.currentBoardLayout)

  #  print(pygame.mouse.get_pos())

    pygame.display.update()
    time.sleep(0.001)

    
pygame.quit()

