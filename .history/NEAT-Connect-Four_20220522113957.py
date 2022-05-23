import pygame
import pickle
import neat
import pickle
from grid import Grid
pygame.init()


class Game:
    def __init__(self, win, width, height):
        self.

def test_ai(config):
    WIDTH, HEIGHT = 700, 500
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    game = Game(win, WIDTH, HEIGHT)
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    
    game.test_ai(winner, config)





        


