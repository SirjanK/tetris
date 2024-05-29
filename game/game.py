from gui.canvas import Canvas
import tkinter as tk


def launch_game():
    # Create the main window
    root = tk.Tk()
    root.title("Tetris")

    canvas = Canvas(root)

    canvas.draw_canvas()

    # Run the application
    root.mainloop()
