import numpy as np
import pandas as pd


# Test Case 4 - exponentially decaying initial concentration of pollutant

def case_4(x, t, theta_source, u, decay_rate):
    theta0 = ic_spike_at_source(x, theta_source)         # Initial conditions: spike at x=0, exp decaying BC at x=0, constant u
    theta_x0 = bc_exp_decay(t, theta_source, decay_rate) # Boundary condition: inlet concentration decays exponentially
    return theta0, theta_x0, float(u)                    # Return constant velocity as a scalar


# Test case 5 - variable stream velocity 

def case_5(x, t, theta_source, u_base, seed=0):          
    theta0 = ic_spike_at_source(x, theta_source)         # Initial condition: Spike in concentration at inlet
    theta_x0 = bc_constant(t, theta_source)              # Boundary condition: Constant inlet concentration over time
    u_x = u_variable_10pct(x, u_base, seed=seed, p=0.10) # Velocity field: Apply ~10% random spatial perturbation to base velocity
    return theta0, theta_x0, u_x