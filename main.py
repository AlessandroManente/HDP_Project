import networkx as nx
import matplotlib.pyplot as plt
import argparse
from utils.basic_graphs_utilities import *


def parsing():
    '''
    Parse arguments given when calling function. Arguments are:
    - d : parameter defining the magnitude of the probability of nodes being connected
    - n : number of nodes (note that the probability is computed as p = d / n)
    - k : each node is connected to k nearest neighbors
    - t : type of graph you want to generat and print
    '''
    parser = argparse.ArgumentParser(
        description='Generate a G(n,p) random graph')

    parser.add_argument('--d',
                        type=float,
                        default=1,
                        help='parameter probability')
    parser.add_argument('--n', type=float, default=10, help='number of nodes')
    parser.add_argument('--k',
                        type=int,
                        default=3,
                        help='number k nearest neighbors')
    parser.add_argument('--t',
                        type=str,
                        default='erdos_renyi',
                        help='tipology of graph')

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    G = generate_graph(parsing())
    print_graph(G)
