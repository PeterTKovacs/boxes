import time
import networkx as nx
from .merge_if_possible import merge_if_possible

def merge_algorithm(network, lb_max, return_for_sa=False, boxing=False,measure_time=False):
    
    # "Three  Algorithms  for  Analyzing  Fractal  Software  Networks"
    # by Mario Locci et al
    
    graph = network.graph

    if not network.shortest_paths:
        network.shortest_paths = dict(nx.all_pairs_shortest_path_length(graph))
    shortest_paths = network.shortest_paths

        # In the initial configuration each cluster c_k contains only a node,
        # so each node is marked with a different label.
    c = [{n} for n in
         graph.nodes()]
 
    lb = 1

    if measure_time:
        boxing_output = [(len(c), 0)]
        while lb <= lb_max:
            
            start_time = time.time()  
            c = merge_if_possible(c, lb, shortest_paths)
            total_time = time.time() - start_time

            if boxing:
                boxing_output += [(len(c), total_time)]
            lb += 1
    else:
        boxing_output = [len(c)]
        while lb <= lb_max: 
            
            c = merge_if_possible(c, lb, shortest_paths)

            if boxing:
                boxing_output += [len(c)]
            lb += 1

    if return_for_sa:
        return c

    elif boxing:
        return boxing_output

    else:
        return list(map(list, c))