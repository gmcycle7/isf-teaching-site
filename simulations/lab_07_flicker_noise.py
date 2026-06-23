"""
lab_07_flicker_noise.py

Goal
----
Show 1/f (flicker) noise upconversion and the role of the ISF DC term c0:

  * Generate flicker current noise (S_i ~ 1/f).
  * Pass it through a SYMMETRIC ISF (c0 = 0) and an ASYMMETRIC ISF (c0 != 0).
  * The asymmetric case lets near-DC flicker noise survive the ISF product,
    which the integrator then shapes into a steep 1/f^3 close-in phase noise.
  * The symmetric case suppresses close-in flicker upconversion.

This is the simulation behind Hajimiri-Lee's central design insight: waveform
symmetry (small c0) suppresses 1/f^3 phase noise (Eq. (23),(24)).

Figure produced
---------------
  static/figures/flicker_upconversion_symmetric_vs_asymmetric.png
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt

from noise_utils import flicker_noise, estimate_psd
from plot_utils import savefig
# Canonical ISF toy models — single source of truth (simulations.common.isf_utils).
from isf_utils import gamma_symmetric, gamma_asymmetric

RNG = np.random.default_rng(7)


def phase_from_isf(i_n, gamma_vals, q_max, fs):
    g = gamma_vals * i_n / q_max
    phi = np.cumsum(g) / fs
    return phi - np.mean(phi)


def main():
    print("[lab_07] flicker noise upconversion ...")
    f0 = 1.0
    fs = 256.0
    n = 2 ** 20
    t = np.arange(n) / fs
    q_max = 1.0

    theta = 2 * np.pi * f0 * t
    # Use the canonical ISF toy models (single source of truth) instead of
    # re-deriving cos(theta) inline. gamma_symmetric has DC = 0 (c0 = 0);
    # gamma_asymmetric(theta, alpha=0.5) shifts DC to 0.5 (c0 = 2*alpha = 1.0).
    gamma_sym = gamma_symmetric(theta)              # c0 = 0
    gamma_asym = gamma_asymmetric(theta, alpha=0.5)  # c0 = 1.0 (DC = 0.5)

    i_flicker = flicker_noise(n, fs, k_flicker=1e-4, rng=RNG)

    phi_sym = phase_from_isf(i_flicker, gamma_sym, q_max, fs)
    phi_asym = phase_from_isf(i_flicker, gamma_asym, q_max, fs)

    f, S_sym = estimate_psd(phi_sym, fs, nperseg=2 ** 16)
    _, S_asym = estimate_psd(phi_asym, fs, nperseg=2 ** 16)

    # Numerical backing for the symmetry claim: in the close-in (lowest-f) band
    # the asymmetric ISF (c0 != 0) upconverts flicker noise into a steep 1/f^3
    # skirt, while the symmetric ISF (c0 = 0) suppresses it. The ratio of the
    # close-in S_asym to S_sym therefore grows toward DC and is >> 1.
    close_in = (f > 0.0) & (f < 2e-2)
    ratio_close_in = np.median(S_asym[close_in] / S_sym[close_in])
    print(f"[lab_07] close-in (low-f) S_asym/S_sym median ratio = "
          f"{ratio_close_in:.1f}  (expect >> 1)")

    mask = (f > 2e-2) & (f < fs / 4)

    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    ax.loglog(f[mask], S_asym[mask], color="tab:red", lw=1.1,
              label=r"asymmetric ISF ($c_0\neq 0$): 強 close-in $1/f^3$")
    ax.loglog(f[mask], S_sym[mask], color="tab:green", lw=1.1,
              label=r"symmetric ISF ($c_0=0$): close-in 被抑制")

    # 1/f^3 and 1/f^2 guide lines
    fref = 0.05
    s_ref = S_asym[np.argmin(np.abs(f - fref))]
    ax.loglog(f[mask], s_ref * (fref / f[mask]) ** 3, "k:", lw=1.0,
              label=r"$1/f^3$ slope (-30 dB/dec)")
    s_ref2 = S_sym[np.argmin(np.abs(f - 0.3))]
    ax.loglog(f[mask], s_ref2 * (0.3 / f[mask]) ** 2, color="gray", ls="--",
              lw=0.9, label=r"$1/f^2$ slope (-20 dB/dec)")

    ax.set_xlabel(r"offset frequency $f$ (normalized, $f_0=1$)")
    ax.set_ylabel(r"$S_\phi(f)$ [rad$^2$/Hz]")
    ax.set_title(r"Flicker upconversion: ISF 對稱性 ($c_0$) 決定 close-in $1/f^3$")
    ax.legend(fontsize=8)
    ax.grid(True, which="both", alpha=0.3)
    savefig(fig, "flicker_upconversion_symmetric_vs_asymmetric.png")


if __name__ == "__main__":
    main()
