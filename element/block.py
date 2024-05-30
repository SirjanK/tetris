from abc import ABC, abstractmethod

from typing import Tuple, List

from gui.canvas import Canvas
from element.point import Point


class Block(ABC):
    """
    The Block class represents a tetris block that we can move
    Each block consists of underlying points and belongs to a canvas.
    """

    def __init__(self, canvas: Canvas):
        """
        Initializes the block
        :param canvas: canvas this block belongs to
        :param color: color of the block
        """

        self._canvas = canvas

        self._points = []
        color = self.get_color()
        for point_loc in self.get_init_point_locations():
            x, y = point_loc
            self._points.append(Point(x, y, color))

    def raster(self) -> bool:
        """
        Raster the block
        :return: bool flag indicating success
        """

        # iterate through the points to ensure you can raster it
        for point in self._points:
            if not self._canvas.can_raster(point.x, point.y):
                return False

        # now raster it
        for point in self._points:
            self._canvas.raster_point(point)

        return True

    def translate(self, delta_x: int, delta_y: int) -> bool:
        """
        Translate the block by delta_x and delta_y. This only succeeds if all underlying translations succeed
        :param delta_x: delta to move in x dir
        :param delta_y: delta to move in y dir
        :return: bool indicating translation success
        """

        # check that all points can be rastered
        for point in self._points:
            if not self._canvas.can_translate(point, delta_x, delta_y):
                return False

        # now translate all points
        for point in self._points:
            self._canvas.translate_point(point, delta_x, delta_y)

        return True

    def remove(self) -> None:
        """
        Remove the block
        """

        for point in self._points:
            self._canvas.remove_point(point)

    @abstractmethod
    def get_init_point_locations(self) -> List[Tuple[int, int]]:
        """
        Get the initial point locations for this block
        :return: List of tuples containing point coordinates
        """

        raise NotImplementedError()

    @abstractmethod
    def get_color(self) -> str:
        """
        Return the hex color of the block
        :return: hex color
        """

        raise NotImplementedError()
