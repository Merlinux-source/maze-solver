from Point_class import Point
from Window_class import Window
from Line_class import Line


class Cell:
	"""A cell is a part of the maze which functions as a possible path."""

	def __init__(
		self,
		top_left: Point,
		bottom_right: Point,
		window: Window = None,
		left_wall: bool = False,
		top_wall: bool = False,
		right_wall: bool = False,
		bottom_wall: bool = False,
		color: str = "black",
		grid_coordinate_x: int = 0,
		grid_coordinate_y: int = 0,
	) -> None:
		"""Initialisation function for the cell class, defining every parameter needed.
		   A cell has four walls and four corners, a square should be square but this is not a fix requirement.

		Args:
				top_left (Point): The point at the top left of the cell.
				bottom_right (Point): The point at the bottom right of the cell.
				window (Window): The window on which the cell is renderd and or parented to.
				left_wall (bool): If the cell has a wall to the left.
				top_wall (bool): If the cell has a wall at the top.
				right_wall (bool): If the cell has a wall at the right.
				bottom_wall (bool): If the cell has a wall at the bottom.
				color (str): The default color the cell is renderd in.
		"""
		# Init Walls
		self.has_left_wall = left_wall
		self.has_top_wall = top_wall
		self.has_right_wall = right_wall
		self.has_bottom_wall = bottom_wall
		# Init Position
		self._x1 = top_left.x
		self._x2 = bottom_right.x
		self._y1 = top_left.y
		self._y2 = bottom_right.y
		# Init Grid pos
		self.grid_coordinate_x = grid_coordinate_x
		self.grid_coordinate_y = grid_coordinate_y
		# Init Miscelaneous
		self._win = window
		self.color = color
		self.visited = False

		return

	def draw_cell(self) -> None:
		"""Draws the cell on the canvas (defined in the init methode)"""
		if self._win == None:
			return
		lines = {
			"left": Line(Point(x=self._x1, y=self._y1), Point(x=self._x1, y=self._y2)),
			"top": Line(Point(x=self._x1, y=self._y1), Point(x=self._x2, y=self._y1)),
			"right": Line(Point(x=self._x2, y=self._y1), Point(x=self._x2, y=self._y2)),
			"bottom": Line(
				Point(x=self._x1, y=self._y2), Point(x=self._x2, y=self._y2)
			),
		}
		for line in lines.values():
			self._win.draw_line(line, "#d9d9d9")

		if self.has_left_wall == True:
			self._win.draw_line(
				lines["left"],
				self.color,
			)

		if self.has_top_wall == True:
			self._win.draw_line(
				lines["top"],
				self.color,
			)

		if self.has_right_wall == True:
			self._win.draw_line(
				lines["right"],
				self.color,
			)

		if self.has_bottom_wall == True:
			self._win.draw_line(
				lines["bottom"],
				self.color,
			)
		return

	def draw_move(self, to_cell, undo: bool = False) -> None:
		"""Draws / Undos a move between two cells.

		Args:
				to_cell (Cell): The destination cell. Self is the current therefroe the startpoint of the draw_move methode.
				undo (bool): Undoes the Move by coloring the move red (undone).
		"""
		start_point = Point((self._x1 + self._x2) / 2, (self._y1 + self._y2) / 2)
		end_point = Point(
			(to_cell._x1 + to_cell._x2) / 2, (to_cell._y1 + to_cell._y2) / 2
		)

		if undo == False:
			color = "gray"
		if undo == True:
			color = "red"

		self._win.draw_line(Line(start_point, end_point), color)
