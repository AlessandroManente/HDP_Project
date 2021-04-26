import networkx as nx
import matplotlib.pyplot as plt
import argparse
from utils.basic_graphs_utilities import *
from utils.giant_component_analysis import *
from utils.node_degree_distribution import *
from utils.path_length_analysis import *
from utils.clustering_coefficient_analysis import *


def erdos_renyi_analysis(args):
    test_1, test_2 = main_giant(args)
    test_3, test_4 = main_node_distribution(args)

    return test_1, test_2, test_3, test_4


def barabasi_albert_analysis(args):
    test_1, test_2 = main_node_distribution(args)
    test_3, test_4 = main_average_path_length(args)

    return test_1, test_2, test_3, test_4


def watts_strogatz_analysis(args):
    test_1, test_2 = main_average_path_length(args)
    #test_1, test_2 = main_clustering_coefficient(args)

    return test_1, test_2

    pass


analysis = {
    'erdos_renyi': erdos_renyi_analysis,
    'barabasi_albert': barabasi_albert_analysis,
    'watts_strogatz': watts_strogatz_analysis
}


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

    parser.add_argument('--n', type=int, default=10, help='number of nodes')

    parser.add_argument('--k',
                        type=int,
                        default=2,
                        help='number k nearest neighbors for WS')

    parser.add_argument('--t',
                        type=str,
                        default='erdos_renyi',
                        help='tipology of graph')

    parser.add_argument('--gm',
                        type=int,
                        default=100,
                        help='number of trials to make statistics')

    parser.add_argument('--gmd',
                        type=int,
                        default=100,
                        help="number of d's to make statistics")

    parser.add_argument('--gmean',
                        type=bool,
                        default=False,
                        help="compute mean of giant component study")

    parser.add_argument(
        '--ndm',
        type=int,
        default=100,
        help="number of graph of which compute degrees of nodes")

    parser.add_argument('--ndmean',
                        type=bool,
                        default=False,
                        help="compute mean of node distribution study")

    parser.add_argument('--all',
                        type=bool,
                        default=False,
                        help="execute analysis of all three types of graphs")

    parser.add_argument('--ndmd',
                        type=int,
                        default=100,
                        help="number of d's to make statistics")

    parser.add_argument('--pws',
                        type=float,
                        default=0.95,
                        help="probability of rewiring a node in WS model")

    parser.add_argument(
        '--mba',
        type=int,
        default=1,
        help=
        "number of nodes to add at each iteration of the growth of the model")

    parser.add_argument(
        '--aplmean',
        type=bool,
        default=False,
        help="compute mean of average path length at increasing values of n")

    parser.add_argument(
        '--aplmeansamples',
        type=int,
        default=100,
        help=
        "number of samples to compute mean of average path length at increasing values of n"
    )

    parser.add_argument(
        '--ccmean',
        type=bool,
        default=False,
        help="compute mean of clustering coefficient at increasing values of n")

    parser.add_argument(
        '--cmeansamples',
        type=int,
        default=100,
        help=
        "number of samples to compute mean of clustering coefficient at increasing values of n"
    )

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parsing()

    results = []
    if args.all:
        for key, tipology in analysis.items():
            results.append(tipology(args))
    else:
        results.append(analysis[args.t](args))