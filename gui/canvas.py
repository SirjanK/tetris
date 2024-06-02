import tkinter as tk
from element.point import Point

from typing import Tuple, Callable


class Canvas:
    """
    The Canvas class manages the grid for tetris and abstracts away the underlying logic with tkinter.
    """

    # Constants for grid dimensions
    H = 21  # Height of the grid
    W = 10  # Width of the grid
    CELL_SIZE = 40  # Size of each cell in pixels
    PADDING = 2  # Padding for rastering points

    def __init__(self, root: tk.Tk):
        self._root = root

        self._canvas = self._init_canvas()

        # occupancies containing number of points in x, y location (for tetris, this is in the range [0, 2]. 2
        # can happen in the intermediate state where we're in the middle of moving an existing block)
        self._occupancies = []
        for _ in range(self.W):
            self._occupancies.append([0] * self.H)

    def raster_point(self, point: Point) -> bool:
        """
        Raster a new point on the canvas. Note: this will error out if there is already a point at that location
        No-op if it cannot raster the point

        :param point: point to raster
        :return: bool indicating raster success
        """

        if not self.can_raster(point.x, point.y):
            return False

        self._create_rectangle(point)

        self._add_occupancy(point)

        return True

    def move_point(self, point: Point, x: int, y: int) -> None:
        """
        Move a point already on the canvas
        :param point: point to move
        :param x: x coordinate to move the point
        :param y: y coordinate to move the point

        No-op if we cannot move
        """

        if not self.can_raster(x, y):
            return None

        # otherwise, execute the move
        x1, y1, x2, y2 = self._get_rectangle_coordinates(x, y)

        self._remove_occupancy(point)
        point.x, point.y = x, y
        self._canvas.coords(point.rectangle, x1, y1, x2, y2)
        self._add_occupancy(point)

    def translate_point(self, point: Point, dx: int, dy: int) -> None:
        """
        Try to translate a point in the direction dx, dy. No-op if we cannot translate
        :param point: point to translate
        :param dx: delta to move in the x dir
        :param dy: delta to move in the y dir
        """

        if not self.can_translate(point, dx, dy):
            return

        self._canvas.move(
            point.rectangle,
            dx * self.CELL_SIZE,
            dy * self.CELL_SIZE,
        )

        new_x = point.x + dx
        new_y = point.y + dy

        self._remove_occupancy(point)
        point.x, point.y = new_x, new_y
        self._add_occupancy(point)

    def remove_point(self, point: Point) -> None:
        """
        Removes a point from the canvas
        :param point: point to remove
        """

        self._canvas.delete(point.rectangle)
        self._remove_occupancy(point)

    def can_translate(self, point: Point, dx: int, dy: int) -> bool:
        """
        Determine if we can translate this point
        :param point: point to translate
        :param dx: delta in x dir
        :param dy: delta in y dir
        :return: bool indicating whether we can translate or not
        """

        new_x = point.x + dx
        new_y = point.y + dy

        return self.can_raster(new_x, new_y)

    def can_raster(self, x: int, y: int) -> bool:
        """
        Determine if we can raster an (x, y) (in bounds and nothing present)
        :param x: x coord
        :param y: y coord
        :return: bool indicating if we can raster or not
        """

        return self._is_inbounds(x, y)

    def is_occupied(self, x: int, y: int) -> bool:
        """
        Determine if the (x, y) point is already occupied
        Raises an error if (x, y) is out of range
        :param x: x coord
        :param y: y coord
        :return: bool indicating if location is occupied or not
        """

        if not self._is_inbounds(x, y):
            raise Exception(f"{x, y} is not in bounds")

        return self._occupancies[x][y] > 0

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

    def _create_rectangle(self, point: Point) -> None:
        """
        Create rectangle for a point
        :param point: point to create rectangle for
        """

        x1, y1, x2, y2 = self._get_rectangle_coordinates(point.x, point.y)
        point.rectangle = self._canvas.create_rectangle(
            x1, y1, x2, y2, outline=point.color, fill=point.color,
        )

    def _is_inbounds(self, x: int, y: int) -> bool:
        """
        Checks if (x, y) coord is in range
        :param x: x to check
        :param y: y to check
        :return: bool indicating whether point is in range or not
        """

        return 0 <= x < self.W and 0 <= y < self.H

    def _init_canvas(self) -> tk.Canvas:
        # Create a frame to act as a viewport
        self.frame = tk.Frame(
            self._root,
            width=self.W * self.CELL_SIZE,
            height=(self.H - 1) * self.CELL_SIZE,
            bg='black'
        )
        self.frame.pack()

        # Create a canvas widget
        canvas = tk.Canvas(
            self._root,
            width=self.W * self.CELL_SIZE,
            height=self.H * self.CELL_SIZE,
            bg='black',
            highlightthickness=0)
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

        # Position the canvas within the frame to hide the top row
        canvas.place(x=0, y=-self.CELL_SIZE)

        canvas.focus_set()

        return canvas

    def _add_occupancy(self, point: Point) -> None:
        """
        Add to point location in occupancies
        :param point: point
        """

        self._occupancies[point.x][point.y] += 1

    def _remove_occupancy(self, point: Point) -> None:
        """
        Subtract point location in occupancies
        :param point: point
        """

        self._occupancies[point.x][point.y] -= 1
