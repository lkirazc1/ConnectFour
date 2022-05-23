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

pygame.init()
row_count = 6
column_count = 7


# --- make board ---#

def board():
    board = np.zeros((row_count, column_count))
    return board


# --- place piece---#

def place_piece(board, column, piece):
    for r in range(row_count - 1, -1, -1):
        if board[r][column] == 0:
            board[r][column] = piece
            return [r, column]
    return None


# --- check finished ---#

def check_done(board, row, column, color):
    # check vertically
    in_a_row = 0
    for r in range(row, row_count):
        if board[r][column] == color:
            in_a_row += 1
        else:
            break
    if in_a_row >= 4:
        return True

    # check horizontally
    in_a_row = 1
    for c in range(column + 1, column_count):
        if board[row][c] == color:
            in_a_row += 1
        else:
            break
    for c in range(column - 1, -1, -1):
        if board[row][c] == color:
            in_a_row += 1
        else:
            break
    if in_a_row >= 4:
        return True

    # check diagonally right
    in_a_row = 0
    for rc in range(1, 1231):
        if row - rc < 0:
            break
        if column + rc >= column_count:
            break
        r = row - rc
        c = column + rc
        if board[r][c] == color:
            in_a_row += 1
        else:
            break
    for rc in range(1231):
        if row + rc >= row_count:
            break
        if column - rc < 0:
            break
        r = row + rc
        c = column - rc
        if board[r][c] == color:
            in_a_row += 1
        else:
            break
    if in_a_row >= 4:
        return True

    # check diagonally left
    in_a_row = 1
    for rc in range(1, 1231):
        if row - rc < 0:
            break
        if column - rc < 0:
            break
        r = row - rc
        c = column - rc
        if board[r][c] == color:
            in_a_row += 1
        else:
            break
    for rc in range(1, 1231):
        if row + rc >= row_count:
            break
        if rc + column >= column_count:
            break
        r = row + rc
        c = column + rc
        if board[r][c] == color:
            in_a_row += 1
        else:
            break
    if in_a_row >= 4:
        return True
    return False


clock = pygame.time.Clock()
display = pygame.display.set_mode((678, 674))
pressed = pygame.key.get_pressed()
done = False
pygame.display.set_caption("Connect Four")


# 41 dividers
# 75 radius for circles
def draw_board():
    display.fill((0, 0, 255))
    pygame.draw.rect(display, (255, 255, 255), pygame.Rect(0, 0, 678, 90))
    y = 147
    for circle in range(0, row_count * column_count):
        if circle % 7 == 0 and circle != 0:
            y += 94
        x = 57 + (circle % 7) * 94
        color = (255, 255, 255)
        if board[circle // column_count][circle % column_count] == 1:
            color = (255, 0, 0)
        if board[circle // column_count][circle % column_count] == -1:
            color = (255, 255, 0)
        pygame.draw.circle(display, color, (x, y), 37)


def update(presses_sum, color):
    draw_board()
    pygame.draw.circle(display, color, (57 + presses_sum * 94, 45), 37)
    pygame.display.update()

presses = 3
board = board()
color_number = -1
update(presses, (255,255,0))
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                if presses > 0 and event.key == pygame.K_LEFT:
                    presses -= 1
                if presses < 6 and event.key == pygame.K_RIGHT:
                    presses += 1
                color = (255, 255, 0)
                if color_number == 1:
                    color = (255, 0, 0)
                update(presses, color)
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                cr = place_piece(board, presses, color_number)
                if cr is not None:
                    row, column = cr
                    if check_done(board, row, column, board[row][column]) or 0 not in board:
                        end_status = check_done(board, row, column, board[row][column])
                        font = pygame.font.SysFont("arial", 100)
                        color = (0, 0, 0)
                        who_wins = "Tie!"
                        if end_status and color_number == 1:
                            who_wins = "Red Wins!"
                            color = (255, 0, 0)
                        if end_status and color_number == -1:
                            who_wins = "Yellow Wins!"
                            color = (205, 205, 0)
                        update(3, color_number)
                        pygame.draw.circle(display, (255,255,255), (678//2, 45), 37)
                        text = font.render(who_wins, True, color)
                        display.blit(text, (text.get_rect(center=(678/2, 45))))
                        pygame.display.update()
                        while not done:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    quit()
                    presses = 3
                    color_number *= -1
                    color = (255, 255, 0)
                    if color_number == 1:
                        color = (255, 0, 0)

                    update(presses, color)
    update(presses, (255, 255, 0) if color_number == -1 else (255, 0, 0))

