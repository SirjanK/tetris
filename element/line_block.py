from element.block import Block
from typing import List, Tuple


class LineBlock(Block):
    def get_init_point_locations(self) -> List[Tuple[int, int]]:
        half_width = self._canvas.W // 2

        return [
            (half_width - 2, 0),
            (half_width - 1, 0),
            (half_width, 0),
            (half_width + 1, 0),
        ]

    def get_color(self) -> str:
        return "#00FFFF"
