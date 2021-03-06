import random

from grid import Grid
from moves import MOVEMENT_NONE, MOVEMENT_LEFT, MOVEMENT_RIGHT, MOVEMENT_DOWN, MOVEMENT_UP
from piece import PieceFactory


class Game:
    def __init__(self, grid_size=20):
        self.grid_size = grid_size

    def play(self):
        grid = Grid(size=self.grid_size)
        piece_factory = PieceFactory()
        game_over = False
        piece = piece_factory.get_piece(9, 0)

        current_piece = self.add_piece_to_grid(grid, piece)
        grid.render()

        while not game_over:
            grid.remove_piece(current_piece)
            moved = False
            if grid.do_piece_has_valid_move(current_piece):
                player_move = self.get_player_move()
                # Avoid double move down
                if player_move is not MOVEMENT_NONE:
                    moved_piece = current_piece.move(player_move)

                    if grid.can_add_piece(moved_piece):
                        current_piece = moved_piece
                        moved = True

            moved_piece = current_piece.move(MOVEMENT_NONE)
            if grid.can_add_piece(moved_piece):
                current_piece = moved_piece
                moved = True

            self.add_piece_to_grid(grid, current_piece)
            if not moved:
                spawn_x_pos = random.randint(1, 17)
                piece = piece_factory.get_piece(spawn_x_pos, 0)
                current_piece = self.add_piece_to_grid(grid, piece)
                if not current_piece:
                    game_over = True
            grid.render()

    @staticmethod
    def add_piece_to_grid(grid, piece):

        if grid.can_add_piece(piece):
            grid.add_piece(piece)
        else:
            return None
        return piece

    def get_player_move(self):
        player_input = self.get_player_input()
        move = None
        if player_input in ["a", "A"]:
            move = MOVEMENT_LEFT
        elif player_input in ["s", "S"]:
            move = MOVEMENT_DOWN
        elif player_input in ["d", "D"]:
            move = MOVEMENT_RIGHT
        elif player_input in ["w", "W"]:
            move = MOVEMENT_UP
        elif player_input in ["", " "]:
            move = MOVEMENT_NONE

        return move

    @staticmethod
    def get_player_input():
        allowed_input = ["a", "A", "s", "S", "d", "D", "w", "W", "", " "]
        raw_input = None
        while raw_input not in allowed_input:
            raw_input = input(f"Choose input from {allowed_input}. Your choice is: ")

        return raw_input
