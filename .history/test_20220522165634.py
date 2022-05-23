import pygame
import unittest
from grid import Grid




class TestGridMethods(unittest.TestCase):
    grid = Grid(6, 7)


    def test(self):
        # check if get_color is correct
        self.assertEqual(self.grid.get_color(0, 0), 0)
        # check place piece returns and places correctly
        self.assertEqual(self.grid.place_piece(1, 1), (5, 1))
        self.assertEqual(self.grid.get_color(5, 1), 1)
        # check check_done doesn't say it's finished when it's not
        self.assertFalse(self.grid.check_done(5, 1, 1))
        # fill up row and check that place_piece rejects it if it can't go into the row
        for i in range(5):
            self.assertEqual(self.grid.place_piece(1, 1), (4 - i, 1))
            last_one = (4 - i, 1)
        self.assertEqual(self.grid.place_piece(1, 1), None)
        # check that check done checks vertical correctly
        self.assertEqual(self.grid.check_done(last_one[0], last_one[1], 1), True)
    
    def test_horizontally(self):
        self.grid.clear()
        for i in range(4):
            self.assertEqual(self.grid.place_piece(i, 1), (5, i))
            last_place = (5, i)
            if i != 3:
                self.assertFalse(self.grid.check_done(last_place[0], last_place[1], 1))
        
        self.assertTrue(self.grid.check_done(last_place[0], last_place[1], 1))
        self.assertTrue(self.grid.check_done(5, 0, 1))

    def test_diagonally_right(self):
        self.grid.clear()
        for i in range(4):
            for j in range(i + 1):
                self.assertEqual(self.grid.place_piece())


if __name__ == '__main__':
    unittest.main()

