import os
import subprocess
import utils
import multiprocessing

def generate_data(index, num_samples):
    directory = os.path.join("MoveGenerator", "connect4", "c4solver.exe")
    process = subprocess.Popen([directory, "-", "w"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

    def evaluate_board(board):
        #board_string = utils.board_to_site_format(board)
        board_string = board
        process.stdin.write(board_string + "\n")
        process.stdin.flush()

        stdout = process.stdout.readline()

        evaluation = int(stdout.split(" ")[1])

        return evaluation

    folder = "TrainingData"
    if not os.path.exists(folder):
        os.makedirs(folder)
    path = os.path.join(folder, f"data{index}.txt")
    if os.path.exists(path):
        os.remove(path)

    running_text = ""
    for x in range(num_samples):
        board = utils.generate_random_position()
        evaluation = evaluate_board(board)
        
        running_text += board + " " + str(evaluation) + "\n"
        if (x + 1) % 1000 == 0 or x == num_samples - 1:
            with open(path, "a") as data:
                data.write(running_text)
            running_text = ""

    process.stdin.close()
    process.stdout.close()
    process.terminate()

if __name__ == "__main__":
    num_samples = 100000
    num_processes = 4
    num_samples_per_process = num_samples // num_processes

    processes = []
    for x in range(num_processes):
        process = multiprocessing.Process(target=generate_data, args=(x, num_samples_per_process))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()