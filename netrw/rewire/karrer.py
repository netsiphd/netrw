import copy

import networkx as nx
import numpy as np

from . import BaseRewirer


class KarrerRewirer(BaseRewirer):
    """Perturb the graph in the way described by Karrer et al. (2008).
    For each edge, with probability alpha delete it and replace it with
    a new edge connecting nodes i and j following the probabilities of
    the configuration model.

    Note that the method may produce graphs with self-loops and multi-edges.

    Karrer, Brian, Elizaveta Levina, and
    M. E. J. Newman. 2008. “Robustness of Community Structure in
    Networks.” Physical Review E 77
    (4). https://doi.org/10.1103/PhysRevE.77.046119.

    """

    def rewire(self, G, alpha=1, copy_graph=True):
        if copy_graph:
            G = copy.deepcopy(G)

        # If probability is equal to 0, do nothing
        if alpha == 0:
            return G

        # Auxiliary list for edge probabilities
        nodes_repeated = [[id] * degree for id, degree in G.degree()]
        nodes_repeated = [elem for elems in nodes_repeated for elem in elems]

        # Random selection of edges to preserve
        current_edges = list(G.edges())
        random_numbers = np.random.uniform(0, 1, len(current_edges))
        selected_edges = [
            current_edges[i]
            for i in range(len(current_edges))
            if random_numbers[i] < (1 - alpha)
        ]

        # Creation of new edges
        n_new_edges = len(current_edges) - len(selected_edges)
        np.random.shuffle(nodes_repeated)
        left_nodes, right_nodes = (
            nodes_repeated[n_new_edges:],
            nodes_repeated[:n_new_edges],
        )
        new_edges = [(x, y) for x, y in zip(left_nodes, right_nodes)]

        # Create new graph, note that it may have self-loops and multi-edges
        new_graph = nx.MultiGraph()
        new_graph.add_nodes_from(G.nodes())
        new_graph.add_edges_from(selected_edges + new_edges)
        return new_graph
