from gui.canvas import Canvas


class Point:
    """
    The Point represents a square on the grid.
    """

    def __init__(self, canvas: Canvas, x: int, y: int, color: str):
        """
        Initializes the point

        :param canvas: canvas this point is contained in
        :param x: x coord
        :param y: y coord
        :param color: color of the Point
        """

        self.canvas = canvas
        self.x = x
        self.y = y
        self.color = color

    def raster(self):
        """
        Raster this point on the canvas
        """

        self.canvas.raster_point(self)

    def move(self, x: int, y: int):
        """
        Move the point on the canvas
        :param x: new x coord
        :param y: new y coord
        """

        if self.canvas.move_point(self, x, y):
            self.x = x
            self.y = y
