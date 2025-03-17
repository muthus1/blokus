"""
Fake implementations of BlokusBase.

We provide a BlokusStub implementation, and
you must provide a BlokusFake implementation.
"""
from shape_definitions import ShapeKind, definitions
from piece import Point, Shape, Piece
from base import BlokusBase, Grid


class BlokusStub(BlokusBase):
    """
    Stub implementation of BlokusBase.

    This stub implementation behaves according to the following rules:

    - It only supports two players.
    - Only three of the 21 Blokus shapes are available:
      the one-square, two-square, and three-square straight pieces.
    - Players are allowed to place pieces in any position of the board
      they want, even if the piece collides with any squares of
      previously played pieces (squares of the new piece replace any
      conflicting ones).
    - Board positions are not validated. If a method is called with
      a position outside the board, it will likely cause an exception.
    - There is no consideration of start positions for a player's
      first move.
    - The constructor simulates two initial moves: placing
      Player 1's "1" piece in the top-left corner and
      Player 2's "2" piece in the bottom-right corner.
    - The game ends after six moves. The player, if any, who has a
      piece occupying the top-right corner of the board wins.
      Otherwise, the players tie.
    - The `remaining_shapes` method always says all three shapes remain.
    - The only shape that is considered available by `available_moves`
      is the one-square shape, and it is considered available everywhere
      on the board regardless of whether the corresponding positions are
      available or occupied.
    - Several methods return simple, unhelpful results (as opposed to
      raising NotImplementedErrors).
    """

    _shapes: dict[ShapeKind, Shape]
    _size: int
    _num_players: int
    _curr_player: int
    _grid: Grid
    _num_moves: int

    def __init__(
        self,
        num_players: int,
        size: int,
        start_positions: set[Point],
    ) -> None:
        """
        Constructor (See BlokusBase)

        This stub initializes a counter for number of moves
        in order to implement a simple game_over condition.

        Once everything is initialized, this stub implementation
        "simulates" two moves.
        """
        super().__init__(num_players, size, start_positions)
        self._shapes = self._load_shapes()
        self._size = size
        self._num_players = 2
        self._curr_player = 1
        self._grid = [[None] * size for _ in range(size)]
        self._num_moves = 0
        self._simulate_two_moves()

    def _load_shapes(self) -> dict[ShapeKind, Shape]:
        """
        Rather than reading in the representations of shapes
        from shape_definitions.py, this method manually builds
        three of the 21 kinds of shapes.

        See shape_definitions.py for more details.
        """
        # See shape_definitions.definitions[ShapeKind.ONE]
        shape_1 = Shape(ShapeKind.ONE, (0, 0), False, [(0, 0)])

        # See shape_definitions.definitions[ShapeKind.TWO]
        shape_2 = Shape(ShapeKind.TWO, (0, 0), True, [(0, 0), (0, 1)])

        # See shape_definitions.definitions[ShapeKind.THREE]
        shape_3 = Shape(
            ShapeKind.THREE, (0, 1), True, [(0, -1), (0, 0), (0, 1)]
        )

        return {
            ShapeKind.ONE: shape_1,
            ShapeKind.TWO: shape_2,
            ShapeKind.THREE: shape_3,
        }

    def _simulate_two_moves(self) -> None:
        """
        Simulates two moves:

        - Player 1 places their ShapeKind.ONE piece in the top-left corner.
        - Player 2 places their ShapeKind.TWO piece in the bottom-right corner.

        This drives the game into a state where four more pieces
        can be played before entering the game_over condition
        (six moves total).
        """
        piece_1 = Piece(self.shapes[ShapeKind.ONE])
        piece_1.set_anchor((0, 0))
        self.maybe_place(piece_1)

        # This anchor position accounts for the origin of
        # ShapeKind.TWO as specified in shape_definitions.py.
        piece_2 = Piece(self.shapes[ShapeKind.TWO])
        piece_2.set_anchor((self.size - 1, self.size - 2))
        self.maybe_place(piece_2)

    @property
    def shapes(self) -> dict[ShapeKind, Shape]:
        """
        See BlokusBase
        """
        return self._shapes

    @property
    def size(self) -> int:
        """
        See BlokusBase
        """
        return self._size

    @property
    def start_positions(self) -> set[Point]:
        """
        See BlokusBase
        """
        return set()

    @property
    def num_players(self) -> int:
        """
        See BlokusBase
        """
        return self._num_players

    @property
    def curr_player(self) -> int:
        """
        See BlokusBase
        """
        return self._curr_player

    @property
    def retired_players(self) -> set[int]:
        """
        See BlokusBase
        """
        return set()

    @property
    def grid(self) -> Grid:
        """
        See BlokusBase
        """
        return self._grid

    @property
    def game_over(self) -> bool:
        """
        See BlokusBase
        """
        return self._num_moves == 6

    @property
    def winners(self) -> list[int]:
        """
        See BlokusBase
        """
        top_right_cell = self.grid[0][self.size - 1]
        if top_right_cell is None:
            return [1, 2]
        else:
            winner = top_right_cell[0]
            return [winner]

    def remaining_shapes(self, player: int) -> list[ShapeKind]:
        """
        See BlokusBase
        """
        return [ShapeKind.ONE, ShapeKind.TWO, ShapeKind.THREE]

    def any_wall_collisions(self, piece: Piece) -> bool:
        """
        See BlokusBase
        """
        return False

    def any_collisions(self, piece: Piece) -> bool:
        """
        See BlokusBase
        """
        return False

    def legal_to_place(self, piece: Piece) -> bool:
        """
        See BlokusBase
        """
        return True

    def maybe_place(self, piece: Piece) -> bool:
        """
        See BlokusBase
        """
        for r, c in piece.squares():
            self._grid[r][c] = (self.curr_player, piece.shape.kind)
        self._curr_player = (self.curr_player % self.num_players) + 1
        self._num_moves += 1
        return True

    def retire(self) -> None:
        """
        See BlokusBase
        """
        pass

    def get_score(self, player: int) -> int:
        """
        See BlokusBase
        """
        return -999

    def available_moves(self) -> set[Piece]:
        """
        See BlokusBase
        """
        pieces = set()
        for r in range(self.size):
            for c in range(self.size):
                piece = Piece(self.shapes[ShapeKind.ONE])
                piece.set_anchor((r, c))
                pieces.add(piece)

        return pieces


class BlokusFake(BlokusBase):
    """
    Fake implementation of Blokus for Milestone 1

    New attributes:
        retired_players : a set keeping track of retired players by player
            number
    """
    _shapes: dict[ShapeKind, Shape]
    _size: int
    _num_players: int
    _curr_player: int
    _grid: Grid
    _retired_players : set[int]
    _scores : dict[int, int]

    def __init__(self, num_players: int,
                  size: int, start_positions: set[Point]) -> None:
        """
        Constructor for Blokus Fake
        """
        super().__init__(num_players, size, start_positions)
        assert num_players < 3
        self._curr_player = 1
        self._grid = [[None] * size for _ in range(size)]
        self._shapes : dict[ShapeKind, Shape] = {}
        for key, val in definitions.items():
            self._shapes[key] = Shape.from_string(key, val)
        self._scores : dict[int, int] = {}
        for player in range(1, self.num_players + 1):
            self._scores[player] = -89
        self._retired_players : set[int] = set()

    @property  
    def shapes(self):
        """
        See Blokus Base
        """
        return self._shapes

    @property
    def size(self) -> int:
        """
        See BlokusBase
        """
        return self._size

    @property
    def start_positions(self) -> set[Point]:
        """
        See BlokusBase
        """
        return self._start_positions

    @property
    def num_players(self) -> int:
        """
        See BlokusBase
        """
        return self._num_players

    @property
    def curr_player(self) -> int:
        """
        See BlokusBase
        """
        return self._curr_player

    @property
    def retired_players(self) -> set[int]:
        """
        See BlokusBase
        """
        return self._retired_players

    @property
    def grid(self) -> Grid:
        """
        See BlokusBase
        """
        return self._grid

    @property
    def game_over(self) -> bool:
        """
        See BlokusBase
        """
        condition_1 = len(self._retired_players) == self._num_players
        condition_2 = True
        for player in range(1, self._num_players + 1):
            if len(self.remaining_shapes(player)) > 0 and \
                    player not in self.retired_players:
                condition_2 = False
        return condition_1 or condition_2

    @property
    def winners(self) -> list[int]:
        """
        See BlokusBase
        """
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


    def remaining_shapes(self, player: int) -> list[ShapeKind]:
        """
        See BlokusBase
        """
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
        """
        See BlokusBase
        """
        if (piece.anchor is None) or (piece.shape.kind not in
                                      self.remaining_shapes(self.curr_player)):
            raise ValueError
        for point in piece.squares():
            r,c = point
            if not (0 <= r < self.size and 0 <= c < self.size):
                return True
        return False

    def any_collisions(self, piece: Piece) -> bool:
        """
        See BlokusBase
        """
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
        """
        See BlokusBase
        """
        return not self.any_collisions(piece)

    def maybe_place(self, piece: Piece) -> bool:
        """
        See BlokusBase
        """

        if self.legal_to_place(piece):
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
        """
        See BlokusBase
        """
        self._retired_players.add(self.curr_player)
        self._curr_player = (self._curr_player % self._num_players) + 1
        # while True:
        #     self._curr_player = (self._curr_player % self._num_players) + 1
        #     if not self.curr_player in self.retired_players:
        #         break

    def get_score(self, player: int) -> int:
        """
        See BlokusBase
        """
        return self._scores[player]

    def available_moves(self) -> set[Piece]:
        """
        Returns the set of all possible moves that the current
        player may make. As with the arguments to the maybe_place
        method, a move is determined by a Piece, namely, one of
        the 21 Shapes plus a location and orientation.

        Caveat: inital shape orientations are used
        """
        
        available_spots = []
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] is None:
                    available_spots.append((r, c))

        moves = set()

        for shape in self.remaining_shapes(self.curr_player):
            piece = Piece(self.shapes[shape])
            #checks if piece has been added to short-cut the code
            piece_added = False

            for spot in available_spots:
                if piece_added:
                    continue

                piece.set_anchor(spot)

                if self.legal_to_place(piece):
                    moves.add(piece)
                    piece_added = True

        return moves
