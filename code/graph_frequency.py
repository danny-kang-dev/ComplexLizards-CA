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
 
hex_map = HexMap(width=35, height=25)
hex_map.set_update_function(helpers.manukyan)

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

def draw_pmf(hexmap, cell_color):
    df = pd.DataFrame({'x': range(7), 'y': update_pmf_values(hexmap, cell_color)})
    plt.plot( 'x', 'y', data=df, linestyle='-', marker='o')
    plt.pause(0.0001)
    plt.clf()

for i in range(100):
    time.sleep(0.1)
    draw_pmf(hex_map, 1)
    hex_map.step()    

