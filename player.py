import pygame
import math
import logic

def Clicked(size) :
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
    return closest[1]

class Player():
    def make_move(self, board, events, size, time_limit):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN :
                return Clicked(size), -1
        return -1, -1