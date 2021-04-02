import random
import copy

# GRID RELATED
NONE = 0
WALL = 1
PIECE = 2

# PIECE RELATED
I_SHAPE = [
    [1, 0], 
    [1, 0], 
    [1, 0], 
    [1, 0]
    ]
L_SHAPE = [
            [1, 0],
            [1, 0],
            [1, 1],
        ]
L_SHAPE_INVERTED = [
        [0, 1],
        [0, 1],
        [1, 1],
    ]
THUNDER_SHAPE = [
    [0, 1],
    [1, 1],
    [1, 0],
]
SQUARE_SHAPE = [
    [1, 1],
    [1, 1],
]
ALL_SHAPES = [L_SHAPE, L_SHAPE_INVERTED, THUNDER_SHAPE, SQUARE_SHAPE]

# MovementTypes
MOVEMENT_DOWN = 0 
MOVEMENT_LEFT = 1
MOVEMENT_RIGHT = 2

POSSIBLE_MOVES = [MOVEMENT_DOWN, MOVEMENT_LEFT, MOVEMENT_RIGHT]


class Grid:
    def __init__(self, size):
        grid_squares = []
        for column_index in range(0, size):
            column = []
            for row_index in range(0, size):
                column.append(GridSquare(x=row_index, y=column_index))
            grid_squares.append(column)
        self.size = size
        self.grid_squares = grid_squares

    def populate_with_walls(self):
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

    # TU TRZEBA POPRAWIĆ KOLEJNOŚĆ X I Y
    # Moze wyniesc piece matrix jako obiekt tej klasy? Czy to nie bedzie złamanie zasad oop
    def add_piece(self, piece):
        piece_position_matrix = piece.get_piece_positions_matrix()
        for position in piece_position_matrix:
            self.grid_squares[position.y][position.x].fill(PIECE)

    def remove_piece(self, piece):
        piece_position_matrix = piece.get_piece_positions_matrix()
        for position in piece_position_matrix:
            self.grid_squares[position.y][position.x].clear()
    
    def can_add_piece(self, piece):
        # to nie dziala
        piece_position_matrix = piece.get_piece_positions_matrix()
        is_position_available = []
        for position in piece_position_matrix:
            grid_cell = self.grid_squares[position.y][position.x]
            is_position_available.append(grid_cell.is_empty() and self._is_position_within_bounds(position))
        return all(is_position_available)

    def _is_position_within_bounds(self, position):
        # Starts with 1 and substracted with 2(instead 1) because of walls
        x_bounds = (1, self.size - 2)
        y_bounds = (1, self.size - 2)
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


class GridSquare:
    def __init__(self, x=None ,y=None):
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

    def fill(self, element):
        self.occupied_by = element
    
    def clear(self):
        self.occupied_by = NONE


class PieceFactory:
    def __init__(self, shapes=ALL_SHAPES):
        self.shapes = shapes

    def get_piece(self, x, y):
        return Piece(x, y, self._get_random_shape())

    def _get_random_shape(self):
        return random.choice(self.shapes)

class Piece:
    def __init__(self, x, y, figure):
        self.position = Position(x, y)
        self.figure = figure

    def __repr__(self):
        return f"x: {self.position.x}, y: {self.position.y}, figure: {self.figure}"

    def move(self, movement):
        new_position = self.position
        if movement == MOVEMENT_DOWN:
            new_position.shift(0, 1)
        if movement == MOVEMENT_LEFT:
            new_position.shift(-1, 0)
        if movement == MOVEMENT_RIGHT:
            new_position.shift(1, 0)
        return Piece(new_position.x, new_position.y, self.figure)

    def get_piece_positions_matrix(self):
        matrix = []
        pos_x = self.position.x
        pos_y = self.position.y
        for f in self.figure:
            for cell in f:
                if cell:
                    matrix.append(Position(pos_x, pos_y))
                pos_x += 1
            pos_x = self.position.x
            pos_y += 1
        return matrix


class Game:
    def __init__(self, grid_size=20):
        self.grid_size = grid_size

    def play(self):
        grid = Grid(size=self.grid_size)
        grid.populate_with_walls()
        piece_factory = PieceFactory()
        game_over = False
        piece = piece_factory.get_piece(2, 2)

        current_piece = self.add_piece_to_grid(grid, piece)
        self.render_grid(grid)

        while not game_over:
            grid.remove_piece(current_piece)
            if grid.do_piece_has_valid_move(current_piece):
                player_move = self.get_player_move()
                current_piece.move(player_move)
                self.add_piece_to_grid(grid, current_piece)
                self.render_grid(grid)

        
    def add_piece_to_grid(self, grid, piece):
        grid.add_piece(piece)
        return piece

    def render_grid(self, grid):
        display_contents = ""
        for column in grid.grid_squares:
            for row in column:
                display_contents += str(row)

            display_contents += "\n"

        print(display_contents)

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
            move = ""

        return move

    @staticmethod
    def get_player_input():
        allowed_input = ["a", "A", "s", "S", "d", "D", "w", "W", "", " "]
        raw_input = None
        while raw_input not in allowed_input:
            raw_input = input(f"Choose input from {allowed_input}. Your choice is: ")
        
        return raw_input


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def shift(self, x, y):
        self.x += x 
        self.y += y
    
    def __repr__(self):
        return f"Postition ({self.x}, {self.y})"

game = Game()
game.play()

