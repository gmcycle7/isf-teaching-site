"""
lab_17_design_sweep.py

Goal
----
Turn the ISF phase-noise law into DESIGN trade-off curves. From [P1] Eq.(21),
in the 1/f^2 region at a fixed offset:

    L proportional to  Gamma_rms^2 / q_max^2 / dw^2

so phase noise improves as:
  * q_max increases  -> -20 dB per decade of q_max (e.g. 2x swing -> -6 dB)
  * Gamma_rms decreases -> -20 dB per decade
  * (ring) increasing N at fixed f0/power: Gamma_rms ~ N^-3/2 BUT more noisy
    devices and lower per-node q_max roughly cancel -> ~flat (the famous
    N-independence). [P2], constants flagged for manual verification.

Figure
------
  static/figures/design_tradeoff_sweeps.png
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt
from plot_utils import savefig


def L_dbc(Grms, qmax, in2_df, dw):
    return 10 * np.log10(Grms ** 2 / qmax ** 2 * in2_df / (4 * dw ** 2))


def main():
    print("[lab_17] design trade-off sweeps ...")
    dw = 2 * np.pi * 1e6   # evaluate at 1 MHz offset
    in2_df = 1e-22
    fig, axes = plt.subplots(1, 3, figsize=(14.5, 4.4))

    # (a) sweep q_max
    ax = axes[0]
    q = np.logspace(-13, -11, 50)  # 0.1 pC .. 10 pC
    ax.semilogx(q / 1e-12, L_dbc(0.5, q, in2_df, dw), color="tab:blue")
    ax.set_xlabel("$q_{max}$ [pC]")
    ax.set_ylabel("$\\mathcal{L}$(1 MHz) [dBc/Hz]")
    ax.set_title("(a) swing↑ → PN↓（$-20$ dB/dec；2× → $-6$ dB）")
    # annotate -6 dB for 2x
    q1 = 1e-12; q2 = 2e-12
    ax.annotate("", xy=(2, L_dbc(0.5, q2, in2_df, dw)), xytext=(1, L_dbc(0.5, q1, in2_df, dw)),
                arrowprops=dict(arrowstyle="->", color="tab:red"))
    ax.text(1.05, L_dbc(0.5, q1, in2_df, dw) + 1, "2× swing\n−6 dB", color="tab:red", fontsize=8)

    # (b) sweep Gamma_rms
    ax = axes[1]
    g = np.linspace(0.1, 1.5, 50)
    ax.plot(g, L_dbc(g, 1e-12, in2_df, dw), color="tab:green")
    ax.set_xlabel("$\\Gamma_{rms}$")
    ax.set_ylabel("$\\mathcal{L}$(1 MHz) [dBc/Hz]")
    ax.set_title("(b) 對稱波形／低 $\\Gamma_{rms}$ → PN↓")

    # (c) ring: N sweep — Gamma_rms ~ N^-3/2, but per-node q_max ~ 1/N and
    # device count ~ N at fixed power roughly cancel -> ~flat
    ax = axes[2]
    N = np.arange(3, 31)
    Grms_N = 0.5 * (5.0 / N) ** 1.5            # scaling (illustrative)
    qmax_N = 1e-12 * (5.0 / N)                 # lower per-node swing as N grows
    noise_N = in2_df * (N / 5.0)               # more noisy devices
    L_N = 10 * np.log10(Grms_N ** 2 / qmax_N ** 2 * noise_N / (4 * dw ** 2))
    ax.plot(N, L_N, "o-", color="tab:purple")
    ax.set_xlabel("ring stages $N$")
    ax.set_ylabel("$\\mathcal{L}$(1 MHz) [dBc/Hz]")
    ax.set_title("(c) 固定 $f_0$,$P$：PN 幾乎與 $N$ 無關（[P2]，常數待查）")

    savefig(fig, "design_tradeoff_sweeps.png")


if __name__ == "__main__":
    main()
