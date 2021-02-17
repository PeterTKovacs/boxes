from .random_sequential import random_sequential

def sampling(network,bsize, inner_algorithm, n_repeat,strategy,maxbox_sampling=False,outer_boxing=True, **kwargs):
    
    # first stage: run the provided algorithm n times and store all boxes
    
    boxes={}
    id_=0
    parent_boxes={node:set() for node in network.graph.nodes()}
    covering_frequency={node:0 for node in network.graph.nodes()}
    
    if maxbox_sampling: # not a standalone boxing algorithm - need estimation from RS
        
        n_estimate=random_sequential(network,int(bsize/2),boxing=True) # maxbox sampling uses lb
        box_batch=inner_algorithm(network,bsize,n_repeat*n_estimate)
        
        for b in box_batch:
            boxes[id_]=b
            
            for node in b:
                covering_frequency[node]+=1
                parent_boxes[node].add(id_)
                
            id_+=1
    else:
        
        for i in range(n_repeat):
            box_batch=inner_algorithm(network,bsize,**kwargs)

            for b in box_batch:
                boxes[id_]=b

                for node in b:
                    covering_frequency[node]+=1
                    parent_boxes[node].add(id_)

                id_+=1
     
    
    sequence=[i for i in boxes.keys()]
    sizes={i:len(boxes[i]) for i in sequence}
    
    uncovered=set(network.graph.nodes())
    sequence=semimerge(set(sequence),sequence,sizes)
    
    final_boxes=[]
    
    # assume that the graph is nonempty, and the above stuff is neither
    
    if strategy=='big_first':
        
        while sizes[sequence[-1]]>0:
            
            box_id=sequence[-1]
            final_boxes.append(boxes[box_id].intersection(uncovered))
            
            
            #cover the biggest box and modify sizes correspondingly
            
            affected_boxes=cover(box_id,boxes,parent_boxes,uncovered,sizes,covering_frequency)
            uncovered=uncovered-boxes[box_id]
            
            # order boxes again
            
            sequence=semimerge(affected_boxes,sequence,sizes)
            
    elif strategy=='small_first':
        
        for j in range(len(sequence)):
            
            cov=False
            for node in boxes[sequence[j]]: # do not test for being covered: we won't get underflow for realistic graphs
                if covering_frequency[node]==1: # we exclude already covered - see cover function
                    cov=True                    # this box must be covered according to strategy
                    break
                else:
                    covering_frequency[node]-=1 # if won't be covered: OK, if it will: doesn't matter cover will set to 0
            if cov:

                box_id=sequence[j]
                final_boxes.append(boxes[box_id].intersection(uncovered))
                affected_boxes=cover(box_id,boxes,parent_boxes,uncovered,sizes,covering_frequency)
                uncovered=uncovered-boxes[box_id]

                if j==len(sequence)-1: # if no point in ordering
                    break
                sequence[j+1:]=semimerge(affected_boxes,sequence[j+1:],sizes) #only order the relevant
  
    
    if outer_boxing:
        return len(final_boxes)
    else:
        return final_boxes
            
def cover(box_id,boxes,parent_boxes,uncovered,sizes,cfreq):
    
    affected_boxes=set()
    
    for node in uncovered.intersection(boxes[box_id]):
        cfreq[node]=0 # not to count later as possible uncovered - see main function
        affected_boxes=affected_boxes.union(parent_boxes[node])
        
        for pbox in parent_boxes[node]:
            sizes[pbox]-=1
    
    return affected_boxes
    
    
def semimerge(unordered,seq,sizes):
    # assuming unordered is hash-based (eg. set)
    # seq is ordered iterable (list)
    
    modified=sorted([e for e in seq if e in unordered], key=lambda x: sizes[x])
    original=[e for e in seq if not (e in unordered)]
    
    result=[None for i in range(len(seq))]
    
    i_m=0
    i_o=0
    
    for i in range(len(result)):
        if i_m==len(modified):
            result[i:]=original[i_o:]
            break
        elif i_o==len(original):
            result[i:]=modified[i_m:]
            break
        else:
            if sizes[modified[i_m]]<sizes[original[i_o]]:
                result[i]=modified[i_m]
                i_m+=1
            else:
                result[i]=original[i_o]
                i_o+=1
                
    return result