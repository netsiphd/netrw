from .base import BaseRewirer

import copy
import warnings

import numpy as np

import networkx as nx
from networkx.algorithms import bipartite

import random as rand


class RewireBipartite(BaseRewirer):
    """

    The algorithm keep the bipartite structure, randomply choose the edges and swap them.
    It stops according to an analitically foung max iter which allow to reach a wanded accuracy,
    defined with the Jaccard Distance between network.

    Ref: Andrea Gobbi, Francesco Iorio, Kevin J. Dawson, David C. Wedge, David Tamborero, Ludmil B. Alexandrov, Nuria Lopez-Bigas, Mathew J. Garnett, Giuseppe Jurman, Julio Saez-Rodriguez, Fast randomization of large genomic datasets while preserving alteration counts, Bioinformatics, Volume 30, Issue 17, 1 September 2014, Pages i617–i623, https://doi.org/10.1093/bioinformatics/btu474

    """

    def rewire(self, G):
        return G

    # Flag that checks if the program performed a single step rewire
    step_rewire_flag = False
    bipartite_flag = True

    def max_iter(self, e, t, accuracy):
        return int(np.ceil((e * (1 - e / t)) * np.log((1 - e / t) / accuracy) / 2.0))

    # Single step: Stochastic
    # This method may return the same graph
    def step_rewire(self, G, verbose = False):
        self.step_rewire_flag = False
        
        #check if still bipartite 
        if bipartite.is_bipartite(G) == False:

            if verbose == True:
                warnings.warn(
                    "This algorithm is designed for bipartite graphs.",
                    SyntaxWarning,
                )

            self.bipartite_flag = False

            return G

        edges = list(G.edges())
        e = len(edges)

        rand1 = rand.randint(0, e - 1)

        while True:
            rand2 = rand.randint(0, e - 1)

            if rand1 != rand2:
                break

        a = edges[rand1][0]
        c = edges[rand2][0]
        b = edges[rand1][1]
        d = edges[rand2][1]

        if (
            a != c
            and d != b
            and G.has_edge(a, d) == False
            and G.has_edge(c, b) == False
        ):
            G.remove_edge(a, b)
            G.remove_edge(c, d)

            G.add_edge(a, d)
            G.add_edge(c, b)

            self.step_rewire_flag = True

        return G

    def full_rewire(self, G, accuracy, timesteps=0, copy_graph=False, verbose=False):
        # Test if the input is a bipartite graph
        if bipartite.is_bipartite(G) == False:

            if verbose == True:
                warnings.warn(
                    "This algorithm is designed for bipartite graphs.",
                    SyntaxWarning,
                )

            self.bipartite_flag = False

            return G

        # Copy the graph
        if copy_graph == True:
            G = copy.deepcopy(G)

        # set the max_iter variable
        edges = list(G.edges())
        e = len(edges)

        X, Y = bipartite.sets(G)
        nc = len(X)
        nr = len(Y)
        t = nc * nr

        if timesteps == 0:
            N = self.max_iter(e, t, accuracy)

        else:
            N = timesteps

            if verbose == True:
                warnings.warn(
                    "Warning: timesteps can different from the theoretical bound.",
                    SyntaxWarning,
                )

        for n in range(N):
            G = self.step_rewire(G)

            # Guarantees that n is the number of succesfull rewirings
            if self.step_rewire_flag == False:
                n = n - 1

        return G
