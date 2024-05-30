from gui.canvas import Canvas
from element.point import Point
import tkinter as tk


def launch_game():
    # Create the main window
    root = tk.Tk()
    root.title("Tetris")

    canvas = Canvas(root)

    # Create an example point
    point = Point(7, 12, "#FF0000")

    canvas.raster_point(point)

    # Run the application
    root.mainloop()
