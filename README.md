# Box-Covering Algorithms for Fractal Networks
This repository contains several box-covering algorithms, which are designed to estimate the fractal dimensionn of complex networks. They are implemeneted in the __boxes__ package.
The following algorithms are implemented:


| Type          | Algorithm                                          | Abbr  | Year | Ref |
|---------------|----------------------------------------------------|-------|------|-----|
| Classic       | Random sequental                                   | RS    | 2007 | [1] |
| Classic       | Greedy coloring                                    | GC    | 2007 | [2] |
| Burning       | Compact-Box-Burning                                | CBB   | 2007 | [2] |
| Burning       | Max-Excluded Mass Burning                          | MEMB  | 2007 | [2] |
| Burning       | Ratio of excluded mass to closeness centrality     | REMCC | 2016 | [3] |
| Burning       | MCWR algortihm                                     | MCWR  | 2019 | [4] |
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

| [1] | ####Fractality and self-similarity in scale-free networks |
|-----|-----------------------------------------------------------|
