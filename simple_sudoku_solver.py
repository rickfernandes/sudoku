# -*- coding: utf-8 -*-
"""
This module is a simple sudoku solver that will return all possible solutions
for the grid.

`Compatible with Python3.7 or higher`\n

_Repository:_ https://github.com/rickfernandes/sudoku_solver
"""

from numpy import matrix


grid = [[5,3,0,0,7,0,0,0,0],
		[6,0,0,1,9,5,0,0,0],
		[0,9,8,0,0,0,0,6,0],
		[8,0,0,0,6,0,0,0,3],
		[4,0,0,8,0,3,0,0,1],
		[7,0,0,0,2,0,0,0,6],
		[0,6,0,0,0,0,2,8,0],
		[0,0,0,4,1,9,0,0,5],
		[0,0,0,0,8,0,0,7,9]]
"""valid sudoku grid that will be used by `solve()`"""

solution = 1
"""varible used to keep track of the number of solutions"""
def possible(y,x,n):
	"""Function to determine if a number can be inserted in a certain position
	of the `grid`

	Args:
		y (int): `grid` row.
		x (int): `grid` column.
		n (int): number to be inserted in row `y` and column `x`.

	Dependencies:
		___None___

	Returns:
		bool: can `n` be inserted. _False_ if not possible. _True_ otherwise.
    """
	for i in range(9):
		if grid[y][i] == n or grid[i][x] == n:
			return False
	
	x0 = (x//3)*3
	y0 = (y//3)*3
	for i in range(3):
		for j in range(3):
			if grid[y0+i][x0+j] == n:
				return False
	return True

def solve():
	"""Recursive function that prints all possible solutions for `grid`.

	Args:
		___None___

	Dependencies:
		`solution` (int): global variable, increments by 1 with each solution. \n
		`grid` (array): global variable, used to find the solutions. \n
		`possible()` (function).

	Returns:
		___None___
    """
	global solution
	for y in range(9):
		for x in range(9):
			if grid[y][x] == 0:
				for n in range(9):
					if possible(y,x,n+1):
						grid[y][x] = n+1
						solve()
						grid[y][x] = 0
				return
	print('-------------')
	print(f'Solution {solution}')
	print(matrix(grid))
	solution +=1

def main():
	'Prints the original grid and calls `solve()`'
	print(matrix(grid))
	solve()
	

if __name__ == '__main__':
	main()