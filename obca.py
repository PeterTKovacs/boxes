import networkx as nx

def overlapping_box_covering(network, lb, boxing=False):
    # "Overlapping-box-covering  method  for  the  fractal  dimension  of  complex  networks"
    # by Yuanyuan Sun et al

    if not network.shortest_paths:
        network.shortest_paths = dict(nx.all_pairs_shortest_path_length(network.graph))
    distance_dictionary = network.shortest_paths
    
    graph = network.graph
    
    if lb == 0:
        boxes = [[node] for node in graph.nodes()]
    elif lb == network.diameter:
        boxes = [list(graph.nodes())]
    else:
        boxes = []
        
        # (2) Set the covered frequency to zero for each node, indicating all nodes are uncovered initially.
        freq = [0] * graph.number_of_nodes()
        sorted_nodes = sorted(list(graph.nodes), key=lambda x: dict(graph.degree())[x])

        # (3) Starting from the nodes with small degrees to the ones with large degrees, repeat the following
        # until all nodes are covered.
        for node in sorted_nodes:

            # (a) If the node is covered, then continue; otherwise, it is selected as the seed to construct a box.
            if freq[node] > 0:
                continue
            else:
                seed = node
                
            # Check whether all distances between any two nodes in the box constructed by the seed are smaller
            # than lB or not.
            
            box = network.ball_of_seed(seed, lb)
            box_list = sorted(list(box),key=lambda x: freq[x]) # 'preferring uncovered nodes'

            # (b) Select one unchecked node i in the box, preferring to select the uncovered nodes.
            # If the distance lij from i to another one j is greater than lB, remove j from the box.
            # Repeat (b) until all distances between any two nodes in the box are smaller than lB.
            # Consequently,  yield  an  EB (effective box, i.e. there's at least one node only belongs to it)
            
            for i in range(len(box_list)):
                if box_list[i] not in box:
                    continue
                for j in range(i + 1, len(box_list)):
                    if distance_dictionary[box_list[i]][box_list[j]] > lb:
                        if box_list[j] != seed:
                            box.discard(box_list[j])
                        else:
                            box.discard(box_list[i])
                            break

            # (d) Increase  the  covered  frequency  by  1  for  each  nodein  it,  and  save  it  temporarily.
            for bn in box:
                freq[bn] += 1
            boxes.append(box)

        # (4) Judging from the covered frequency of each node, check whether the boxes finally obtained are the EB.
        # Since some EBs may be divided by others and become the RB, if one RB is found,
        # delete it and decrease the covered frequency by 1 for each node in it
        
        for i, b in enumerate(boxes):
            redundancy = 0
            for n in b:
                if freq[n] > 1:
                    redundancy += 1
            if redundancy == len(b):
                for n in b:
                    freq[n] -= 1
                boxes[i] = None

        while None in boxes:
            boxes.remove(None)
    if boxing:
        return len(boxes)
    else:
        return list(map(list, boxes))
