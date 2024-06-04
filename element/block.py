from abc import ABC, abstractmethod

from typing import Tuple, List, Dict, Set

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

    def raster(self) -> bool:
        """
        Raster the block
        :return: bool flag indicating success
        """

        pass

    def translate(self, dx: int, dy: int) -> bool:
        """
        Translate the block by dx and dy. This only succeeds if all underlying translations succeed
        :param dx: delta to move in x dir
        :param dy: delta to move in y dir
        :return: bool indicating translation success
        """

        pass

    def rotate(self) -> bool:
        """
        Rotate the block 90 deg
        :return: bool indicating rotation success
        """

        pass

    def remove(self) -> None:
        """
        Remove the block
        """

        pass

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
