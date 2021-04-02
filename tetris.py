import random

# GRID RELATED
NONE = 0,
WALL = 1,
PIECE = 2,

# PIECE RELATED
I_SHAPE = [1, 1, 1, 1]
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
ALL_SHAPES = [I_SHAPE, L_SHAPE, L_SHAPE_INVERTED, THUNDER_SHAPE, SQUARE_SHAPE]


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
        self.x_bounds = (0, size - 1)
        self.y_bounds = (0, size - 1)

    def populate_with_walls(self):
        for grid_row in self.grid_squares:
            for grid_cell in grid_row:
                if self._is_wall(grid_cell):
                    grid_cell.occupied_by = WALL
    
    def _is_wall(self, grid_cell):
        position = grid_cell.position
        return any([
            position.x == 0, 
            position.x == self.size - 1, 
            position.y == self.size - 1,
        ])

    def add_piece(self, piece):
        self.grid_squares[piece.x][piece.y].fill(WALL)
        # Do wizualizacji tyhlko
        for grid in self.grid_squares:
            print(grid)

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
        self.x = x
        self.y = y
        self.figure = figure

    def __repr__(self):
        return f"x: {self.x}, y: {self.y}, figure: {self.figure}"

    

class Game:
    def __init__(self, grid_size=20):
        self.grid_size = grid_size

    def play(self):
        grid = Grid(size=self.grid_size)
        grid.populate_with_walls()
        piece_factory = PieceFactory()
        game_over = False

        current_piece = self.add_piece_to_grid(grid, piece_factory)

    
    def add_piece_to_grid(self, grid, piece_facotry):
        piece = piece_facotry.get_piece(2, 2)
        grid.add_piece(piece)


    def get_player_move(self):
        player_input = get_player_input()
        move = None
        if player_input in ["a", "A"]:
            move = ""
        elif player_input in ["s", "S"]:
            move = ""
        elif player_input in ["s", "S"]:
            move = ""
        elif player_input in ["s", "S"]:
            move = ""

        return move

    @staticmethod
    def get_player_input():
        allowed_input = ["a", "A", "s", "S", "d", "D", "w", "W"]
        raw_input = None
        while raw_input not in allowed_input:
            raw_input = input(f"Choose input from {allowed_input}. Your choice is: ")
        
        return raw_input


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"Postition ({self.x}, {self.y})"

game = Game()
game.play()

