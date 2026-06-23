"""
noise_utils.py — noise generation, PSD estimation, and phase-noise <-> jitter
conversions used throughout the ISF teaching site.

Conventions
-----------
* S_phi(f)        : one-sided phase PSD [rad^2/Hz]
* L(f)            : single-sideband phase noise [dBc/Hz], L(f) ~= 0.5*S_phi(f)
                    (small-angle / single-sideband approximation)
* sigma_phi^2     : integrated phase variance [rad^2]
* sigma_t         : rms timing jitter [s]
"""
import numpy as np
from scipy.signal import welch

# NumPy 2.0 renamed np.trapz -> np.trapezoid; support both.
try:
    from numpy import trapezoid as _trapz
except ImportError:
    from numpy import trapz as _trapz


# ---------------------------------------------------------------------------
# Noise generators
# ---------------------------------------------------------------------------
def white_noise(n, psd, fs, rng=None):
    """
    Generate white noise samples with two-sided PSD `psd` [units^2/Hz] at
    sample rate `fs`. Variance = psd * fs / 2 ... we use the standard relation
    var = psd * (fs/2) for a one-sided PSD interpretation; here we set the
    sample variance so that welch() with scaling='density' recovers `psd`
    as a one-sided density: var = psd * (fs/2).

    Returns an array of length n.
    """
    rng = np.random.default_rng() if rng is None else rng
    # One-sided density `psd` over [0, fs/2] => total power = psd*fs/2 = variance
    sigma = np.sqrt(psd * fs / 2.0)
    return rng.standard_normal(n) * sigma


def flicker_noise(n, fs, k_flicker=1.0, f_low=None, rng=None):
    """
    Generate 1/f (flicker) noise via frequency-domain spectral shaping.

    The one-sided PSD is approximately S(f) = k_flicker / f for f >= f_low.
    `f_low` (default fs/n) sets the lowest resolved frequency to avoid the
    divergence at DC.

    Method: white noise -> rFFT -> scale magnitude by 1/sqrt(f) -> irFFT.
    """
    rng = np.random.default_rng() if rng is None else rng
    w = rng.standard_normal(n)
    F = np.fft.rfft(w)
    f = np.fft.rfftfreq(n, d=1.0 / fs)
    if f_low is None:
        f_low = fs / n
    shape = np.ones_like(f)
    nz = f > 0
    shape[nz] = 1.0 / np.sqrt(np.maximum(f[nz], f_low))
    shape[0] = shape[nz][0] if np.any(nz) else 1.0  # tame DC bin
    x = np.fft.irfft(F * shape, n=n)
    # normalize so that the 1/f level roughly matches k_flicker
    x *= np.sqrt(k_flicker)
    return x


# ---------------------------------------------------------------------------
# PSD estimation
# ---------------------------------------------------------------------------
def estimate_psd(x, fs, nperseg=None):
    """Welch one-sided PSD estimate. Returns (f, Pxx)."""
    if nperseg is None:
        nperseg = min(4096, len(x) // 4)
    nperseg = max(nperseg, 8)
    f, pxx = welch(x, fs=fs, nperseg=nperseg, scaling="density")
    return f, pxx


# ---------------------------------------------------------------------------
# Phase-noise / jitter conversions
# ---------------------------------------------------------------------------
def phase_psd_to_l_dbc_per_hz(s_phi):
    """
    For small phase modulation:  L(f) ~= 0.5 * S_phi(f).
    Returns L in dBc/Hz.
    """
    s_phi = np.asarray(s_phi, dtype=float)
    return 10 * np.log10(0.5 * s_phi)


def phase_to_time_error(phi, f0):
    """Delta t = phi / (2*pi*f0).  phi [rad] -> t [s]."""
    return phi / (2 * np.pi * f0)


def integrate_rms_jitter(f, l_dbc_per_hz, f0, fmin, fmax):
    """
    Convert L(f) in dBc/Hz to phase PSD and integrate to get rms jitter.

        L_linear   = 10^(L_dBc/Hz / 10)
        S_phi      = 2 * L_linear
        sigma_phi  = sqrt( integral_{fmin}^{fmax} S_phi df )
        sigma_t    = sigma_phi / (2*pi*f0)

    Returns (sigma_t [s], sigma_phi [rad]).
    """
    f = np.asarray(f, dtype=float)
    l_dbc_per_hz = np.asarray(l_dbc_per_hz, dtype=float)
    mask = (f >= fmin) & (f <= fmax)
    l_linear = 10 ** (l_dbc_per_hz[mask] / 10)
    s_phi = 2 * l_linear
    sigma_phi = np.sqrt(_trapz(s_phi, f[mask]))
    sigma_t = sigma_phi / (2 * np.pi * f0)
    return sigma_t, sigma_phi


def leeson_one_over_f2(f, L_ref_dbc, f_ref, f0=None):
    """
    Build an idealized 1/f^2 SSB phase-noise skirt anchored at (f_ref, L_ref).

        L(f) = L_ref + 20*log10(f_ref / f)   [dBc/Hz]

    Useful for the jitter-integration lab where we start from a single
    datasheet number such as L(1 MHz) = -100 dBc/Hz.
    """
    f = np.asarray(f, dtype=float)
    return L_ref_dbc + 20 * np.log10(f_ref / f)
