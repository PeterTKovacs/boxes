import random
import networkx as nx
    
def mcwr(network, rb,p=1, boxing=False):
        # "How to calculate the fractal dimension of a complex network: the box covering algorithm"
        # by Chaoming Song et al

        graph = network.graph
        
        if rb == 0:
            boxes = [[node] for node in graph.nodes()]
        else:
            if not network.distance_dict:
                print('computing shortest path data')
                network.get_dist_dict()
                
            distances = network.distance_dict # {node:{distance:set_of_nodes}}
            
            if not network.shortest_paths:
                print('computing shortest path data')
                network.shortest_paths = dict(nx.all_pairs_shortest_path_length(graph)) 
            
            distance_dictionary = network.shortest_paths # {node1:{node2:dist12}}

            # (i) Initially,  all  the  nodes  are  marked  as  uncovered  and  non-centers
            uncovered = set(graph.nodes())
            non_center = set(graph.nodes())

            centers = set()
            unc_or_non_center = set(graph.nodes())
            c_dist = {}  # "central distance"
            c_id = {}  # box id's
            
            
#   Modification1: initialize m_excluded for all

        # For a given radus rb, we define the excluded mass of a node as the number of uncovered nodes
        # within a chemical distance less than rB 
            
            excluded_mass = {}  # dictionary of nodes excluded mass
        
            for node in graph.nodes():
                excluded_mass[node] = len(network.ball_of_seed(node, rb)) # ball contains node too, no one is covered yet

#   first part: choosing centers in the randomized way
            
            # (Repeat until  all  nodes  are  either  covered  or  centers. [ambiguity again]
            
            while unc_or_non_center: # 'and' would be better, wouldn't it? :) ; every center is covered -> THIS IS uncovered
                # if there were no ambiguity in unc_..., this could cause problems
                # but we are saved due to the fact that centers are covered too, opposed to the paper
                
#   Choosing a new center either MEMB or RS way        
                
                if random.random()<p: # the MEMB branch
                
                    max_excluded_mass = 0
                    p_node = 0
                
                    for node in non_center:
                    
                        if excluded_mass[node] > max_excluded_mass:
                            max_excluded_mass = excluded_mass[node]
                            p_node = node
                            
                else: # the RS branch
                    
                    p_node=random.choice(list(non_center)) # avoid choosing centers that are to be discarded
                    
                    while len(network.ball_of_seed(p_node, rb).intersection(uncovered))==0: # p_node must be discarded
                        p_node=random.choice(list(non_center))
                    
#   updating the excluded masses, after finding p_node
            
                for newly_covered in network.ball_of_seed(p_node, rb).intersection(uncovered):
                    for neighbour in network.ball_of_seed(newly_covered,rb):
                        
                        excluded_mass[neighbour]-=1 # decrements its own mass too
                    
#   Administration of changes   
    
                centers.add(p_node)
                non_center -= {p_node}
                uncovered -= network.ball_of_seed(p_node, rb)
                unc_or_non_center = uncovered.intersection(non_center) # ambiguity, every center is covered -> this is uncovered
                c_dist[p_node] = 0
                c_id[p_node] = p_node
                

                
# After everyone is covered, we sort non-center nodes to some approporiate center  (original MEMB code)        
            
    # find the nearest-center distance
    
            for non_center_node in non_center:
                radius = 1
                while non_center_node not in c_dist:
                    if distances[non_center_node][radius].intersection(centers): #there is a center in radius distance 
                        c_dist[non_center_node] = radius
                    radius += 1
                    
            sorted_non_center = sorted(list(non_center), key=lambda x: c_dist[x]) 
            
    # in every iteration, one node is sorted to a center
    
            for node in sorted_non_center:
            
                neighbours = list(graph.neighbors(node)) # centers are included too
                random.shuffle(neighbours)
                
                for neigh in neighbours:
                    if c_dist[neigh] < c_dist[node]: # equivalent to c_dist[neigh]==c_dist[node]-1
                        
    # as we iterate over sorted_non_center, neigh is sorted to a center if this point is reached
    
                        c_id[node] = c_id[neigh]
                        break
            
            boxes = list(network.invert_dict_list(c_id).values()) # yields list of values of {c_id:list_of_nodes}

        if boxing:
            return len(boxes)
        else:
            return boxes
