import tkinter as tk
from tkinter import BOTH, Canvas
import time


class Window:


    def __init__(self, width, height):
        self.__root = tk.Tk()
        self.__root.title("Maze Solver")
    
        self.__canvas = tk.Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack()
        self.running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        # Tkinter is not a reactive framework like React or Vue - we need to tell the window when it should
        # render to visuals
        self.__root.update_idletasks()
        self.__root.update()


    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False


    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)



class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:

    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas, fill_color):

        x1 = self.point1[0]
        y1 = self.point1[1]
        x2 = self.point2[0]
        y2 = self.point2[1]

        canvas.create_line(x1, y1, x2, y2, fill=fill_color, width=2)
        canvas.pack()


class Cell:

    def __init__(self, point1, point2, window):

        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = point1[0]
        self._y1 = point1[1]
        self._x2 = point2[0]
        self._y2 = point2[1]
        self._window = window

    def draw(self):

        # left wall
        if self.has_left_wall:
            line = Line((self._x1, self._y1), (self._x1, self._y2))
            self._window.draw_line(line, "black")

        # top wall
        if self.has_top_wall:
            line = Line((self._x1, self._y1), (self._x2, self._y1))
            self._window.draw_line(line, "black")


        # right wall
        if self.has_right_wall:
            line = Line((self._x2, self._y1), (self._x2, self._y2))
            self._window.draw_line(line, "black")

        # bottom wall
        if self.has_bottom_wall:
            line = Line((self._x1, self._y2), (self._x2, self._y2))
            self._window.draw_line(line, "black")

    def draw_move(self, to_cell, undo=False):

        # from cell mid point
        diff_x1 = self._x2 - self._x1
        diff_y1 = self._y2 - self._y1

        mid_x1 = self._x1 + (diff_x1/2)
        mid_y1 = self._y1 + (diff_y1/2)

        # to cell mid point
        diff_x2 = to_cell._x2 - to_cell._x1
        diff_y2 = to_cell._y2 - to_cell._y1

        mid_x2 = to_cell._x1 + (diff_x2/2)
        mid_y2 = to_cell._y1 + (diff_y2/2)

        # set color
        if undo:
            color = "red"
        else:
            color = "gray"

        line = Line((mid_x1, mid_y1), (mid_x2, mid_y2))
        self._window.draw_line(line, color)



class Maze:


    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win):

        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win

        self._create_cells()


    def _create_cells(self):

        self._cells = []
        cur_x = self.x1
        cur_y = self.y1
        x_offset = self.cell_size_x
        y_offset = self.cell_size_y

        # populate maze with cells
        for i in range(0, self.num_rows):
            cur_x = self.x1
            list = []
            self._cells.append(list)
            cur_y = cur_y + y_offset
            for j in range(0, self.num_cols):
                self._cells[i].append(Cell((cur_x, cur_y), (cur_x+x_offset, cur_y+y_offset), self.win))
                cur_x = cur_x + x_offset
                


        # draw cells

        for i in range(0, len(self._cells)):
            for j in range(0, len(self._cells[i])):

                self._cells[i][j].draw()

                self._animate()

                
    def _animate(self):

        self.win.redraw()
        time.sleep(0.2)




def main():


    win = Window(800, 600)
    # line = Line((200, 200), (300, 300))
    # win.draw_line(line, "black")

    # cell = Cell((200, 200), (300, 300), win)
    # cell.draw()


    # cell2 = Cell((400, 400), (550, 550), win)
    # cell2.has_bottom_wall = False
    # cell2.draw()

    # cell.draw_move(cell2)

    maze = Maze(0, 0, 5, 5, 50, 50, win)




    win.wait_for_close()
    
main()