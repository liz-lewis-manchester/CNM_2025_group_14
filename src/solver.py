import numpy as np

  # Make x and t grids
def make_grid(L, T, dx, dt):
  
    # Number of spatial and temporal points (includes both endpoints)
    nx = int(round(L / dx)) + 1
    nt = int(round(T / dt)) + 1

    # Uniform grids in space and time
    x = np.linspace(0.0, float(L), nx)
    t = np.linspace(0.0, float(T), nt)
    return x, t


# Courant number
def courant(u, dt, dx):
    u_arr = np.asarray(u, dtype=float) # Convert u to a NumPy array to allow both scalar and array input
    c = u_arr * float(dt) / float(dx) # Courant number
    return float(np.max(c))


# a and b arrays
def _coefficients(u, dt, dx, nx):
    if np.isscalar(u):
        u_x = np.full(nx, float(u), dtype=float)
    else:
        u_x = np.asarray(u, dtype=float)
        if u_x.shape[0] != nx:
            raise ValueError("u(x) must have length nx")

    a = 1.0 / float(dt) + u_x / float(dx)
    b = u_x / float(dx)
    return a, b


# One time step solve using forward substitution (lower triangular)
def forward_substitution(theta_old, a, b, theta_left, dt):
    nx = theta_old.shape[0]
    theta_new = np.zeros(nx, dtype=float)

    theta_new[0] = float(theta_left)
    f = theta_old / float(dt)

    for i in range(1, nx):
        theta_new[i] = (f[i] + b[i] * theta_new[i - 1]) / a[i]

    return theta_new


# Solve the 1D advection equation using backward Euler in time 
# and backward difference in space
def solve(theta0, theta_x0, x, t, u, dx, dt, cfl_warn=1.0):
    x = np.asarray(x, dtype=float)
    t = np.asarray(t, dtype=float)
    theta0 = np.asarray(theta0, dtype=float)
    theta_x0 = np.asarray(theta_x0, dtype=float)

    nx = x.size
    nt = t.size

    if theta0.size != nx:
        raise ValueError("theta0 must have length nx")
    if theta_x0.size != nt:
        raise ValueError("theta_x0 must have length nt")

    c = courant(u, dt, dx) # Compuete the Courant number and warn if large
    if c > float(cfl_warn):
        print(f"warning: max(u*dt/dx) = {c:.3f} > {cfl_warn} (accuracy may drop)")

    a, b = _coefficients(u, dt, dx, nx)

    Theta = np.zeros((nt, nx), dtype=float) # Set initial condition
    Theta[0, :] = theta0

    theta_old = theta0.copy()

    # Time-stepping loop
    for n in range(1, nt):
        theta_left = theta_x0[n]
        theta_new = forward_substitution(theta_old, a, b, theta_left, dt) # Solve for new time step

        Theta[n, :] = theta_new
        theta_old = theta_new

    return Theta
