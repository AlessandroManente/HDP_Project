import networkx as nx
import numpy as np
from utils.basic_graphs_utilities import *
from os import path


def compute_clustering_coefficient(args, tipology=None):
    empirical_values = []
    theoretical_values = []

    for i in range(3, args.n + 1):
        if args.ccmean:
            temp = []

            for j in range(args.ccmeansamples):
                graph = generate_graph(args, None, i, tipology)
                clustering_coefficient = nx.algorithms.cluster.clustering(graph)
                temp.append(clustering_coefficient)

            clustering_coefficient = np.mean(temp)

        else:
            graph = generate_graph(args, None, i, tipology)
            clustering_coefficient = nx.algorithms.cluster.clustering(graph)

        empirical_values.append(clustering_coefficient)

        theoretical_values.append(args.k / (i - 1))

    return empirical_values, theoretical_values


def main_clustering_coefficient(args, tipology):
    empirical_values, theoretical_values = compute_clustering_coefficient(
        args, tipology)

    plt.plot(list(range(3, args.n + 1)), empirical_values, label="empirical")
    plt.plot(list(range(3, args.n + 1)),
             theoretical_values,
             label="theoretical")
    plt.legend()
    plt.title(
        'Empirical clustering coefficient against theoretical one -' +
        args.t + ' m =' + str(args.mba))
    plt.savefig(path.join('results', 'cca_{}.png'.format(tipology)))
    # plt.show()

    return empirical_values, theoretical_values