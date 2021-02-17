import networkx as nx


def read_from_edgelist(edge_file,header=0):
    
    # reads graph from file containig (unweighted) links, header gives the length of header part
    
    g=nx.Graph()
    
    with open(edge_file,'r') as f:
        
        i=0
        
        for line in f: # expected to have lines with space separator
            
            if i<header:
                i+=1
                continue
            
            spl=line.split()
            
            if len(spl)==2:
                g.add_edge(int(spl[0]),int(spl[1]))
            else:
                
                print('invalid data type')
                print(line)
                print(i)
                return -1
            
    return g

def read_max_connected_component(path,header_length=0):
    
    graph=read_from_edgelist(path,header_length)
    
    if not nx.is_connected(graph):
        
        max_connected=graph.subgraph((max(nx.connected_components(graph),key=len)))
        
        return max_connected
    
    else:
        return graph
    
                