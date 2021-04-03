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


class Shape:
    def __init__(self, shape_matrix):
        self.matrix = shape_matrix

    def rotate_clockwise(self):
        self.matrix = [list(reversed(col)) for col in zip(*self.matrix)]
        return self.matrix

    def rotate_counter_clockwise(self):
        n = len(self.matrix)
        for x in range(0, int(n / 2)):
            for y in range(x, n - x - 1):
                temp = self.matrix[x][y]
                self.matrix[x][y] = self.matrix[y][n - 1 - x]
                self.matrix[y][n - 1 - x] = self.matrix[n - 1 - x][n - 1 - y]
                self.matrix[n - 1 - x][n - 1 - y] = self.matrix[n - 1 - y][x]
                self.matrix[n - 1 - y][x] = temp
        return self.matrix


i_shape = Shape(I_SHAPE)
l_shape = Shape(L_SHAPE)
l_shape_inverted = Shape(L_SHAPE_INVERTED)
thunder_shape = Shape(THUNDER_SHAPE)
square_shape = Shape(SQUARE_SHAPE)
ALL_SHAPES = [i_shape, l_shape, l_shape_inverted, thunder_shape, square_shape]
