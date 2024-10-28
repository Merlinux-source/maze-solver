from tkinter import Tk, BOTH, Canvas
from Line_class import Line

class Window:
	def __init__(self, width, height):
		self.__root = Tk();
		self.__root.protocol("WM_DELETE_WINDOW", self.close)
		self.__root.title = "test"
		self.canvas = Canvas(master=self.__root)
		self.window_running = False
		self.canvas.pack(expand=1,fill=BOTH)
	def redraw(self):
		self.__root.update_idletasks()
		self.__root.update()
		return
	def wait_for_close(self):
		self.window_running = True
		while self.window_running == True:
			self.redraw()
	def close(self):
		self.window_running = False

	def draw_line(self, line:Line, fill_color:str):
		"""Draws a line class on the canvas using the given color

		Args:
			line (Line instance class): the line that is to be drawn
			fill_color (str): The color the line should get.
		"""
		line.draw(self.canvas, fill_color=fill_color)