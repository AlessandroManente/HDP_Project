import networkx as nx
import matplotlib.pyplot as plt

# Switches for types of random graphs generation
type_graph = {
    'erdos_renyi': nx.gnp_random_graph,
    'barabasi_albert': nx.barabasi_albert_graph,
    'watts_strogatz': nx.watts_strogatz_graph
}


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


def generate_graph(args, d=None):
    '''
    Given arguments parsed from function parsing, it generates a graph of 
    given number of nodes, probability of connection, number of nearest 
    neighbors and tipology.
    '''
    if d is None:
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


def connected_components(graph):
    '''
    Generate a sorted list of connected components of the given graph
    '''
    return [
        len(c)
        for c in sorted(nx.connected_components(graph), key=len, reverse=True)
    ]
