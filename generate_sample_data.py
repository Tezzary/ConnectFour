import os
import subprocess
import utils
import multiprocessing
import torch

folder = "TrainingData"

def evaluate_board(process, board):
    #board_string = utils.board_to_site_format(board)
    board_string = board
    process.stdin.write(board_string + "\n")
    process.stdin.flush()

    stdout = process.stdout.readline()

    evaluation = int(stdout.split(" ")[1])

    return evaluation

def load_data(data):
    data = data.split("\n")
    print(data[-1])
    data = data[:-1]
    boards = []
    evaluations = []
    for d in data:
        board, evaluation = d.split(" ")
        #print(evaluation)
        board = utils.board_to_tensor(board)
        evaluation = torch.tensor([int(evaluation)], dtype=torch.float)
        boards.append(board)
        evaluations.append(evaluation)
    return boards, evaluations
def generate_data(index, num_samples):
    directory = os.path.join("MoveGenerator", "connect4", "c4solver.exe")
    process = subprocess.Popen([directory, "-", "w"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    
    path = os.path.join(folder, f"temp{index}.txt")
    if os.path.exists(path):
        os.remove(path)

    running_text = ""
    for x in range(num_samples):
        board = utils.generate_random_position()
        evaluation = evaluate_board(process, board)
        
        running_text += board + " " + str(evaluation) + "\n"
        if (x + 1) % 1000 == 0 or x == num_samples - 1:
            with open(path, "a") as data:
                data.write(running_text)
            running_text = ""

    process.stdin.close()
    process.stdout.close()
    process.terminate()

if __name__ == "__main__":
    num_samples = 32000000 # 3.2 million | 3 million training, 200k testing
    num_processes = 16
    num_processes_allocated_testing = 1
    num_samples_per_process = num_samples // num_processes

    processes = []

    if not os.path.exists(folder):
        os.makedirs(folder)
    

    for x in range(num_processes):
        process = multiprocessing.Process(target=generate_data, args=(x, num_samples_per_process))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

    
    path = os.path.join("TrainingData", "data.txt")
    if os.path.exists(path):
        os.remove(path)

    boards_training = None
    evaluations_training = None
    
    boards_testing = None
    evaluations_testing = None
    running_training_text = ""
    running_testing_text = ""

    for dir in os.listdir("TrainingData"):
        if "temp" in dir:
            with open(os.path.join("TrainingData", dir), "r") as temp:
                num = int(dir[4:-4])
                if num < num_processes_allocated_testing:
                    running_testing_text += temp.read()
                else:
                    running_training_text += temp.read()
            os.remove(os.path.join("TrainingData", dir))
    

    boards, evaluations = load_data(running_training_text)

    boards_training = torch.stack(boards)
    evaluations_training = torch.cat(evaluations)
    
    torch.save(boards_training, os.path.join("TrainingData", "boards_train.pt"))
    torch.save(evaluations_training, os.path.join("TrainingData", "evaluations_train.pt"))

    boards, evaluations = load_data(running_testing_text)

    boards_testing = torch.stack(boards)
    evaluations_testing = torch.cat(evaluations)

    torch.save(boards_testing, os.path.join("TrainingData", "boards_test.pt"))
    torch.save(evaluations_testing, os.path.join("TrainingData", "evaluations_test.pt"))