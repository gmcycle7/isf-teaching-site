"""
lab_14_cyclostationary_isf.py

Goal
----
Show cyclostationary noise via the effective ISF. A device (e.g. a tail current
or a switching transistor) only injects noise during PART of the period. Model
that "when is the device noisy" with a periodic noise-modulating function (NMF)
alpha(theta) in [0,1]. The phase-noise-relevant sensitivity is then the
EFFECTIVE ISF, Gamma_eff = Gamma * alpha. WHERE alpha overlaps the ISF matters.

Figure
------
  static/figures/cyclostationary_effective_isf.png
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt
from isf_utils import gamma_lc_ideal, gamma_rms, effective_isf
from plot_utils import savefig


def nmf_window(theta, center, width):
    """Smooth periodic gate in [0,1], centered at `center`, of given width (rad)."""
    d = np.angle(np.exp(1j * (theta - center)))  # wrapped distance
    return 0.5 * (1 + np.cos(np.pi * np.clip(d / (width / 2), -1, 1)))


def main():
    print("[lab_14] cyclostationary effective ISF ...")
    theta = np.linspace(0, 2 * np.pi, 2000, endpoint=True)
    gamma = gamma_lc_ideal(theta)  # -sin

    # case 1: device noisy near the ZERO CROSSING (where |Gamma| is max) -> bad
    a_bad = nmf_window(theta, center=np.pi / 2, width=np.pi)
    # case 2: device noisy near the PEAK (where |Gamma|~0) -> good
    a_good = nmf_window(theta, center=0.0, width=np.pi)

    g_bad = effective_isf(gamma, a_bad)
    g_good = effective_isf(gamma, a_good)

    grms = gamma_rms(theta, gamma)
    grms_bad = gamma_rms(theta, g_bad)
    grms_good = gamma_rms(theta, g_good)

    fig, axes = plt.subplots(1, 2, figsize=(13.0, 4.8))

    ax = axes[0]
    ax.plot(theta / (2 * np.pi), gamma, color="black", label=r"$\Gamma=-\sin\theta$")
    ax.plot(theta / (2 * np.pi), a_bad, color="tab:red", ls="--",
            label=r"$\alpha$（noise 在 zero crossing）")
    ax.plot(theta / (2 * np.pi), a_good, color="tab:green", ls="--",
            label=r"$\alpha$（noise 在 peak）")
    ax.set_xlabel(r"phase $\theta/2\pi$")
    ax.set_ylabel("value")
    ax.set_title("(a) ISF 與兩種 NMF $\\alpha(\\theta)$")
    ax.legend(fontsize=8)

    ax = axes[1]
    ax.plot(theta / (2 * np.pi), g_bad, color="tab:red",
            label=fr"$\Gamma_{{eff}}$ (bad) rms={grms_bad:.3f}")
    ax.plot(theta / (2 * np.pi), g_good, color="tab:green",
            label=fr"$\Gamma_{{eff}}$ (good) rms={grms_good:.3f}")
    ax.axhline(0, color="gray", lw=0.6)
    ax.set_xlabel(r"phase $\theta/2\pi$")
    ax.set_ylabel(r"$\Gamma_{eff}=\Gamma\cdot\alpha$")
    ax.set_title(fr"(b) 同一顆 device，注入相位決定 $\Gamma_{{eff,rms}}$ "
                 fr"(stationary={grms:.3f})")
    ax.legend(fontsize=8)
    savefig(fig, "cyclostationary_effective_isf.png")
    print(f"    Gamma_rms stationary={grms:.3f}, bad={grms_bad:.3f}, good={grms_good:.3f}")


if __name__ == "__main__":
    main()
