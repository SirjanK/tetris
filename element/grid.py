from gui.canvas import Canvas
from element.point import Point

from typing import Optional, Callable


class Grid:
    """
    The grid class manages points on the board along with the rules of tetris.
    """

    def __init__(self, canvas: Canvas):
        """
        Initializes the grid with a canvas
        """

        self._height = canvas.height
        self._width = canvas.width
        self._canvas = canvas
    
    def add_point(self, point: Point) -> bool:
        """
        Adds a point to the grid

        :param point: point to add
        :return: success flag
        """

        pass

    def move_point(self, point: Point, x: int, y: int) -> bool:
        """
        Moves a point to a location x, y. This will only succeed if
        x, y is a valid location

        :param point: point to move
        :param x: x coord
        :param y: y coord
        :return: success flag
        """

        pass

    def translate_point(self, point: Point, dx: int, dy: int) -> bool:
        """
        Translates a point by dx, dy deltas.

        :param point: point to translate
        :param dx: delta in x dir
        :param dy: delta in y dir
        """

        pass

    def get_point(self, x: int, y: int) -> Optional[Point]:
        """
        Get the point if it exists at location x, y

        :param x: x coord
        :param y: y coord
        :return: Point if it exists at x, y, otherwise None
        """

        pass

    def remove(self, point: Point) -> None:
        """
        Remove the point from the grid
        """

        self._canvas.remove_point(point)

    def clear_rows(self) -> None:
        """
        Clear any full rows on the board
        """

        pass

    def bind_key_listener(self, key: str, fn: Callable) -> None:
        """
        Binds a keyboard listener
        :param key: keyboard key
        :param fn: callback function
        """

        pass

    def can_add(self, x: int, y: int) -> bool:
        """
        Determine if we can add a point at (x, y), i.e. is (x, y) in bounds

        :param x: x coord
        :param y: y coord
        :return: can add flag
        """

        return self._canvas.is_inbounds(x, y)
