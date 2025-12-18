import numpy as np
import pandas as pd


# TEST CASE 4: Decaying upstream boundary concentration (exponential decay)

# Create a spike at x = 0 and zero everywhere else
def ic_spike_at_source(x, theta_source):
    theta0 = np.zeros_like(x, dtype=float)
    theta0[0] = float(theta_source)
    return theta0


# Upstream boundary decays over time: theta(t, 0) = theta_source * exp(-k t)
def bc_exp_decay(t, theta_source, k):
    return float(theta_source) * np.exp(-float(k) * t)


# Set up everything needed for test case 4
def case_4(x, t, theta_source, u, decay_rate):
    # Initial condition: spike at x = 0
    theta0 = ic_spike_at_source(x, theta_source)

    # Boundary condition: exponential decay at x = 0
    theta_x0 = bc_exp_decay(t, theta_source, decay_rate)

    # Constant velocity
    return theta0, theta_x0, float(u)


# TEST CASE 5: Variable velocity along the channel

# Keep the upstream boundary concentration constant in time
def bc_constant(t, theta_source):
    return np.full_like(t, float(theta_source), dtype=float)


# Create a velocity profile u(x) with random perturbations around u_base
def u_variable_10pct(x, u_base, seed=0, p=0.10):
    rng = np.random.default_rng(int(seed))
    eps = rng.uniform(-float(p), float(p), size=len(x))
    u_x = float(u_base) * (1.0 + eps)

    # Just in case, keep it non-negative
    return np.maximum(u_x, 0.0)


# Set up everything needed for test case 5
def case_5(x, t, theta_source, u_base, seed=0):
    # Initial condition: spike at x = 0
    theta0 = ic_spike_at_source(x, theta_source)

    # Boundary condition: constant at x = 0
    theta_x0 = bc_constant(t, theta_source)

    # Variable velocity profile u(x)
    u_out = u_variable_10pct(x, u_base, seed=seed, p=0.10)

    return theta0, theta_x0, u_out
