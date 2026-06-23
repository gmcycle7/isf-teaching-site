"""
lab_01_sinusoidal_oscillator.py

Goal
----
Build geometric intuition for oscillator phase:
  * the limit cycle in 2-D state space,
  * the difference between PHASE perturbation (tangential, persists) and
    AMPLITUDE perturbation (radial, decays back to the limit cycle),
  * why a current impulse at the waveform PEAK changes amplitude only, while
    at the ZERO CROSSING it changes phase only.

Figures produced
----------------
  static/figures/limit_cycle_phase_amplitude.png
  static/figures/waveform_with_impulse_markers.png

Corresponds to: Hajimiri-Lee (1998) Fig. 4 (impulse at peak vs zero crossing,
state-space limit cycle) and docs/02_foundations/oscillator_phase.md.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt

from oscillator_models import simulate_lc, sinusoidal_oscillator
from plot_utils import savefig


def fig_limit_cycle():
    f0 = 1.0  # normalized
    fs = 4000.0

    # Limit cycle: integrate with amplitude restoration from an off-cycle start.
    t, x, y = simulate_lc(f0, t_end=3.0, fs=fs, mu=0.6, x0=1.7, y0=0.0)

    fig, ax = plt.subplots(figsize=(6.2, 6.0))
    # ideal unit-circle limit cycle
    th = np.linspace(0, 2 * np.pi, 400)
    ax.plot(np.cos(th), np.sin(th), "k--", lw=1.4, label="limit cycle (穩態軌跡)")
    # relaxing trajectory
    ax.plot(x, y, color="tab:blue", lw=1.0, alpha=0.8,
            label="amplitude 擾動後鬆弛回 limit cycle")

    # operating point
    p = np.array([np.cos(np.pi / 4), np.sin(np.pi / 4)])
    ax.plot(*p, "o", color="black", ms=7)
    # tangential (phase) arrow
    tang = np.array([-p[1], p[0]]) * 0.45
    ax.annotate("", xy=p + tang, xytext=p,
                arrowprops=dict(arrowstyle="->", color="tab:green", lw=2.4))
    ax.text(*(p + tang + [0.05, 0.05]), "phase 擾動 Δφ\n(切線方向，持續累積)",
            color="tab:green", fontsize=9)
    # radial (amplitude) arrow
    rad = p * 0.45
    ax.annotate("", xy=p + rad, xytext=p,
                arrowprops=dict(arrowstyle="->", color="tab:red", lw=2.4))
    ax.text(*(p + rad + [0.04, -0.12]), "amplitude 擾動 ΔA\n(徑向，會被拉回)",
            color="tab:red", fontsize=9)

    ax.set_aspect("equal")
    ax.set_xlim(-2.0, 2.0)
    ax.set_ylim(-2.0, 2.0)
    ax.set_xlabel("state $x$ (e.g. 電容電壓, normalized)")
    ax.set_ylabel("state $y$ (e.g. 電感電流, normalized)")
    ax.set_title("Limit cycle: phase (tangential) vs amplitude (radial) 擾動")
    ax.legend(loc="upper right", fontsize=8)
    savefig(fig, "limit_cycle_phase_amplitude.png")


def fig_impulse_markers():
    f0 = 1.0
    fs = 4000.0
    t = np.arange(int(2.0 * fs)) / fs
    v = sinusoidal_oscillator(t, f0, amp=1.0)

    fig, ax = plt.subplots(figsize=(8.2, 4.2))
    ax.plot(t, v, color="tab:blue", label=r"$V(t)=\cos(2\pi f_0 t)$")

    # peak (theta = 0) -> amplitude change only
    t_peak = 0.0
    ax.plot(t_peak, 1.0, "v", color="tab:red", ms=12)
    ax.annotate("impulse @ peak\n→ 只有 ΔA, 無 Δφ  (Γ≈0)",
                xy=(t_peak, 1.0), xytext=(0.05, 1.35),
                color="tab:red", fontsize=9,
                arrowprops=dict(arrowstyle="->", color="tab:red"))

    # zero crossing (theta = pi/2 -> t = 0.25 T) -> phase change only
    t_zc = 0.25 / f0
    ax.plot(t_zc, 0.0, "v", color="tab:green", ms=12)
    ax.annotate("impulse @ zero crossing\n→ 最大 Δφ, 無 ΔA  (|Γ| 最大)",
                xy=(t_zc, 0.0), xytext=(0.30, 0.55),
                color="tab:green", fontsize=9,
                arrowprops=dict(arrowstyle="->", color="tab:green"))

    ax.axhline(0, color="gray", lw=0.6)
    ax.set_xlabel("time $t$ (periods)")
    ax.set_ylabel("normalized $V(t)$")
    ax.set_title("同樣大小的 impulse，注入相位不同 → 效果完全不同 (LTV 本質)")
    ax.set_xlim(0, 1.5)
    ax.set_ylim(-1.5, 1.7)
    ax.legend(loc="lower right")
    savefig(fig, "waveform_with_impulse_markers.png")


def main():
    print("[lab_01] sinusoidal oscillator / limit cycle ...")
    fig_limit_cycle()
    fig_impulse_markers()


if __name__ == "__main__":
    main()
