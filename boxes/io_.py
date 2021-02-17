import time
import gc
import numpy as np

def run_boxing(names,time_offset,network,box_sizes,algorithm,merge_alg=False,**kwargs):
    
    '''
    
    assuming that necessary preprocessing (e.g. get shortest path data) has been perfomed
    its time passed in time_offset
    
    names: dicitonary for log naming, names['path'],names['net'],names['alg']
    
    '''
    
    
    
    nb_results={}
    runtimes={}
    
    if merge_alg:
        
        nb_res=algorithm(network,box_sizes,**kwargs) # in this case, only the max lb is passed
        
        for index,item in enumerate(nb_res): # assuming measure_time=True, list of Nb starting from lb=0
            
            nb_results[index]=item[0]
            runtimes[index]=item[1]+time_offset
            
            gc.collect()
    
    else: 
        for box_size in box_sizes:
        
            start=time.time()
            nb_results[box_size]=algorithm(network,box_size,**kwargs)
            end=time.time()
            
            runtimes[box_size]=end-start+time_offset
            
            gc.collect()
            
            if nb_results[box_size]==1:
                break
        
    
    
    with open(names['path']+names['net']+'_'+names['alg']+'.txt','w') as f:
        
        f.write('network: '+names['net']+'\n')
        f.write('algorithm: '+names['alg']+'\n')
        f.write('keyword arguments:'+str(kwargs)+'\n')
        f.write('box size\tNb\tt\n')
        
        for size in nb_results.keys():
            f.write(str(size)+'\t'+str(nb_results[size])+'\t'+str(runtimes[size])+'\n')
            
def benchmark(names,time_offset,network,box_sizes,algorithm,n,merge_alg=False,**kwargs):
    
    with open(names['path']+names['net']+'_'+names['alg']+'_benchmark.txt','w') as f:
        
        f.write('network: '+names['net']+'\n')
        f.write('algorithm: '+names['alg']+'\n')
        f.write('keyword arguments:'+str(kwargs)+'\n')
        
    
    
    
        
        
        if merge_alg:
            
            nbs=np.zeros((n,box_sizes+1),float) # merge gives 0 too
            runtimes=np.zeros((n,box_sizes+1),float)
            
            for i in range(n):
                
                output=algorithm(network,box_sizes,**kwargs)
                
                nbs[i,:]=np.array([item[0] for item in output])
                runtimes[i,:]=np.array([item[1]+time_offset for item in output])
                
                gc.collect()

        else: 
            
            nbs=np.zeros((n,len(box_sizes)),float) # fuzzy
            runtimes=np.zeros((n,len(box_sizes)),float)
            
            nmax=len(box_sizes)
            
            for index,size in enumerate(box_sizes):
                for j in range(n):
                    
                    start=time.time()
                    nbs[j,index]=algorithm(network,size,**kwargs)
                    end=time.time()
                    
                    runtimes[j,index]=end-start+time_offset
                    
                    gc.collect()
                    
                if np.sum(nbs[:,index])==n: # all ones, terminate!
                    nmax=index
                    break
        
        
                                         
        f.write('box size\tNbs\tts\n')

        for box_ in range(nbs.shape[1]): # iterate over box sizes
              
            if merge_alg:
                
                f.write(str(box_)+'\t'+np.array2string(nbs[:,box_],separator=',',max_line_width=n*1000)+'\t'
                                      +np.array2string(runtimes[:,box_],separator=',',max_line_width=n*1000)+'\n')
                         
            else:
                
                if nmax<box_:
                          break
            
                f.write(str(box_sizes[box_])+'\t'+np.array2string(nbs[:,box_],separator=',',max_line_width=n*1000)+'\t'
                                                 +np.array2string(runtimes[:,box_],separator=',',max_line_width=n*1000)+'\n')
    
def read_logfile(path):
    
    readout=[]
    
    with open(path,'r') as f:
        data=False

        for line in f:
            tmp=line.split('\t')
            
            if data:
                readout.append((int(tmp[0]),float(tmp[1]),float(tmp[2]))) # because of fuzzy
            
            if tmp[0]=='box size':
                data=True
    return readout


def read_logfile_bench(path):
    
    readout=[]
    
    with open(path,'r') as f:
        data=False

        for line in f:
            tmp=line.split('\t')
            
            if data:
                         
                lb=int(tmp[0])
                nbs=np.fromstring(tmp[1][1:-1],sep=',',dtype=float)   # because of fuzzy and trailing [..]  
                runtimes=np.fromstring(tmp[2][1:-1],sep=',',dtype=float)
                         
                readout.append((lb,nbs,runtimes))
            
            if tmp[0]=='box size':
                data=True
                         
    return readout

def canonized_lb(path,alg,lb_alg,rb_alg):
    
    readout=read_logfile(path)
    
    if alg=='fuzzy':
        # no modification is needed - see original paper
        
        return readout
    
    elif alg in rb_alg: #['mcwr_0.75','mcwr_0.5','mcwr_0.25','memb','random_sequential','remcc','sampling_rs']:
        
        curated=[]
        
        for item in readout:
            curated.append((2*item[0]+1,item[1],item[2]))
        
        return curated
    
    elif alg in lb_alg:  #['cbb','greedy','obca','merge','sampling_maxbox','simulated_annealing','differential_evolution',
                #'pso']:
        
        curated=[]
        
        for item in readout:
            curated.append((item[0]+1,item[1],item[2]))
        
        return curated
    
    else:
        
        print('Algorithm out of the set of curated ones, try later')
        return 0
    
def canonized_lb_bench(path,alg,lb_alg,rb_alg):
    
    readout=read_logfile_bench(path)
    
    if alg=='fuzzy':
        # no modification is needed - see original paper
        
        return readout
    
    elif alg in rb_alg: #['mcwr_0.75','mcwr_0.5','mcwr_0.25','memb','random_sequential','remcc','sampling_rs']:
        
        curated=[]
        
        for item in readout:  # item[1], item[2] is numpy array now
            curated.append((2*item[0]+1,item[1],item[2]))
        
        return curated
    
    elif alg in lb_alg: #['cbb','greedy','obca','merge','sampling_maxbox','simulated_annealing','differential_evolution',
                #'pso']:
        
        curated=[]
        
        for item in readout: # item[1], item[2] is numpy array now
            curated.append((item[0]+1,item[1],item[2]))
        
        return curated
    
    else:
        
        print('Algorithm out of the set of curated ones, try later')
        return 0
    
    
  
