import pygame
import pickle
import neat
import pickle
import os
from concurrent.futures.thread import ThreadPoolExecutor
from grid import Grid
pygame.init()
YELLOW = -1
RED = 1

class Game:
    def __init__(self):
        #self.width = width
        #self.height = height
        #self.win = win
        self.grid = Grid(6, 7)
        self.cols = self.grid.cols
        self.rows = self.grid.rows
        self.board = self.grid.board
    
    def unpack_board(self):
        return [self.grid.get_color(r, c) for r in range(self.rows) for c in range(self.cols)]

    def train_ai(self, win, width, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        done = False
        presses = 3
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT
            



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
            for i, val in sorted(list(enumerate(output1)), key=lambda x: x[1], reverse=True):
                place1 = self.grid.place_piece(i, YELLOW)
                if place1 is not None:
                    break
                else:
                    genome1.fitness -= 1

            if self.grid.check_done(place1[0], place1[1], YELLOW):
                genome1.fitness += 1
                break
            elif 0 not in self.unpack_board():
                genome1.fitness += 1
                genome2.fitness += 1
                break

            output2 = net2.activate(self.unpack_board())
            for i, val in sorted(list(enumerate(output2)), key=lambda x: x[1], reverse=True):
                place2 = self.grid.place_piece(i, RED)
                if place2 is not None:
                    break
                else:
                    genome2.fitness -= 1        
            if self.grid.check_done(place2[0], place2[1], RED):
                genome2.fitness += 1
                break
            elif 0 not in self.unpack_board():
                genome1.fitness += 1
                genome2.fitness += 1
                break

            #self.grid.draw(self.win)
    


def eval_genomes(genomes, config):
    #WIDTH, HEIGHT = 678, 674
    #win = pygame.display.set_mode((WIDTH, HEIGHT))

    with ThreadPoolExecutor(max_workers=8) as executor:
        for i, (genome_id1, genome1) in enumerate(genomes):
            if i == len(genomes) - 1:
                break
            genome1.fitness = 0
            for genome_id2, genome2 in genomes[i + 1:]:
                genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
                game = Game()
                executor.submit(Game.train_ai, game, genome1, genome2, config)
                #game.train_ai(genome1, genome2, config)

def run_neat(config):
    #p = neat.Population(config)
    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-122')
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, 1)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)
    

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "neat-config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, 
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, 
                         config_path)
    
    run_neat(config)
    #test_ai(config)




        


