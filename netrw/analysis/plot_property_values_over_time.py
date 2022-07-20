import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import netrw


def plot_property_values_over_time(propvals, ylabel=""):
    """
    Plot mean and standard deviation of how a network property changes over time during multiple iterations of a rewiring process.

    Parameters
    ----------
    propvals :2d nump array
        2d numpy array of output values from dictionary of properties_overtime.
        The network property is calculated at each step and iteration of the rewiring process. Rows are single iteration over a rewiring process.
        Columns show different iterations of the rewiring process from the initial graph.
        
    ylabel: string, optional
        Label for y axis of graph for mean and standard deviation of network property
        Default is no label.

    Returns
    -------
    fig: matplotlib figure
        Figure of mean and standard deviation for a network property throughout the rewiring process.

    """
    
    alllist = []  # list of all properties for all iterations at each of the time steps
    
    valarray = propvals
    num_rows, num_cols = valarray.shape
        
    for k in range(num_cols):
        alllist.append([])
        for l in range(num_rows):
            alllist[k].append(valarray[l][k])

    # find mean and standard deviation over different iterations of rewiring process
    meanlist = []
    sdlist = []
    for k in range(num_cols):
        meanlist.append(np.mean(alllist[k]))
        sdlist.append(np.std(alllist[k]))

    # find upper and lower bound of standard deviation interval around the mean
    upperbd = []
    lowerbd = []
    for a in range(len(meanlist)):
        upperbd.append(meanlist[a] + sdlist[a])
        lowerbd.append(meanlist[a] - sdlist[a])

    fig, (ax0) = plt.subplots(nrows=1)
    ax0.plot(range(num_cols), meanlist, color="blue", linewidth=2)
    ax0.plot(range(num_cols), upperbd, color="blue")
    ax0.plot(range(num_cols), lowerbd, color="blue")
    ax0.fill_between(range(num_cols), upperbd, lowerbd, color="cornflowerblue", alpha=0.5)

    ax0.set_xlabel("number of rewiring steps")
    ax0.set_ylabel(ylabel)

    fig.show()

    return fig
