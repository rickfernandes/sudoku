from tkinter import Button, Tk, Canvas, Frame, BOTH, X, ALL
from copy import deepcopy
from threading import Thread, enumerate
from random import randint

# Global variables
GRID_COLOR = '#00444d'
BACKGROUND_COLOR = '#e3fcff'
NUMBER_COLOR = '#00bf39'
CURSOR_COLOR = 'red'
CELL_SIZE = 60
FONT_TYPE = 'Tahoma'

# Fix global variables
BUTTONS_SIZE = 84
HEIGHT = WIDTH = 9 * CELL_SIZE + 6

def WaitThread():
	while len(enumerate()) > 1: True

def InvertBoard(board):
	return [[board[j][i] for j in range(len(board))] for i in range(len(board[0]))]

class MainWindow(Tk):
	def __init__(self,board):
		Tk.__init__(self)
		self.body = Body()
		self.cursor = Cursor()
		self.game = Game(InvertBoard(board))
		self.buttons = Buttons(self)
		self.Config()
		self.InitiateGame()

	def Config(self):
		self.title('SUDOKU')
		self.geometry(f'{WIDTH+2}x{HEIGHT+2 + BUTTONS_SIZE}')
		self.config(bg=BACKGROUND_COLOR)
		print('main window loaded and configured')

	def InitiateGame(self):
		self.Binder()
		self.body.DrawGrid()
		self.body.DrawNumbers(self.game.original_board,GRID_COLOR)
		self.buttons.DrawButtons()
		self.body.pack(fill=X)
		self.buttons.pack(fill=X)
		print('game initiated')

	def Binder(self):
		def __MoveHandler(event,window=self):
			if str(event.type) == 'ButtonPress':
				x, y = int((event.x) / CELL_SIZE), int((event.y) / CELL_SIZE)
				if x > 8: x = 8
				if y > 8: y = 8
				self.cursor.x_pos, self.cursor.y_pos = x, y
			self.cursor.MoveCursor(event,window)

		def __InsertHandler(event):
			if event.keysym == 'Escape': self.HardReset()
			if event.keysym == 'BackSpace':self.body.DeleteNumber(self.game, self.cursor.x_pos,self.cursor.y_pos)
			elif not self.game.gameover: self.body.InsertNumber(event.keysym,self.game,self.cursor.x_pos,self.cursor.y_pos)
			
			self.game.isGameOver()

			if self.game.gameover:
				self.body.InsertMiddleText('Game over')
			else:
				self.body.delete('gameover')

		self.body.bind('<Button-1>',__MoveHandler)
		self.bind('<Key>',__InsertHandler)
		for key in ['<Left>','<Right>','<Up>','<Down>']:
			self.bind(key,__MoveHandler)

	def HardReset(self):
		self.game.ResetGame()
		self.body.delete(ALL)
		self.body.inserted_numbers = []
		self.InitiateGame()

class Body(Canvas):
	def __init__(self):
		Canvas.__init__(self)
		self.config(bg=BACKGROUND_COLOR,height=HEIGHT-4)
		self.inserted_numbers = []

	def DrawGrid(self):
		for i in range(0,10):
			x = i * CELL_SIZE
			if i % 3 == 0:
				self.create_line(x + 4, 2, x + 4, HEIGHT-1, fill=GRID_COLOR, width=2)
				self.create_line(2, x + 4, WIDTH-1, x + 4, fill=GRID_COLOR, width=2)
			else:
				pass
				self.create_line(x + 4, 2, x + 4, HEIGHT-1, fill=GRID_COLOR, dash=(1,1))
				self.create_line(2, x + 4, WIDTH-1, x + 4, fill=GRID_COLOR, dash=(1,1))

	def DrawNumbers(self,board,color):
		self.delete('numbers')
		for i in range(9):
			for j in range(9):
				x, y = i * CELL_SIZE + CELL_SIZE / 2 + 4, j * CELL_SIZE + CELL_SIZE / 2 + 4
				n = board[i][j]
				if n != 0:
					self.create_text(x, y, text=n, tags='numbers',fill=GRID_COLOR, font=(FONT_TYPE,int(CELL_SIZE/3)))

	def InsertNumber(self,key,game,x_pos,y_pos,**kwargs):
		x, y = 4 + x_pos * CELL_SIZE + CELL_SIZE / 2, 4 + y_pos * CELL_SIZE + CELL_SIZE / 2
		try: move_type = kwargs['move_type']
		except:  move_type = ''
		try: int(key)
		except: pass
		else:
			number = int(key)
			if game.PossibleMove(number,x_pos,y_pos) and game.original_board[x_pos][y_pos] == 0 and number != 0:
				self.delete(f'number{x_pos}x{y_pos}')
				game.board[x_pos][y_pos] = number
				self.create_text(x, y, text=number, tags=f'number{x_pos}x{y_pos}', fill=NUMBER_COLOR, font=(FONT_TYPE,int(CELL_SIZE/3)))
				if move_type != 'backwards':
					self.inserted_numbers.append([x_pos,y_pos,number,'insert'])


	def DeleteNumber(self,game,x_pos,y_pos,**kwargs):
		try: move_type = kwargs['move_type']
		except:  move_type = ''
		if move_type != 'backwards':
			self.inserted_numbers.append([x_pos,y_pos,game.board[x_pos][y_pos],'delete'])
		game.board[x_pos][y_pos] = 0
		self.delete(f'number{x_pos}x{y_pos}')
		game.gameover = False

	def InsertMiddleText(self,text):
		self.delete('cursor')
		text = self.create_text(WIDTH / 2,HEIGHT / 2 - int(CELL_SIZE/2), text=text, font=('Helvetica', int(CELL_SIZE/2)),fill=CURSOR_COLOR,tags='gameover')
		rect = self.create_rectangle(self.bbox(text),fill=BACKGROUND_COLOR,tags='gameover')
		self.tag_lower(rect,text)

class Cursor():
	def __init__(self):
		self.x_pos = 0
		self.y_pos = 0
		self.number = 0

	def DrawCursor(self,body):
		x, y = 4 + (self.x_pos * CELL_SIZE), 4 + (self.y_pos * CELL_SIZE)
		body.delete('cursor')
		body.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, outline=CURSOR_COLOR, tags='cursor',width=2)

	def MoveCursor(self,event,window):
		moves = {'Up':[0,-1],'Down':[0,1],'Left':[-1,0],'Right':[1,0],}
		x, y = self.x_pos, self.y_pos
		while event.keysym in list(moves):
			x += moves[event.keysym][0]
			y += moves[event.keysym][1]
			if x <= 8 and x >= 0 and y <= 8 and y >= 0:
				if window.game.original_board[x][y] == 0:
					self.x_pos, self.y_pos = x, y
					break
			else: break
		if window.game.original_board[self.x_pos][self.y_pos] == 0:
			self.DrawCursor(window.body)

class Game():
	def __init__(self,board):
		self.gameover = False
		self.board = board
		self.original_board = deepcopy(board)
		self.original_solutions = []
		Thread(target=self.SudokuSolver).start()

	def PossibleMove(self, number, x_pos, y_pos):
		for i in range(9):
			if self.board[x_pos][i] == number or self.board[i][y_pos] == number: return False
		x_temp, y_temp = (x_pos//3)*3, (y_pos//3)*3
		for i in range(3):
			for j in range(3):
				if self.board[x_temp+i][y_temp+j] == number: return False
		return True

	def RemoveInvalidSolutions(self):
		def MatchSolution(board,solution):
			for x in range(9):
				for y in range(9):
					if board[x][y] != 0 and board[x][y] != solution[x][y]:
						return False
			return True
		for s in range(len(self.solutions)-1,-1,-1):
			if not MatchSolution(self.board,self.solutions[s]):
				del self.solutions[s]

	def SudokuSolver(self):
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
					if self.PossibleMove(n+1,row,col):
						self.board[row][col] = n+1
						SolveSudoku(queue[1:])
						self.board[row][col] = 0
				return 
			solution = deepcopy(self.board)
			self.original_solutions.append(solution)
		SolveSudoku(QueueBlank(self.board))
		print('solutions thread finished')

	def isGameOver(self):
		rows = []
		for row in self.board:
			rows += row
		if 0 not in rows:
			self.gameover = True
		else:
			self.gameover = False

	def ResetGame(self):
		self.board = deepcopy(self.original_board)
		self.solutions = deepcopy(self.original_solutions)

class Buttons(Frame):
	def __init__(self,mainwindow):
		Frame.__init__(self)
		self.config(bg='green')
		self.clear_button = Button(self, text='Clear numbers',bd=0,command=lambda: self.ClearBoard(mainwindow))
		self.solve_button = Button(self, text='Solve sudoku',bd=0,command=lambda: self.SolveBoard(mainwindow))
		self.back_button = Button(self, text='Move back',bd=0,command=lambda: self.MoveBackwards(mainwindow))

	def ClearBoard(self,mainwindow):
		WaitThread()
		print('board cleared')
		mainwindow.HardReset()


	def SolveBoard(self,mainwindow):
		WaitThread()
		game = mainwindow.game
		game.solutions = deepcopy(game.original_solutions)
		game.RemoveInvalidSolutions()
		if game.solutions == []:
			mainwindow.body.InsertMiddleText('No possible solutions')
		else:
			mainwindow.body.delete('gameover')
			r = randint(0,len(game.solutions)-1)
			for x in range(9):
				for y in range(9):
					if game.solutions[r][x][y] != game.original_board[x][y]:
						mainwindow.body.InsertNumber(game.solutions[r][x][y],game,x,y)

	def MoveBackwards(self,mainwindow):
		if mainwindow.body.inserted_numbers != []:
			last_move = mainwindow.body.inserted_numbers[-1]
			if last_move[-1] == 'insert':
				mainwindow.body.DeleteNumber(mainwindow.game,last_move[0],last_move[1],move_type='backwards')
			elif last_move[-1] == 'delete':
				mainwindow.body.InsertNumber(last_move[2],mainwindow.game,last_move[0],last_move[1],move_type='backwards')
			mainwindow.body.inserted_numbers = mainwindow.body.inserted_numbers[0:-1]
		mainwindow.body.delete('gameover')
		
	def DrawButtons(self):
		self.clear_button.pack(fill=X)
		self.solve_button.pack(fill=X)
		self.back_button.pack(fill=X)

if __name__ == '__main__':
	board = [
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[8,2,9,7,0,1,5,0,0],
		[4,5,6,8,9,3,7,0,0],
		[7,1,3,4,2,5,8,0,0],
		[9,6,1,3,5,4,2,0,0],
		[0,0,7,6,0,9,4,0,0],
		[0,0,5,2,8,7,6,0,0]
		]

	MainWindow(board).mainloop()