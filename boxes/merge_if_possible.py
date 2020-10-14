# The merge_if_possible is an auxiliary function for the merge_algorithm and simulated_annealing functions

import random 

def merge_if_possible(c, lb, distance_dict):

        def is_mergeable(box_a, box_b, l, dist_dict):
            # checks if is it possible to merge box_a and box_b.
            mergeable = True
            for node_of_a in box_a:
                for node_of_b in box_b:
                    if dist_dict[node_of_a][node_of_b] > l:
                        mergeable = False
                        break
                if not mergeable:
                    break
            return mergeable

        d = []
        while len(c) > 0:
            ck = random.choice(c)  # Get a random cluster from C
            c_prime = []  # C'
            for cj in list(c):
                if ck == cj:
                    continue
                if is_mergeable(ck, cj, lb, distance_dict):
                    c_prime.append(cj)
            if len(c_prime) != 0:
                ci = random.choice(c_prime)  # Get a random cluster Ci from C'
                d += [ck.union(ci)]  # c = merge(Ck,Cj), D = D union c
                # Remove Ck and Ci from C
                c.remove(ci)
                c.remove(ck)
            else:
                d += [ck]
                c.remove(ck)
        return d
