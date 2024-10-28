from tkinter import Tk, BOTH, Canvas
from Window_class import Window
from Point_class import Point
from Line_class import Line
from Cell_class import Cell
from Maze_class import Maze
def __main__():
	win = Window(800, 600)
	maze = Maze(win, x1=20, y1=20, cell_size_x=25, cell_size_y=25)
	maze.grid[0][0].draw_move(maze.grid[0][1])
	maze.grid[0][0].draw_move(maze.grid[1][0])
	win.wait_for_close()

if __name__ == "__main__":
	__main__()
