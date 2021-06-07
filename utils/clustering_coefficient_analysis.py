import networkx as nx
import numpy as np
from utils.basic_graphs_utilities import *
from os import path
import sys
plt.style.use("ggplot")


def compute_clustering_coefficient(args, tipology=None, n=None, k=None):
    '''
    Computes the clustering coefficient given the parameters obtained by the parsing. If required, it can compute a mean
    of the clustering coefficients, so as to limit the effects of the variance in the random process
    '''
    empirical_values = []
    theoretical_values = []

    for i in [i / 1000 for i in range(1001)]:
        if args.ccmean:
            temp = []

            for j in range(args.cmeansamples):
                graph = generate_graph(args, None, n, tipology, i, None, k)
                clustering_coefficient = np.mean(
                    list(nx.algorithms.cluster.clustering(graph).values()))
                temp.append(clustering_coefficient)

            clustering_coefficient = np.mean(temp)

        else:
            graph = generate_graph(args, None, n, tipology, i, None, k)
            clustering_coefficient = np.mean(
                list(nx.algorithms.cluster.clustering(graph).values()))

        empirical_values.append(clustering_coefficient)

        theoretical_values.append(3 / 4 * (args.k - 2) / (args.k - 1) *
                                  (1 - i)**3)

    return empirical_values, theoretical_values


def main_clustering_coefficient(args, tipology):
    '''
    Main function that calls subroutines and plot and save the results
    '''
    theor = []
    empir = []
    combinations = []
    for n in [1000, 2000, 5000]:
        for k in [50, 75, 100]:
            empirical_values, theoretical_values = compute_clustering_coefficient(
                args, tipology, n, k)

            plt.plot([i / 1000 for i in range(1001)],
                     empirical_values,
                     label="empirical")
            plt.plot([i / 1000 for i in range(1001)],
                     theoretical_values,
                     label="theoretical")
            plt.legend()
            plt.title(
                'Empirical clustering coefficient against theoretical one - Watts-Strogatz - n='
                + str(n) + ' - k=' + str(k))
            plt.xscale('log')
            plt.savefig(
                path.join('results', 'cca_{}_{}_{}.png'.format(n, k,
                                                               tipology)))
            # plt.show()

            theor.append(theoretical_values)
            empir.append(empirical_values)
            combinations.append([n, k])

            print('done with ' + str(n) + ' ' + str(k))

    for i, el in enumerate(empir):
        plt.plot([i / 1000 for i in range(1001)],
                 el,
                 label="empirical_" + str(combinations[i][0]) + '_' +
                 str(combinations[i][1]))
        plt.plot([i / 1000 for i in range(1001)],
                 theor[i],
                 label="theoretical_" + str(combinations[i][0]) + '_' +
                 str(combinations[i][1]))

    plt.legend()
    plt.title(
        'Empirical clustering coefficient against theoretical one - Watts-Strogatz'
    )
    plt.xscale('log')
    plt.savefig(path.join('results', 'cca', 'cca_{}.png'.format(tipology)))

    return empir, theor