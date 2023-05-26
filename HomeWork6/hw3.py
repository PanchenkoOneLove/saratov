"""
Given a Tic-Tac-Toe 3x3 board (can be unfinished).
Write a function that checks if the are some winners.
If there is "x" winner, function should return "x wins!"
If there is "o" winner, function should return "o wins!"
If there is a draw, function should return "draw!"
If board is unfinished, function should return "unfinished!"

Example:
    [[-, -, o],
     [-, x, o],
     [x, o, x]]
    Return value should be "unfinished"

    [[-, -, o],
     [-, o, o],
     [x, x, x]]

     Return value should be "x wins!"

"""
from typing import List
import numpy as np


def tic_tac_toe_checker(board):
    board_np = np.array(board)

    # Checking winning combinations by rows, columns, and diagonals
    for player in ['x', 'o']:
        if any(all(row == player) for row in board_np) or \
           any(all(col == player) for col in board_np.T) or \
           np.all(board_np.diagonal() == player) or \
           np.all(np.fliplr(board_np).diagonal() == player):
            return f"{player} wins!"

    # Checking for empty cells
    if '-' in board_np:
        return "unfinished"

    # If there are no empty cells and no combination wins, then it is a draw
    return "draw!"


board1 = [['-', '-', 'o'],
          ['-', 'x', 'o'],
          ['x', 'o', 'x']]
print(tic_tac_toe_checker(board1))  # unfinished

board2 = [['-', '-', 'o'],
          ['-', 'o', 'o'],
          ['x', 'x', 'x']]
print(tic_tac_toe_checker(board2))  # x wins!