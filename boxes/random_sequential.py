import random

def random_sequential(network, rb, boxing=False):
    
        """
        The random sequential algorithm from 'A box-covering algorithm for fractal scaling in scale-free networks'
        by Kim et al.
        :param rb: Radius of the box/ball, i.e diameter lB = 2rB
        :param boxing: Determines the type of output.
        :return: If boxing=False then it returns a list of the boxes, otherwise its the Nb number of boxes
        """
        
        unburned = set(network.graph.nodes())
        
        if rb == 0:
            boxes = [[node] for node in network.graph.nodes()]
        else:    
            boxes = []
            
            if network.distance_dict==None:
                print('computation of shortest path data')
                network.get_dist_dict()
            
            while unburned:
                
                # Originally Kim et al selected from the whole set of nodes, but we obtain better results if we
                # select the seed from the unburned nodes. Better means less noisy Nb(lb), optimal Nb numbers and
                # slightly shorter running time
                
                seed = random.choice(list(unburned))
                box = list(network.ball_of_seed(seed, rb).intersection(unburned))
                if box:
                    boxes.append(box)
                    unburned -= set(box)
                    
        if boxing:
            return len(boxes)
        else:
            return boxes