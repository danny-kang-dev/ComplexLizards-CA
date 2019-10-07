from constants import *
from helpers import *
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
        self.num_steps = 0 # Number of steps taken so far; used to help color switching

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

    def step(self):
        """ Updates each cell in the automaton. The cell should have an observe_neighbors method that
            observes the states of nearby cells and an update_state method that applies changes for
            the step.
        """
        self.num_steps += 1
        # Store neighbor states for each cell
        for cell in self.tiles():
            cell.observe_neighbors()

        # Update each cell
        for cell in self.tiles():
            cell.update_state(self.num_steps)

    def set_update_function(self, new_func):
        """ Sets the update function for all cells in the array. See HexCell.set_update_function"""

        for cell in self.tiles():
            cell.set_update_function(new_func)

    def state_histogram(self):
        """ Returns a dictionary mapping different states to their respective counts in the map. """

        dictionary = {}
        for cell in self.tiles():
            dictionary[cell.state] = dictionary.get(cell.state, 0) + 1
        return dictionary


class HexCell(object):
    """ Represents a hexagonal cell in a 2D array. """

    def __init__(self):
        self.state = None
        self.randomize_state()
        self.neighbors = []
        self.stored_neighbor_states = None
        self.update_function = manukyan
        self.unique_color = WHITE   # TODO: Consider eveyrthing a diffusion model to slowly have colors change
        self.node_num = 0

    def set_neighbors(self, neighbors):
        """ Assigns neighbors to the HexCell. """
        self.neighbors = neighbors

    def observe_neighbors(self):
        """ Observes neighboring cells and stores their states in self.stored_neighbor_states. """
        self.stored_neighbor_states = [neighbor.state for neighbor in self.neighbors]

    def update_state(self, curr_turn=0):
        """ Updates the cell's current state based on the observed state of its neighbors.
            Observe_neighbors should be called prior to updating the state.
        """

        if self.stored_neighbor_states is None:
            raise ValueError("No neighboring states are stored. Did you call HexCell.observe_neighbors?")

        # Update current state based on update function
        self.state = self.update_function(self.state, self.stored_neighbor_states, curr_turn)

        # Reset stored neighbor states, so update isn't called twice
        self.stored_neighbor_states = None

    def set_update_function(self, new_func):
        """ Changes the function that updates a cell's state.

            inputs:
                new_func(current_state, neighbors): takes two arguments ---
                    - current_state (int): state of current cell
                    - neighbors (list): list of neighboring cell states
        """

        # TODO make sure update function is valid if using multiple states
        self.update_function = new_func

    def color(self):
        """ Returns an RGB color value based on the current state. """
        # TODO expand switch statement for more than two states
        if self.state is BLACK_STATE:
            return GRAY
        elif self.state is GREEN_STATE:
            return GREEN
        elif self.state is BROWN_STATE:
            return BROWN
        elif self.state is WHITE_STATE:
            return WHITE
        return RED

    def randomize_state(self, aging=True):
        """ Sets the state to a random value. """
        # TODO expand to choose between all valid states, if more than two
        # We want to start off as white/brown, so we want to randomize between 2/3 to start
        if not aging:
            self.state = random.choice([0, 1])
        else:
            self.state = random.choice([2, 3])

    def __repr__(self):
        return "<HexCell at %s, state %s>" % (id(self), self.state)
