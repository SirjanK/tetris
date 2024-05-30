from abc import ABC

import tkinter as tk
from gui.canvas import Canvas


class Block(ABC):
    """
    The Block class represents a tetris block that we can move
    Each block consists of underlying rectangles and belongs to a canvas. This is all abstracted away to the user.
    """

    CELL_SIZE = Canvas.CELL_SIZE

    def __init__(self, canvas: tk.Canvas):
        self._canvas = canvas
