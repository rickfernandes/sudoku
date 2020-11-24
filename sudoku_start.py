# -*- coding: utf-8 -*-
"""
This module is a sudoku generator that will load a `.sudoku` file with sudoku boards. And runs `MainWindow` from tk_sudoku_game.

__External modules__: `random`, `os`, `argparse`

`Compatible with Python3.7 or higher`\n

_Repository:_ https://github.com/rickfernandes/sudoku_solver
"""

from tk_sudoku_game import MainWindow
from os import listdir
from random import randint
from argparse import ArgumentParser

FOLDER = 'boards/'
"""Folder containing the sudoku boards as `.sudoku` files."""

def ParseArguments():
	"""Function to parse the arguments passed by the user. Argument `--board` is not required and, if not passed, uses `random` as default.

	Args:
		__None__

	Dependencies:
		`ArgumentParser()` (function): from `argparse` module.

	Returns:
		`board_name` (str): returns a string that represents the board (i.e. file) name.
    """
	arg_parser = ArgumentParser()
	arg_parser.add_argument("--board",
							help="Board name or random",
							type=str,
							default='random',
							required=False)
	args = vars(arg_parser.parse_args())
	return args['board']

def ConvertBoard(board_name):
	"""Function to convert the `board_name` file to a matrix.

	Args:
		`board_name` (str): the value must be `random` or a filename present in `FOLDER` directory.

	Dependencies:
		`ArgumentParser()` (function): from `argparse` module.

	Returns:
		`board_name` (str): returns a string that represents the board (i.e. file) name.
    """
	board = []
	with open(f'{FOLDER}{board_name}.sudoku', 'r') as board_file:
		flat_board = board_file.read()
		"""Opens and reads the board file."""
	for i in range(0,90,10):
		"""Loops through all numbers in `flat_board` converting them into a matrix."""
		row = []
		for j in range(9):
			row.append(int(flat_board[i+j]))
		board.append(row)
	return board

def GetBoards():
	"""Function to get list of boards (i.e. files) in `FOLDER`.

	Args:
		__None__

	Dependencies:
		__None__

	Returns:
		`boards` (array): array with all files in `FOLDER`.
	"""
	boards = listdir(f'./{FOLDER}')
	for board in boards:
		if '.sudoku' not in board:
			"""Loops through the files in `FOLDER` and removes if it's not .sudoku"""
			boards.remove(board)

	try: boards.remove('debug.sudoku')
	except: pass
	"""Tries to remove `debug` board"""
	return boards

def GetBoard():
	"""Function to get a board from the boards (i.e. files) in `FOLDER`.

	Args:
		__None__

	Dependencies:
		__None__

	Returns:
		`board_name` (str): string with the filename.
	"""
	board_name, boards = ParseArguments(), GetBoards()
	
	if board_name == 'random':
		board_name = boards[randint(0,len(boards)-1)]
	elif board_name not in boards:
		print('invalid board, random used')
		board_name = boards[randint(0,len(boards)-1)]
	else:
		pass
	board_name = board_name.replace('.sudoku','')
	print(f'{board_name} board used')
	return board_name

if __name__ == '__main__':
	board = ConvertBoard(GetBoard())
	MainWindow(board).mainloop()