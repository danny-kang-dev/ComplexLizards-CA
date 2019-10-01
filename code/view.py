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
        self.UI_elements = []

    def create_window(self):
        """ Creates a pygame window for the View object. """
        pygame.init()
        pygame.font.init()
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

        #   Draw UI elements
        for item in self.UI_elements:
            item.draw(self.screen)

        #   Flip to next frame if flip attribute is True
        if flip:
            pygame.display.flip()

    def add_UI_element(self, element):
        """ Adds a UI element to the View. """
        self.UI_elements.append(element)

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

    def update(self):
        """ Updates all UI elements in the view. """

        for element in self.UI_elements:
            element.update()


class DataVizElement(object):
    """ Visualizes data relating to a hexMap. """

    def __init__(self, hex_map):
        """ Initializes the element.

            inputs:
                hex_map (hexMap): the hex map object to visualize
        """

        self.map = hex_map
        self.position = (0, 0)

        self.surface = pygame.Surface(UI_ELEMENT_SIZE)
        self.border_color = GRAY
        self.background_color = DARK_GRAY

        self.large_font = pygame.font.SysFont("arial_narrow", 30)
        self.small_font = pygame.font.SysFont("arial_narrow", 16)

        self.clear()

    def clear(self):
        """ Clears the element surface and redraws border. """
        if UI_ELEMENT_WIDTH < 3 or UI_ELEMENT_HEIGHT < 3:
            raise ValueError("UI elements cannot be smaller than 3px by 3px.")

        self.surface.fill(self.border_color)
        rectangle = (1, 1, UI_ELEMENT_WIDTH - 2, UI_ELEMENT_HEIGHT - 2)
        pygame.draw.rect(self.surface, self.background_color, rectangle)

    def update(self):
        """ Updates local attributes by observing hex map. """
        pass

    def draw(self, surf):
        """ Draws the element on a surface at a specified position. """
        surf.blit(self.surface, self.position)


class StateCounter(DataVizElement):
    """ UI element that displays the relative count of different states in the
        hex map over time.
    """

    def __init__(self, hex_map):
        """ Create StateCounter object. """

        DataVizElement.__init__(self, hex_map)
        buffer_size = 100
        self.buffer = [0] * buffer_size
        self.position = (10, WINDOW_HEIGHT - UI_ELEMENT_HEIGHT - 10)  # TODO don't hardcode position

    def update(self):

        histogram = self.map.state_histogram()
        total_cell_count = sum(histogram.values())
        if total_cell_count == 0:
            proportion_green = 0
        else:
            proportion_green = histogram[GREEN_STATE]/total_cell_count
        self.buffer.pop()
        self.buffer.insert(0, proportion_green)

    def draw(self, surf):
        """ Draws the element on a surface at a specified position. """

        # Clear surface
        self.clear()

        # Draw count over time figure
        self.draw_buffer((15, 10), height=80)

        # Draw text representation
        self.draw_proportion_text()

        surf.blit(self.surface, self.position)

    def meter_rectangle(self, proportion, background_color=BLACK, foreground_color=GREEN, width=1, height=80):
        """ Returns a rectangular pygame Surface that is filled a particular proportion.

            inputs:
                proportion (float): A value (0, 1) for how filled the bar should be
                background_color (tuple): an RGB tuple for the background of the bar
                foreground_color (tuple): an RGB tuple for the foreground of the bar
                width (int): The width of the surface, in pixels
                height (int): The height of the surface, in pixels
        """

        surface = pygame.Surface((width, height))
        surface.fill(background_color)
        bar_height = int(height * proportion)   # Width of foreground area
        pygame.draw.rect(surface, foreground_color, (0, height - bar_height, width, bar_height))
        return surface

    def draw_buffer(self, position, height=80):
        """ Draws the entire buffer of meter rectangles onto the screen. This forms a graph representing
            proportion over time.

            inputs:
                position: position to draw the graph, from the top left corner
                height: height of the graph, in pixels
        """

        bars = [self.meter_rectangle(value, width=1, height=height) for value in self.buffer][::-1]
        x_offset = 0
        for bar in bars:
            x, y = position
            x += x_offset
            self.surface.blit(bar, (x, y))
            x_offset += 1

    def draw_proportion_text(self, color=GREEN, inverse_color=GRAY):
        """ Draws text relating to the first proportion in the buffer onto the element, as a percentage.
            This text is formatted as a floating point number, truncated to two decimel points,
            followed by a percent sign.

            inputs:
                color (tuple): RGB tuple for the color of the active proportion
                inverse_color (tuple): RGB tuple for the color of the inactive proportion
        """

        # Draw active proportion text
        proportion = self.buffer[0]
        text = "%.2f%%" % (proportion * 100)
        render = self.large_font.render(text, 1, color)
        self.surface.blit(render, (124, 55))

        # Draw inactive proportion text
        inverse_proportion = 1 - proportion
        inverse_text = "%.2f%%" % (inverse_proportion * 100)
        inverse_render = self.large_font.render(inverse_text, 1, inverse_color)
        self.surface.blit(inverse_render, (124, 30))

