import os
from typing import List, Sequence, Optional

import numpy as np
import matplotlib.pyplot as plt


# -------------------------------------------------------------------
# Utility: ensure the output directory exists
# -------------------------------------------------------------------

def _ensure_dir(filename: str) -> str:
    """
    Ensures `filename` exists.
    If not there, save into a default 'results' folder.
    Returns the updated filename.
    """
    directory = os.path.dirname(filename)

    if directory == "":
        directory = "results"
        filename = os.path.join(directory, filename)

    os.makedirs(directory, exist_ok=True)
    return filename


# -------------------------------------------------------------------
# 1. Final concentration profile
# -------------------------------------------------------------------

def plot_final_profile(
    x: np.ndarray,
    theta_final: np.ndarray,
    filename: str,
    title: str = "Final concentration profile",
    label: Optional[str] = None,
) -> None:
    """
    Plot the pollutant concentration θ(x) at a single chosen time.
    """
    filename = _ensure_dir(filename)

    plt.figure(figsize=(8, 4))

    if label:
        plt.plot(x, theta_final, linewidth=2, label=label)
        plt.legend()
    else:
        plt.plot(x, theta_final, linewidth=2)

    plt.xlabel("Distance x (m)")
    plt.ylabel("Concentration θ (µg/m³)")
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


# -------------------------------------------------------------------
# 2. Time evolution of θ(x, t)
# -------------------------------------------------------------------

def plot_time_evolution(
    x: np.ndarray,
    theta_all: np.ndarray,
    dt: float,
    filename: str,
    title: str = "Pollutant transport over time",
    n_curves: int = 6,
    specific_times: Optional[Sequence[float]] = None,
) -> None:
    """
    Plot of concentration profiles to show how θ(x, t) evolves.
    """
    filename = _ensure_dir(filename)

    Nt_plus_1, _ = theta_all.shape
    Nt = Nt_plus_1 - 1

    # Decide which time indices to include
    if specific_times:
        inds = []
        for t in specific_times:
            idx = int(round(t / dt))
            idx = max(0, min(idx, Nt))
            inds.append(idx)
        time_indices = sorted(set(inds))
    else:
        # Evenly spaced time slices
        n_curves = max(2, min(n_curves, Nt_plus_1))
        time_indices = np.linspace(0, Nt, n_curves, dtype=int)

    plt.figure(figsize=(9, 5))

    for idx in time_indices:
        t = idx * dt
        plt.plot(x, theta_all[idx], linewidth=1.8, label=f"t = {t:.0f} s")

    plt.xlabel("Distance x (m)")
    plt.ylabel("Concentration θ (µg/m³)")
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


# -------------------------------------------------------------------
# 3. Initial CSV data vs interpolated grid values
# -------------------------------------------------------------------

def plot_initial_vs_interpolated(
    x_data: np.ndarray,
    c_data: np.ndarray,
    x_grid: np.ndarray,
    c_interp: np.ndarray,
    filename: str,
    title: str = "Initial conditions: data vs interpolated values",
) -> None:
    """
    Compare the raw initial condition data from CSV with the interpolated model grid.
    """
    filename = _ensure_dir(filename)

    plt.figure(figsize=(8, 4))
    plt.scatter(x_data, c_data, s=30, label="CSV data")
    plt.plot(x_grid, c_interp, linewidth=2, label="Interpolated")

    plt.xlabel("Distance x (m)")
    plt.ylabel("Concentration θ (µg/m³)")
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


# -------------------------------------------------------------------
# 4. Parameter sensitivity plots (U, dx, dt, etc.)
# -------------------------------------------------------------------

def plot_parameter_sensitivity(
    x: np.ndarray,
    profiles: List[np.ndarray],
    labels: List[str],
    filename: str,
    title: str = "Sensitivity analysis",
) -> None:
    """
    Plot multiple final concentration profiles together to compare parameter effects.
    """
    if len(profiles) != len(labels):
        raise ValueError("profiles and labels must have same length.")

    filename = _ensure_dir(filename)

    plt.figure(figsize=(9, 5))

    for theta, lab in zip(profiles, labels):
        plt.plot(x, theta, linewidth=2, label=lab)

    plt.xlabel("Distance x (m)")
    plt.ylabel("Concentration θ (µg/m³)")
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


# -------------------------------------------------------------------
# 5. Velocity profile u(x)
# -------------------------------------------------------------------

def plot_velocity_profile(
    x: np.ndarray,
    u_array: np.ndarray,
    filename: str,
    title: str = "Velocity profile u(x)",
    base_U: Optional[float] = None,
) -> None:
    """
    Plot the velocity distribution u(x) used in Case 5.
    """
    filename = _ensure_dir(filename)

    plt.figure(figsize=(8, 4))
    plt.plot(x, u_array, linewidth=2, label="u(x)")

    if base_U is not None:
        plt.axhline(base_U, linestyle="--", linewidth=1.5, label=f"U = {base_U:.3f}")

    plt.xlabel("Distance x (m)")
    plt.ylabel("Velocity (m/s)")
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()