import networkx as nx
import numpy as np
from netrw.rewire import KarrerRewirer


def test_same_return_type():
    """The graph and the rewired graph should be of the same type (Graph, DiGraph)."""
    G = nx.fast_gnp_random_graph(20, 0.1, directed=True)

    original_degree = [degree for id, degree in G.degree()]

    rewirer = KarrerRewirer()
    avg_degree = np.zeros(G.number_of_nodes())

    iterations = len(G.nodes()) * 100
    for _ in range(iterations):
        new_graph = rewirer.rewire(G, 0.5)
        avg_degree += np.array([degree for node, degree in new_graph.degree()])

    avg_degree /= iterations

    assert np.linalg.norm(original_degree - avg_degree) < 1