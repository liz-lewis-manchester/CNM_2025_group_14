"""
Declaring the variables of the system
User-defined model inputs.
Designed for the user to edit the values below to change the simulation.

"""

#Spatial and temporal domain
L = 20.0        # Length of model in metres (m)
T = 300.0       # Length of test in seconds (s)

#Spacial and temporal resolution
dx = 0.2        # in metres (m)
dt = 10.0       # in seconds (s)

#Velcoity of the stream
u = 0.1         # (m/s)

#Initial pollutant concentration at x=0 - boundary condition
theta_source = 250.0  # micro-g/m^3