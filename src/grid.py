from abc import ABC, abstractmethod
from typing import Optional

from shape_definitions import ShapeKind, definitions
from piece import Point, Shape, Piece
from blokus import Blokus, Grid

Cell = Optional[tuple[int, ShapeKind]]

symbols = {
ShapeKind.ONE : "1",
ShapeKind.TWO : "2",
ShapeKind.THREE : "3",
ShapeKind.FOUR : "4",
ShapeKind.FIVE : "5",
ShapeKind.SEVEN : "7",
ShapeKind.A : "A",
ShapeKind.C : "C",
ShapeKind.F : "F",
ShapeKind.S : "S",
ShapeKind.L : "L",
ShapeKind.N : "N",
ShapeKind.LETTER_O : "O",
ShapeKind.P : "P",
ShapeKind.T : "T",
ShapeKind.U : "U",
ShapeKind.V : "V",
ShapeKind.W : "W",
ShapeKind.X : "X",
ShapeKind.Y : "Y",
ShapeKind.Z : "Z",
}

def place_many_pieces() -> None:
    """
    This helper is designed to place 19 pieces, so that the final pieces
    played can be changed. This is a copy of the one from test_blokus.py. I 
    could not figure out how to import it.
    """
    blokus = Blokus(2, 20, {(0, 0), (19, 19)})

    def place_piece(kind: ShapeKind, row: int, col: int, flip: bool = False, 
                    rotate: int = 0) -> None:
        """
        This helper function is called 19 times below,
        to place each one of Player 2's pieces at the
        designated positions
        """

        assert blokus.curr_player == 2
        assert not blokus.game_over

        piece = Piece(blokus.shapes[kind])

        piece.set_anchor((row, col))

        if flip:
            piece.flip_horizontally()
        for _ in range(rotate):
            piece.rotate_right()

        assert blokus.maybe_place(piece)

    assert blokus.curr_player == 1
    blokus.retire()

    assert blokus.curr_player == 2
    place_piece(ShapeKind.Y, 1, 0, True)
    place_piece(ShapeKind.TWO, 4, 1)
    place_piece(ShapeKind.W, 3, 3, False, 3)
    place_piece(ShapeKind.SEVEN, 6, 2, False, 1)
    place_piece(ShapeKind.U, 6, 6, False, 3)
    place_piece(ShapeKind.FIVE, 9, 0)
    place_piece(ShapeKind.L, 13, 2, False, 2)
    place_piece(ShapeKind.LETTER_O, 16, 0)
    place_piece(ShapeKind.C, 18, 3, False, 2)
    place_piece(ShapeKind.T, 18, 5, False, 2)
    place_piece(ShapeKind.X, 15, 6)
    place_piece(ShapeKind.A, 18, 8)
    place_piece(ShapeKind.S, 17, 11, False, 1)
    place_piece(ShapeKind.THREE, 16, 13)
    place_piece(ShapeKind.FOUR, 13, 11, False, 1)
    place_piece(ShapeKind.F, 13, 8, False, 1)
    place_piece(ShapeKind.P, 9, 3, True)
    place_piece(ShapeKind.V, 9, 8, False, 2)
    place_piece(ShapeKind.Z, 6, 11, True)

    return blokus

def grid_to_string(grid: Grid) -> str:
    """
    Convert Grid values (as defined in src/base.py) to a string. The string 
    indicates the board size by drawing an explicit border with '|'. For each 
    cell occupied by a square, the string indicates which player’s piece 
    is covering it by using two characters per cell and filling only the first 
    character to indicate that the square is occupied by the first player and 
    filling only the second character to indicate that the square is occupied 
    by the second player.
    """
    size = len(grid)
    string = ""
    header = "|" * 4 + (2 * size) * "|"
    string += header
    for lst in grid:
        string += "\n||"
        for cell in lst:
            if cell is None:
                string += "  "
            else:
                player, kind = cell
                symbol = symbols[kind]
                if player == 1:
                    string += symbol + " "
                else:
                    string += " " + symbol
        string += "||"
    string += "\n" + header
    return string
 

def string_to_grid(s: str) -> Grid:
    """Convert the strings from above into a grid."""
    string = s.replace("|", "")
    lines = string.split('\n')[1: -1]
    size = len(lines)
    grid = [[None] * size for _ in range(size)]
    for r, val in enumerate(lines):
        for c in range(0, size * 2, 2):
            cell = val[c]
            if cell != " ":
                kind = [n for n in symbols if symbols[n] == cell][0]
                grid[r][c//2] = (1, kind)
        for c in range(1, size * 2, 2):
            cell = val[c]
            if cell != " ":
                kind = [n for n in symbols if symbols[n] == cell][0]
                grid[r][c//2] = (2, kind)
    return grid

def test_grid_1() -> None:
    """
    Test that the grid_to_string() and string_to_grid() functions work for a
    one player Blokus game with a 5x5 board.
    """
    blokus = Blokus(1, 5, {(0, 0), (4, 4)})

    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((0, 0))
    assert blokus.maybe_place(piece_one)
    assert blokus.curr_player == 1
    assert not blokus.game_over

    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_two.set_anchor((1, 1))
    assert blokus.maybe_place(piece_two)
    assert blokus.curr_player == 1
    assert not blokus.game_over

    grid = blokus.grid
    s = """||||||||||||||
||1         ||
||  2 2     ||
||          ||
||          ||
||          ||
||||||||||||||"""

    assert s == grid_to_string(grid)
    assert grid == string_to_grid(grid_to_string(grid))

def test_grid_2() -> None:
    """
    Test that the grid_to_string() and string_to_grid() functions work for a
    two player Blokus game with a 5x5 board.
    """
    blokus = Blokus(2, 5, {(0, 0), (4, 4)})

    assert blokus.curr_player == 1
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((0, 0))
    assert blokus.maybe_place(piece_one)
    assert not blokus.game_over

    assert blokus.curr_player == 2
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((4, 4))
    assert blokus.maybe_place(piece_one)
    assert not blokus.game_over

    assert blokus.curr_player == 1
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_two.set_anchor((1, 1))
    assert blokus.maybe_place(piece_two)
    assert not blokus.game_over

    assert blokus.curr_player == 2
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_two.set_anchor((3, 2))
    assert blokus.maybe_place(piece_two)
    assert not blokus.game_over

    grid = blokus.grid
    s = """||||||||||||||
||1         ||
||  2 2     ||
||          ||
||     2 2  ||
||         1||
||||||||||||||"""
    assert s == grid_to_string(grid)
    assert grid == string_to_grid(grid_to_string(grid))

def test_grid_3() -> None:
    """
    Test that the grid_to_string() and string_to_grid() functions work for a
    two player Blokus game with a 7x7 board.
    """
    blokus = Blokus(2, 7, {(0, 0), (6, 6)})

    assert blokus.curr_player == 1
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((0, 0))
    assert blokus.maybe_place(piece_one)
    assert not blokus.game_over

    assert blokus.curr_player == 2
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((6, 6))
    assert blokus.maybe_place(piece_one)
    assert not blokus.game_over

    assert blokus.curr_player == 1
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_two.set_anchor((1, 1))
    assert blokus.maybe_place(piece_two)
    assert not blokus.game_over

    assert blokus.curr_player == 2
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_two.set_anchor((5, 4))
    assert blokus.maybe_place(piece_two)
    assert not blokus.game_over

    grid = blokus.grid
    s = """||||||||||||||||||
||1             ||
||  2 2         ||
||              ||
||              ||
||              ||
||         2 2  ||
||             1||
||||||||||||||||||"""
    assert s == grid_to_string(grid)
    assert grid == string_to_grid(grid_to_string(grid))

def test_grid_4():
    """
    Test that the grid_to_string() and string_to_grid() functions work for a
    two player Blokus game with a 20x20 board.
    """
    blokus = place_many_pieces()

    piece = Piece(blokus.shapes[ShapeKind.ONE])
    piece.set_anchor((1, 4))
    assert blokus.maybe_place(piece)

    piece = Piece(blokus.shapes[ShapeKind.N])
    piece.set_anchor((2, 7))
    piece.rotate_right()
    assert blokus.maybe_place(piece)

    grid = blokus.grid
    s = """||||||||||||||||||||||||||||||||||||||||||||
|| Y                                      ||
|| Y Y     1                              ||
|| Y   W W   N N N                        ||
|| Y     W W     N N                      ||
||   2 2   W                              ||
||       7   U U         Z Z              ||
||   7 7 7     U         Z                ||
|| 5         U U       Z Z                ||
|| 5     P P     V V V                    ||
|| 5     P P     V                        ||
|| 5       P     V                        ||
|| 5                                      ||
||   L L           F     4                ||
||     L         F F F   4                ||
||     L       X     F   4                ||
||     L     X X X       4                ||
|| O O         X       S   3 3 3          ||
|| O O   C   T     A   S S                ||
||     C C   T   A A A   S                ||
||         T T T                          ||
||||||||||||||||||||||||||||||||||||||||||||"""

    assert s == grid_to_string(grid)
    assert grid == string_to_grid(grid_to_string(grid))

def test_grid_5():
    """
    Test that the grid_to_string() and string_to_grid() functions work for a
    two player Blokus game with a 20x20 board, with slightly different
    placements.
    """
    blokus = place_many_pieces()

    piece = Piece(blokus.shapes[ShapeKind.N])
    piece.set_anchor((1, 6))
    piece.rotate_right()
    assert blokus.maybe_place(piece)
    
    piece = Piece(blokus.shapes[ShapeKind.ONE])
    piece.set_anchor((3, 8))
    assert blokus.maybe_place(piece)

    grid = blokus.grid
    s = """||||||||||||||||||||||||||||||||||||||||||||
|| Y                                      ||
|| Y Y     N N N                          ||
|| Y   W W     N N                        ||
|| Y     W W       1                      ||
||   2 2   W                              ||
||       7   U U         Z Z              ||
||   7 7 7     U         Z                ||
|| 5         U U       Z Z                ||
|| 5     P P     V V V                    ||
|| 5     P P     V                        ||
|| 5       P     V                        ||
|| 5                                      ||
||   L L           F     4                ||
||     L         F F F   4                ||
||     L       X     F   4                ||
||     L     X X X       4                ||
|| O O         X       S   3 3 3          ||
|| O O   C   T     A   S S                ||
||     C C   T   A A A   S                ||
||         T T T                          ||
||||||||||||||||||||||||||||||||||||||||||||"""

    assert s == grid_to_string(grid)
    assert grid == string_to_grid(grid_to_string(grid))