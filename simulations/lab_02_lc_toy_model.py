"""
lab_02_lc_toy_model.py

Goal
----
Show the ideal parallel-LC oscillator state model and its physically-derived
ISF, Gamma(theta) = -sin(theta), and verify the *linearity* of excess phase
vs injected charge for small charge (Hajimiri-Lee Fig. 6).

Figure produced
---------------
  static/figures/lc_waveform_and_isf.png

Corresponds to: Hajimiri-Lee (1998) Figs. 4, 6, 7(a); Eq. (10),(11).
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt

from oscillator_models import simulate_lc, excess_phase
from isf_utils import gamma_lc_ideal
from plot_utils import savefig


def main():
    print("[lab_02] LC toy model: waveform, ISF, charge linearity ...")
    f0 = 1.0
    fs = 8000.0
    theta = np.linspace(0, 2 * np.pi, 400)

    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.2))

    # (a) waveform + ISF over one period
    ax = axes[0]
    ax.plot(theta / (2 * np.pi), np.cos(theta), color="tab:blue",
            label=r"$V(\theta)=\cos\theta$ (tank 電壓)")
    ax.plot(theta / (2 * np.pi), gamma_lc_ideal(theta), color="tab:red",
            label=r"$\Gamma(\theta)=-\sin\theta$ (ISF)")
    ax.axhline(0, color="gray", lw=0.6)
    ax.set_xlabel(r"phase $\theta/2\pi$")
    ax.set_ylabel("normalized")
    ax.set_title("(a) LC 波形與其 ISF")
    ax.legend(fontsize=8)

    # (b) linearity: excess phase vs injected charge (small-signal)
    ax = axes[1]
    dq_list = np.linspace(-0.05, 0.05, 11)  # dq/q_max
    T = 1.0 / f0
    t_end = 10 * T
    # inject at the zero crossing (theta=pi/2) where ISF = -1 (max sensitivity)
    t_inj = 4 * T + (np.pi / 2) / (2 * np.pi * f0)
    t_ref, xr, yr = simulate_lc(f0, t_end, fs, mu=0.3)
    phi_ref = excess_phase(t_ref, xr, yr, f0)
    dphi = []
    for dq in dq_list:
        t_p, xp, yp = simulate_lc(f0, t_end, fs, mu=0.3,
                                  impulse_time=t_inj, impulse_dx=dq)
        phi_p = excess_phase(t_p, xp, yp, f0)
        m = t_p >= (t_end - T)
        dphi.append(np.mean(phi_p[m] - phi_ref[m]))
    dphi = np.array(dphi)
    ax.plot(dq_list, dphi, "o-", color="tab:purple", label="numeric")
    ax.plot(dq_list, -1.0 * dq_list, "k--",
            label=r"theory $\Delta\phi=\Gamma\,\Delta q/q_{max}=-\Delta q/q_{max}$")
    ax.set_xlabel(r"injected charge $\Delta q / q_{max}$")
    ax.set_ylabel(r"excess phase $\Delta\phi$ [rad]")
    ax.set_title("(b) Δφ 與注入電荷成正比 (small-signal)")
    ax.legend(fontsize=8)

    # (c) state-space impulse at zero crossing -> pure phase jump
    ax = axes[2]
    t_p, xp, yp = simulate_lc(f0, 6 * T, fs, mu=0.0, impulse_time=2 * T + 0.25 * T,
                              impulse_dx=0.25)
    th = np.linspace(0, 2 * np.pi, 300)
    ax.plot(np.cos(th), np.sin(th), "k--", lw=1.0, label="unperturbed cycle")
    ax.plot(xp, yp, color="tab:green", lw=1.0, label="impulse @ zero crossing")
    ax.set_aspect("equal")
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.6, 1.6)
    ax.set_xlabel("state $x$")
    ax.set_ylabel("state $y$")
    ax.set_title("(c) zero-crossing 注入 → 相位跳變")
    ax.legend(fontsize=8)

    savefig(fig, "lc_waveform_and_isf.png")


if __name__ == "__main__":
    main()
