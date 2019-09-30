from constants import *
import random


class HexMap(object):
    """ Represents a 2D array of hexagonal cells. """

    def __init__(self, width=50, height=50):
        """ Creates the HexMap object.

            inputs:
                width (int): width of array, in tiles
                height (int): height of array, in tiles
        """

        self.width = width
        self.height = height
        self.array = self.populate_cell_array()

        # Assign neighbors to each cell
        self.neighbor_kernel = HEX_KERNEL
        for _, position in self.tiles(index=True):
            self.assign_neighbors(*position)

    def populate_cell_array(self):
        """ Returns an n*m nested list of HexCell objects, where n is
            the height of the array and m is the width.
        """

        row = lambda n: [HexCell() for _ in range(n)]
        array = [row(self.width) for _ in range(self.height)]
        return array

    def assign_neighbors(self, y, x):
        """ Assigns the correct neighbors to the cell at position (y, x).

            inputs:
                y (int): row of cell to populate
                x (int): column of cell to populate
        """

        cell = self.array[y][x]

        # Add a neighbor to the cell for each 1 in the neighbor kernel
        neighbors = []
        for k_y, row in enumerate(self.neighbor_kernel):
            for k_x, value in enumerate(row):
                y_neighbor = y + k_y - 1
                x_neighbor = x + k_x - 1
                if value and self.in_array_bounds(y=y_neighbor, x=x_neighbor):
                    new_neighbor = self.array[y_neighbor][x_neighbor]
                    neighbors.append(new_neighbor)

        # Set the cell's neighbor field
        cell.set_neighbors(neighbors)

    def in_array_bounds(self, y=0, x=0):
        """ Returns True if the coordinate (y, x) is the valid position of
            a tile. If unspecified, an argument defaults to zero, so you can
            call in_array_bounds(x=_) to only check an x value.
        """

        if y < 0 or y >= len(self.array):
            return False
        if x < 0 or x >= len(self.array[0]):
            return False
        return True

    def tiles(self, index=False):
        """ Generator function that yields each HexCell in the HexMap.

            If index is True, instead returns a tuple, where the first
            item is the cell object, and the second item is its (y, x) position.
        """

        for y, row in enumerate(self.array):
            for x, item in enumerate(row):
                if index:
                    yield item, (y, x)
                else:
                    yield item


class HexCell(object):
    """ Represents a hexagonal cell in a 2D array. """

    def __init__(self):
        self.state = 0
        self.neighbors = []

    def set_neighbors(self, neighbors):
        """ Assigns neighbors to the HexCell. """
        self.neighbors = neighbors
        self.randomize_state()

    def color(self):
        """ Returns an RGB color value based on the current state. """
        if self.state == 0:
            return GRAY
        elif self.state == 1:
            return GREEN
        return RED

    def randomize_state(self):
        """ Sets the state to a random value. """
        self.state = random.choice([0, 1])

    def __repr__(self):
        return f"<HexCell at {id(self)}, state {self.state}>"
