from gui.canvas import Canvas
from element.block import Block
from element.tetris_blocks import (
    SquareBlock,
    LBlock,
    LineBlock,
    RBlock,
    SBlock,
    TBlock,
    TwoBlock,
)
import tkinter as tk
import random


class Game:
    """
    Manages a single game session.
    """

    # instantiation functions for blocks
    BLOCK_BUILDERS = [
        lambda canvas: SquareBlock(canvas),
        lambda canvas: LBlock(canvas),
        lambda canvas: LineBlock(canvas),
        lambda canvas: RBlock(canvas),
        lambda canvas: SBlock(canvas),
        lambda canvas: TBlock(canvas),
        lambda canvas: TwoBlock(canvas),
    ]

    def __init__(self):
        self.score = 0

        self._root = tk.Tk()
        self._root.title("Tetris")

        self._canvas = Canvas(self._root)

        # initial block
        self._active_block = self._get_random_block()

        # key bindings
        self._bind_keys()

    def start(self) -> None:
        """
        Start the game
        """

        self._active_block.raster()

        self._root.mainloop()

    def _bind_keys(self) -> None:
        """
        Helper method to bind keys
        """

        self._canvas.bind_key_listener("<Up>", self._rotate)
        self._canvas.bind_key_listener("<Down>", self._move_down)
        self._canvas.bind_key_listener("<Left>", self._move_left)
        self._canvas.bind_key_listener("<Right>", self._move_right)
        self._canvas.bind_key_listener("<space>", self._move_to_bottom)

    def _rotate(self, event: tk.Event) -> None:
        """
        Rotate the active block
        :param event: event
        """

        self._active_block.rotate()

    def _move_down(self, event: tk.Event) -> None:
        """
        Move down the active block
        :param event: event
        """

        if not self._active_block.translate(dx=0, dy=1):
            # if we could not translate, assign a new one
            # TODO revisit this logic after we implement timer
            self._next_block_state()

    def _move_left(self, event: tk.Event) -> None:
        """
        Move left the active block
        :param event: event
        """

        self._active_block.translate(dx=-1, dy=0)

    def _move_right(self, event: tk.Event) -> None:
        """
        Move right the active block
        :param event: event
        """

        self._active_block.translate(dx=1, dy=0)

    def _move_to_bottom(self, event: tk.Event) -> None:
        """
        Move to the bottom the active block
        :param event: event
        """

        while self._active_block.translate(dx=0, dy=1):
            continue

        # to trigger reset
        self._move_down(event)

    def _next_block_state(self) -> None:
        """
        Start the next block state
        """

        # self._canvas.clear_rows()
        self._active_block = self._get_random_block()
        self._active_block.raster()

    def _get_random_block(self) -> Block:
        """
        Get a random block instance
        """

        return random.choice(self.BLOCK_BUILDERS)(self._canvas)


def launch_game():
    game = Game()

    game.start()
