"""
serdes_utils.py — SerDes eye-diagram and BER helpers driven by oscillator jitter.

The whole point of the ISF curriculum for a SerDes designer: oscillator phase
noise integrates to an rms timing jitter sigma_t; that sigma_t is the random
jitter (RJ) of the sampling clock; RJ closes the eye and sets the BER.

For random (Gaussian) jitter only, the bit-error rate when sampling at offset
t from the eye center (one edge at -UI/2, one at +UI/2) is

    BER(t) = 1/2 * [ Q((UI/2 - t)/sigma_t) + Q((UI/2 + t)/sigma_t) ]

with Q(x) = 1/2 erfc(x/sqrt(2)). The classic "bathtub" curve.

These are first-order models: RJ only (no ISI/DJ), ideal 2-level data.
"""
import numpy as np
from scipy.special import erfc


def Q(x):
    """Gaussian tail probability Q(x) = 0.5*erfc(x/sqrt(2))."""
    return 0.5 * erfc(np.asarray(x, dtype=float) / np.sqrt(2.0))


def ber_bathtub(t_offsets, sigma_t, ui):
    """
    BER vs sampling-time offset for RJ-only.

    Parameters
    ----------
    t_offsets : array of sampling offsets from eye center [s]
    sigma_t   : rms random jitter [s]
    ui        : unit interval (bit period) [s]

    Returns BER array (clipped to a 1e-300 floor for log plotting).
    """
    t = np.asarray(t_offsets, dtype=float)
    half = ui / 2.0
    ber = 0.5 * (Q((half - t) / sigma_t) + Q((half + t) / sigma_t))
    return np.maximum(ber, 1e-300)


def eye_traces(sigma_t, ui, n_traces=400, n_pts=200, rng=None):
    """
    Generate overlaid NRZ eye-diagram traces with random edge jitter.

    Returns (t_axis [in UI, spanning -1..1], list_of_traces). Each trace is a
    random bit transition whose edge time is perturbed by N(0, sigma_t).
    """
    rng = np.random.default_rng() if rng is None else rng
    t = np.linspace(-1.0, 1.0, n_pts)  # in units of UI
    traces = []
    for _ in range(n_traces):
        # random previous/next bits -> level pattern
        a = rng.integers(0, 2) * 2 - 1
        b = rng.integers(0, 2) * 2 - 1
        jit = rng.normal(0.0, sigma_t / ui)  # edge jitter in UI
        # smooth transition (raised-cosine-ish) centered at 0 + jitter
        x = (t - jit) * np.pi
        edge = 0.5 * (1 + np.tanh(3.0 * (t - jit)))  # 0..1 transition
        trace = a + (b - a) * edge
        traces.append(trace)
    return t, traces
