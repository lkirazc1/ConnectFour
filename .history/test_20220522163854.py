import pygame
import unittest
from grid import Grid




class TestGridMethods(unittest.TestCase):

    def test(self):
        grid = Grid(6, 7)
        # check if get_color is correct
        self.assertEqual(grid.get_color(0, 0), 0)
        # check place piece returns and places correctly
        self.assertEqual(grid.place_piece(1, 1), (5, 1))
        self.assertEqual(grid.get_color(5, 1), 1)
        self.assertFalse(grid.check_done(5, 1, 1))
        for i in range(5):
            self.assertEqual(grid.place_piece(1, 1), (4 - i, 1))
            last_one = (4 - i, 1)
        self.assertEqual(grid.place_piece(1, 1), None)
        self.assertEqual(grid.check_done(last_one[0], last_one[1], 1), True)


if __name__ == '__main__':
    unittest.main()

