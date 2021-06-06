import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# Switches for types of random graphs generation
type_graph = {
    'erdos_renyi': nx.gnp_random_graph,
    'barabasi_albert': nx.barabasi_albert_graph,
    'watts_strogatz': nx.connected_watts_strogatz_graph
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

    # plt.show()


def generate_graph(args, d=None, n=None, tipology=None, p=None, mba=None, k=None):
    '''
    Given arguments parsed from function parsing, it generates a graph of 
    given number of nodes, probability of connection, number of nearest 
    neighbors and tipology.
    '''
    if d is None:
        d = args.d
    if n is None:
        n = args.n
    if mba is None:
        mba = args.mba
    if tipology is None:
        tipology = args.t

    if tipology == 'erdos_renyi':
        p = d / n
        G = type_graph[tipology](n, p)

    elif tipology == 'watts_strogatz':
        if k is None:
            k = args.k
        if p is None:
            p = args.pws

        G = type_graph[tipology](n, k, p)
    else:
        G = type_graph[tipology](n, mba)

    return G


def connected_components(graph):
    '''
    Generate a sorted list of connected components of the given graph
    '''
    return [
        len(c)
        for c in sorted(nx.connected_components(graph), key=len, reverse=True)
    ]

def generate_barabasi_albert(n, m,save_steps=False):
    """
    Generates a random network using the model proposed by Barabasi and Albert and  redefined later by Bollobas, Riordan et al. (2001) by extending to multigraphs and specifying the initialization and updating steps.
    It starts from a single node with m self loops attached to it (it's a multigraph).
    It adds one single node at a time with m edges attached to it, and attaches the other ends to existing nodes in the graph with probability proportional to their degree. Note that the edges are added sequentially, one at a time, with intermediate updating of the nodes degrees.
    Parameters:
    
    n : number of time steps to complete the model;
    m : number of edges to add for each new node;
    save_steps : wether to return the history of all the created graphs """

    if m < 1 or m >= n:
        raise nx.NetworkXError(
            f"Barabási–Albert network must have m >= 1 and m < n, m = {m}, n = {n}"
        )

    G = nx.MultiGraph()
    nodes_list = list(range(n))
    G.add_node(0)
    intermediate_graphs=[]

    # init graph with one node with m self loops
    for i in range(m):
        G.add_edge(0,0)

    for t in range(1,n):
        G.add_node(t)
        for edge in range(m):
            ## Define the probability distribution with which we pick the nodes
            xk = list(G.nodes)

            if edge == 0:
                # convention that D_(t+1)(0,t) =  1
                # i.e. before attaching any edges to the new node, we pretend
                # that it has degree = 1 (check Hofstadt book page 174)
                # TODO: if we use this convention, defining prepk like this:

                #  prepk = [G.degree[i] for i in G.nodes][:-1] + [1]

                #  there is the possibility to get a disconnected graph!!
                # is it normal/accepted by barabasi?
                prepk = [G.degree[i] for i in G.nodes][:-1] + [0]
                pk = prepk/np.sum(prepk)
            else:
                prepk = [G.degree[i] for i in G.nodes]
                pk = prepk/np.sum(prepk)

            custom_dist = stats.rv_discrete(name="degree_distribution", values=(xk,pk))
            extracted = custom_dist.rvs(size=1)[0]
            G.add_edge(t, extracted)

        if save_steps:
            intermediate_graphs.append(G.copy())
    return G, intermediate_graphs

def ba_model_A(n,m, save_steps=False):
    """
    Limiting case for the BA Model, used to prove that both 
    growth and preferential attachment are necessary to obtain the scale-free distribution.
    This model keeps the growing character of the network without preferential attachment.
    """
    if m < 1 or m >= n:
        raise nx.NetworkXError(
            f"Barabási–Albert network must have m >= 1 and m < n, m = {m}, n = {n}"
        )

    G = nx.MultiGraph()
    G.add_node(0)
    intermediate_graphs=[]

    # init graph with one node with m self loops
    for i in range(m):
        G.add_edge(0,0)

    for t in range(1,n):
        G.add_node(t)
        extracted = np.random.choice(list(G.nodes)[:-1], m)
        G.add_edges_from([(t,chosen) for chosen in extracted])

        if save_steps:
            intermediate_graphs.append(G.copy())

    return G, intermediate_graphs

def ba_model_B(n,t, save_steps=False):
    """
    Limiting case for the BA Model, used to prove that both 
    growth and preferential attachment are necessary to obtain the scale-free distribution.
    This model starts with n nodes and no edges, and adds one at a time with preferential attachment.
    Parameters:
    - n: number of nodes to start with;
    - t: total number of timesteps to perform
    """

    G = nx.MultiGraph()
    nodes_list = list(range(n))
    G.add_nodes_from(nodes_list)

    # NB: this is a custom initialization.
    # Barabasi-Albert don't specify
    # how to initialize the first edges. i add a self loop for each node.
    for i in range(n):
        G.add_edge(i,i)
    intermediate_graphs=[]

    for t in range(1,t):
        ## Define the probability distribution with which we pick the nodes
        xk = list(G.nodes)

        prepk = [G.degree[i] for i in G.nodes]
        pk = prepk/np.sum(prepk)

        custom_dist = stats.rv_discrete(name="degree_distribution", values=(xk,pk))
        extracted = custom_dist.rvs(size=1)[0]
        G.add_edge(np.random.choice(nodes_list), extracted)

        if save_steps:
            intermediate_graphs.append(G.copy())
    return G, intermediate_graphs


def analytical_path_length(x):
    a = np.sqrt(x**2 + 2 * x)
    b = 1 / a
    c = np.arctanh(x * b)
    return b * 0.5 * c