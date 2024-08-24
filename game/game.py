from gui.canvas import Canvas
from element.grid import Grid
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
from configs import config

import tkinter as tk
import random
import threading
import time


class Game:
    """
    Manages a single game session.
    """

    GAME_TITLE = "Tetris"

    # instantiation functions for blocks
    BLOCK_BUILDERS = [
        lambda grid: SquareBlock(grid),
        lambda grid: LBlock(grid),
        lambda grid: LineBlock(grid),
        lambda grid: RBlock(grid),
        lambda grid: SBlock(grid),
        lambda grid: TBlock(grid),
        lambda grid: TwoBlock(grid),
    ]

    # array of points gotten for number of rows cleared
    POINTS = [0, 1, 3, 5, 8]

    # seconds to move the active block down
    MOVE_DOWN_TIME = 1

    # event name for periodic events
    PERIODIC_EVENT = "<<periodic>>"
    # other binding names
    UP_EVENT = "<Up>"
    DOWN_EVENT = "<Down>"
    LEFT_EVENT = "<Left>"
    RIGHT_EVENT = "<Right>"
    SPACE_EVENT = "<space>"
    SHIFT_EVENT = "<Shift_L>"

    def __init__(self):
        self._score = 0

        self._root = tk.Tk()
        self._root.title(self.GAME_TITLE)

        self._canvas = Canvas(
            root=self._root,
            height=config.HEIGHT,
            width=config.WIDTH,
            cell_size=config.CELL_SIZE,
            padding=config.PADDING,
        )

        self._grid = Grid(self._canvas)
        self._active = False
        # initial block
        self._active_block = self._get_random_block()
        # saved block
        self._saved_block = None
        # key bindings
        self._bind_keys()
        # event bindings
        self._bind_periodic_events()

    def start(self) -> None:
        """
        Start the game
        """

        self._active = True
        self._active_block.activate()

        # start thread to move down the active block periodically
        periodic_thread = threading.Thread(target=self._periodic_move_down)
        periodic_thread.daemon = True
        periodic_thread.start()

        self._root.mainloop()
            
    def _periodic_move_down(self) -> None:
        while self._active:
            time.sleep(self.MOVE_DOWN_TIME)
            self._root.event_generate(self.PERIODIC_EVENT, when="tail")

    def _bind_keys(self) -> None:
        """
        Helper method to bind keys
        """

        self._grid.bind_key_listener(self.UP_EVENT, self._rotate)
        self._grid.bind_key_listener(self.DOWN_EVENT, self._move_down)
        self._grid.bind_key_listener(self.LEFT_EVENT, self._move_left)
        self._grid.bind_key_listener(self.RIGHT_EVENT, self._move_right)
        self._grid.bind_key_listener(self.SPACE_EVENT, self._move_to_bottom)
        self._grid.bind_key_listener(self.SHIFT_EVENT, self._save_block)

    def _bind_periodic_events(self) -> None:
        """
        Helper method to bind periodic events in the game
        """

        self._root.bind("<<periodic>>", self._move_down)

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

        self._move_down_impl()

    def _move_down_impl(self) -> bool:
        """
        Helper function to move down the active block

        :return: bool that indicates whether we could translate or not
        """

        if not self._active_block.translate(dx=0, dy=1):
            # if we could not translate, assign a new one
            self._settle_block()
            return False

        return True

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

        while self._move_down_impl():
            continue
    
    def _save_block(self, event: tk.Event) -> None:
        curr_saved_block, self._saved_block = self._saved_block, self._active_block

        # remove saved block and reset its state
        self._saved_block.remove()
        self._saved_block.reset()

        if curr_saved_block is None:
            # start next block state
            self._next_block_state()
        else:
            # set next active block as the saved block
            self._active_block = curr_saved_block

            # activate the block
            self._active_block.activate()
    
    def _settle_block(self) -> None:
        """
        Settle the block after being placed
        """

        num_rows_cleared = self._grid.clear_full_rows()
        self._score += self.POINTS[num_rows_cleared]

        self._next_block_state()

    def _next_block_state(self) -> None:
        """
        Start the next block state
        """

        self._active_block = self._get_random_block()
        if not self._active_block.activate():
            # game is over
            self._end_game()
    
    def _end_game(self) -> None:
        def end_game_and_relaunch():
            self._root.destroy()
            launch_game()

        self._active = False
        self._canvas.display_game_over(
            start_over_fn=end_game_and_relaunch,
            score=self._score)

    def _get_random_block(self) -> Block:
        """
        Get a random block instance
        """

        return random.choice(self.BLOCK_BUILDERS)(self._grid)


def launch_game():
    game = Game()
    game.start()
