# -*- coding: utf-8 -*-
"""
This module is a sudoku generator that will write `.sudoku` files with sudoku boards.

__External modules__: `random`

`Compatible with Python3.7 or higher`\n

_Repository:_ https://github.com/rickfernandes/sudoku_solver
"""
from random import sample, randint

FOLDER = 'boards/'
"""Destination folder where the `.sudoku` files will be save."""

def CreateOrigin():
	"""Function to create a full sudoku board (matrix) with random numbers.

	Args:
		__None__

	Dependencies:
		`sample()` (function): from `random` module.

	Returns:
		`array` (matrix): returns a `9x9` filled valid suduko board.
    """
	base = 3
	side  = base*base
	def Pattern(r,c):
		"""Returns the pattern for `r` and `c`"""
		return (base*(r%base)+r//base+c)%side

	def Shuffle(s): 
		"""Creates and shuffles an array of size `s`"""
		return sample(s,len(s)) 

	rows  = [ g*base + r for g in Shuffle(range(base)) for r in Shuffle(range(base)) ] 
	"""Random rows array"""
	
	cols  = [ g*base + c for g in Shuffle(range(base)) for c in Shuffle(range(base)) ]
	"""Random columns array"""
	
	nums  = Shuffle(range(1,side+1))
	"""Random numbers array from 1 to 9 (valid sudoku numbers)"""
	
	return [[nums[Pattern(r,c)] for c in cols] for r in rows]

def RemoveNums(board,num):
	"""Function to randomly remove a certain quantity of elements from `board`.

	Args:
		`board` (matrix): valid filled sudoku board.
		`num` (int): quantity of numbers to be removed.

	Dependencies:
		`randint()` (function): from `random` module

	Returns:
		board (matrix): returns a `9x9` (matrix) sudoku board with random `0`s
    """
	positions = [(n//9,n%9) for n in range(0,81)]
	"""Array with all possible positions in the matrix board"""

	for _ in range(num):
		"""Loops through `num` times randomly removing elements from board, using `positions` array
		to keep track of removed elements"""
		r = randint(0,len(positions)-1)
		pos = positions[r]
		board[pos[0]][pos[1]] = 0

	return board

def WriteFiles(n,rem):
	"""Function to create and write boards (as flat string) to `.sudoku` files in `FOLDER` folder.
	The boards will have `rem` missing elements (i.e. matrix positions with `0`). It has a hard limit of 10,000 boards.

	Args:
		`n` (int): number of boards to be created/written\n
		`rem` (int): quantity of numbers to be removed from each board.

	Dependencies:
		__None__

	Returns:
		__None__
    """
    if n > 10000: n = 10000
    """Makes sure that at most 10,000 boards will be created. Due to file naming (i.e. :04d)"""
	for b in range(n):
		"""Loops n times creating and writing a board"""
		board = RemoveNums(CreateOrigin(),rem)
		with open('{}/s{:04d}.sudoku'.format(FOLDER,b), 'w') as file:
			for row in range(9):
				for col in range(9):
					file.write(str(board[row][col]))
				file.write('\n')

if __name__ == '__main__':
	WriteFiles(15,randint(10,30))