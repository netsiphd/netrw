from .base import BaseRewirer
import itertools as it
import networkx as nx
import numpy as np
import numpy.linalg as nl
import copy
import random

class SpectralRadius(BaseRewirer):
    """
    Rewire a network for increase by a specific parameter of the
    spectral radius of a network. It does this by specifying the required
    improvement for the largest eigenvalue and keeping incremental
    improvements while removing rewires that decrease spectral radius.
    For a large network where increasing robustness is required but
    optimization is time and memory intensive, this may be preferred.
    """

    def full_rewire(
            self, G, alpha=0.05, maxiter=1000, verbose=False, copy_graph=True
    ):
        """
        Rewire network to improve spectral radius.
        Parameters:
            G (networkx)
            alpha (float) - amount of desired increase in the largest eigenvalue
            maxiter (int) - maximum number of rewiring iterations
            verbose (bool) - indicator to return edges changed at each timestep
            copy_graph (bool) - return a copy of the network
        Return:
            G (networkx)
        Verbose Return:
            G (networkx)
            added_edges (dict) - dictionary (timestep, edge) of edges added during rewiring
            removed_edges (dict) - dictionary (timestep, edge) of edges removed during rewiring
        """

        # find the max eigval
        adj_mat = nx.to_numpy_array(G)
        evl = nl.eigvals(adj_mat)
        baseline_max = max(evl)
        init_max = baseline_max
        criteria = baseline_max + alpha
        temp_max = 0
        timestep = 0

        # create arrays for add/remove edges
        added_edges = {}
        removed_edges = {}

        # while loop to attempt improvements
        while temp_max < criteria and timestep <= maxiter:

            # run step_rewire
            G, added_edge, removed_edge, temp_max, delta = self.step_rewire(G, baseline_max, verbose=True)
            if baseline_max + delta > baseline_max:
                baseline_max += delta
                if verbose:
                    added_edges[timestep] = added_edge
                    removed_edges[timestep] = removed_edge
            else:
                if verbose:
                    added_edges[timestep] = []
                    removed_edges[timestep] = []

        improvement = temp_max - init_max
        if verbose:
            return G, added_edges, removed_edges, improvement
        else:
            return G

    def step_rewire(
            self, G, baseline_max=-1, verbose=False, copy_graph=False
    ):
        """
        Rewire edges to improve the spectral radius (increase the value of the largest
        eigenvalue to improve robustness of the network).
        Parameters:
            G (networkx)
            baseline_max (float) - largest eigenvalue of the network before rewire step
            verbose (bool) - indicator to return edges changed at each timestep
            copy_graph (bool) - return a copy of the network
        Return:
            G (networkx)
        Verbose Return:
            G (networkx)
            add_edge (tuple) - the tuple denoting the added edge
            removed_edge (tuple) - the tuple denoting the removed edge
            temp_max (float) - the spectral radius of the rewired network after the step
            delta (float) - the amount of increase of spectral radius between inital
                            graph and rewired graph
        """

        if copy_graph:
            G = copy.deepcopy(G)

        if baseline_max == -1:
            # find the max eigval
            adj_mat = nx.to_numpy_array(G)
            evl = nl.eigvals(adj_mat)
            baseline_max = max(evl)

        temp_max = 0
        delta = 0

        # set list of potential new edges
        regular_edges = set([(i[0], i[1]) for i in list(G.edges())])
        reversed_edges = set([(i[1], i[0]) for i in list(G.edges())])
        if nx.is_directed(G):
            potential_edges = (
                    set(it.product(G.nodes, G.nodes))
                    - set(zip(G.nodes, G.nodes))
                    - regular_edges
            )
        else:
            potential_edges = (
                    set(it.product(G.nodes, G.nodes))
                    - set(zip(G.nodes, G.nodes))
                    - regular_edges - reversed_edges
            )

        # random choice of add/remove edges for this iteration
        i = random.choice(list(G.nodes))
        num_neighbors_i = len(list(G.edges(i)))
        while num_neighbors_i <= 1:
            i = random.choice(list(G.nodes))
        new_edge = random.choice(list(potential_edges))
        old_edge = random.choice(list(G.edges(i)))

        # rewire
        G.remove_edges_from([old_edge])
        G.add_edges_from([new_edge])
        # print(np.mean(list(dict(G.degree()).values())), G.number_of_nodes(), G.number_of_edges())
        if verbose:
            added_edge = [new_edge]
            removed_edge = [old_edge]

        # test whether the change was an improvement
        temp_adj = nx.to_numpy_array(G)
        temp_evl = nl.eigvals(temp_adj)
        temp_max = max(temp_evl)
        delta = temp_max - baseline_max

        # if the rewire decreased the spectral radius, undo the rewire
        if temp_max < baseline_max:
            G.remove_edges_from([new_edge])
            G.add_edges_from([old_edge])

        if verbose:
            return G, added_edge, removed_edge, temp_max, delta
        else:
            return G