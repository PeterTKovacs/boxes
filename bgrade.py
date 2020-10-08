import itertools

def bgrade(network,center):
    
    if network.distance_dict==None:
        network.get_distance_dict()
    
    bgrade=0
    bottleneck=True
    i=1
    
    while bottleneck:
        
        if not (i in network.distance_dict[center].keys()): # no more nodes
            bottleneck=False
            bgrade=i-1
        elif len(network.distance_dict[center][i])==1: # only one - terminate! [not considered bottlenenck for i] 
            bottleneck=False
            bgrade=i-1
        else:
            ri_nodes=network.distance_dict[center][i]
            
            bottleneck=False
            
            for pair in itertools.combinations(ri_nodes,2):
                
                if network.shortest_paths[pair[0]][pair[1]]==2*i:
                    bottleneck=True
                    break
                    
            if bottleneck:
                i+=1
            else:
                bgrade=i-1
    
    return bgrade