import time

from helpers import *
from view import View
from hexMap import HexMap


def draw_tiles_demo():
    """ Draws a 25x20 hex array, then waits for two seconds. """

    assert_python_version(3, 7)
    view = View()
    view.create_window()
    hex_map = HexMap(width=25, height=20)
    view.draw_hex_map(hex_map)
    start = time.time()
    while time.time() < start + 2:
        pass


if __name__=="__main__":
    draw_tiles_demo()
