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
        Dictionary of output where the keys are the iteration number and the values are a list of the network property calculated
        at each step of the rewiring process.
    fig: matplotlib figure
        Plot of the mean value of the given network property at each step of the rewiring process, where shading within 
        the upper and lower bounds represent the standard deviation of the property value around the mean. 
    """
     
    property_dict = {}
    rw = rewire_method()

    for i in range(numit):
        G0 = deepcopy(init_graph)
        property_list = [property1(G0)] # calculate property of initial network
        for j in range(tmax):
            G0 = rw.step_rewire(G0, copy_graph=False) #rewire 
            property_list.append(property1(G0)) #calculate property of the rewired network
        property_dict[i] = property_list
        
    
    alllist = [] # list of all properties for all iterations at each of the time steps
    for k in range(tmax):
        alllist.append([])
        for l in range(numit):
            alllist[k].append(property_dict[l][k])
            
    # find mean and standard deviation over different iterations of rewiring process        
    meanlist = []
    sdlist = []
    for k in range(tmax):
        meanlist.append(np.mean(alllist[k]))
        sdlist.append(np.std(alllist[k]))

    # find upper and lower bound of standard deviation interval around the mean
    upperbd = []
    lowerbd = []
    for a in range(len(meanlist)):
        upperbd.append(meanlist[a]+sdlist[a])
        lowerbd.append(meanlist[a]-sdlist[a])

    return property_dict 