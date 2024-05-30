import tkinter as tk
from element.point import Point

from typing import Tuple, Callable


class Canvas:
    # Constants for grid dimensions
    H = 20  # Height of the grid
    W = 10  # Width of the grid
    CELL_SIZE = 40  # Size of each cell in pixels
    PADDING = 2  # Padding for rastering points

    def __init__(self, root: tk.Tk):
        self._root = root

        self._canvas = self._init_canvas()

        # boolean bitmap indicating point presence or not
        self._bitmap = []
        for _ in range(self.W):
            bitmap_row = [False] * self.H
            self._bitmap.append(bitmap_row)

    def raster_point(self, point: Point) -> None:
        """
        Raster a new point on the canvas. Note: this will error out if there is already a point at that location

        :param point: point to raster
        """

        assert self._is_inbounds(point.x, point.y), f"point of coordinate {(point.x, point.y)} must be in bounds of the {self.H} by {self.W} grid"

        x1, y1, x2, y2 = self._get_rectangle_coordinates(point.x, point.y)
        point.rectangle = self._canvas.create_rectangle(
            x1, y1, x2, y2, outline=point.color, fill=point.color,
        )

        # update the bitmap
        self._bitmap[point.x][point.y] = True

    def move_point(self, point: Point, x: int, y: int) -> None:
        """
        Move a point already on the canvas
        :param point: point to move
        :param x: x coordinate to move the point
        :param y: y coordinate to move the point

        Raises an exception if you try moving to an out-of-bounds location or an item already exists there
        """

        if not self._is_inbounds(x, y):
            raise Exception(f"{(x, y)} not in range")
        if self._bitmap[x][y]:
            raise Exception(f"{(x, y)} already is occupied")

        # otherwise, execute the move
        x1, y1, x2, y2 = self._get_rectangle_coordinates(x, y)
        self._canvas.coords(point.rectangle, x1, y1, x2, y2)

        self._bitmap[point.x][point.y] = False
        self._bitmap[x][y] = True

        point.x, point.y = x, y

    def translate_point(self, point: Point, delta_x: int, delta_y: int) -> bool:
        """
        Try to translate a point in the direction delta_x, delta_y
        :param point: point to translate
        :param delta_x: delta to move in the x dir
        :param delta_y: delta to move in the y dir
        :return: bool if the translation can go through (in bounds and no item exists there)
        """

        new_x = point.x + delta_x
        new_y = point.y + delta_y

        if not self._is_inbounds(new_x, new_y) or self._bitmap[new_x][new_y]:
            return False

        self._canvas.move(
            point.rectangle,
            delta_x * self.CELL_SIZE,
            delta_y * self.CELL_SIZE,
        )

        self._bitmap[point.x][point.y] = False
        self._bitmap[new_x][new_y] = True

        point.x, point.y = new_x, new_y

        return True

    def bind_key_listener(self, key: str, fn: Callable) -> None:
        """
        Binds a keyboard listener
        :param key: keyboard key
        :param fn: callback function
        """

        self._canvas.bind(key, fn)

    def _get_rectangle_coordinates(self, x: int, y: int) -> Tuple[int, int, int, int]:
        """
        Get the pixel rectangle coordinates given an x, y
        :param x: x coord
        :param y: y coord
        :return: Tuple containing rectangle coordinates (x1, y1, x2, y2)
        """

        x1 = x * self.CELL_SIZE + self.PADDING
        y1 = y * self.CELL_SIZE + self.PADDING
        x2 = (x + 1) * self.CELL_SIZE - self.PADDING
        y2 = (y + 1) * self.CELL_SIZE - self.PADDING

        return x1, y1, x2, y2

    def _is_inbounds(self, x: int, y: int) -> bool:
        """
        Checks if (x, y) coord is in range
        :param x: x to check
        :param y: y to check
        :return: bool indicating whether point is in range or not
        """

        return 0 <= x < self.W and 0 <= y < self.H

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

        canvas.focus_set()

        return canvas
