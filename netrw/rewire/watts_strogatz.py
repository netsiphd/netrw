from .base import BaseRewirer
import networkx as nx


class WattsStrogatz(BaseRewirer):
    """
    Rewire a ring lattice network of size n with node degree k with probability p.
    It initializes a ring lattice network of size n where each node is connected
    to its k nearest neighbors. Then each edge is rewired to a randomly chosen node
    with probability p. The resulting network is then returned.

    Watts, D., Strogatz, S. Collective dynamics of ‘small-world’ networks. Nature 393, 440–442 (1998). https://doi.org/10.1038/30918
    """

    def watts_strogatz_network(n, k, p, seed=None):
        """
        Generate a Watts-Strogatz network with n nodes where each node is connected
        to its k-nearest neighbors and each edge is rewired with probability p.

        This is done with networkx standard implementation.

        Aric A. Hagberg, Daniel A. Schult and Pieter J. Swart, “Exploring network structure, dynamics, and function using NetworkX”, in Proceedings of the 7th Python in Science Conference (SciPy2008), Gäel Varoquaux, Travis Vaught, and Jarrod Millman (Eds), (Pasadena, CA USA), pp. 11–15, Aug 2008

        Parameters:
            n (int) - number of nodes
            k (int) - number of nearest-neighbors with which each node connects
            p (float) - probability of edge rewiring
            seed (int) - indicator of random seed generator state

        Returns:
            G (networkx)
        """
        return nx.watts_strogatz_graph(n, k, p, seed)
