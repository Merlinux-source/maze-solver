from Window_class import Window
from Point_class import Point
from Cell_class import Cell
from Player_class import Player
from time import sleep as wait
import random


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
		entropy: int = 69420,
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
		# another refrence for convinience.
		self.width = num_rows
		self.height = num_cols

		self.grid: list[list[Cell]] = []
		self._cells = self.grid

		self.cell_size_x = cell_size_x
		self.cell_size_y = cell_size_y

		self._win = win
		self._x = x1
		self._y = y1
		random.seed(entropy)

		self._create_cells()
		self._break_entrance_and_exit()
		self._break_walls_r()
		self._reset_cells_visited()
		self.sovle()

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
					grid_coordinate_y=column,
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
		"""wait."""
		self._win.redraw()
		wait(0.05)

	def _break_entrance_and_exit(self):
		"""ensure there is a start and a end for the maze"""
		self.grid[0][0].has_top_wall = False
		self.grid[0][0].draw_cell()

		self.grid[self.column_count - 1][self.row_count - 1].has_bottom_wall = False
		self.grid[self.column_count - 1][self.row_count - 1].draw_cell()

	def dedup(self, core: list[Cell], filter: list[Cell]):
		"""
		Returns a list containing elements from `core` that are not present in `filter`.

		Parameters:
		core (list): The main list of elements.
		filter (list): The list containing elements to be removed from `core`.

		Returns:
		list: A new list with elements from `core` excluding those found in `filter`.
		"""
		return [item for item in core if item not in filter and not None]

	def _break_walls_r(self, current_x=0, current_y=0, visited=None):
		if visited == None:
			visited = list()
		#print(
	#		f"_break_walls_r(self, current_x={current_x}, current_y={current_y}, visited={visited})"
	#	)
		visited.append(self.grid[current_y][current_x])
		visited[-1].visited = True
		while True:
			options = list()
			if current_x + 1 <= len(self.grid[0]) - 1:  # updated to use width (columns)
				cell = self.grid[current_y][current_x + 1]
				if cell:
					options.append(cell)
			if current_y + 1 <= len(self.grid) - 1:  # updated to use height (rows)
				cell = self.grid[current_y + 1][current_x]
				if cell:
					options.append(cell)

			if current_y > 0:
				cell = self.grid[current_y - 1][current_x]
				if cell:
					options.append(cell)
			if current_x > 0:
				cell = self.grid[current_y][current_x - 1]
				if cell:
					options.append(cell)

			options = self.dedup(core=options, filter=visited)
			if len(options) == 0:
				return
			choice = random.randint(0, len(options) - 1)
			#print(f"Choice = {choice}; len = {len(options)}")
			choice = options[choice]

			# Adjustments for walls between cells:
			if choice.grid_coordinate_x != current_x:
				if choice.grid_coordinate_x > current_x:
					self.grid[current_y][current_x].has_right_wall = False
					choice.has_left_wall = False
				elif choice.grid_coordinate_x < current_x:
					self.grid[current_y][current_x].has_left_wall = False
					choice.has_right_wall = False

			if choice.grid_coordinate_y != current_y:
				if choice.grid_coordinate_y > current_y:
					self.grid[current_y][current_x].has_bottom_wall = False
					choice.has_top_wall = False
				elif choice.grid_coordinate_y < current_y:
					self.grid[current_y][current_x].has_top_wall = False
					choice.has_bottom_wall = False

			choice.draw_cell()
			self.grid[current_y][current_x].draw_cell()
			self._animate()
			self._break_walls_r(
				choice.grid_coordinate_x, choice.grid_coordinate_y, visited
			)

	def _reset_cells_visited(self):
		for column in self.grid:
			for cell in column:
				cell.visited = False

	def get_cell(self, x: int, y: int):
		return self.grid[y][x]

	def sovle(self) -> bool:
		return self._solve_r(x=0, y=0)

	def _solve_r(self, x: int, y: int) -> bool:
		self._animate()
		if x == self.width-1 and y == self.height-1:
			print("S O L V E D")
			return True
		self.get_cell(x, y).visited = True
		possible_moves = []

		# Define potential moves with directions
		directions = {
			'up': (x, y - 1),
			'down': (x, y + 1),
			'left': (x - 1, y),
			'right': (x + 1, y)
		}

		# Check each direction for wall constraints and boundaries
		for direction, (nx, ny) in directions.items():
			# Ensure we don't go out of bounds
			if 0 <= nx < self.width and 0 <= ny < self.height:
				current_cell = self.get_cell(x,y)
				new_cell = self.get_cell(nx, ny)

				# Check for walls and visited status if required
				if direction == 'up' and not current_cell.has_top_wall and not new_cell.has_bottom_wall:
					if new_cell.visited == False:
						possible_moves.append(new_cell)
				elif direction == 'down' and not current_cell.has_bottom_wall and not new_cell.has_top_wall:
					if new_cell.visited == False:
						possible_moves.append(new_cell)
				elif direction == 'left' and not current_cell.has_left_wall and not new_cell.has_right_wall:
					if new_cell.visited == False:
						possible_moves.append(new_cell)
				elif direction == 'right' and not current_cell.has_right_wall and not new_cell.has_left_wall:
					if new_cell.visited == False:
						possible_moves.append(new_cell)
		
		solved = False
		for move in possible_moves:
			self.get_cell(x,y).draw_move(move)
			if self._solve_r(move.grid_coordinate_x, move.grid_coordinate_y) == True:
				solved = True
			else:
				self.get_cell(x,y).draw_move(move, True)
		
		return solved
			
		""" niggers do what?
		direction_solve_occured = False
		for direction, (nx, ny) in directions.items():
			if self.get_cell(nx, ny) not in possible_moves:
				self.get_cell(nx, ny).draw_move(self.get_cell(x, y), True)
				continue
			self.get_cell(nx, ny).draw_move(self.get_cell(x, y))
			if self._solve_r(nx, ny) == True:
				direction_solve_occured
		return direction_solve_occured
		"""

