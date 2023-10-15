import torch
import utils
import bot

class Network(torch.nn.Module):
    def __init__(self):
        super(Network, self).__init__()
        self.fc1 = torch.nn.Linear(42, 256)
        self.fc2 = torch.nn.Linear(256, 256)
        self.fc3 = torch.nn.Linear(256, 256)
        self.fc4 = torch.nn.Linear(256, 256)
        self.fc5 = torch.nn.Linear(256, 256)
        self.fc6 = torch.nn.Linear(256, 128)
        self.fc7 = torch.nn.Linear(128, 64)
        self.fc8 = torch.nn.Linear(64, 1)

    def forward(self, x):
        x = torch.nn.functional.relu(self.fc1(x))
        x = torch.nn.functional.relu(self.fc2(x))
        x = torch.nn.functional.relu(self.fc3(x))
        x = torch.nn.functional.relu(self.fc4(x))
        x = torch.nn.functional.relu(self.fc5(x))
        x = torch.nn.functional.relu(self.fc6(x))
        x = torch.nn.functional.relu(self.fc7(x))
        return self.fc8(x)

    

class Agent():
    def __init__(self, device="cpu"):
        self.network = Network().to(device)
    def save(self, path):
        torch.save(self.network.state_dict(), path)

    def load(self, path):
        self.network.load_state_dict(torch.load(path))
    
    def choose_column(self, board):
        game_length = utils.get_game_length(board)
        if game_length % 2 == 0:
            current_player = 1
        else:
            current_player = 2
        possible_boards, possible_columns = utils.possibleMoves(board, current_player)

        best_column = -1
        best_evaluation = -1000000
        for i in range(len(possible_boards)):
            possible_board = utils.board_to_tensor(possible_boards[i])
            possible_column = possible_columns[i]

            #negative as evaluation is for the other player after move completed
            evaluation = -self.network(possible_board).item()
            if evaluation > best_evaluation:
                best_evaluation = evaluation
                best_column = possible_column

        return best_column, best_evaluation

    def evaluate(self, board):
        return self.network(board)
    
class Player():
    def __init__(self):
        self.agent = Agent()
        self.agent.load("agentv8-1.1.pt")
    def make_move(self, board, events, size, time_limit):
        return self.agent.choose_column(board)[0], -1
            

