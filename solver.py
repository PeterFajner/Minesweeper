import random
import time

WAIT_TIME = 0.1 # seconds

def solve(app):

	"""
	# no need to work with rows
	cells = []
	for row in app.cells:
		for cell in row:
			cells.append(cell)
			"""

	marked_mines = 0
	total_mines = app.num_mines

	while marked_mines < total_mines:
		need_random_click = True
		for row in app.cells:
			for cell in row:
				if cell.is_revealed and cell.number > 0:
					neighbours = cell.get_neighbours(app.cells)

					# if the number of unrevealed neighbours is equal to the number on the cell, mark all unrevealed neighbours
					num_nearby_unrevealed = 8
					for neighbour in neighbours:
						if neighbour.is_revealed:
							num_nearby_unrevealed -= 1
					if num_nearby_unrevealed == cell.number:
						for neighbour in neighbours:
							if not neighbour.is_revealed and not neighbour.is_marked:
								neighbour.right_mouse(None)
								flush(app)
								time.sleep(WAIT_TIME)
								marked_mines += 1
								need_random_click = False

					# if the number of marked neighbours is equal to the number on the cell, reveal all unmarked neighbours
					num_nearby_marked = 0
					for neighbour in neighbours:
						if neighbour.is_marked:
							num_nearby_marked += 1
					if num_nearby_marked == cell.number:
						for neighbour in neighbours:
							if not neighbour.is_marked and not neighbour.is_revealed:
								neighbour.left_mouse(None)
								flush(app)
								time.sleep(WAIT_TIME)
								need_random_click = False

		print need_random_click
		if need_random_click:
			x = 0
			y = 0

			iteration = 0

			while True:
				x = random.randrange(0, len(app.cells))
				y = random.randrange(0, len(app.cells[0]))
				iteration += 1
				if iteration > 100:
					return
				#if app.cells[x][y].is_marked:
					#print "is marked"
				#if app.cells[x][y].is_revealed:
					#print "is revealed"
				if not app.cells[x][y].is_marked and not app.cells[x][y].is_revealed:
					break
				#print app.cells[x][y].x, app.cells[x][y].y
			app.cells[x][y].left_mouse(None)
			flush(app)
			time.sleep(WAIT_TIME)

	# make sure all non-marked cells are revealed
	for row in app.cells:
		for cell in row:
			if not cell.is_marked and not cell.is_revealed:
				cell.is_revealed = True
				app.update_cell_widget(cell)
				flush(app)
				time.sleep(WAIT_TIME)

def flush(app):
	# prints to screen
	app.update_widgets()

def hint():
	return