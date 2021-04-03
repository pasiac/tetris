# GRID RELATED
import copy

from moves import POSSIBLE_MOVES
from position import Position

NONE = 0
WALL = 1
PIECE = 2


class Grid:
    def __init__(self, size):
        grid_squares = []
        for column_index in range(0, size):
            column = []
            for row_index in range(0, size):
                column.append(GridCell(x=row_index, y=column_index))
            grid_squares.append(column)

        self.size = size
        self.grid_squares = grid_squares
        self._populate_with_walls()

    def _populate_with_walls(self):
        for grid_row in self.grid_squares:
            for grid_cell in grid_row:
                if self._is_wall(grid_cell):
                    grid_cell.occupied_by = WALL

    def _is_wall(self, grid_cell):
        position = grid_cell.position
        return any([
            position.y == self.size - 1,
            position.x == 0,
            position.x == self.size - 1,
        ])

    def add_piece(self, piece):
        piece_position_matrix = piece.get_piece_positions_matrix()
        for position in piece_position_matrix:
            self.grid_squares[position.y][position.x].fill(PIECE)

    def remove_piece(self, piece):
        piece_position_matrix = piece.get_piece_positions_matrix()
        for position in piece_position_matrix:
            self.grid_squares[position.y][position.x].clear()

    def can_add_piece(self, piece):
        piece_position_matrix = piece.get_piece_positions_matrix()
        is_position_available = []
        for position in piece_position_matrix:
            try:
                grid_cell = self.grid_squares[position.y][position.x]
            except IndexError:
                return False
            is_position_available.append(grid_cell.is_empty() and self._is_position_within_bounds(position))
        return all(is_position_available)

    def _is_position_within_bounds(self, position):
        x_bounds = (1, self.size - 2)
        y_bounds = (0, self.size - 1)
        within_bounds_conditions = [
            position.x >= x_bounds[0], position.x <= x_bounds[1],
            position.y >= y_bounds[0], position.y <= y_bounds[1]
        ]
        return all(within_bounds_conditions)

    def do_piece_has_valid_move(self, piece):
        are_valid_moves = []
        for move_type in POSSIBLE_MOVES:
            new_piece = copy.deepcopy(piece)
            new_piece.move(move_type)
            is_valid_move = self.can_add_piece(new_piece)
            are_valid_moves.append(is_valid_move)
        return any(are_valid_moves)

    def render(self):
        display_contents = ""
        for column in self.grid_squares:
            for row in column:
                display_contents += str(row) + " "

            display_contents += "\n"

        print(display_contents)


class GridCell:
    def __init__(self, x=None, y=None):
        self.occupied_by = NONE
        self.position = Position(x, y)

    def __repr__(self):
        if self.is_empty():
            return f" "
        else:
            return "*"

    def is_empty(self):
        return self.occupied_by == NONE

    def is_wall(self):
        return self.occupied_by == WALL

    def is_piece(self):
        return self.occupied_by == PIECE

    def fill(self, element_type):
        self.occupied_by = element_type

    def clear(self):
        self.occupied_by = NONE
