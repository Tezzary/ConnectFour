import torch
import os
import utils

class Network(torch.nn.Module):
    def __init__(self):
        super(Network, self).__init__()
        self.fc1 = torch.nn.Linear(42, 32)
        self.fc2 = torch.nn.Linear(32, 32)
        self.fc3 = torch.nn.Linear(32, 32)
        self.fc4 = torch.nn.Linear(32, 1)

    def forward(self, x):
        x = torch.nn.functional.relu(self.fc1(x))
        x = torch.nn.functional.relu(self.fc2(x))
        x = torch.nn.functional.relu(self.fc3(x))
        return self.fc4(x)
    
def board_to_tensor(board):
    if type(board) == str:
        board = utils.site_to_board_format(board)

    move_count = utils.get_game_length(board)
    if move_count % 2 == 0:
        current_player = 1
    else:
        current_player = 2
    tensor = torch.zeros(42, dtype=torch.float)
    for y in range(6):
        for x in range(7):
            index = 7 * y + x
            if board[y][x] == current_player:
                tensor[index] = 1
            elif board[y][x] == 0:
                tensor[index] = 0
            else:
                tensor[index] = -1
    return tensor

def load_data(path):
    boards = []
    evaluations = []
    with open(path, "r") as data:
        data = data.readlines()
        for d in data:
            board, evaluation = d.split(" ")
            board = board_to_tensor(board)
            evaluation = torch.tensor(int(evaluation), dtype=torch.float)
            boards.append(board)
            evaluations.append(evaluation)
    return boards, evaluations
num_epochs = 10
batch_size = 128

network = Network()
optimizer = torch.optim.Adam(network.parameters(), lr=0.001)
criterion = torch.nn.MSELoss()

folder = "TrainingData"
training_filename = "data.txt"
testing_filename = "testdata.txt"

training_data_path = os.path.join(folder, training_filename)
testing_data_path = os.path.join(folder, testing_filename)

training_boards, training_evaluations = load_data(training_data_path)
testing_boards, testing_evaluations = load_data(testing_data_path)

print(testing_boards[0])
print(testing_evaluations[0])
print("Training Data Loaded")

for epoch in range(num_epochs):
    for x in range(0, len(training_boards), batch_size):
        batch = training_boards[x:x + batch_size]
        batch = torch.stack(batch)
        evaluation = training_evaluations[x:x + batch_size]
        evaluation = torch.stack(evaluation)
        outputs = network(batch).squeeze()
        loss = criterion(outputs, evaluation)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    print("Epoch: " + str(epoch) + " Loss: " + str(loss.item()))

for x in range(0, len(testing_boards), batch_size):
    batch = testing_boards[x:x + batch_size]
    batch = torch.stack(batch)
    evaluation = testing_evaluations[x:x + batch_size]
    evaluation = torch.stack(evaluation)
    outputs = network(batch).squeeze()
    loss = criterion(outputs, evaluation)
    print("Test Loss: " + str(loss.item()))

torch.save(network.state_dict(), "agent.pt")
