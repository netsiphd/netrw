import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def visualize_rewiring(G1, G2, pos):
    A1 = nx.adjacency_matrix(G1)
    A2 = nx.adjacency_matrix(G2)
    A_dif = abs(A2 - A1)
    G3 = nx.Graph(A_dif)
    nx.draw(G3, pos, edge_color="r", node_color="b", node_size=0, width=8)
    nx.draw(G2, pos, edge_color="b", node_color="b", node_size=80, width=5)


def visualize_graph(G, pos):
    nx.draw(G, pos, edge_color="b", node_color="b", node_size=80, width=5)
