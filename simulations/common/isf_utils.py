"""
isf_utils.py — Impulse Sensitivity Function (ISF) toy models and operators.

These functions implement, in the cleanest possible way, the mathematical
objects of the Hajimiri-Lee LTV phase-noise theory:

    phi(t) = (1/q_max) * integral_{-inf}^{t} Gamma(omega0*tau) * i_n(tau) dtau

References
----------
A. Hajimiri and T. H. Lee, "A General Theory of Phase Noise in Electrical
Oscillators," IEEE J. Solid-State Circuits, vol. 33, no. 2, pp. 179-194,
Feb. 1998.  (Eqs. (10)-(13), (20).)

NOTE: gamma_symmetric / gamma_asymmetric below are *pedagogical toy ISFs*.
They are NOT extracted from any transistor-level oscillator. The physically
derived ideal-LC ISF is gamma_lc_ideal(theta) = -sin(theta) (see derivation
in docs/03_isf_core_theory/isf_definition.md).
"""
import numpy as np

# NumPy 2.0 renamed np.trapz -> np.trapezoid; support both.
try:
    from numpy import trapezoid as _trapz
except ImportError:  # numpy < 2.0
    from numpy import trapz as _trapz


def wrap_phase(theta):
    """Wrap phase to [0, 2*pi)."""
    return np.mod(theta, 2 * np.pi)


def gamma_symmetric(theta):
    """
    Example *symmetric* ISF toy model: Gamma(theta) = cos(theta).

    This is not a universal oscillator ISF. It is a pedagogical toy model
    whose DC (average) value is exactly zero, representing a perfectly
    symmetric waveform (no 1/f upconversion via the c0 term).
    """
    theta = wrap_phase(theta)
    return np.cos(theta)


def gamma_asymmetric(theta, alpha=0.3):
    """
    Example *asymmetric* ISF toy model: Gamma(theta) = cos(theta) + alpha.

    alpha shifts the DC value, so the Fourier coefficient c0 (= 2*alpha here)
    becomes non-zero. This is the knob that controls 1/f-noise upconversion
    into close-in phase noise (Hajimiri-Lee Eq. (24)).
    """
    theta = wrap_phase(theta)
    return np.cos(theta) + alpha


def gamma_lc_ideal(theta):
    """
    Physically derived ISF of an *ideal* lossless parallel-LC oscillator for a
    current injected into the capacitor node:

        Gamma(theta) = -sin(theta)

    Derivation: state z=(v,w)=A(cos theta, sin theta); a charge impulse shifts
    v by dv=dq/C; the induced phase shift is dphi = -(sin theta)/A * dv, and
    with q_max = C*A this gives dphi = Gamma(theta)/q_max * dq with
    Gamma(theta) = -sin(theta). Maximum |Gamma| at the zero crossing
    (theta = pi/2), zero at the peak (theta = 0).
    """
    return -np.sin(theta)


def gamma_triangular(theta, n_stages=5):
    """
    Crude triangular ISF toy model meant to evoke a ring-oscillator ISF whose
    energy concentrates at the transitions. Peak height shrinks with the
    number of stages (slope gets steeper as N grows), echoing the
    Gamma_rms ~ 1/N^{3/2} scaling argued in Hajimiri-Limotyrakis-Lee (1999).

    This is a TOY MODEL, not an extracted ring ISF.
    """
    theta = wrap_phase(theta)
    # Two transitions per period (rising + falling edge), triangular bumps.
    x = theta / (2 * np.pi)
    tri = np.abs(((x * 2) % 1.0) - 0.5) * 2.0  # 0..1 triangle, period 0.5
    peak = 1.0 / np.sqrt(n_stages)
    return peak * (2 * tri - 1.0)


def impulse_to_phase_step(delta_q, gamma_value, qmax):
    """
    Delta phi = Gamma * Delta q / qmax.

    Parameters
    ----------
    delta_q     : injected charge [C]
    gamma_value : ISF value at the injection phase [dimensionless]
    qmax        : maximum charge displacement (q_max) [C]

    Returns
    -------
    delta_phi   : phase step [rad]
    """
    return gamma_value * delta_q / qmax


def integrate_phase_from_noise(t, i_noise, gamma_values, qmax):
    """
    Numerically integrate the LTV phase response (Hajimiri-Lee Eq. (11)):

        phi(t) = integral Gamma(w0*tau)/qmax * i_noise(tau) dtau

    Implemented as a running (cumulative) integral so that each past
    perturbation persists into the future (the integrator has infinite memory,
    which is exactly why phase error accumulates).

    Parameters
    ----------
    t            : time vector [s] (assumed uniformly sampled)
    i_noise      : noise current samples [A]
    gamma_values : ISF sampled along the trajectory, Gamma(w0*t) [dimensionless]
    qmax         : q_max [C]

    Returns
    -------
    phi(t) [rad]
    """
    dt = np.mean(np.diff(t))
    return np.cumsum(gamma_values * i_noise / qmax) * dt


def apply_isf_weighting(t, i_noise, gamma_func, qmax, omega0):
    """
    The 'ISF multiplier' block:  x(t) = Gamma(omega0*t)/qmax * i_noise(t).

    gamma_func is a callable theta -> Gamma(theta).
    """
    gamma_values = gamma_func(omega0 * t)
    return gamma_values * i_noise / qmax


def compute_fourier_coefficients(theta, gamma, n_harmonics):
    """
    Numerically compute the ISF Fourier coefficients.

        Gamma(theta) ~= a0/2 + sum_n [ a_n cos(n theta) + b_n sin(n theta) ]
                      =  c0/2 + sum_n c_n cos(n theta + phase_n)

    `theta` should span exactly one period [0, 2*pi] (endpoint included) for
    the trapezoidal rule to give the correct (1/pi) * integral over 2*pi.

    Returns
    -------
    a0     : 2 * (DC value)  -> a0/2 is the mean of Gamma; in Hajimiri notation
             c0 = a0 (so the DC term written as c0/2 equals a0/2 = mean).
    a, b   : cosine / sine coefficients, arrays of length (n_harmonics+1)
    c      : magnitudes c_n = sqrt(a_n^2 + b_n^2)
    phase  : phase angles theta_n = atan2(-b_n, a_n)
    """
    theta = np.asarray(theta, dtype=float)
    gamma = np.asarray(gamma, dtype=float)

    a0 = (1 / np.pi) * _trapz(gamma, theta)
    a = np.zeros(n_harmonics + 1)
    b = np.zeros(n_harmonics + 1)

    for n in range(1, n_harmonics + 1):
        a[n] = (1 / np.pi) * _trapz(gamma * np.cos(n * theta), theta)
        b[n] = (1 / np.pi) * _trapz(gamma * np.sin(n * theta), theta)

    c = np.sqrt(a ** 2 + b ** 2)
    c[0] = abs(a0)  # c0 magnitude (the DC coefficient)
    phase = np.arctan2(-b, a)

    return a0, a, b, c, phase


def reconstruct_from_fourier(theta, a0, a, b):
    """Reconstruct Gamma(theta) from its Fourier coefficients (inverse of above)."""
    theta = np.asarray(theta, dtype=float)
    out = np.full_like(theta, a0 / 2.0)
    for n in range(1, len(a)):
        out += a[n] * np.cos(n * theta) + b[n] * np.sin(n * theta)
    return out


def gamma_rms(theta, gamma):
    """
    Gamma_rms = sqrt( (1/2pi) * integral_0^{2pi} Gamma^2 dtheta ).

    `theta` must span one full period [0, 2*pi]. This matches Hajimiri-Lee
    Eq. (20):  sum_{n=0}^inf c_n^2 = (1/pi) integral |Gamma|^2 dx = 2*Gamma_rms^2.
    """
    theta = np.asarray(theta, dtype=float)
    gamma = np.asarray(gamma, dtype=float)
    span = theta[-1] - theta[0]
    mean_sq = _trapz(gamma ** 2, theta) / span
    return np.sqrt(mean_sq)


def effective_isf(gamma_values, alpha_values):
    """
    Effective ISF for a cyclostationary noise source (Hajimiri-Lee Sec. on
    cyclostationary noise):

        Gamma_eff(x) = Gamma(x) * alpha(x)

    where alpha(x) in [0,1] is the periodic noise-modulating function (NMF)
    describing how the device noise power is gated by the operating point
    (e.g. a transistor only injects noise while it conducts).
    """
    return np.asarray(gamma_values) * np.asarray(alpha_values)
