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
from typing import Callable, Optional
from configs import config

from enum import Enum
import tkinter as tk
import random
import threading
import time
import os


class Mode(Enum):
    HUMAN = 1
    SIMULATION = 2


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
    END_EVENT = "<<end>>"
    # binding names for arrow keys during human gameplay
    UP_EVENT = "<Up>"
    DOWN_EVENT = "<Down>"
    LEFT_EVENT = "<Left>"
    RIGHT_EVENT = "<Right>"
    SPACE_EVENT = "<space>"
    SHIFT_EVENT = "<Shift_L>"

    # output paths for metrics
    OUT_DIR = "out/"
    KEYSTROKE_DELTA_FPATH = os.path.join(OUT_DIR, "keystroke_delta_{0}.csv")
    HUMAN_BENCHMARK_FPATH = os.path.join(OUT_DIR, "human_benchmark_{0}.csv")
    SIM_RESULTS_FPATH = os.path.join(OUT_DIR, "sim_results_{0}.csv")


    def __init__(self, mode: Mode, id: str, restart_fn: Callable, log_keystroke_delta: bool = False, human_benchmark_time: float = None):
        """
        Initialize the game

        :param mode: mode to launch tetris
        :param id: id for the game used in outputting metrics
        :param restart_fn: function to restart the game
        :param log_keystroke_delta: whether to log the keystroke delta
        :param human_benchmark_time: time period to log the score and reset the game
        """

        self._mode = mode
        self._id = id

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
        self._keystroke_deltas = None
        self._last_keystroke_time = None
        if log_keystroke_delta:
            # initialize list to store keystroke deltas
            self._keystroke_deltas = []
            # last keystroke time - for now initialize to zero, will be updated in start()
            self._last_keystroke_time = 0
            self._keystroke_delta_fpath = self.KEYSTROKE_DELTA_FPATH.format(self._id)
        self._human_benchmark_time = human_benchmark_time
        self._human_benchmark_fpath = self.HUMAN_BENCHMARK_FPATH.format(self._id)
        self._sim_results_fpath = self.SIM_RESULTS_FPATH.format(self._id)
        self._restart_fn = restart_fn
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
 
        if self._last_keystroke_time is not None:
            # set last keystroke time to current time
            self._last_keystroke_time = time.time()

        self._start_time = time.time()

        # start thread to move down the active block periodically
        self._periodic_thread = threading.Thread(target=self._periodic_move_down)
        self._periodic_thread.daemon = True
        self._periodic_thread.start()

        self._root.mainloop()
    
    def terminate(self, relaunch: bool = False) -> None:
        """
        Terminate the game optionally relaunching it
        """

        self._end_game_state()
        self._shutdown_gui(relaunch=relaunch)
    
    def _periodic_move_down(self) -> None:
        while self._active:
            self._root.event_generate(self.PERIODIC_EVENT, when="tail")

            if self._human_benchmark_time is not None:
                if time.time() - self._start_time >= self._human_benchmark_time:
                    self._root.event_generate(self.END_EVENT, when="tail")
            
            time.sleep(self.MOVE_DOWN_TIME)

    def _bind_keys(self) -> None:
        """
        Helper method to bind keys
        """

        def wrap(fn: Callable):
            if self._last_keystroke_time is None:
                return fn

            def wrapped_fn(event: tk.Event):
                self._record_keystroke_delta()
                fn(event)
            
            return wrapped_fn

        if self._mode == Mode.HUMAN:
            self._grid.bind_key_listener(self.UP_EVENT, wrap(self._rotate))
            self._grid.bind_key_listener(self.DOWN_EVENT, wrap(self._move_down))
            self._grid.bind_key_listener(self.LEFT_EVENT, wrap(self._move_left))
            self._grid.bind_key_listener(self.RIGHT_EVENT, wrap(self._move_right))
            self._grid.bind_key_listener(self.SPACE_EVENT, wrap(self._move_to_bottom))
            self._grid.bind_key_listener(self.SHIFT_EVENT, wrap(self._save_block))
        else:  # sim
            self._grid.bind_key_listener(Action.ROTATE.binding, wrap(self._rotate))
            self._grid.bind_key_listener(Action.MOVE_DOWN.binding, wrap(self._move_down))
            self._grid.bind_key_listener(Action.MOVE_LEFT.binding, wrap(self._move_left))
            self._grid.bind_key_listener(Action.MOVE_RIGHT.binding, wrap(self._move_right))
            self._grid.bind_key_listener(Action.MOVE_TO_BOTTOM.binding, wrap(self._move_to_bottom))
            self._grid.bind_key_listener(Action.SAVE_BLOCK.binding, wrap(self._save_block))
    
    def _record_keystroke_delta(self) -> None:
        """
        Record the keystroke delta
        """

        curr_time = time.time()
        delta = curr_time - self._last_keystroke_time
        self._keystroke_deltas.append(delta)
        self._last_keystroke_time = curr_time

    def _bind_periodic_events(self) -> None:
        """
        Helper method to bind periodic events in the game
        """

        self._root.bind(self.PERIODIC_EVENT, self._move_down)
        self._root.bind(self.END_EVENT, lambda _: self.terminate(relaunch=True))

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
        self._end_game_state()

        # dump keystroke deltas to file
        if self._keystroke_deltas is not None:
            # Create the output directory if it doesn't exist
            os.makedirs(self.OUT_DIR, exist_ok=True)
            
            try:
                with open(self._keystroke_delta_fpath, "w") as f:
                    for delta in self._keystroke_deltas:
                        f.write(f"{delta}\n")
            except IOError as e:
                print(f"Error writing to file: {e}")

        self._canvas.display_game_over(
            start_over_fn=lambda: self._shutdown_gui(relaunch=True),
            score=self._score)
        
    def _end_game_state(self) -> None:
        """
        End the game state
        """

        self._active = False
        self._periodic_thread.join()

        # append score to human benchmark file
        if self._human_benchmark_time is not None:
            with open(self._human_benchmark_fpath, "a") as f:
                f.write(f"{self._score}\n")
    
    def _shutdown_gui(self, relaunch: bool = False) -> None:
        """
        Shutdown the GUI
        """

        self._root.destroy()
        if relaunch:
            self._restart_fn()
    
    def _get_random_block(self) -> Block:
        """
        Get a random block instance
        """

        return random.choice(self.BLOCK_BUILDERS)(self._grid)
