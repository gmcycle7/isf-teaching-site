"""
lab_04_impulse_sweep.py

Goal
----
1. Numerically recover the ISF of the LC limit-cycle model by sweeping the
   injection phase, and compare to the analytic prediction Gamma(theta)=-sin(theta).
2. Illustrate LTI vs LTV impulse response: an LTI system's response depends only
   on (t - tau); the oscillator's phase impulse response depends on the
   ABSOLUTE injection phase tau (periodically time-varying sensitivity).

Figures produced
----------------
  static/figures/sinusoidal_impulse_phase_sweep.png
  static/figures/isf_impulse_sweep_sinusoidal.png
  static/figures/lti_vs_ltv_impulse_response.png

Corresponds to: Hajimiri-Lee (1998) Eqs. (10),(11), Figs. 3,4; docs lti_vs_ltv.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt

from oscillator_models import extract_isf_by_injection
from plot_utils import savefig


def fig_isf_sweep():
    f0 = 1.0
    fs = 8000.0
    theta, g_num, g_ana = extract_isf_by_injection(
        f0, fs, n_inject_periods=6, settle_periods=4,
        dq_over_qmax=1e-3, n_points=48, mu=0.3)

    # (1) phase shift vs injection phase
    fig, ax = plt.subplots(figsize=(7.8, 4.4))
    ax.plot(theta / (2 * np.pi), g_num * 1e-3, "o", ms=4, color="tab:blue",
            label=r"numeric $\Delta\phi$ for $\Delta q/q_{max}=10^{-3}$")
    ax.plot(theta / (2 * np.pi), g_ana * 1e-3, "k--",
            label=r"theory $\Delta\phi = -\sin\theta \cdot \Delta q/q_{max}$")
    ax.axhline(0, color="gray", lw=0.6)
    ax.set_xlabel(r"injection phase $\theta/2\pi$")
    ax.set_ylabel(r"persistent $\Delta\phi$ [rad]")
    ax.set_title("Phase shift vs injection phase (LC limit-cycle model)")
    ax.legend()
    savefig(fig, "sinusoidal_impulse_phase_sweep.png")

    # (2) the recovered ISF itself
    fig, ax = plt.subplots(figsize=(7.8, 4.4))
    ax.plot(theta / (2 * np.pi), g_num, "o", ms=4, color="tab:purple",
            label="numeric ISF $\\Gamma(\\theta)=\\Delta\\phi/(\\Delta q/q_{max})$")
    ax.plot(theta / (2 * np.pi), g_ana, "k--", label=r"$-\sin\theta$")
    ax.axhline(0, color="gray", lw=0.6)
    err = np.max(np.abs(g_num - g_ana))
    ax.set_xlabel(r"injection phase $\theta/2\pi$")
    ax.set_ylabel(r"$\Gamma(\theta)$ [dimensionless]")
    ax.set_title(f"Recovered ISF vs theory (max abs error = {err:.3f})")
    ax.legend()
    savefig(fig, "isf_impulse_sweep_sinusoidal.png")


def fig_lti_vs_ltv():
    f0 = 1.0
    fs = 2000.0
    t = np.arange(int(3.0 * fs)) / fs

    fig, axes = plt.subplots(2, 1, figsize=(8.4, 6.2), sharex=True)

    # LTI: impulse response depends only on (t - tau); same shape, shifted.
    ax = axes[0]
    for tau, c in zip([0.3, 0.9, 1.5], ["tab:blue", "tab:orange", "tab:green"]):
        h = np.where(t >= tau, np.exp(-(t - tau) / 0.4) * (t >= tau), 0.0)
        ax.plot(t, h, color=c, label=fr"$\tau={tau}$")
    ax.set_title(r"LTI: $h(t,\tau)=h(t-\tau)$ — 形狀相同，只是平移")
    ax.set_ylabel("response")
    ax.legend(fontsize=8)

    # LTV (oscillator phase): step of height Gamma(w0 tau)/qmax * u(t - tau).
    ax = axes[1]
    for tau, c in zip([0.0, 0.25, 0.5], ["tab:blue", "tab:orange", "tab:green"]):
        gamma = -np.sin(2 * np.pi * f0 * tau)  # ISF at injection phase
        h = gamma * (t >= tau)
        ax.plot(t, h, color=c,
                label=fr"$\tau={tau}$, $\Gamma=-\sin(2\pi\tau)={gamma:+.2f}$")
    ax.axhline(0, color="gray", lw=0.6)
    ax.set_title(r"LTV phase response: $h_\phi(t,\tau)=\frac{\Gamma(\omega_0\tau)}{q_{max}}u(t-\tau)$"
                 r" — 階高隨注入相位改變")
    ax.set_xlabel("time $t$ (periods)")
    ax.set_ylabel(r"$\phi$ response")
    ax.legend(fontsize=8)
    savefig(fig, "lti_vs_ltv_impulse_response.png")


def main():
    print("[lab_04] impulse injection sweep / LTI vs LTV ...")
    fig_isf_sweep()
    fig_lti_vs_ltv()


if __name__ == "__main__":
    main()
