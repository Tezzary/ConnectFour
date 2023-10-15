import math
import pygame
import logic
import time
import bot
import platform
import model
import minimaxmodel
import player

possible_players = {
    "Player" : player,
    "NeuralBot" : model,
    "MMBot" : bot,
    "NeuralMMBot" : minimaxmodel,
    "PerfectBot" : 4,
}

wanted_players = ["NeuralMMBot", "MMBot"]

players = []
for i in range(2):
    players.append(possible_players[wanted_players[i]].Player())

scores = [0, 0]

pygame.init()

size = 0

os = platform.system()

if os == "Darwin":
    size = 140
else:
    size = 160
screen = pygame.display.set_mode((size * 10, size * 6))

gameOver = False

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

def RenderScoreboard():
    offset = (size * 8.5, size * 6 / 2)
    font = pygame.font.Font('freesansbold.ttf', int(size / 4))
    text = font.render(f"{wanted_players[0]} - {wanted_players[1]}", True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (offset[0], offset[1])
    screen.blit(text, textRect)
    text = font.render(f"{scores[0]} - {scores[1]}", True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (offset[0], offset[1] + size / 2)
    screen.blit(text, textRect)
while not gameOver :
    '''
    if (logic.player == 2 and not botPlaysFirst or logic.player == 1 and botPlaysFirst) and botEnabled:
        print("askign bot")
        column, evaluation = agent.choose_column(logic.currentBoardLayout)
        for row in range(len(logic.currentBoardLayout)):
            logic.AddChecker((column, row))
        print(f"Bot played column {column + 1} with evaluation {evaluation}")
        t1 = time.time()

        analysis = move = okayMoves = callCount = None
        upperBound = 25
        for depth in range(2, upperBound + 1):
            analysis, move, callCount = bot.getBestMove(logic.currentBoardLayout, depth)
            if analysis >= 1000 or time.time() - t1 > 0.2:
                for row in range(len(logic.currentBoardLayout)):
                    logic.AddChecker((move, row))
                break

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
        t2 = time.time()
        print(f"{text} After searching at a {depth} depth for {round(t2 - t1, 2)} seconds with {callCount} positions searched!")
        '''
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT :
            gameOver = True

    column, depth = players[logic.player - 1].make_move(logic.currentBoardLayout, events, size, 1)

    if depth != -1:
        print(f"Player {logic.player} played column {column + 1} with depth {depth}")

    if column != -1:
        for row in range(len(logic.currentBoardLayout)):
            logic.AddChecker((column, row))

    RenderCheckers(logic.currentBoardLayout)
    RenderScoreboard()
    pygame.display.update()

    if logic.checkWin(logic.currentBoardLayout, 1) or logic.checkWin(logic.currentBoardLayout, 2):
        pos1, pos2, pos3, pos4 = logic.winPositions(logic.currentBoardLayout)
        previous_player = 1 if logic.player == 2 else 2
        scores[previous_player - 1] += 1
        pygame.draw.circle(screen, (255, 255, 255), (size / 2 + pos1[1] * size, size / 2 + pos1[0] * size), size * 0.45)
        pygame.draw.circle(screen, (255, 255, 255), (size / 2 + pos2[1] * size, size / 2 + pos2[0] * size), size * 0.45)
        pygame.draw.circle(screen, (255, 255, 255), (size / 2 + pos3[1] * size, size / 2 + pos3[0] * size), size * 0.45)
        pygame.draw.circle(screen, (255, 255, 255), (size / 2 + pos4[1] * size, size / 2 + pos4[0] * size), size * 0.45)
        pygame.display.update()
        time.sleep(5)
        logic.newGame()

    time.sleep(0.01)

    
pygame.quit()

