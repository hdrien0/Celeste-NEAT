import neat

from visualize import *
from CelestePythonInterface import SocketInterface, SessionParameters, SocketServer
from utils import inputs_preprocessor, score_function
from FileReporter import *

class CelesteNeat:

    def __init__(self, session_parameters, neat_config_file, output_folder, restore_checkpoint = False, restore_file = None):
        self.client_socket = None
        self.restore_checkpoint = restore_checkpoint
        self.restore_file = restore_file
        self.session_parameters = session_parameters
        self.output_folder = output_folder
        self.neat_config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                            neat.DefaultSpeciesSet, neat.DefaultStagnation,
                            neat_config_file)
        
    def eval_genomes(self, genomes, config):
        for genome_id, genome in genomes:
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            inter = SocketInterface(self.client_socket, net.activate, self.session_parameters, inputs_preprocessor)
            genome.fitness = score_function(inter.run(), self.session_parameters)

    def run(self):

        # Create the population, which is the top-level object for a NEAT run.
        if not self.restore_checkpoint:
            p = neat.Population(self.neat_config)
        else:
            p = neat.Checkpointer.restore_checkpoint(self.restore_file)

        # p.add_reporter(FileReporter(self.output_folder+'/', True))
        # see the FileReporter class in FileReporter.py to see what it does
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        p.add_reporter(neat.Checkpointer(1,10000,self.output_folder + "/neat-checkpoint-"))

        socket_server = SocketServer()
        self.client_socket, addr = socket_server.await_connection()
        winner = p.run(self.eval_genomes, 500)

        # Display the winning genome.
        print('\nBest genome:\n{!s}'.format(winner))

        node_names = {-1: 'D_E', -2: 'D_NE', -3: 'D_N', -4: 'D_NW', -5: 'D_W', -6: 'D_SW', -7: 'D_S', -8: 'D_SE',-9:'T_E',-10:'T_NE',-11:'T_N',-12:'T_NW',-13:'T_W',-14:'T_SW',-15:'T_S',-16:'T_SE',-17:'X_VELOCITY',-18:'Y_VELOCITY',-19:'CAN_DASH',-20:'ON_GROUND',-21:'STAMINA',-22:'ANGLE_TO_OBJ',-23:'DIST_TO_OBJ', 0: 'RIGHT', 1: 'LEFT', 2: 'UP', 3: 'DOWN', 4: 'JUMP', 5: 'DASH',6:'GRAB'}
        draw_net(self.neat_config, winner, True, node_names=node_names)
        draw_net(self.neat_config, winner, True, node_names=node_names, prune_unused=True)
        plot_stats(stats, ylog=False, view=True)
        plot_species(stats, view=True)


if __name__ == '__main__':
    session_parameters = SessionParameters()
    session_parameters.Level = "1"
    session_parameters.AreaKey = 1
    session_parameters.AreaMode = 0
    session_parameters.TimeoutSeconds = 5
    session_parameters.ObjectiveXCoordinate = 282
    session_parameters.ObjectiveYCoordinate = -24
    celeste_neat = CelesteNeat(session_parameters, 'celeste_neat_config', 'run-0')
    celeste_neat.run()