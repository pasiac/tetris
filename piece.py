import copy
import random

from moves import *
from position import Position
from shape import ALL_SHAPES


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
        new_piece = copy.deepcopy(self)
        if movement == MOVEMENT_NONE:
            new_piece.position.shift(0, 1)
        if movement == MOVEMENT_LEFT:
            new_piece.position.shift(-1, 0)
        if movement == MOVEMENT_RIGHT:
            new_piece.position.shift(1, 0)
        if movement == MOVEMENT_DOWN:
            new_piece.figure.rotate_clockwise()
        if movement == MOVEMENT_UP:
            new_piece.figure.rotate_counter_clockwise()
        return new_piece

    def get_piece_positions_matrix(self):
        matrix = []
        pos_x = self.position.x
        pos_y = self.position.y
        for f in self.figure.matrix:
            for cell in f:
                if cell:
                    matrix.append(Position(pos_x, pos_y))
                pos_x += 1
            pos_x = self.position.x
            pos_y += 1
        return matrix
