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

pygame.init()
row_count = 6
column_count = 7

COMPUTER_COLUMN_ORDER = [3, 4, 2, 5, 1, 6, 0]

YELLOW = -1
RED = 1

DEPTH = 8

# --- make board ---#

def board() -> np.ndarray:
    board = np.zeros((row_count, column_count), dtype=int)
    return board

# --- place piece---#

def place_piece(board: np.ndarray, column: int, piece: int) -> None or tuple:
    for r in range(row_count - 1, -1, -1):
        if board[r, column] == 0:
            board[r, column] = piece
            return (r, column)
    return None


# --- check finished ---#

def check_done(board: np.ndarray, row: int, column: int, color: int) -> int:


    # check vertically
    in_a_row = 1
    for r in range(row + 1, row_count):
        if board[r][column] == color:
            in_a_row += 1
        else:
            break
    if in_a_row >= 4:
        return 10*color

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
        return 10*color

    # check diagonally right
    in_a_row = 1
    r = row - 1
    c = column + 1
    while r >= 0 and c < column_count:
        if board[r][c] == color:
            in_a_row += 1
        else:
            break
        r -= 1
        c += 1
    r = row + 1
    c = column - 1
    while r < row_count and c >= 0:
        if board[r][c] == color:
            in_a_row += 1
        else:
            break
        r += 1
        c -= 1
    if in_a_row >= 4:
        return 10*color

    # check diagonally left
    in_a_row = 1
    r = row - 1
    c = column - 1
    while r >= 0 and c >= 0:
        if board[r][c] == color:
            in_a_row += 1
        else:
            break
        r -= 1
        c -= 1
    r = row + 1
    c = column + 1
    while r < row_count and c < column_count:
        if board[r][c] == color:
            in_a_row += 1
        else:
            break
        r += 1
        c += 1
    if in_a_row >= 4:
        return 10*color

    return 0


def next_move(board: np.ndarray, color: int, last_col: int, last_row: int, depth_left: int) -> tuple:
    depth_left -= 1
    current_score = check_done(board, last_row, last_col, -color)  # last color is reverse of current turn
    if current_score != 0:  # red or yellow wins
        return (current_score, None)
    elif 0 not in board:
        return (0, None)
    
    if color == RED:  # red = computer so maximize the score
        max_score = -123
        max_move = None
        for column in COMPUTER_COLUMN_ORDER:
            if board[0, column] != 0:
                continue
            if depth_left <= 0:
                return (0, column)
            row, place_col = place_piece(board, column, RED)
            (best_score, best_move) = next_move(board, YELLOW, column, row, depth_left)
            board[row, column] = 0
            if best_score > max_score:
                max_score = best_score
                max_move = column
                if best_score == 10:
                    break
        return (max_score, max_move)
    else:
        min_score = 11
        min_move = None
        for column in COMPUTER_COLUMN_ORDER:
            if board[0, column] != 0:
                continue
            if depth_left <= 0:
                return (0, column)
            row, place_col = place_piece(board, column, YELLOW)
            (worst_score, worst_move) = next_move(board, RED, column, row, depth_left)
            board[row, column] = 0
            if worst_score < min_score:
                min_score = worst_score
                min_move = column
                if worst_score == -10:
                    break
        return (min_score, min_move)









clock = pygame.time.Clock()
WIDTH, HEIGHT = 1378, 1365
display = pygame.display.set_mode((1378, 1365))
pressed = pygame.key.get_pressed()
done = False
pygame.display.set_caption("Connect Four")


# 41 dividers
# 75 radius for circles
def draw_board() -> None:
    display.fill((0, 0, 255))
    pygame.draw.rect(display, (255, 255, 255), pygame.Rect(0, 0, 1378, 180))
    y = 296
    for circle in range(1, row_count * column_count):
        if circle % 7 == 0:
            y += 191
        x = 116 + (circle % 7) * 191
        color = (255, 255, 255)
        if board[circle // column_count][circle % column_count] == 1:
            color = (255, 0, 0)
        if board[circle // column_count][circle % column_count] == -1:
            color = (255, 255, 0)
        pygame.draw.circle(display, color, (x, y), 75)
    color = (255, 255, 255)
    if board[0][0] == 1:
        color = (255, 0, 0)
    elif board[0][0] == -1:
        color = (255, 255, 0)
    pygame.draw.circle(display, color, (116, 296), 75)


def update(presses_sum: int, color: tuple) -> None:
    draw_board()
    pygame.draw.circle(display, color, (116 + presses_sum * 191, 90), 75)
    pygame.display.update()



def main():
    presses = 3
    board = board()
    color_number = -1
    update(presses, (255, 255, 0))
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
                    
                    color = (255,255,0)
                    if color_number == 1:
                        color = (255, 0, 0)

                    update(presses, color)
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    board_pos = place_piece(board, presses, color_number)
                    if board_pos is None:
                        pass
                    else:
                        row, column = board_pos
                        if not check_done(board, row, column, board[row][column]) and 0 in board:
                            presses = 3
                            draw_board()
                            font = pygame.font.SysFont("arial", 100)
                            text = font.render("Thinking ...", True, (0, 0, 0))
                            display.blit(text, (text.get_rect(center=(WIDTH // 2, 90))))
                            pygame.display.update()
                            computer_choice = next_move(board, RED, column, row, DEPTH) #fonts is map of size, color, 
                            print(computer_choice)
                            computer_column = computer_choice[1]
                            row, column = place_piece(board, computer_column, RED)
                            update(presses, (255, 255, 0))
                        if check_done(board, row, column, board[row][column]) or 0 not in board:
                            end_status = check_done(board, row, column, board[row][column])
                            font = pygame.font.SysFont("arial", 100)
                            color = (0, 0, 0)
                            who_wins = "Tie!"
                            if end_status and board[row][column] == 1:
                                who_wins = "Red Wins!"
                                color = (255, 0, 0)
                            if end_status and board[row][column] == -1:
                                who_wins = "Yellow Wins!"
                                color = (205, 205, 0)
                            update(presses, (255, 255, 255))
                            text = font.render(who_wins, True, color)
                            display.blit(text, (text.get_rect(center=(WIDTH // 2, 90))))
                            pygame.display.update()
                            while not done:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        pygame.quit()
                                        quit()
        update(presses, (255, 255, 0) if color_number == -1 else (255, 0, 0))
        pygame.display.update()
    pygame.quit()
    