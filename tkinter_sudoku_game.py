from copy import deepcopy
from random import randint
from tkinter import Tk, Canvas, Frame, BOTH, Button, X, ALL

CELL = 20

BORDER = int(CELL/10)
BORDER_COLOR ='#006CFF'
CURSOR_COLOR = 'red'
INSIDE_BORDER_COLOR = '#14c414'

WIDTH = HEIGHT = 2 * BORDER + 9 * CELL 

class MainWindow():
	def __init__(self,main,game):
		self.main = main
		self.frame = Canvas(main, highlightbackground=BORDER_COLOR, highlightthickness=BORDER,height=HEIGHT-BORDER*2-1,width=WIDTH-BORDER*2-1,bd=0)
		self.buttons = Frame(main) # Frama displaying the options buttons
		self.game = game
		self.__buildLayout()
		self.Cursor(self)

	def __buildLayout(self):
		main.title('SUDOKU')
		frame = self.frame
		frame.propagate(0)
		frame.pack()
		
		self.game._drawGrid(frame)
		self.game._drawNumbers(frame,self.game.original)

		buttons = self.buttons
		buttons.pack(fill=BOTH)

		clear_button = Button(buttons, text='Clear numbers',bd=0)
		solve_button = Button(buttons, text='Solve sudoku',bd=0)
		
		SolveSudokuButton = self.game.SolveSudokuButton
		ClearButton = self.game.ClearButton

		solve_button.config(command=lambda: SolveSudokuButton(self.frame,solve_button))
		clear_button.config(command=lambda: ClearButton(self.frame, solve_button))
		
		clear_button.pack(fill=X)
		solve_button.pack(fill=X)		
		
	class Cursor():
		def __init__(self,window):
			self.window = window
			self.bindKeys()
			self.key = None
			self.x = 0
			self.y = 0

		def bindKeys(self):
			self.window.main.bind('<Key>',self.insertNum)
			self.window.frame.bind('<Button-1>',self.clickedCell)
			self.window.main.bind('<Left>',self.moveCursor)
			self.window.main.bind('<Right>',self.moveCursor)
			self.window.main.bind('<Up>',self.moveCursor)
			self.window.main.bind('<Down>',self.moveCursor)

		def moveCursor(self,event):
			if not self.window.game.gameover:
				moves = {
					'Up':[0,-1],
					'Down':[0,1],
					'Left':[-1,0],
					'Right':[1,0],
				}
				x, y = self.x, self.y
				while True:
					x += moves[event.keysym][0]
					y += moves[event.keysym][1]
					if x <= 8 and x >= 0 and y <= 8 and y >= 0:
						if self.window.game.original[x][y] == 0:
							self.x, self.y = x, y
							break
					else: break
				self.drawCursor()	

		def drawCursor(self):
			if not self.window.game.gameover:
				x,y = BORDER+(self.x*CELL)-1, BORDER+(self.y*CELL)-1
				self.window.frame.delete('cursor')
				self.window.frame.create_rectangle(x,y,x+CELL,y+CELL,outline=CURSOR_COLOR,tags='cursor')

		def drawNumber(self):
			if not self.window.game.gameover:
				x,y = BORDER+(self.x*CELL)-1+CELL/2, BORDER+(self.y*CELL)-1+CELL/2
				if self.window.game.original[self.x][self.y] == 0:
					if Possible(self.window.game.board,self.x,self.y,self.key):
						self.window.frame.delete('number'+str(self.x)+'x'+str(self.y))
						self.window.frame.create_text(x, y, text=self.key, tags='number'+str(self.x)+'x'+str(self.y),fill=INSIDE_BORDER_COLOR)
						self.window.game.board[self.x][self.y] = self.key
						if self.window.game.GameOver():
							self.window.frame.create_text(WIDTH/2,HEIGHT/2-CELL/3,text='Sudoku Over',fill=CURSOR_COLOR)
							self.window.frame.delete('cursor')

		def insertNum(self,event):
			try: int(event.keysym)
			except ValueError:
				if event.keysym == 'BackSpace': self.key = None
				else: self.key = self.key
			else: self.key = int(event.keysym)
			self.drawNumber()
			
		def clickedCell(self,event):
			self.x, self.y = int((event.x-BORDER)/CELL), int((event.y-BORDER)/CELL)
			if self.x < 9 and self.y < 9 and self.window.game.original[self.x][self.y] == 0:
				self.drawCursor()

class SudokuGame():
	def __init__(self,board):
		self.original = deepcopy(board)
		self.board = board
		self.solutions = []
		self.gameover = False

	def GameOver(self):
		rows = []
		for row in self.board:
			rows += row
		if 0 not in rows:
			self.gameover = True
			return True

	def ClearButton(self,frame, solve_button):
		solve_button.config(text='Solve sudoku')
		self.board = deepcopy(self.original)
		frame.delete(ALL)
		self._drawNumbers(frame,self.board)
		self._drawGrid(frame)
		self.gameover = False
		self.solutions = []

	def SolveSudokuButton(self,frame,button):
		if not self.gameover:
			if self.solutions == []:
				self.solutions = Solve(self.board)
			if self.solutions == []:
				solution_text = 'This Sudoku has no possible solutions'
			else:

				sol = randint(0,len(self.solutions)-1)
				self.board = self.solutions[sol]
				solution_text = f'{len(self.solutions)} solutions - Solution {sol+1}'
			frame.delete('cursor')
			button.config(text=solution_text)
			self._drawNumbers(frame,self.board)


	def _drawGrid(self,frame):
		for i in range(0,9):
			x = BORDER+i*CELL-1
			if i % 3 == 0:
				frame.create_line(x,BORDER,x,HEIGHT-BORDER,fill=BORDER_COLOR,width=2)
				frame.create_line(BORDER,x,HEIGHT-BORDER,x,fill=BORDER_COLOR,width=2)
			else:
				frame.create_line(x,BORDER,x,HEIGHT-BORDER,fill=BORDER_COLOR,dash=(1,1))
				frame.create_line(BORDER,x,HEIGHT-BORDER,x,fill=BORDER_COLOR,dash=(1,1))

	def _drawNumbers(self,frame,source):
		frame.delete('numbers')
		for i in range(9):
			for j in range(9):
				x, y = BORDER+i*CELL-1+CELL/2, BORDER+j*CELL-1+CELL/2
				n = source[i][j]
				if n != 0:
					frame.create_text(x, y, text=n, tags='numbers')


def Possible(board,row,col,n):
		for i in range(9):
			if board[row][i] == n or board[i][col] == n: return False
		row_temp, col_temp = (row//3)*3, (col//3)*3
		
		for i in range(3):
			for j in range(3):
				if board[row_temp+i][col_temp+j] == n: return False
		return True

def Solve(board):
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
				if Possible(board,row,col,n+1):
					board[row][col] = n+1
					SolveSudoku(queue[1:])
					board[row][col] = 0
			return 
		solution = deepcopy(board)
		solutions.append(solution)
	SolveSudoku(QueueBlank(board))
	return solutions

def InvertBoard(board):
	return [[board[j][i] for j in range(len(board))] for i in range(len(board[0]))]

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
	[0,0,5,2,8,7,6,0,0]]

	main = Tk()
	board = InvertBoard(board)
	game = SudokuGame(board)
	MainWindow(main,game)

	main.mainloop()