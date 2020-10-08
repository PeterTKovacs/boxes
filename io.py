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
        
        for index,item in enumerate(nb_res): # list of tuples, 0th element is the box no in each
            
            nb_results[index]=item[0]
    
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
            
def benchmark(names,network,box_sizes,algorithm,n,**kwargs):
    
    with open(names['path']+names['net']+'_'+names['alg']+'_benchmark.txt','w') as f:
        
        f.write('network: '+names['net']+'\n')
        f.write('algorithm: '+names['alg']+'\n')
        f.write('keyword arguments:'+str(kwargs)+'\n')
        f.write('box size\tNbs\n')
    
    
        if names['alg']=='merge':
            
            nbs=np.zeros((n,box_sizes[-1]+1),int) # merge gives 0 too
            
            for i in range(n):
                
                nbs[i,:]=np.array([item[0] for item in algorithm(network,box_sizes[-1],**kwargs)])
                
            for row in range(nbs.shape[1]):
                
                f.write(str(row)+'\t'+str(nbs[:,row])+'\n')
            
        else:
            
            for size in box_sizes:

                nb=np.zeros(n,int)

                for j in range(n):
                    nb[j]=algorithm(network,size,**kwargs)

                f.write(str(size)+'\t'+str(nb)+'\n')
            
        
    
def read_logfile(path):
    
    readout=[]
    exec_time=-1.
    
    with open(path,'r') as f:
        data=False

        for line in f:
            tmp=line.split('\t')
            
            if 'time' in line:
                tmp2=line.split(' ')
                exec_time=float(tmp2[-1])
            
            if data:
                readout.append((int(tmp[0]),float(tmp[1]))) # because of fuzzy
            
            if tmp[0]=='box size':
                data=True
    return exec_time,readout


def read_logfile_bench(path):
    
    readout=[]
    
    with open(path,'r') as f:
        data=False

        for line in f:
            tmp=line.split('\t')
            
            if data:
                
                tmp[1]=tmp[1].replace('[','')
                tmp[1]=tmp[1].replace(']','')
                
                if tmp[1][0]!=' ' and tmp[1][0].isalnum():
                
                    kill_double_space=tmp[1][0]
                          
                for i in range(1,len(tmp[1])):
                    if tmp[1][i]==tmp[1][i-1]==' ':
                        continue
                    elif tmp[1][i]==' ':
                        kill_double_space+=tmp[1][i]
                    elif not tmp[1][i].isalnum():
                        continue
                    else:
                        kill_double_space+=tmp[1][i]
                        
                numbers=str.strip(kill_double_space).split(' ')
                
                readout.append((int(tmp[0]),[float(no) for no in numbers])) # fuzzy
            
            if tmp[0]=='box size':
                data=True
    return readout