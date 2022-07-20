import networkx as nx
import numpy as np
import random
import copy
from .base import BaseRewirer


class SpatialSmallWorld(BaseRewirer):
    """
    Implements spatial small worlds with optional periodic boundary conditions and optional rewiring instead of edge addition following the algorithm described in:
    Barthelemy, Marc. "Spatial Small-Worlds." Spatial Networks. Springer, Cham, 2022. 243-252.

    Nodes *MUST* have names equal to lists of their coordinates. Lattice graphs with this scheme can be initialized by the intialize function.
    """

    # int(p*len(G.nodes()))
    def step_rewire(
        self,
        G,
        p,
        dim,
        alpha,
        copy_graph=False,
        is_periodic=True,
        does_remove=True,
        timesteps=1,
        directed=False,
        verbose=False,
    ):
        if copy_graph:
            G = copy.deepcopy(G)
        if nx.is_directed(G) and directed is True:
            warnings.warn(
                "This algorithm is designed for undirected graphs. The graph input is directed and will be formatted to an undirected graph.",
                SyntaxWarning,
            )
            G = nx.to_undirected(G)
        if verbose:
            removed_edges = {}
            added_edges = {}
        for t in range(timesteps):
            if len(dim) == 3:
                dimsize = 3
            elif len(dim) == 2:
                dimsize = 2
            else:
                raise ValueError("Lattice Dimension is not 2-3")
            if dimsize == 3:
                non_edge_list = list(nx.Graph(nx.non_edges(G)).edges())
                if not is_periodic:
                    edge_p = [
                        (
                            (edge_pair[0][0] - edge_pair[1][0]) ** 2
                            + (edge_pair[0][1] - edge_pair[1][1]) ** 2
                            + (edge_pair[0][2] - edge_pair[1][2]) ** 2
                        )
                        ** (1 / 2)
                        for edge_pair in non_edge_list
                    ]
                    unique_lengths = np.unique(edge_p)
                else:
                    edge_p = [
                        (
                            abs(edge_pair[0][0] - edge_pair[1][0]),
                            abs(edge_pair[0][1] - edge_pair[1][1]),
                            abs(edge_pair[0][2] - edge_pair[1][2]),
                        )
                        for edge_pair in non_edge_list
                    ]
                    edge_p = [
                        (
                            (dim[2] - dists[0])
                            if dists[0] > (dim[2]) / 2
                            else dists[0],
                            (dim[1] - dists[1])
                            if dists[1] > (dim[1]) / 2
                            else dists[1],
                            (dim[0] - dists[2])
                            if dists[2] > (dim[0]) / 2
                            else dists[2],
                        )
                        for dists in edge_p
                    ]
                    edge_p = [
                        (dists[0] ** 2 + dists[1] ** 2 + dists[2] ** 2) ** (1 / 2)
                        for dists in edge_p
                    ]
                    unique_lengths = np.unique(edge_p)
                randomVal = random.choices(
                    unique_lengths, weights=(1 / np.power(unique_lengths, (alpha))), k=1
                )
                indices = list(np.where(np.array(edge_p) == randomVal)[0])
                randomList = random.choices([non_edge_list[i] for i in indices], k=1)
                edge_list = list(G.edges())
                rand_edge = edge_list[random.randint(0, len(edge_list) - 1)]
                if does_remove:
                    G.remove_edge(rand_edge[0], rand_edge[1])
                G.add_edge(randomList[0][0], randomList[0][1])
            elif dimsize == 2:
                non_edge_list = list(nx.Graph(nx.non_edges(G)).edges())
                if not is_periodic:
                    edge_p = [
                        (
                            (edge_pair[0][0] - edge_pair[1][0]) ** 2
                            + (edge_pair[0][1] - edge_pair[1][1]) ** 2
                        )
                        ** (1 / 2)
                        for edge_pair in non_edge_list
                    ]
                    unique_lengths = np.unique(edge_p)
                else:
                    edge_p = [
                        (
                            abs(edge_pair[0][0] - edge_pair[1][0]),
                            abs(edge_pair[0][1] - edge_pair[1][1]),
                        )
                        for edge_pair in non_edge_list
                    ]
                    edge_p = [
                        (
                            dim[1] - dists[0] if dists[0] > (dim[1]) / 2 else dists[0],
                            dim[0] - dists[1] if dists[1] > (dim[0]) / 2 else dists[1],
                        )
                        for dists in edge_p
                    ]
                    edge_p = [
                        (dists[0] ** 2 + dists[1] ** 2) ** (1 / 2) for dists in edge_p
                    ]
                    unique_lengths = np.unique(edge_p)
                randomVal = random.choices(
                    unique_lengths, weights=(1 / np.power(unique_lengths, (alpha))), k=1
                )
                indices = list(np.where(np.array(edge_p) == randomVal)[0])
                randomList = random.choices([non_edge_list[i] for i in indices], k=1)
                edge_list = list(G.edges())
                rand_edge = edge_list[random.randint(0, len(edge_list) - 1)]
                if does_remove:
                    G.remove_edge(rand_edge[0], rand_edge[1])
                G.add_edge(randomList[0][0], randomList[0][1])
            if verbose:
                if does_remove:
                    removed_edges[t] = [rand_edge[0], rand_edge[1]]
                added_edges[t] = [randomList[0][0], randomList[0][1]]
        if verbose:
            return G, removed_edges, added_edges
        else:
            return G

    def full_rewire(
        self,
        G,
        p,
        dim,
        alpha,
        copy_graph=False,
        is_periodic=True,
        does_remove=True,
        timesteps=-1,
        directed=False,
        verbose=False,
    ):
        if timesteps == -1:
            timesteps = int(p * len(G.nodes()))
        G = self.step_rewire(
            G,
            p,
            dim,
            alpha,
            copy_graph,
            is_periodic,
            does_remove,
            timesteps,
            directed,
            verbose,
        )
        return G

    def initialize_graph(self, dim):
        if len(dim) == 3:
            dimsize = 3
        elif len(dim) == 2:
            dimsize = 2
        else:
            raise ValueError("Lattice Dimension is not 2-3")
        G = nx.grid_graph(dim=dim, periodic=False)
        return G

    def plot(self, G, dim):
        if len(dim) == 3:
            dimsize = 3
        elif len(dim) == 2:
            dimsize = 2
        else:
            raise ValueError("Lattice Dimension is not 2-3")
        if dimsize == 3:
            pos = {(x, y, z): (x + 5 * z / 7, y + 5 * z / 7) for x, y, z in G.nodes()}
        elif dimsize == 2:
            pos = {(x, y): (x, y) for x, y in G.nodes()}
        nx.draw(G, pos)
