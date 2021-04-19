import networkx as nx
import matplotlib.pyplot as plt
import argparse


# Switches for types of random graphs generation
type_graph = {
    'erdos_renyi': nx.gnp_random_graph,
    'barabasi_albert': nx.barabasi_albert_graph,
    'watts_strogatz': nx.watts_strogatz_graph
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


def print_graph(graph):
    '''
    Simple function to plot a given graph
    '''
    plt.subplot(121)

    nx.draw(graph, with_labels=True, font_weight='bold')
    plt.subplot(122)

    nx.draw_shell(graph,
                  nlist=[range(5, 10), range(5)],
                  with_labels=True,
                  font_weight='bold')

    plt.show()


def generate_graph(args):
    '''
    Given arguments parsed from function parsing, it generates a graph of 
    given number of nodes, probability of connection, number of nearest 
    neighbors and tipology.
    '''
    d = args.d
    n = args.n
    k = args.k
    p = d / n
    tipology = args.t

    if tipology == 'watts_strogatz':
        G = type_graph[tipology](n, k, p)
    else:
        G = type_graph[tipology](n, p)

    return G


if __name__ == "__main__":
    G = generate_graph(parsing())
    print_graph(G)
