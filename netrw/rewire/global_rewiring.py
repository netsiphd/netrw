from .base import BaseRewirer
import copy
import random
import warnings


class GlobalRewiring(BaseRewirer):
    """
    Rewire a network where a random edge is chosen and rewired with probability p.
    """

    def full_rewire(
        self, G, p, timesteps=-1, tries=100, copy_graph=True, verbose=False
    ):
        """
        Run a full rewire of the global edge rewiring.
        """
        return self.step_rewire(G, p, timesteps, tries, copy_graph, verbose)

    def step_rewire(self, G, p, timesteps=1, tries=100, copy_graph=True, verbose=False):
        """
        Generate a Watts-Strogatz network with n nodes where each node is connected
        to its k-nearest neighbors and each edge is rewired with probability p.
        This is done with networkx standard implementation.
        Parameters:
            G (networkx)
            p (float) - probability of edge rewiring
            timesteps (int) - number of edges to rewire. if -1, timesteps is the number of edges.
            tries (int) - number of attempts to find a new edge.
            copy_network (bool) - indicator of whether to rewire network copy
            verbose (bool) - indicator to return edges changed at each timestep
        Returns:
            G (networkx)
            removed_edges (dict) - edges deleted at each timestep
            added_edges (dict) - edges added at each timestep
        """
        # Make copy if necessary
        if copy_graph:
            G = copy.deepcopy(G)

        # Check for empty graph
        if len(G.edges()) == 0:
            warnings.warn(
                "Resulting graph is empty as input was an empty graph and no edges can be rewired."
            )
            return G

        # If verbose save edge changes
        if verbose:
            removed_edges = {}
            added_edges = {}

        # Give every edge opportunity to change
        if timesteps == -1:
            timesteps = len(list(G.edges())) * 10

        # Rewire at each timestep
        for t in range(timesteps):
            # Decide whether to rewire
            if p > random.random():
                # Attempt to rewire
                valid = False
                for _ in range(tries):
                    # Choose edge to rewire
                    edge = random.choice(list(G.edges()))

                    # Choose end to rewire
                    end_to_rewire = random.choice([0, 1])
                    end_to_stay = abs(end_to_rewire - 1)

                    # Choose random node to rewire to
                    nodes_to_choose = list(G.nodes())
                    nodes_to_choose.pop(edge[end_to_stay])
                    node = random.choice(nodes_to_choose)

                    # Rewire edge
                    if end_to_rewire == 0:
                        new_edge = (node, edge[end_to_stay])
                    else:
                        new_edge = (edge[end_to_stay], node)

                    # Check that edge is new
                    if new_edge not in G.edges():
                        valid = True
                        break

                # Check that no edge was added
                if valid is False:
                    warnings.warn(
                        "No rewiring occured as no new edge was found in tries allotted."
                    )

                else:
                    # Update dictionaries if verbose
                    if verbose:
                        removed_edges[t] = [edge]
                        added_edges[t] = [new_edge]

                    # Update network
                    G.remove_edge(edge[0], edge[1])
                    G.add_edge(new_edge[0], new_edge[1])

        if verbose:
            return G, removed_edges, added_edges

        else:
            return G
