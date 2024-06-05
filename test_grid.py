from gui.canvas import Canvas
from element.grid import Grid
from element.point import Point
from configs import config

from typing import Callable

from overrides import override


# TODO replace this with a mock library
class MockCanvas(Canvas):
    """
    A mock canvas used for testing
    """

    @override
    def raster_point(self, point: Point) -> bool:
        return True
    
    @override
    def move_point(self, point: Point, x: int, y: int) -> bool:
        return True
    
    @override
    def translate_point(self, point: Point, dx: int, dy: int) -> bool:
        return True

    @override
    def remove_point(self, point: Point) -> None:
        return True
    

def create_grid() -> Grid:
    canvas = MockCanvas(
        root=None, 
        height=config.HEIGHT, 
        width=config.WIDTH,
        cell_size=config.CELL_SIZE,
        padding=config.PADDING)

    return Grid(canvas)


def test_can_place():
    grid = create_grid()

    assert grid.can_place(4, 13)
    assert grid.can_place(0, 0)
    assert grid.can_place(9, 20)
    assert not grid.can_place(-1, 0)
    assert not grid.can_place(0, -1)
    assert not grid.can_place(10, 20)
    assert not grid.can_place(9, 21)

    print("test_can_place success!")


def test_add_get_remove():
    grid = create_grid()

    # add 6 points, 3 neighboring each other
    # add 1 replacing another
    points = [
        Point(x=4, y=5, color='red'),
        Point(x=7, y=13, color='orange'),
        Point(x=7, y=12, color='yellow'),
        Point(x=6, y=13, color='green'),
        Point(x=2, y=17, color='blue'),
        Point(x=3, y=20, color='indigo'),
    ]

    for point in points:
        assert grid.add_point(point)
    
    # assert adding out of bounds returns False
    assert not grid.add_point(Point(x=10, y=20, color='gray'))
    # assert adding to an already occupied location returns False
    assert not grid.add_point(Point(x=6, y=13, color='green'))
    assert not grid.add_point(Point(x=6, y=13, color='gray'))

    # test get all return the appropriate point
    assert grid.get_point(4, 5) == points[0]
    assert grid.get_point(7, 13) == points[1]
    assert grid.get_point(7, 12) == points[2]
    assert grid.get_point(6, 13) == points[3]
    assert grid.get_point(2, 17) == points[4]
    assert grid.get_point(3, 20) == points[5]

    assert grid.get_point(0, 0) is None
    assert grid.get_point(7, 15) is None

    assert _is_error_caught(lambda: grid.get_point(10, 20))

    # test removing three of the points
    grid.remove(points[1])
    grid.remove(points[4])
    grid.remove(points[5])

    # assert we catch an error if we try to remove an unavailable point
    assert _is_error_caught(lambda: grid.remove(Point(x=6, y=13, color='gray')))

    # test get works
    assert grid.get_point(4, 5) == points[0]
    assert grid.get_point(7, 13) == None
    assert grid.get_point(7, 12) == points[2]
    assert grid.get_point(6, 13) == points[3]
    assert grid.get_point(2, 17) == None
    assert grid.get_point(3, 20) == None

    assert grid.get_point(0, 0) is None
    assert grid.get_point(7, 15) is None

    # test adding one back into removed spot
    new_point = Point(x=7, y=13, color='gray')
    assert grid.add_point(new_point)

    # test get works for that
    assert grid.get_point(7, 13) == new_point

    print("test_add_get_remove success!")


def test_move():
    grid = create_grid()
    print("test_move success!")


def test_translate():
    grid = create_grid()
    print("test_translate success!")


def test_clear_rows_single():
    grid = create_grid()
    print("test_clear_rows_single success!")


def test_clear_rows_top():
    grid = create_grid()
    print("test_clear_rows_top success!")


def test_clear_rows_multiple():
    grid = create_grid()
    print("test_clear_rows_multiple success!")


def _is_error_caught(fn: Callable):
    try:
        fn()
    except Exception as _:
        return True
    return False


# TODO replace this with pytest
if __name__ == '__main__':
    test_can_place()
    test_add_get_remove()
