import tkinter as tk
from element.point import Point


class Canvas:
    # Constants for grid dimensions
    H = 20  # Height of the grid
    W = 10  # Width of the grid
    CELL_SIZE = 20  # Size of each cell in pixels

    def __init__(self, root: tk.Tk):
        self._root = root

        self._canvas = self._init_canvas()

        # boolean bitmap indicating point presence or not
        self._bitmap = []
        for _ in range(self.W):
            bitmap_row = [False] * self.H
            self._bitmap.append(bitmap_row)

    def raster_point(self, point: Point):
        """
        Raster a new point on the canvas. Note: this will error out if there is already a point at that location

        :param point: point to raster
        """

        pass

    def move_point(self, point: Point, x: int, y: int) -> bool:
        """
        Move a point already on the canvas
        :param point: point to move
        :param x: x coordinate to move the point
        :param y: y coordinate to move the point
        :return boolean flag indicating if the move was successful or not
        """

        pass

    def _init_canvas(self) -> tk.Canvas:
        # Create a canvas widget
        canvas = tk.Canvas(
            self._root,
            width=self.W * self.CELL_SIZE,
            height=self.H * self.CELL_SIZE,
            bg='black')
        canvas.pack()
        # Draw the grid
        grid_color = '#555555'  # Light gray color
        for i in range(self.H + 1):
            canvas.create_line(
                0,
                i * self.CELL_SIZE,
                self.W * self.CELL_SIZE,
                i * self.CELL_SIZE,
                fill=grid_color,
                dash=(2, 2),)
        for j in range(self.W + 1):
            canvas.create_line(
                j * self.CELL_SIZE,
                0,
                j * self.CELL_SIZE,
                self.H * self.CELL_SIZE,
                fill=grid_color,
                dash=(2, 2),)

        return canvas
