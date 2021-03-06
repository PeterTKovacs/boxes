"""
Generators for some fractal networks

"""
# Marcell Nagy <marcessz@math.bme.hu>
import networkx as nx
import random


def uv_flower(u, v, n):
    # Returns an a (u,v)-flower
    # TODO: átnézni
    graph = nx.cycle_graph(u + v)
    for i in range(n - 1):
        for e in list(graph.edges):
            graph.remove_edge(e[0], e[1])

            path_nodes = [e[0]]
            for x in range(u - 1):
                path_nodes.append(graph.number_of_nodes())
                graph.add_node(graph.number_of_nodes())
                graph.add_edge(path_nodes[-2], path_nodes[-1])
            graph.add_edge(path_nodes[-1], e[1])

            path_nodes = [e[0]]
            for x in range(v - 1):
                path_nodes.append(graph.number_of_nodes())
                graph.add_node(graph.number_of_nodes())
                graph.add_edge(path_nodes[-2], path_nodes[-1])
            graph.add_edge(path_nodes[-1], e[1])

    return graph


def fractal_model(generation, m, x, e):
    """
    Returns the fractal model introduced by
    Song, Havlin, Makse in Nature Physics 2, 275.
    generation = number of generations
    m = number of offspring per edge end-point
    x = number of connections between offsprings
    e = probability that hubs stay connected
    1-e = probability that x offsprings connect.
    If e=1 we are in MODE 1 (pure small-world).
    If e=0 we are in MODE 2 (pure fractal).
    """
    graph = nx.Graph()
    graph.add_edge(0, 1)  # This is the seed for the network (generation 0)
    node_index = 2
    for n in range(1, generation+1):
        all_links = list(graph.edges())
        while all_links: # added m new nodes per link - sufficient to go by edges
            link = all_links.pop()
            
            new_nodes_a = range(node_index, node_index + m)
            node_index += m
            
            new_nodes_b = range(node_index, node_index + m)
            node_index += m
            
            graph.add_edges_from([(link[0], node) for node in new_nodes_a])
            graph.add_edges_from([(link[1], node) for node in new_nodes_b])
            
            # original version
            
#             repulsive_links = list(zip(new_nodes_a, new_nodes_b)) # yields tuples
#             graph.add_edges_from([repulsive_links.pop() for _ in range(x-1)])  # TODO: ezt meg kell nézni a cikkben
            
            if x>m: # this is needed in order to avoid triggering error by popping from empty list
                repulsive_no=m
                print('invalid arguments: x>m\n set x=m instead')
            else:
                repulsive_no=x
            
            
            if random.random() > e:
                repulsive_links = list(zip(new_nodes_a, new_nodes_b)) # yields tuples
                graph.add_edges_from([repulsive_links.pop() for _ in range(repulsive_no)])  # TODO: ezt meg kell nézni a cikkben
                graph.remove_edge(link[0], link[1])
          
    return graph


def hub_attraction_dynamical_growth_model(generations, m, a, b, t_cutoff):
    """
    Returns a fractal graph generated by the model, introduced by Li Kuang et al. in:
    "A Fractal and Scale-free Model of Complex Networks with Hub Attraction Behaviors"

    This is a modification of the previous fractal model

    :param generations: number of iterations
    :param m: number of new offsprings per edge end-point
    :param a: connection probability of hubs
    :param b: connection probability of non-hubs
    :param t_cutoff: threshold separating hubs and non-hubs
    :return: graph
    """
    x = 1

    graph = nx.Graph()
    graph.add_edge(0, 1) # this is generation 0 so to speak
    node_index = 2

    t = 1
  
    while t <= generations:
        
        all_links = list(graph.edges())
        degrees = dict(graph.degree)
        k_max = max(degrees.values())  # The maximum degree in the graph at time t
        offsprings = {}  # dict: keys are nodes, values are set of new offsprings
        
        for edge in all_links:

            new_nodes_a = range(node_index, node_index + m)
            node_index += m
            
            new_nodes_b = range(node_index, node_index + m)
            node_index += m

            if edge[0] in offsprings:
                offsprings[edge[0]] = offsprings[edge[0]].union(set(new_nodes_a))
            else:
                offsprings[edge[0]] = set(new_nodes_a)

            if edge[1] in offsprings:
                offsprings[edge[1]] = offsprings[edge[1]].union(set(new_nodes_b))
            else:
                offsprings[edge[1]] = set(new_nodes_b)

            graph.add_edges_from([(edge[0], node) for node in new_nodes_a])
            graph.add_edges_from([(edge[1], node) for node in new_nodes_b])
            
            repulsive_links = list(zip(new_nodes_a, new_nodes_b))
            
            # degrees dictionary contains the degrees from the previous generation
            
            if degrees[edge[0]] / k_max > t_cutoff and degrees[edge[1]] / k_max > t_cutoff:
                e_prob = a
            else:
                e_prob = b

            if random.random() > e_prob:
                graph.remove_edge(edge[0], edge[1])
                graph.add_edges_from([repulsive_links.pop()])

        # TODO: max degree kellene a boxból
        
        within_box_edges = []
        
        for node, offspg in offsprings.items():
            rnd_node = random.choice(list(offspg))
            within_box_edges += [(rnd_node, n) for n in random.sample(offspg - {rnd_node}, degrees[node])]

        graph.add_edges_from(within_box_edges)
        
        t += 1

    return graph