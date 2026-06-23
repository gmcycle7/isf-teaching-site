"""
lab_21_topology_isf.py

Goal
----
Illustrate the most important real-topology ISF lesson: in a cross-coupled LC
VCO the DIFFERENTIAL TANK sees a clean fundamental ISF (Gamma ~ -sin, only c1),
but the TAIL current source noise sees an EFFECTIVE ISF rich in a DC term (c0)
and a 2nd-harmonic term (c2). That is why:
  * tail FLICKER noise (near DC) upconverts to close-in 1/f^3 via c0, and
  * tail thermal noise near 2*omega0 folds to the carrier via c2,
motivating a symmetric design plus a tail filter tuned to 2*f0 (Hajimiri-Lee
cyclostationary noise; E. Hajimiri & Andreani tail-noise analyses).

NOTE: this is an ILLUSTRATIVE model of a KNOWN mechanism (the tail effective ISF
is constructed, not extracted from a transistor netlist). The tank ISF -sin is
exact for an ideal LC.

Figure
------
  static/figures/cross_coupled_vco_isf.png
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt
from isf_utils import compute_fourier_coefficients, gamma_rms
from plot_utils import savefig


def main():
    print("[lab_21] cross-coupled VCO: tank vs tail effective ISF ...")
    theta = np.linspace(0, 2 * np.pi, 2000, endpoint=True)

    # tank ISF: ideal LC differential node -> exact -sin (only c1)
    gamma_tank = -np.sin(theta)

    # tail effective ISF: illustrative model with DC (c0) + 2nd harmonic (c2).
    # (tail node swings at 2*omega0; switching commutates the tail noise.)
    c0, c2, c1res = 0.30, 0.55, 0.10
    gamma_tail = c0 / 2 + c1res * np.cos(theta) + c2 * np.cos(2 * theta)

    a0_t, a_t, b_t, c_t, _ = compute_fourier_coefficients(theta, gamma_tank, 4)
    a0_e, a_e, b_e, c_e, _ = compute_fourier_coefficients(theta, gamma_tail, 4)

    fig, axes = plt.subplots(1, 2, figsize=(13.5, 4.8))

    ax = axes[0]
    ax.plot(theta / (2 * np.pi), gamma_tank, color="tab:blue",
            label=fr"tank ISF $-\sin\theta$ (純 $c_1$, $\Gamma_{{rms}}$={gamma_rms(theta, gamma_tank):.2f})")
    ax.plot(theta / (2 * np.pi), gamma_tail, color="tab:red",
            label=fr"tail 有效 ISF (含 $c_0,c_2$, $\Gamma_{{rms}}$={gamma_rms(theta, gamma_tail):.2f})")
    ax.axhline(0, color="gray", lw=0.6)
    ax.set_xlabel(r"phase $\theta/2\pi$")
    ax.set_ylabel(r"$\Gamma(\theta)$")
    ax.set_title("(a) cross-coupled VCO：tank 乾淨、tail 有效 ISF 富含諧波（illustrative）")
    ax.legend(fontsize=8)

    ax = axes[1]
    nh = np.arange(5)
    w = 0.38
    ax.bar(nh - w / 2, c_t[:5], width=w, color="tab:blue", label="tank ISF")
    ax.bar(nh + w / 2, c_e[:5], width=w, color="tab:red", label="tail 有效 ISF")
    ax.set_xlabel("harmonic number $n$")
    ax.set_ylabel(r"$|c_n|$")
    ax.set_title("(b) tail 的 $c_0$（flicker 上轉）與 $c_2$（$2\\omega_0$ 折回）才是麻煩")
    ax.set_xticks(nh)
    ax.legend(fontsize=9)
    for i in range(5):
        if c_e[i] > 0.02:
            ax.text(i + w / 2, c_e[i] + 0.01, f"{c_e[i]:.2f}", ha="center", fontsize=7)
    savefig(fig, "cross_coupled_vco_isf.png")


if __name__ == "__main__":
    main()
