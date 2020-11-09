import time
import gc
import numpy as np

def run_boxing(names,time_offset,network,box_sizes,algorithm,merge_alg=False,**kwargs):
    
    '''
    
    assuming that necessary preprocessing (e.g. get shortest path data) has been perfomed
    its time passed in time_offset
    
    names: dicitonary for log naming, names['path'],names['net'],names['alg']
    
    '''
    
    start=time.time()
    
    nb_results={}
    
    if merge_alg:
        
        nb_res=algorithm(network,box_sizes,**kwargs) # in this case, only the max lb is passed
        
        for index,item in enumerate(nb_res): # assuming measure_time=False, list of Nb starting from lb=0
            
            nb_results[index]=item
            
            gc.collect()
    
    else: 
        for box_size in box_sizes:
        
            nb_results[box_size]=algorithm(network,box_size,**kwargs)
            
            gc.collect()
            
            if nb_results[box_size]==1:
                break
        
    end=time.time()
    
    with open(names['path']+names['net']+'_'+names['alg']+'.txt','w') as f:
        
        f.write('network: '+names['net']+'\n')
        f.write('algorithm: '+names['alg']+'\n')
        f.write('keyword arguments:'+str(kwargs)+'\n')
        f.write('execution time: '+str(end-start+time_offset)+'\n')
        f.write('box size\tNb\n')
        
        for size in nb_results.keys():
            f.write(str(size)+'\t'+str(nb_results[size])+'\n')
            
def benchmark(names,time_offset,network,box_sizes,algorithm,n,merge_alg=False,**kwargs):
    
    with open(names['path']+names['net']+'_'+names['alg']+'_benchmark.txt','w') as f:
        
        f.write('network: '+names['net']+'\n')
        f.write('algorithm: '+names['alg']+'\n')
        f.write('keyword arguments:'+str(kwargs)+'\n')
        
    
    
    
        start=time.time()
        
        if merge_alg:
            
            nbs=np.zeros((n,box_sizes+1),int) # merge gives 0 too
            
            for i in range(n):
                
                nbs[i,:]=np.array(algorithm(network,box_sizes,**kwargs))
                
                gc.collect()

        else:
            
            nbs=np.zeros((n,len(box_sizes)),int)
            
            nmax=len(box_sizes)
            
            for index,size in enumerate(box_sizes):
                for j in range(n):
                         
                    nbs[j,index]=algorithm(network,size,**kwargs)
                    
                    gc.collect()
                    
                if np.sum(nbs[:,index])==n: # all ones, terminate!
                    nmax=index
                    break
        
        end=time.time()
                         
        f.write('execution time: '+str(end-start+time_offset)+'\n')                 
        f.write('box size\tNbs\n')

        for box_ in range(nbs.shape[1]): # iterate over box sizes
              
            if merge_alg:
                
                f.write(str(box_)+'\t'+np.array2string(nbs[:,box_],separator=',',max_line_width=n*100)+'\n')
                         
            else:
                
                if nmax<box_:
                          break
            
                f.write(str(box_sizes[box_])+'\t'+np.array2string(nbs[:,box_],separator=',',max_line_width=n*100)+'\n')
    
def read_logfile(path):
    
    readout=[]
    exec_time=-1.
    
    with open(path,'r') as f:
        data=False

        for line in f:
            tmp=line.split('\t')
            
            if 'execution time' in line:
                tmp2=line.split(' ')
                exec_time=float(tmp2[-1])
            
            if data:
                readout.append((int(tmp[0]),float(tmp[1]))) # because of fuzzy
            
            if tmp[0]=='box size':
                data=True
    return exec_time,readout


def read_logfile_bench(path):
    
    readout=[]
    exec_time=-1.
    
    with open(path,'r') as f:
        data=False

        for line in f:
            tmp=line.split('\t')
            
            if 'execution time' in line:
                tmp2=line.split(' ')
                exec_time=float(tmp2[-1])
            
            if data:
                         
                lb=int(tmp[0])
                nbs=np.fromstring(tmp[1][1:-1],sep=',',dtype=float)   # because of fuzzy and trailing [..]       
                         
                readout.append((lb,nbs))
            
            if tmp[0]=='box size':
                data=True
                         
    return exec_time,readout

def canonized_lb(path,alg):
    
    exec_time,readout=read_logfile(path)
    
    if alg=='fuzzy':
        # no modification is needed - see original paper
        
        return exec_time,readout
    
    elif alg in ['mcwr_0.75','mcwr_0.5','mcwr_0.25','memb','random_sequential','remcc']:
        
        curated=[]
        
        for item in readout:
            curated.append((2*item[0]+1,item[1]))
        
        return exec_time,curated
    
    elif alg in ['cbb','greedy','obca','merge']:
        
        curated=[]
        
        for item in readout:
            curated.append((item[0]+1,item[1]))
        
        return exec_time,curated
    
    else:
        
        print('Algorithm out of the set of curated ones, try later')
        return 0
    
def canonized_lb_bench(path,alg):
    
    exec_time,readout=read_logfile_bench(path)
    
    if alg=='fuzzy':
        # no modification is needed - see original paper
        
        return exec_time,readout
    
    elif alg in ['mcwr_0.75','mcwr_0.5','mcwr_0.25','memb','random_sequential','remcc']:
        
        curated=[]
        
        for item in readout:
            curated.append((2*item[0]+1,item[1]))
        
        return exec_time,curated
    
    elif alg in ['cbb','greedy','obca','merge']:
        
        curated=[]
        
        for item in readout:
            curated.append((item[0]+1,item[1]))
        
        return exec_time,curated
    
    else:
        
        print('Algorithm out of the set of curated ones, try later')
        return 0
    
    
  
