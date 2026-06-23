"""
signal_utils.py — small generic signal helpers (time axes, unwrapping,
edge detection) shared by the ISF labs.
"""
import numpy as np


def time_axis(fs, duration):
    """Uniformly sampled time vector [0, duration) at rate fs. Returns (t, dt)."""
    dt = 1.0 / fs
    n = int(round(duration * fs))
    t = np.arange(n) * dt
    return t, dt


def instantaneous_phase(x, analytic=True):
    """
    Estimate the instantaneous (unwrapped) phase of a real oscillatory signal
    using the analytic signal (Hilbert transform).
    """
    from scipy.signal import hilbert

    z = hilbert(x)
    return np.unwrap(np.angle(z))


def zero_crossings_rising(x, t):
    """Return the (interpolated) times of rising zero crossings of x(t)."""
    s = np.signbit(x)
    idx = np.where((~s[1:]) & (s[:-1]))[0]  # - to + transition
    cross_t = []
    for i in idx:
        x0, x1 = x[i], x[i + 1]
        t0, t1 = t[i], t[i + 1]
        if x1 != x0:
            cross_t.append(t0 + (t1 - t0) * (0 - x0) / (x1 - x0))
        else:
            cross_t.append(t0)
    return np.array(cross_t)


def period_jitter(edge_times, T_nominal):
    """
    period jitter: deviation of each measured period from nominal.
    Returns array of (T_k - T_nominal).
    """
    periods = np.diff(edge_times)
    return periods - T_nominal


def cycle_to_cycle_jitter(edge_times):
    """cycle-to-cycle jitter: difference between consecutive periods, T_{k+1}-T_k."""
    periods = np.diff(edge_times)
    return np.diff(periods)


def db10(x):
    """10*log10 with a floor to avoid -inf."""
    x = np.asarray(x, dtype=float)
    return 10 * np.log10(np.maximum(x, 1e-300))


def db20(x):
    """20*log10 with a floor."""
    x = np.asarray(x, dtype=float)
    return 20 * np.log10(np.maximum(np.abs(x), 1e-300))
