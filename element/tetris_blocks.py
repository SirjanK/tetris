from element.block import Block
from typing import List, Tuple


class LBlock(Block):
    def get_init_point_locations(self) -> List[Tuple[int, int]]:
        half_width = self._canvas.W // 2

        return [
            (half_width - 2, 0),
            (half_width - 2, 1),
            (half_width - 1, 1),
            (half_width, 1),
        ]

    def get_rotation_deltas(self) -> List[Tuple[int, int]]:
        if self._rotation_state == 0:
            return [
                (2, 0),
                (1, -1),
                (0, 0),
                (-1, 1),
            ]
        elif self._rotation_state == 1:
            return [
                (0, 2),
                (1, 1),
                (0, 0),
                (-1, -1),
            ]
        elif self._rotation_state == 2:
            return [
                (-2, 0),
                (-1, 1),
                (0, 0),
                (1, -1)
            ]
        elif self._rotation_state == 3:
            return [
                (0, -2),
                (-1, -1),
                (0, 0),
                (1, 1),
            ]

    def get_color(self) -> str:
        return "#0000FF"


class LineBlock(Block):
    def get_init_point_locations(self) -> List[Tuple[int, int]]:
        half_width = self._canvas.W // 2

        return [
            (half_width - 2, 1),
            (half_width - 1, 1),
            (half_width, 1),
            (half_width + 1, 1),
        ]

    def get_rotation_deltas(self) -> List[Tuple[int, int]]:
        if self._rotation_state == 0 or self._rotation_state == 2:
            return [
                (2, -2),
                (1, -1),
                (0, 0),
                (-1, 1),
            ]
        else:
            return [
                (-2, 2),
                (-1, 1),
                (0, 0),
                (1, -1),
            ]

    def get_color(self) -> str:
        return "#00FFFF"


class RBlock(Block):
    def get_init_point_locations(self) -> List[Tuple[int, int]]:
        half_width = self._canvas.W // 2

        return [
            (half_width - 2, 1),
            (half_width - 1, 1),
            (half_width, 1),
            (half_width, 0),
        ]

    def get_rotation_deltas(self) -> List[Tuple[int, int]]:
        if self._rotation_state == 0:
            return [
                (1, -1),
                (0, 0),
                (-1, 1),
                (0, 2),
            ]
        elif self._rotation_state == 1:
            return [
                (1, 1),
                (0, 0),
                (-1, -1),
                (-2, 0),
            ]
        elif self._rotation_state == 2:
            return [
                (-1, 1),
                (0, 0),
                (1, -1),
                (0, -2),
            ]
        elif self._rotation_state == 3:
            return [
                (-1, -1),
                (0, 0),
                (1, 1),
                (2, 0),
            ]

    def get_color(self) -> str:
        return "#FF7F00"


class SBlock(Block):
    def get_init_point_locations(self) -> List[Tuple[int, int]]:
        half_width = self._canvas.W // 2

        return [
            (half_width - 2, 1),
            (half_width - 1, 1),
            (half_width - 1, 0),
            (half_width, 0),
        ]

    def get_rotation_deltas(self) -> List[Tuple[int, int]]:
        if self._rotation_state == 0 or self._rotation_state == 2:
            return [
                (1, -2),
                (0, -1),
                (1, 0),
                (0, 1),
            ]
        else:
            return [
                (-1, 2),
                (0, 1),
                (-1, 0),
                (0, -1),
            ]

    def get_color(self) -> str:
        return "#00FF00"


class SquareBlock(Block):
    def get_init_point_locations(self) -> List[Tuple[int, int]]:
        half_width = self._canvas.W // 2

        return [
            (half_width - 1, 0),
            (half_width, 0),
            (half_width - 1, 1),
            (half_width, 1),
        ]

    def get_rotation_deltas(self) -> List[Tuple[int, int]]:
        return [(0, 0)] * 4

    def get_color(self) -> str:
        return "#FFFF00"


class TBlock(Block):
    def get_init_point_locations(self) -> List[Tuple[int, int]]:
        half_width = self._canvas.W // 2

        return [
            (half_width - 2, 1),
            (half_width - 1, 1),
            (half_width - 1, 0),
            (half_width, 1),
        ]

    def get_rotation_deltas(self) -> List[Tuple[int, int]]:
        if self._rotation_state == 0:
            return [
                (1, -1),
                (0, 0),
                (1, 1),
                (-1, 1),
            ]
        elif self._rotation_state == 1:
            return [
                (1, 1),
                (0, 0),
                (-1, 1),
                (-1, -1),
            ]
        elif self._rotation_state == 2:
            return [
                (-1, 1),
                (0, 0),
                (-1, -1),
                (1, -1),
            ]
        elif self._rotation_state == 3:
            return [
                (-1, -1),
                (0, 0),
                (1, -1),
                (1, 1),
            ]

    def get_color(self) -> str:
        return "#800080"


class TwoBlock(Block):
    def get_init_point_locations(self) -> List[Tuple[int, int]]:
        half_width = self._canvas.W // 2

        return [
            (half_width - 2, 0),
            (half_width - 1, 0),
            (half_width - 1, 1),
            (half_width, 1),
        ]

    def get_rotation_deltas(self) -> List[Tuple[int, int]]:
        if self._rotation_state == 0 or self._rotation_state == 2:
            return [
                (2, -1),
                (1, 0),
                (0, -1),
                (-1, 0),
            ]
        else:
            return [
                (-2, 1),
                (-1, 0),
                (0, 1),
                (1, 0),
            ]

    def get_color(self) -> str:
        return "#FF0000"
