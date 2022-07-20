from .base import BaseRewirer
import networkx as nx
import numpy as np
import copy
from scipy import linalg as la
import warnings


class AssortativityLocalMaximum(BaseRewirer):
    """
    Check all possible pairs of links for valid rewirings
    Make a rewiring if the rewiring increases assortativity
    Repeat until no rewirings increase assortativity

    Shi Zhou and Ra ́ul J Mondrag ́on. Structural constraints in complex networks. New Journal of
    Physics, 9(6):173, 2007.
    """

    def assortativity(self, G):
        if isinstance(G, nx.classes.digraph.DiGraph):
            return nx.degree_pearson_correlation_coefficient(G, x="out", y="in")

        return nx.degree_pearson_correlation_coefficient(G)

    def compare_assortativity(self, G, e1, e2, e1_new, e2_new, max_assort):
        if (
            e1_new[0] == e1_new[1]
            or e2_new[0] == e2_new[1]
            or e1_new[0] == e2_new[0]
            or e1_new[1] == e2_new[1]
            or G.has_edge(e1_new[0], e1_new[1])
            or G.has_edge(e2_new[0], e2_new[1])
        ):
            return None

        G.remove_edge(e1[0], e1[1])
        G.remove_edge(e2[0], e2[1])
        G.add_edge(e1_new[0], e1_new[1])
        G.add_edge(e2_new[0], e2_new[1])
        cur_assort = self.assortativity(G)

        if cur_assort > max_assort:
            return cur_assort

        # replace the swapped edges if assortativity does not increase
        else:
            G.remove_edge(e1_new[0], e1_new[1])
            G.remove_edge(e2_new[0], e2_new[1])
            G.add_edge(e1[0], e1[1])
            G.add_edge(e2[0], e2[1])
            return None

    def full_rewire(self, G, timesteps=np.inf, copy_graph=True, verbose=False):
        """
        Rewire network to maximize algebraic connectivity. In Sydney et al. paper,
        they find that rewiring 30% of the edges is sufficient.
        """

        if not isinstance(G, nx.classes.digraph.DiGraph) and not isinstance(
            G, nx.classes.graph.Graph
        ):
            raise ValueError(
                "Only nx.Graphs and nx.DiGraphs are allowed for this method"
            )

        if copy_graph:
            G = copy.deepcopy(G)

        possible_edges = []
        node_list = list(G.nodes)
        original_edges = list(G.edges)
        removed_edges = {}
        added_edges = {}

        max_assort = self.assortativity(G)

        # loop through all combinations of two edges
        i = 0
        time = -1
        while i < len(G.edges):
            for j in range(len(G.edges)):
                time += 1
                if time >= timesteps:
                    if verbose:
                        return G, removed_edges, added_edges
                    return G

                edge_list = list(G.edges)
                if i == j:
                    continue
                e1 = edge_list[i]
                e2 = edge_list[j]

                # try edge swaps until we find one where assortativity increases (decreases)
                # switch sources
                e1_new = (e2[0], e1[1])
                e2_new = (e1[0], e2[1])
                new_assort = self.compare_assortativity(
                    G, e1, e2, e1_new, e2_new, max_assort
                )
                if new_assort is not None:
                    max_assort = new_assort
                    i = 0
                    removed_edges[time] = [e1, e2]
                    added_edges[time] = [e1_new, e2_new]
                    break

                # switch targets
                e1_new = (e1[0], e2[1])
                e2_new = (e2[0], e1[1])
                new_assort = self.compare_assortativity(
                    G, e1, e2, e1_new, e2_new, max_assort
                )
                if new_assort is not None:
                    max_assort = new_assort
                    i = 0
                    removed_edges[time] = [e1, e2]
                    added_edges[time] = [e1_new, e2_new]
                    break

                # ss, tt
                if isinstance(G, nx.classes.graph.Graph):
                    e1_new = (e1[0], e2[0])
                    e2_new = (e1[1], e2[1])
                    new_assort = self.compare_assortativity(
                        G, e1, e2, e1_new, e2_new, max_assort
                    )
                    if new_assort is not None:
                        max_assort = new_assort
                        i = 0
                        removed_edges[time] = [e1, e2]
                        added_edges[time] = [e1_new, e2_new]
                        break

                # make the swap and repeat

            i += 1
            # exit once no edge swap can increase assortativity

        if verbose:
            return G, removed_edges, added_edges
        return G

    def step_rewire(
        self, G, timesteps=1, copy_graph=False, directed=True, verbose=False
    ):
        """
        Rewire ``timesteps`` edges to maximize algebraic connectivity.

        Parameters:
            G (networkx)
            timesteps (int) - number of edge rewires
            copy_graph (bool) - return a copy of the network
            directed (bool) - compute for directed network on undirected copy
            verbose (bool) - indicator to return edges changed at each timestep

        Return:
            G (networkx)
        """
        return self.full_rewire(G, timesteps, copy_graph, directed, verbose)
