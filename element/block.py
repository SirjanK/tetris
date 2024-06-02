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
        """

        self._canvas = canvas

        # list of points
        self._points = []

        color = self.get_color()
        for point_loc in self.get_init_point_locations():
            x, y = point_loc
            self._points.append(Point(x, y, color))

        self._rotation_state = 0  # rotation state modulo 4 (across four possible rotations)

    def raster(self) -> bool:
        """
        Raster the block
        :return: bool flag indicating success
        """

        # iterate through the points to ensure you can raster it
        for point in self._points:
            if not self._can_raster(point):
                return False

        # now raster it
        for point in self._points:
            self._canvas.raster_point(point)

        return True

    def translate(self, dx: int, dy: int) -> bool:
        """
        Translate the block by dx and dy. This only succeeds if all underlying translations succeed
        :param dx: delta to move in x dir
        :param dy: delta to move in y dir
        :return: bool indicating translation success
        """

        # check that all points can be translated
        for point in self._points:
            if not self._can_translate(point, dx, dy):
                return False

        # now translate all points
        for point in self._points:
            self._canvas.translate_point(point, dx, dy)

        return True

    def rotate(self) -> bool:
        """
        Rotate the block 90 deg
        :return: bool indicating rotation success
        """

        rotation_deltas = self.get_rotation_deltas()

        # check that all points can be translated
        for (point, deltas) in zip(self._points, rotation_deltas):
            dx, dy = deltas
            if not self._can_translate(point, dx, dy):
                return False

        # now translate all points
        for (point, deltas) in zip(self._points, rotation_deltas):
            dx, dy = deltas
            self._canvas.translate_point(point, dx, dy)

        self._rotation_state = (self._rotation_state + 1) % 4

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
    def get_rotation_deltas(self) -> List[Tuple[int, int]]:
        """
        Get translation deltas for each block after rotating by 90 degrees
        :return: List of dx, dy
        """

        raise NotImplementedError()

    @abstractmethod
    def get_color(self) -> str:
        """
        Return the hex color of the block
        :return: hex color
        """

        raise NotImplementedError()

    def _can_raster(self, point: Point) -> bool:
        """
        Helper method to determine if we can raster a point
        Checks,
          1. Can the location be rastered?
          2. Is the location not occupied? However, it can be occupied by other points belonging to the block
        :param point: point to check
        :return: bool indicating if we can place a point belonging to this block at this location
        """

        return self._canvas.can_raster(point.x, point.y) and self._is_loc_free(point.x, point.y)

    def _can_translate(self, point: Point, dx: int, dy: int) -> bool:
        """
        Helper method to determine if we can translate a point by some (dx, dy)
        :param point: point to check
        :param dx: delta in x dir
        :param dy: delta in y dir
        :return: bool indicating if we can translate a point belonging to this block at this location
        """

        return self._canvas.can_translate(point, dx, dy) and self._is_loc_free(point.x + dx, point.y + dy)

    def _is_loc_free(self, x: int, y: int) -> bool:
        """
        Helper method to determine if the (x, y) loc is free for this block.
        It checks if the canvas has marked this location as occupied but also that this location isn't already part
        of this block's points
        :param x: x coord
        :param y: y coord
        :return: bool indicating if (x, y) loc is free for this block
        """

        if not self._canvas.is_occupied(x, y):
            return True

        # otherwise, iterate through the points to see if x, y matches any of the locations
        # we could have used a set to store locations, but that adds unnecessary overhead when len(points) == 4
        loc = (x, y)
        for point in self._points:
            if loc == (point.x, point.y):
                return True

        return False
