# CNM_2025_group_14
Our code simulates the evolution of a pollutant concentration in  a river. Thanks to our code, we can be able to how its concentration changes along the river over time. Our model is done such as the simulation is true at any time and any point in the domain.

Our code is able to provide plots for a polluant transport problem such as one displaying pollutant concentration against distance downstream and another one against time at the upstream boundary(at x=0) so that it is going to be possible to compare them.  To run this part, the plots are going to be saved and are NOT being displayed.
The solver part uses a differential equation to solve a linear equation in order to simulates the transports of the pollutant. It creates uniform spatial and temporal grids and control the accuracy thanks to the courant number in order to attempt the forward substitution where all these coefficients are occuting. It also applies boundary conditions at x=0. To run this part, we have to create a main script by inputing the values of all the different parameters.


This is actually what our 5 test cases does as it give some specific conditions in order to see how it is actually going to evoluates with these given values. It is also helping us to see what impact it is going to have such as  how sensitive our model results are to its parameters and how a decaying concentration will alter our results. All these are helping us to understand the behavior of this pollutant in the river. 
