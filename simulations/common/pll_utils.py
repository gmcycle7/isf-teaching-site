"""
pll_utils.py — second-order PLL / CDR jitter-transfer helpers for the ISF site.

A type-II second-order PLL has open-loop gain that gives a closed-loop response
where, referred to the OUTPUT phase:

  * reference / divider phase noise is LOW-PASS filtered  -> H_lp(s)
  * the VCO's own phase noise is HIGH-PASS filtered       -> H_hp(s) = 1 - H_lp(s)

Standard normalized forms (natural frequency w_n, damping zeta):

  H_lp(s) = (2 zeta w_n s + w_n^2) / (s^2 + 2 zeta w_n s + w_n^2)
  H_hp(s) = s^2 / (s^2 + 2 zeta w_n s + w_n^2)

This is exactly why a clean reference + a noisy ring VCO can still give a good
clock: the loop tracks (passes) low-offset noise from the reference but
suppresses the VCO's close-in noise, while the VCO dominates far out.

A CDR behaves like the loop seen by the *data*: it tracks low-frequency input
jitter (low-pass) and rejects high-frequency jitter (the jitter-tolerance
corner).

All transfer functions here are POWER transfers |H(j2*pi*f)|^2 unless noted.
These are first-order pedagogical models, not a specific silicon loop.
"""
import numpy as np


def loop_natural_freq(fn_hz):
    """Convenience: natural frequency w_n [rad/s] from f_n [Hz]."""
    return 2 * np.pi * fn_hz


def H_lowpass_mag2(f, fn_hz, zeta=0.707):
    """|H_lp(j2*pi*f)|^2 for a type-II 2nd-order PLL (reference -> output)."""
    w = 2 * np.pi * np.asarray(f, dtype=float)
    wn = loop_natural_freq(fn_hz)
    num = (2 * zeta * wn * w) ** 2 + wn ** 4
    den = (wn ** 2 - w ** 2) ** 2 + (2 * zeta * wn * w) ** 2
    return num / den


def H_highpass_mag2(f, fn_hz, zeta=0.707):
    """|H_hp(j2*pi*f)|^2 = |1 - H_lp|^2 for the VCO -> output path."""
    w = 2 * np.pi * np.asarray(f, dtype=float)
    wn = loop_natural_freq(fn_hz)
    num = w ** 4
    den = (wn ** 2 - w ** 2) ** 2 + (2 * zeta * wn * w) ** 2
    return num / den


def shape_output_phase_noise(f, S_ref, S_vco, fn_hz, zeta=0.707):
    """
    Closed-loop output phase-noise PSD:

        S_out(f) = S_ref(f) * |H_lp|^2 + S_vco(f) * |H_hp|^2

    Returns (S_out, S_ref_shaped, S_vco_shaped).
    """
    lp = H_lowpass_mag2(f, fn_hz, zeta)
    hp = H_highpass_mag2(f, fn_hz, zeta)
    sref = np.asarray(S_ref) * lp
    svco = np.asarray(S_vco) * hp
    return sref + svco, sref, svco
