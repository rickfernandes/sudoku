def print_grid(grid):
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
	queue = {}
	blanks = 0
	for r in range(9):
		for c in range(9):
			if grid[r][c] == 0:
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
			if blanks != 0:
				queue.update({(r,c):blanks})
			blanks = 0
	temp_queue = sorted(queue.items(), key=lambda x: x[1])
	return [v[0] for v in temp_queue]

def possible(row,col,n,grid):
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

# This could be replaced with deepcopy from copy module
def copy_grid(grid):
	temp_grid = []
	for row in grid:
		temp_row = []
		for column in row:
			temp_row.append(column)
		temp_grid.append(temp_row)
	return temp_grid


def solve(grid):
	solutions = []

	def solve_sudoku(grid,queue):
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
	if qty > len(solutions): qty = len(solutions)
	print(f'The grid has {len(solutions)} solutions')
	print(f'Printing {qty} solutions')
	for i in range(qty):
		print(f'--Solution {i+1}--')
		print_grid(solutions[i])

def main():
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


	print_grid(grid)
	solutions = solve(grid)
	print_solutions(solutions,1)


if __name__ == '__main__':
	main()