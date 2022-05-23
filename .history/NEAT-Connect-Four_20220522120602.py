import pygame
import pickle
import neat
import pickle
from grid import Grid
pygame.init()
YELLOW = -1
RED = 1

class Game:
    def __init__(self, win, width, height):
        self.width = width
        self.height = height
        self.win = win
        self.grid = Grid(6, 7)
        self.cols = self.grid.cols
        self.rows = self.grid.rows
        self.board = self.grid.board
    
    def unpack_board(self):
        return [self.board[r][c] for r in range(self.rows) for c in range(self.cols)]


    def train_ai(self, genome1, genome2, config):
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)
        
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            
            output1 = net1.activate(self.unpack_board())
            decision1 = output1.index(max(output1))
            place1 = self.grid.place_piece(decision1, YELLOW)
            if place1 is None:
                genome2.fitness -= 1
                genome1.fitness += 1
            if self.grid.check_done()

def test_ai(config):
    WIDTH, HEIGHT = 700, 500
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    game = Game(win, WIDTH, HEIGHT)
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    
    game.test_ai(winner, config)





        


