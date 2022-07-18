import networkx as nx
from netrw import rewire
from netrw.rewire import BaseRewirer


def test_same_return_type():
    """The graph and the rewired graph should be of the same type (Graph, DiGraph)."""
    G = nx.fast_gnp_random_graph(50, 0.1, directed=True)
    H = nx.Graph(G)

    for label, obj in rewire.__dict__.items():
        if isinstance(obj, type) and BaseRewirer in obj.__bases__:
            G_rewired = obj().rewire(G, copy_graph=True)
            H_rewired = obj().rewire(H, copy_graph=True)

            assert isinstance(G_rewired, type(G))
            assert isinstance(H_rewired, type(H))
