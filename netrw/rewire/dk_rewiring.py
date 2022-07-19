from .base import BaseRewirer
import networkx as nx
import warnings

class DkRewire(BaseRewirer):
    """
    Rewires a given network such that its "d"k-distribution is preserved.
    This class preserves distributions up through 4k-distributions.
    It can be implemented for one time step or a series of rewirings.
    At each steps, a pair of edges is selected and rewired such that the
    "d"k-distribution is preserved for a given value of d.

    Orsini, C. et al. Quantifying randomness in real networks. Nat. Commun. 6:8627 doi: 10.1038/ncomms9627 (2015).
    """
    def dk_rewire(G,d,timesteps=1,directed=False,verbose=False):
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
            timesteps (int) - number of edges to rewire
            directed (bool) - indicator of whether to force directed graph to be undirected
            verbose (bool) - indicator of whether edges rewired should be returned

        Returns:
            G (networkx)
            prev_edges (dict) - edges deleted at each timestep
            new_edges (dict) - edges added at each timestep
        """
        # Check that graph is undirected
        if nx.is_directed(G):
            if directed:
                warnings.warn("This algorithm is designed for undirected graphs. The graph input is directed and will be formatted to an undirected graph.",
                SyntaxWarning)
                G = nx.to_undirected(G)
            else:
                raise ValueError("This algorithm is designed for undirected graphs. If you wish to run anyway as an undirected graph, set directed=True")

        # Check for verbose
        if verbose:
            prev_edges = {}
            new_edges = {}

        
