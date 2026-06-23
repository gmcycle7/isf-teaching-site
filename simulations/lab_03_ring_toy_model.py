"""
lab_03_ring_toy_model.py

Goal
----
Two ring-oscillator intuitions:
  1. Accumulated (random-walk) jitter: sigma_dt grows as sqrt(Delta t).
  2. The ring ISF concentrates at transitions and has a smaller, sharper shape
     than the LC's smooth -sin(theta); rms ISF shrinks as the number of stages
     N grows (Gamma_rms ~ N^{-3/2} scaling argument).

Figures produced
----------------
  static/figures/ring_oscillator_timing_noise_accumulation.png
  static/figures/lc_vs_ring_isf_comparison.png

Corresponds to: Hajimiri-Limotyrakis-Lee (1999), Eqs. (10),(16); Fig. 8.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt

from oscillator_models import accumulated_jitter_curve
from isf_utils import gamma_lc_ideal, gamma_triangular, gamma_rms
from plot_utils import savefig

RNG = np.random.default_rng(12345)


def fig_accumulation():
    f0 = 5e9  # 5 GHz
    sigma_edge = 50e-15  # 50 fs rms per-period timing perturbation
    lags, sigma_dt = accumulated_jitter_curve(
        f0, sigma_edge, max_lag_periods=500, n_trials=2000, rng=RNG)

    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    ax.loglog(lags, sigma_dt / 1e-15, "o", ms=3, color="tab:blue",
              label="simulated (random walk)")
    ax.loglog(lags, sigma_edge * np.sqrt(lags) / 1e-15, "k--",
              label=r"theory $\sigma_{\Delta t}=\sigma_{edge}\sqrt{\Delta N}$")
    ax.set_xlabel(r"measurement interval $\Delta N$ [periods]")
    ax.set_ylabel(r"accumulated jitter $\sigma_{\Delta t}$ [fs]")
    ax.set_title(r"Ring osc: accumulated jitter $\propto\sqrt{\Delta t}$ "
                 r"(no absolute time reference)")
    ax.legend()
    ax.grid(True, which="both", alpha=0.3)
    savefig(fig, "ring_oscillator_timing_noise_accumulation.png")


def fig_lc_vs_ring_isf():
    theta = np.linspace(0, 2 * np.pi, 1000, endpoint=True)
    g_lc = gamma_lc_ideal(theta)
    g_r5 = gamma_triangular(theta, n_stages=5)
    g_r15 = gamma_triangular(theta, n_stages=15)

    fig, ax = plt.subplots(figsize=(8.2, 4.6))
    ax.plot(theta / (2 * np.pi), g_lc, color="tab:blue",
            label=fr"LC: $-\sin\theta$  ($\Gamma_{{rms}}$={gamma_rms(theta, g_lc):.3f})")
    ax.plot(theta / (2 * np.pi), g_r5, color="tab:red",
            label=fr"ring N=5 (toy)  ($\Gamma_{{rms}}$={gamma_rms(theta, g_r5):.3f})")
    ax.plot(theta / (2 * np.pi), g_r15, color="tab:green",
            label=fr"ring N=15 (toy) ($\Gamma_{{rms}}$={gamma_rms(theta, g_r15):.3f})")
    ax.axhline(0, color="gray", lw=0.6)
    ax.set_xlabel(r"phase $\theta/2\pi$")
    ax.set_ylabel(r"$\Gamma(\theta)$ [dimensionless]")
    ax.set_title("LC vs ring ISF (toy):敏感度集中在 transition，N 越大 rms 越小")
    ax.legend(fontsize=8)
    savefig(fig, "lc_vs_ring_isf_comparison.png")


def main():
    print("[lab_03] ring oscillator toy model ...")
    fig_accumulation()
    fig_lc_vs_ring_isf()


if __name__ == "__main__":
    main()
