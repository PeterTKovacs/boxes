import networkx as nx
from .io_ import benchmark,run_boxing
import numpy as np
import random
import os
import time

def boxing_(network,net,alg_dict,box_sizes,path,preprocessing='distance_dict',benchmark_n=-1):
    
    '''For expected inputs, see tutorial 
    
    path shall be directory/ where all results are saved into this.
    
    When not existing, generated.
    If it does, overwrite files therein.
    '''

    if not os.path.isdir(path):
        os.mkdir(path)
    
    network.distance_dict=None
    network.shortest_paths=None
    
    start=time.time()
    
    if preprocessing=='distance_dict':
        network.get_dist_dict()
        
    elif preprocessing=='shortest_paths':
        network.shortest_paths=dict(nx.all_pairs_shortest_path_length(network.graph))
        
    else:
        pass
        
    time_offset=time.time()-start
    
    if benchmark_n==-1:
        benchmarking=False
    else:
        benchmarking=True
        
    if benchmarking:
    
        for alg in alg_dict.keys():

            random.seed(137)  #reproducibility
            np.random.seed(137)
            
            if alg=='merge':
                bsizes=box_sizes[-1]
                
                benchmark({'path':path,'net':net,'alg':alg},
                               time_offset,
                                network,
                                bsizes,                         # box sizes
                               alg_dict[alg]['alg'], # set algorithm
                                benchmark_n,
                                merge_alg=True,
                               **alg_dict[alg]['kwargs']) # unpack keyword arguments


            else:
                bsizes=box_sizes
                
                benchmark({'path':path,'net':net,'alg':alg},
                                   time_offset,
                                    network,
                                    bsizes,                         # box sizes
                                   alg_dict[alg]['alg'], # set algorithm
                                    benchmark_n,
                                   **alg_dict[alg]['kwargs']) # unpack keyword arguments
    else: 
        
        for alg in alg_dict.keys():

            random.seed(137)  #reproducibility
            np.random.seed(137)
            
            if alg=='merge':
                bsizes=box_sizes[-1]
                
                run_boxing({'path':path,'net':net,'alg':alg},
                                   time_offset,
                                    network,
                                    bsizes,                         # box sizes
                                    alg_dict[alg]['alg'],      # set algorithm
                                   merge_alg=True,
                                   **alg_dict[alg]['kwargs']) # unpack keyword arguments

            else:
                bsizes=box_sizes
                
                run_boxing({'path':path,'net':net,'alg':alg},
                                   time_offset,
                                    network,
                                    bsizes,                         # box sizes
                                    alg_dict[alg]['alg'],      # set algorithm
                                   **alg_dict[alg]['kwargs']) # unpack keyword arguments
