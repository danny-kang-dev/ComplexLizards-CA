# Standard libraries
import math

# Outside libraries
import pygame

# Project modules
from constants import *
from helpers import *


class View(object):
    """ Represents a window used to visualize hexagonal cellular automata. """

    def __init__(self):
        """ Instantiates the View object. """
        self.screen = None

    def create_window(self):
        """ Creates a pygame window for the View object. """
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Snake Simulator 3000")

    def get_map_size(self, hex_map):
        """ Given a hexMap object, returns a tuple representing the maximum width
            and height of the array when rendered, in pixels.
        """

        x_size = len(hex_map.array[0])
        y_size = len(hex_map.array)
        width = x_size * HEX_SPACING_X + (y_size * HEX_SPACING_Y)//2 + HEX_SPACING_X * 2
        height = y_size * HEX_SPACING_Y + HEX_SPACING_Y * 2
        return width, height

    def draw_hex_map(self, hex_map, flip=True):
        """ Draws a HexMap object onto the screen. If flip is True, additionally
            commits the changes to the actual display window.
        """

        # Offset the map based on how large the map is
        max_width, max_height = self.get_map_size(hex_map)
        x_origin = (WINDOW_WIDTH - max_width)//2 + HEX_SPACING_X
        y_origin = (WINDOW_HEIGHT - max_height)//2 + HEX_SPACING_Y

        #   Draw each cell
        for cell, position in hex_map.tiles(index=True):
            self.draw_hex_cell(cell, position, offset=(y_origin, x_origin))

        #   Flip to next frame if flip attribute is True
        if flip:
            pygame.display.flip()

    def draw_hex_cell(self, cell, position, offset=(0, 0)):
        """ Draws a single hexagon cell on the screen.

            input:
                cell (HexCell): cell to draw
                position (tuple): position in hex array (y, x)
        """

        y, x = position  # Position in hex array
        ypx = y * HEX_SPACING_Y + offset[0]  # Position in pixels
        xpx = x * HEX_SPACING_X + (y * HEX_SPACING_X)//2 + offset[1]

        #   Enumerate vertices of a hexagon to pass to pygame.draw.polygon
        center_to_edge = (HEX_LENGTH * math.sqrt(3))//2
        half_edge = HEX_LENGTH//2
        points = [(xpx - center_to_edge, ypx - half_edge),
                  (xpx, ypx - HEX_LENGTH),
                  (xpx + center_to_edge, ypx - half_edge),
                  (xpx + center_to_edge, ypx + half_edge),
                  (xpx, ypx + HEX_LENGTH),
                  (xpx - center_to_edge, ypx + half_edge)]

        #   Draw the shape on the screen
        pygame.draw.polygon(self.screen, cell.color(), points)
