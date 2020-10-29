from tkinter import *
from copy import deepcopy

# Global variables
GRID_COLOR = 'black'
CELL_SIZE = 30
BUTTONS_SIZE = 90
BORDER_SIZE = int(CELL_SIZE/10)
HEIGHT = WIDTH = 9 * CELL_SIZE + 2 * BORDER_SIZE
NUMBER_COLOR = 'green'
CURSOR_COLOR = 'red'

class MainWindow(Tk):
	def __init__(self,board):
		Tk.__init__(self)
		self.body = Body()
		self.cursor = Cursor()
		self.game = Game(board)
		self.buttons = Buttons()
		self.Config()
		self.InitiateGame()

	def Config(self):
		self.title('SUDOKU')
		self.geometry(f'{WIDTH + BORDER_SIZE * 2}x{HEIGHT + BORDER_SIZE * 2 + BUTTONS_SIZE}')

	def InitiateGame(self):
		self.Binder()
		self.body.pack()
		self.buttons.pack()
		self.body.DrawGrid()
		self.body.DrawNumbers(self.game.original_board)
		self.buttons.DrawButtons()
		self.RunGame()

	def RunGame(self):
		pass
		# if self.game.gameover:
		# 	self.body.create_text(WIDTH/2,HEIGHT/2-CELL_SIZE/3,text='Sudoku Over',fill=CURSOR_COLOR)
		# else:
		# 	self.cursor.DrawCursor(self.body)
		# 	self.body.InsertNumber(self.game.board,self.cursor)

	def Binder(self):
		self.bind('<Key>',self.body.InsertNumber)
		self.bind('<Button-1>',self.cursor.MoveCursor)
		self.bind('<Left>',self.cursor.MoveCursor)
		self.bind('<Right>',self.cursor.MoveCursor)
		self.bind('<Up>',self.cursor.MoveCursor)
		self.bind('<Down>',self.cursor.MoveCursor)

class Body(Canvas):
	def __init__(self):
		Canvas.__init__(self)
		self.inserted_numbers = []

	def DrawGrid(self):
		self.create_rectangle(2 * BORDER_SIZE,2 * BORDER_SIZE,HEIGHT - BORDER_SIZE,WIDTH - BORDER_SIZE,width=2)
		for i in range(0,9):
			x = BORDER_SIZE + i * CELL_SIZE
			if i % 3 == 0:
				self.create_line(x, BORDER_SIZE, x, HEIGHT - BORDER_SIZE, fill=GRID_COLOR, width=2)
				self.create_line(BORDER_SIZE, x, HEIGHT - BORDER_SIZE, x, fill=GRID_COLOR, width=2)
			else:
				self.create_line(x, BORDER_SIZE, x, HEIGHT - BORDER_SIZE, fill=GRID_COLOR, dash=(1,1))
				self.create_line(BORDER_SIZE, x, HEIGHT - BORDER_SIZE, x, fill=GRID_COLOR, dash=(1,1))

	def DrawNumbers(self,board):
		self.delete('numbers')
		for i in range(9):
			for j in range(9):
				x, y = BORDER_SIZE + i * CELL_SIZE + CELL_SIZE / 2, BORDER_SIZE + j * CELL_SIZE + CELL_SIZE / 2
				n = board[i][j]
				if n != 0:
					self.create_text(x, y, text=n, tags='numbers')

	def InsertNumber(event,board,cursor):
		print(event.keysym)
		pass

	def DeleteNumber(self,board):
		pass

class Cursor():
	def __init__(self):
		self.x_pos = 0
		self.y_pos = 0
		self.number = 0

	def DrawCursor(self,body):
		pass

	def MoveCursor(self,event):
		moves = {'Up':[0,-1],'Down':[0,1],'Left':[-1,0],'Right':[1,0],}
		x, y = self.x_pos, self.y_pos
		while True:
			x += moves[event.keysym][0]
			y += moves[event.keysym][1]
			# if x <= 8 and x >= 0 and y <= 8 and y >= 0:
				# if game.original[x][y] == 0:
				# 	self.x, self.y = x, y
				# 	break
			# else: break

class Game():
	def __init__(self,board):
		self.gameover = False
		self.board = board
		self.original_board = deepcopy(board)
		self.solutions = []

	def PossibleMove(self, number, x_pos, y_pos,board):
		for i in range(9):
			if board[x_pos][i] == number or board[i][y_pos] == number: return False
		x_temp, y_temp = (x_pos//3)*3, (y_pos//3)*3
		
		for i in range(3):
			for j in range(3):
				if board[x_temp+i][y_temp+j] == number: return False
		return True

	def SudokuSolver(self):
		solutions = []

		def QueueBlank(board):
			queue = {}
			blanks = 0
			for r in range(9):
				for c in range(9):
					if board[r][c] == 0:
						for i in range(9):
							if board[i][c] == 0: blanks += 1
							if board[r][i] == 0: blanks += 1
						r_temp, c_temp = (r//3) * 3, (c//3) * 3
						for i in range(3):
							for j in range(3):
								if board[r_temp+i][c_temp+j] == 0: blanks += 1
					if blanks != 0: queue.update({(r,c):blanks})
					blanks = 0
			temp_queue = sorted(queue.items(), key=lambda x: x[1])
			return [v[0] for v in temp_queue]

		def SolveSudoku(queue):
			if queue:
				row, col = queue[0][0], queue[0][1]
				for n in range(9):
					if self.PossibleMove(n+1,row,col,board):
						board[row][col] = n+1
						SolveSudoku(queue[1:])
						board[row][col] = 0
				return 
			solution = deepcopy(board)
			solutions.append(solution)

		SolveSudoku(QueueBlank(self.board))
		self.solutions = solutions

	def isGameOver(self):
		rows = []
		for row in self.board:
			rows += row
		if 0 not in rows:
			self.gameover = True
			return True

	def ResetGame(self):
		pass

class Buttons(Frame):
	def __init__(self):
		Frame.__init__(self)
		self.clear_button = Button(self, text='Clear numbers',bd=0,command=lambda: ClearBoard(mainwindow))
		self.solve_button = Button(self, text='Solve sudoku',bd=0,command=lambda: SolveBoard(mainwindow))
		self.back_button = Button(self, text='Solve sudoku',bd=0,command=lambda: MoveBackwards(mainwindow))

	def ClearBoard(mainwindow):
		pass

	def SolveBoard(mainwindow):
		pass

	def MoveBackwards(mainwindow):
		pass

	def DrawButtons(self):
		pass

if __name__ == '__main__':
	board = [
		[5,3,2,9,4,6,1,0,0],
		[6,7,4,1,3,8,9,0,0],
		[1,9,8,5,7,2,3,0,0],
		[8,2,9,7,0,1,5,0,0],
		[4,5,6,8,9,3,7,0,0],
		[7,1,3,4,2,5,8,0,0],
		[9,6,1,3,5,4,2,0,0],
		[0,0,7,6,0,9,4,0,0],
		[0,0,5,2,8,7,6,0,0]
		]
	main = MainWindow(board).mainloop()