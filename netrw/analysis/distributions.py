from copy import deepcopy
import numpy as np

def get_property_distribution(G, rewiring_method, property, skip=10, num_samples=1000):
    G = deepcopy(G)
    rw = rewiring_method()
    properties = np.zeros(num_samples)
    for i in range(num_samples):
        for j in range(skip):
            G = rw.rewire(G, copy_graph=False)
            if j >= skip - 1:
                properties[i] = property(G)
        print(i)
    return properties