"""
lab_05_fourier_isf.py

Goal
----
Compute the Fourier coefficients of an ISF and show:
  * reconstruction from a few harmonics,
  * the coefficient magnitude spectrum c_n,
  * how a symmetric ISF (c0 = 0) vs an asymmetric ISF (c0 != 0) differ — the c0
    term is the gateway for 1/f-noise upconversion.

Figures produced
----------------
  static/figures/isf_fourier_reconstruction.png
  static/figures/isf_fourier_coefficients.png
  static/figures/symmetric_vs_asymmetric_isf_c0.png

Corresponds to: Hajimiri-Lee (1998) Eq. (12),(24).
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt

from isf_utils import (gamma_asymmetric, compute_fourier_coefficients,
                       reconstruct_from_fourier, gamma_rms)
from plot_utils import savefig


def make_isf(theta):
    """A richer asymmetric ISF so several harmonics are non-trivial."""
    return (-np.sin(theta) + 0.35 * np.sin(2 * theta)
            + 0.18 * np.cos(3 * theta) + 0.25)  # the +0.25 sets a non-zero c0


def fig_reconstruction():
    theta = np.linspace(0, 2 * np.pi, 2000, endpoint=True)
    g = make_isf(theta)
    a0, a, b, c, ph = compute_fourier_coefficients(theta, g, n_harmonics=8)

    fig, ax = plt.subplots(figsize=(8.2, 4.4))
    ax.plot(theta / (2 * np.pi), g, color="black", lw=2, label="original ISF")
    for N in [1, 2, 4]:
        rec = reconstruct_from_fourier(theta, a0, a[:N + 1], b[:N + 1])
        ax.plot(theta / (2 * np.pi), rec, lw=1.2, label=f"reconstruct N={N}")
    ax.axhline(0, color="gray", lw=0.6)
    ax.set_xlabel(r"phase $\theta/2\pi$")
    ax.set_ylabel(r"$\Gamma(\theta)$")
    ax.set_title("ISF Fourier reconstruction (越多 harmonic 越接近)")
    ax.legend(fontsize=8)
    savefig(fig, "isf_fourier_reconstruction.png")


def fig_coefficients():
    theta = np.linspace(0, 2 * np.pi, 2000, endpoint=True)
    g = make_isf(theta)
    a0, a, b, c, ph = compute_fourier_coefficients(theta, g, n_harmonics=8)

    # check Parseval: (c0/2)^2 + sum_{n>=1} c_n^2 ?= 2 Gamma_rms^2
    # The DC harmonic enters Parseval as (c0/2)^2, not c0^2.
    parseval_lhs = c[0] ** 2 / 2 + np.sum(c[1:] ** 2)
    grms = gamma_rms(theta, g)

    fig, ax = plt.subplots(figsize=(7.6, 4.4))
    n = np.arange(len(c))
    ax.bar(n, c, color="tab:blue", width=0.6)
    ax.set_xlabel("harmonic number $n$")
    ax.set_ylabel(r"$|c_n|$")
    ax.set_title(fr"ISF coefficients   ($c_0$={c[0]:.3f}, "
                 fr"$\Gamma_{{rms}}$={grms:.3f}, "
                 fr"$(c_0/2)^2+\sum_{{n\geq1}} c_n^2$={parseval_lhs:.3f} "
                 fr"$=2\Gamma_{{rms}}^2$={2*grms**2:.3f})"
                 "\n"
                 r"DC harmonic 以 $(c_0/2)^2$ 進入 Parseval")
    for i in range(len(c)):
        ax.text(i, c[i] + 0.01, f"{c[i]:.2f}", ha="center", fontsize=7)
    savefig(fig, "isf_fourier_coefficients.png")


def fig_symmetric_vs_asymmetric():
    theta = np.linspace(0, 2 * np.pi, 2000, endpoint=True)
    g_sym = np.cos(theta)               # c0 = 0 (symmetric)
    g_asym = gamma_asymmetric(theta, alpha=0.4)  # c0 = 2*alpha = 0.8

    a0s, *_ , = compute_fourier_coefficients(theta, g_sym, 4)
    a0a, *_ = compute_fourier_coefficients(theta, g_asym, 4)

    fig, ax = plt.subplots(figsize=(8.2, 4.4))
    ax.plot(theta / (2 * np.pi), g_sym, color="tab:green",
            label=fr"symmetric $\cos\theta$ ($c_0$={abs(a0s):.2f})")
    ax.plot(theta / (2 * np.pi), g_asym, color="tab:red",
            label=fr"asymmetric $\cos\theta+0.4$ ($c_0$={abs(a0a):.2f})")
    ax.axhline(0, color="gray", lw=0.6)
    ax.fill_between(theta / (2 * np.pi), g_asym, 0.4, alpha=0.12, color="tab:red")
    ax.axhline(0.4, color="tab:red", ls=":", lw=1,
               label=r"DC of asymmetric ISF = $c_0/2$")
    ax.set_xlabel(r"phase $\theta/2\pi$")
    ax.set_ylabel(r"$\Gamma(\theta)$")
    ax.set_title(r"$c_0\neq 0$ 才會把 1/f noise upconvert 到 close-in phase noise")
    ax.legend(fontsize=8)
    savefig(fig, "symmetric_vs_asymmetric_isf_c0.png")


def main():
    print("[lab_05] ISF Fourier coefficients ...")
    fig_reconstruction()
    fig_coefficients()
    fig_symmetric_vs_asymmetric()


if __name__ == "__main__":
    main()
