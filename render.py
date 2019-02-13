
from tkinter import Frame, Label, CENTER

SIZE = 500
GRID_PADDING = 10
BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"
BACKGROUND_COLOR_DICT = {   2:"#eee4da", 4:"#ede0c8", 8:"#f2b179", 16:"#f59563", \
                            32:"#f67c5f", 64:"#f65e3b", 128:"#edcf72", 256:"#edcc61", \
                            512:"#edc850", 1024:"#edc53f", 2048:"#edc22e" }
CELL_COLOR_DICT = { 2:"#776e65", 4:"#776e65", 8:"#f9f6f2", 16:"#f9f6f2", \
                    32:"#f9f6f2", 64:"#f9f6f2", 128:"#f9f6f2", 256:"#f9f6f2", \
                    512:"#f9f6f2", 1024:"#f9f6f2", 2048:"#f9f6f2" }
FONT = ("Verdana", 40, "bold")

def init_grid(root, grid_len):
	background = Frame(root, bg=BACKGROUND_COLOR_GAME, width=SIZE, height=SIZE)
	background.grid()
	grid_cells = []
	for i in range(grid_len):
		grid_row = []
		for j in range(grid_len):
			cell = Frame(background, bg=BACKGROUND_COLOR_CELL_EMPTY, width=SIZE/grid_len, height=SIZE/grid_len)
			cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
			# font = Font(size=FONT_SIZE, family=FONT_FAMILY, weight=FONT_WEIGHT)
			t = Label(master=cell, text="", bg=BACKGROUND_COLOR_CELL_EMPTY, justify=CENTER, font=FONT, width=4, height=2)
			t.grid()
			grid_row.append(t)
		grid_cells.append(grid_row)
	return grid_cells

def update_grid_cells(grid_cells, matrix):
	if len(grid_cells) != len(matrix)\
	or len(grid_cells[0]) != len(matrix[0]):
		raise Exception("Grid and matrix size miss match")
	for i in range(len(grid_cells)):
		for j in range(len(grid_cells)):
			new_number = matrix[i][j]
			if new_number == 0:
				grid_cells[i][j].configure(text="", bg=BACKGROUND_COLOR_CELL_EMPTY)
			else:
				grid_cells[i][j].configure(text=str(new_number), bg=BACKGROUND_COLOR_DICT[new_number], fg=CELL_COLOR_DICT[new_number])


