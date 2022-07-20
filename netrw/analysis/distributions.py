from copy import deepcopy

import numpy as np


def get_property_distribution(
    G, rewiring_method, property, skip=10, num_samples=1000, **kwargs
):
    """_summary_

    More details

    Parameters
    ----------
    G : NetworkX graph
        The initial graph
    rewiring_method : Rewire method
        The class that will rewire the graph step-by-step. Must have the method `step_rewire`.
    property : function
        a function that accepts a NetworkX Graph object as an input. This computes a property of interest.
    skip : int, default:100
        How often to store the property of interest.
    num_samples : int, default: 1000
        The number of samples to form the empirical distribution.
    **kwargs : optional keyword args for the rewiring method

    Returns
    -------
    numpy array
        an array of properties from each point outputted in the rewiring process.
    """
    G = deepcopy(G)
    rw = rewiring_method()
    properties = np.zeros(num_samples)
    for i in range(num_samples):
        for j in range(skip):
            G = rw.step_rewire(G, copy_graph=False, **kwargs)
            if j >= skip - 1:
                properties[i] = property(G)
        print(i)
    return properties
