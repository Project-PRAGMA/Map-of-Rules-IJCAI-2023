Supplementary Material for "An Experimental Comparison of Multiwinner Voting Rules on Approval Elections" 

====================

To perform the experiments it is necessary to install the following python packages:

1) mapel (for printing the maps)
2) abcvoting (for computing the winning committees)

Moreover, GUROBI is needed.

====================

In order to run the experiments do the following:

# generate elections, compute winning committees, and compute distances between them
> python preparations.py

# generate Figures 1 and 2 (i.e., maps of rules):
> python figure_1_and_2.py

# generate Figure 3 (i.e., matrices with distances):
> python figure_3.py

# generate data for Tables 1 and 2 (i.e., Priceability, EJR, PJR, JR, Core):
> python tables_1_and_2.py

====================

