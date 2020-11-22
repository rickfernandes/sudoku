# -*- coding: utf-8 -*-
"""
This module is a simple sudoku solver that will return `n` possible solutions
for a board.
It does not use global variables.

__External modules__: _None_

`Compatible with Python3.7 or higher`\n

_Repository:_ https://github.com/rickfernandes/sudoku_solver
"""
def print_grid(grid):
	"""Function to print the sudoku board with `|` and `-` delimiters.

	Args:
		`grid` (matrix): valid matrix representing the sudoku board to be printed.

	Dependencies:
		__None__

	Returns:
		__None__
    """
	for _ in range(25): print('-',end='')
	print('')
	for r in range(9):
		print('|',end='')
		for c in range(9):
			if c in [2,5,8]: print(grid[r][c],end='')
			else: print(grid[r][c],' ',end='')
			if c in [2,5]: print('|',end='')
		print('|')
		if r-1 in [-2,1,4,7]:
			for _ in range(25): print('-',end='')
			print('')

def queue_blank(grid):
	"""Creates a queue with the blank positions (i.e. `0`s) of grid and the quantity of blank spaces
	on its row, column and square.

	Args:
		`grid` (matrix): valid matrix representing the sudoku board to be printed.

	Dependencies:
		__None__

	Returns:
		`queue` (array): sorted array, from positions with least blanks to most blanks
    """
	queue, blanks = {}, 0
	for r in range(9):
		for c in range(9):
			"""Loops through all `grid` positions."""
			if grid[r][c] == 0:
				"""Gets all blanks for each position and add to `blanks`."""
				for i in range(9):
					if grid[i][c] == 0:
						blanks += 1
					if grid[r][i] == 0:
						blanks += 1
				r_temp = (r//3) * 3
				c_temp = (c//3) * 3
				for i in range(3):
					for j in range(3):
						if grid[r_temp+i][c_temp+j] == 0:
							blanks += 1
			if blanks > 0:
				"""Add position to queue with the amount of blanks, if blanks > 0"""
				queue.update({(r,c):blanks})
			blanks = 0
	queue = sorted(queue.items(), key=lambda x: x[1])
	"""Sorts the queue"""
	queue = [v[0] for v in queue]
	"""Extracts the positions, removing the `blanks` key"""
	return queue

def possible(row,col,n,grid):
	"""Function to determine if a number can be inserted in a certain position
	of the `grid`

	Args:
		`row` (int): `grid` row.
		`col` (int): `grid` column.
		`n` (int): number to be inserted in `row` and `column` position.
		`grid` (matrix): valid matrix representing the sudoku board to be printed.

	Dependencies:
		___None___

	Returns:
		bool: can `n` be inserted. _False_ if not possible. _True_ otherwise.
    """
	for i in range(9):
		if grid[row][i] == n or grid[i][col] == n:
			return False
	row_temp = (row//3)*3
	col_temp = (col//3)*3
	for i in range(3):
		for j in range(3):
			if grid[row_temp+i][col_temp+j] == n:
				return False
	return True

def copy_grid(grid):
	"""Function to correctly copy a `grid` to a new variable.	
	_This could be replaced with `deepcopy` from `copy` module_
	
	Args:
		`grid` (matrix): valid matrix representing the sudoku board to be printed.

	Dependencies:
		___None___

	Returns:
		`temp_grid` (matrix): valid matrix representing the sudoku board to be printed.
    """
	temp_grid = []
	for row in grid:
		temp_row = []
		for column in row:
			temp_row.append(column)
		temp_grid.append(temp_row)
	return temp_grid


def solve(grid):
	"""Function to get all possible solutions for `grid`.	
	
	Args:
		`grid` (matrix): valid matrix representing the sudoku board to be printed.

	Dependencies:
		___None___

	Returns:
		`solutions` (array): array of matrices with all possible solutions for `grid`.
    """
	solutions = []
	def solve_sudoku(grid,queue):
		"""Recursively solve the grid and add the `solution` to the solutions array."""
		if queue:
			row = queue[0][0]
			col = queue[0][1]
			for n in range(9):
				if possible(row,col,n+1,grid):
					grid[row][col] = n+1
					solve_sudoku(grid, queue[1:])
					grid[row][col] = 0
			return 
		solution = copy_grid(grid)
		solutions.append(solution)

	solve_sudoku(grid,queue_blank(grid))
	return solutions

def print_solutions(solutions,qty):
	"""Function print a certain `qty` of solutions.	
	
	Args:
		`solutions` (array): array of matrices with all possible solutions for `grid`.
		`qty` (int): quantity of solutions to be printed.

	Dependencies:
		___None___

	Returns:
		__None__
    """
	if qty > len(solutions): qty = len(solutions)
	print(f'The grid has {len(solutions)} solutions')
	print(f'Printing {qty} solution(s)')
	for i in range(qty):
		print(f'--Solution {i+1}--')
		print_grid(solutions[i])

def main():
	"""Main function that defines and prints `grid` than prints `n` solutions.	"""
	grid = [
	[5,3,2,0,0,0,0,0,0],
	[6,7,4,0,0,0,0,0,0],
	[1,9,8,0,0,0,0,6,0],
	[8,2,0,0,6,0,0,0,3],
	[4,5,0,8,0,3,0,0,1],
	[7,1,0,0,2,0,0,0,6],
	[9,6,0,0,0,0,2,8,0],
	[0,0,0,0,1,9,0,0,5],
	[0,0,0,0,0,0,0,0,0]]

	n = 10
	print_grid(grid)
	solutions = solve(grid)
	print_solutions(solutions,n)


if __name__ == '__main__':
	main()