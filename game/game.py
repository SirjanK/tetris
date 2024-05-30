from gui.canvas import Canvas
from element.point import Point
import tkinter as tk


def launch_game():
    # Create the main window
    root = tk.Tk()
    root.title("Tetris")

    canvas = Canvas(root)

    # Create an example point
    point = Point(5, 2, "#FF0000")

    canvas.raster_point(point)

    def move_up(event: tk.Event) -> None:
        canvas.translate_point(point, 0, -1)

    def move_down(event: tk.Event) -> None:
        canvas.translate_point(point, 0, 1)

    def move_left(event: tk.Event) -> None:
        canvas.translate_point(point, -1, 0)

    def move_right(event: tk.Event) -> None:
        canvas.translate_point(point, 1, 0)

    def move_to_bottom(event: tk.Event) -> None:
        canvas.move_point(point, point.x, canvas.H - 1)

    canvas.bind_key_listener("<Up>", move_up)
    canvas.bind_key_listener("<Down>", move_down)
    canvas.bind_key_listener("<Left>", move_left)
    canvas.bind_key_listener("<Right>", move_right)
    canvas.bind_key_listener("<space>", move_to_bottom)

    # Run the application
    root.mainloop()
