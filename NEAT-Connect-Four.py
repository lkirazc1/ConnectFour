import pygame
import pickle
import neat
import pickle
import os
from grid import Grid
import time
from neat import parallel

pygame.init()
YELLOW = -1
RED = 1
DEPTH = 8


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

    def test_ai(self, win, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        done = False
        presses = 3
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and presses > 0:
                        presses -= 1
                    elif event.key == pygame.K_RIGHT and presses < 6:
                        presses += 1
                    elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        place = self.grid.place_piece(presses, -1)
                        if place is None:
                            break
                        presses = 3
                        is_done = self.grid.check_done(place[0], place[1], -1)
                        if is_done:
                            print("player wins")
                            quit()
                        output = net.activate(self.unpack_board())
                        for i, val in sorted(list(enumerate(output)), key=lambda x: x[1], reverse=True):
                            place = self.grid.place_piece(i, RED)
                            if place is not None:
                                break
                        if self.grid.check_done(place[0], place[1], RED):
                            print("computer wins")
                            quit()

            self.grid.update(win, presses, (255, 255, 0))



    def train_ai(self, genome, config, first=False):
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        done = False
        first_round = True
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            if not first_round or first:
                output1 = net.activate(self.unpack_board())
                for i, val in sorted(list(enumerate(output1)), key=lambda x: x[1], reverse=True):
                    place1 = self.grid.place_piece(i, YELLOW)
                    if place1 is not None:
                        break
                    else:
                        genome.fitness -= 1

                if self.grid.check_done(place1[0], place1[1], YELLOW):
                    genome.fitness += 25
                    break
                elif 0 not in self.unpack_board():
                    genome.fitness += 15
                    break
            else:
                first_round = False


            if first:
                col = self.grid.computer_choice(RED, place1[0], place1[1], DEPTH)
                last_row, last_row = self.grid.place_piece(col, RED)
            else:
                try:
                    col = self.grid.computer_choice(YELLOW, place1[0], place1[1], DEPTH)
                except NameError:
                    col = self.grid.computer_choice(YELLOW, 0, 0, time.time())
                last_row, last_col = self.grid.place_piece(col, YELLOW)

            minimax_wins = self.grid.check_done(last_row, last_col, self.grid.get_color(last_row, last_col))
            if minimax_wins:
                for color in self.unpack_board():
                    if color != 0:
                        genome.fitness += 1
            
            #self.grid.draw(self.win)


def eval_genomes(genome, config):
    #WIDTH, HEIGHT = 678, 674
    #win = pygame.display.set_mode((WIDTH, HEIGHT))

    # with thread poll executor

    #with ThreadPoolExecutor(max_workers=8) as executor:
    #    for i, (genome_id1, genome1) in enumerate(genomes):
    #        if i == len(genomes) - 1:
    #            break
    #        genome1.fitness = 0
    #        for genome_id2, genome2 in genomes[i + 1:]:
    #            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
    #            game = Game()
    #            executor.submit(Game.train_ai, game, genome1, genome2, config)
                #game.train_ai(genome1, genome2, config)

    #genome = genome_config_tuple[0]
    #config = genome_config_tuple[1]
    genome.fitness = 0 if genome.fitness == None else genome.fitness
    for _ in range(5):
        game = Game()
        genome.fitness += game.train_ai(genome, config, first=True)
    for _ in range(5):
        game = Game()
        genome.fitness += game.train_ai(genome, config, first=False)

    return float(genome.fitness)



def run_neat(config):
    pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.Checkpointer(1))
    pe = neat.ParallelEvaluator(8, eval_genomes)
    winner = pop.run(pe.evaluate, 100)
    with open('winner.pickle', 'wb') as f:
        pickle.dump(winner, f)
    


def test_ai(config):
    width, height = 678, 674
    window = pygame.display.set_mode((width, height))
    game = Game()
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    
    game.test_ai(window, winner, config)




if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "neat-config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, 
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, 
                         config_path)

    run_neat(config)

