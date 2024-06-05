import tkinter as tk
from element.point import Point

from typing import Tuple, Callable


class Canvas:
    """
    The Canvas class manages the gui abstracts away the underlying logic with tkinter.
    """

    def __init__(self, root: tk.Tk, height: int, width: int, cell_size: int, padding: int):
        """
        Initialize the Canvas

        :param root: underlying tkinter root instance
        :param height: height of the board (includes one hidden row at the top)
        :param width: width of board
        :param cell_size: cell size for the display
        :param padding: padding between squares on the board
        """

        self._root = root

        self.height = height
        self.width = width

        self._cell_size = cell_size
        self._padding = padding

        self._canvas = self._init_canvas()

    def raster_point(self, point: Point) -> bool:
        """
        Raster a new point on the canvas if point is in bounds (returns False otherwise)

        :param point: point to raster
        :return: bool indicating raster success
        """

        if not self.is_inbounds(point.x, point.y):
            return False

        self._create_rectangle(point)

        return True

    def move_point(self, point: Point, x: int, y: int) -> bool:
        """
        Move a point already on the canvas
        :param point: point to move
        :param x: x coordinate to move the point
        :param y: y coordinate to move the point

        No-op if we cannot move

        :return: true if success, false otherwise
        """

        if not self.is_inbounds(x, y) or point.rectangle is None:
            return False

        # otherwise, execute the move
        x1, y1, x2, y2 = self._get_rectangle_coordinates(x, y)
        self._canvas.coords(point.rectangle, x1, y1, x2, y2)

    def translate_point(self, point: Point, dx: int, dy: int) -> bool:
        """
        Try to translate a point in the direction dx, dy. No-op if we cannot translate
        :param point: point to translate
        :param dx: delta to move in the x dir
        :param dy: delta to move in the y dir

        :return: true if we can translate, false ow
        """

        if not self.is_inbounds(point.x + dx, point.y + dy):
            return

        self._canvas.move(
            point.rectangle,
            dx * self._cell_size,
            dy * self._cell_size,
        )

    def remove_point(self, point: Point) -> None:
        """
        Removes a point from the canvas
        :param point: point to remove
        """

        self._canvas.delete(point.rectangle)
        point.rectangle = None

    def bind_key_listener(self, key: str, fn: Callable) -> None:
        """
        Binds a keyboard listener
        :param key: keyboard key
        :param fn: callback function
        """

        self._canvas.bind(key, fn)

    def is_inbounds(self, x: int, y: int) -> bool:
        """
        Checks if (x, y) coord is in range
        :param x: x to check
        :param y: y to check
        :return: bool indicating whether point is in range or not
        """

        return 0 <= x < self.width and 0 <= y < self.height
    
    def _create_rectangle(self, point: Point) -> None:
        """
        Create rectangle for a point
        :param point: point to create rectangle for
        """

        x1, y1, x2, y2 = self._get_rectangle_coordinates(point.x, point.y)
        point.rectangle = self._canvas.create_rectangle(
            x1, y1, x2, y2, outline=point.color, fill=point.color,
        )

    def _get_rectangle_coordinates(self, x: int, y: int) -> Tuple[int, int, int, int]:
        """
        Get the pixel rectangle coordinates given an x, y
        :param x: x coord
        :param y: y coord
        :return: Tuple containing rectangle coordinates (x1, y1, x2, y2)
        """

        x1 = x * self._cell_size + self._padding
        y1 = y * self._cell_size + self._padding
        x2 = (x + 1) * self._cell_size - self._padding
        y2 = (y + 1) * self._cell_size - self._padding

        return x1, y1, x2, y2 
 
    def _init_canvas(self) -> tk.Canvas:
        # Create a frame to act as a viewport
        self.frame = tk.Frame(
            self._root,
            width=self.width * self._cell_size,
            height=(self.height - 1) * self._cell_size,
            bg='black'
        )
        self.frame.pack()

        # Create a canvas widget
        canvas = tk.Canvas(
            self._root,
            width=self.width * self._cell_size,
            height=self.height * self._cell_size,
            bg='black',
            highlightthickness=0)
        canvas.pack()
        # Draw the grid
        grid_color = '#555555'  # Light gray color
        for i in range(self.height + 1):
            canvas.create_line(
                0,
                i * self._cell_size,
                self.width * self._cell_size,
                i * self._cell_size,
                fill=grid_color,
                dash=(2, 2),)
        for j in range(self.width + 1):
            canvas.create_line(
                j * self._cell_size,
                0,
                j * self._cell_size,
                self.height * self._cell_size,
                fill=grid_color,
                dash=(2, 2),)

        # Position the canvas within the frame to hide the top row
        canvas.place(x=0, y=-self._cell_size)

        canvas.focus_set()

        return canvas
