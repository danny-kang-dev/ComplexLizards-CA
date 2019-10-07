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

import networkx as nx
import random

hexmap = HexMap(width=35, height=25)

def convert_graph_draw(hexmap, steps):

    for i in range(steps):
        hexmap.step()

    X=nx.Graph()

    node_num = 1
    offset = 0
    colors = []
    for index, row in enumerate(hexmap.array):
        for i, cell in enumerate(row):
            if cell.state == GREEN_STATE:
                colors.append('green')
            elif cell.state == BLACK_STATE:
                colors.append('black')
            elif cell.state == BROWN_STATE:
                colors.append('brown')
            else:
                colors.append('gray')
            cell.node_num = node_num
            X.add_node(node_num, pos=(10*i+offset, 25-index))
            node_num += 1
        offset += 5
    pos=nx.get_node_attributes(X,'pos')

    for row in hexmap.array:
        for cell in row:
            cell.observe_neighbors()
            for neighbor in cell.neighbors:
                if cell.state == neighbor.state:
                    X.add_edge(cell.node_num, neighbor.node_num)
    

    nx.draw(X,pos, node_size=50, node_color=colors)
    plt.show()

convert_graph_draw(hexmap,250)