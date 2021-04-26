import networkx as nx
import numpy as np
from utils.basic_graphs_utilities import *


def compute_distribution_average_path_length(args):
    empirical_values = []
    theoretical_values = []

    h = args.k + 1

    for i in range(h, args.n + 1):
        if args.aplmean:
            temp = []

            for j in range(args.aplmeansamples):
                graph = generate_graph(args, None, i)
                avg_path_length = nx.average_shortest_path_length(graph)
                temp.append(avg_path_length)

            avg_path_length = np.mean(temp)

        else:
            graph = generate_graph(args, None, i)
            avg_path_length = nx.average_shortest_path_length(graph)

        empirical_values.append(avg_path_length)

        if args.t == 'barabasi_albert':
            if args.mba:
                theoretical_values.append(np.log(i))
            else:
                theoretical_values.append(np.log(i) / np.log(np.log(i)))

        else:
            if args.pws > 0.5:
                theoretical_values.append(np.log(i) / np.log(args.k))
            else:
                theoretical_values.append(i / (2 * args.k))

    return empirical_values, theoretical_values


def main_average_path_length(args):
    empirical_values, theoretical_values = compute_distribution_average_path_length(
        args)

    h = args.k + 1

    plt.plot(list(range(h, args.n + 1)), empirical_values, label="empirical")
    plt.plot(list(range(h, args.n + 1)),
             theoretical_values,
             label="theoretical")
    plt.legend()
    plt.title(
        'Empirical average shortest path length against theoretical one -' +
        args.t + ' m =' + str(args.mba))
    plt.show()

    return empirical_values, theoretical_values
