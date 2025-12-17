from pathlib import Path
import numpy as np

from src import variables
from src.solver import make_grid, solve
from src.testcases_1_3 import (
    test_case_1,
    test_case_2,
    test_case_3_sets,
)
from src.testcases_4_5 import (
    case_4,
    case_5,
)
from src.plotting import plot_profile, plot_time_series, plot_multiple_profiles


def _fmt_u(u_val: float) -> str:
    return f"u = {u_val:.3f} m/s"


def _fmt_dx(dx_val: float) -> str:
    return f"Δx = {dx_val:.3f} m"


def _fmt_dt(dt_val: float) -> str:
    return f"Δt = {dt_val:.1f} s"


def main():
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    L = variables.L
    T = variables.T
    dx = variables.dx
    dt = variables.dt
    u = variables.u
    theta_source = variables.theta_source

    x, t = make_grid(L, T, dx, dt)

    # -------------------------
    # TEST CASE 1 (baseline)
    # -------------------------
    title = "Test Case 1: Concentration vs distance (baseline case)"
    theta0, theta_x0, u_out = test_case_1(x, t, theta_source, u)
    Theta = solve(theta0, theta_x0, x, t, u_out, dx, dt)

    # BC plot (baseline)
    plot_time_series(
        t,
        theta_x0,
        results_dir / "case1_boundary_condition.png",
        "Test Case 1: Concentration vs time at x = 0",
    )

    plot_profile(
        x,
        Theta[-1, :],
        t[-1],
        results_dir / "case1_final_profile.png",
        title,
    )

    # -------------------------
    # TEST CASE 2 (CSV IC)
    # -------------------------
    title = "Test Case 2: Concentration vs distance (initial condition from CSV)"
    csv_path = "data/initial_conditions.csv"
    theta0, theta_x0, u_out = test_case_2(x, t, theta_source, u, csv_path)
    Theta = solve(theta0, theta_x0, x, t, u_out, dx, dt)

    plot_profile(
        x,
        Theta[-1, :],
        t[-1],
        results_dir / "case2_final_profile.png",
        title,
    )

    # -------------------------
    # TEST CASE 3 (sensitivity)
    # -------------------------
    x_ref, t_ref = make_grid(L, T, dx, dt)

    # 3A: sensitivity to u
    title_u = "Test Case 3: Concentration vs distance (sensitivity to u)"
    u_values = [0.5 * u, u, 2.0 * u]

    profiles_u, labels_u = [], []
    for u_val in u_values:
        theta0, theta_x0, u_out = test_case_1(x_ref, t_ref, theta_source, u_val)
        Theta_u = solve(theta0, theta_x0, x_ref, t_ref, u_out, dx, dt)
        profiles_u.append(Theta_u[-1, :])
        labels_u.append(_fmt_u(u_val))

    plot_multiple_profiles(
        x_ref,
        profiles_u,
        labels_u,
        t_ref[-1],
        results_dir / "case3_sensitivity_to_u.png",
        title_u,
    )

    # 3B: sensitivity to Δx
    title_dx = "Test Case 3: Concentration vs distance (sensitivity to Δx)"
    dx_values = [dx, 0.5 * dx]

    profiles_dx, labels_dx = [], []
    for dx_val in dx_values:
        x_s, t_s = make_grid(L, T, dx_val, dt)
        theta0, theta_x0, u_out = test_case_1(x_s, t_s, theta_source, u)
        Theta_s = solve(theta0, theta_x0, x_s, t_s, u_out, dx_val, dt)
        profiles_dx.append(np.interp(x_ref, x_s, Theta_s[-1, :]))
        labels_dx.append(_fmt_dx(dx_val))

    plot_multiple_profiles(
        x_ref,
        profiles_dx,
        labels_dx,
        t_ref[-1],
        results_dir / "case3_sensitivity_to_dx.png",
        title_dx,
    )

    # 3C: sensitivity to Δt
    title_dt = "Test Case 3: Concentration vs distance (sensitivity to Δt)"
    dt_values = [dt, 0.5 * dt]

    profiles_dt, labels_dt = [], []
    for dt_val in dt_values:
        x_s, t_s = make_grid(L, T, dx, dt_val)
        theta0, theta_x0, u_out = test_case_1(x_s, t_s, theta_source, u)
        Theta_s = solve(theta0, theta_x0, x_s, t_s, u_out, dx, dt_val)
        profiles_dt.append(np.interp(x_ref, x_s, Theta_s[-1, :]))
        labels_dt.append(_fmt_dt(dt_val))

    plot_multiple_profiles(
        x_ref,
        profiles_dt,
        labels_dt,
        t_ref[-1],
        results_dir / "case3_sensitivity_to_dt.png",
        title_dt,
    )

    # -------------------------
    # TEST CASE 4 (decaying BC)
    # -------------------------
    decay_rate = 0.01  # 1/s
    title = "Test Case 4: Concentration vs distance (decaying source)"
    theta0, theta_x0, u_out = case_4(x, t, theta_source, u, decay_rate)
    Theta = solve(theta0, theta_x0, x, t, u_out, dx, dt)

    # BC plot (decaying source)
    plot_time_series(
        t,
        theta_x0,
        results_dir / "case4_boundary_condition.png",
        "Test Case 4: Concentration vs time at x = 0",
    )

    plot_profile(
        x,
        Theta[-1, :],
        t[-1],
        results_dir / "case4_final_profile.png",
        title,
    )

    # -------------------------
    # TEST CASE 5 (variable velocity)
    # -------------------------
    title = "Test Case 5: Concentration vs distance (variable velocity)"
    theta0, theta_x0, u_out = case_5(x, t, theta_source, u, seed=0)
    Theta = solve(theta0, theta_x0, x, t, u_out, dx, dt)

    plot_profile(
        x,
        Theta[-1, :],
        t[-1],
        results_dir / "case5_final_profile.png",
        title,
    )


if __name__ == "__main__":
    main()
