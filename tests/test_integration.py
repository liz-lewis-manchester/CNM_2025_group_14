import numpy as np 

from src.solver import make_grid, solve
from src.testcases_1_3 import case_1 

def test_end_to_end_small_run_is_finite():
    """
    End to end integration test; build grid, generate ICs and BCs from case_1, run solver and check output shape, finiteness and BC enforcement
    """
    L, T, dx, dt = 1.0, 0.3, 0.1, 0.1
    u = 0.2
    theta_source = 1.0

    #build grid
    x, t = make_grid(L, T, dx, dt)

    #generate initial and boundary conditions
    theta0, theta_x0, u_out = case_1(x, t, theta_source, u)

    #solve advection equation
    Theta = solve(theta0, theta_x0, x, t, u_out, dx, dt)

    #shape check
    assert Theta.shape == (len(t), len(x))

    #numerical sanity
    assert np.isfinite(Theta).all()

    #boundary condition enforced at x=0
    assert np.allclose(Theta[1:, 0], theta_x0[1:])