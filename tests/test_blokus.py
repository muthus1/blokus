import pytest
from typing import Optional

import shape_definitions
from shape_definitions import ShapeKind
from piece import Shape, Piece
from blokus import Blokus
from base import BlokusBase

def test_inheritance() -> None:
    assert issubclass(
        Blokus, BlokusBase
    ), "Blokus should inherit from BlokusBase"

def init_blokus_mini(num_players: int) -> BlokusBase:
    return Blokus(num_players, 5, {(0, 0), (4, 4)})

def init_blokus_mono() -> BlokusBase:
    return Blokus(1, 11, {(5, 5)})


def init_blokus_duo() -> BlokusBase:
    return Blokus(2, 14, {(4, 4), (9, 9)})


def init_blokus_classic(num_players: int = 2) -> BlokusBase:
    return Blokus(num_players, 20, {(0, 0), (0, 19), (19, 0), (19, 19)})


def test_init_blokus_mini_1() -> None:
    """
    Construct an instance of a 1-player Blokus Mini game configuration. 
    Verify that the size, start_positions, num_players, and curr_player 
    properties have been initialized correctly. Also verify that grid has been 
    initialized correctly.
    """
    b = init_blokus_mini(1)
    assert b.num_players == 1
    assert b.size == 5
    assert b.start_positions == {(0, 0), (4, 4)}
    assert b.grid == [[None] * 5] * 5


def test_init_blokus_mini_2() -> None:
    """
    Ditto above for 2-player Blokus Mini.
    """
    b = init_blokus_mini(2)
    assert b.num_players == 2
    assert b.size == 5
    assert b.start_positions == {(0, 0), (4, 4)}
    assert b.grid == [[None] * 5] * 5


def test_init_blokus_mono() -> None:
    """
    Ditto above for Blokus Mono.
    """
    b = init_blokus_mono()
    assert b.num_players == 1
    assert b.size == 11
    assert b.start_positions == {(5, 5)}
    assert b.grid == [[None] * 11] * 11


def test_init_blokus_duo_2() -> None:
    """
    Ditto above for Blokus Duo.
    """
    b = init_blokus_duo()
    assert b.num_players == 2
    assert b.size == 14
    assert b.start_positions == {(4, 4), (9, 9)}
    assert b.grid == [[None] * 14] * 14

def test_shapes_loaded() -> None:
    """Test that the shapes have been loaded correctly"""
    blokus = init_blokus_duo()

    shape = blokus.shapes[ShapeKind.ONE]
    assert shape.kind == ShapeKind.ONE
    assert shape.origin == (0, 0)
    assert not shape.can_be_transformed
    assert shape.squares == [(0, 0)]

    shape = blokus.shapes[ShapeKind.TWO]
    assert shape.kind == ShapeKind.TWO
    assert shape.origin == (0, 0)
    assert shape.can_be_transformed
    assert shape.squares == [(0, 0), (0, 1)]

    shape = blokus.shapes[ShapeKind.THREE]
    assert shape.kind == ShapeKind.THREE
    assert shape.origin == (0, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(0, -1), (0, 0), (0, 1)]
    
    shape = blokus.shapes[ShapeKind.C]
    assert shape.kind == ShapeKind.C
    assert shape.origin == (0, 0)
    assert shape.can_be_transformed
    assert shape.squares == [(0, 0), (0, 1), (1, 0)]
    
    shape = blokus.shapes[ShapeKind.FOUR]
    assert shape.kind == ShapeKind.FOUR
    assert shape.origin == (0, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(0, -1), (0, 0), (0, 1), (0, 2)]
    
    shape = blokus.shapes[ShapeKind.SEVEN]
    assert shape.kind == ShapeKind.SEVEN
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(-1, -1), (-1, 0), (0, 0), (1, 0)]

    shape = blokus.shapes[ShapeKind.S]
    assert shape.kind == ShapeKind.S
    assert shape.origin == (0, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(0, 0), (0, 1), (1, -1), (1, 0)]

    shape = blokus.shapes[ShapeKind.LETTER_O]
    assert shape.kind == ShapeKind.LETTER_O
    assert shape.origin == (0, 0)
    assert not shape.can_be_transformed
    assert shape.squares == [(0, 0), (0, 1), (1, 0), (1, 1)]

    shape = blokus.shapes[ShapeKind.A]
    assert shape.kind == ShapeKind.A
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(-1, 0), (0, -1), (0, 0), (0, 1)]

    shape = blokus.shapes[ShapeKind.F]
    assert shape.kind == ShapeKind.F
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(-1, 0), (-1, 1), (0, -1), (0, 0), (1, 0)]
    
    shape = blokus.shapes[ShapeKind.FIVE]
    assert shape.kind == ShapeKind.FIVE
    assert shape.origin == (2, 0)
    assert shape.can_be_transformed
    assert shape.squares == [(-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0)]
    
    shape = blokus.shapes[ShapeKind.L]
    assert shape.kind == ShapeKind.L
    assert shape.origin == (2, 0)
    assert shape.can_be_transformed
    assert shape.squares == [(-2, 0), (-1, 0), (0, 0), (1, 0), (1, 1)]

    shape = blokus.shapes[ShapeKind.N]
    assert shape.kind == ShapeKind.N
    assert shape.origin == (1, 0)
    assert shape.can_be_transformed
    assert shape.squares == [(-1, 1), (0, 0), (0, 1), (1, 0), (2, 0)]
    
    shape = blokus.shapes[ShapeKind.P]
    assert shape.kind == ShapeKind.P
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(-1, -1), (-1, 0), (0, -1), (0, 0), (1, -1)]

    shape = blokus.shapes[ShapeKind.T]
    assert shape.kind == ShapeKind.T
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(-1, -1), (-1, 0), (-1, 1), (0, 0), (1, 0)]

    shape = blokus.shapes[ShapeKind.U]
    assert shape.kind == ShapeKind.U
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(-1, -1), (-1, 1), (0, -1), (0, 0), (0, 1)]

    shape = blokus.shapes[ShapeKind.V]
    assert shape.kind == ShapeKind.V
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(-1, 1), (0, 1), (1, -1), (1, 0), (1, 1)]

    shape = blokus.shapes[ShapeKind.W]
    assert shape.kind == ShapeKind.W
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(-1, 1), (0, 0), (0, 1), (1, -1), (1, 0)]
    
    shape = blokus.shapes[ShapeKind.V]
    assert shape.kind == ShapeKind.V
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(-1, 1), (0, 1), (1, -1), (1, 0), (1, 1)]

    shape = blokus.shapes[ShapeKind.X]
    assert shape.kind == ShapeKind.X
    assert shape.origin == (1, 1)
    assert not shape.can_be_transformed
    assert shape.squares == [(-1, 0), (0, -1), (0, 0), (0, 1), (1, 0)]
    
    shape = blokus.shapes[ShapeKind.Y]
    assert shape.kind == ShapeKind.Y
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(-1, 0), (0, -1), (0, 0), (1, 0), (2, 0)]

    shape = blokus.shapes[ShapeKind.Z]
    assert shape.kind == ShapeKind.Z
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(-1, -1), (-1, 0), (0, 0), (1, 0), (1, 1)]

def test_some_flipped_shapes() -> None:
    """
    Construct an instance of any Blokus game configuration, and test that at 
    least three kinds of shapes can be flipped correctly via the 
    Shape.flip_horizontally method.
    """
    
    blokus = init_blokus_duo()

    shape = blokus.shapes[ShapeKind.V]
    shape.flip_horizontally()
    assert shape.squares == [(-1, -1), (0, -1), (1, 1), (1, 0), (1, -1)]

    shape = blokus.shapes[ShapeKind.Y]
    shape.flip_horizontally()
    assert shape.squares == [(-1, 0), (0, 1), (0, 0), (1, 0), (2, 0)]

    shape = blokus.shapes[ShapeKind.Z]
    shape.flip_horizontally()
    assert shape.squares == [(-1, 1), (-1, 0), (0, 0), (1, 0), (1, -1)]

def test_some_left_rotated_shapes() -> None:
    """
    Ditto above for Shape.rotate_left
    """

    blokus = init_blokus_duo()

    shape = blokus.shapes[ShapeKind.V]
    shape.rotate_left()
    assert shape.squares == [(-1, -1), (-1, 0), (1, 1), (0, 1), (-1, 1)]

    shape = blokus.shapes[ShapeKind.Y]
    shape.rotate_left()
    assert shape.squares == [(0, -1), (1, 0), (0, 0), (0, 1), (0, 2)]

    shape = blokus.shapes[ShapeKind.Z]
    shape.rotate_left()
    assert shape.squares == [(1, -1), (0, -1), (0, 0), (0, 1), (-1, 1)]

def test_some_right_rotated_shapes() -> None:
    """
    Ditto above for Shape.rotate_right
    """

    blokus = init_blokus_duo()

    shape = blokus.shapes[ShapeKind.V]
    shape.rotate_right()
    assert shape.squares == [(1, 1), (1, 0), (-1, -1), (0, -1), (1, -1)]

    shape = blokus.shapes[ShapeKind.Y]
    shape.rotate_right()
    assert shape.squares == [(0, 1), (-1, 0), (0, 0), (0, -1), (0, -2)]

    shape = blokus.shapes[ShapeKind.Z]
    shape.rotate_right()
    assert shape.squares == [(-1, 1), (0, 1), (0, 0), (0, -1), (1, -1)]

def test_some_cardinal_neighbors() -> None:
    """
    Test that Piece.cardinal_neighbors correctly computes the cardinal 
    neighbors of at least three kinds of pieces.
    """

    blokus = init_blokus_mini(1)
    piece_v = Piece(blokus.shapes[ShapeKind.V])
    piece_v.set_anchor((3, 3))

    blokus_2 = init_blokus_mini(1)
    piece_y = Piece(blokus_2.shapes[ShapeKind.Y])
    piece_y.set_anchor((2, 4))

    blokus_3 = init_blokus_mini(1)
    piece_z = Piece(blokus_3.shapes[ShapeKind.Z])
    piece_z.set_anchor((3, 3))

    assert piece_v.cardinal_neighbors() == {(1, 4),
                                            (2, 3),
                                            (2, 5),
                                            (3, 2),
                                            (3, 3),
                                            (3, 5),
                                            (4, 1),
                                            (4, 5),
                                            (5, 2),
                                            (5, 3),
                                            (5, 4)}
    assert piece_y.cardinal_neighbors() == {(0, 4),
                                            (1, 3),
                                            (1, 5),
                                            (2, 2),
                                            (2, 5),
                                            (3, 3),
                                            (3, 5),
                                            (4, 3),
                                            (4, 5),
                                            (5, 4)}
    assert piece_z.cardinal_neighbors() == {(1, 2),
                                            (1, 3),
                                            (2, 1),
                                            (2, 4),
                                            (3, 2),
                                            (3, 4),
                                            (4, 2),
                                            (4, 5),
                                            (5, 3),
                                            (5, 4)}

def test_some_intercardinal_neighbors() -> None:
    """
    Test that Piece.intercardinal_neighbors correctly computes the cardinal 
    neighbors of at least three kinds of pieces.
    """
    
    blokus = init_blokus_mini(1)
    piece_v = Piece(blokus.shapes[ShapeKind.V])
    piece_v.set_anchor((3, 3))

    blokus_2 = init_blokus_mini(1)
    piece_y = Piece(blokus_2.shapes[ShapeKind.Y])
    piece_y.set_anchor((2, 4))

    blokus_3 = init_blokus_mini(1)
    piece_z = Piece(blokus_3.shapes[ShapeKind.Z])
    piece_z.set_anchor((3, 3))

    assert piece_v.intercardinal_neighbors() == {(1, 3), (1, 5), (3, 1), (5, 1), 
                                                 (5, 5)}
    assert piece_y.intercardinal_neighbors() == {(0, 3), (0, 5), (1, 2), (3, 2),
                                                 (5, 3), (5, 5)}
    assert piece_z.intercardinal_neighbors() == {(1, 1), (1, 4), (3, 1), (3, 5),
                                                 (5, 2), (5, 5)}

def test_one_player_blokus_mini_game() -> None:
    """
    Test that the player can place two or more pieces before retiring.
    """
    blokus = init_blokus_mini(1)

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

    blokus.retire()

    assert blokus.game_over
    assert blokus.winners == [1]
    assert blokus.get_score(1) == -86

def test_two_player_blokus_mini_game() -> None:
    """
    Test that each player can place two or more pieces before retiring.
    """
    blokus = init_blokus_mini(2)

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

    assert blokus.curr_player == 1
    blokus.retire()
    assert not blokus.game_over

    assert blokus.curr_player == 2
    blokus.retire()
    assert blokus.game_over

    assert blokus.winners == [1,2]
    assert blokus.get_score(1) == -86
    assert blokus.get_score(2) == -86

def test_exception_init() -> None:
    """
    Verify that four calls to the Blokus constructor each raise a ValueError, 
    one for each of the four situations described in the docstring.
    """
    with pytest.raises(ValueError):
        blokus = init_blokus_mini(5)
    with pytest.raises(ValueError):
        blokus = Blokus(2, 3, {(0, 0), (3, 3)})
    with pytest.raises(ValueError):
        blokus = Blokus(2, 5, {(0, 0), (6, 6)})
    with pytest.raises(ValueError):
        blokus = Blokus(2, 3, {(0, 0)})
        
def test_exception_place_already_played() -> None:
    """
    Create an instance of any Blokus game configuration. Verify that maybe_place
    raises a ValueError when trying to place an already played piece.
    """
    blokus = init_blokus_mini(1)

    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((0, 0))
    assert blokus.maybe_place(piece_one)

    piece_two = Piece(blokus.shapes[ShapeKind.ONE])
    piece_two.set_anchor((1, 1))
    with pytest.raises(ValueError):
        blokus.maybe_place(piece_two)


def test_exception_place_without_anchor() -> None:
    """
    Create an instance of any Blokus game configuration. Verify that maybe_place
    raises a ValueError when trying to place a piece without an anchor.
    """
    blokus = init_blokus_mini(1)

    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    with pytest.raises(ValueError):
        blokus.maybe_place(piece_one)

def test_start_positions_1() -> None:
    """
    Create an instance of any 1-player Blokus game configuration with one start
    position. Verify that maybe_place will not place a piece that does not cover
    the start position. Then verify that maybe_place will place a piece that 
    does cover the start position, and that the player can place a second piece 
    on the board.
    """
    blokus = init_blokus_mono()

    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((0, 0))
    assert not blokus.maybe_place(piece_one)
    
    piece_one.set_anchor((5, 5))
    assert blokus.maybe_place(piece_one)

    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_two.set_anchor((6, 6))
    assert blokus.maybe_place(piece_two)

def test_start_positions_2() -> None:
    """
    Create an instance of any 2-player Blokus game configuration with two start
    positions. Verify that Player 1 cannot place a piece which does not cover a 
    start position, before then playing a piece which does. Then verify that 
    Player 2 cannot place a piece that does not cover a start position nor one 
    that covers only the already covered start position. Then verify that 
    Player 2 can cover the remaining start position. After all that, verify that
    Player 1 and Player 2 can each play another piece. (This sequence involves
    four placed pieces in total.)
    """

    blokus = init_blokus_mini(2)

    assert blokus.curr_player == 1
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((1, 0))
    assert not blokus.maybe_place(piece_one)
    piece_one.set_anchor((0, 0))
    assert blokus.maybe_place(piece_one)

    assert blokus.curr_player == 2
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((0, 0))
    assert not blokus.maybe_place(piece_one)
    piece_one.set_anchor((1, 0))
    assert not blokus.maybe_place(piece_one)
    piece_one.set_anchor((4, 4))
    assert blokus.maybe_place(piece_one)

    assert blokus.curr_player == 1
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_two.set_anchor((1, 1))
    assert blokus.maybe_place(piece_two)

    assert blokus.curr_player == 2
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_two.set_anchor((3, 2))
    assert blokus.maybe_place(piece_two)

def test_start_positions_3() -> None:
    """
    Same as the previous test, except the game board has four start positions 
    rather than two.
    """
    blokus = init_blokus_classic()

    assert blokus.curr_player == 1
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((1, 0))
    assert not blokus.maybe_place(piece_one)
    piece_one.set_anchor((0, 0))
    assert blokus.maybe_place(piece_one)

    assert blokus.curr_player == 2
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((0, 0))
    assert not blokus.maybe_place(piece_one)
    piece_one.set_anchor((1, 0))
    assert not blokus.maybe_place(piece_one)
    piece_one.set_anchor((19, 19))
    assert blokus.maybe_place(piece_one)

    assert blokus.curr_player == 1
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_two.set_anchor((1, 1))
    assert blokus.maybe_place(piece_two)

    assert blokus.curr_player == 2
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_two.set_anchor((18, 17))
    assert blokus.maybe_place(piece_two)

def test_place_flipped_shape_1() -> None:
    """
    Create an instance of any 1-player Blokus game configuration. 
    Choose a piece, anchor it somewhere, flip it, and verify that its squares() 
    are correct. Then place the piece, and verify that grid stores the correct 
    values for every cell in the matrix.
    """

    blokus = init_blokus_mono()
    piece = Piece(blokus.shapes[ShapeKind.C])
    piece.set_anchor((5, 5))
    assert piece.squares() == [(5, 5), (5, 6), (6, 5)]
    piece.flip_horizontally()
    assert piece.squares() == [(5, 5), (5, 4), (6, 5)]
    assert blokus.maybe_place(piece)

    for r in range(11):
        for c in range(11):
            if (r, c) in [(5, 5), (5, 4), (6, 5)]:
                assert blokus.grid[r][c] == (1, ShapeKind.C)
            else:
                assert blokus.grid[r][c] is None

def test_rotated_shape_1() -> None:
    """
    Same as the previous, except for a shape that is rotated once (90 degrees) 
    to the right.
    """
    blokus = init_blokus_mono()
    piece = Piece(blokus.shapes[ShapeKind.C])
    piece.set_anchor((5, 5))
    assert piece.squares() == [(5, 5), (5, 6), (6, 5)]
    piece.rotate_right()
    assert piece.squares() == [(5, 5), (6, 5), (5, 4)]
    assert blokus.maybe_place(piece)

    for r in range(11):
        for c in range(11):
            if (r, c) in [(5, 5), (6, 5), (5, 4)]:
                assert blokus.grid[r][c] == (1, ShapeKind.C)
            else:
                assert blokus.grid[r][c] is None

def test_rotated_shape_2() -> None:
    """
    Same as the previous, except for a shape that is rotated twice (180 degrees)
    to the right.
    """
    blokus = init_blokus_mono()
    piece = Piece(blokus.shapes[ShapeKind.C])
    piece.set_anchor((5, 5))
    assert piece.squares() == [(5, 5), (5, 6), (6, 5)]
    piece.rotate_right()
    piece.rotate_right()
    assert piece.squares() == [(5, 5), (5, 4), (4, 5)]
    assert blokus.maybe_place(piece)

    for r in range(11):
        for c in range(11):
            if (r, c) in [(5, 5), (5, 4), (4, 5)]:
                assert blokus.grid[r][c] == (1, ShapeKind.C)
            else:
                assert blokus.grid[r][c] is None
    
def test_flipped_and_rotated_shape_1() -> None:
    """
    Same as the previous, except for a shape that is flipped and then rotated 
    three times (270 degrees) to the right.
    """
    blokus = init_blokus_mono()
    piece = Piece(blokus.shapes[ShapeKind.C])
    piece.set_anchor((5, 5))
    assert piece.squares() == [(5, 5), (5, 6), (6, 5)]
    piece.flip_horizontally()
    piece.rotate_right()
    piece.rotate_right()
    piece.rotate_right()
    assert piece.squares() == [(5, 5), (6, 5), (5, 6)]
    assert blokus.maybe_place(piece)

    for r in range(11):
        for c in range(11):
            if (r, c) in [(5, 5), (5, 6), (6, 5)]:
                assert blokus.grid[r][c] == (1, ShapeKind.C)
            else:
                assert blokus.grid[r][c] is None

def test_flipped_and_rotated_shape_2() -> None:
    """
    Same as the previous, except for a shape that is flipped twice and then 
    rotated four times (360 degrees) to the right.
    """
    blokus = init_blokus_mono()
    piece = Piece(blokus.shapes[ShapeKind.C])
    piece.set_anchor((5, 5))
    assert piece.squares() == [(5, 5), (5, 6), (6, 5)]
    piece.flip_horizontally()
    piece.flip_horizontally()
    piece.rotate_right()
    piece.rotate_right()
    piece.rotate_right()
    piece.rotate_right()
    assert piece.squares() == [(5, 5), (5, 6), (6, 5)]
    assert blokus.maybe_place(piece)

    for r in range(11):
        for c in range(11):
            if (r, c) in [(5, 5), (5, 6), (6, 5)]:
                assert blokus.grid[r][c] == (1, ShapeKind.C)
            else:
                assert blokus.grid[r][c] is None

def test_prevent_own_edges_1() -> None:
    """
    Create an instance of any 1-player Blokus game configuration. After placing 
    a piece, verify that the player cannot place another piece that shares an 
    edge with their first played piece.
    """
    blokus = init_blokus_mini(1)

    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((0, 0))
    blokus.maybe_place(piece_one)
    
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_two.set_anchor((0, 1))
    assert not blokus.maybe_place(piece_two)

def test_prevent_own_edges_2() -> None:
    """
    Create an instance of any 2-player Blokus game configuration. After Player 1
    and Player 2 each play a piece, verify that Player 1 cannot play a piece 
    that shares an edge with their first played piece; Player 1 should then play
    a legal piece. Verify that Player 2 cannot play a piece that shares an 
    edge with their first played piece; Player 2 should then play a legal 
    piece. Verify that Player 1 can play a piece that shares one or more edges
    with Player 2’s pieces, and vice versa. (This sequence involves six 
    placed pieces in total.)
    """
    blokus = Blokus(2, 6, {(0, 0), (5, 5)})

    assert blokus.curr_player == 1
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((0, 0))
    assert blokus.maybe_place(piece_one)

    assert blokus.curr_player == 2
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((5, 5))
    assert blokus.maybe_place(piece_one)

    assert blokus.curr_player == 1
    piece_3 = Piece(blokus.shapes[ShapeKind.THREE])
    piece_3.set_anchor((0, 2))
    assert not blokus.maybe_place(piece_3)
    piece_3.set_anchor((1, 2))
    assert blokus.maybe_place(piece_3)

    assert blokus.curr_player == 2
    piece_3 = Piece(blokus.shapes[ShapeKind.THREE])
    piece_3.set_anchor((4, 4))
    assert not blokus.maybe_place(piece_3)
    piece_3.set_anchor((4, 3))
    assert blokus.maybe_place(piece_3)

    assert blokus.curr_player == 1
    piece_two = Piece(blokus.shapes[ShapeKind.LETTER_O])
    piece_two.set_anchor((2, 4))
    assert blokus.maybe_place(piece_two)

    assert blokus.curr_player == 2
    piece_two = Piece(blokus.shapes[ShapeKind.LETTER_O])
    piece_two.set_anchor((2, 0))
    assert blokus.maybe_place(piece_two)

def test_require_own_corners_1() -> None:
    """
    Analogous to above but requiring own-corners rather than preventing 
    own-edges:
    Create an instance of any 1-player Blokus game configuration. After placing
    a piece, verify that the player cannot place another piece that shares zero
    corners with their first played piece.
    """
    blokus = init_blokus_mini(1)

    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((0, 0))
    blokus.maybe_place(piece_one)
    
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_two.set_anchor((3, 3))
    assert not blokus.maybe_place(piece_two)
    
def test_require_own_corners_2() -> None:
    """
    Analogous to above but requiring own-corners rather than preventing 
    own-edges:
    Create an instance of any 2-player Blokus game configuration. After Player 1
    and Player 2 each play a piece, verify that Player 1 cannot play a piece that
    shares zero corners with their first played piece; Player 1 should then 
    play a legal piece. Verify that Player 2 cannot play a piece that shares 
    zero corners with their first played piece; Player 2 should then play a 
    legal piece. Verify that Player 1 can play a piece that shares zero corners
    with Player 2’s pieces, and vice versa. (In sum, this sequence involves 
    six placed pieces.)
    """
    blokus = Blokus(2, 6, {(0, 0), (5, 5)})

    assert blokus.curr_player == 1
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((0, 0))
    assert blokus.maybe_place(piece_one)

    assert blokus.curr_player == 2
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((5, 5))
    assert blokus.maybe_place(piece_one)

    assert blokus.curr_player == 1
    piece_3 = Piece(blokus.shapes[ShapeKind.THREE])
    piece_3.set_anchor((0, 3))
    assert not blokus.maybe_place(piece_3)
    piece_3.set_anchor((1, 2))
    assert blokus.maybe_place(piece_3)

    assert blokus.curr_player == 2
    piece_3 = Piece(blokus.shapes[ShapeKind.THREE])
    piece_3.set_anchor((4, 2))
    assert not blokus.maybe_place(piece_3)
    piece_3.set_anchor((4, 3))
    assert blokus.maybe_place(piece_3)

    assert blokus.curr_player == 1
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_two.set_anchor((0, 4))
    assert blokus.maybe_place(piece_two)

    assert blokus.curr_player == 2
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_two.set_anchor((5, 0))
    assert blokus.maybe_place(piece_two)
    
def test_some_available_moves() -> None:
    """
    Create an instance of any Blokus game configuration. Verify that 
    available_moves is non-empty. Play a few pieces, and verify that the number
    of available_moves decreases after each step.
    """
    blokus = init_blokus_mini(1)

    assert blokus.available_moves() != set()

    len_1 = len(blokus.available_moves())
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((0, 0))
    blokus.maybe_place(piece_one)
    
    len_2 = len(blokus.available_moves())
    assert len_2 < len_1
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_two.set_anchor((1, 1))
    blokus.maybe_place(piece_two)

    len_3 = len(blokus.available_moves())
    assert len_3 < len_2
    piece_O = Piece(blokus.shapes[ShapeKind.LETTER_O])
    piece_O.set_anchor((2, 3))
    blokus.maybe_place(piece_O)

    len_4 = len(blokus.available_moves())
    assert len_4 < len_3

def test_no_available_moves() -> None:
    """
    Create an instance of any Blokus game configuration. Play pieces until there
    are no more available moves, and verify that available_moves is empty.
    """
    blokus = init_blokus_mini(1)

    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((0, 0))
    assert blokus.maybe_place(piece_one)
    
    piece_O = Piece(blokus.shapes[ShapeKind.LETTER_O])
    piece_O.set_anchor((1, 1))
    assert blokus.maybe_place(piece_O)

    piece_2 = Piece(blokus.shapes[ShapeKind.TWO])
    piece_2.set_anchor((0, 3))
    assert blokus.maybe_place(piece_2)

    piece_C = Piece(blokus.shapes[ShapeKind.C])
    piece_C.set_anchor((4, 0))
    piece_C.rotate_left()
    assert blokus.maybe_place(piece_C)

    piece_A = Piece(blokus.shapes[ShapeKind.A])
    piece_A.set_anchor((3, 4))
    piece_A.rotate_left()
    assert blokus.maybe_place(piece_A)

    assert len(blokus.available_moves()) == 0


def place_many_pieces() -> None:
    """
    This helper is designed to place 19 pieces, so that the final pieces
    played can be changed.
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

def test_15_points() -> None:
    """
    Simulate a game where a player scores 15 points, that is, plays all 21 of 
    their pieces! You can do this for any game configuration you like. After all
    21 pieces are played, then — either right away, or after other players, 
    if any, continue playing — verify the expected values for get_score(), 
    game_over, winners, and remaining_shapes. The last three tests in 
    test_fake.py may provide some inspiration for strategizing how to test 
    such long sequences of moves.
    """
    blokus = place_many_pieces()

    piece = Piece(blokus.shapes[ShapeKind.ONE])
    piece.set_anchor((1, 4))
    assert blokus.maybe_place(piece)

    piece = Piece(blokus.shapes[ShapeKind.N])
    piece.set_anchor((2, 7))
    piece.rotate_right()
    assert blokus.maybe_place(piece)
    
    assert blokus.game_over
    assert blokus.get_score(1) == -89
    assert blokus.get_score(2) == 15
    assert blokus.winners == [2]
    
def test_20_points() -> None:
    """
    Same as above, but where a player scores 20 points, that is, plays all 21 
    pieces with ONE as the last piece played. The sequence of moves in this test
    can be very similar to the previous test. If so, factor your code in a way
    that avoids a giant amount of copy-pasted code.
    """
    blokus = place_many_pieces()

    piece = Piece(blokus.shapes[ShapeKind.N])
    piece.set_anchor((1, 6))
    piece.rotate_right()
    assert blokus.maybe_place(piece)
    
    piece = Piece(blokus.shapes[ShapeKind.ONE])
    piece.set_anchor((3, 8))
    assert blokus.maybe_place(piece)

    assert blokus.game_over
    assert blokus.get_score(1) == -89
    assert blokus.get_score(2) == 20
    assert blokus.winners == [2]

