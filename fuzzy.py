import networkx as nx
import math

def fuzzy(network, lb, boxing=True):
    # Fuzzy fractal dimension of complex networks

    graph = network.graph

    num_of_nodes = graph.number_of_nodes()
    
    if lb==0:
        return num_of_nodes
    elif num_of_nodes==1:
        return 1
    
    if not network.shortest_paths:
        network.shortest_paths = dict(nx.all_pairs_shortest_path_length(graph))
    dist_dict = network.shortest_paths

    nb_inv = 0
    
    for i in range(num_of_nodes): # again leveraged that node labels are nonnegative integers
        for j in range(i+1, num_of_nodes):

            if dist_dict[i].get(j): # guess its not needed because we only do connected subgraphs
                d = dist_dict[i][j]
            else:
                continue
                
            if d <= lb:
                nb_inv+=2*math.exp(-(d ** 2 / lb ** 2)) # both d_ij and d_ji taken into account
                
                
    nb_inv = nb_inv / (num_of_nodes * (num_of_nodes - 1))
    
    if boxing:
        if nb_inv>0:
            return 1/nb_inv
        else:
            raise ValueError('nb_inv not positive!')
    else:
        raise ValueError('Fuzzy algorithm cannot create actual boxes')
