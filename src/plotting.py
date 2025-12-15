import matplotlib.pyplot as plt


_Y_LABEL = "Pollutant concentration, Θ (µg/m³)"
_X_LABEL = "Distance downstream, x (m)"
_T_LABEL = "Time, t (s)"


def _style(ax):
    ax.grid(True, which="both", linestyle="--", linewidth=0.6, alpha=0.6)


def plot_profile(x, theta, time, filename, title):
    """plot Θ vs x at a given time"""
    fig, ax = plt.subplots()

    ax.plot(x, theta)
    ax.set_xlabel(_X_LABEL)
    ax.set_ylabel(_Y_LABEL)
    ax.set_title(title + f"\nProfile at t = {time:.0f} s")
    _style(ax)

    fig.tight_layout()
    fig.savefig(str(filename), dpi=200)
    plt.close(fig)


def plot_time_series(t, theta_x0, filename, title):
    """plot Θ at x=0 vs time"""
    fig, ax = plt.subplots()

    ax.plot(t, theta_x0)
    ax.set_xlabel(_T_LABEL)
    ax.set_ylabel(_Y_LABEL)
    ax.set_title(title + "\nUpstream boundary concentration at x = 0")
    _style(ax)

    fig.tight_layout()
    fig.savefig(str(filename), dpi=200)
    plt.close(fig)


def plot_multiple_profiles(x, profiles, labels, time, filename, title):
    """plot multiple Θ(x) curves on one figure"""
    fig, ax = plt.subplots()

    for theta, label in zip(profiles, labels):
        ax.plot(x, theta, label=label)

    ax.set_xlabel(_X_LABEL)
    ax.set_ylabel(_Y_LABEL)
    ax.set_title(title + f"\nFinal-time comparison at t = {time:.0f} s")
    ax.legend()
    _style(ax)

    fig.tight_layout()
    fig.savefig(str(filename), dpi=200)
    plt.close(fig)
