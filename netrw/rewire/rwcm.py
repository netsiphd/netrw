from . import BaseRewirer
import copy
import itertools as it
import random
import networkx as nx
import numpy as np


class rwcm(BaseRewirer):
    
    def weigth_swap(G, copy_graph=True):
        if copy_graph:
            G=copy.deepcopy(G)

        e_list=list(G.edges(data=True))
        e_1=random.choice(e_list)
        e_list.remove(e_1)
        e_2=random.choice(e_list)

        print(e_1)
        print(e_2)

        w_1=e_1[2]['weight']
        w_2=e_2[2]['weight']

        G.edges[e_1[0],e_1[1]]['weight']=w_2
        G.edges[e_2[0],e_2[1]]['weight']=w_1

        return G
    
    def redistribute_weight(G, copy_graph=True):
        if copy_graph:
            G=copy.deepcopy(G)

        e_list=list(G.edges(data=True))
        e_1=random.choice(e_list)
        e_list.remove(e_1)
        e_2=random.choice(e_list)

        print(e_1)
        print(e_2)

        a_1=random.random()
        print(a_1)

        w_sum=e_1[2]['weight']+e_2[2]['weight']

        G.edges[e_1[0],e_1[1]]['weight']=a_1*w_sum
        G.edges[e_2[0],e_2[1]]['weight']=(1-a_1)*w_sum

        return G  
    
    def original_rwcm(G, copy_graph=True):
        if copy_graph:
            G=copy.deepcopy(G)

        alphas=np.random.rand(len(G.edges()))
        alphas=alphas/np.sum(alphas)

        w = [x[2]['weight'] for x in list(G.edges(data=True))]
        w_sum=np.sum(w)
        aw=alphas*w_sum

        e_list=list(G.edges())
        nx.set_edge_attributes(G,dict(zip(e_list,aw)),'weight')

        print(aw)
        return G    