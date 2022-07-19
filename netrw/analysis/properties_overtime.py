from copy import deepcopy
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import netrw
from netrw.rewire import KarrerRewirer, AlgebraicConnectivity, NetworkXEdgeSwap


def properties_overtime(init_graph, rewire_method, property1, tmax, numit):
    '''
        Look at network properties as rewiring method changes the network.
        Input: 
        init_graph = original graph that will be rewired
        rewire_method = netrw method of rewiring that you want to implement that outputs a graph
        property1 = property of interest, (ex. nx.average_clustering, nx.average_shortest_path_length, etc.) 
                    that outputs a single value for a given network
        tmax = amount of time steps (rewirings)
        numit = number of iterations of rewiring the original graph using the method to see variation in results

        Output: 
        property_dict = dictionary of property values for each iteration for each step of the rewiring process
        fig = plot of mean and standard deviation of property of interest at each step of rewiring process
    ''' 

    
    property_dict = {}

    for i in range(numit):
        G0 = deepcopy(init_graph)
        property_list = [property1(G0)] # calculate property of initial network
        for j in range(tmax):
            rewire_method.rewire(G0) #rewire 
            property_list.append(property1(G0)) #calculate property of the rewired network
        property_dict[i] = property_list
        
    
    alllist = [] # list of all properties
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

    # plot mean and standard deviation for chosen property for the given time steps of rewiring
    fig, (ax0) = plt.subplots(nrows=1)
    ax0.plot(range(tmax), meanlist, marker='o', color = 'blue')
    ax0.plot(range(tmax), upperbd, color = 'blue')
    ax0.plot(range(tmax), lowerbd, color = 'blue' )  
    ax0.fill_between(range(tmax), upperbd,lowerbd, color='cornflowerblue',alpha=.5) 
    ax0.set_xlabel('time step', fontsize=15)
    ax0.set_ylabel('Mean property value', fontsize=15)

    fig.show()

    return property_dict, fig

