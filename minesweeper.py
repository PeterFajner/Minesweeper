from Tkinter import *
import random
import datetime
#import ttk

# defaults
NUMROWS = 10
NUMCOLUMNS = 10
NUMMINES = 10

# colours
COLOUR_MINE = "red"
COLOUR_UNREVEALED = "grey70"
COLOUR_REVEALED = "grey80"
COLOUR_MARKED = "green yellow"

class App:

	def __init__(self, master):

		# win and lose conditions
		self.has_lost = False
		self.has_won = False

		# a list of the cells as objects
		self.cells = []

		# a list of the cells as widgets
		self.cells_widgets = []

		# frame containing new game options
		self.top = Frame(master) 
		self.top.grid(row=0, padx=4, pady=4)

		self.top.label_rows = Label(self.top, text="Rows:")
		self.top.label_rows.grid(row=0, column=0)

		self.top.entry_rows = Entry(self.top)
		self.top.entry_rows.insert(0, NUMROWS)
		self.top.entry_rows.grid(row=1, column=0, padx=1)

		self.top.label_columns = Label(self.top, text="Columns:")
		self.top.label_columns.grid(row=0, column=1)

		self.top.entry_columns = Entry(self.top)
		self.top.entry_columns.insert(0, NUMCOLUMNS)
		self.top.entry_columns.grid(row=1, column=1, padx=1)

		self.top.label_mines = Label(self.top, text="Mines:")
		self.top.label_mines.grid(row=0, column=2)

		self.top.entry_mines = Entry(self.top)
		self.top.entry_mines.insert(0, NUMMINES)
		self.top.entry_mines.grid(row=1, column=2, padx=1)

		self.top.button_start = Button(self.top, text="New Board", command=self.setup_board)
		self.top.button_start.grid(row=1, column=3, padx=1)


		# a separator between the new game options and the current game board
		#self.separator_frame = Frame(height=2, bd=1, relief=SUNKEN)
		#self.separator_frame.grid(row=1, padx=5, pady=5)

		#self.separator_frame.separator = ttk.Separator(self.separator_frame)
		#self.separator_frame.separator.grid(row=0, sticky=N+S+E+W)


		# frame containing the current game board
		self.bottom = Frame(master)
		self.bottom.grid(row=2)

		self.bottom.button_think = Button(self.bottom, text="Hint")
		self.bottom.button_think.grid(row=0, column=0)

		self.bottom.button_solve = Button(self.bottom, text="Solve")
		self.bottom.button_solve.grid(row=0, column=1)
		
		self.bottom.gameboard = Frame(self.bottom)
		self.bottom.gameboard.grid(row=1, column=0)

	def setup_board(self):
		self.create_cells()
		self.set_mines()
		self.draw_cells()
	 

	# creates Cell objects in memory
	def create_cells(self):

		self.cells = []

		# defaults
		rows = 5 
		columns = 5

		# get values from row and column inputs
		try:
			rows = int(self.top.entry_rows.get())
		except ValueError:
			pass
		try:
			columns = int(self.top.entry_columns.get())
		except ValueError:
			pass

		for x in xrange(columns):
			self.cells.append([])
			for y in xrange(rows):
				cell = Cell(self)
				cell.x = x
				cell.y = y
				self.cells[x].append(cell)

	# draw cells to the screen
	def draw_cells(self):
		for row in self.cells_widgets:
			for widget in row:
				widget.destroy()

		self.cells_widgets = []

		for row in self.cells:
			self.cells_widgets.append([])
			for cell in row:
				container = Frame(self.bottom.gameboard, borderwidth=1, relief=RAISED)
				container.grid(row=cell.y, column=cell.x)
				widget = Label(container, bg=COLOUR_UNREVEALED, text="   ", font="TkFixedFont")
				widget.bind("<Button-1>", cell.left_mouse)
				widget.bind("<Button-3>", cell.right_mouse)
				widget.grid()
				self.cells_widgets[self.cells.index(row)].append(widget)

	# turn some cells into mines
	def set_mines(self):
		num_mines = NUMMINES
		try:
			num_mines = int(self.top.entry_mines.get())
		except ValueError:
			pass
		for i in xrange(num_mines):
			x = random.randrange(len(self.cells))
			y = random.randrange(len(self.cells[0]))
			mine = self.cells[x][y]
			if mine.is_mine:
				i -= 1 # can't have two mines be the same mine
				continue
			mine.is_mine = True

			# set numbers of nearby cells
			for cell in mine.get_neighbours(self.cells):
				cell.number += 1

	# TODO: split this into separate methods (ex: mark(), etc)
	# updates the widget of the given Cell object
	def update_cell_widget(self, cell):
		#container = cells_widgets[cell.y][cell.x]
		#widget = container.winfo_children()[0]
		
		widget = None
		
		try:
			widget = self.cells_widgets[cell.x][cell.y]
		except IndexError: # leftclick seems to be called at init
			return

		if cell.is_revealed:
			if not cell.is_mine:
				widget.config(bg=COLOUR_REVEALED)
				if cell.number > 0:
					widget.config(text=" "+str(cell.number)+" ")
			else:
				widget.config(bg=COLOUR_MINE)
		else:
			if cell.is_marked:
				widget.config(bg=COLOUR_MARKED)
			else:
				widget.config(bg=COLOUR_UNREVEALED)

	def lose(self):
		return




class Cell:
	
	def __init__(self, master):
		self.number = 0
		self.island = 0
		self.is_mine = False
		self.is_revealed = False
		self.is_marked = False

		self.x = 0
		self.y = 0

		self.master = master #deprecated, use "app" instead

	# returns a list of all 8 neighbour cells
	def get_neighbours(self, cells):
		neighbours = []
		for x in [-1, 0, 1]:
			for y in [-1, 0, 1]:
				if not (x == 0 and y == 0) and self.x+x >= 0 and self.y+y >= 0: # the latter two checks are necessary because negative indexes wrap around to the end of a list
					try:
						neighbours.append(cells[self.x + x][self.y + y])
					except IndexError:
						pass
		return neighbours

	# returns a list of the 4 orthogonal neighbour cells
	def get_ortho_neighbours(self, cells):
		neighbours = []
		for x in [-1, 0, 1]:
			for y in [-1, 0, 1]:
				if abs(x+y) == 1 and self.x+x >= 0 and self.y+y >= 0:
					try:
						neighbours.append(cells[self.x + x][self.y + y])
					except IndexError:
						pass
		return neighbours


	# if the cell is not marked, reveal it
	def left_mouse(self, event):
		#print "left mouse" + str(datetime.datetime.now()) + str(dir(self))
		self.reveal_cell()
		app.update_cell_widget(self)

	# toggle marking
	def right_mouse(self, event):
		if not self.is_revealed:
			self.is_marked = not self.is_marked
			app.update_cell_widget(self)
		
	# reveals the cell if not marked, handles revealing neighbouring cells if they're empty and mine checking
	def reveal_cell(self):
		if not self.is_marked and not self.master.has_lost:
			self.is_revealed = True
			if self.is_mine:
				app.lose()

			if self.number == 0 and not self.is_mine:
				for cell in self.get_neighbours(app.cells):
					if not cell.is_revealed and not cell.is_mine:
						cell.reveal_cell()
						app.update_cell_widget(cell)




root = Tk()

app = App(root)

root.mainloop()