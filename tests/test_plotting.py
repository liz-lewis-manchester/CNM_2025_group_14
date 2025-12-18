import os
#using non-interactive backend means tests can run headlessly
os.environ["MPLBACKEND"] = "Agg"

import numpy as np 

from src.plotting import (
    plot_profile,
    plot_time_series,
    plot_multiple_profiles,
)

def test_plot_profile_creates_file(tmp_path):
    """
    check that plot_profile runs without error and creates a non empty output file
    """
    x = np.linspace(0, 1, 10)
    theta = np.linspace(0, 1, 10)

    out = tmp_path / "profile.png"
    plot_profile(
        x,
        theta,
        1.0,
        out,
        "Test Case 1: Concentration vs distance (baseline case)",
    )

    assert out.exists()
    assert out.stat().st_size > 0


def test_plot_time_series_creates_file(tmp_path):
    """
    checking that plot_time_series runs without error and creates a non empty output file
    """
    t = np.linspace(0, 1, 10)
    theta_x0 = np.ones_like(t)

    out = tmp_path / "bc.png"
    plot_time_series(
        t,
        theta_x0,
        out,
        "test case 1: concentration vs time at x=0",
    )
    assert out.exists()
    assert out.stat().st_size > 0


def test_plot_multiple_profiles_creates_file(tmp_path):
    """
    check that plot_multiple_profiles runs without error and creates a non empty output file
    """
    x = np.linspace(0, 1, 10)
    profiles = [
        np.linspace(0, 1, 10),
        np.linspace(0, 0.5, 10),
    ]
    labels = ["baseline", "variant"]

    out = tmp_path / "multi.png"
    plot_multiple_profiles(
        x,
        profiles,
        labels,
        1.0,
        out,
        "test case 3: concentration vs distance", 
    )

    assert out.exists()
    assert out.stat().st_size > 0
