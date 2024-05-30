from gui.canvas import Canvas
from element.square_block import SquareBlock
import tkinter as tk


def launch_game():
    # Create the main window
    root = tk.Tk()
    root.title("Tetris")

    canvas = Canvas(root)

    # Create an example point
    block = SquareBlock(canvas, "#FF0000")

    block.raster()

    def move_up(event: tk.Event) -> None:
        block.translate(0, -1)

    def move_down(event: tk.Event) -> None:
        block.translate(0, 1)

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
