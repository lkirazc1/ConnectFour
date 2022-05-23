import pygame
import pickle
import neat
import pickle
import os
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
        return [self.grid.get_color(r, c) for r in range(self.rows) for c in range(self.cols)]


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
            print(output1)
            for i, val in sorted(list(enumerate(output1), key=))

            if self.grid.check_done(place1[0], place1[1], YELLOW):
                genome1.fitness += 1
                break
            elif 0 not in self.unpack_board():
                genome1.fitness += 1
                genome2.fitness += 1
                break

            output2 = net2.activate(self.unpack_board())
            print(output2)
            place2 = self.grid.place_piece(output2.index(max(output2)), RED)
            while place2 is None:
                genome2.fitness -= 1
                output2.remove(max(output2))
                place2 = self.grid.place_piece(output2.index(max(output2)), RED)
            
            if self.grid.check_done(place2[0], place2[1], RED):
                genome2.fitness += 1
                break
            elif 0 not in self.unpack_board():
                genome1.fitness += 1
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
    #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-6')
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, 10000)
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




        


