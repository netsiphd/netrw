from matplotlib import pyplot
import networkx
import netrd



def distanceTrajectory(G, distance=..., rewire=..., null_model=None, 
    num_rewire=100, num_networks=100, distance_kwargs={}, rewire_kwargs={}, 
    null_model_kwargs={}, **kwargs):

    G0 = copy.deepcopy(G)
    
    if hasattr(num_rewire, "__iter__"):
        rewire_steps = num_rewire
    else:
        rewire_steps = range(num_rewire)
        
    data = np.zeros(len(rewire_steps))
    
    for i, r in enumerate(rewire_steps):
       rewire(G0, **rewire_kwargs)
       data[i] = distance(G0, G, **distance_kwargs)

    return data

def plotDistanceTrajectory(G, **kwargs):
    
    data = distanceTrajectory(G, kwargs**)
    
    