"""
lab_06_white_noise_phase_noise.py

Goal
----
Demonstrate, end to end, how WHITE current noise becomes 1/f^2 phase noise:

    i_n(t)  --x Gamma(w0 t)/q_max-->  --integrate-->  phi(t)

The integrator (infinite memory) turns a flat input into a 1/f^2 output PSD.
We compare the simulated phase PSD to the theory line

    S_phi(f) = Gamma_rms^2 * S_i / ( q_max^2 * (2 pi f)^2 ).

NOTE on the factor of 2: this clean time-domain derivation gives the prefactor
above. Hajimiri-Lee Eq. (21) carries an extra 1/2 (i.e. /4 instead of /2 in the
SSB form) from single-sideband bookkeeping; that well-known constant-factor
subtlety does not change the Gamma_rms^2/q_max^2 scaling or the -20 dB/decade
slope, which are the physics that matter. (See white_noise_to_phase_noise.md.)

Everything here is in NORMALIZED units (f0 = 1). Absolute dBc/Hz numbers are
worked analytically in the docs and in lab_08.

Figure produced
---------------
  static/figures/white_noise_phase_noise_psd.png
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt

from noise_utils import white_noise, estimate_psd
from isf_utils import gamma_lc_ideal, gamma_rms
from plot_utils import savefig

RNG = np.random.default_rng(2024)


def main():
    print("[lab_06] white noise -> 1/f^2 phase noise ...")
    f0 = 1.0
    fs = 256.0                 # 256 samples per period
    n = 2 ** 20                # ~4096 periods -> good low-freq resolution
    t = np.arange(n) / fs

    q_max = 1.0
    S_i = 1.0e-4               # one-sided white current PSD [A^2/Hz] (normalized)

    # ISF and its rms
    theta_grid = np.linspace(0, 2 * np.pi, 4000, endpoint=True)
    Grms = gamma_rms(theta_grid, gamma_lc_ideal(theta_grid))  # = 1/sqrt(2)

    # 1) white current noise
    i_n = white_noise(n, psd=S_i, fs=fs, rng=RNG)
    # 2) ISF weighting
    g = gamma_lc_ideal(2 * np.pi * f0 * t) * i_n / q_max
    # 3) integrate (cumulative) -> excess phase
    dt = 1.0 / fs
    phi = np.cumsum(g) * dt
    phi = phi - np.mean(phi)   # remove the random-walk DC offset for PSD est.

    # 4) estimate phase PSD
    f, Sphi = estimate_psd(phi, fs, nperseg=2 ** 16)

    # theory line
    mask = (f > 2e-2) & (f < fs / 4)
    Sphi_theory = Grms ** 2 * S_i / (q_max ** 2 * (2 * np.pi * f) ** 2)

    # quantify the theory match over the valid band (expect ~1.0)
    print("Sphi/theory median ratio:",
          round(float(np.median(Sphi[mask] / Sphi_theory[mask])), 3))

    fig, ax = plt.subplots(figsize=(8.0, 5.0))
    ax.loglog(f[mask], Sphi[mask], color="tab:blue", lw=1.0, alpha=0.7,
              label="simulated $S_\\phi(f)$")
    ax.loglog(f[mask], Sphi_theory[mask], "k--",
              label=r"theory $\Gamma_{rms}^2 S_i/(q_{max}^2(2\pi f)^2)$")
    # reference -20 dB/decade guide
    fref = 0.1
    guide = Sphi_theory[np.argmin(np.abs(f - fref))] * (fref / f[mask]) ** 2
    ax.loglog(f[mask], guide, color="tab:red", ls=":", lw=1.2,
              label="-20 dB/decade ($1/f^2$) slope")
    ax.set_xlabel(r"offset frequency $f$ (normalized, $f_0=1$)")
    ax.set_ylabel(r"$S_\phi(f)$ [rad$^2$/Hz]")
    ax.set_title(fr"White current noise $\to$ $1/f^2$ phase noise "
                 fr"($\Gamma_{{rms}}$={Grms:.3f})")
    ax.legend()
    ax.grid(True, which="both", alpha=0.3)
    savefig(fig, "white_noise_phase_noise_psd.png")


if __name__ == "__main__":
    main()
