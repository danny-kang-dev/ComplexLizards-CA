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

def convert_graph_draw(hexmap, steps=0, show=False):
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
    pos = nx.get_node_attributes(X,'pos')

    for row in hexmap.array:
        for cell in row:
            cell.observe_neighbors()
            for neighbor in cell.neighbors:
                if cell.state == neighbor.state:
                    X.add_edge(cell.node_num, neighbor.node_num)
    if show:
        nx.draw(X,pos, node_size=50, node_color=colors)
        plt.show()
    return X

def plot_graph_pmf(G):
    num_nodes = np.array([])
    for i in sorted(nx.connected_components(G), key=len, reverse=True):
        num_nodes = np.append(num_nodes, len(i))
    val, cnt = np.unique(num_nodes, return_counts=True)
    pmf = cnt / len(num_nodes)
    X = np.column_stack((val, pmf))
    plt.bar(x=X[:, 0], height=X[:, 1])
    plt.show()
    
G = convert_graph_draw(hexmap, show=True)
plot_graph_pmf(G)