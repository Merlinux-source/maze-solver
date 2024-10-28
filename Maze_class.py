from Window_class import Window
from Point_class import Point
from Cell_class import Cell
from time import sleep as wait


class Maze:
	def __init__(
		self,
		win: Window = None,
		x1: int = 50,
		y1: int = 50,
		num_rows: int = 14,
		num_cols: int = 10,
		cell_size_x: int = 50,
		cell_size_y: int = 50,
	):
		"""Creates a Maze instance, assumes most of the options, draws the maze and animates it. contains maze lol (List of Lists)

		Args:
			win (Window): The window / canvas it's drawn on to.
			x1 (int, optional): Maze start position, X Coordinate. Defaults to 50.
			y1 (int, optional): Maze start position, Y Coordinate. Defaults to x1.
			num_rows (int, optional): Number of cell Rows (-). Defaults to 14.
			num_cols (int, optional): Number of cell Columns (|). Defaults to 10.
			cell_size_x (int, optional): Pixel Width per cell. Defaults to 50.
			cell_size_y (int, optional): Pixel Height per cell. Defaults to cell_size_x.
		"""
		self.row_count = num_rows
		self.column_count = num_cols
		self.grid: list[list[Cell]] = []
		self._cells = self.grid

		self.cell_size_x = cell_size_x
		self.cell_size_y = cell_size_y

		self._win = win
		self._x = x1
		self._y = y1
		self._create_cells()
		self._break_entrance_and_exit()

	def get_grid_by_pos(self, x: int, y: int):
		if x > self.cell_size_x:
			raise Exception("invalid X coordinate.")
		if y > self.cell_size_y:
			raise Exception("invalid Y coordinate.")

		return self.grid[y][x]

	def _create_cells(self):
		self.grid = [
			[None for _ in range(self.row_count)] for _ in range(self.column_count)
		]
		self._cells = self.grid
		for column in range(self.column_count):
			for row in range(self.row_count):
				self.grid[column][row] = Cell(
					Point(
						(self.cell_size_x * row) + self._x,
						(self.cell_size_y * column) + self._y,
					),
					Point(
						(self.cell_size_x * (row + 1)) + self._x,
						(self.cell_size_y * (column + 1)) + self._y,
					),
					self._win,
					True,
					True,
					True,
					True,
					grid_coordinate_x=row,
					grid_coordinate_y=column
				)
		self._draw_cell()

	def _draw_cell(self):
		for column in range(self.column_count):
			for row in range(self.row_count):
				if self.grid[column][row] is not None:
					if self._win == None:
						continue
					self.grid[column][row].draw_cell()
					self._animate()

	def _animate(self):
		self._win.redraw()
		wait(0.05)

	def _break_entrance_and_exit(self):
		self.grid[0][0].has_top_wall = False
		self.grid[0][0].draw_cell()

		self.grid[self.column_count - 1][self.row_count - 1].has_bottom_wall = False
		self.grid[self.column_count - 1][self.row_count - 1].draw_cell()
	
	def _break_walls_r(self, visited:Cell=None, current:Cell=None):
		if visited == None:
			current = self.grid[0][0]
		while True:
			to_visit = [i,j]

