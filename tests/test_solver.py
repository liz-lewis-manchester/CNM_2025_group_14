import numpy as np 
import pytest

from src.solver import make_grid, solve

def test_make_grid_endpoints_and_lengths():
    """
    check that spatial and temporal grids start at 0, end at L and T and have the expected number of points
    """
    L, T, dx, dt = 1.0, 0.3, 0.1, 0.1

    x, t = make_grid(L, T, dx, dt)

    #endpoints
    assert x[0] == pytest.approx(0.0)
    assert x[-1] == pytest.approx(L)
    assert t[0] == pytest.approx(0.0)
    assert t[-1] == pytest.approx(T)

    #grid lengths
    assert len(x) == int(round(L / dx)) + 1
    assert len(t) == int(round(T / dt)) + 1

def test_solve_shape_and_ic_bc_enforced():
    """
    toy run of solver to check output array shape, initial condition applied at t=0, boundary condition enforced at x=0, and solution contains no NaNs or Infs
    """
    L, T, dx, dt = 1.0, 0.3, 0.1, 0.1
    u = 0.2

    x, t = make_grid(L, T, dx, dt)
    nx, nt = len(x), len(t)

    #initial condition = zero everywhere except boundary
    theta0 = np.zeros(nx)
    theta0 = 1.0

    #boundary condition = constant concentration at x=0
    theta_x0 = np.full(nt, 1.0)

    Theta = solve(theta0, theta_x0, x, t, u, dx, dt)

    #shape check
    assert Theta.shape == (nt, nx)

    #applying initial condition 
    assert np.allclose(Theta[0, :], theta0)

    #boundary condition enforced
    assert np.allclose(Theta[:, 0], theta_x0)

    #numerical sanity
    assert np.isfinite(Theta).all()

def test_solve_raises_for_bad_lengths():
    """
    solver should raise value error if array lengths do not match the grid sizes
    """
    x = np.linspace(0, 1, 6)
    t = np.linspace(0, 1, 4)
    dx = x[1] - x[0]
    dt = t[1] - t[0]

    #wrong theta0 length
    with pytest.raises(ValueError):
        solve(
            theta0=np.zeros(5),
            theta_x0=np.zeros(4),
            x=x,
            t=t,
            u=0.1,
            dx=dx,
            dt=dt,
        )
    #wrong theta_x0 length
    with pytest.raises(ValueError):
        solve(
            theta0=np.zeros(6),
            theta_x0=np.zeros(3),
            x=x,
            t=t,
            u=0.1,
            dx=dx,
            dt=dt,
        )
