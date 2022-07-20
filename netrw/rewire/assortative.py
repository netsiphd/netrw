from . import BaseRewirer
import copy
import random
import networkx as nx
import numpy as np


class DegreeAssortativeRewirer(BaseRewirer):

    """
        Do degree-preserving rewiring that increases/decreases assortativity
        as described in CHANGING CORRELATIONS IN NETWORKS: ASSORTATIVITY AND DISSORTATIVITY,
        R. Xulvi-Brunet and I.M. Sokolov

    """

    def step_rewire(self, G, p=0.5, assortative=True, copy_graph=True, verbose=False):

        """
        Inputs:
            p (float) -- the probability of making the swap be in favor of
                            increasing/decreasing assortativity. Otherwise,
                            the swap is of the form (i,j),(k,l)-->(i,l),(j,k).

            assortative (bool) -- if assortative==True, the non-random swaps
                                    favor increasing assortativity. Otherwise,
                                    they favor increasing disassortativity.
        """

        if copy_graph:
            G = copy.deepcopy(G)

        (i, j), (k, l) = random.sample(list(G.edges), 2)

        # repeat until a valid rewiring is found
        valid = False
        while not valid:

            if np.random.rand() <= p:

                # degree-sorting for edge-swap with probability p
                sor = sorted([i, j, k, l], key=lambda y: G.degree[y])

                if assortative:
                    I, J, K, L = sor
                else:
                    I, J, K, L = sor[0], sor[3], sor[1], sor[2]

            else:

                # standard edge-swap with probability 1-p
                I, J, K, L = i, l, j, k

            # make sure new edges aren't already there
            if (not G.has_edge(I, J)) and (not G.has_edge(K, L)):
                valid = True

                # remove previous edge
                G.remove_edge(i, j)
                G.remove_edge(k, l)
                G.add_edge(I, J)
                G.add_edge(K, L)

            if verbose:
                removed_edges = [(i, j), (k, l)]
                added_edges = [(I, J), (K, L)]

        if verbose:
            return G, removed_edges, added_edges
        else:
            return G

    def full_rewire(self, G, timesteps=1000, p=0.5, assortative=True, copy_graph=True):
        """
        Runs step_rewire for a number of steps (default 1000 for no reason)
        """
        for t in range(timesteps):
            G = self.step_rewire(G, p=p, assortative=assortative, copy_graph=copy_graph)

        return G
