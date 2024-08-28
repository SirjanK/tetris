from enum import Enum


class Action(Enum):
    ROTATE = 1
    MOVE_DOWN = 2
    MOVE_LEFT = 3
    MOVE_RIGHT = 4
    MOVE_TO_BOTTOM = 5
    SAVE_BLOCK = 6

    @property
    def binding(self):
        return f"<<{self.name}>>"
