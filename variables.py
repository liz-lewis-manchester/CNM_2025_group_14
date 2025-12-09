#Code to declare variables

import numpy as np
import pandas as pd

#Initialise model demain and variables
def variables():
  L = 20.0    #domain length (m)
  U = 0.1     #velocity (m/s)
  T = 300     #domain time(s)
  dx = 0.2    #spacial resolution (m)
  dt = 10     #timestep (s)

  print("enter model parameters (or press enter to use default results):")

  # helper to read input with fallback default
  def get_value(prompt, default):
    value = input(f"{prompt} [{default}]: ").strip()
    return float(value) if value else default

  L = get_value("Domain length L (m)", L_default)
  U = get_value("Velocity U (m/s)", U_default)
  T = get_value("Simulation time T (s)", T_default)
  dx = get_value("Spatial resolution dx (m)", dx_default)
  dt = get_value("Timestep dt (s)", dt_default)
  
  return(L, U, T, dx, dt)
L, U, T, dx, dt = variables()

#Number of discrete intervals in space and time
Nx = int(L/dx) + 1
Nt = int(T/dt)
x = np.linspace(0, L, Nx)

#Theta is the pollutant concentration
#An array to hold the current solution
theta_new = np.zeros(Nx)

#An array to store the previous solution
theta_old = np.zeros(Nx)

#Arrays to hold the martrix coefficients
A = np.zeros(Nx-1)
B= np.zeros(Nx-1)

#Right hand side array
F = np.zeros(Nx-1)

#Check if u = constant or u = u(x) and define array
if np.isscalar(U):
  u_array = np.full(Nx -1, U)

else:
  u_array = np.array(U)
  if len(u_array) != Nx-1:
    raise ValueError("Velocity array U(x) must be a list or array with Nx-1 values")

#Values of A and B based on U, dx and dt
A[:] = u_array * dt/dx
B[:] = 1 - A[:]

#Read in initial condictions 
df = pd.read_csv("initial_conditions.csv", encoding="latin1")
x_data = df.iloc[:, 0].to_numpy(float)
c_data = df.iloc[:, 1].to_numpy(float)
theta_old = np.interp(x, x_data, c_data, left=c_data[0], right=c_data[-1]) 




