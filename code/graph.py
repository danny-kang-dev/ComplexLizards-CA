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
        if cell.state == cell_color:
            for neighbor in cell.neighbors:
                neighbor.observe_neighbors()
                if sum(neighbor.stored_neighbor_states) == num_neighbors:
                    count += 1
    return count

def update_pmf_values(hexmap, cell_color):
    """ produces list of pmf values for cell_color
        for each number of neighbors
    """
    y_values_black = []
    y_values_green = []
    pmf = []
    y_val = 0
    if cell_color:
        for i in range (7):
            y_val = count_scale_neighbor(hexmap, i, 1)
            y_values_black.append(y_val)
        total = sum(y_values_black)
        for val in y_values_black:
            pmf.append(val/total)
        return pmf
    else:
        for i in range (7):
            y_val = count_scale_neighbor(hexmap, i, 0)
            y_values_green.append(y_val)
        total = sum(y_values_green)
        for val in y_values_green:
            pmf.append(val/total)
        return pmf

def draw_pmf(update_function, steps):
    """ draw pmf graph for each state of HexMap object
    """
    hexmap = HexMap(width=35, height=25)
    hexmap.set_update_function(update_function)
    if update_function == helpers.manukyan:
        y_lim = 0.45
    else:
        y_lim = 1
    plt.ion()
    for i in range(steps):
        time.sleep(0.0001)
        df1 = pd.DataFrame({'x': range(7), 'y': update_pmf_values(hexmap, 1)})
        df2 = pd.DataFrame({'x': range(7), 'y': update_pmf_values(hexmap, 0)})
        _, ax = plt.subplots()
        plt.ylim(0, y_lim)
        plt.xlabel('number of neighbors')
        plt.ylabel('frequency')

        ax.plot( 'x', 'y', data=df1, linestyle='-', marker='o', color = 'green', label = 'Green')
        ax.plot( 'x', 'y', data=df2, linestyle='-', marker='o', color = 'black', label = 'Black')

        ax.legend(loc='upper right', shadow=True, fontsize='x-large')
        plt.pause(0.0001)
        plt.clf()
        hexmap.step()
    

draw_pmf(helpers.manukyan, 100)
draw_pmf(helpers.deterministic, 100)