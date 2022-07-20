import copy
import itertools as it
import random

import networkx as nx
import numpy as np

from .base import BaseRewirer


class RandomizedWeightCM_swap(BaseRewirer):
    """
    Swap weights of a weighted network without rewiring edges.

    - rewire_step: Swap weights bewteen two randomly chosen edges
    - rewire: Over the list of edges, permutate the list of associated weigths

    4th method is from Ghavasieh, A.; De Domenico, M.
    "Multiscale Information Propagation in Emergent Functional Networks".
    Entropy 2021, 23, 1369. https://doi.org/10.3390/e23101369
    """

    def edge_pair_random_choice(self, G):
        e_list = list(G.edges(data=True))
        e_1 = random.choice(e_list)
        e_list.remove(e_1)
        e_2 = random.choice(e_list)

        return e_1, e_2

    def step_rewire(self, G, copy_graph=True):
        if copy_graph:
            G = copy.deepcopy(G)

        e_1, e_2 = self.edge_pair_random_choice(G)

        w_1 = e_1[2]["weight"]
        w_2 = e_2[2]["weight"]

        G.edges[e_1[0], e_1[1]]["weight"] = w_2
        G.edges[e_2[0], e_2[1]]["weight"] = w_1

        return G

    def full_rewire(self, G, copy_graph=True):
        if copy_graph:
            G = copy.deepcopy(G)

        e_list = list(G.edges())
        w_list = [x[2]["weight"] for x in list(G.edges(data=True))]

        w_list = np.random.permutation(w_list)
        nx.set_edge_attributes(G, dict(zip(e_list, w_list)), "weight")

        return G


class RandomizedWeightCM_redistribution(BaseRewirer):
    """
    Redistribute weights of a weighted network without rewiring edges.

    - rewire_step: the total sum of weight of a randomly chosen pair of links is randomly re-distributed over this two links
    - rewire: The total sum of weights of all links in the netwrok is randomly distributed over the links
    """

    def step_rewire(self, G, copy_graph=True):
        if copy_graph:
            G = copy.deepcopy(G)

        e_1, e_2 = self.edge_pair_random_choice(G)

        a_1 = random.random()

        w_sum = e_1[2]["weight"] + e_2[2]["weight"]

        G.edges[e_1[0], e_1[1]]["weight"] = a_1 * w_sum
        G.edges[e_2[0], e_2[1]]["weight"] = (1 - a_1) * w_sum

        return G

    def full_rewire(self, G, copy_graph=True):
        if copy_graph:
            G = copy.deepcopy(G)

        alphas = np.random.rand(len(G.edges()))
        alphas = alphas / np.sum(alphas)

        w = [x[2]["weight"] for x in list(G.edges(data=True))]
        w_sum = np.sum(w)
        aw = alphas * w_sum

        e_list = list(G.edges())
        nx.set_edge_attributes(G, dict(zip(e_list, aw)), "weight")

        return G
