import sys
import curses
import random
from base import BlokusBase, Grid
from fakes import BlokusFake, BlokusStub
from piece import Piece
from shape_definitions import ShapeKind


class TUI:



    def __init__(self, stdscr):
        """
        Constructor for TUI class
        """
        self.stdscr = stdscr
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        self.setup_game()

    def select_pending_piece(self) -> None:
        """
        Randomly picks a pending piece.

        Inputs:
            None
            
        """
        shapes_left: list[ShapeKind] = list(self.game.shapes.keys())
        some_shape: ShapeKind = random.choice(shapes_left)
        self.pending_piece: Piece = Piece(self.game.shapes[some_shape])
        self.pending_piece.set_anchor((self.game.size // 2, self.game.size // 2))

    def setup_game(self):
        """

        """
        if len(sys.argv) != 2:
            self.stdscr.addstr('Usage: python3 src/tui.py [BOARD_SIZE|duo|mono]\n', curses.color_pair(2))
            self.stdscr.refresh()
            self.stdscr.getch()
            sys.exit(1)
        arg: int | str = sys.argv[1]
        if arg.isdigit():
            size: int = int(arg)
            assert 5 <= size <= 20
            self.game: BlokusFake = BlokusFake(2, size, {(0, 0), (size - 1, size - 1)})
        elif arg == 'mono':
            self.game: BlokusFake = BlokusFake(2, 11, {(5, 5)})
        elif arg == 'duo':
            self.game: BlokusFake = BlokusFake(2, 14, {(4, 4), (9, 9)})
        else:
            self.stdscr.addstr('Please input a valid argument\n', curses.color_pair(1))
            self.stdscr.refresh()
            self.stdscr.getch()
            sys.exit(1)
        self.select_pending_piece()

    def draw_board(self):
        """
        """
        self.stdscr.clear()
        nrows, ncols = self.game.size, self.game.size
        for r in range(nrows):
            for c in range(ncols):
                cell: tuple[int, ShapeKind] = self.game.grid[r][c]
                char: str = '█'
                color = curses.color_pair(1)
                if cell is None: 
                    if (r, c) in self.game.start_positions:
                        color = curses.color_pair(4)
                        char = '▋'
                    if self.pending_piece and (r, c) in self.pending_piece.squares():
                        color = curses.color_pair(self.game.curr_player + 1)
                        char: str = '▋'
                if cell is not None:
                    player, _ = cell
                    color = curses.color_pair(player + 1)
                    char: str = '▋'
                self.stdscr.addstr(r + 2, c * 2, char, color)
            self.stdscr.addstr(r + 2, ncols * 2, '\n', curses.color_pair(1))
        self.stdscr.refresh()

    def handle_movement(self, key):
        """
        """
        row, col = self.pending_piece.anchor
        new_col = None
        new_row = None
        if key == curses.KEY_LEFT:
            new_col = col - 1
        elif key == curses.KEY_RIGHT:
            new_col = min(col + 1, self.game.size - 1)
        elif key == curses.KEY_UP:
            new_row = max(row - 1, 0)
        elif key == curses.KEY_DOWN:
            new_row = min(row + 1, self.game.size - 1)
        if new_row is None:
            new_row = row
        if new_col is None:
            new_col = col
        self.pending_piece.set_anchor((new_row, new_col))
        if self.game.any_wall_collisions(self.pending_piece):
            self.pending_piece.set_anchor((row, col))

    def main_loop(self) -> None:
        """

        """
        while True:
            self.draw_board()
            key = self.stdscr.getch()
            if key in [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN]:
                self.handle_movement(key)
            elif key == 10:
                if self.game.maybe_place(self.pending_piece):
                    self.select_pending_piece()
                if self.game.game_over:
                    break
            elif key == 27:
                break
        self.stdscr.refresh()
        self.stdscr.getch()

def main(stdscr) -> None:
    """

    """
    tui = TUI(stdscr)
    tui.main_loop()

if __name__ == '__main__':
    curses.wrapper(main)
