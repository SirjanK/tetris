from gui.canvas import Canvas
from element.point import Point

from typing import Optional, Callable, List, Dict, Tuple


class Grid:
    """
    The grid class manages points on the board along with the rules of tetris.
    """

    def __init__(self, canvas: Canvas):
        """
        Initializes the grid with a canvas
        """

        self.height = canvas.height
        self.width = canvas.width
        self._canvas = canvas

        # container for points at a location (H x W matrix)
        self._points: List[List[Optional[Point]]] = []
        # row counts
        self._row_counts: List[int] = []

        for _ in range(self.height):
            self._row_counts.append(0)
            self._points.append([None] * self.width)

    def add_point(self, point: Point) -> bool:
        """
        Adds a point to the grid

        :param point: point to add
        :return: success flag
        """

        if not self.can_place(point.x, point.y):
            return False
        
        # otherwise, add
        self._add_occupancy(point)
        self._canvas.raster_point(point)
        
        return True
 
    def get_point(self, x: int, y: int) -> Optional[Point]:
        """
        Get the point if it exists at location x, y

        :param x: x coord
        :param y: y coord
        :return: Point if it exists at x, y, otherwise None
        """

        if not self._canvas.is_inbounds(x, y):
            raise Exception(f"Point coordinates {x, y} is not in bounds")

        return self._points[y][x]

    def remove(self, point: Point) -> None:
        """
        Remove the point from the grid
        """

        if self.get_point(point.x, point.y) != point:
            raise Exception("Point does not exist")

        self._remove_occupancy(point)
        self._canvas.remove_point(point)
    
    def batch_move(self, point_locations: Dict[Point, Tuple[int, int]]) -> bool:
        """
        Batch move points to new locations

        Raises an exception if any point locations are the same

        :param point_locations: map from point to new location
        :return: success flag
        """

        # validate uniqueness of point locations
        assert len(set(point_locations.items())) == len(point_locations), \
            f"Passed in point locations contains duplicates: {point_locations.items()}"
        
        # otherwise, we can move!
        # first, remove from old locations
        for point in point_locations:
            self._remove_occupancy(point)
        
        # next, verify we can place all the points
        invalid = False
        for loc in point_locations.values():
            x, y = loc
            if not self.can_place(x, y):
                invalid = True
                break
        
        if invalid:
            # add back all the points
            for point in point_locations:
                self._add_occupancy(point)

            return False
        
        # now, add to the new locations and execute the move
        for point, loc in point_locations.items():
            point.x, point.y = loc
            self._add_occupancy(point)
            self._canvas.move_point(point, point.x, point.y)
        
        return True

    def batch_translate(self, point_deltas: Dict[Point, Tuple[int, int]]) -> bool:
        """
        Batch translates points to new locations

        Raises an exception if any point locations are the same

        :param point_deltas: map from point to deltas (dx, dy) to translate by
        :return: success flag
        """

        pass

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

        self._canvas.bind_key_listener(key, fn)

    def can_place(self, x: int, y: int) -> bool:
        """
        Determine if we can place a point at (x, y), i.e. is (x, y) in bounds and
        not occupied

        :param x: x coord
        :param y: y coord
        :return: can place flag
        """

        return self._canvas.is_inbounds(x, y) and self.get_point(x, y) is None
    
    def _add_occupancy(self, point: Point) -> None:
        """
        Add point to occupancy data structures

        :param point: point to add
        """

        self._points[point.y][point.x] = point
        self._row_counts[point.y] += 1

    def _remove_occupancy(self, point: Point) -> None:
        """
        Remove point from occupancy data structures.

        :param point: point to remove
        """

        self._points[point.y][point.x] = None
        self._row_counts[point.y] -= 1
