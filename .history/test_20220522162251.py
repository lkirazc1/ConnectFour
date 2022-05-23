import pygame
import unittest
from grid import Grid




class TestGridMethods(unittest.TestCase):

    def test(self):
        grid = Grid(6, 7)
        self.assertEqual(grid.get_color(0, 0), 0)
        self.assertEqual(grid.place_piece(1, 1), (5, 1))
        self.assertEqual(grid.get_color(0, 1), 1)

if __name__ == '__main__':
    unittest.main()

