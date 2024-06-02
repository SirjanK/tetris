from gui.canvas import Canvas
from element.square_block import SquareBlock
from element.l_block import LBlock
from element.line_block import LineBlock
from element.r_block import RBlock
from element.s_block import SBlock
from element.t_block import TBlock
from element.two_block import TwoBlock
import tkinter as tk
import random


def launch_game():
    # Create the main window
    root = tk.Tk()
    root.title("Tetris")

    canvas = Canvas(root)

    # instantiation functions for blocks
    block_builders = [
        lambda: SquareBlock(canvas),
        lambda: LBlock(canvas),
        lambda: LineBlock(canvas),
        lambda: RBlock(canvas),
        lambda: SBlock(canvas),
        lambda: TBlock(canvas),
        lambda: TwoBlock(canvas),
    ]

    block = random.choice(block_builders)()

    block.raster()

    def rotate(event: tk.Event) -> None:
        block.rotate()

    def move_down(event: tk.Event) -> None:
        nonlocal block
        if not block.translate(0, 1):
            # if we could not translate, assign a new one
            block = random.choice(block_builders)()
            block.raster()

    def move_left(event: tk.Event) -> None:
        block.translate(-1, 0)

    def move_right(event: tk.Event) -> None:
        block.translate(1, 0)

    def move_to_bottom(event: tk.Event) -> None:
        while block.translate(0, 1):
            continue

        move_down(event)

    canvas.bind_key_listener("<Up>", rotate)
    canvas.bind_key_listener("<Down>", move_down)
    canvas.bind_key_listener("<Left>", move_left)
    canvas.bind_key_listener("<Right>", move_right)
    canvas.bind_key_listener("<space>", move_to_bottom)

    # Run the application
    root.mainloop()
