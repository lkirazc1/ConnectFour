import pygame
import unittest
from grid import Grid




class TestGridMethods(unittest.TestCase):

    def test(self):
        grid = Grid(6, 7)
        self.assertEqual(grid.get_color(0, 0), 0)
        self.assertEqual(grid.place_piece(1, 1), (5, 1))
        self.assertEqual(grid.get_color(5, 1), 1)
        for i in range(5):
            self.assertEqual(grid.place_piece(1, 1), (4 - i, 1))
        self.assertEqual(grid.))

if __name__ == '__main__':
    unittest.main()

