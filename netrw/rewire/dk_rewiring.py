from .base import BaseRewirer
import networkx as nx
import warnings
import copy
import random

class DkRewire(BaseRewirer):
    """
    Rewires a given network such that its "d"k-distribution is preserved.
    This class preserves distributions up through 4k-distributions.
    It can be implemented for one time step or a series of rewirings.
    At each steps, a pair of edges is selected and rewired such that the
    "d"k-distribution is preserved for a given value of d.

    Orsini, C. et al. Quantifying randomness in real networks. Nat. Commun. 6:8627 doi: 10.1038/ncomms9627 (2015).
    """
    def step_rewire(G,d,copy_graph=True,timesteps=1,tries=1000,directed=False,verbose=False):
        """
        This function calls the necessary function to rewire such that the
        'd'k-distribution is preserved for given d. This function is implemented
        for undirected, simple networks.

        Parameters:
            G (networkx)
            d (int) - distribution to analyze
                d = 0 - average degree
                d = 1 - degree distribution
                d = 2 - joint degree distribution
                d = 3 - triangle and wedge degree distributions
                d = 4 - star, path, triangle with path, square, square with diagonal, and K4 distributions
            copy_graph (bool) - update a copy of the network. default True.
            timesteps (int) - number of edge swaps to perform. default 1.
            tries (int) - maximum number of tries to perform an edge swap. default 100.
            directed (bool) - indicator of whether to force directed graph to be undirected. default False.
            verbose (bool) - indicator of whether edges rewired should be returned. default False.

        Returns:
            G (networkx)
            removed_edges (dict) - edges deleted at each timestep
            added_edges (dict) - edges added at each timestep
        """
        # Check that graph is undirected
        if nx.is_directed(G):
            if directed:
                warnings.warn("This algorithm is designed for undirected graphs. The graph input is directed and will be formatted to an undirected graph.",
                SyntaxWarning)
                G = nx.to_undirected(G)
            else:
                raise ValueError("This algorithm is designed for undirected graphs. If you wish to run anyway as an undirected graph, set directed=True")

        # Make copy if necessary
        if copy_graph:
            G = copy.deepcopy(G)

        # Calculate 0k-swap
        if d == 0:
            zero_k_swap(G,timesteps,verbose)

        # Calculate 1k-swap
        elif d == 1:
            one_k_swap(G,timesteps,tries,verbose)

        # Calculate 2k-swap
        elif d == 2:
            two_k_swap(G,timesteps,tries,verbose)

        # Calculate 2.1k-swap
        elif d == 2.1:
            two_one_k_swap(G,timesteps,tries,verbose)

        # Calculate 2.5k-swap
        elif d == 2.5:
            two_five_k_swap(G,timesteps,tries,verbose)

        else:
            raise ValueError("d must be 0, 1, 2, 2.1, or 2.5")


        pass

    def zero_k_swap(G,timesteps,verbose):
        """
        Rewires one edge to a random node. This maintains the average degree of the network.
        At each timestep, a random edge is chosen and a random end of the edge is chosen.
        This edge is rewired to a randomly chosen node from all nodes in the graph with the
        exception of the node being connected.


        Parameters:
            G (networkx)
            timesteps (int) - number of edge swaps to perform
            verbose (bool) - indicator of storing edges deleted and added
            seed (int) - indicator of random seed generator state

        Returns:
            G (networkx)
            removed_edges (dict) - edges deleted at each timestep
            added_edges (dict) - edges added at each timestep
        """
        # Initialize dictionaries if verbose
        if verbose:
            removed_edges = {}
            added_edges = {}

        # Edge swap for each time step
        for t in range(timesteps):
            # Choose a random edge
            edge = random.choice(G.edges())

            # Choose a random end of the edge
            end_of_edge = random.choice([0,1])
            not_end_of_edge = abs(end_of_edge-1)

            # Choose a random node
            nodes_to_choose = list(G.nodes())
            nodes_to_choose.pop(edge[end_of_edge])
            node = random.choice(nodes_to_choose)

            # If verbose, store edges
            if verbose:
                removed_edges[t] = [edge]
                added_edges[t] = [(edge[not_end_of_edge],node)]

            # Update network
            G.remove_edge(edge[0],edge[1])
            G.add_edge(edge[not_end_of_edge],node)

        if verbose:
            return G, removed_edges, added_edges
        else:
            return G

    def one_k_swap(G,timesteps,tries,verbose,seed):
        """
        Rewires an edge while maintaining the degree distribution of the network.
        A swap is done such that if edges (u,v) and (x,y) are selected, the new edges are (u,x) and (v,y)
        or (u,y) and (v,x). Each is chosen with a fifty-percent chance.

        Parameters:
            G (networkx)
            timesteps (int) - number of edge swaps to perform
            tries (int) - number of tries for each edge swap
            verbose (bool) - indicator of storing edges deleted and added
            seed (int) - indicator of random seed generator state

        Return:
            G (networkx)
            prev_edges (dict) - edges deleted at each timestep
            new_edges (dict) - edges added at each timestep
        """
        # intialize storing dictionaries if verbose
        if verbose:
            prev_edges = {}
            new_edges = {}

        # Perform `timesteps` edge swaps
        for t in range(timesteps):
            # Attempt at rewiring
            valid = False
            for _ in range(tries):
                # Get current edges
                edges = list(G.edges())

                # Choose two random edges
                old_edge_1 = random.choice(edges)
                old_edge_2 = random.choice(edges)

                if .5 < np.random.random(seed=seed)
                    # Swap edges
                    new_edge_1 = (old_edge_1[0],old_edge_2[0])
                    new_edge_2 = (old_edge_1[1],old_edge_2[1])

                    # Check for valid edges
                    if new_edge_1 in list(G.edges()) or new_edge_2 not in list(G.edges()):
                        valid = True
                        break

                else:
                    new_edge_1 = (old_edge_1[0],old_edge_2[1])
                    new_edge_2 = (old_edge_1[1],old_edge_2[0])
                    # Check for valid edges
                    if new_edge_1 in list(G.edges()) or new_edge_2 not in list(G.edges()):
                        valid = True
                        break

            # Check that tries was not maximized
            if valid is False:
                warnings.warn("No pair of edges was found with new edges that did not exist in tries allotted. Switch was not made at this timestep.")

            # Store edges if verbose
            if verbose:
                prev_edges[t] = [old_edge_1,old_edge_2]
                new_edges[t] = [new_edge_1,new_edge_2]

            # Update network
            G.remove_edges_from([old_edge_1,old_edge_2])
            G.add_edges_from([new_edge_1,new_edge_2])

        return G

    def two_k_swap(G,timesteps,tries,verbose):
        """
        Rewires an edge while maintaining the joint degree distribution of the network.
        A swap is done by selecting two edges which each have a node of equal degree
        (e_1 = (v_1,v_2) and e_2 = (w_1,w_2) where d(v_1)=d(w_1)). It then swaps the edges
        to become (v_1,w_2) and (w_1,v_2).

        Parameters:
            G (networkx)
            timesteps (int) - number of edge swaps to perform
            tries (int) - maximum number of edge swap attempts at each timestep
            verbose (bool) - indicator of storing edges deleted and added

        Returns:
            G (networkx)
            removed_edges (dict) - dictionary of edges removed
            added_edges (dict) - dictionary of edges added
        """
        # Initialize storing
        pass
