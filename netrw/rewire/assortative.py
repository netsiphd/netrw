from . import BaseRewirer
import copy
import random
import networkx as nx
import numpy as np


class AssortativeRewirer(BaseRewirer):

    """
        Do degree-preserving rewiring that increases/decreases assortativity
        as described in CHANGING CORRELATIONS IN NETWORKS: ASSORTATIVITY AND DISSORTATIVITY,
        R. Xulvi-Brunet and I.M. Sokolov

    """

    def step_rewire(self, G, p=0.5, assortative=True, copy_graph=True):

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

        # initialize nodes for swap
        i, j, k, l = -1, -1, -1, -1

        # loop until all four nodes involved in the swap are distinct
        while len(set([i, j, k, l])) != 4:

            i, j = random.choice(list(G.edges))
            k, l = random.choice(list(G.edges))

            if len(set([i, j, k, l])) == 4:

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

                    # remove previous edge
                    G.remove_edge(i, j)
                    G.remove_edge(k, l)
                    G.add_edge(I, J)
                    G.add_edge(K, L)

                else:
                    i, j, k, l = -1, -1, -1, -1

        return G

    def full_rewire(self, G, p=0.5, assortative=True, copy_graph=True):
        """
        Not implemented
        """
        raise NotImplementedError
