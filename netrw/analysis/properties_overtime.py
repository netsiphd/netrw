from copy import deepcopy
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import netrw
from netrw.rewire import KarrerRewirer, AlgebraicConnectivity, NetworkXEdgeSwap


def properties_overtime(init_graph, rewire_method, property1, tmax, numit):
    """
    Analyze the property values of a network as a function of rewire steps.
    Looks at how a network property changes as a rewiring process occurs.

    Parameters
    ----------
    init_graph : NetworkX graph
        Initial graph upon which rewiring will occur.
    rewire_method : netrw rewire class object
        Algorithm for rewiring a network with step_rewire option
    property1 : NetworkX function
        Network description property that outputs a single value for a given network. Should work with any function that
        summarizes a NetworkX graph object into a single value. For example, nx.average_clustering, nx.average_shortest_path_length, etc.
    tmax : int
        Number of rewiring steps to perform for each iteration.
    numit : int
        Number of rewiring iterations to perform on the initial graph. The given rewiring process will be performed numit
        times on the initial graph to look at the distribution of outcomes for this rewiring process on the initial graph.
    Returns
    -------
    property_dict: dictionary
        Dictionary of output where the keys are the property name and the values are a 2D numpy arry of the network property 
        calculated at each step and iteration of the rewiring process. Rows are single iteration over a rewiring process.
        Columns show different iterations of the rewiring process from the initial graph.

    """
    property_dict = {}
    property_dict[property1.__name__] = np.zeros((numit, tmax))
    rw = rewire_method()

    for i in range(numit):
        G0 = deepcopy(init_graph)
        propertyval = property1(G0)  # calculate property of initial network
        property_dict[property1.__name__][i,0] = propertyval
        for j in range(1,tmax):
            G0 = rw.step_rewire(G0, copy_graph=False)  # rewire
            propertyval = property1(G0) # calculate property of the rewired network
            property_dict[property1.__name__][i,j] = propertyval
  
    return property_dict
