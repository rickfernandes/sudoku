import numpy as np

grid = [
	[5,3,0,0,7,0,0,0,0],
	[6,0,0,1,9,5,0,0,0],
	[0,9,8,0,0,0,0,6,0],
	[8,0,0,0,6,0,0,0,3],
	[4,0,0,8,0,3,0,0,1],
	[7,0,0,0,2,0,0,0,6],
	[0,6,0,0,0,0,2,8,0],
	[0,0,0,4,1,9,0,0,5],
	[0,0,0,0,8,0,0,7,9]
]

sol = 1

def possible(y,x,n):
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
	global sol
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
	print(f'Solution {sol}')
	print(np.matrix(grid))
	sol +=1

def main():
	print(np.matrix(grid))
	solve()
	

if __name__ == '__main__':
	main()