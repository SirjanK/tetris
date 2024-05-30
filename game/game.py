from gui.canvas import Canvas
from element.square_block import SquareBlock
import tkinter as tk
import random


def launch_game():
    # Create the main window
    root = tk.Tk()
    root.title("Tetris")

    canvas = Canvas(root)

    # instantiation functions for blocks
    block_builders = [
        lambda: SquareBlock(canvas)
    ]

    block = random.choice(block_builders)()

    block.raster()

    def move_up(event: tk.Event) -> None:
        block.translate(0, -1)

    def move_down(event: tk.Event) -> None:
        nonlocal block
        if not block.translate(0, 1):
            # if we could not translate, delete this block, and assign a new one
            block.remove()
            block = random.choice(block_builders)()
            block.raster()

    def move_left(event: tk.Event) -> None:
        block.translate(-1, 0)

    def move_right(event: tk.Event) -> None:
        block.translate(1, 0)

    canvas.bind_key_listener("<Up>", move_up)
    canvas.bind_key_listener("<Down>", move_down)
    canvas.bind_key_listener("<Left>", move_left)
    canvas.bind_key_listener("<Right>", move_right)
    # canvas.bind_key_listener("<space>", move_to_bottom)

    # Run the application
    root.mainloop()
