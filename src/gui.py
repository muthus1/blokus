"""
Blokus GUI file

Opens a 5x5 to 20x20 window
"""
import sys
import os
import random
import click
from base import BlokusBase, Grid
from blokus import Blokus
from fakes import BlokusFake
from piece import Piece
from shape_definitions import ShapeKind
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

class GUI:
    """
    Class for GUI of Blokus game
    """
    width_height : int
    disp_height : int
    size : int
    outline : int
    game : "BlokusBase"
    sq_side : int
    sq_grid : Grid
    pend_piece : Piece
    pend_loc : tuple[int, int]
    play_colors : dict[int, tuple[int, int, int]]

    font : pygame.font.Font
    clock : pygame.time.Clock

    def __init__(self, game : "BlokusBase", outline : int = 3) -> None:
        """
        Constructor for GUI of Blokus game

        Parameters:
            dim : length of side in squares of window
            outline : width of the outline of squares and the window
            game : the Blokus game to base the window off of
            sq_side : the length of each grid square
        """
        self.size = game.size
        self.sq_side = 600 // self.size
        self.width_height = self.size * self.sq_side + (self.size + 1) * outline
        self.disp_height = 130
        self.outline = outline
        self.game = game
        self.sq_grid = game.grid
        self.pend_piece = Piece(self.game.shapes[random.choice
                                                 (list(game.shapes.keys()))])
        self.pend_loc = (self.size // 2, self.size // 2)
        self.play_colors = {}
        for player in range(1, self.game.num_players + 1):
            if player % 4 == 0:
                self.play_colors[player] = (255,0,0)
            elif player % 4 == 1:
                self.play_colors[player] = (0,255,0)
            elif player % 4 == 2:
                self.play_colors[player] = (0,0,255)
            else:
                self.play_colors[player] = (255, 165, 0)

        pygame.init()
        pygame.display.set_caption("Blokus")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, size = 26)
        self.surface = pygame.display.set_mode((self.width_height,
                                                 self.width_height + 
                                                 self.disp_height))

        self.event_loop()

    def draw_grid(self) -> None:
        """
        Draws the grid over the window for the Blokus game

        Returns (None) : Nothing, draws
        """
        for i in range(self.size + 1):
            line_pos = i * (self.sq_side + self.outline)
            h_line = pygame.Rect(0, line_pos, self.width_height, self.outline)
            v_line = pygame.Rect(line_pos, 0, self.outline, self.width_height)
            pygame.draw.rect(self.surface, (0,0,0), h_line)
            pygame.draw.rect(self.surface, (0,0,0), v_line)

    def draw_starts(self) -> None:
        """
        Grays out parts of the grid that are start points

        Returns (None) : Nothing, draws
        """
        for pt in self.game.start_positions:
            r,c = pt
            if r < self.size and c < self.size:
                top = (r + 1) * self.outline + r * self.sq_side
                left = (c + 1) * self.outline + c * self.sq_side
                pt_rect = pygame.Rect(left, top, self.sq_side, self.sq_side)
                pygame.draw.rect(self.surface, (173,166,166), pt_rect)

    def draw_display(self) -> None:
        """
        Draw the display showing remaining pieces and current player.

        Returns (None) : Nothing, draws
        """
        temp_font = pygame.font.Font(None, size = 20)
        disp = pygame.Rect(0, self.width_height, self.width_height,
                            self.disp_height)
        pygame.draw.rect(self.surface, (0,0,0), disp)

        curr = self.game.curr_player
        curr_text = self.font.render(f"Current Player: {curr}", True,
                                     (255,255,255))
        score_text = self.font.render("Scores:", True, (255,255,255))
        self.surface.blit(curr_text, (10, self.width_height + 10))
        self.surface.blit(score_text, (10, self.width_height + 30))

        for player in range(1, self.game.num_players + 1):
            score_val = self.game.get_score(player)
            score = temp_font.render(f"Player {player}: {score_val}", True,
                                     (255,255,255))
            self.surface.blit(score, (10, self.width_height + 30 + 20 * player))

        for player in range(1, self.game.num_players + 1):
            remain = self.game.remaining_shapes(player)
            for i, shape in enumerate(self.game.shapes.keys()):
                if (player == self.game.curr_player) and \
                    (shape == self.pend_piece.shape.kind):
                    shape_str = temp_font.render(shape.value, True,
                                                 (255,255,255))
                elif shape in remain:
                    shape_str = temp_font.render(shape.value, True,
                                                 self.play_colors[player])
                else:
                    shape_str = temp_font.render(shape.value, True,
                                                 (97,93,93))
                top_right = (250 + i * 15,
                             self.width_height + 10 + 22 * (player - 1))
                self.surface.blit(shape_str, top_right)

        for player in self.game.retired_players:
            retire_bum = pygame.Rect(250, self.width_height + 13 + 22
                                     * (player - 1), 320, 2)
            retire_text = temp_font.render("Retired!", True, (150,53,53))
            self.surface.blit(retire_text, (580, self.width_height + 10 + 22
                                     * (player - 1)))
            pygame.draw.rect(self.surface, (150,53,53), retire_bum)


    def draw_gameover(self) -> None:
        """
        Draws the game over pop-up.

        Returns (None) : Nothing, draws
        """
        over_rect = pygame.Rect(self.width_height // 2 - 100,
                                self.width_height // 2 - 100, 200, 200)
        pygame.draw.rect(self.surface, (0,0,0), over_rect)

        over_text = self.font.render("Game Over!", True, (253,255,50))
        winner_text = self.font.render("Winners:", True, (255,255,255))
        self.surface.blit(over_text,
                          (self.width_height // 2 - 90, 
                           self.width_height // 2 - 90))
        self.surface.blit(winner_text,
                          (self.width_height // 2 - 90, 
                           self.width_height // 2 - 75))
        for i, winner in enumerate(self.game.winners):
            win_text = self.font.render(f"Player {winner}", True, (255,255,255))
            self.surface.blit(win_text,
                              (self.width_height // 2 - 90,
                               self.width_height // 2 - 60 + (15 * i)))

    def draw_pending(self) -> None:
        """
        Draws the pending piece of the current player

        Returns (None) : Nothing, draws
        """
        self.pend_piece.set_anchor(self.pend_loc)

        for coord in self.pend_piece.squares():
            r, c = coord
            top = r * (self.sq_side + self.outline) + self.outline
            left = c * (self.sq_side + self.outline) + self.outline
            rect = pygame.Rect(left, top, self.sq_side, self.sq_side)
            if not self.game.legal_to_place(self.pend_piece):
                pygame.draw.rect(self.surface, (150,53,53), rect)
            else:
                pygame.draw.rect(self.surface, (253, 255, 50), rect)



    def draw_blocks(self) -> None:
        """
        Draws blocks that are already on the board

        Returns (None) : Nothing, draws
        """
        for i, row in enumerate(self.sq_grid):
            for j, col in enumerate(row):
                if isinstance(col, tuple):
                    top = i * self.sq_side + (i + 1) * self.outline
                    left = j * self.sq_side + (j + 1) * self.outline
                    block = pygame.Rect(left, top,
                                             self.sq_side, self.sq_side)
                    pygame.draw.rect(self.surface, self.play_colors[col[0]],
                                      block)

    def draw_window(self) -> None:
        """
        Draws the window.

        Returns (None) : Nothing, draws.
        """
        self.surface.fill((255,255,255))
        self.draw_grid()
        self.draw_starts()
        self.draw_blocks()
        self.draw_display()
        self.draw_pending()
        if self.game.game_over:
            self.draw_gameover()

    def event_loop(self) -> None:
        """
        Event loop for showing the display.

        Returns (None): Nothing
        """
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    curr = self.game.curr_player
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if not self.game.game_over:
                        if event.key == pygame.K_LEFT:
                            r, c = self.pend_loc
                            self.pend_piece.set_anchor((r, c - 1))
                            if not self.game.any_wall_collisions(self.pend_piece):
                                self.pend_loc = (r, c - 1)
                        elif event.key == pygame.K_RIGHT:
                            r, c = self.pend_loc
                            self.pend_piece.set_anchor((r, c + 1))
                            if not self.game.any_wall_collisions(self.pend_piece):
                                self.pend_loc = (r, c + 1)
                        elif event.key == pygame.K_UP:
                            r, c = self.pend_loc
                            self.pend_piece.set_anchor((r - 1, c))
                            if not self.game.any_wall_collisions(self.pend_piece):
                                self.pend_loc = (r - 1, c)
                        elif event.key == pygame.K_DOWN:
                            r, c = self.pend_loc
                            self.pend_piece.set_anchor((r + 1, c))
                            if not self.game.any_wall_collisions(self.pend_piece):
                                self.pend_loc = (r + 1, c)
                        elif event.key == pygame.K_RETURN:
                            self.pend_piece.set_anchor(self.pend_loc)
                            if self.game.maybe_place(self.pend_piece):
                                curr = self.game.curr_player
                                self.pend_piece = Piece(self.game.shapes
                                                        [random.choice
                                                        (self.game.remaining_shapes
                                                        (curr))])
                                self.pend_loc = (self.size // 2, self.size // 2)
                        elif event.key == pygame.K_1:
                            if (self.pend_piece.shape.kind !=  ShapeKind.ONE) \
                                and (ShapeKind.ONE in
                                     self.game.remaining_shapes(curr)):
                                self.pend_loc = (self.size // 2, self.size // 2)
                                self.pend_piece = Piece(self.game.shapes
                                                        [ShapeKind.ONE])
                        elif event.key == pygame.K_2:
                            if (self.pend_piece.shape.kind !=  ShapeKind.TWO) \
                                and (ShapeKind.TWO in
                                     self.game.remaining_shapes(curr)):
                                self.pend_loc = (self.size // 2, self.size // 2)
                                self.pend_piece = Piece(self.game.shapes
                                                        [ShapeKind.TWO])
                        elif event.key == pygame.K_3:
                            if (self.pend_piece.shape.kind !=  ShapeKind.THREE)\
                                and (ShapeKind.THREE in
                                     self.game.remaining_shapes(curr)):
                                self.pend_loc = (self.size // 2, self.size // 2)
                                self.pend_piece = Piece(self.game.shapes
                                                        [ShapeKind.THREE])
                        elif event.key == pygame.K_4:
                            if (self.pend_piece.shape.kind !=  ShapeKind.FOUR)\
                                and (ShapeKind.FOUR in
                                     self.game.remaining_shapes(curr)):
                                self.pend_loc = (self.size // 2, self.size // 2)
                                self.pend_piece = Piece(self.game.shapes
                                                        [ShapeKind.FOUR])
                        elif event.key == pygame.K_5:
                            if (self.pend_piece.shape.kind !=  ShapeKind.FIVE)\
                                and (ShapeKind.FIVE in
                                     self.game.remaining_shapes(curr)):
                                self.pend_loc = (self.size // 2, self.size // 2)
                                self.pend_piece = Piece(self.game.shapes
                                                        [ShapeKind.FIVE])
                        elif event.key == pygame.K_7:
                            if (self.pend_piece.shape.kind !=  ShapeKind.SEVEN)\
                                and (ShapeKind.SEVEN in
                                     self.game.remaining_shapes(curr)):
                                self.pend_loc = (self.size // 2, self.size // 2)
                                self.pend_piece = Piece(self.game.shapes
                                                        [ShapeKind.SEVEN])
                        elif event.key == pygame.K_a:
                            if (self.pend_piece.shape.kind !=  ShapeKind.A)\
                                and (ShapeKind.A in
                                     self.game.remaining_shapes(curr)):
                                self.pend_loc = (self.size // 2, self.size // 2)
                                self.pend_piece = Piece(self.game.shapes
                                                        [ShapeKind.A])
                        elif event.key == pygame.K_c:
                            if (self.pend_piece.shape.kind !=  ShapeKind.C)\
                                and (ShapeKind.C in
                                     self.game.remaining_shapes(curr)):
                                self.pend_loc = (self.size // 2, self.size // 2)
                                self.pend_piece = Piece(self.game.shapes
                                                        [ShapeKind.C])
                        elif event.key == pygame.K_f:
                            if (self.pend_piece.shape.kind !=  ShapeKind.F)\
                                and (ShapeKind.F in
                                     self.game.remaining_shapes(curr)):
                                self.pend_loc = (self.size // 2, self.size // 2)
                                self.pend_piece = Piece(self.game.shapes
                                                        [ShapeKind.F])
                        elif event.key == pygame.K_s:
                            if (self.pend_piece.shape.kind !=  ShapeKind.S)\
                                and (ShapeKind.S in
                                     self.game.remaining_shapes(curr)):
                                self.pend_loc = (self.size // 2, self.size // 2)
                                self.pend_piece = Piece(self.game.shapes
                                                        [ShapeKind.S])
                        elif event.key == pygame.K_l:
                            if (self.pend_piece.shape.kind !=  ShapeKind.L)\
                                and (ShapeKind.L in
                                     self.game.remaining_shapes(curr)):
                                self.pend_loc = (self.size // 2, self.size // 2)
                                self.pend_piece = Piece(self.game.shapes
                                                        [ShapeKind.L])
                        elif event.key == pygame.K_n:
                            if (self.pend_piece.shape.kind !=  ShapeKind.N)\
                                and (ShapeKind.N in
                                     self.game.remaining_shapes(curr)):
                                self.pend_loc = (self.size // 2, self.size // 2)
                                self.pend_piece = Piece(self.game.shapes
                                                        [ShapeKind.N])
                        elif event.key == pygame.K_o:
                            if (self.pend_piece.shape.kind!=ShapeKind.LETTER_O)\
                                and (ShapeKind.LETTER_O in
                                     self.game.remaining_shapes(curr)):
                                self.pend_loc = (self.size // 2, self.size // 2)
                                self.pend_piece = Piece(self.game.shapes
                                                        [ShapeKind.LETTER_O])
                        elif event.key == pygame.K_p:
                            if (self.pend_piece.shape.kind !=  ShapeKind.P)\
                                and (ShapeKind.P in
                                     self.game.remaining_shapes(curr)):
                                self.pend_loc = (self.size // 2, self.size // 2)
                                self.pend_piece = Piece(self.game.shapes
                                                        [ShapeKind.P])
                        elif event.key == pygame.K_t:
                            if (self.pend_piece.shape.kind !=  ShapeKind.T)\
                                and (ShapeKind.T in
                                     self.game.remaining_shapes(curr)):
                                self.pend_loc = (self.size // 2, self.size // 2)
                                self.pend_piece = Piece(self.game.shapes
                                                        [ShapeKind.T])
                        elif event.key == pygame.K_u:
                            if (self.pend_piece.shape.kind !=  ShapeKind.U)\
                                and (ShapeKind.U in
                                     self.game.remaining_shapes(curr)):
                                self.pend_loc = (self.size // 2, self.size // 2)
                                self.pend_piece = Piece(self.game.shapes
                                                        [ShapeKind.U])
                        elif event.key == pygame.K_v:
                            if (self.pend_piece.shape.kind !=  ShapeKind.V)\
                                and (ShapeKind.V in
                                     self.game.remaining_shapes(curr)):
                                self.pend_loc = (self.size // 2, self.size // 2)
                                self.pend_piece = Piece(self.game.shapes
                                                        [ShapeKind.V])
                        elif event.key == pygame.K_w:
                            if (self.pend_piece.shape.kind !=  ShapeKind.W)\
                                and (ShapeKind.W in
                                     self.game.remaining_shapes(curr)):
                                self.pend_loc = (self.size // 2, self.size // 2)
                                self.pend_piece = Piece(self.game.shapes
                                                        [ShapeKind.W])
                        elif event.key == pygame.K_x:
                            if (self.pend_piece.shape.kind !=  ShapeKind.X)\
                                and (ShapeKind.X in
                                     self.game.remaining_shapes(curr)):
                                self.pend_loc = (self.size // 2, self.size // 2)
                                self.pend_piece = Piece(self.game.shapes
                                                        [ShapeKind.X])
                        elif event.key == pygame.K_y:
                            if (self.pend_piece.shape.kind !=  ShapeKind.Y)\
                                and (ShapeKind.Y in
                                     self.game.remaining_shapes(curr)):
                                self.pend_loc = (self.size // 2, self.size // 2)
                                self.pend_piece = Piece(self.game.shapes
                                                        [ShapeKind.Y])
                        elif event.key == pygame.K_z:
                            if (self.pend_piece.shape.kind !=  ShapeKind.Z)\
                                and (ShapeKind.Z in
                                     self.game.remaining_shapes(curr)):
                                self.pend_loc = (self.size // 2, self.size // 2)
                                self.pend_piece = Piece(self.game.shapes
                                                        [ShapeKind.Z])
                        elif event.key == pygame.K_r:
                            self.pend_piece.set_anchor(self.pend_loc)
                            self.pend_piece.rotate_right()
                            if self.game.any_wall_collisions(self.pend_piece):
                                self.pend_piece.rotate_left()
                        elif event.key == pygame.K_e:
                            self.pend_piece.set_anchor(self.pend_loc)
                            self.pend_piece.rotate_left()
                            if self.game.any_wall_collisions(self.pend_piece):
                                self.pend_piece.rotate_right()
                        elif event.key == pygame.K_SPACE:
                            self.pend_piece.set_anchor(self.pend_loc)
                            self.pend_piece.flip_horizontally()
                            if self.game.any_wall_collisions(self.pend_piece):
                                self.pend_piece.flip_horizontally()
                        elif event.key == pygame.K_q:
                            self.game.retire()
                            curr = self.game.curr_player
                            self.pend_piece = Piece(self.game.shapes
                                                        [random.choice
                                                        (self.game.remaining_shapes
                                                        (curr))])

                self.draw_window()
                pygame.display.update()
                self.clock.tick(24)


@click.command
@click.option('-n', '--num-players', default=2, help='number of players')
@click.option('-s', '--size', default=14, help='board size')
@click.option('-p', '--start-position', nargs=2, 
              multiple=True, default=((4,4),(9,9)), help='start points')
@click.option('--game', type=click.Choice(['duo', 'mono','classic-2'
                                           ,'classic-3','classic-4']))
def main_gui(num_players, size, start_position, game):
    """
    click command for gui
    """
    if game is not None:
        if game == 'duo':
            GUI(Blokus(2, 14, {(4,4), (9,9)}))
        elif game == 'mono':
            GUI(Blokus(1, 11, {(5,5)}))
        elif game == 'classic-2':
            GUI(Blokus(2, 20, {(0,0), (0, 19), (19, 0), (19, 19)}))
        elif game == 'classic-3':
            GUI(Blokus(3, 20, {(0,0), (0, 19), (19, 0), (19, 19)}))
        elif game == 'classic-4':
            GUI(Blokus(4, 20, {(0,0), (0, 19), (19, 0), (19, 19)}))
    else:
        starts = set(start_position)
        GUI(Blokus(num_players, size, starts))

if __name__ == "__main__":
    main_gui()