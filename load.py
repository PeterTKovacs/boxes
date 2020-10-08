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
    
                