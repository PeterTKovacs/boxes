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
from .load import read_from_edgelist
from .bgrade import bgrade
import boxes.io

algorithms=['random sequential','greedy_coloring (various strategies)','cbb','memb','remcc','mcwr','merge_algorithm','simulated annealing','differential_evolution']