import pygame
import pickle
import neat
import pickle
from grid import Grid
pygame.init()


class Game:
    def __init__(self, win, width, height):
        self.width = width
        self.height = height
        self.win = win
        self.grid = Grid(6, 7)
        self.board = self.grid.board
    
    def test_ai(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    


def test_ai(config):
    WIDTH, HEIGHT = 700, 500
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    game = Game(win, WIDTH, HEIGHT)
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    
    game.test_ai(winner, config)





        


