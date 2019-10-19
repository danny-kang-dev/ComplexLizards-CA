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
from matplotlib.font_manager import FontProperties
import numpy as np
import pandas as pd
import seaborn as sns

import networkx as nx
import random
from pylab import *


hexmap = HexMap(width=100, height=100)
# hexmap = HexMap(width=25, height=25)

all_vals = dict()

def create_hexmap(hexmap, show=False):
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

def convert_graph_draw(hexmap, steps=0, show=False):
    all_data = []
    all_steps = []
    distributions = []
    for i in range(steps):
        if (i % 10) == 0:
            all_steps.append(i)
            all_data.append(get_data(create_hexmap(hexmap)))
        distributions.append(hexmap.state_histogram())
        hexmap.step()
    distributions.append(hexmap.state_histogram())

    green_num = []
    black_num = []
    white_num = []
    brown_num = []

    for x in distributions:
        green_num.append(x[GREEN_STATE])
        white_num.append(x[WHITE_STATE])
        black_num.append(x[BLACK_STATE])
        brown_num.append(x[BROWN_STATE])

    fig, ax = plt.subplots()

    plt.plot(green_num, color='green', label='Green')
    plt.plot(white_num, color='grey', label='White')
    plt.plot(brown_num, color='brown', label='Brown')
    plt.plot(black_num, color='black', label='Black')
    plt.xlabel('Time Step')
    plt.ylabel('Number of Nodes')
    plt.title('Plot of Number of Colored Nodes over Time')
    fontP = FontProperties()
    fontP.set_size('small')
    plt.legend(prop=fontP)
    plt.show()

    all_data.append(get_data(create_hexmap(hexmap)))
    all_steps.append(steps)
    fig, ax = plt.subplots()
    plt.yscale('log')
    all = [x for x in range(0, len(all_data) )]
    bp = boxplot(all_data, positions = all, manage_ticks=True, widths = 0.6)
    plt.xticks(range(0, len(all)), all_steps, fontsize=6)
    plt.title('Boxplot of Subgraph Size over Time')
    plt.xlabel('Time Step')
    plt.ylabel('Number of Nodes in Subgraph')
    plt.show()
    X = create_hexmap(hexmap, True)
    return X

def get_data(G):
    num_nodes = np.array([])
    for i in sorted(nx.connected_components(G), key=len, reverse=True):
        num_nodes = np.append(num_nodes, len(i))
    return num_nodes

def get_pmf_data(num_nodes, steps=None):
    val, cnt = np.unique(num_nodes, return_counts=True)
    pmf = cnt / len(num_nodes)
    X = np.column_stack((val, pmf))
    _, ax = plt.subplots()
    ax.bar(x=X[:, 0], height=X[:, 1])
    ax.set_yscale('log')
    ax.set_xscale('log')
    title = 'Initial state (Max: %s nodes)' %(str(int(num_nodes[0]))) if not steps else '%s steps (Max: %s nodes)' %(str(steps), str(int(num_nodes[0])))
    plt.title(title, fontdict=None, loc='center', pad=None)
    plt.xlabel('Number of nodes (per connected subgraph)')
    plt.ylabel('PMF')
    plt.show()

def plot_graph_cdf(G, steps=None):
    num_nodes = np.array([])
    for i in sorted(nx.connected_components(G), key=len, reverse=True):
        num_nodes = np.append(num_nodes, len(i))
    val, cnt = np.unique(num_nodes, return_counts=True)
    pmf = cnt / len(num_nodes)
    cdf = np.cumsum(pmf)
    title = 'Initial state' if not steps else '%s steps' %(str(steps))
    plt.title(title, fontdict=None, loc='center', pad=None)
    plt.xlabel('Number of nodes (per connected subgraph)')
    plt.ylabel('CDF')
    plot(val, cdf)
    show()

def plot_graph_pmf(G, steps=None):
    X = get_pmf_data(get_data(G), steps=steps)
    plt.bar(x=X[:, 0], height=X[:, 1])
    plt.show()

G = convert_graph_draw(hexmap, steps=500)
plot_graph_pmf(G,500)
# plot_graph_cdf(G,)



# G = convert_graph_draw(hexmap, steps=150, show=True)
# plot_graph_pmf(G)
