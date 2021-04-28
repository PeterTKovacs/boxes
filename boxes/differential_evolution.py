import random
import numpy as np
import itertools

def differential_evolution(network, lb, num_p=15, big_f=0.9, cr=0.85, gn=15, boxing=False,dual_new=False):
    
    # "A  Differential  Evolution  Box-covering  Algorithm  forFractal  Dimension  on  Complex  Networks"
    # by Li Kuang et al

    # NP >= 4 number of parameter vectors (population size)
    # 0 < F <= 2  constant factor: controls the amplification of the differential variation (Mutation step)
    # 0 <= CR <= 1 crossover probability
    # GN: generation number

    #TODO: át kell nézni, nagyon sokáig fut

# auxiliary function for R^N -> ordering of nodes
    
    def get_node_order(l):
        return [t[1] for t in sorted([(item, index) for index, item in enumerate(l)])]  # returns indices ordered by the values

# sequential greedy coloring, original (slow) version
    # implements greedy coloring: the sequence of nodes is given in nodes
    # the smallest possible color ID is assigned to each node

    def greedy_d_e(nodes):
        
        colors = {}
        for node in nodes:
            
            # Set to keep track of colors of neighbours (that are already colored)
            neighbour_colors = {colors[neigh] for neigh in dual_graph[node] if neigh in colors} #set
            # Find the first unused color.
            color = None
            
            for color in itertools.count():
                if color not in neighbour_colors:
                    break
                    
            # Assign the new color to the current node. (smallest color ID possible)
            colors[node] = color

        boxes = []

        inverted_colors = network.invert_dict_list(colors) # {color:[nodes]} type dictionary
        
        for box in inverted_colors.keys(): #range(len(inverted_colors)):, here color_i == box_i
            boxes.append(inverted_colors[box])

        return len(boxes), boxes
    
# faster version of greedy coloring
    # idea: store dual graph as a dicitionary with set values (hashing: intersection is relatively cheap)
    # thus we omit iterating over all neighbours (uncolored ones too)

    def greedy_d_e_new(nodes):
        
        colors = {0:set()}
        max_color=0
        
        for node in nodes:
            color=0
            while color<=max_color:
                
                if len(dual_neighbours[node].intersection(colors[color]))==0: # no neighbor with color: use this
                    colors[color].add(node)
                    break
                    
                color+=1
                
            if color>max_color: # all colors are exhausted with neighbours
                colors[max_color+1]={node}
                max_color+=1
        
        return max_color+1, [list(colors[c]) for c in colors.keys()] # same format as in the slow version

# initialization   

    graph = network.graph
    
# Find  the  dual  network: way depends on what's desired

    if not dual_new:
    
        dual_graph = network.dual_network(lb)
    else:
    
        if not network.distance_dict:
            print('computing shortest path data')
            network.get_dist_dict()

        dual_neighbours={}
    
        for node in graph.nodes():
            dual_neighbours[node]=set(graph.nodes())-network.ball_of_seed(node,lb)
        
    
    

# Randomly  initialize X. G x NP x NumNodes

    big_x = [[[random.random() for _ in graph.nodes()] for _ in range(num_p)]] #triple list: [gen][instance][node_val]

    best = [graph.number_of_nodes(), list(graph.nodes())] # lb=0 guess

    for y in range(gn):
        
        v = [] # will contain the mutated vectors
        
        # 5. The Mutation phase
        
        for i in range(num_p): # the instance to mutate
            r1 = random.randint(0, num_p - 1) # random choice more effectively? r1, r2, r3 = np.random.choice(range(num_p), size=3, replace=False)
            r2 = random.randint(0, num_p - 1)
            r3 = random.randint(0, num_p - 1)
            while i == r1 or i == r2 or i == r3 or r1 == r2 or r1 == r3 or r2 == r3: # itself or not mutually different
                r1 = random.randint(0, num_p - 1)
                r2 = random.randint(0, num_p - 1)
                r3 = random.randint(0, num_p - 1)
            x1 = np.array(big_x[-1][r1]) # from the last generation
            x2 = np.array(big_x[-1][r2])
            x3 = np.array(big_x[-1][r3])
            v.append(x1 + big_f * (x2 - x3)) # np array, so OK

        big_u = [] # contains instances after the crossover
        
        # 9. The Crossover phase
        
        for i in range(num_p):
            
            u = [] # contains the i-th crossover outcome
            mutated_j=random.randint(0, graph.number_of_nodes()-1) # makes sure one is mutated at least
            
            for j in range(graph.number_of_nodes()): # shall we accept i instance's mutation wrt. the j-th node? 
                if random.random() < cr or j == mutated_j: # originally got the role of mutated_j wrong!
                    u.append(v[i][j])
                else:
                    u.append(big_x[-1][i][j])
            big_u.append(u) 

# now for the verdict on the crossover results            
            
        x = [] # will contain the evolved set of instances
        for i in range(num_p):
            
            # 13. Calculate the fitness of each individual Fdebc(X_i) by greedy oloring algorithm
            
            if dual_new:
                
                f1 = greedy_d_e_new(get_node_order(big_u[i]))
                f2 = greedy_d_e_new(get_node_order(big_x[-1][i]))
            else:
                f1 = greedy_d_e(get_node_order(big_u[i]))
                f2 = greedy_d_e(get_node_order(big_x[-1][i]))

            # tracking the least box no.   
                
            if f1[0] < best[0]:
                best = f1
            if f2[0] < best[0]:
                best = f2

            # 14. The selection phase
            
            if f1[0] < f2[0]:
                x.append(big_u[i])
            else:
                x.append(big_x[-1][i])
                
        big_x.append(x) # logs this generation

    if boxing:
        return best[0]
    else:
        return best[1]
