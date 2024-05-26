import dill
import neat
import os

from CelestePythonInterface import SocketInterface, SessionParameters, SocketServer
from utils import inputs_preprocessor, score_function

def display_genome(file, session_parameters, neat_config, socket):
    with open(file, "rb") as f:
        genome = dill.load(f)
        net = neat.nn.FeedForwardNetwork.create(genome, neat_config)
        interface = SocketInterface(socket,net.activate, session_parameters, inputs_preprocessor)            

        return score_function(interface.run(),session_parameters)


def display_neat_generations(folder, session_parameters, neat_config, socket):
    GEN = 0
    while True:
        if os.path.exists(f"{folder}/winner-{GEN}.bin"):
            print(display_genome(f"{folder}/winner-{GEN}.bin", session_parameters, neat_config, socket))
            GEN += 1
        else:
            break

if __name__ == '__main__':
    session_parameters = SessionParameters()
    session_parameters.Level = "1"
    session_parameters.AreaKey = 1
    session_parameters.AreaMode = 0
    session_parameters.TimeoutSeconds = 5
    session_parameters.ObjectiveXCoordinate = 282
    session_parameters.ObjectiveYCoordinate = -24
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        'celeste_neat_config')
    socket_server = SocketServer()
    client_socket, addr = socket_server.await_connection()
    while True:
        print(display_neat_generations('runs-6', session_parameters, config, client_socket))
    