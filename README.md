# Box-Covering Algorithms for Fractal Networks
This repository contains several box-covering algorithms, which are designed to estimate the fractal dimensionn of complex networks. They are implemeneted in the __boxes__ package. 

Moreover, the supplementary data for the paper [*Comparative Analysis of Box-Covering Algorithms for Fractal Networks*](https://arxiv.org/abs/2105.01939) - P. T. Kovács, M. Nagy, R. Molontay (2021) can be found in [this folder](ans_2021_supplementary).


## How to Cite
```
@article{kovacs2021comparative,
         title={Comparative {A}nalysis of {B}ox-{C}overing {A}lgorithms for {F}ractal {N}etworks},
         author={Kovács, Tamás Péter and Nagy, Marcell and Molontay, Roland},
         year={2021},
         eprint={2105.01939},
         archivePrefix={arXiv},
         primaryClass={cs.SI}
}
```


## Implemented Algorithms

| Type          | Algorithm                                          | Abbr  | Year | Ref |
|---------------|----------------------------------------------------|-------|------|-----|
| Classic       | Random sequental                                   | RS    | 2007 | [[1]](#random-sequential) |
| Classic       | Greedy coloring                                    | GC    | 2007 | [[2]](#how-to-calc)       |
| Burning       | Compact-Box-Burning                                | CBB   | 2007 | [[2]](#how-to-calc)       |
| Burning       | Max-Excluded Mass Burning                          | MEMB  | 2007 | [[2]](#how-to-calc)       |
| Burning       | Ratio of excluded mass to closeness centrality     | REMCC | 2016 | [[3]](#remcc)             |
| Burning       | MCWR algortihm                                     | MCWR  | 2019 | [[4]](#mcwr)              |
| Classic       | Merge algorithm                                    | MA    | 2010 | [[5]](#ma-sa)             |
| Metaheuristic | Simulated annealing algorithm                      | SA    | 2010 | [[5]](#ma-sa)             |
| Other         | Overlapping Box Covering Algorithm                 | OBCA  | 2014 | [[6]](#obca)              |
| Metaheuristic | Differential evolution                             | DE    | 2014 | [[7]](#debc)              |
| Other         | Fuzzy box-covering                                 | Fuzzy | 2014 | [[8]](#fuzzy)             |
| Metaheuristic | Particle Swarm Optimization Box-covering Algorithm | PSO   | 2015 | [[9]](#psobc) |


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
| <a name="remcc"></a>[3] | Zheng, W., Pan, Q., Sun, C., Deng, Y. F., Zhao, X. K., & Kang, Z. (2016). Fractal analysis of mobile social networks. *Chinese Physics Letters*, 33(3), 038901. |
| <a name="mcwr"></a>[4] | Liao, H., Wu, X., Wang, B. H., Wu, X., & Zhou, M. (2019). Solving the speed and accuracy of box-covering problem in complex networks. *Physica A: Statistical Mechanics and its Applications*, 523, 954-963. |
| <a name="ma-sa"></a>[5] | Locci, M., Concas, G., Tonelli, R., & Turnu, I. (2010). Three algorithms for analyzing fractal software networks. *WSEAS Trans. Info. Sci. and App*, 7, 371-380. |
| <a name="obca"></a>[6] | Sun, Y., & Zhao, Y. (2014). Overlapping-box-covering method for the fractal dimension of complex networks. *Physical Review E*, 89(4), 042809. |
| <a name="debc"></a>[7] | Kuang, L., Zhao, Z., Wang, F., Li, Y., Yu, F., & Li, Z. (2014, July). A differential evolution box-covering algorithm for fractal dimension on complex networks. In *2014 IEEE Congress on Evolutionary Computation (CEC)* (pp. 693-699). IEEE. |
| <a name="fuzzy"></a>[8] | Zhang, H., Hu, Y., Lan, X., Mahadevan, S., & Deng, Y. (2014). Fuzzy fractal dimension of complex networks. *Applied Soft Computing*, 25, 514-518. |
| <a name="psobc"></a>[9] |Kuang, L., Wang, F., Li, Y., Mao, H., Lin, M., & Yu, F. (2015, May). A discrete particle swarm optimization box-covering algorithm for fractal dimension on complex networks. In *2015 IEEE Congress on Evolutionary Computation (CEC)* (pp. 1396-1403). IEEE. |
