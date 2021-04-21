import networkx as nx
import numpy as np
from utils.basic_graphs_utilities import *


def compute_clustering_coefficient(args):
    empirical_values = []
    theoretical_values = []

    for i in range(3, args.n + 1):
        if args.ccmean:
            temp = []

            for j in range(args.ccmeansamples):
                graph = generate_graph(args, None, i)
                clustering_coefficient = nx.algorithms.cluster.clustering(graph)
                temp.append(clustering_coefficient)

            clustering_coefficient = np.mean(temp)

        else:
            graph = generate_graph(args, None, i)
            clustering_coefficient = nx.algorithms.cluster.clustering(graph)

        empirical_values.append(clustering_coefficient)

        theoretical_values.append(args.k / (i - 1))

    return empirical_values, theoretical_values


def main_clustering_coefficient(args):
    empirical_values, theoretical_values = compute_clustering_coefficient(args)
    print(empirical_values)
    print(theoretical_values)

    plt.plot(list(range(3, args.n + 1)), empirical_values, label="empirical")
    plt.plot(list(range(3, args.n + 1)),
             theoretical_values,
             label="theoretical")
    plt.legend()
    plt.title(
        'Empirical clustering coefficient against theoretical one -' +
        args.t + ' m =' + str(args.mba))
    plt.show()

    return empirical_values, theoretical_values