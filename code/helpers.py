# Standard libraries
import sys
import random

# Outside libraries
import pygame

# Project modules
from constants import *


def assert_python_version(major, minor=0):
    """ Checks whether the current version of Python is
        greater or equal to the specified version. Otherwise,
        prints an error messages and closes the program.

        inputs:
            major (int): Most significant version number (3.6 -> 3)
            minor (int): Secondary version number (3.6 -> 6)
    """

    actual_major = sys.version_info.major
    actual_minor = sys.version_info.minor

    if actual_major > major or (actual_major == major and actual_minor >= minor):
        return

    print("This program requires Python version %s.%s. You are using Python %s.%s." %
          (major, minor, actual_major, actual_minor))
    sys.exit()


# When considering color changing, white oscilli -> BLACK on average
# Otherwise, on average it goes to green

def manukyan(current_state, neighbors, curr_turn=0):
    """ Returns the next state of a cell based on a list of neighbor states.

        The manukyan function follows the probabilistic model observed in
        this paper: https://www.nature.com/articles/nature22031#f4

        inputs:
            current state (int): either 1 (representing green) or 0 (representing black)
            neighbors (list): a list of states for neighbors, with the same pattern
    """
    num_green = neighbors.count(GREEN_STATE)
    num_black = neighbors.count(BLACK_STATE)
    num_white = neighbors.count(WHITE_STATE)
    num_brown = neighbors.count(BROWN_STATE)

    # Probability mappings sampled from figure 4D of manukyan paper and
    # converted to values with Logger Pro
    p_green_to_black = {0: 0,
                        1: 0.011,
                        2: 0.013,
                        3: 0.029,
                        4: 0.082,
                        5: 0.166,
                        6: 0.274,
                        7: 0.438}
    p_black_to_green = {0: 0,
                        1: 0.002,
                        2: 0.002,
                        3: 0.005,
                        4: 0.041,
                        5: 0.132,
                        6: 0.355,
                        7: 0.476}

    p_white_to_brown = {0: 0,
                        1: 0.011,
                        2: 0.013,
                        3: 0.029,
                        4: 0.082,
                        5: 0.166,
                        6: 0.274,
                        7: 0.438}


    #TODO: Discuss what values may be better
    p_brown_to_white = {0: 0,
                        1: 0.002,
                        2: 0.002,
                        3: 0.005,
                        4: 0.041,
                        5: 0.132,
                        6: 0.355,
                        7: 0.476}

    # Pretty arbitrarily decided tbh.
    p_color_change = {
                    0 : 0.004,
                    1 : 0.008,
                    2 : 0.016,
                    3 : 0.032,
                    4 : 0.064,
                    5 : 0.128,
                    6 : 0.256,
                    7 : 0.512,
                    }


    time_step = 0.1  # Decrease for more gradual changes; decreases all probabilities by a ratio

    p_convert_color = 0 # white -> black; brown -> green [on average, not always]
    p_color_choice = 0

    p_white_to_green = 0.4
    p_brown_to_green = 0.6

    turn_color_shifting_starts = 200

    if current_state in [WHITE_STATE, BROWN_STATE]:
        if curr_turn > turn_color_shifting_starts:
            p_convert_color = random.random() < p_color_change[num_green + num_black] * curr_turn / 200

    if current_state is GREEN_STATE:
        p_change = poisson(p_green_to_black[num_green], time_step)
        new_state = BLACK_STATE if random.random() < p_change else GREEN_STATE

    elif current_state is BLACK_STATE:
        p_change = poisson(p_black_to_green[num_black], time_step)
        new_state = GREEN_STATE if random.random() < p_change else BLACK_STATE

    elif current_state is WHITE_STATE:
        if p_convert_color:
            if random.random() < p_white_to_green:
                new_state = GREEN_STATE
            else:
                new_state = BLACK_STATE
        else:
            p_change = poisson(p_white_to_brown[7 - num_white], time_step)
            new_state = BROWN_STATE if random.random() < p_change else WHITE_STATE

    elif current_state is BROWN_STATE:
        if p_convert_color:
            if random.random() < p_brown_to_green:
                new_state = GREEN_STATE
            else:
                new_state = BLACK_STATE
        else:
            p_change = poisson(p_brown_to_white[7 - num_brown], time_step)
            new_state = WHITE_STATE if random.random() < p_change else BROWN_STATE
    else:
        raise ValueError("Current state is invalid for Manukyan model.")

    return new_state

def deterministic(current_state, neighbors, curr_turn=0):
    """ Returns the next state of a cell based on a list of neighbor states.

        if current_state is GREEN_STATE, turns black when 4 or more neighbors are black
        if current_state is BLACK_STATE, turns green when 3 or more neighbors are green

        inputs:
            current state (int): either 1 (representing green) or 0 (representing black)
            neighbors (list): a list of states for neighbors, with the same pattern
    """

    p_color_change = {
                    0 : 0.001,
                    1 : 0.002,
                    2 : 0.004,
                    3 : 0.008,
                    4 : 0.016,
                    5 : 0.032,
                    6 : 0.064,
                    7 : 0.128,
                    }


    time_step = 0.1  # Decrease for more gradual changes; decreases all probabilities by a ratio

    p_convert_color = 0 # white -> black; brown -> green [on average, not always]
    p_color_choice = 0

    p_white_to_green = 0.4
    p_brown_to_green = 0.6

    turn_color_shifting_starts = 200
    num_green = neighbors.count(GREEN_STATE)
    num_black = neighbors.count(BLACK_STATE)
    num_white = neighbors.count(WHITE_STATE)
    num_brown = neighbors.count(BROWN_STATE)

    if current_state in [WHITE_STATE, BROWN_STATE]:
        if curr_turn > turn_color_shifting_starts:
            p_convert_color = random.random() < p_color_change[num_green + num_black]

    if p_convert_color:
        if current_state is WHITE_STATE:
            new_state = GREEN_STATE
        else:
            new_state = BLACK_STATE

    if current_state is GREEN_STATE:
        if num_black > 3:
            new_state = BLACK_STATE
        else:
            new_state = current_state

    elif current_state is BLACK_STATE:
        if num_green > 2:
            new_state = GREEN_STATE
        else:
            new_state = current_state
    elif current_state is WHITE_STATE:
        if num_brown > 3:
            new_state = BROWN_STATE
        else:
            new_state = current_state
    elif current_state is BROWN_STATE:
        if num_white > 2:
            new_state = WHITE_STATE
        else:
            new_state = current_state
    else:
        raise ValueError("Current state is invalid for deterministic model.")

    return new_state


def poisson(probability, step):
    """ Returns the probability of an event occurring over a fractional time step. """
    return 1 - ((1 - probability) ** step)


def pygame_quit_event(events):
    """ Returns True if a quit event has been raised by Pygame. """

    for event in events:
        if event.type == pygame.QUIT:
            return True
