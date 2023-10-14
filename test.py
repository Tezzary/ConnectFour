import subprocess
import os
import time
import utils

board = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 2, 0, 0, 0, 0, 0],
    [1, 2, 1, 2, 1, 2, 1],
    [2, 1, 2, 1, 2, 1, 2],
    [1, 2, 1, 2, 1, 2, 1],
]

board_string = utils.board_to_site_format(board)

test_string = "73421661771566276172547361446613664475"

print(utils.site_to_board_format(test_string))

[[1, 0, 0, 2, 0, 1, 1], 
 [2, 0, 0, 1, 0, 1, 1], 
 [2, 0, 0, 2, 0, 2, 2], 
 [1, 2, 2, 1, 1, 1, 2], 
 [2, 1, 2, 2, 1, 1, 1], 
 [1, 2, 2, 1, 2, 2, 1]]