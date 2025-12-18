from pathlib import Path
import numpy as np


#importing necessary information from other sections of code
from src import variables
from src.solver import make_grid, solve
from src.testcases_1_3 import (
    case_1,
    case_2,
)
from src.testcases_4_5 import (
    case_4,
    case_5,
)
from src.plotting import plot_profile, plot_time_series, plot_multiple_profiles

#define helper functions for plotting
def _fmt_u(u_val: float) -> str:
    return f"u = {u_val:.3f} m/s"


def _fmt_dx(dx_val: float) -> str:
    return f"Δx = {dx_val:.3f} m"


def _fmt_dt(dt_val: float) -> str:
    return f"Δt = {dt_val:.1f} s"

#define output folder
#to run all test cases and save plots
def main():
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)       #ensure results folder exists

    L = variables.L                        #loads model settings from variables.py
    T = variables.T
    dx = variables.dx
    dt = variables.dt
    u = variables.u
    theta_source = variables.theta_source

    x, t = make_grid(L, T, dx, dt)         #build baseline grid used for test cases 1, 2, 4, 5

    
    #Test Case 1

    #retrieves conditions from test case 1 and solves for theta
    title = "Test Case 1: Concentration vs distance (baseline case)"
    theta0, theta_x0, u_out = case_1(x, t, theta_source, u)
    Theta = solve(theta0, theta_x0, x, t, u_out, dx, dt)

    #boundary condition vs time plot
    plot_time_series(
        t,
        theta_x0,
        results_dir / "case1_boundary_condition.png",
        "Test Case 1: Concentration vs time at x = 0",
    )
    #concentration vs distance at final time plot
    plot_profile(
        x,
        Theta[-1, :],
        t[-1],
        results_dir / "case1_final_profile.png",
        title,
    )

    
    #Test case 2

    #read initial conditions, apply same boundary conditions and solve for theta
    title = "Test Case 2: Concentration vs distance (initial condition from CSV)"
    csv_path = "data/initial_conditions.csv"
    theta0, theta_x0, u_out = case_2(x, t, theta_source, u, csv_path)
    Theta = solve(theta0, theta_x0, x, t, u_out, dx, dt)

    #plot concentration vs distance at final time
    plot_profile(
        x,
        Theta[-1, :],
        t[-1],
        results_dir / "case2_final_profile.png",
        title,
    )


    
    #Test Case 3

    #Create standard grid
    x_ref, t_ref = make_grid(L, T, dx, dt)

    #3A: sensitivity to u
    #builds conditions with different values of u and solves for theta
    title_u = "Test Case 3: Concentration vs distance (sensitivity to u)"
    u_values = [0.5 * u, u, 2.0 * u]

    profiles_u, labels_u = [], []
    for u_val in u_values:
        theta0, theta_x0, u_out = case_1(x_ref, t_ref, theta_source, u_val)
        Theta_u = solve(theta0, theta_x0, x_ref, t_ref, u_out, dx, dt)
        profiles_u.append(Theta_u[-1, :])
        labels_u.append(_fmt_u(u_val))

    #plots all values of u on same figure
    plot_multiple_profiles(
        x_ref,
        profiles_u,
        labels_u,
        t_ref[-1],
        results_dir / "case3_sensitivity_to_u.png",
        title_u,
    )

    #3B: sensitivity to dx
    #builds grid with each value of dx and solves
    #interpolates final profile onto x_ref
    title_dx = "Test Case 3: Concentration vs distance (sensitivity to Δx)"
    dx_values = [dx, 0.5 * dx]

    profiles_dx, labels_dx = [], []
    for dx_val in dx_values:
        x_s, t_s = make_grid(L, T, dx_val, dt)
        theta0, theta_x0, u_out = case_1(x_s, t_s, theta_source, u)
        Theta_s = solve(theta0, theta_x0, x_s, t_s, u_out, dx_val, dt)
        profiles_dx.append(np.interp(x_ref, x_s, Theta_s[-1, :]))
        labels_dx.append(_fmt_dx(dx_val))

    #plots both profiles together
    plot_multiple_profiles(
        x_ref,
        profiles_dx,
        labels_dx,
        t_ref[-1],
        results_dir / "case3_sensitivity_to_dx.png",
        title_dx,
    )

    #3C sensitivity to dt
    #builds grid with each value of dt and solves
    #interpolates final profile onto x_ref
    title_dt = "Test Case 3: Concentration vs distance (sensitivity to Δt)"
    dt_values = [dt, 0.5 * dt]

    profiles_dt, labels_dt = [], []
    for dt_val in dt_values:
        x_s, t_s = make_grid(L, T, dx, dt_val)
        theta0, theta_x0, u_out = case_1(x_s, t_s, theta_source, u)
        Theta_s = solve(theta0, theta_x0, x_s, t_s, u_out, dx, dt_val)
        profiles_dt.append(np.interp(x_ref, x_s, Theta_s[-1, :]))
        labels_dt.append(_fmt_dt(dt_val))

    #plots both profiles together
    plot_multiple_profiles(
        x_ref,
        profiles_dt,
        labels_dt,
        t_ref[-1],
        results_dir / "case3_sensitivity_to_dt.png",
        title_dt,
    )

    
    #Test case 4 (decaying BC)

    #boundary concentration decreases exponentially
    #creates initial spike then exponential decrease
    decay_rate = 0.01  # 1/s
    title = "Test Case 4: Concentration vs distance (decaying source)"
    theta0, theta_x0, u_out = case_4(x, t, theta_source, u, decay_rate)
    Theta = solve(theta0, theta_x0, x, t, u_out, dx, dt)

    #BC vs time plot
    plot_time_series(
        t,
        theta_x0,
        results_dir / "case4_boundary_condition.png",
        "Test Case 4: Concentration vs time at x = 0",
    )

    #final concentration profile plot
    plot_profile(
        x,
        Theta[-1, :],
        t[-1],
        results_dir / "case4_final_profile.png",
        title,
    )

    
    #Test Case 5 - Variable Velocity

    #case_5 returns a varying velocity field - often an array
    #seed makes this reproducible
    #solves for theta
    title = "Test Case 5: Concentration vs distance (variable velocity)"
    theta0, theta_x0, u_out = case_5(x, t, theta_source, u, seed=0)
    Theta = solve(theta0, theta_x0, x, t, u_out, dx, dt)

    #plots final profile of concentration against distance at final time
    plot_profile(
        x,
        Theta[-1, :],
        t[-1],
        results_dir / "case5_final_profile.png",
        title,
    )

#if this file is run directly, main() will be executed 
if __name__ == "__main__":
    main()
