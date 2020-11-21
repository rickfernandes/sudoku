from tk_sudoku_game_advanced import MainWindow
from os import listdir
from random import randint
import argparse


def ParseArguments():
	arg_parser = argparse.ArgumentParser()
	arg_parser.add_argument("--board",
							help="Board name or random",
							type=str,
							required=False)
	args = vars(arg_parser.parse_args())
	if not args['board']: args['board'] = 'random'
	return args['board']

def ConvertBoard(board_name):
	board = []
	with open(f'boards/{board_name}.sudoku', 'r') as board_file:
		flat_board = board_file.read()
	for i in range(0,90,10):
		row = []
		for j in range(9):
			row.append(int(flat_board[i+j]))
		board.append(row)
	return board

def GetBoards():
	files = listdir('./boards')
	for file in files:
		if '.sudoku' not in file:
			files.remove(file)
	files.remove('debug.sudoku')
	return files

def GetBoard():
	board_name = ParseArguments()
	if board_name == 'random':
		boards = GetBoards()
		board = boards[randint(0,len(boards)-1)]
	else:
		board = board_name
	return board.replace('.sudoku','')

board = ConvertBoard(GetBoard())
MainWindow(board).mainloop()