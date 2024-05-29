import tkinter as tk


class Canvas:
    # Constants for grid dimensions
    H = 20  # Height of the grid
    W = 10  # Width of the grid
    CELL_SIZE = 20  # Size of each cell in pixels

    def __init__(self, root: tk.Tk):
        self._root = root

    def draw_canvas(self) -> tk.Canvas:
        # Create a canvas widget
        canvas = tk.Canvas(
            self._root,
            width=self.W * self.CELL_SIZE,
            height=self.H * self.CELL_SIZE,
            bg='black')
        canvas.pack()

        # Draw the grid
        grid_color = '#555555'  # Light gray color
        for i in range(self.H + 1):
            canvas.create_line(
                0,
                i * self.CELL_SIZE,
                self.W * self.CELL_SIZE,
                i * self.CELL_SIZE,
                fill=grid_color,
                dash=(2, 2),)
        for j in range(self.W + 1):
            canvas.create_line(
                j * self.CELL_SIZE,
                0,
                j * self.CELL_SIZE,
                self.H * self.CELL_SIZE,
                fill=grid_color,
                dash=(2, 2),)

        return canvas
