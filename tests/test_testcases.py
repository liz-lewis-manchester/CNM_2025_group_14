import numpy as np 
import pytest

from src.testcases import (
    bc_constant,
    bc_exp_decay,
    ic_from_csv, 
    case_1,
    case_2,
    case_3_sets,
    case_4,
    case_5,
)

def test_boundary_condition_helpers():
    """test boundary condition helper functions; constant boundary condition, exponentially decaying boundary condition
    """
    t = np.array([0.0, 1.0, 2.0])

    bc = bc_constant(t, theta_source=10.0)
    assert bc.shape == t.shape
    assert np.allclose(bc, 10.0)

    bc2 = bc_exp_decay(t, theta_source=10.0, k=0.5)
    assert bc2.shape == t.shape
    assert bc2[0] == pytest.approx(10.0)
    assert bc2[1] < bc2[0]
    assert bc2[2] < bc2[1]

def test_case_1_shapes():
    """
    case 1 should return correctly sized 
    initial condition, boundary condition, and velocity.
    """
    x = np.linspace(0, 1, 6)
    t = np.linspace(0, 1, 4)
    
    theta0, theta_x0, u_out = case_1(x, t, theta_source=10.0, u=0.1)

    assert theta0.shape == x.shape
    assert theta_x0.shape == t.shape
    assert np.isscalar(u_out)


def test_case_3_sets_structure():
    """
    case 3 should return a list of parameter sets
    for sensitivity testing.
    """
    sets = case_3_sets(u=0.1, dx=0.2, dt=10.0)

    assert isinstance(sets, list)
    assert lens(sets) >= 5