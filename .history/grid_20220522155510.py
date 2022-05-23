import pygame
import cConnectFour

pygame.init()

class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.board = cConnectFour.Board()
        #self.board = [[0 for _ in range(cols)] for _ in range(rows)]

    def _get_color(self):
        ret = self.board.get_color(self.)

    def place_piece(self, col: int, piece: int) -> None or tuple:
        ret = self.board.place_piece(col, piece)
        if ret is None:
            return None
        else:
            return ret, col
        #for r in range(self.rows - 1, -1, -1):
        #    if self.board[r][col] == 0:
        #        self.board[r][col] = piece
        #        # return the position index where the piece was placed
        #        return r, col

        #return None


    def check_done(self, row, column, color):
        return self.board.check_done(row, column, color) != 0

        # # check vertically
        # in_a_row = 1
        # for r in range(row + 1, self.rows):
        #     if self.board[r][column] == color:
        #         in_a_row += 1
        #     else:
        #         break

        # if in_a_row >= 4:
        #     return True

        # # check horizontally

        # in_a_row = 1
        # for c in range(column + 1, self.cols):
        #     if self.board[row][c] == color:
        #         in_a_row += 1

        #     else:
        #         break

        # for c in range(column - 1, -1 , -1):
        #     if self.board[row][c] == color:
        #         in_a_row += 1
        #     else:
        #         break

        # if in_a_row >= 4:
        #     return True

        # # check diagonally right
        # in_a_row = 1
        # r = row - 1
        # c = column + 1
        # while r >= 0 and c < self.cols:
        #     if self.board[r][c] == color:
        #         in_a_row += 1
        #     else:
        #         break
        #     r -= 1
        #     c += 1

        # r = row + 1
        # c = column - 1
        # while r < self.rows and c >= 0:
        #     if self.board[r][c] == color:
        #         in_a_row += 1
        #     else:
        #         break
        #     r += 1
        #     c -= 1

        
        # if in_a_row >= 4:
        #     return True
        
        # # check diagonally left

        # in_a_row = 1
        # r = row - 1
        # c = column - 1
        # while r >= 0 and c >= 0:
        #     if self.board[r][c] == color:
        #         in_a_row += 1
        #     else:
        #         break
        #     r -= 1
        #     c -= 1


        # r = row + 1
        # c = column + 1
        # while r < self.rows and c < self.cols:
        #     if self.board[r][c] == color:
        #         in_a_row += 1
        #     else:
        #         break
        #     r += 1
        #     c += 1

        
        # if in_a_row >= 4:
        #     return True
        
        # return False        


    def draw(self, win):
        win.fill((0, 0, 255))
        pygame.draw.rect(win, (255, 255, 255), pygame.Rect(0, 0, 678, 90))
        y = 147
        for circle in range(self.rows * self.cols):
            if circle % 7 == 0 and circle != 0:
                y += 94
            x = 57 + (circle % 7) * 94
            color = (255, 255, 255)
            if self.board[circle // self.cols][circle % self.cols] == 1:
                color = (255, 0, 0)
            elif self.board[circle // self.cols][circle % self.cols] == -1:
                color = (255, 255, 0)
            pygame.draw.circle(win, color, (x, y), 37)
        pygame.display.update()
