#!/usr/bin/env python
# coding: utf-8

from .base import BaseRewirer
import networkx as nx
import numpy as np
import copy
from operator import itemgetter
import random


class RobustRewiring(BaseRewirer):
    """
    Increases network robustness by building triangles around high degree nodes following algorithm described in:
    Louzada, V. H. P., Daolio, F., Herrmann, H. J., & Tomassini, M. (2013). Smart rewiring for network robustness. Journal of Complex Networks, 1(2), 150–159. https://doi.org/10.1093/comnet/cnt010
    """

    def robust_rewire(self, G, copy_graph=False, num_steps=100):

        if copy_graph:
            G = copy.deepcopy(G)

        for t in range(num_steps):
            A = nx.adjacency_matrix(G)
            degree_list = G.degree

            neighbors = []
            for i in range(len(degree_list)):
                sorted_degrees = sorted(
                    list(degree_list(np.nonzero(A[i, :])[1])), key=itemgetter(1)
                )
                if len(sorted_degrees) > 1:
                    if sorted_degrees[-2][1] > 1 and sorted_degrees[-1][1] > 1:
                        neighbors.append(i)

            index_i = neighbors[random.randint(0, len(neighbors) - 1)]
            sorted_degrees_i = sorted(
                list(degree_list(np.nonzero(A[index_i, :])[1])), key=itemgetter(1)
            )

            min_degree = sorted_degrees_i[0][1]
            max_degree = sorted_degrees_i[-1][1]

            j = []
            k = []

            for item in sorted_degrees_i:
                if item[1] == min_degree:
                    j.append(item[0])
                if item[1] == max_degree:
                    k.append(item[0])

            index_j = j[random.randint(0, len(j) - 1)]
            index_k = k[random.randint(0, len(k) - 1)]

            m = sorted(
                list(degree_list(np.nonzero(A[index_j, :])[1])), key=itemgetter(1)
            )
            n = sorted(
                list(degree_list(np.nonzero(A[index_k, :])[1])), key=itemgetter(1)
            )

            index_m = m[random.randint(0, len(m) - 1)][0]
            index_n = n[random.randint(0, len(n) - 1)][0]

            if len(np.unique([index_i, index_j, index_k, index_m, index_n])) == 5:
                G.remove_edge(index_j, index_m)
                G.remove_edge(index_k, index_n)
                G.add_edge(index_k, index_j)
                G.add_edge(index_m, index_n)
                print("HI")

        return G
