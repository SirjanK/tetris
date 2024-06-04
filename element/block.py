from abc import ABC, abstractmethod

from typing import Tuple, List

from element.grid import Grid
from element.point import Point


class Block(ABC):
    """
    The Block class represents a tetris block that we can move
    Each block consists of underlying points and belongs to a grid.
    """

    def __init__(self, grid: Grid):
        """
        Initializes the block
        :param grid: grid this block belongs to
        """

        self._grid = grid

        # list of points
        self._points = []

        color = self.get_color()
        for point_loc in self.get_init_point_locations():
            x, y = point_loc
            self._points.append(Point(x, y, color))

        self._rotation_state = 0  # rotation state modulo 4 (across four possible rotations)

    def activate(self) -> bool:
        """
        Activate the block if possible
        :return: bool flag indicating success
        """

        # iterate through the points and exit if we cannot place any of the points
        for point in self._points:
            if not self._can_place(point.x, point.y):
                return False
        
        # now add all the points
        for point in self._points:
            self._grid.add_point(point)

    def translate(self, dx: int, dy: int) -> bool:
        """
        Translate the block by dx and dy. This only succeeds if all underlying translations succeed
        :param dx: delta to move in x dir
        :param dy: delta to move in y dir
        :return: bool indicating translation success
        """

        return self._translate_with_deltas(deltas=[(dx, dy)] * len(self._points))

    def rotate(self) -> bool:
        """
        Rotate the block 90 deg
        :return: bool indicating rotation success
        """

        deltas = self.get_rotation_deltas()

        return self._translate_with_deltas(deltas)

    def remove(self) -> None:
        """
        Remove the block
        """

        for point in self._points:
            return self._grid.remove(point)

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

    def _can_place(self, x: int, y: int) -> bool:
        """
        Determine if we can place a point in this block to location (x, y).

        This returns True if 
        (x, y) is a valid location AND (
            (x, y) is not occupied OR
            (x, y) is occupied by a point in this block
        )

        :return: can place bool
        """

        if not self._grid.can_add(x, y):
            return False
        
        # get the point
        maybe_point = self._grid.get_point(x, y)

        if maybe_point is None:
            # not occupied
            return True
        
        # otherwise, check if point belongs to this block, if it is we can place
        return maybe_point in self._points
    
    def _translate_with_deltas(self, deltas: List[Tuple[int, int]]) -> bool:
        """
        Translate points according to a passed in deltas list

        :param deltas: list of (dx, dy) of equivalent length to points
        :return: success flag
        """

        assert len(deltas) == len(self._points)

        # check that we can translate all these points
        for point, direction_vector in zip(self._points, deltas):
            dx, dy = direction_vector

            if not self._can_place(point.x + dx, point.y + dy):
                return False
        
        # now, translate
        for point, direction_vector in zip(self._points, deltas):
            dx, dy = direction_vector

            self._grid.translate_point(point, dx, dy)
