from matplotlib import pyplot
import networkx
import netrd

def distanceTrajectory(G, distance=netrd.distance.Hamming, rewire=netrw.rewire.KarrerRewirer, null_model=None, 
    num_steps=100, num_runs=100, distance_kwargs={}, rewire_kwargs={}, 
    null_model_kwargs={}, **kwargs):
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
    if hasattr(num_rewire, "__iter__"):
        rewire_steps = num_rewire
    else:
        rewire_steps = range(num_rewire)
        
    # initialize data array
    data = np.zeros(len(rewire_steps))    
    
    # define a rewire function
    step_rewire = rewire().step
    rewire_function = lambda g : step_rewire(g, copy_graph=False, **rewire_kwargs)
    
    # define a distance function
    distfun = distance() # get a class instantiation
    distance_function = lambda g1, g2: distfun(g1, g2, **distance_kwargs)
    
    for i in range(max(rewire_steps)):
       rewire_function(G0)
       data[i+1] = distance(G0, G)

    return data


def plotDistanceTrajectory(G, num_rewire=100, **kwargs):
        
    # check whether input for num rewire in a number of rewiring steps (int)
    # or a list of steps
    if hasattr(num_rewire, "__iter__"):
        rewire_steps = num_rewire
    else:
        rewire_steps = range(num_rewire)

    data = distanceTrajectory(G, num_rewire=num_rewire, **kwargs)
    
    
    mean = np.mean(data, axis=1)
    std = np.std(data, axis=1)
    
    plt.fill_between(rewire_steps, mean-std, mean+std)
    plt.plot(rewire_steps, mean)
    
    
    
    
    