import networkx as nx
import pandas as pd
import numpy as np
from utils.basic_graphs_utilities import *


def count_degrees(args, d=None):
    '''
    Counts the degrees depending on the args, eventually d
    can be specified
    '''
    if d is None:
        graph = generate_graph(args)
    else:
        graph = generate_graph(args, d)

    degrees = [val for (node, val) in graph.degree()]

    return degrees


def count_degrees_fixed_d(args, d=None):
    '''
    Compute the degrees of each node of the graph for 
    fixed arguments, it can save the mean value for each 
    node and d if required.
    '''
    data = []

    for i in range(args.ndm):
        degrees = count_degrees(args)
        data.append(degrees)

    data_df = pd.DataFrame(
        data, columns=['degree_node' + str(i) for i in range(args.n)])

    return data_df


def count_degrees_varying_d(args, mean=False):
    '''
    Compute the degrees of each node of the graph at varying 
    value of d, it can save the mean value for each node and d 
    if required.
    TODO: rethink the distribution of the d's.
    '''
    data_df = []

    d_list = list(np.arange(0.01, args.n, (args.n - 0.01) / args.ndmd))

    if mean:
        for d in d_list:
            degrees = count_degrees_fixed_d(args, d)
            data_df.append(degrees)

    else:
        for d in d_list:
            degrees = count_degrees(args, d)
            data_df.append(degrees)

    data_df = pd.DataFrame(
        data_df, columns=['degree_node' + str(i) for i in range(args.n)])

    return data_df


def main_node_distribution(args):
    data_fixed_args = count_degrees_fixed_d(args)
    data_varying_d = count_degrees_varying_d(args, args.ndmean)

    plt.plot(np.arange(len(data_fixed_args.mean())), data_fixed_args.mean())
    plt.title('Degrees of nodes - fixed parameters')
    plt.show()

    plt.plot(np.arange(len(data_fixed_args.iloc[:, 0])),
             data_fixed_args.iloc[:, 0])
    plt.title('Degrees of node 0 - fixed parameters')
    plt.show()

    return data_fixed_args, data_varying_d
