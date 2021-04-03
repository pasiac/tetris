import copy
import random

from position import Position
from moves import *

I_SHAPE = [
    [0, 0, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 0]
]
L_SHAPE = [
    [1, 0, 0],
    [1, 0, 0],
    [1, 1, 0],
]
L_SHAPE_INVERTED = [
    [0, 1, 0],
    [0, 1, 0],
    [1, 1, 0],
]
THUNDER_SHAPE = [
    [0, 1, 0],
    [1, 1, 0],
    [1, 0, 0],
]
SQUARE_SHAPE = [
    [1, 1],
    [1, 1],
]
ALL_SHAPES = [I_SHAPE, L_SHAPE, L_SHAPE_INVERTED, THUNDER_SHAPE, SQUARE_SHAPE]


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
        new_position = copy.deepcopy(self.position)
        new_figure = copy.deepcopy(self.figure)
        if movement == MOVEMENT_NONE:
            new_position.shift(0, 1)
        if movement == MOVEMENT_LEFT:
            new_position.shift(-1, 0)
        if movement == MOVEMENT_RIGHT:
            new_position.shift(1, 0)
        if movement == MOVEMENT_DOWN:
            self.figure = self.rotate_clockwise()
        if movement == MOVEMENT_UP:
            self.figure = self.rotate_counter_clockwise()
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

    def rotate_clockwise(self):
        n = len(self.figure)
        new_figure = []
        for j in range(n):
            column = []
            for i in range(n - 1, -1, -1):
                column.append(self.figure[i][j])
            new_figure.append(column)
        return new_figure

    def rotate_counter_clockwise(self):
        new_figure = copy.deepcopy(self.figure)
        n = len(new_figure)
        for x in range(0, int(n / 2)):
            for y in range(x, n - x - 1):
                temp = new_figure[x][y]
                new_figure[x][y] = new_figure[y][n - 1 - x]
                new_figure[y][n - 1 - x] = new_figure[n - 1 - x][n - 1 - y]
                new_figure[n - 1 - x][n - 1 - y] = new_figure[n - 1 - y][x]
                new_figure[n - 1 - y][x] = temp
        return new_figure
