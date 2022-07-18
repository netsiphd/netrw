from . import BaseRewirer
import copy
import itertools as it
import random
import networkx as nx


class KarrerRewirer(BaseRewirer):
    """Perturb one edge of node `i` in the way described by Karrer et al. (2008).
    Choose an edge incident on `i` at random; delete it and replace it with
    a new edge that is not already present in the network (and is not
    necessarily incident on `i`).

    Karrer, Brian, Elizaveta Levina, and
    M. E. J. Newman. 2008. “Robustness of Community Structure in
    Networks.” Physical Review E 77
    (4). https://doi.org/10.1103/PhysRevE.77.046119.

    """

    def rewire(self, G, alpha=1, copy_graph=True):
        if copy_graph:
            G = copy.deepcopy(G)

        if random.random() > alpha:
            return G

        i = random.choice(list(G.nodes))

        potential_edges = (
            set(it.product(G.nodes, G.nodes))
            - set(zip(G.nodes, G.nodes))
            - set(G.edges)
        )

        new_edge = random.choice(list(potential_edges))
        old_edge = random.choice(list(G.edges(i)))

        G.remove_edges_from([old_edge])
        G.add_edges_from([new_edge])

        return G
