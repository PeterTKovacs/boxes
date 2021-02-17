import networkx as nx

def greedy_coloring(network, lb, boxing=False, pso_position=False, strategy='random_sequential'):
    
# To achieve boxing, the original problem is mapped to the famous graph coloring problem.
# This means that we color the dual graph of the original network.
    
        dual_graph = network.dual_network(lb)
        
# coloring via networkx: Returns a dictionary with keys representing nodes and values representing corresponding coloring.
        
        dual_colors = nx.greedy_color(dual_graph, strategy=strategy)
        
        # TODO: kipróbálni a networkx többi stratégiáját. esetleg beállítani paraméternek.

        inved_dual_colors = network.invert_dict_list(dual_colors) # returns {color:list_of_nodes}
        
        boxes = []
        
        for color in inved_dual_colors.keys():
            boxes.append(set(inved_dual_colors[color]))

# Recovering coloring for individual nodes, if needed          
            
        if pso_position:
            
            color_map = [None] * network.graph.number_of_nodes() # returns [None,None,...] the aprropriate times
            
            for n in dual_colors: # the keys of dual_colors are the IDs of nodes
                color_map[n] = dual_colors[n]
            return color_map
        
        if boxing:
            return len(boxes)
        else:
            return boxes
