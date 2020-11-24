# -*- coding: utf-8 -*-
"""
This module is a full sudoku game with GUI using `tkinter`. It also provides a solution for the loaded board.

__External modules__: `copy`, `threading`, `random`, `tkinter`

`Compatible with Python3.7 or higher`\n

_Repository:_ https://github.com/rickfernandes/sudoku_solver
"""

from tkinter import Button, Tk, Canvas, Frame, BOTH, X, ALL, ttk
from copy import deepcopy
from threading import Thread, enumerate
from random import randint

# Colour and design
GRID_COLOR = '#2C75A3'
"""Grid colour"""

BACKGROUND_COLOR = '#EEB8B8'
"""Background colour"""

NUMBER_COLOR = '#59B5F0'
"""Numbers colour"""

CURSOR_COLOR = '#F0ED41'
"""Cursor border colour"""

FONT_TYPE = 'Tahoma'
"""Numbers font"""

CELL_SIZE = 60
"""Sudoku board cell size"""

# Constant global variables
BUTTONS_SIZE = 75
HEIGHT = WIDTH = 9 * CELL_SIZE + 6

def WaitThread():
	"""Function to wait process thread responsible for calculation the solutions.

	Args:
		__None__

	Returns:
		__None__
	"""
	while len(enumerate()) > 1: True

def InvertBoard(board):
	"""Function to transpose the imported sudoku board to match the game UI.

	Args:
		`board` (matrix): valid sudoku board.

	Returns:
		Inverted board matrix
	"""
	return [[board[j][i] for j in range(len(board))] for i in range(len(board[0]))]

class MainWindow(Tk):
	"""Toplevel widget of Tk which represents mostly the main window of an application. It has an associated Tcl interpreter."""
	def __init__(self,board):
		"""It's the main game window that contains the sudoku game, sudoku frame (where numbers and grid will be drawn)
		and buttons frame (where the buttons will be packed).

		Uses super class `Tk` from module `tkinter`
		"""
		Tk.__init__(self)
		# Initiates the Tk instance in self
		self.body = Body()
		"""`Body` class"""
		self.cursor = Cursor()
		"""`Cursor` class"""
		self.game = Game(InvertBoard(board))
		"""`Game` class with `InvertBoard`"""
		self.buttons = Buttons(self)
		"""`Cursor` class"""
		self.Config()
		"""Calls `Config` to configure the window"""
		self.InitiateGame()
		"""Calls `InitiateGame` to start the sudoku game"""

	def Config(self):
		"""Method called when `MainWindow` instance is initiate. Configures title, window size and background colour.
		
		Args:
			`self` (MainWindow): `MainWindow` object.

		Returns:
			__None__
		"""
		self.title('SUDOKU')
		self.geometry(f'{WIDTH+2}x{HEIGHT+2 + BUTTONS_SIZE}')
		self.config(bg=BACKGROUND_COLOR)
		print('main window loaded and configured')

	def InitiateGame(self):
		"""Method called when the games starts or is reset with clear board button.
		It calls `Binder`, `DrawGrid`, `DrawNumbers` (with `original_board`), `DrawButtons` and, packs `body` and `buttons`.
		
		Args:
			`self` (MainWindow): `MainWindow` object.

		Returns:
			__None__
		"""
		self.Binder()
		self.body.DrawGrid()
		self.body.DrawNumbers(self.game.original_board,GRID_COLOR)
		self.buttons.DrawButtons()
		self.body.pack(fill=X)
		self.buttons.pack(fill=X)
		print('game initiated')

	def Binder(self):
		"""Method to bind/map keyboard and mouse clicks to their methods.
		
		Args:
			`self` (MainWindow): `MainWindow` object.

		Returns:
			__None__
		"""
		def __MoveHandler(event,window=self):
			# Gets the mouse position and moves/draws the cursor there
			if str(event.type) == 'ButtonPress':
				x, y = int((event.x) / CELL_SIZE), int((event.y) / CELL_SIZE)
				if x > 8: x = 8
				if y > 8: y = 8
				self.cursor.x_pos, self.cursor.y_pos = x, y
			self.cursor.MoveCursor(event,window)

		def __InsertHandler(event):
			# Gets the stroked key and handles what to do with it
			if event.keysym == 'Escape': self.HardReset()
			if event.keysym == 'BackSpace':self.body.DeleteNumber(self.game, self.cursor.x_pos,self.cursor.y_pos)
			elif not self.game.gameover: self.body.InsertNumber(event.keysym,self.game,self.cursor.x_pos,self.cursor.y_pos)
			
			self.game.isGameOver()
			#  Checks if the game is over and draws the game over text

			if self.game.gameover:
				self.body.InsertMiddleText('Game over')
			else:
				self.body.delete('gameover')

		self.body.bind('<Button-1>',__MoveHandler)
		for key in ['<Left>','<Right>','<Up>','<Down>']:
			self.bind(key,__MoveHandler)
		self.bind('<Key>',__InsertHandler)

	def HardReset(self):
		"""Method to completely reset the game. 
		Calls `ResetGame`, delete everything inside `Body` frame and reset `inserted_numbers` array.
		
		Args:
			`self` (MainWindow): `MainWindow` object.

		Returns:
			__None__
		"""
		self.game.ResetGame()
		self.body.delete(ALL)
		self.body.inserted_numbers = []
		self.InitiateGame()

class Body(Canvas):
	"""Canvas widget to display graphical elements like lines or text
	Uses super class `Canvas` from module `tkinter`"""

	def __init__(self):
		"""Constructs a canvas widget"""
		Canvas.__init__(self)
		# Initiate `Canvas` instance
		self.config(bg=BACKGROUND_COLOR,height=HEIGHT-4)
		# Configures background colour.
		self.inserted_numbers = []
		"""Array that keeps track of the inserted numbers sequence."""

	def DrawGrid(self):
		"""Method to draw sudoku board grid. 
		
		Args:
			`self` (Body): `Body` object.

		Returns:
			__None__
		"""
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
		"""Method to draw original (i.e. loaded) sudoku board numbers. 
		
		Args:
			`self` (Body): `Body` object.\n
			`board` (matrix): valid sudoku board, loaded at the beginning of the program.\n
			`color` (str): `GRID_COLOR` colour.\n

		Returns:
			__None__
		"""
		self.delete('numbers')
		# delete all numbers with tag 'numbers'
		for i in range(9):
			for j in range(9):
				x, y = i * CELL_SIZE + CELL_SIZE / 2 + 4, j * CELL_SIZE + CELL_SIZE / 2 + 4
				n = board[i][j]
				if n != 0:
					self.create_text(x, y, text=n, tags='numbers',fill=GRID_COLOR, font=(FONT_TYPE,int(CELL_SIZE/3)))

	def InsertNumber(self,key,game,x_pos,y_pos,**kwargs):
		"""Method to draw the inserted number in a valid position of the sudoku board.
		The number will only be inserted if the position on `original_board` is `0`, `PossibleMove` returns True and if the number is not `0`.
		
		Args:
			`self` (Body): `Body` object.\n
			`key` (str): comes from binder. If not an integer, it will be ignored.\n
			`game` (Game): `Game` object.\n
			`x_pos` (int): x position of the number to be inserted.\n
			`y_pos` (int): y position of the number to be inserted.\n
			`kwargs['move_type']` (str): if `backwards` does not update `inserted_numbers`\n

		Returns:
			__None__
		"""
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
		"""Method to delete a number in a valid position of the sudoku board.
		
		Args:
			`self` (Body): `Body` object.\n
			`game` (Game): `Game` object.\n
			`x_pos` (int): x position of the number to be deleted.\n
			`y_pos` (int): y position of the number to be deleted.\n
			`kwargs['move_type']` (str): if `backwards` does not update `inserted_numbers`\n

		Returns:
			__None__
		"""
		try: move_type = kwargs['move_type']
		except:  move_type = ''
		if move_type != 'backwards':
			self.inserted_numbers.append([x_pos,y_pos,game.board[x_pos][y_pos],'delete'])
		game.board[x_pos][y_pos] = 0
		self.delete(f'number{x_pos}x{y_pos}')
		game.gameover = False

	def InsertMiddleText(self,text):
		"""Method to insert a text in the middle of `Body`.
		
		Args:
			`self` (Body): `Body` object.\n
			`text` (str): text to be inserted/drawn object.\n

		Returns:
			__None__
		"""
		self.delete('cursor')
		text = self.create_text(WIDTH / 2,HEIGHT / 2 - int(CELL_SIZE/2), text=text, font=(FONT_TYPE, int(CELL_SIZE/2)),fill=CURSOR_COLOR,tags='gameover')
		rect = self.create_rectangle(self.bbox(text),fill=BACKGROUND_COLOR,tags='gameover')
		self.tag_lower(rect,text)

class Cursor():	
	"""Cursor widget to display/select the cells in the sudoku board."""
	def __init__(self):
		self.x_pos = 0
		"""Column position of the cursor"""
		self.y_pos = 0
		"""Row position of the cursor"""
		self.number = 0

	def DrawCursor(self,body):
		"""Method to draw the cursor in positions `x_pos` and `y_pos`. 
		
		Args:
			`body` (Body): `Body` object.
			`self` (Cursor): `Cursor` object.

		Returns:
			__None__
		"""
		x, y = 4 + (self.x_pos * CELL_SIZE), 4 + (self.y_pos * CELL_SIZE)
		body.delete('cursor')
		body.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, outline=CURSOR_COLOR, tags='cursor',width=2)

	def MoveCursor(self,event,window):
		"""Method to move cursor positions `x_pos` and `y_pos` according to the arrow keyboard input.
		The movement skips cells with numbers from original board.
		
		Args:
			`self` (Cursor): `Cursor` object.
			`body` (Window): `MainWindow` object.
			`event` (bind.event): event from `Tk.bind` method.

		Returns:
			__None__
		"""
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
	"""Contains all necessary info for the correct handling of the sudoku game.
	Takes one parameter `board` (a valid sudoku board) to be initiated."""

	def __init__(self,board):
		self.gameover = False
		"""Boolean value to determine if the game is over"""
		self.board = board
		"""Valid sudoku board. Will be updated with the number inserted by the user."""
		self.original_board = deepcopy(board)
		"""Copy of the `board` used to initiate the class. Will not change throughout the game."""
		self.original_solutions = []
		"""Array with all possible solutions for the original board. It's calculated at the game start and will not change throughout the game."""
		self.solutions = []
		"""Array with possible solutions for current `board` (i.e. board with inserted numbers."""
		Thread(target=self.SudokuSolver).start()
		# Thread initiate to calculate all possible solutions for original board.

	def PossibleMove(self, number, x_pos, y_pos):
		"""Method to check if `number` can be inserted in positions `x_pos` & `y_pos` of the `board`.
		
		Args:
			`self` (Game): `Game` object.\n
			`number` (int): number to be inserted.\n
			`x_pos` (int): board column.\n
			`y_pos` (int): board row.\n

		Returns:
			boolean: can `n` be inserted. _False_ if not possible. _True_ otherwise.
		"""
		for i in range(9):
			if self.board[x_pos][i] == number or self.board[i][y_pos] == number: return False
		x_temp, y_temp = (x_pos//3)*3, (y_pos//3)*3
		for i in range(3):
			for j in range(3):
				if self.board[x_temp+i][y_temp+j] == number: return False
		return True

	def RemoveInvalidSolutions(self):
		"""Method to remove all invalid solutions for current `board`.
		
		Args:
			`self` (Game): `Game` object.

		Returns:
			__None__
		"""
		def MatchSolution(board,solution):
			# Matches the solution with the board.
			# If solution cannot be applied to board, returns False
			for x in range(9):
				for y in range(9):
					if board[x][y] != 0 and board[x][y] != solution[x][y]:
						return False
			return True
		for s in range(len(self.solutions)-1,-1,-1):
			# loops through all solutions and remove the invalid ones.
			if not MatchSolution(self.board,self.solutions[s]):
				del self.solutions[s]

	def SudokuSolver(self):
		"""Method to solve the sudoku board, inserting all solutions into `original_solutions`.
		
		Args:
			`self` (Game): `Game` object.

		Returns:
			__None__
		"""
		def QueueBlank(board):
			# Creates a queue with the blank positions (i.e. `0`s) of grid and the quantity of blank spaces on its row, column and square.
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
			# Basic sudoku solver algorithm using recursion.
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
		"""Method to check there are `0` in board, if not the game is over. Stores the value in `gameover` variable of `Game`.
		
		Args:
			`self` (Game): `Game` object.

		Returns:
			__None__
		"""
		rows = []
		for row in self.board: 
			rows += row
		if 0 not in rows:
			self.gameover = True
		else:
			self.gameover = False

	def ResetGame(self):
		"""Method to reset `board` to `original_board` and `solutions` to `original_solutions`.
	
		Args:
			`self` (Game): `Game` object.

		Returns:
			__None__
		"""
		self.board = deepcopy(self.original_board)
		self.solutions = deepcopy(self.original_solutions)

class Buttons(Frame):
	"""Frame widget which contains the buttons. Has the `MainWindow` object as argument.
	"""
	def __init__(self,mainwindow):
		"""Uses super class `Frame` from module `tkinter`"""
		Frame.__init__(self)
		"""Initiates Frame instance in self."""
		self.clear_button = ttk.Button(self, text='Clear numbers',command=lambda: self.ClearBoard(mainwindow))
		"""Button that call `ClearBoard` method"""
		self.solve_button = ttk.Button(self, text='Solve sudoku',command=lambda: self.SolveBoard(mainwindow))
		"""Button that call `SolveBoard` method"""
		self.back_button = ttk.Button(self, text='Move back',command=lambda: self.MoveBackwards(mainwindow))
		"""Button that call `MoveBackwards` method"""

	def ClearBoard(self,mainwindow):
		"""Method to clear/reset `board`. Calls `HardReset` method.
	
		Args:
			`self` (Buttons): `Buttons` object.

		Returns:
			__None__
		"""
		WaitThread()
		mainwindow.HardReset()
		print('board cleared')


	def SolveBoard(self,mainwindow):
		"""Method to print one random possible solution for the board. Calls method `RemoveInvalidSolutions` and draws the solution (if it exists).

		Args:
			`self` (Buttons): `Buttons` object.

		Returns:
			__None__
		"""
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
		"""Method to print one random possible solution for the board. Calls method `RemoveInvalidSolutions` and draws a solution (if there are any).

		Args:
			`self` (Buttons): `Buttons` object.

		Returns:
			__None__
		"""
		if mainwindow.body.inserted_numbers != []:
			last_move = mainwindow.body.inserted_numbers[-1]
			if last_move[-1] == 'insert':
				mainwindow.body.DeleteNumber(mainwindow.game,last_move[0],last_move[1],move_type='backwards')
			elif last_move[-1] == 'delete':
				mainwindow.body.InsertNumber(last_move[2],mainwindow.game,last_move[0],last_move[1],move_type='backwards')
			mainwindow.body.inserted_numbers = mainwindow.body.inserted_numbers[0:-1]
		mainwindow.body.delete('gameover')
		
	def DrawButtons(self):
		"""Method to pack all buttons"""
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