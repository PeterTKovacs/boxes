from .network import network
import boxes.generators 
from .random_sequential import random_sequential
from .greedy_coloring import greedy_coloring
from .cbb import cbb
from .memb import memb
from .remcc import remcc
from .mcwr import mcwr
from .merge_algorithm import merge_algorithm
from .simulated_annealing import simulated_annealing
from .differential_evolution import differential_evolution
from .bgrade import bgrade
import boxes.io_
import boxes.load
from .pso import pso
from .obca import  overlapping_box_covering as obca
from .fuzzy import fuzzy
from .boxing import boxing_
from .maximal_box_sampling import maximal_box_sampling
from .sampling import sampling

algorithms=['random sequential','greedy_coloring (various strategies)','cbb','memb','remcc','mcwr','merge_algorithm','simulated annealing','differential_evolution','pso','obca']