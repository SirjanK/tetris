from abc import ABC, abstractmethod

from typing import Tuple, List, Dict, Set

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

        # check that we can raster this block

        # iterate through the points to ensure you can raster it
        for point in self._points:
            if not self._canvas.can_raster(point.x, point.y) or self._canvas.is_occupied(point.x, point.y):
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

        return self._translate_points([(dx, dy)] * len(self._points))

    def rotate(self) -> bool:
        """
        Rotate the block 90 deg
        :return: bool indicating rotation success
        """

        rotation_deltas = self.get_rotation_deltas()

        return self._translate_points(rotation_deltas)

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

    def _translate_points(self, translation_deltas: List[Tuple[int, int]]) -> bool:
        """
        Translate points based on translation deltas
        :param translation_deltas: list of equivalent length to self._points that correspond to the dx, dy to
        translate each point
        :return: True if can be successfully translated
        """

        assert len(self._points) == len(translation_deltas)

        # create a map from point to delta
        delta_map: Dict[Point, Tuple[int, int]] = {
            self._points[i]: translation_deltas[i] for i in range(len(self._points))
        }

        # check that the block can be translated - we also store the blocks in topological order for the DAG where
        # if point A runs into point B during the translate, we'll make sure to translate point B first
        # edges holds the adjacency list of the DAG holding the translation dependencies
        edges: Dict[Point, List[Point]] = {
            point: [] for point in self._points
        }

        for point in self._points:
            dx, dy = delta_map[point]
            if not self._canvas.can_translate(point, dx, dy):
                # we could not translate
                return False

            next_x, next_y = point.x + dx, point.y + dy
            if not self._canvas.is_occupied(next_x, next_y):
                # not occupied, so continue
                continue

            # get the point in the dx and dy location
            slotted_point = self._canvas.get_point(next_x, next_y)

            if slotted_point not in self._points:
                # occupied by a point not in this block, exit
                return False
            elif slotted_point == point:
                # looks like no delta, so continue
                continue
            else:
                # dependency on another block point - add edge
                edges[point].append(slotted_point)

        # get translation order for the points
        translation_order = self._get_translation_order(edges)

        # now translate all points
        for point in translation_order:
            dx, dy = delta_map[point]
            self._canvas.translate_point(point, dx, dy)

        return True

    @staticmethod
    def _get_translation_order(edges: Dict[Point, List[Point]]) -> List[Point]:
        """
        Get translation order for points given the adjacency list of the DAG containing translation dependencies.
        A translation dependency directed edge A->B occurs when point A's translation needs to come 'after' point
        B's to avoid overwrites. Therefore, we will topologically sort edges and return the reverse order
        :param edges: adjacency list
        :return: List of points of the necessary translation order to avoid conflicts. Raises an exception if
        we detect a cycle in the edges (this should never happen in tetris)
        """

        # container of visited points
        visited: Set[Point] = set()
        order: List[Point] = []

        tmp_visited: Set[Point] = set()

        # helper method to carry out a DFS and populate the topological order
        # return False if we detect a cycle
        def _dfs(vertex: Point) -> bool:
            if vertex in tmp_visited:
                # cycle!!!
                return False

            if vertex in visited:
                # we can terminate
                return True

            order.append(vertex)
            visited.add(vertex)
            tmp_visited.add(vertex)

            for next_point in edges[vertex]:
                if not _dfs(next_point):
                    return False

            tmp_visited.remove(vertex)

            return True

        for point in edges:
            if not _dfs(point):
                raise Exception("CYCLE DETECTED - incorrect translation set")

        return order
