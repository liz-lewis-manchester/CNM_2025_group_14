import numpy as np
import pandas as pd


# TEST CASE 1: simple spike at the source, constant boundary, constant velocity

# create a spike at x = 0 and zero everywhere else
def ic_spike_at_source(x, theta_source):
    theta0 = np.zeros_like(x, dtype=float)
    theta0[0] = float(theta_source)
    return theta0


# keep the upstream boundary concentration constant
def bc_constant(t, theta_source):
    return np.full_like(t, float(theta_source), dtype=float)


# set up everything needed for test case 1
def case_1(x, t, theta_source, u):
    # initial condition
    theta0 = ic_spike_at_source(x, theta_source)

    # boundary condition at x = 0
    theta_x0 = bc_constant(t, theta_source)

    # constant velocity
    return theta0, theta_x0, float(u)


# TEST CASE 2: initial condition read from CSV, constant boundary, constant velocity

# read initial conditions from CSV and interpolate onto the grid
def ic_from_csv(x, csv_path):
    try:
        df = pd.read_csv(csv_path)
    except UnicodeDecodeError:
        df = pd.read_csv(csv_path, encoding="latin1")

    # assume first column is x and second is theta
    x_data = df.iloc[:, 0].to_numpy(dtype=float)
    th_data = df.iloc[:, 1].to_numpy(dtype=float)

    # sort by x so interpolation works properly
    order = np.argsort(x_data)
    x_data = x_data[order]
    th_data = th_data[order]

    return np.interp(x, x_data, th_data)


# set up everything needed for test case 2
def case_2(x, t, theta_source, u, csv_path):
    # initial condition from CSV
    theta0 = ic_from_csv(x, csv_path)

    # same constant upstream boundary as case 1
    theta_x0 = bc_constant(t, theta_source)

    # constant velocity
    return theta0, theta_x0, float(u)
