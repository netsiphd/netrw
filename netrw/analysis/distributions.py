from copy import deepcopy
import numpy as np

def get_property_distribution(G, rewiring_method, property, burn_in=100, num_samples=1000):
    G_copy = deepcopy(G)

    property_list = np.zeros()
    for i in range(num_samples):
        for j in range(burn_in):
            rewiring_method(G_copy, copy=False)
            if j > burn_in:
                property_list[i] = property(G_copy)
        
        
    return property_list