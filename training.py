import torch
import os
import utils
from model import Agent
import plot

num_epochs = 100
batch_size = 8192

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(device)
agent = Agent(device)
optimizer = torch.optim.Adam(agent.network.parameters(), lr=0.0001)
criterion = torch.nn.MSELoss()

folder = "TrainingData"

training_boards_filename = "boards_train.pt"
training_evaluations_filename = "evaluations_train.pt"
testing_boards_filename = "boards_test.pt"
testing_evaluations_filename = "evaluations_test.pt"

training_boards_path = os.path.join(folder, training_boards_filename)
training_evaluations_path = os.path.join(folder, training_evaluations_filename)
testing_boards_path = os.path.join(folder, testing_boards_filename)
testing_evaluations_path = os.path.join(folder, testing_evaluations_filename)

training_boards = torch.load(training_boards_path).to(device)
training_evaluations = torch.load(training_evaluations_path).to(device)
testing_boards = torch.load(testing_boards_path).to(device)
testing_evaluations = torch.load(testing_evaluations_path).to(device)

#print(training_boards.shape)
#print(training_evaluations.shape)
#print(testing_boards.shape)
#print(testing_evaluations.shape)
print("Training Data Loaded")

for epoch in range(num_epochs):
    epoch_losses = []
    for x in range(0, len(training_boards), batch_size):
        batch = training_boards[x:x + batch_size]
        evaluation = training_evaluations[x:x + batch_size]
        outputs = agent.evaluate(batch).squeeze()
        loss = criterion(outputs, evaluation)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        epoch_losses.append(loss.item())
        #plot.plot(loss.item())
    print("Epoch " + str(epoch) + " Average Loss: " + str(sum(epoch_losses) / len(epoch_losses)))
    print("Epoch contained " + str(len(epoch_losses)) + " batches")
    plot.plot(sum(epoch_losses) / len(epoch_losses))
    agent.save(f"agent{epoch}.pt")

test_losses = []
for x in range(0, len(testing_boards), batch_size):
    batch = testing_boards[x:x + batch_size]
    evaluation = testing_evaluations[x:x + batch_size]
    outputs = agent.evaluate(batch).squeeze()
    loss = criterion(outputs, evaluation)
    test_losses.append(loss.item())

print("Average Test Loss: " + str(sum(test_losses) / len(test_losses)))

agent.save(f"agent.pt")