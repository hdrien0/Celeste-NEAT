from CelestePythonInterface import SessionData
from math import pi

def inputs_preprocessor(player_state): #for normalisation purposes
    inputs = list(player_state)
    for i in range(8,16):
        inputs[i] = 0 if (inputs[i] == 0 or inputs[i] == 3) else 1

    inputs[SessionData.X_VELOCITY.value] /= 300
    inputs[SessionData.Y_VELOCITY.value] /= 300
    inputs[SessionData.STAMINA.value] /= 110
    inputs[SessionData.ANGLE_TO_OBJECTIVE.value] /= 2*pi
    inputs[SessionData.DISTANCE_TO_OBJECTIVE.value] /= inputs[SessionData.LEVEL_DIAGONAL_LENGTH.value]

    return inputs[:23]

def score_function(final_player_state, session_parameters):
    if final_player_state[SessionData.NUMBER_OF_LEVELS_FINISHED.value] >= 1:
        return (session_parameters.TimeoutSeconds - final_player_state[SessionData.SECONDS_ELAPSED.value]) * 1000
    return -final_player_state[SessionData.DISTANCE_TO_OBJECTIVE.value]
