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


def manukyan(current_state, neighbors):
    """ Returns the next state of a cell based on a list of neighbor states.

        The manukyan function follows the probabilistic model observed in
        this paper: https://www.nature.com/articles/nature22031#f4

        inputs:
            current state (int): either 1 (representing green) or 0 (representing black)
            neighbors (list): a list of states for neighbors, with the same pattern
    """

    num_green = neighbors.count(GREEN_STATE)
    num_black = neighbors.count(BLACK_STATE)

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

    if current_state is GREEN_STATE:
        p_change = p_green_to_black[num_green]
        new_state = BLACK_STATE if random.random() < p_change else GREEN_STATE

    elif current_state is BLACK_STATE:
        p_change = p_black_to_green[num_black]
        new_state = GREEN_STATE if random.random() < p_change else BLACK_STATE

    else:
        raise ValueError("Current state is invalid for Manukyan model.")

    return new_state


def pygame_quit_event(events):
    """ Returns True if a quit event has been raised by Pygame. """

    for event in events:
        if event.type == pygame.QUIT:
            return True
