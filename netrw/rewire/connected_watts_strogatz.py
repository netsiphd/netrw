from .base import BaseRewirer
import networkx as nx


class ConnectedWattsStrogatz(BaseRewirer):
    """
    Rewire a ring lattice network of size n with node degree k with probability p.
    It initializes a ring lattice network of size n where each node is connected
    to its k nearest neighbors. Then each edge is rewired to a randomly chosen node
    with probability p. The resulting network is then checked for connectivity.
    If the network is connected, it is returned. If it is not connected, the process
    is rerun.

    Watts, D., Strogatz, S. Collective dynamics of ‘small-world’ networks. Nature 393, 440–442 (1998). https://doi.org/10.1038/30918
    """

    def connected_watts_strogatz_network(n, k, p, tries=100, seed=None):
        """
        Generate a Watts-Strogatz network with n nodes where each node is connected
        to its k-nearest neighbors and each edge is rewired with probability p. The
        process is repeated until a connected graph results or the number of attempts
        has reached maximum (tries).

        This is done with networkx standard implementation.

        Aric A. Hagberg, Daniel A. Schult and Pieter J. Swart, “Exploring network structure, dynamics, and function using NetworkX”, in Proceedings of the 7th Python in Science Conference (SciPy2008), Gäel Varoquaux, Travis Vaught, and Jarrod Millman (Eds), (Pasadena, CA USA), pp. 11–15, Aug 2008

        Parameters:
            n (int) - number of nodes
            k (int) - number of nearest-neighbors with which each node connects
            p (float) - probability of edge rewiring
            tries (int) - number of iterations to attempt to create connected graph
            seed (int) - indicator of random seed generator state

        Returns:
            G (networkx)
        """
        return nx.connected_watts_strogatz_graph(n, k, p, tries, seed)
