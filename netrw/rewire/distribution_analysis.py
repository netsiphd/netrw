import numpy as np
import networkx as nx

def logbin_dist(z,bins=15):
    """
    Logbin a collection of datapoints to estimate a function
    
    Parameters:
        x - xvalues of data
        y - f(x)
        bins - number of bins
        
    Returns:
        log_bin_data
    """
    # Get first and last psi and b
    psi = np.zeros(bins+1)
    b = np.zeros(bins+1)
    b[0] = np.min(z)
    b[-1] = np.max(z)
    psi[0] = np.log(b[0])
    psi[-1] = np.log(b[-1])
    # Get size of psis and interval sizes
    D = psi[-1] - psi[0]
    L = D/bins
    
    # Get updated psi and b
    for i in range(1,bins):
        # Find psi
        psi[i] = psi[i-1] + L
        b[i] = np.exp(psi[i])

    # Create binned data arrays
    x_bin = np.sqrt(b[:-1]*b[1:])
    z_bin = np.zeros(bins)
    
    # Sort data
    z_sort = np.argsort(z)
    z = z[z_sort]
    
    n = len(z)
    
    # Get average of bins
    for i in range(bins-1):
        
        # Get data in bin
        loc_in_bin = np.where(z[np.where(z < b[i+1])[0]]  >= b[i])[0]
        S = len(loc_in_bin)
        L = b[i+1]-b[i]
        z_bin[i] = S/(L*n)
    
    loc_in_bin = np.where(z>=b[-2])[0]
    S = len(loc_in_bin)
    L = b[-1] - b[-2]
    z_bin[-1] = S/(L*n)
    
    return x_bin, z_bin

def graph_distributions(G,bins=15,degree_dist=True,avg_nn_dist=True,dd_clustering=True):
    """
    Build the degree distribution, average nearest neighbor degree
    and degree-dependent clustering of a graph.
    
    Parameters:
        G (networkx) - network
        bins (int) - number of bins
        degree_dist (bool) - create degree distribution
        avg_nn_dist (bool) - create average nearest-neighbor degree distribution
        dd_clustering (bool) - create degree-dependent clustering
    
    Returns:
        deg_dist_bins (ndarray) - bins for degree dist
        deg_dist_vals (ndarray) - y-values for degree dist
        avg_nn_bins (ndarray) - bins for avg_nn
        avg_nn_vals (ndarray) - y-values for avg_nn
        dd_cluster_bins (ndarray) - bins for dd_clustering
        dd_cluster_vals (ndarray) - y-values for dd_clustering
    """
    # Get degree sequence
    degree_sequence = np.array([d for n, d in G.degree()])
    nodes_by_deg = {d: np.where(degree_sequence==d)[0] for d in np.sort(np.unique(degree_sequence))}
    # Get minimum and maximum degree
    min_deg = np.min(degree_sequence)
    max_deg = np.max(degree_sequence)
    to_ret = []
    
    # Create degree distribution
    if degree_dist:
        deg_dist_bins, deg_dist_vals = logbin_dist(degree_sequence,bins = bins)
        to_ret.append(degree_sequence)
        to_ret.append(deg_dist_bins)
        to_ret.append(deg_dist_vals)
    
    # Create average nearest neighbor degree distribution
    if avg_nn_dist:
        # Create distribution
        avg_nn = np.zeros_like(np.unique(degree_sequence))
        neighbor_degrees = np.array(list(nx.average_neighbor_degree(G).values()))
        for i, d in enumerate(np.sort(np.unique(degree_sequence))):
            node_idx = nodes_by_deg[d]
            avg_nn[i] = np.mean(neighbor_degrees[node_idx])

        # Get log bin
        avg_nn_bins, avg_nn_vals = logbin_fxn(np.sort(np.unique(degree_sequence)),avg_nn,bins = bins)
        to_ret.append(avg_nn)
        to_ret.append(avg_nn_bins)
        to_ret.append(avg_nn_vals)
        
    # Create clustering by degree
    if dd_clustering:
        # Create distribution
        dd_cluster = []
        cluster_degrees = np.array(list(nx.cluster.clustering(g).values()))
        for i,d in enumerate(np.sort(np.unique(degree_sequence))):
            node_idx = nodes_by_deg[d]
            if len(node_idx) > 1:
                dd_cluster.append(float(np.mean(cluster_degrees[node_idx])))
            else:
                dd_cluster.append(float(cluster_degrees[node_idx]))
        dd_cluster = np.array(dd_cluster)
        # Get log binning
        dd_cluster_bins, dd_cluster_vals = logbin_fxn(np.sort(np.unique(degree_sequence)),dd_cluster,bins=bins)
        to_ret.append(dd_cluster)
        to_ret.append(dd_cluster_bins)
        to_ret.append(dd_cluster_vals)
    
    return tuple(to_ret)