from random import sample, randint

def CreateOrigin():
	base = 3
	side  = base*base
	def Pattern(r,c): return (base*(r%base)+r//base+c)%side

	def Shuffle(s): return sample(s,len(s)) 

	rows  = [ g*base + r for g in Shuffle(range(base)) for r in Shuffle(range(base)) ] 
	cols  = [ g*base + c for g in Shuffle(range(base)) for c in Shuffle(range(base)) ]
	nums  = Shuffle(range(1,side+1))

	return [[nums[Pattern(r,c)] for c in cols] for r in rows]

def RemoveNums(board,num):
	positions = [(n//9,n%9) for n in range(0,81)]
	for _ in range(num):
		r = randint(0,len(positions)-1)
		pos = positions[r]
		board[pos[0]][pos[1]] = 0
	return board

def WriteFiles(n,rem):
	for b in range(n):
		board = RemoveNums(CreateOrigin(),rem)
		with open('boards/s{:04d}.sudoku'.format(b), 'w') as file:
			for row in range(9):
				for col in range(9):
					file.write(str(board[row][col]))
				file.write('\n')

WriteFiles(10,randint(10,30))