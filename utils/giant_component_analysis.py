import networkx as nx
import pandas as pd
import numpy as np
from utils.basic_graphs_utilities import *


def find_components(graph):
    '''
    Returns the size of the greatest connected component and the number of
    connected components in the given graph
    '''
    cc = connected_components(graph)

    return [cc[0], len(cc)]


def giant_components_fixed_args(args, d=None):
    '''
    Test the presence and dimension of giant connected component as well as number of
    usual connected components for fixed parameters, for a given number of times args.m.
    '''
    data = []
    for i in range(args.gm):
        if d is None:
            graph = generate_graph(args)
        else:
            graph = generate_graph(args, d)

        data_cc = find_components(graph)
        data.append(data_cc)

    return pd.DataFrame(
        data,
        columns=['size_giant_component', 'number_of_connected_components'])


def giant_component_varying_d(args, mean=False):
    '''
    Test the presence and dimension of giant connected component as well as number of
    usual connected components for a varying value of d.
    TODO: rethink the distribution of the d's.
    '''
    data = []

    # d_list = list(range(0.01, args.n, (args.n - 0.01) / args.gmd))
    d_list = list(np.arange(0.01, args.n, (args.n - 0.01) / args.gmd))

    if mean:
        for d in d_list:
            data_cc = giant_components_fixed_args(args, d)
            data.append([
                data_cc['size_giant_component'].mean(),
                data_cc['number_of_connected_components'].mean()
            ])

    else:
        for d in d_list:
            graph = generate_graph(args, d)
            data_cc = find_components(graph)
            data.append(data_cc)

    return pd.DataFrame(
        data,
        columns=['size_giant_component', 'number_of_connected_components'])


def main_giant(args):
    data_fixed_args = giant_components_fixed_args(args)
    data_varying_d = giant_component_varying_d(args, args.gmean)

    plt.plot(np.arange(len(data_fixed_args['size_giant_component'])),
             data_fixed_args['size_giant_component'])
    plt.title('Size giant component in various trials - fixed parameters')
    plt.show()

    plt.plot(np.arange(len(data_fixed_args['number_of_connected_components'])),
             data_fixed_args['number_of_connected_components'])
    plt.title('Number of components in various trials - fixed parameters')
    plt.show()

    plt.plot(np.arange(0.01, args.n, (args.n - 0.01) / args.gmd),
             data_varying_d['size_giant_component'])
    plt.title('Size giant component in various trials - varying d')
    plt.show()

    plt.plot(np.arange(0.01, args.n, (args.n - 0.01) / args.gmd),
             data_varying_d['number_of_connected_components'])
    plt.title('Number of components in various trials - varying d')
    plt.show()

    return data_fixed_args, data_varying_d
