import networkx as nx
import matplotlib.pyplot as plt
import argparse
from utils.basic_graphs_utilities import *
from utils.giant_component_analysis import *
from utils.node_degree_distribution import *
from utils.path_length_analysis import *
from utils.clustering_coefficient_analysis import *
import os


def erdos_renyi_analysis(args):
    '''
    Function that calls all the analysis for the erdos_renyi model
    '''
    print('----- Analysis of ER model -----')
    tipology = 'erdos_renyi'
    if not tipology in os.listdir(os.path.join('results', str(args.n))):
        os.mkdir(os.path.join('results', str(args.n), tipology))

    main_giant(args, tipology)
    main_node_distribution(args, tipology)


def barabasi_albert_analysis(args):
    '''
    Function that calls all the analysis for the barabasi_albert model
    '''
    print('----- Analysis of BA model -----')
    tipology = 'barabasi_albert'
    if not tipology in os.listdir(os.path.join('results', str(args.n))):
        os.mkdir(os.path.join('results', str(args.n), tipology))

    main_node_distribution(args, tipology)
    main_average_path_length(args, tipology)


def watts_strogatz_analysis(args):
    '''
    Function that calls all the analysis for the watts_strogatz model
    '''
    print('----- Analysis of WS model -----')
    tipology = 'watts_strogatz'
    if not tipology in os.listdir(os.path.join('results', str(args.n))):
        os.mkdir(os.path.join('results', str(args.n), tipology))

    main_node_distribution(args, tipology)
    main_average_path_length(args, tipology)
    main_average_path_length(args, tipology)


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
    - a shit-ton of other paramaters, sorry guys
    '''
    parser = argparse.ArgumentParser(
        description='Generate a G(n,p) random graph')

    parser.add_argument('--d',
                        type=float,
                        default=1,
                        help='parameter probability')

    parser.add_argument('--n', type=int, default=1000, help='number of nodes')

    parser.add_argument('--k',
                        type=int,
                        default=10,
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
                        default=True,
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
        "number of edges to add to the new node at each iteration of the growth of the model"
    )

    parser.add_argument(
        '--aplmean',
        type=bool,
        default=True,
        help="compute mean of average path length at increasing values of n")

    parser.add_argument(
        '--aplmeansamples',
        type=int,
        default=1,
        help=
        "number of samples to compute mean of average path length at increasing values of n"
    )

    parser.add_argument(
        '--aplwsvaryingbeta',
        type=bool,
        default=True,
        help=
        "true if you want to study the length depending on the beta parameter (pws)"
    )

    parser.add_argument(
        '--ccmean',
        type=bool,
        default=True,
        help="compute mean of clustering coefficient at increasing values of n"
    )

    parser.add_argument(
        '--cmeansamples',
        type=int,
        default=1,
        help=
        "number of samples to compute mean of clustering coefficient at increasing values of n"
    )

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parsing()

    # create a folder for the analysis of a given number of nodes
    if not str(args.n) in os.listdir(os.path.join('results')):
        os.mkdir(os.path.join('results', str(args.n)))

    main_clustering_coefficient(args, 'watts_strogatz')

    # if args.all:
    #     for key, tipology in analysis.items():
    #         tipology(args)
    # else:
    #     analysis[args.t](args)