import pygame
from grid import Grid




class TestGridMethods(unittest.TestCase):

    def test_get_color(self):
        grid = Grid(6, 7)
        self.assertEqual(grid.get_color(0, 0), 0)
        self.assertEqual(grid.place_piece(1, 1), (0, 1))
        self.assertEqual(grid.get_color())
