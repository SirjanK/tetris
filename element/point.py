class Point:
    """
    The Point represents a square on the grid.
    """

    def __init__(self, x: int, y: int, color: str):
        """
        Initializes the point

        :param x: x coord
        :param y: y coord
        :param color: color of the Point
        """

        self.x = x
        self.y = y
        self.color = color

        # Underlying rectangle for the point. This will be updated once the point is rastered
        self.rectangle = None
