import numpy as np

def dist_confusion_thang(G, rewiring_methods, distance_measures, timesteps=100, ensemble_size=10):
    n = len(rewiring_methods)
    m = len(distance_measures)
    C = np.zeros([n, m])
    for i in range(n):
        rw = rewiring_methods[i]()
        for j in range(m):
            dist = distance_measures[i]()
            for k in range(ensemble_size):
                rG = rw.full_rewire(G, timesteps=timesteps)
                C[i, j] += dist(rG, G)/ensemble_size
    return C