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
    def raster_point(self, point: Point) -> None:
        pass
    
    @override
    def move_point(self, point: Point, x: int, y: int) -> None:
        pass
    
    @override
    def translate_point(self, point: Point, dx: int, dy: int) -> None:
        pass

    @override
    def remove_point(self, point: Point) -> None:
        pass
    

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


def test_batch_move():
    grid = create_grid()

    # Test successful case first
    # Add 6 points grouped as (4, 2)
    points = [
        Point(x=4, y=5, color='red'),
        Point(x=4, y=6, color='orange'),
        Point(x=5, y=5, color='yellow'),
        Point(x=5, y=6, color='green'),
        Point(x=6, y=17, color='blue'),
        Point(x=6, y=18, color='indigo'),
    ]

    for point in points:
        grid.add_point(point)

    # Batch move the group of 4
    assert grid.batch_move({
        points[0]: (8, 8),
        points[1]: (8, 9),
        points[2]: (9, 8),
        points[3]: (9, 9),
    })

    # Test gets
    def _check_get(expected_point: Point, x: int, y: int):
        maybe_point = grid.get_point(x, y)
        assert maybe_point is not None
        assert maybe_point == expected_point
        assert maybe_point.x == x
        assert maybe_point.y == y

    _check_get(points[0], 8, 8)
    _check_get(points[1], 8, 9)
    _check_get(points[2], 9, 8)
    _check_get(points[3], 9, 9)
    _check_get(points[4], 6, 17)
    _check_get(points[5], 6, 18)

    assert grid.get_point(4, 5) is None
    assert grid.get_point(4, 6) is None
    assert grid.get_point(5, 5) is None
    assert grid.get_point(5, 6) is None

    # Batch move the group of 2
    assert grid.batch_move({
        points[4]: (4, 5),
        points[5]: (4, 6),
    })

    # Test gets
    _check_get(points[0], 8, 8)
    _check_get(points[1], 8, 9)
    _check_get(points[2], 9, 8)
    _check_get(points[3], 9, 9)
    _check_get(points[4], 4, 5)
    _check_get(points[5], 4, 6)

    assert grid.get_point(6, 17) is None
    assert grid.get_point(6, 18) is None

    # Batch move the four with intersecting regions
    assert grid.batch_move({
        points[0]: (7, 8),
        points[1]: (7, 9),
        points[2]: (8, 8),
        points[3]: (8, 9),
    })

    _check_get(points[0], 7, 8)
    _check_get(points[1], 7, 9)
    _check_get(points[2], 8, 8)
    _check_get(points[3], 8, 9)

    assert grid.get_point(9, 8) is None
    assert grid.get_point(9, 9) is None

    # Make sure moving to duplicate locations raises an error
    _is_error_caught(lambda: grid.batch_move({
        points[0]: (3, 12),
        points[1]: (3, 13),
        points[2]: (3, 12),
    }))

    # Assert that move out of bounds does not work
    assert not grid.batch_move({points[3]: (10, 20)})

    # Assert that move to an already occupied location does not work
    assert not grid.batch_move({
        points[4]: (10, 9),
        points[5]: (10, 10),
    })

    print("test_batch_move success!")


def test_batch_translate():
    grid = create_grid()

    # Test successful case first
    # Add 6 points grouped as (4, 2)
    points = [
        Point(x=4, y=5, color='red'),
        Point(x=4, y=6, color='orange'),
        Point(x=5, y=5, color='yellow'),
        Point(x=5, y=6, color='green'),
        Point(x=6, y=17, color='blue'),
        Point(x=6, y=18, color='indigo'),
    ]

    for point in points:
        grid.add_point(point)

    # Batch translate the group of 4
    assert grid.batch_translate({
        points[0]: (0, 1),
        points[1]: (0, 1),
        points[2]: (1, 2),
        points[3]: (2, 2),
    })

    # Test gets
    def _check_get(expected_point: Point, x: int, y: int):
        maybe_point = grid.get_point(x, y)
        assert maybe_point is not None
        assert maybe_point == expected_point
        assert maybe_point.x == x
        assert maybe_point.y == y

    _check_get(points[0], 4, 6)
    _check_get(points[1], 4, 7)
    _check_get(points[2], 6, 7)
    _check_get(points[3], 7, 8)
    _check_get(points[4], 6, 17)
    _check_get(points[5], 6, 18)

    assert grid.get_point(4, 5) is None
    assert grid.get_point(5, 5) is None
    assert grid.get_point(5, 6) is None

    # Make sure translating to duplicate locations raises an error
    _is_error_caught(lambda: grid.batch_translate({
        points[0]: (1, 2),
        points[1]: (1, 1),
        points[2]: (0, 0),
    }))

    # Assert that translate out of bounds does not work
    assert not grid.batch_translate({points[4]: (2, 4)})

    # Assert that translate to an already occupied location does not work
    assert not grid.batch_translate({
        points[4]: (0, 0),
        points[5]: (1, -10),
    })

    print("test_batch_translate success!")


def test_clear_rows_single():
    grid = create_grid()

    # populate a full row at row_idx=17
    for x in range(grid.width):
        grid.add_point(Point(x=x, y=17, color='black'))
    
    # populate two points below
    grid.add_point(Point(x=4, y=18, color='black'))
    grid.add_point(Point(x=1, y=20, color='black'))

    # populate three points above
    grid.add_point(Point(x=7, y=16, color='black'))
    grid.add_point(Point(x=9, y=12, color='black'))
    grid.add_point(Point(x=1, y=5, color='black'))

    # clear the row
    grid.clear_full_rows()

    # test correctness
    def _check_get(x: int, y: int):
        maybe_point = grid.get_point(x, y)
        assert maybe_point is not None
        assert maybe_point.x == x
        assert maybe_point.y == y
    
    _check_get(4, 18)
    _check_get(1, 20)
    _check_get(7, 17)
    _check_get(9, 13)
    _check_get(1, 6)

    assert grid.get_point(7, 16) is None
    assert grid.get_point(9, 12) is None
    assert grid.get_point(1, 5) is None

    for x in range(grid.width):
        if x != 7:
            assert grid.get_point(x=x, y=17) is None

    print("test_clear_rows_single success!")


def test_clear_rows_top():
    grid = create_grid()

    # populate a full row at row_idx=0
    for x in range(grid.width):
        grid.add_point(Point(x=x, y=0, color='black'))
    
    # populate two points below
    grid.add_point(Point(x=8, y=2, color='black'))
    grid.add_point(Point(x=4, y=18, color='black'))

    # clear the row
    grid.clear_full_rows()

    # test correctness
    def _check_get(x: int, y: int):
        maybe_point = grid.get_point(x, y)
        assert maybe_point is not None
        assert maybe_point.x == x
        assert maybe_point.y == y
    
    _check_get(8, 2)
    _check_get(4, 18)

    for x in range(grid.width):
        assert grid.get_point(x=x, y=0) is None

    print("test_clear_rows_top success!")


def test_clear_rows_multiple():
    grid = create_grid()

    # populate full rows at row_idx=20, 17, and 4
    full_rows = [20, 17, 4]
    for row in full_rows:
        for x in range(grid.width):
            grid.add_point(Point(x=x, y=row, color='black'))
    
    # populate two points btwn 20 and 17
    grid.add_point(Point(x=4, y=18, color='black'))
    grid.add_point(Point(x=1, y=19, color='black'))

    # populate two points between 17 and 4
    grid.add_point(Point(x=8, y=5, color='black'))
    grid.add_point(Point(x=9, y=12, color='black'))

    # populate two points above 4
    grid.add_point(Point(x=3, y=3, color='black'))
    grid.add_point(Point(x=7, y=1, color='black'))

    # clear the rows
    grid.clear_full_rows()

    # test correctness
    def _check_get(x: int, y: int):
        maybe_point = grid.get_point(x, y)
        assert maybe_point is not None
        assert maybe_point.x == x
        assert maybe_point.y == y
    
    _check_get(4, 19)
    _check_get(1, 20)
    _check_get(8, 7)
    _check_get(9, 14)
    _check_get(3, 6)
    _check_get(7, 4)

    assert grid.get_point(4, 18) is None
    assert grid.get_point(1, 19) is None
    assert grid.get_point(8, 5) is None
    assert grid.get_point(9, 12) is None
    assert grid.get_point(3, 3) is None
    assert grid.get_point(7, 1) is None

    for x in range(grid.width):
        if x != 1:
            assert grid.get_point(x=x, y=20) is None
    
    for x in range(grid.width):
        assert grid.get_point(x=x, y=17) is None

    for x in range(grid.width):
        if x != 7:
            assert grid.get_point(x=x, y=4) is None

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
    test_batch_move()
    test_batch_translate()
    test_clear_rows_single()
    test_clear_rows_top()
    test_clear_rows_multiple()
