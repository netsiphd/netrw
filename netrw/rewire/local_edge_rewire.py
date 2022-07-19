from . import BaseRewirer
import copy
import random
import networkx as nx
import numpy as np

class LocalEdgeRewiring(BaseRewirer):
    """Perturb one edge of node `i` in the way described by Klein & McCabe
    (2019). Select a random node `i`, randomly select one of its edges `ij`,
    delete `ij` and add a new edge `ik` where `k` is a neighbor of `j` (i.e., 
    a "friend of friend" rewiring where `jk` is an edge present in the graph).

    If `ij` is a weighted edge, its weight gets carried over to the new edge
    `ik`.

    Klein, Brennan & Stefan McCabe. “Local edge perturbations as a measure for
    community persistence in complex networks” (2019). NetSci. Burlington,
    Vermont (poster presentation).

    Details:
    - Does not produce multi-edges.
    - Is not implemented specifically for directed graphs. (Could be though.)
    """

    def step_rewire(
        self, G, copy_graph=True, verbose=False
    ):
        """
        Parameters
        ----------
        G (networkx graph)
            The original network in question.

        copy_graph (bool)
            Useful parameter for making sure input data doesnt change.

        Returns
        -------
        G (networkx graph)
            The graph with a single rewired edge. If the algorithm randomly
            attempts to rewire in a location where no rewirings are permitted,
            the graph does not change and the original G is returned.
        
        """

        if copy_graph:
            G = copy.deepcopy(G)

        if nx.is_directed(G):
            warnings.warn(
            "This algorithm is designed for undirected graphs. \
            The graph input is directed and will be formatted to an \
            undirected graph.", SyntaxWarning,
            )
            G = nx.to_undirected(G)

        # randomly select a node, i
        i = random.choice(list(G.nodes))

        # randomly select one of its neighbors, j. if none available, return G
        if len(list(G[i])) == 0:
            return G
        j = random.choice(list(G[i]))
        e_ij = (i,j)
        
        # store edge attributes of e_ij to add to e_ik if needed
        ### Note: If there are no edge (e.g.) weights, this adds an empty
        ### dictionary as the "edge attribute" (this is standard for networkx)
        e_ij_attr = G.get_edge_data(*e_ij)

        # get the set of all edges incident to i and j but are not ij or ji
        all_non_eij_edges = set(G.edges([i,j])) - set([(i,j)]) - set([(j,i)])
        
        # Two steps: First, narrow that list down to only edges of j, then
        # subset the list again to make sure that none of the candidate edges
        # are already connected to i.
        candidate_edges = [(i,x[1]) for x in all_non_eij_edges if i not in x]
        candidate_edges = list(set(candidate_edges) - set(G.edges(i)))

        # If there are no candidate edges eligible, we'll be returning the 
        # same graph that was input. Otherwise, randomly select a candidate
        # edge to be the new e_ik added to the network.
        e_ik = e_ij
        if len(candidate_edges)>0:
            e_ik = candidate_edges[np.random.choice(len(candidate_edges))]

        # remove old edge, add new edge (and give it the old edge's attribs)
        G.remove_edge(*e_ij)
        G.add_edge(*e_ik)
        nx.set_edge_attributes(G, {e_ik:e_ij_attr})

        if not verbose:
            return G
        else:
            removed_edges = {0:[e_ij]}
            added_edges = {0:[e_ik]}

            return G, added_edges, removed_edges

    def full_rewire(
        self, G, timesteps=-1, copy_graph=True, verbose=False
    ):
        """
        Repeatedly apply the `step_rewire` for `timesteps` iterations. If 
        timesteps=-1, we default to timesteps = 10 * number_of_edges
        iterations.
        """

        if copy_graph:
            G = copy.deepcopy(G)

        # Give every edge opportunity to change
        if timesteps == -1:
            timesteps = len(list(G.edges())) * 10

        # If verbose save edge changes
        if verbose:
            removed_edges = {}
            added_edges = {}

        for t in range(timesteps):
            if verbose:
                G, remov_t, added_t = step_rewire(G, copy_graph, verbose)
                removed_edges[t] = remov_t[0]
                added_edges[t] = added_t[0]


        if not verbose:
            return G
        else:
            return G, added_edges, removed_edges
