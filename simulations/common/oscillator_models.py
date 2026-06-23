"""
oscillator_models.py — toy oscillator models for the ISF labs.

Contents
--------
1. sinusoidal_oscillator      : the simplest carrier model V(t)=A cos(w0 t+phi)
2. simulate_lc / lc_limit_cycle: 2-D state-space LC oscillator with optional
                                 amplitude restoration (limit cycle) and an
                                 injectable current impulse.
3. extract_isf_by_injection   : numerically recover Gamma(theta) for the LC
                                 model by sweeping the injection phase.
4. ring_edge_times            : N-stage ring oscillator modeled at the level of
                                 transition (edge) times with per-edge timing
                                 noise -> accumulated (random-walk) jitter.
5. phase_to_time              : Delta t = phi/(2 pi f0).

ALL of these are TOY MODELS. They reproduce the *mechanisms* of the LTV
phase-noise theory, not transistor-level numbers. Limitations are documented
on each lab page and in docs/00_overview/build_report.md.
"""
import numpy as np

TWO_PI = 2.0 * np.pi


# ---------------------------------------------------------------------------
# 1. Sinusoidal carrier
# ---------------------------------------------------------------------------
def sinusoidal_oscillator(t, f0, amp=1.0, phi0=0.0):
    """V(t) = amp * cos(2*pi*f0*t + phi0)."""
    return amp * np.cos(TWO_PI * f0 * t + phi0)


def phase_to_time(phi, f0):
    """Delta t = phi / (2*pi*f0).  phi [rad] -> t [s]."""
    return phi / (TWO_PI * f0)


# ---------------------------------------------------------------------------
# 2. LC oscillator state-space model (limit cycle)
# ---------------------------------------------------------------------------
def _lc_deriv(x, y, w0, mu):
    """
    State derivative for a normalized 2-D oscillator:

        dx/dt = -w0*y + mu*(1 - r^2)*x
        dy/dt =  w0*x + mu*(1 - r^2)*y      (r^2 = x^2 + y^2)

    mu = 0  -> ideal lossless LC (pure rotation, marginally stable amplitude).
    mu > 0  -> Van der Pol-like amplitude restoration; the trajectory relaxes
               onto the unit-radius limit cycle, modeling the AGC / device
               nonlinearity that every real oscillator must have.
    """
    r2 = x * x + y * y
    g = mu * (1.0 - r2)
    return (-w0 * y + g * x, w0 * x + g * y)


def simulate_lc(f0, t_end, fs, mu=0.0, x0=1.0, y0=0.0,
                impulse_time=None, impulse_dx=0.0):
    """
    Integrate the 2-D LC oscillator with RK4.

    A current impulse injected into the capacitor node produces an
    instantaneous voltage step dv = dq/C; in normalized units (A=1, q_max=C*A=C)
    this is a step impulse_dx = dq/q_max added to the x-state at impulse_time.

    Returns (t, x, y).
    """
    w0 = TWO_PI * f0
    dt = 1.0 / fs
    n = int(round(t_end * fs))
    t = np.arange(n) * dt
    x = np.empty(n)
    y = np.empty(n)
    xi, yi = float(x0), float(y0)
    imp_idx = int(round(impulse_time * fs)) if impulse_time is not None else -1

    for k in range(n):
        x[k] = xi
        y[k] = yi
        if k == imp_idx:
            xi += impulse_dx  # charge impulse -> voltage step on the x state
        k1x, k1y = _lc_deriv(xi, yi, w0, mu)
        k2x, k2y = _lc_deriv(xi + 0.5 * dt * k1x, yi + 0.5 * dt * k1y, w0, mu)
        k3x, k3y = _lc_deriv(xi + 0.5 * dt * k2x, yi + 0.5 * dt * k2y, w0, mu)
        k4x, k4y = _lc_deriv(xi + dt * k3x, yi + dt * k3y, w0, mu)
        xi += dt / 6.0 * (k1x + 2 * k2x + 2 * k3x + k4x)
        yi += dt / 6.0 * (k1y + 2 * k2y + 2 * k3y + k4y)

    return t, x, y


def excess_phase(t, x, y, f0):
    """
    Excess phase phi(t) = unwrap(atan2(y,x)) - 2*pi*f0*t.
    Removes the carrier rotation so only the perturbation-induced phase remains.
    """
    inst = np.unwrap(np.arctan2(y, x))
    return inst - TWO_PI * f0 * t


def extract_isf_by_injection(f0, fs, n_inject_periods=6, settle_periods=4,
                             dq_over_qmax=1e-3, n_points=64, mu=0.3):
    """
    Numerically recover the ISF Gamma(theta) of the LC limit-cycle model by
    injecting a small charge impulse at many phases theta = w0*tau and reading
    off the persistent excess phase shift:

        Gamma(theta) ~= (dphi_persistent) / (dq/q_max)

    Returns (theta_array, gamma_numeric, gamma_analytic) where the analytic
    prediction is Gamma(theta) = -sin(theta).
    """
    T = 1.0 / f0
    settle = settle_periods * T
    t_end = (settle_periods + n_inject_periods) * T
    thetas = np.linspace(0.0, TWO_PI, n_points, endpoint=False)
    gamma_num = np.zeros(n_points)

    # Reference (no impulse), started from the limit cycle.
    t_ref, xr, yr = simulate_lc(f0, t_end, fs, mu=mu, x0=1.0, y0=0.0)
    phi_ref = excess_phase(t_ref, xr, yr, f0)

    for i, th in enumerate(thetas):
        t_inj = settle + th / (TWO_PI * f0)  # phase th occurs at this time
        t_p, xp, yp = simulate_lc(f0, t_end, fs, mu=mu, x0=1.0, y0=0.0,
                                  impulse_time=t_inj, impulse_dx=dq_over_qmax)
        phi_p = excess_phase(t_p, xp, yp, f0)
        # persistent phase difference measured over the last period
        m = t_p >= (t_end - T)
        dphi = np.mean(phi_p[m] - phi_ref[m])
        gamma_num[i] = dphi / dq_over_qmax

    gamma_analytic = -np.sin(thetas)
    return thetas, gamma_num, gamma_analytic


# ---------------------------------------------------------------------------
# 4. Ring oscillator timing-noise (edge-time) model
# ---------------------------------------------------------------------------
def ring_edge_times(n_periods, f0, sigma_edge, rng=None):
    """
    Model an N-stage ring oscillator at the level of output transition times.

    Each period the edge picks up an INDEPENDENT timing perturbation with
    standard deviation `sigma_edge` (seconds). Because each perturbation is
    added to the running edge time, the *absolute* edge time performs a random
    walk -> accumulated jitter variance grows linearly with the number of
    cycles (sigma ~ sqrt(Delta t)). This is the hallmark of an open-loop
    oscillator with no absolute time reference.

    Returns the array of edge times (length n_periods+1).
    """
    rng = np.random.default_rng() if rng is None else rng
    T = 1.0 / f0
    per_period = T + sigma_edge * rng.standard_normal(n_periods)
    edges = np.concatenate(([0.0], np.cumsum(per_period)))
    return edges


def accumulated_jitter_curve(f0, sigma_edge, max_lag_periods=400,
                             n_trials=400, rng=None):
    """
    Estimate the accumulated-jitter function sigma_dt(Delta N) of the ring
    model: the rms spread of (t_{k+m} - t_k) over many trials, for lag m.

    Returns (lag_periods, sigma_dt). Theory: sigma_dt = sigma_edge * sqrt(m).
    """
    rng = np.random.default_rng() if rng is None else rng
    T = 1.0 / f0
    lags = np.arange(1, max_lag_periods + 1)
    # Each trial: a random walk increment per period.
    incr = sigma_edge * rng.standard_normal((n_trials, max_lag_periods))
    walk = np.cumsum(incr, axis=1)  # walk[:, m-1] = sum of first m increments
    sigma_dt = np.std(walk, axis=0)
    return lags, sigma_dt
