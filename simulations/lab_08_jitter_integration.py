"""
lab_08_jitter_integration.py

Goal
----
Turn a datasheet-style SSB phase-noise curve L(f) [dBc/Hz] into an rms timing
jitter, and verify the numerical integral against the 1/f^2 closed form.

Scenario (the canonical "手感" example):
    f0           = 5 GHz
    L(1 MHz)     = -100 dBc/Hz, assumed pure 1/f^2 skirt
    integrate from 1 MHz to 100 MHz

Closed form for a 1/f^2 skirt L(f) = L_ref*(f_ref/f)^2:
    sigma_phi^2 = integral 2*L(f) df = 2 L_ref_lin f_ref^2 (1/f1 - 1/f2)
    sigma_t     = sigma_phi / (2 pi f0)

Figure produced
---------------
  static/figures/phase_noise_to_jitter_integration.png
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt

from noise_utils import leeson_one_over_f2, integrate_rms_jitter
from plot_utils import savefig


def main():
    print("[lab_08] phase noise -> rms jitter integration ...")
    f0 = 5e9
    f_ref = 1e6
    L_ref = -100.0  # dBc/Hz
    f1, f2 = 1e6, 100e6

    f = np.logspace(np.log10(f1), np.log10(f2), 4000)
    L = leeson_one_over_f2(f, L_ref, f_ref)

    # numerical integration
    sigma_t, sigma_phi = integrate_rms_jitter(f, L, f0, f1, f2)

    # analytic closed form (1/f^2)
    L_ref_lin = 10 ** (L_ref / 10)
    sigma_phi2_analytic = 2 * L_ref_lin * f_ref ** 2 * (1 / f1 - 1 / f2)
    sigma_phi_analytic = np.sqrt(sigma_phi2_analytic)
    sigma_t_analytic = sigma_phi_analytic / (2 * np.pi * f0)

    print(f"    sigma_phi (numeric)  = {sigma_phi*1e3:.4f} mrad")
    print(f"    sigma_phi (analytic) = {sigma_phi_analytic*1e3:.4f} mrad")
    print(f"    sigma_t   (numeric)  = {sigma_t*1e15:.2f} fs")
    print(f"    sigma_t   (analytic) = {sigma_t_analytic*1e15:.2f} fs")

    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    ax.semilogx(f, L, color="tab:blue", lw=1.8, label=r"$L(f)$ (1/$f^2$ skirt)")
    ax.fill_between(f, L, L.min() - 5, alpha=0.12, color="tab:blue")
    ax.plot(f_ref, L_ref, "o", color="tab:red")
    ax.annotate(f"L(1 MHz) = {L_ref:.0f} dBc/Hz", xy=(f_ref, L_ref),
                xytext=(2e6, L_ref + 8),
                arrowprops=dict(arrowstyle="->", color="tab:red"))
    txt = (f"integrate {f1/1e6:.0f}–{f2/1e6:.0f} MHz\n"
           f"$\\sigma_\\phi$ = {sigma_phi*1e3:.2f} mrad\n"
           f"$\\sigma_t$ = {sigma_t*1e15:.1f} fs\n"
           f"(analytic {sigma_t_analytic*1e15:.1f} fs)")
    ax.text(0.62, 0.72, txt, transform=ax.transAxes, fontsize=10,
            bbox=dict(boxstyle="round", fc="white", ec="gray"))
    ax.set_xlabel("offset frequency $f$ [Hz]")
    ax.set_ylabel("$L(f)$ [dBc/Hz]")
    ax.set_title(r"Phase noise $\to$ rms jitter ($f_0$ = 5 GHz)")
    ax.legend(loc="lower left")
    savefig(fig, "phase_noise_to_jitter_integration.png")


if __name__ == "__main__":
    main()
