import math
import random
import networkx as nx
import copy
from .greedy_coloring import greedy_coloring

def pso(network, lb, gmax=5, pop=5, c1=1.494, c2=1.494, boxing=False):
    
    # "A Discrete Particle Swarm Optimization Box-covering Algorithm for Fractal Dimension on Complex Networks"
    # by Li Kuang et al

    #TODO: át kell nézni, gyanúsan sokáig fut.

    def xor(y, z):
        return int(y != z)

    def sig(y):
        def sigmoid(z):
            return 1 / (1 + math.exp(-z))

        if random.random() < sigmoid(y):
            return 1
        else:
            return 0

    # Find Nbest_i
    def nbest(ni, xi, b_neighbour_boxes, dist_dict, boxes_dictionary):

        # B = neighboring boxes set
        # ni is the node to be checked for switching box.
        # xi is the origin box where node ni belongs to.

        while len(b_neighbour_boxes) > 0:
            xk = random.choice(list(b_neighbour_boxes))
            b_neighbour_boxes.remove(xk)
            out = False
            if xk == xi:
                continue
            for node in list(boxes_dictionary[xk]):
                if dist_dict[ni][node] > lb:
                    out = False
                    break
                else:
                    out = True  
            if out:
                return xk  # if ni fits into the box, return the box ID
        return xi          # if ni fits into no box, return the original box ID

    graph = network.graph
    if not network.shortest_paths:
        network.shortest_paths = dict(nx.all_pairs_shortest_path_length(graph))

    # 1. Find out the all-pairs shortest paths of the network and store them in a dictionary
    
    distance_dictionary = network.shortest_paths
    p = []
    v = []
    gbest = None
    gbestsize = None
    
    for _ in range(pop):
        
        # 2. Initialize the position of each particle by greedy algorithm: 𝑃 = {𝑥1, 𝑥2, ..., 𝑥𝑝𝑜𝑝}.
        p.append(greedy_coloring(network,lb, pso_position=True,strategy='random_sequential')) # returns node-box list 
                 
        # 3. Initialize the velocity: 𝑉 = {𝑣1, 𝑣2, ..., 𝑣𝑝𝑜𝑝} and gbest.
                 
        v.append([0] * graph.number_of_nodes())               # couldn't find it in the paper
        box_number = len(set(p[-1]))                          # maybe overkill to create a set?
        if not gbest or box_number < gbestsize:
            gbest = copy.deepcopy(p[-1])
            gbestsize = box_number

    # 4. Initialize the personal best solution for each particle: 𝑃𝑏𝑒𝑠𝑡={𝑝𝑏𝑒𝑠𝑡1,..., 𝑝𝑏𝑒𝑠𝑡𝑝𝑜𝑝}, 𝑝𝑏𝑒𝑠𝑡𝑖 = 𝑥𝑖
    pbest = copy.deepcopy(p)
                 
    # 5., 6.
    for t in range(gmax):
        for i in range(pop):
                 
            # Boxes: dictionary of the boxes: key = box id, value: set of nodes.
            boxes_dict = {}                     
            for x, n in enumerate(p[i]):   # x-es indexed from 0
                if n in boxes_dict:
                    boxes_dict[n].add(x)
                else:
                    boxes_dict[n] = {x}
                 
            for j in range(graph.number_of_nodes()): # leverages that nodes labeled from 0
                omega = random.random()
                r1 = random.random()
                r2 = random.random()

                # 7. Calculate the new velocity 𝑣𝑡 𝑖 of the 𝑖th particle according to Eq. 3.
                 
                v[i][j] = sig(omega * v[i][j] + c1 * r1 * xor(pbest[i][j], p[i][j]) + c2 * r2 * xor(
                    gbest[j], p[i][j]))

                # 8. Calculate the new position 𝑥𝑡i of the ith particle according to Eq. 6
                 # in fact, update pi component-wise (p_ij)
                 
                 # REMARK: when moving, smaller indices have priority! ~ maybe not a good method...
                 
                if v[i][j] == 1:
                 
                    orig = p[i][j]
                    p[i][j] = nbest(j, p[i][j],
                                    set([p[i][neighbor] for neighbor in graph.neighbors(j)]),
                                    distance_dictionary, boxes_dict)
                    
                    if orig != p[i][j]:
                        boxes_dict[orig].discard(j)
                        boxes_dict[p[i][j]].add(j)

            # 9. Evaluate the 𝑥𝑡𝑖 by calculating the number of distinct boxes in it.
            boxsize = len(set(p[i]))
                 
            if boxsize < len(set(pbest[i])):
                # 10. Update the personal best solution 𝑝𝑏𝑒𝑠𝑡𝑖 and the global best solution 𝑔𝑏𝑒𝑠𝑡.
                # https://www.kdnuggets.com/2019/01/python-patterns-max-instead-if.html
                pbest[i] = copy.deepcopy(p[i])
                if boxsize < len(set(gbest)):
                    gbest = copy.deepcopy(p[i])

    boxes = []
    for box in set(gbest):
        thisbox = []
        for n, b in enumerate(gbest):
            if box == b:
                thisbox.append(n)
        boxes.append(thisbox)
    if boxing:
        return len(boxes)
    else:
        return boxes
