import unittest

from grid import GridCell
from piece import PieceFactory


class GridCellTestCase(unittest.TestCase):
    def setUp(self):
        self.piece_factory = PieceFactory()

    def test_should_be_empty_on_creation(self):
        grid_square = GridCell()

        self.assertTrue(grid_square.is_empty())

    def test_should_be_filled_with_piece(self):
        grid_square = GridCell()

        grid_square.fill(self.piece_factory.get_piece(2, 2))

        self.assertFalse(grid_square.is_empty())

    def test_should_clear(self):
        grid_square = GridCell()
        grid_square.fill(self.piece_factory.get_piece(2, 2))

        grid_square.clear()

        self.assertTrue(grid_square.is_empty())
