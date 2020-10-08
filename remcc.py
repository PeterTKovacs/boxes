import networkx as nx

def remcc(network,rb,return_centres=True):
    
#implementation of the REMCC algorithm
    
    if rb==0:
        return [[node] for node in network.graph.nodes()]
    else:
        
        uncovered=set(network.graph.nodes())
        centres=set()
        
        # if weigthing is needed on the edges later, here shall be implemented
        
        if not network.distance_dict:
            print('computing shortest path data') # both distance_dict and shortest_paths
            network.get_dist_dict()
            
        n=network.graph.number_of_nodes()    
            
        # computing 'closeness centrality' which is in fact the inverse of the average of shortest distances
        
        closeness={}
        
        for node in network.graph.nodes():
            
            sum_distance=0
            
            for neighbour in network.shortest_paths[node].keys(): # self-shortest-path is 0
                sum_distance+=network.shortest_paths[node][neighbour]
            
            if sum_distance>0:
                closeness[node]=(n-1)/sum_distance
            else:
                closeness[node]=1
                print('invalid closeness')
            
            
        while uncovered:
            
            # in every step, we calulate the f_point for uncovered nodes, which determines the next center
            
            max_f_point=0 # this is used instead of excluded mass for the determination of the new center
            p_node=0 # as an uncovered itself counts in its ex. mass, it's not possible to have max_f_point=0
            
            for node in uncovered:
                
                ex_mass=len(uncovered.intersection(network.ball_of_seed(node,rb)))
                f_point=ex_mass/closeness[node]
                
                if f_point>max_f_point:
                    max_f_point=f_point
                    p_node=node
              
            uncovered -= network.ball_of_seed(p_node,rb)
            centres.add(p_node)
            
        # now, we do not propose a boxing scheme, as no is present in the paper
        # e.g. the MEMB could be used for connected boxes, or a greedy approach
        
        if return_centres:
            return centres
        else:
            return len(centres)
            
            