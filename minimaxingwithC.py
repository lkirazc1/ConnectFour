# numpy zeros makes a big list of the first value then the second value amount of list
# 6 columns and 5 rows starts at 0
# first index is the row and then the column
# 1 is top and 6 is bottom
# 7 is right and 1 is left
# red is 1 and yellow is -1
# rows then columns
import numpy as np
import random
import math
import pygame
import time
from grid import Grid
import cConnectFour
RED = 1
YELLOW = -1
COMPUTER_COLUMN_ORDER = [3, 4, 2, 5, 1, 6, 0]
COMPUTER_MILLISECONDS_LIMIT = 5000


def minimax(grid: Grid, color, last_col, last_row, start_time, depth):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    depth += 1
    current_score = grid.check_done(last_row, last_col, -color)
    if current_score != 0:
        return (current_score, None)
    elif 0 not in board:
        return (0, None)
    
    if color == RED:
        max_score = -123
        max_move = None
        for column in COMPUTER_COLUMN_ORDER:
            if grid.get_color(0, column) != 0:
                continue
            if round(time.time() * 1000) - start_time > COMPUTER_MILLISECONDS_LIMIT:
                return (0, column)
            row, _ = grid.place_piece(column, RED)
            (best_score, best_move) = minimax(grid, YELLOW, column, row, start_time, depth)
            





