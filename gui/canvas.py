import tkinter as tk
from element.point import Point

from typing import Tuple, Callable


class Canvas:
    """
    The Canvas class manages the gui abstracts away the underlying logic with tkinter.
    """

    def __init__(self, root: tk.Tk, height: int, width: int, cell_size: int, padding: int):
        """
        Initialize the Canvas

        :param root: underlying tkinter root instance
        :param height: height of the board (includes one hidden row at the top)
        :param width: width of board
        :param cell_size: cell size for the display
        :param padding: padding between squares on the board
        """

        self._root = root

        self.height = height
        self.width = width

        self._cell_size = cell_size
        self._padding = padding

        self._canvas = self._init_canvas()

    def raster_point(self, point: Point) -> None:
        """
        Raster a new point on the canvas if point is in bounds (returns False otherwise)

        :param point: point to raster
        """

        self._create_rectangle(point)

    def move_point(self, point: Point, x: int, y: int) -> None:
        """
        Move a point already on the canvas
        :param point: point to move
        :param x: x coordinate to move the point
        :param y: y coordinate to move the point
        """

        x1, y1, x2, y2 = self._get_rectangle_coordinates(x, y)
        self._canvas.coords(point.rectangle, x1, y1, x2, y2)

    def translate_point(self, point: Point, dx: int, dy: int) -> None:
        """
        Try to translate a point in the direction dx, dy. No-op if we cannot translate
        :param point: point to translate
        :param dx: delta to move in the x dir
        :param dy: delta to move in the y dir
        """

        self._canvas.move(
            point.rectangle,
            dx * self._cell_size,
            dy * self._cell_size,
        )

    def remove_point(self, point: Point) -> None:
        """
        Removes a point from the canvas
        :param point: point to remove
        """

        self._canvas.delete(point.rectangle)
        point.rectangle = None

    def bind_key_listener(self, key: str, fn: Callable) -> None:
        """
        Binds a keyboard listener
        :param key: keyboard key
        :param fn: callback function
        """

        self._canvas.bind(key, fn)

    def is_inbounds(self, x: int, y: int) -> bool:
        """
        Checks if (x, y) coord is in range
        :param x: x to check
        :param y: y to check
        :return: bool indicating whether point is in range or not
        """

        return 0 <= x < self.width and 0 <= y < self.height
    
    def display_game_over(self, start_over_fn: Callable, score: int):
        """
        Create a game over screen

        :param start_over_fn: function to invoke when pressing the start over btn
        :param score: score to display
        """

        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()
        text_x = canvas_width / 2
        text_y = canvas_height / 2

        # Define the padding around the text
        padding_x = 20
        padding_y = 20

        # Calculate the rectangle's dimensions based on text size and padding
        rect_width = 400  # Adjust as needed
        rect_height = 200  # Adjust as needed

        # Calculate the coordinates for the rectangle
        rect_x1 = text_x - rect_width / 2 - padding_x
        rect_y1 = text_y - padding_y
        rect_x2 = text_x + rect_width / 2 + padding_x
        rect_y2 = text_y + rect_height + padding_y

        # Draw the rectangle with a gray background
        self._canvas.create_rectangle(rect_x1, rect_y1, rect_x2, rect_y2, fill="gray", outline="")

        # Create "Game Over" text
        self._canvas.create_text(text_x, text_y, text="Game Over", font=("Arial", 50), fill="red")

        # Display the score
        self._canvas.create_text(text_x, text_y + 50, text=f"Score: {score}", font=("Arial", 50), fill="red")

        # Create "Start Over" button below the rectangle
        button = tk.Button(self._root, text="Start Over", command=start_over_fn)
        self._canvas.create_window(text_x, text_y + 100, window=button)

    def _create_rectangle(self, point: Point) -> None:
        """
        Create rectangle for a point
        :param point: point to create rectangle for
        """

        x1, y1, x2, y2 = self._get_rectangle_coordinates(point.x, point.y)
        point.rectangle = self._canvas.create_rectangle(
            x1, y1, x2, y2, outline=point.color, fill=point.color,
        )

    def _get_rectangle_coordinates(self, x: int, y: int) -> Tuple[int, int, int, int]:
        """
        Get the pixel rectangle coordinates given an x, y
        :param x: x coord
        :param y: y coord
        :return: Tuple containing rectangle coordinates (x1, y1, x2, y2)
        """

        x1 = x * self._cell_size + self._padding
        y1 = y * self._cell_size + self._padding
        x2 = (x + 1) * self._cell_size - self._padding
        y2 = (y + 1) * self._cell_size - self._padding

        return x1, y1, x2, y2 
 
    def _init_canvas(self) -> tk.Canvas:
        # Create a frame to act as a viewport
        self.frame = tk.Frame(
            self._root,
            width=self.width * self._cell_size,
            height=(self.height - 1) * self._cell_size,
            bg='black'
        )
        self.frame.pack()

        # Create a canvas widget
        canvas = tk.Canvas(
            self._root,
            width=self.width * self._cell_size,
            height=self.height * self._cell_size,
            bg='black',
            highlightthickness=0)
        canvas.pack()
        # Draw the grid
        grid_color = '#555555'  # Light gray color
        for i in range(self.height + 1):
            canvas.create_line(
                0,
                i * self._cell_size,
                self.width * self._cell_size,
                i * self._cell_size,
                fill=grid_color,
                dash=(2, 2),)
        for j in range(self.width + 1):
            canvas.create_line(
                j * self._cell_size,
                0,
                j * self._cell_size,
                self.height * self._cell_size,
                fill=grid_color,
                dash=(2, 2),)

        # Position the canvas within the frame to hide the top row
        canvas.place(x=0, y=-self._cell_size)

        canvas.focus_set()

        return canvas
