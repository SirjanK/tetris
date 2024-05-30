from element.block import Block
from typing import List, Tuple


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