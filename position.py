class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def shift(self, x, y):
        self.x += x
        self.y += y

    def __repr__(self):
        return f"Position ({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
