# This script contains the implementation of the network class of the boxing package.
# It is used to store information on the investigated graph and to some basic processing on it.

# The class is built upon the 'networkx' package to some extent.

import networkx as nx
import sys

class network:

    def __init__(self, graph):
        
        # initialization with type(graph) = networkx.classes.graph.Graph
        self.graph = nx.convert_node_labels_to_integers(graph, first_label=0)
        
        self.dd = None  # distance matrix
        self.shortest_paths = None  # length of shortest path between any pair of nodes
        self.distance_dict=None     # {node:{distance:set_of_nodes}} type dictionary - produced by self.get_dist_dict
        self.connected=nx.is_connected(self.graph)
        self.diameter=sys.maxsize
        
        if self.connected:
            self.diameter = nx.diameter(self.graph)  # igraph diameter is faster
        else:
            print('unconnected graph')

    def get_dist_dict(self):
        
        # purpose: {node:{distance:set_of_nodes}} type dictionary
        # also: sets self.shortest_paths
        
        graph = self.graph
        if not self.shortest_paths:
            
            # returns dicts in dict
            # for every node as a key, we have a dict with the node:min_dist pairs
            
            self.shortest_paths = dict(nx.all_pairs_shortest_path_length(graph)) 
            
            
        distances = self.shortest_paths

        def invert_dict_set(d): # processing the node_id:min_dist type dicts 
            new_dict = {}
            for k, v in d.items():
                new_dict.setdefault(v, set()).add(k) #creating dist:set_of_nodes dictionary
                                        #setdefault returns the appropriate set or an empty if the key is valid
            return new_dict

        dist_dict = {k: invert_dict_set(v) for k, v in distances.items()}
        self.distance_dict=dist_dict
        
        if not self.connected: # find the longest geodesic inside connected components
            m=0 
            
            for node in self.distance_dict.keys():
                for dist in self.distance_dict[node].keys():
                    if dist>m:
                        m=dist
                        
            self.diameter=m # we will need this in the evaluation of Nb(lb) function
        
        return 'self.shortest_paths, self.distance_dict set successfully'

    @staticmethod
    def invert_dict_list(dictionary):
        new_dict = {}
        for k, v in dictionary.items():
            new_dict.setdefault(v, []).append(k)
        return new_dict

   
     
# Rewritten: uses self.distance_dict instead of self.shortest_paths

    def ball_of_seed(self,seed, rb):
        
        if not self.distance_dict:
            self.get_dist_dict()
        
        ball = set()
        dist=0
        while dist<=rb:
            
            if (dist in self.distance_dict[seed].keys()): # not testing caused errors: fixed 2020.09.12.
                ball.update(self.distance_dict[seed][dist]) #Update the set, adding elements from all others
                
            dist+=1
        return ball
    
    
    def dual_network(self, lb):
        # It only works for connected graphs
        # (because len(dd) otherwise we should iterate over its items instead of indices)

#         Generating the shortest path dictionary if not already present
        
        if not self.distance_dict:
            print('computation of shortest path data')
            self.get_dist_dict()
            
        dd_nx = self.distance_dict
        graph = self.graph
        dual_graph = nx.empty_graph(graph.number_of_nodes())

#         Idea: for every node, we leverage the dist_dict structure to get the nodes farther than lb-1???
#         What definition/convention do we use?
        
        for n in graph.nodes(): # tries to add every dual egde twice
            
            for i in range(lb+1, len(dd_nx[n])): #key for the distance, note that distance goes like 0,1,2,....,n
                for nd in dd_nx[n][i]:
                    dual_graph.add_edge(n, nd)
        return dual_graph



