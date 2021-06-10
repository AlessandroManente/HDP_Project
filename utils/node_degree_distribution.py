import networkx as nx
import pandas as pd
import numpy as np
from utils.basic_graphs_utilities import *
from os import path
plt.style.use("ggplot")


def count_degrees(args, d=None, tipology=None):
    '''
    Counts the degrees depending on the args, eventually d
    can be specified
    '''
    graph = generate_graph(args, d, None, tipology)
    degrees = [val for (node, val) in graph.degree()]

    return degrees


def count_degrees_fixed_d(args, d=None, tipology=None):
    '''
    Compute the degrees of each node of the graph for 
    fixed arguments, it can save the mean value for each 
    node and d if required.
    '''
    data = []

    for i in range(args.ndm):
        degrees = count_degrees(args, d, tipology)
        data = data + degrees

    return data


def count_degrees_varying_d(args, tipology=None):
    '''
    Compute the degrees of each node of the graph at varying 
    value of d, it can save the mean value for each node and d 
    if required.
    TODO: rethink the distribution of the d's.
    '''
    data = []

    d_list = [i / 100 for i in range(0, 201, 2)]

    for d in d_list:
        degrees = count_degrees_fixed_d(args, d, tipology)
        data = data + degrees

    return data


def main_node_distribution(args, tipology):
    '''
    Main function that calls subroutines and plot and save the results
    '''
    data_fixed_args = count_degrees_fixed_d(args, None, tipology)
    data_varying_d = count_degrees_varying_d(args, tipology)

    plt.figure()
    plt.hist(data_fixed_args, bins=10)
    plt.title('Distribution of degrees of nodes with d={}'.format(args.d))
    plt.xlabel('k (degree)')
    plt.ylabel('Counts')
    plt.savefig(
        path.join('results', str(args.n), tipology,
                  'ndd_allnodes_dist_fixed_{}.png'.format(tipology)))
    # plt.show()

    # USELESS as shit
    plt.figure()
    plt.hist(data_varying_d, bins=10)
    plt.title('Distribution of degrees of nodes - varying parameters')
    plt.savefig(
        path.join('results', str(args.n), tipology,
                  'ndd_allnodes_dist_varying_{}.png'.format(tipology)))
    # plt.show()

    return data_fixed_args, data_varying_d
