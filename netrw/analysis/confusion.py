import numpy as np

def rewiring_distance_confusion_matrix(G, rewiring_methods, distance_measures, timesteps=100, ensemble_size=10):
    """Plotting distances from start graph for different rewiring schemes and distance metrics

    Parameters
    ----------
    G : NetworkX Graph
        The starting graph
    rewiring_methods : list of Rewiring classes in the rewiring module.
        methods for rewiring graphs. each class specified must have a
        `full_rewire` method and that method must have `timesteps` as
        a keyword argument.
    distance_measures : netrd Distance
        metric for measuring the distance between the before and after graphs
    timesteps : int, default: 100
        the number of iterations 
    ensemble_size : int, default: 10
        the number of rewiring trajectories to run.

    Returns
    -------
    numpy matrix
        a matrix where rows are rewiring methods, columns are distance metrics
        and entries are average distances.

    Notes
    -----
    Currently this method does not support keyword args for the rewiring methods
    and distance metrics.
    """
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