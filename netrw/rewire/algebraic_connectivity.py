from .base import BaseRewirer
import networkx as nx
import numpy as np
import copy
from scipy import linalg as la
import warnings


class AlgebraicConnectivity(BaseRewirer):
    """
    Rewire a network such that the rewire maximally increases
    the algebraic connectivity of a network. It does this by
    computing the Fielder vector of a given network and determining
    the value of alpha for each edge, where v is the Fielder vector
    and alpha_{ij} = |v_i-v_j| is absolute difference of the entries
    in the Fiedler vector for nodes i and j such that (i,j) in E(G).
    The edge with the smallest value of alpha is removed and the non-edge
    with the largest alpha is added.

    Sydney, Ali, Caterina Scoglio, and Don Gruenbacher.
    "Optimizing algebraic connectivity by edge rewiring."
    Applied Mathematics and computation 219.10 (2013): 5465-5479.
    """

    def full_rewire(
        self, G, timesteps=-1, copy_graph=True, directed=False, verbose=False
    ):
        """
        Rewire network to maximize algebraic connectivity. In Sydney et al. paper,
        they find that rewiring 30% of the edges is sufficient.
        """
        return self.step_rewire(G, timesteps, copy_graph, directed, verbose)

    def step_rewire(
        self, G, timesteps=1, copy_graph=False, directed=False, verbose=False
    ):
        """
        Rewire ``timesteps`` edges to maximize algebraic connectivity.

        Parameters:
            G (networkx)
            timesteps (int) - number of edge rewires
            copy_graph (bool) - return a copy of the network
            directed (bool) - compute for directed network on undirected copy
            verbose (bool) - indicator to return edges changed at each timestep

        Return:
            G (networkx)
        """
        if copy_graph:
            G = copy.deepcopy(G)

        if not nx.is_connected(G):
            raise ValueError(
                "Disconnected graph. This method is implemented for undirected, connected graphs."
            )

        if nx.is_directed(G) and directed is True:
            warnings.warn(
                "This algorithm is designed for undirected graphs. The graph input is directed and will be formatted to an undirected graph.",
                SyntaxWarning,
            )
            G = nx.to_undirected(G)

        # Initialize storing dictionaries if necessary
        if verbose:
            removed_edges = {}
            added_edges = {}

        # Check for full rewire
        if timesteps == -1:
            timesteps = int(0.3 * len(G.edges()))

        # Get necessary parameters
        nodes = list(G.nodes())
        edges = list(G.edges())
        n = len(nodes)
        m = len(edges)

        # Check for complete graph
        if m == int(n * (n - 1) / 2):
            raise Warning("Algebraic connectivity is already maximized.")
            return G

        # Rewire ``timesteps`` edges
        for t in range(timesteps):
            # Reset edge and node list
            nodes = list(G.nodes())
            edges = list(G.edges())

            # Compute fielder vector
            L = nx.laplacian_matrix(G).toarray()
            vals, vecs = la.eig(L)
            fiedler_idx = np.where(np.argsort(np.abs(vals)))[0][0]
            v = vecs[:, fiedler_idx]

            # Get all values of alpha
            alpha = np.abs(np.subtract.outer(v, v))

            # Get alpha_values for edges and non_edges
            non_edges = []
            edge_alpha = []
            non_edge_alpha = []
            for i in range(n):
                for j in range(i + 1, n):
                    if (nodes[i], nodes[j]) in edges:
                        edge_alpha.append(alpha[i, j])
                    else:
                        non_edges.append((nodes[i], nodes[j]))
                        non_edge_alpha.append(alpha[i, j])

            # Get max alpha
            alpha_max = np.argmax(non_edge_alpha)

            # Get minimum alpha
            accept_min = False
            if accept_min is False:
                alpha_min = np.argmin(edge_alpha)

                # Create G without e_min
                g_copy = copy.deepcopy(G)
                g_copy.remove_edge(edges[alpha_min][0], edges[alpha_min][1])

                # Get fiedler value
                lap_spec = nx.laplacian_spectrum(g_copy)

                # Check that fiedler value is positive on G\e_{min}
                if sorted(np.abs(lap_spec))[1] > 0:
                    accept_min = True
                else:
                    # Delete e_{min} from possible edges
                    edge_alpha[alpha_min] = np.inf
                    # Check for lack of convergence
                    if np.array(edge_alpha).all() == np.inf:
                        raise ValueError("Failed to converge.")

            # Update dictionaries
            if verbose:
                removed_edges[t] = [(edges[alpha_min][0], edges[alpha_min][1])]
                added_edges[t] = [(non_edges[alpha_max][0], non_edges[alpha_max][1])]

            # Remove edge
            G.remove_edge(edges[alpha_min][0], edges[alpha_min][1])
            # Add edge
            G.add_edge(non_edges[alpha_max][0], non_edges[alpha_max][1])

        # Return new network
        if verbose:
            return G, removed_edges, added_edges
        else:
            return G
