# Standard libraries
import time
import sys

# Project modules
import helpers
from view import View
from hexMap import HexMap
from constants import *

# libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

def count_scale_neighbor(hexmap, num_neighbors, cell_color):
    """ Counts number of cells with num_neighbors number of
        differently colored neighbors
    """
    count = 0
    for cell in hexmap.tiles():
        if cell.state != cell_color:
            cell.observe_neighbors()
            if cell.stored_neighbor_states.count(cell_color) == num_neighbors:
                count += 1
    return count

def update_pmf_values(hexmap, cell_color):
    """ produces list of pmf values for cell_color
        for each number of neighbors
    """
    y_values = []
    pmf = []
    y_val = 0
    if cell_color == 0:
        val_other = 1
    elif cell_color == 1:
        val_other = 0
    elif cell_color == 2:
        val_other = 3
    elif cell_color == 3:
        val_other = 2
    else:
        raise ValueError("Current state is invalid.")

    for i in range (7):
        y_val = count_scale_neighbor(hexmap, i, val_other)
        y_values.append(y_val)
    total = sum(y_values)
    for val in y_values:
        if total == 0:
            pmf.append(0)
        else:
            pmf.append(val/total)

    return pmf


def draw_pmf(update_function, steps):
    """ draw pmf graph for each state of HexMap object
    """
    hexmap = HexMap(width=35, height=25)
    hexmap.set_update_function(update_function)
    if update_function == helpers.manukyan:
        y_lim = 0.5
    else:
        y_lim = 1
    plt.ion()
    for i in range(steps):
        time.sleep(0.0001)
        df1 = pd.DataFrame({'x': range(7), 'y': update_pmf_values(hexmap, 1)})
        df2 = pd.DataFrame({'x': range(7), 'y': update_pmf_values(hexmap, 0)})
        df3 = pd.DataFrame({'x': range(7), 'y': update_pmf_values(hexmap, 2)})
        df4 = pd.DataFrame({'x': range(7), 'y': update_pmf_values(hexmap, 3)})
        plt.ylim(0, y_lim)
        plt.xlabel('number of neighbors')
        plt.ylabel('frequency')

        plt.plot( 'x', 'y', data=df1, linestyle='-', marker='o', color = 'green', label = 'Green')
        plt.plot( 'x', 'y', data=df2, linestyle='-', marker='o', color = 'black', label = 'Black')
        plt.plot( 'x', 'y', data=df3, linestyle='-', marker='o', color = 'brown', label = 'Brown')
        plt.plot( 'x', 'y', data=df4, linestyle='-', marker='o', color = 'red', label = 'White')

        plt.legend(loc='upper right', shadow=True, fontsize='x-large')
        plt.pause(0.0001)

        plt.clf()
        hexmap.step()


draw_pmf(helpers.manukyan, 500)
# draw_pmf(helpers.deterministic, 10)
