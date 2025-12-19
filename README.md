# CNM_2025_group_14
1.Project intro:
Our code simulates the evolution of a pollutant concentration in  a river. Thanks to our code, we can be able to how its concentration changes along the river over time. Our model is done such as the simulation is true at any time and any point in the domain.

2. Project structure:
Our project is organised in different folders in order to make it more easier to use. The data file contains the initial conditions given in the task. The src folder contains the major code part with all the test cases we conducted, the solver (in this project of a specific differential equation), and the plotting code. There is also the tests files where the plots and all the tests are saved automatically when you run the code.

3. Project overview:
Our code is able to provide plots for a polluant transport problem such as one displaying pollutant concentration against distance downstream and another one against time at the upstream boundary(at x=0) so that it is going to be possible to compare them. When running the code, the plots are going to be saved and are NOT being displayed directly.
We introduced a solver part that uses a differential equation to solve a linear equation in order to simulates the transports of the pollutant. It creates uniform spatial and temporal grids and control the accuracy thanks to the courant number in order to attempt the forward substitution where all these coefficients are occuting. It also applies boundary conditions at x=0. To run this part, we have to create a main script by inputing the values of all the different parameters.

4. Test cases:
This is actually what our 5 test cases does as it give some specific conditions in order to see how it is actually going to evoluates with these given values. It is also helping us to see what impact it is going to have and to understand the behavior of this pollutant in the river.
For example, the first test case is acting on a 1D model extending to a 20m downstream (with a 20 cm spatial resolution) of the point that the pollutant is entering the river. The idea is to see how it is going to move over the five minutes after he enters the river. The second test case acts on the same model domain but according with our initial conditions so that we will be able to have different simulations to compare and have a better understanding. The third test case showcases the sensitivity of the model result to its parameters. The fourth test case tries to see how an expontially decaying initial concentration of the pollutant in time can alter our results whereas the fifth case tests how the variable stream velocity can alter our results.

6. How to run the code: To run a specific file, you can use the command run.py which is going to run the script. But before that, it is good to install dependencies such as requirements.txt. Its command is represented by "pip install -r requirements.txt". Another dependencies is pytest which is used for all testings.
