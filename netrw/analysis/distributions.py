from copy import deepcopy
import numpy as np

def get_property_distribution(G, rewiring_method, property, burn_in=100, num_samples=1000):
    G = deepcopy(G)
    property_list = np.zeros(num_samples)
    for i in range(num_samples):
        for j in range(burn_in):
            rewiring_method(G)
            if j >= burn_in - 1:
                property_list[i] = property(G)

    return property_list

def get_property_distribution_choosing_chaos(G, rewiring_method, property, burn_in=100, num_samples=1000):
    G = deepcopy(G)
    rw = rewiring_method()
    property_list = np.zeros(num_samples)
    for i in range(num_samples):
        for j in range(burn_in):
            G = rw.rewire(G, copy_graph=False)
            if j >= burn_in - 1:
                property_list[i] = property(G)

    return property_list