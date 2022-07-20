from copy import deepcopy
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import netrw
from netrw.rewire import KarrerRewirer, AlgebraicConnectivity, NetworkXEdgeSwap


def various_properties_overtime(
    init_graph, rewire_method, property_functions, function_names, tmax, numit
):
    """
    Analyze the property values of a network as a function of rewire steps.
    Looks at how a network property changes as a rewiring process occurs.

    Parameters
    ----------
    init_graph : NetworkX graph
        Initial graph upon which rewiring will occur.
    rewire_method : netrw rewire class object
        Algorithm for rewiring a network with step_rewire option
    property_functions : list of functions with input being NetworkX graphs
    function_names : list of strings describing the functions
        Network description property that outputs a single value for a given network. Should work with any function that
        summarizes a NetworkX graph object into a single value. For example, nx.average_clustering, nx.average_shortest_path_length, etc.
    tmax : int
        Number of rewiring steps to perform for each iteration.
    numit : int
        Number of rewiring iterations to perform on the initial graph. The given rewiring process will be performed numit
        times on the initial graph to look at the distribution of outcomes for this rewiring process on the initial graph.
    Returns
    -------
    property_dict: dictionary
        Dictionary of output where the keys are the iteration number and the values are a list of the network property calculated
        at each step of the rewiring process.
    """

    all_properties = {}

    rw = rewire_method()

    for name in function_names:

        all_properties[name] = np.zeros((numit, tmax))

    # loop over rewiring instances
    for i in range(numit):

        G0 = deepcopy(init_graph)

        # calculate properties of initial network
        for func, name in zip(property_functions, function_names):

            all_properties[name][i, 0] = func(G0)

        # loop over timesteps
        for j in range(1, tmax):

            G0 = rw.step_rewire(G0, copy_graph=False)  # rewire

            # calculate properties of the rewired network

            for name, func in zip(function_names, property_functions):

                all_properties[name][i, j] = func(G0)

        return all_properties


def calculate_statistics(all_properties):
    """
    Find the mean, standard deviation, mean-std, and mean+std of the data from rewirings

    Inputs:
        all_properties: dict of 2D np.arrays of shape numit x tmax with keys that are property names

    Outputs:
        all_means: dict of mean values of each property at each timestep (keys are property names, values are 1D np.arrays of length tmax)
        all_stds: likewise for standard deviations
        all_lowers: likewise for mean-std
        all_uppers: likewise for mean+std

    """

    # find mean and standard deviation over different iterations of rewiring process
    all_means = {}
    all_stds = {}
    all_lowers = {}
    all_uppers = {}

    for name, data in all_properties.items():

        all_means[name] = np.mean(data, axis=0)
        all_stds[name] = np.std(data, axis=0)
        all_lowers[name] = all_means[name] - all_stds[name]
        all_uppers[name] = all_means[name] + all_stds[name]

    return all_means, all_stds, all_lowers, all_uppers


def average_local_clustering(G):
    """
    Calculates average local clustering of networkx graph G

    Note: divides by the number of nodes with degree at least 2,
    since local clustering is undefined for nodes with degree less than 2.

    """
    # get degrees and find how many nodes have degree at least 2
    k = np.array(list(dict(nx.degree(G)).values()))
    n_kg1 = np.sum(k > 1)

    # find and sum up local clustering coefficient of all nodes
    clu = nx.clustering(G)
    tot = np.sum(list(nx.clustering(G).values()))

    # calculate average
    barc = tot / n_kg1
    return barc


def average_shortest_path_length(G):
    """
    Calculates average shortest path length of networkx graph G

    Note: divides by total number of shortest paths, namely the sum over components
     of component-size-choose-2, so as to still get a meaningful result when
     the graph is not connected.
    """
    # find the sizes of connected components
    C = list(nx.connected_components(G))
    Nv = list(map(len, C))

    # calculate the total number of shortest paths
    Npairs = np.sum([N * (N - 1) / 2 for N in Nv])

    # sum up all shortest path lengths
    total = np.sum(
        [np.sum(list(v[1].values())) for v in nx.all_pairs_shortest_path_length(G)]
    )

    # calculate average
    barl = total / Npairs
    return barl


property_functions = [
    lambda G: G.number_of_nodes(),
    lambda G: G.number_of_edges(),
    lambda G: average_shortest_path_length(G),
    lambda G: nx.number_connected_components(G),
    lambda G: nx.assortativity.degree_assortativity_coefficient(G),
    lambda G: np.sum(np.array(list(dict(nx.degree(G)).values())) ** 2)
    / G.number_of_nodes(),
    lambda G: np.min(np.array(list(dict(nx.degree(G)).values()))),
    lambda G: np.max(np.array(list(dict(nx.degree(G)).values()))),
    lambda G: average_local_clustering(G),
]

function_names = [
    "Number of nodes",
    "Number of edges",
    "Average shortest path length",
    "Number of components",
    "Degree correlation coefficient",
    "Second moment of degree distribution",
    "Minimum degree",
    "Maximum degree",
    "Average local clustering coefficient",
]


# test run
init_graph = nx.fast_gnp_random_graph(100, 0.03)
rewire_method = NetworkXEdgeSwap
tmax = 100
numit = 10
all_properties = various_properties_overtime(
    init_graph, rewire_method, property_functions, function_names, tmax, numit
)


# test plot
for name in function_names:
    fi, ax = plt.subplots(1, figsize=(5, 2), dpi=200)
    plt.plot(range(tmax), np.mean(all_properties[name], axis=0))
    plt.title(name)
    plt.xlabel("$t$")
    plt.tight_layout()
    plt.savefig("figures/" + name)
