import networkx as nx
import numpy as np
from utils.basic_graphs_utilities import *
from os import path


def compute_distribution_average_path_length(args, tipology=None):
    '''
    Compute the average path length for the given type of graph varying the number of nodes. 
    It is only available for BA and WS, because ER does not have a theoretical expression
    for that value.
    It also computes the theoretical value, making it possible to compare the empirical results 
    with the theory.
    '''
    empirical_values = []
    theoretical_values = []

    h = args.k + 1

    for i in range(h, args.n + 1):
        if args.aplmean:
            temp = []

            for j in range(args.aplmeansamples):
                graph = generate_graph(args, None, i, tipology)
                avg_path_length = nx.average_shortest_path_length(graph)
                temp.append(avg_path_length)

            avg_path_length = np.mean(temp)

        else:
            graph = generate_graph(args, None, i, tipology)
            avg_path_length = nx.average_shortest_path_length(graph)

        empirical_values.append(avg_path_length)

        if tipology == 'barabasi_albert':
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


def compute_distribution_average_path_length_varying_pws(args, tipology=None):
    empirical_values = []

    for i in [1 - 1 / i for i in range(1, 21)]:
        if args.aplmean:
            temp = []

            for j in range(args.aplmeansamples):
                graph = generate_graph(args, None, None, tipology, i)
                avg_path_length = nx.average_shortest_path_length(graph)
                temp.append(avg_path_length)

            avg_path_length = np.mean(temp)

        empirical_values.append(avg_path_length)

    return empirical_values


def main_average_path_length(args, tipology=None):
    '''
    Main function that calls subroutines and plot and save the results
    '''
    empirical_values, theoretical_values = compute_distribution_average_path_length(
        args, tipology)

    h = args.k + 1

    plt.figure()
    plt.plot(list(range(h, args.n + 1)), empirical_values, label="empirical")
    plt.plot(list(range(h, args.n + 1)),
             theoretical_values,
             label="theoretical")
    plt.legend()
    plt.title(
        'Empirical average shortest path length against theoretical one -' +
        tipology + ' m =' + str(args.mba))

    if tipology == 'watts_strogatz':
        plt.savefig(
            path.join(
                'results', str(args.n), tipology,
                'pla_fixed_{}_{}_{}.png'.format(tipology, args.k, args.pws)))

    plt.savefig(
        path.join('results', str(args.n), tipology,
                  'pla_fixed_{}.png'.format(tipology)))
    # plt.show()

    # if required, shows the behaviour varying parameter pws instead of the number of nodes
    if args.aplwsvaryingbeta and tipology == 'watts_strogatz':
        values_var = compute_distribution_average_path_length_varying_pws(
            args, tipology)

        plt.figure()
        plt.plot([1 - 1 / i for i in range(1, 21)],
                 values_var,
                 label="empirical")
        plt.plot([1 - 1 / i for i in range(1, 21)],
                 [np.log(args.n) / np.log(args.k) for i in range(20)],
                 label="theoretical beta->0")
        plt.plot([1 - 1 / i for i in range(1, 21)],
                 [args.n / (2 * args.k) for i in range(20)],
                 label="theoretical beta->1")
        plt.legend()
        plt.title(
            'Empirical average shortest path length against theoretical one -'
            + tipology + ' m =' + str(args.mba))
        plt.savefig(
            path.join('results', str(args.n), tipology,
                      'pla_varyingbeta_{}.png'.format(tipology)))
        # plt.show()

    return empirical_values, theoretical_values
