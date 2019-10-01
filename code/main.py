# Standard libraries
import time
import sys

# Outside libraries
import pygame

# Project modules
import helpers
from view import View, DataVizElement, StateCounter
from hexMap import HexMap


def draw_tiles_demo():
    """ Draws a hex array, then runs a manukyan simulation
        on it for 1000 time steps.
    """

    helpers.assert_python_version(3, 6)

    #   Create View object
    view = View()
    view.create_window()

    #   Initialize Map
    hex_map = HexMap(width=35, height=25)
    hex_map.set_update_function(helpers.manukyan)
    view.draw_hex_map(hex_map, flip=False)

    #   Initialize visualization elements
    cell_counter = StateCounter(hex_map)
    view.add_UI_element(cell_counter)

    for i in range(1000):
        time.sleep(0.1)
        hex_map.step()
        view.update()
        view.draw_hex_map(hex_map)

        events = pygame.event.get()
        if helpers.pygame_quit_event(events):
            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    draw_tiles_demo()
