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
    
    def _unpack_board(self):
        return (self.board[r][c] for r in range(self.rows) for c in range(self.cols))


    def train_ai(self, genome1, genome2, config):
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)
        
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            
            output1 = net1.activate(self._unpack_board())
            decision1 = output1.index(max(output1))
            place1 = self.grid.place_piece(decision1, YELLOW)
            if place1 is None:
                genome2.fitness -= 1
                genome1.fitness += 1
                break
            if self.grid.check_done(place1[0], place1[1], YELLOW):
                genome1.fitness += 1
                break


            output2 = net2.activate(self._unpack_board())
            decision2 = output2.index(max(output2))
            place2 = self.grid.place_piece(decision2, RED)
            if place1 is None:
                genome2.fitness -= 1
                genome1.fitness += 1
                break
            if self.grid.check_done(place2[0], place2[1], RED):
                genome2.fitness += 1
                break

            self.grid.draw(self.win)
    


def eval_genomes(genomes, config):
    WIDTH, HEIGHT = 678, 674
    win = pygame.display.set_mode((WIDTH, HEIGHT))

    for i, (genome_id1, genome1) in enumerate(genomes):
        if i == len(genomes) - 1:
            break
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[i + 1:]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            game = Game(win, WIDTH, HEIGHT)
            game.train_ai(genome1, genome2, config)


def run_neat(config):
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.CheckPointer)




        


