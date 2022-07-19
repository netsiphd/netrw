from matplotlib import pyplot as plt
import networkx as nx
import numpy as np
import warnings, copy
import netrd
from ..rewire import NetworkXEdgeSwap

def distanceTrajectory(G, distance=netrd.distance.Hamming, 
    rewire=NetworkXEdgeSwap, null_model=None, 
    num_steps=100, num_runs=100, distance_kwargs={}, 
    rewire_kwargs={}, null_model_kwargs={}, **kwargs):
    '''
    Get some data on graph distances as a function of number of rewiring steps.
    
    Parameters
    ----------
    G : networkx Graph or DiGraph
    
    distance : netrd graph distance class
    
    rewire : netrw rewire class
    
    null_model : ???
    
    num_steps : integer or list
       number of rewiring steps to be tracked or ordered list of rewiring
       steps to be tracked
       
    num_runs : integer
       number of trajectories to be generated for evaluating the standard 
       deviation for a set of rewiring trajectories
       
    distance_kwargs : dictionary
       a dictionary of keyword arguments for an instantiation of the netrd
       distance class
       
    rewire_kwargs : dictionary
       a dictionary of keyword arguments for an instantiation of
       the netrw rewire class
       
    null_model_kwargs : dictionary
       a dictionary of keyword arguments for the null model (?)
    
    '''

    G0 = copy.deepcopy(G)
    
    # check whether input for num rewire in a number of rewiring steps (int)
    # or a list of steps
    if hasattr(num_steps, "__iter__"):
        rewire_steps = num_rewire
    else:
        rewire_steps = range(num_steps)
        
    # initialize data array
    data = np.zeros((len(rewire_steps),num_runs))    
    
    # define a rewire function
    step_rewire = rewire().step_rewire
    rewire_function = lambda g : step_rewire(g, copy_graph=False, **rewire_kwargs)
    
    # define a distance function
    distfun = distance() # get a class instantiation
    distance_function = lambda g1, g2: distfun(g1, g2, **distance_kwargs)
    
    for j in range(num_runs):
        for i in range(max(rewire_steps)):
            rewire_function(G0)
            data[i+1,j] = distance_function(G0, G)

    return data


def plotDistanceTrajectory(G, distance=netrd.distance.Hamming, num_steps=100, 
    show=['mean', 'median', 'std-env'], labels=None, add_legend=True, fig=None,
    ax=None, linecolors=None, envcolor='cyan', 
    xlabel='Number of rewiring steps', ylabel=None, **kwargs):
        
    # check whether input for num steps in a number of rewiring steps (int)
    # or a list of steps
    if hasattr(num_steps, "__iter__"):
        rewire_steps = num_steps
    else:
        rewire_steps = range(num_steps)

    # set ylabel
    if ylabel is None:
        ylabel = distance.__name__ + r' distance to $G_0$'

    # set line labels
    if labels is None:
        labels = show
    elif hasattr(labels, "__iter__"):
        if len(labels) != len(show):
            raise ValueError('List for keyword argument `show` and list for'
                +'`keyword argument` must have the same length.')
    else:
        raise ValueError(
            'Keyword argument `labels` must be None or list.')
        
    # set line colors
    if linecolors is None:
        tabcolors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple']
        linecolors = [tabcolors[i % len(tabcolors)] for i in range(len(show))]
    elif hasattr(linecolors, "__iter__"):
        if len(linecolors) != len(show):
            raise ValueError('List for keyword argument `show` and list for'
                +'`keyword argument` must have the same length.')
    else:
        raise ValueError(
            'Keyword argument `labels` must be None or list.')
    
    # get data
    data = distanceTrajectory(G, distance=distance, num_steps=num_steps, **kwargs)
    
    # get data for lines for plot
    line_data = []
    for s in show:
        if s=='mean':
            line_data += [np.mean(data, axis=1)]
        elif s=='std':
            line_data += [np.std(data, axis=1)]
        elif s=='median':
            line_data += [np.median(data, axis=1)]
        elif s=='std-env':
            mean = np.mean(data, axis=1)
            std = np.std(data, axis=1)
            env_data = [std-mean, std+mean]
        else:
            warnings.warn("Unknown summary statistic", s, "will be ignored.")
            
    std = np.std(data, axis=1)
    
    if fig is None:
        fig = plt.gcf()
    if ax is None:
        ax = plt.subplot(111)
    if 'std-env' in show:  
        ax.fill_between(rewire_steps, env_data[0], env_data[1], color=envcolor)
        
    for i in range(len(line_data)):
        ax.plot(rewire_steps, line_data[i], color=linecolors[i], label=labels[i])    
    
    if add_legend:
        plt.legend()
    
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    
    