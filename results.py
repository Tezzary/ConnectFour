import os
import prettytable
import time

players = []

def get_player_index(player_name):
    for i in range(len(players)):
        if players[i]["name"] == player_name:
            return i
    return -1

def sort_players():
    players.sort(key=lambda x: x["scoreTotal"][0] - x["scoreTotal"][2], reverse=True)
def save_results(match_results, start_time, time_limit):
    global players
    players = []
    games_played = 0
    for i in range(len(match_results)):
        players_in_match = match_results[i]["players"]
        for player in players_in_match:
            if get_player_index(player) == -1:
                players.append({
                    "name" : player,
                    "scoreTotal" : [0, 0, 0],
                })
        scores = match_results[i]["scores"]
        player_one = get_player_index(players_in_match[0])
        player_two = get_player_index(players_in_match[1])

        players[player_one]["scoreTotal"][0] += scores[0]
        players[player_one]["scoreTotal"][1] += scores[1]
        players[player_one]["scoreTotal"][2] += scores[2]

        players[player_two]["scoreTotal"][0] += scores[2]
        players[player_two]["scoreTotal"][1] += scores[1]
        players[player_two]["scoreTotal"][2] += scores[0]

        games_played += scores[0] + scores[1] + scores[2]

    sort_players()

    table = prettytable.PrettyTable()
    table.field_names = ["Player", "Wins", "Draws", "Losses", "Score"]
    for player in players:
        table.add_row([player["name"], player["scoreTotal"][0], player["scoreTotal"][1], player["scoreTotal"][2], player["scoreTotal"][0] - player["scoreTotal"][2]])
    print(table)

    if not os.path.exists("SimulationResults"):
        os.makedirs("SimulationResults")
    path = os.path.join("SimulationResults", f"results-{time.time()}.txt")
    with open(path, "a") as results_file:
        results_file.write(f"Statistics:\n\n")
        results_file.write(f"Simulation took {round(time.time() - start_time, 2)}s\n")
        results_file.write(f"Time limit: {time_limit}s\n")
        results_file.write(f"Games played: {games_played}\n\n")
        results_file.write("Player Results:\n\n")
        results_file.write(str(table) + "\n\n")
        results_file.write("Match Results:\n\n")
        for match in match_results:
            wanted_players = match["players"]
            scores = match["scores"]
            results_file.write(f"{wanted_players[0]} - {wanted_players[1]}\n")
            results_file.write(f"{scores[0]} - {scores[1]} - {scores[2]}\n\n")

        
        
        

if __name__ == "__main__":
    sample_data = [
        {
            "players" : ["MMBot", "NeuralMMBot"],
            "scores" : [32, 4, 14],
        },
        {
            "players" : ["NeuralBot", "MMBot"],
            "scores" : [12, 4, 14],
        }
    ]
    save_results(sample_data, time.time(), 0.01)