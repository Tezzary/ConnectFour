import math
import pygame
import logic
import time
import bot
import platform
import model
import minimaxmodel
import player
import os

simulation_mode = True
gui_enabled = True

start_move = 0

possible_players = {
    "Player" : player,
    "NeuralBot" : model,
    "MMBot" : bot,
    "NeuralMMBot" : minimaxmodel,
    "PerfectBot" : 4,
}

wanted_players = ["NeuralMMBot", "MMBot"]

players = []
scores = [0, 0, 0]

start_time = time.time()

if simulation_mode:
    start_move = 8
    simulation_game_count = 500
    simulation_participants = ["NeuralBot", "NeuralMMBot", "MMBot"]
    matches = []
    for i in range(len(simulation_participants)):
        for j in range(i + 1, len(simulation_participants)):
            matches.append([simulation_participants[i], simulation_participants[j]])

    matches_copy = matches.copy()
    for i in range(len(matches_copy)):
        matches_copy[i] = matches_copy[i][::-1]
    matches = matches + matches_copy

    wanted_players = matches[0]
    matches = matches[1:]

for i in range(2):
    players.append(possible_players[wanted_players[i]].Player())



size = 0

operating_system = platform.system()

if operating_system == "Darwin":
    size = 140
else:
    size = 160
if gui_enabled:
    pygame.init()
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
    font = pygame.font.Font('freesansbold.ttf', int(size / 5))
    text = font.render(f"{wanted_players[0]} - {wanted_players[1]}", True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (offset[0], offset[1] - size / 4)
    screen.blit(text, textRect)
    text = font.render(f"{scores[0]} - {scores[1]} - {scores[2]}", True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (offset[0], offset[1] + size / 4)
    screen.blit(text, textRect)

def restart_simulation():
    global scores, players, wanted_players, matches

    if len(matches) == 0:
        print("Simulation finished")
        print(f"Simulation took {round(time.time() - start_time, 2)} seconds")
        exit()
    if not os.path.exists("SimulationResults"):
        os.makedirs("SimulationResults")
    path = os.path.join("SimulationResults", f"results-{start_time}.txt")
    with open(path, "a") as results:
        results.write(f"{wanted_players[0]} - {wanted_players[1]}\n")
        results.write(f"{scores[0]} - {scores[1]} - {scores[2]}\n")
        results.write(f"Simulation took {round(time.time() - start_time, 2)} seconds\n")

    
    
    wanted_players = matches[0]
    matches = matches[1:]
    scores = [0, 0, 0]
    players = []
    for i in range(2):
        players.append(possible_players[wanted_players[i]].Player())

games_played = 0
while not gameOver :
    if gui_enabled:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT :
                gameOver = True
    else:
        events = []
    column, depth = players[logic.player - 1].make_move(logic.currentBoardLayout, events, size, 0.2)
    #print(logic.player)
    #print(column)
    #if depth != -1:
        #print(f"Player {logic.player} played column {column + 1} with depth {depth}")

    if column != -1:
        for row in range(len(logic.currentBoardLayout)):
            logic.AddChecker((column, row))
    if gui_enabled:
        RenderCheckers(logic.currentBoardLayout)
        RenderScoreboard()
        pygame.display.update()

    result = [logic.checkWin(logic.currentBoardLayout, 1), logic.check_draw(logic.currentBoardLayout), logic.checkWin(logic.currentBoardLayout, 2)]
    if any(result):
        games_played += 1
        scores[result.index(True)] += 1
        if gui_enabled and (result[0] or result[2]):
            pos1, pos2, pos3, pos4 = logic.winPositions(logic.currentBoardLayout)
            pygame.draw.circle(screen, (255, 255, 255), (size / 2 + pos1[1] * size, size / 2 + pos1[0] * size), size * 0.45)
            pygame.draw.circle(screen, (255, 255, 255), (size / 2 + pos2[1] * size, size / 2 + pos2[0] * size), size * 0.45)
            pygame.draw.circle(screen, (255, 255, 255), (size / 2 + pos3[1] * size, size / 2 + pos3[0] * size), size * 0.45)
            pygame.draw.circle(screen, (255, 255, 255), (size / 2 + pos4[1] * size, size / 2 + pos4[0] * size), size * 0.45)
            pygame.display.update()
            if not simulation_mode:
                time.sleep(5)
        if(simulation_mode and sum(scores) == simulation_game_count):
            restart_simulation()
        logic.newGame(start_move)
        print(f"Game {games_played} finished")
        print(f"Starting new game between {wanted_players[0]} and {wanted_players[1]}")

    time.sleep(0.01)

if gui_enabled:
    pygame.quit()

