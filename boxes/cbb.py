import random

def cbb(network, lb, boxing=False):

        graph = network.graph

        # collects nodes that are farther than k_cutoff from source
       
        def far_away_nodes(distance_dictionary, source, k_cutoff):
            
            k_fa = set([])
            
            for k in range(k_cutoff + 1, max(distance_dictionary[source].keys()) + 1):
                k_fa = k_fa.union(distance_dictionary[source][k])
            
            return k_fa

        boxes = []

        if lb == 0:
            boxes = [[node] for node in graph.nodes()]
        elif lb == network.diameter:
            boxes = [list(graph.nodes())]
        else:
            if not network.distance_dict:
                print('computing shortest path data')
                network.get_dist_dict()

            distances = network.distance_dict

            uncovered_nodes = set(graph.nodes())

            while len(uncovered_nodes) > 0:
                candidate_set = uncovered_nodes.copy() # set of nodes that are compatible with all in the box
                box = set() # modified from list
                while len(candidate_set) > 0:
                    
                    #new member of the box - valid
                    p = random.choice(list(candidate_set))
                    candidate_set.discard(p)
                    box.add(p)
                    
                   # remove the ones incompatible with the newly chosen: result is again compatible with all in the box
                    candidate_set = candidate_set - far_away_nodes(distances, p, lb) 
                
                boxes.append(box)
                uncovered_nodes = uncovered_nodes - box
        if boxing:
            return len(boxes)
        else:
            return boxes