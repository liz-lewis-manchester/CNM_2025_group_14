import numpy as np 
import pytest

from src.testcases_1_3 import (
    bc_constant,
    case_1,
)

from src.testcases_4_5 import (
    bc_exp_decay,
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
