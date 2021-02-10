# Box-Covering Algorithms for Fractal Networks
This repository contains several box-covering algorithms, which are designed to estimate the fractal dimensionn of complex networks. They are implemeneted in the __boxes__ package.
The following algorithms are implemented:


| Type          | Algorithm                                          | Abbr  | Year | Ref |
|---------------|----------------------------------------------------|-------|------|-----|
| Classic       | Random sequental                                   | RS    | 2007 | [[1]](#random-sequential) |
| Classic       | Greedy coloring                                    | GC    | 2007 | [[2]](#how-to-calc)       |
| Burning       | Compact-Box-Burning                                | CBB   | 2007 | [[2]](#how-to-calc)       |
| Burning       | Max-Excluded Mass Burning                          | MEMB  | 2007 | [[2]](#how-to-calc)       |
| Burning       | Ratio of excluded mass to closeness centrality     | REMCC | 2016 | [3] |
| Burning       | MCWR algortihm                                     | MCWR  | 2019 | [[4]](#mcwr) |
| Classic       | Merge algorithm                                    | MA    | 2010 | [5] |
| Metaheuristic | Simulated annealing algorithm                      | SA    | 2010 | [5] |
| Other         | Overlapping Box Covering Algorithm                 | OBCA  | 2014 | [6] |
| Metaheuristic | Differential evolution                             | DE    | 2014 | [7] |
| Other         | Fuzzy box-covering                                 | Fuzzy | 2014 | [8] |
| Metaheuristic | Particle Swarm Optimization Box-covering Algorithm | PSO   | 2015 | [9] |


This repository was developed by Marcell Nagy and Péter Kovács at the Budapest University of Technology and Economics (BME), Department of Stochastics. We are grateful for the contributions of Botond Diviki-Nagy.



Fork if you feel like.

Some basic tutorial provided but recommend to read the docs & the report first.

Obviously, you may want to run the [tutorial notebook](./tutorial/boxing_tutorial.ipynb) outside the tutorial folder to be able to load the __boxes__ package.

If you plan to add new algorithms, it is really easy but you will have to consider amending the logfile management (eg. canonization, reading).



## References

| Ref | Paper |
|-----|-------|
| <a name="random-sequential"></a>[1] | Kim, J. S., Goh, K. I., Kahng, B., & Kim, D. (2007). Fractality and self-similarity in scale-free networks. *New Journal of Physics*, 9(6), 177.  |
| <a name="how-to-calc"></a>[2] | Song, C., Gallos, L. K., Havlin, S., & Makse, H. A. (2007). How to calculate the fractal dimension of a complex network: the box covering algorithm. *Journal of Statistical Mechanics: Theory and Experiment*, 2007(03), P03006. |
| <a name="mcwr"></a>[4] | Liao, H., Wu, X., Wang, B. H., Wu, X., & Zhou, M. (2019). Solving the speed and accuracy of box-covering problem in complex networks. *Physica A: Statistical Mechanics and its Applications*, 523, 954-963. |
