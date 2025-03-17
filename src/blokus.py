from abc import ABC, abstractmethod
from typing import Optional

from shape_definitions import ShapeKind, definitions
from piece import Point, Shape, Piece
from base import BlokusBase, Grid

Cell = Optional[tuple[int, ShapeKind]]

class Blokus(BlokusBase):
    """
    Abstract base class for Blokus."""

    _num_players: int
    _size: int
    _start_positions: set[Point]

    def __init__(
        self,
        num_players: int,
        size: int,
        start_positions: set[Point],
    ) -> None:
        """
        Subclasses should have constructors which accept these
        same first three arguments:

            num_players: Number of players
            size: Number of squares on each side of the board
            start_positions: Positions for players' first moves

        Raises ValueError...
            if num_players is less than 1 or more than 4,
            if the size is less than 5,
            if not all start_positions are on the board, or
            if there are fewer start_positions than num_players.
        """
        if num_players < 1 or num_players > 4:
            raise ValueError("Incorrect # of players.")
        if size < 5:
            raise ValueError("Incorrect size")
        for tup in start_positions:
            r, c = tup
            if r > size or c > size:
                raise ValueError("Start position not on board.")
        if len(start_positions) < num_players:
            raise ValueError("Fewer start positions than # of players.")
            
        super().__init__(num_players, size, start_positions)

        self._curr_player = 1

        self._grid = [[None] * size for _ in range(size)]

        self._shapes : dict[ShapeKind, Shape] = {}
        for key, val in definitions.items():
            self._shapes[key] = Shape.from_string(key, val)

        self._scores : dict[int, int] = {}
        for player in range(1, self.num_players + 1):
            self._scores[player] = -89

        self._retired_players : set[int] = set()

        self._placed_pieces : dict[int, set[Piece]] = {}
        for player in range(1, self.num_players + 1):
            self._placed_pieces[player] = set()
    
    @property
    def shapes(self) -> dict[ShapeKind, Shape]:
        return self._shapes

    @property
    def size(self) -> int:
        return self._size

    @property
    def start_positions(self) -> set[Point]:
        return self._start_positions

    @property
    def num_players(self) -> int:
        return self._num_players

    @property
    def curr_player(self) -> int:
        return self._curr_player

    @property
    def retired_players(self) -> set[int]:
        return self._retired_players
    
    @property
    def placed_pieces(self) -> dict[int, Piece]:
        return self._placed_pieces

    @property
    def grid(self) -> Grid:
        return self._grid

    @property
    def game_over(self) -> bool:
        condition_1 = len(self._retired_players) == self._num_players
        condition_2 = True
        for player in range(1, self._num_players + 1):
            if len(self.remaining_shapes(player)) > 0 and \
                    player not in self.retired_players:
                condition_2 = False
        return condition_1 or condition_2

    @property
    def winners(self) -> Optional[list[int]]:
        if self.game_over:
            scores = {} 
            for player in range(1, self._num_players + 1):
                scores[player] = self.get_score(player)
            winning_score = max(scores.values())
            winners = []
            for player, score in scores.items():
                if score == winning_score:
                    winners.append(player)
            return winners
        return []

    #
    # METHODS
    #

    def remaining_shapes(self, player: int) -> list[ShapeKind]:
        shapes_played = set()
        for row in self.grid:
            for tup in row:
                if tup is not None:
                    grid_player, kind = tup
                    if grid_player == player:
                        shapes_played.add(kind)
        shapes_not_played = []
        for kind in self.shapes:
            if kind not in shapes_played:
                shapes_not_played.append(kind)
        return shapes_not_played

    def any_wall_collisions(self, piece: Piece) -> bool:
        if (piece.anchor is None) or (piece.shape.kind not in
                                      self.remaining_shapes(self.curr_player)):
            raise ValueError
        for point in piece.squares():
            r,c = point
            if not (0 <= r < self.size and 0 <= c < self.size):
                return True
        return False

    def any_collisions(self, piece: Piece) -> bool:
        if (piece.anchor is None) or (piece.shape.kind not in
                                      self.remaining_shapes(self.curr_player)):
            raise ValueError

        if self.any_wall_collisions(piece):
            return True
        for point in piece.squares():
            r,c = point
            if self.grid[r][c] is not None:
                return True
        return False

    def legal_to_place(self, piece: Piece) -> bool:
        if self.any_collisions(piece):
            return False

        if len(self.remaining_shapes(self.curr_player)) == 21:
            for position in self._start_positions:
                for point in piece.squares():
                    if position == point:
                        return True
            return False

        condition_3 = False
        for placed_piece in self.placed_pieces[self.curr_player]:
            for corner in placed_piece.intercardinal_neighbors():
                for point in piece.squares():
                    if corner == point:
                        condition_3 = True
        for placed_piece in self.placed_pieces[self.curr_player]:
            for edge in placed_piece.cardinal_neighbors():
                if edge in piece.squares():
                    condition_3 = False

        return condition_3

    def maybe_place(self, piece: Piece) -> bool:
        if self.legal_to_place(piece):
            self._placed_pieces[self.curr_player].add(piece)
            if len(self.placed_pieces[self.curr_player]) == 21:
                if piece.shape.kind == ShapeKind.ONE:
                    self._scores[self.curr_player] += 20
                else:
                    self._scores[self.curr_player] += 15
            for point in piece.squares():
                r,c = point
                self.grid[r][c] = (self.curr_player, piece.shape.kind)
                self._scores[self.curr_player] += 1
            while True:
                self._curr_player = (self._curr_player % self._num_players) + 1
                if not self.curr_player in self.retired_players:
                    break
            return True
        return False

    def retire(self) -> None:
        self._retired_players.add(self.curr_player)
        self._curr_player = (self._curr_player % self._num_players) + 1

    def get_score(self, player: int) -> int:
        return self._scores[player]

    def available_moves(self) -> set[Piece]:

        available_spots = []
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] is None:
                    available_spots.append((r, c))

        moves = set()

        for shape in self.remaining_shapes(self.curr_player):
            piece = Piece(self.shapes[shape])
            flipped_piece = Piece(self.shapes[shape])
            for spot in available_spots:
                piece.set_anchor(spot)
                for _ in range(4):
                    piece.rotate_right()
                    if self.legal_to_place(piece):
                        moves.add(piece)
                
                flipped_piece.set_anchor(spot)
                flipped_piece.flip_horizontally()
                for _ in range(4):
                    flipped_piece.rotate_right()
                    if self.legal_to_place(flipped_piece):
                        moves.add(flipped_piece)

        return moves
        


    