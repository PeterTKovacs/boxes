from .merge_algorithm import merge_algorithm
from .merge_if_possible import merge_if_possible
import copy
import random
import math
import networkx as nx

def simulated_annealing(network, lb, k1=20, k2=2, k3=15, temp=0.6, cc=0.995):
    
    # "Three  Algorithms  for  Analyzing  Fractal  Software  Networks"
    # by Mario Locci et al
    # Simulated Annealing (SA)
    
    graph = network.graph
    
    if not network.shortest_paths:
        network.shortest_paths = dict(nx.all_pairs_shortest_path_length(graph))
    shortest_paths = network.shortest_paths
    
    # TODO: kell boxing parameter. Ha true, akkor itt s_all = merge_algorithm(boxing=True) visszadja az összes lb-re
    # a dobozolást, és s = s_all[lb] ezzel némi időt spórolhatunk. Ehhez át kell kicsit írni a merge algoritmust
    
    s = merge_algorithm(network,lb, return_for_sa=True) # list of clusters as sets
    
    if lb == 0:
        return s
    else:
        for j in range(k3): # the cycle for temperature manipulation
            
            s2 = copy.deepcopy(s)  # S' 

# try to move k1 nodes
            
            i = 0 # number of successful movements
            max_trials = 2*k1  # if the movement is not possible, then
            trial = 0
            
            while i < k1 and trial < max_trials:
                trial += 1
                
                box_b = random.choice(s2)
                
                adj = set()
                for n in box_b:
                    adj = adj.union(set(graph.neighbors(n)))
                adj = adj - box_b # neighbours that are not in box_b? - candidates for movement to 

                for node_a in adj:
                    movable = True
                    
                    for n in box_b:
                        if shortest_paths[node_a][n] > lb:
                            movable = False
                            break
                    if not movable:
                        continue # to the next candidate in adj
                        
           # this part is executed when a is movable: moving a
                    
                    box_a = set()  # box_a is the box of node_a
                                   
                    for c in s2: # already existing clusters
                        if node_a in c:
                            box_a = c
                            break
                    if len(box_a) < 2: # single node in the cluster
                        continue # to the next candidate in adj
                    else:
                        box_a.discard(node_a) #alias!
                        box_b.add(node_a)
                        i += 1 #successful churn
                        break # and throw away the remaining candidates
            
# try to create k2 clusters - 'k2 trials': maximum k2 new clusters: AMENDED

            i = 0
            while i < k2:
                box_a = random.choice(s2)
                
                while len(box_a) < 2:  # runs until len(box_a)>1
                    box_a = random.choice(s2)
                    i += 1
                    
                if i >= k2:
                    break
                
            #executes if i<k2
                
                n = random.choice(list(box_a)) 
                box_a.discard(n)
                s2.append({n})
                
                i+=1 # ORIGINALLY ABSENT, this is needed not to exceed k2


            
# if E(S') <= E(S) ...

            if len(s2) <= len(s) or random.random() < math.exp(-(len(s2) - len(s)) / temp):
                s = s2
            temp = cc * temp
            
# Merge clusters using MA algorithm: AMENDED - in the paper, it is placed here but originally it was just before the E test 

            s = merge_if_possible(s, lb, shortest_paths)

    return list(map(list, s))