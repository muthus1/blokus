"""
Blokus shapes and pieces.

Modify only the methods marked as TODO.
"""
import copy
from typing import Optional

from shape_definitions import ShapeKind

# A point is represented by row and column numbers (r, c). The
# top-left corner of a grid is (0, 0). Note that rows/columns
# correspond to vertical/horizontal axes, respectively. So, we
# will typically index into a 2-dimensional grid using
# grid[r][c] (as opposed to grid[y][x]).
#
Point = tuple[int, int]


# We will typically unpack a Point as follows: (r, c) = point
# In other cases, the row and col functions may be helpful.
#
def row(point: Point) -> int:
    return point[0]


def col(point: Point) -> int:
    return point[1]


class Shape:
    """
    Representing the 21 Blokus shapes, as named and defined by
    the string representations in shape_definitions.py.

    The locations of the squares are relative to the origin.

    The can_be_transformed boolean indicates whether or not
    the origin was explicitly defined in the string
    representation of the shape.

    See shape_definitions.py for more details.
    """

    kind: ShapeKind
    origin: Point
    can_be_transformed: bool
    squares: list[Point]

    def __init__(
        self,
        kind: ShapeKind,
        origin: Point,
        can_be_transformed: bool,
        squares: list[Point],
    ) -> None:
        """
        Constructor
        """
        self.kind = kind
        self.origin = origin
        self.can_be_transformed = can_be_transformed
        self.squares = squares

    def __str__(self) -> str:
        """
        Returns a complete string representation of the
        shape.
        """
        return f"""
            Shape
                kind = {self.kind}
                origin = {self.origin}
                can_be_transformed = {self.can_be_transformed}
                squares = {list(map(str, self.squares))}
        """

    @staticmethod
    def from_string(kind: ShapeKind, definition: str) -> "Shape":
        """
        Create a Shape based on its string representation
        in shape_definitions.py. See that file for details.
        """
        squares = []
        lines = definition.split('\n')
        first_line = 0
        for i, line in enumerate(lines):
            if line.find('X') != -1 or line.find('O') != -1 or \
                                        line.find('@') != -1:
                first_line = i
                break
        min_space = min(len(s) - len(s.lstrip()) for s in lines[first_line:])
        origin = (0,0)
        transform = True
        for r, line in enumerate(lines[first_line:]):
            for c, char in enumerate(line[min_space:]):
                if char == 'X':
                    r_0, c_0 = origin
                    squares.append((r - r_0, c - c_0))
                elif char == 'O':
                    squares.append((r, c))
                    origin = (r, c)
                    for i, square in enumerate(squares):
                        r_0, c_0 = origin
                        r_1, c_1 = square
                        squares[i] = (r_1 - r_0, c_1 - c_0)
                elif char == '@':
                    origin = (r, c)
                    for i, square in enumerate(squares):
                        r_0, c_0 = origin
                        r_1, c_1 = square
                        squares[i] = (r_1 - r_0, c_1 - c_0)

        if kind in [ShapeKind.ONE, ShapeKind.LETTER_O, ShapeKind.X]:
            transform = False
        return Shape(kind, origin, transform, squares)

    def flip_horizontally(self) -> None:
        """
        Flip the shape horizontally
        (across the vertical axis through its origin),
        by modifying the squares in place.
        """
        lst = []
        for tup in self.squares:
            r, c = tup
            if c == 0:
                lst.append(tup)
            else:
                lst.append((r, -c))
        self.squares = lst

    def rotate_left(self) -> None:
        """
        Rotate the shape left by 90 degrees,
        by modifying the squares in place.
        """
        lst = []
        for tup in self.squares:
            r, c = tup
            if tup != (0,0):
                lst.append((-c, r))
            else:
                lst.append(tup)
        self.squares = lst

    def rotate_right(self) -> None:
        """
        Rotate the shape right by 90 degrees,
        by modifying the squares in place.
        """
        lst = []
        for tup in self.squares:
            r, c = tup
            if tup != (0,0):
                lst.append((c, -r))
            else:
                lst.append(tup)
        self.squares = lst


class Piece:
    """
    A Piece takes a Shape and orients it on the board.

    The anchor point is used to locate the Shape.

    For flips and rotations, rather than storing these
    orientations directly (for example, using two attributes
    called face_up: bool and rotation: int), we modify
    the shape attribute in place. Therefore, it is important
    that each Piece object has its own deep copy of a
    Shape, so that transforming one Piece does not affect
    other Pieces that have the same Shape.
    """

    shape: Shape
    anchor: Optional[Point]

    def __init__(self, shape: Shape, face_up: bool = True, rotation: int = 0):
        """
        Each Piece will get its own deep copy of the given shape
        subject to initial transformations according to the arguments:

            face_up:  If true, the initial Shape will be flipped
                      horizontally.
            rotation: This number, modulo 4, indicates how many
                      times the shape should be right-rotated by
                      90 degrees.
        """
        # Deep copy shape, so that it can be transformed in place
        self.shape = copy.deepcopy(shape)

        # The anchor will be set by set_anchor
        self.anchor = None

        # We choose to flip...
        if not face_up:
            self.flip_horizontally()

        # ... before rotating
        for _ in range(rotation % 4):
            self.rotate_right()

    def set_anchor(self, anchor: Point) -> None:
        """
        Set the anchor point.
        """
        self.anchor = anchor

    def _check_anchor(self) -> None:
        """
        Raises ValueError if anchor is not set.
        Used by the flip and rotate methods below,
        so each of those may raise ValueError.
        """
        if self.anchor is None:
            raise ValueError(f"Piece does not have anchor: {self.shape}")

    def flip_horizontally(self) -> None:
        """
        Flip the piece horizontally.
        """
        self._check_anchor()
        self.shape.flip_horizontally()

    def rotate_left(self) -> None:
        """
        Rotate the shape left by 90 degrees,
        by modifying the squares in place.
        """
        self._check_anchor()
        self.shape.rotate_left()

    def rotate_right(self) -> None:
        """
        Rotate the shape right by 90 degrees,
        by modifying the squares in place.
        """
        self._check_anchor()
        self.shape.rotate_right()

    def squares(self) -> list[Point]:
        """
        Returns the list of points corresponding to the
        current position and orientation of the piece.

        Raises ValueError if anchor is not set.
        """
        self._check_anchor()
        return [
            (row(self.anchor) + r, col(self.anchor) + c)
            for r, c in self.shape.squares
        ]

    def cardinal_neighbors(self) -> set[Point]:
        """
        Returns the combined cardinal neighbors
        (north, south, east, and west)
        corresponding to all of the piece's squares.

        Raises ValueError if anchor is not set.
        """
        self._check_anchor()
        result = set()
        for square in self.squares():
            square_row, square_col = square
            cardinals = [(-1, 0), (0, -1), (0, 1), (1, 0)]
            for point in cardinals:
                r, c = point
                card_neighbor = (square_row + r, square_col + c)
                if card_neighbor not in self.squares():
                    result.add(card_neighbor)
        return result

    def intercardinal_neighbors(self) -> set[Point]:
        """
        Returns the combined intercardinal neighbors
        (northeast, southeast, southwest, and northwest)
        corresponding to all of the piece's squares.

        Raises ValueError if anchor is not set.
        """
        self._check_anchor()
        result = set()
        for square in self.squares():
            square_row, square_col = square
            inter_cards = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            for point in inter_cards:
                r, c = point
                inter_card_neighbor = (square_row + r, square_col + c)
                if inter_card_neighbor not in self.squares() and \
                inter_card_neighbor not in self.cardinal_neighbors():
                    result.add(inter_card_neighbor)
        return result
