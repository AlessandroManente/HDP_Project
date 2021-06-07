import networkx as nx
import pandas as pd
import numpy as np
from utils.basic_graphs_utilities import *
from os import path
plt.style.use("ggplot")


def find_components(graph):
    '''
    Returns the size of the greatest connected component and the number of
    connected components in the given graph
    '''
    cc = connected_components(graph)

    return [cc[0], len(cc)]


def giant_components_fixed_args(args, d=None, tipology=None):
    '''
    Test the presence and dimension of giant connected component as well as number of
    usual connected components for fixed parameters, for a given number of times args.m.
    '''
    data = []
    for i in range(args.gm):
        if d is None:
            graph = generate_graph(args, None, None, tipology)
        else:
            graph = generate_graph(args, d, None, tipology)

        data_cc = find_components(graph)
        data.append(data_cc)

    return pd.DataFrame(
        data,
        columns=['size_giant_component', 'number_of_connected_components'])


def giant_component_varying_d(args, mean=False, tipology=None):
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
            data_cc = giant_components_fixed_args(args, d, None, tipology)
            data.append([
                data_cc['size_giant_component'].mean(),
                data_cc['number_of_connected_components'].mean()
            ])

    else:
        for d in d_list:
            graph = generate_graph(args, d, None, tipology)
            data_cc = find_components(graph)
            data.append(data_cc)

    return pd.DataFrame(
        data,
        columns=['size_giant_component', 'number_of_connected_components'])


def main_giant(args, tipology=None):
    '''
    Main function that calls subroutines and plot and save the results.
    Here are shown the size of the giant component and the number of components,
    both with fixed parameters or varying the value of args.d.
    '''
    data_fixed_args = giant_components_fixed_args(args, None, tipology)
    data_varying_d = giant_component_varying_d(args, args.gmean, tipology)

    plt.figure()
    plt.plot(np.arange(len(data_fixed_args['size_giant_component'])),
             data_fixed_args['size_giant_component'])
    plt.title('Size giant component in various trials - fixed parameters')
    plt.xlabel('Number of trial')
    plt.ylabel('Size of giant component')
    plt.savefig(path.join('results', str(args.n), tipology, 'gca_size_fixed_{}.png'.format(tipology)))
    # plt.show()

    plt.figure()
    plt.plot(np.arange(len(data_fixed_args['number_of_connected_components'])),
             data_fixed_args['number_of_connected_components'])
    plt.title('Number of components in various trials - fixed parameters')
    plt.xlabel('Number of trial')
    plt.ylabel('Number of components')
    plt.savefig(
        path.join('results', str(args.n), tipology,
                  'gca_ncomp_fixed_{}.png'.format(tipology)))
    # plt.show()

    plt.figure()
    plt.plot(np.arange(0.01, args.n, (args.n - 0.01) / args.gmd),
             data_varying_d['size_giant_component'])
    plt.title('Size giant component in various trials - varying d')
    plt.xlabel('d')
    plt.ylabel('Size of giant component')
    plt.savefig(
        path.join('results', str(args.n), tipology,
                  'gca_size_varying_{}.png'.format(tipology)))
    # plt.show()

    plt.figure()
    plt.plot(np.arange(0.01, args.n, (args.n - 0.01) / args.gmd),
             data_varying_d['number_of_connected_components'])
    plt.title('Number of components in various trials - varying d')
    plt.xlabel('d')
    plt.ylabel('Number of components')
    plt.savefig(
        path.join('results', str(args.n), tipology,
                  'gca_ncomp_varying_{}.png'.format(tipology)))
    # plt.show()

    return data_fixed_args, data_varying_d
