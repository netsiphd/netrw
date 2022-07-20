from .base import BaseRewirer
import copy
import random
import networkx as nx
import numpy as np

class PreferentialRewirer(BaseRewirer):
    """Selected nodes rewire based on their preference to connect to other nodes in the network. Preferences
    are tracked via the node attribute 'preference_weights'. This is a vector of raw weights associated with each 
    node in the network, and new outgoing links are selected at random proportional to these weights. If the nodes
    of the passed graph object do not contain a 'preference_weights' attribute, this attribute is added with 
    uniform weights that exclude the possiblity of self-loops. This function is intended to allow for users to
    specify and update their 'preference_weights' in any manner external to this function assuming sychronus 
    preference updating. This function is also degree perserving, so users should specify their desired degree 
    sequence in the input graph. Finally, the input graph must be directed as outgoing links represent the 
    focal node's preferential link formation.
    
    Inputs:
    -error_rate: this is the liklihood that a selected node makes an error and rewires all new links uniformly at 
    random excluding self-loops
    -multiedges: specifies if multiedges can form, if true new links are selected with replacement, if false new 
    links are selected without replacement. If true graph input is required to be a multigraph object.
    -copy_graph: if true deepcoopy of graph object is created for rewiring
    -verbose: if true dictionary objects tracking deleted and new edges at each iteration are created
    
    For example of preferential interaction see:
    Z. Fulker, P. Forber, R. Smead, C. Riedl, Spite is contageous in dynamic networks. Nat Commun 12 (2021).
    """
    #every agent selcts new partners
    def full_rewire(self, G, error_rate=0, multiedges=False, copy_graph=True, verbose=True):

        if copy_graph:
            G = copy.deepcopy(G)

        #G must be multigraph if multiedges=True   
        if multiedges:
            if not G.is_multigraph():
                raise Exception('Must pass multigraph to enable multiedges=True')
        #G must be directed
        if not G.is_directed():
            raise Exception('Must pass directed graph')

        num_nodes = G.number_of_nodes()
        new_edges = []
        edges_to_remove = []

        removed_edges = {}
        added_edges = {}

        for node in G.nodes(data=True):
            #determine if node makes a partner selction error
            selection_error = random.uniform(0, 1) < error_rate

            #get current node and its raw preference weights
            cur_node = node[0]

            #check if node has required attributes
            try:
                cur_preferences = node[1]['preference_weights']
            #create intitial raw weights if none given
            except:
                cur_preferences = [5]*num_nodes
                cur_preferences[cur_node] = 0
                nx.set_node_attributes(G, {cur_node:cur_preferences}, 'preference_weights')

            #delete this nodes current edges
            edges_to_remove.extend(list(G.edges(cur_node)))
            num_new_edges = len(list(G.edges(cur_node)))

            #convert raw weights to probabilities
            total_weight = sum(cur_preferences)
            normalized_cur_preferenes = [x/total_weight for x in cur_preferences]

            #select specified number of partners with or without replacement
            if multiedges:
                if not selection_error:
                    partner_choices = np.random.choice(range(num_nodes),num_new_edges,replace=True, p=normalized_cur_preferenes)
                else:
                    #prevent self-links
                    node_options = list(range(num_nodes))
                    node_options.pop(cur_node)
                    partner_choices = np.random.choice(node_options,num_new_edges,replace=True)
            else:
                if not selection_error:
                    partner_choices = np.random.choice(range(num_nodes),num_new_edges,replace=False, p=normalized_cur_preferenes)
                else:
                    #prevent self-links
                    node_options = list(range(num_nodes))
                    node_options.pop(cur_node)
                    partner_choices = np.random.choice(node_options,num_new_edges,replace=False)

            #add newly created edges to new edge list
            for partner in partner_choices:
                new_edges.append((cur_node, partner))

        G.remove_edges_from(edges_to_remove)
        G.add_edges_from(new_edges)

        removed_edges[0] = edges_to_remove
        added_edges[0] = new_edges

        if verbose:
            return G, removed_edges, added_edges
        else:  
            return G
    
    #selects one agent at random at each timestep to rewire their links
    def step_rewire(self, G, error_rate=0, multiedges=False, copy_graph=False, timesteps=1, verbose=True):

        if copy_graph:
            G = copy.deepcopy(G)

        #G must be multigraph if multiedges=True   
        if multiedges:
            if not G.is_multigraph():
                raise Exception('Must pass multigraph to enable multiedges=True')

        #G must be directed
        if not G.is_directed():
            raise Exception('Must pass directed graph')

        num_nodes = G.number_of_nodes()

        removed_edges = {}
        added_edges = {}

        for time in range(timesteps):
            new_edges = []

            #pick node at random to update
            node = random.choice(list(G.nodes(data=True)))

            #determine if node makes a partner selction error
            selection_error = random.uniform(0, 1) < error_rate

            #get current node and its raw preference weights
            cur_node = node[0]

            #check if node has required attributes
            try:
                cur_preferences = node[1]['preference_weights']
            #create intitial uniform raw weights with no self-loops if none given
            except:
                cur_preferences = [5]*num_nodes
                cur_preferences[cur_node] = 0
                nx.set_node_attributes(G, {cur_node:cur_preferences}, 'preference_weights')

            #delete this nodes current edges
            edges_to_remove = list(G.edges(cur_node))
            num_new_edges = len(list(G.edges(cur_node)))
            G.remove_edges_from(edges_to_remove)

            #convert raw weights to probabilities
            total_weight = sum(cur_preferences)
            normalized_cur_preferenes = [x/total_weight for x in cur_preferences]

            #select specified number of partners with or without replacement
            if multiedges:
                if not selection_error:
                    partner_choices = np.random.choice(range(num_nodes),num_new_edges,replace=True, p=normalized_cur_preferenes)
                else:
                    #prevent self-links
                    node_options = list(range(num_nodes))
                    node_options.pop(cur_node)
                    partner_choices = np.random.choice(node_options,num_new_edges,replace=True)
            else:
                if not selection_error:
                    partner_choices = np.random.choice(range(num_nodes),num_new_edges,replace=False, p=normalized_cur_preferenes)
                else:
                    #prevent self-links
                    node_options = list(range(num_nodes))
                    node_options.pop(cur_node)
                    partner_choices = np.random.choice(node_options,num_new_edges,replace=False)

            #add newly created edges to new edge list
            for partner in partner_choices:
                new_edges.append((cur_node, partner))

            G.add_edges_from(new_edges)

            removed_edges[time] = edges_to_remove
            added_edges[time] = new_edges

        if verbose:
            return G, removed_edges, added_edges
        else:  
            return G