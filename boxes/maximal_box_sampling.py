import random
import networkx as nx

def maximal_box_sampling(network, lb, n):

    uncovered=set(network.graph.nodes())
    
    if len(uncovered)==0:
        return 0
    
    if network.distance_dict==None:
                print('computation of shortest path data')
                network.get_dist_dict()
    
    proposals=[]
    nodes=list(network.graph.nodes())
    
    for i in range(n):
        
        if len(uncovered)>0:
            seed=random.choice(list(uncovered))
        else:
            seed=random.choice(nodes)
        
        # make a new box proposal around seed
        
        candidates=network.ball_of_seed(seed,lb)
        candidates.discard(seed)
        
        box=set([seed])
        
        while len(candidates)>0:
            new=random.choice(list(candidates))
            box.add(new)
            candidates.discard(new)
            
            candidates=candidates.intersection(network.ball_of_seed(new,lb))
        
        proposals.append(box)
        
        uncovered=uncovered-box
        
    return proposals
        