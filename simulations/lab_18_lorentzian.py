"""
lab_18_lorentzian.py

Goal
----
Show the result the 1/f^2 formula hides: a real oscillator's carrier is NOT a
delta line and NOT actually 1/f^2 all the way in. Phase undergoes a random walk
(Wiener process), which makes the CARRIER AUTOCORRELATION decay exponentially,
so the spectrum is a LORENTZIAN with a finite 3-dB linewidth. The 1/f^2 skirt is
only the far-from-carrier asymptote; near the carrier the Lorentzian flattens
(finite peak) and total power is conserved (= carrier power).

Model
-----
  phi(t): Wiener process with Var[phi(t)] = 2 D t   (D = phase diffusion [rad^2/s])
  carrier x(t) = cos(2 pi f0 t + phi(t))
  R_x(tau) = 1/2 cos(2 pi f0 tau) e^{-D|tau|}  ->  S_x = Lorentzian
  one-sided about carrier:  S(df) ∝ D / (D^2 + (2 pi df)^2)
  HWHM(df) = D/(2 pi) Hz ;  FWHM (3-dB linewidth) = D/pi Hz.

Figure
------
  static/figures/lorentzian_carrier_lineshape.png
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch
from plot_utils import savefig

RNG = np.random.default_rng(18)


def main():
    print("[lab_18] Lorentzian carrier lineshape ...")
    fs = 4096.0
    n = 2 ** 20
    t = np.arange(n) / fs
    f0 = 400.0                 # carrier (normalized units)
    D = 2.0                    # phase diffusion [rad^2/s] -> FWHM = D/pi ~ 0.64 Hz

    # Wiener phase: increments N(0, 2 D dt)
    dphi = RNG.standard_normal(n) * np.sqrt(2 * D / fs)
    phi = np.cumsum(dphi)
    x = np.cos(2 * np.pi * f0 * t + phi)

    f, P = welch(x, fs=fs, nperseg=2 ** 16, scaling="density")
    off = f - f0
    m = (np.abs(off) < 50) & (off != 0)

    # theory Lorentzian about carrier, normalized to the simulated peak region
    lor = D / (D ** 2 + (2 * np.pi * off) ** 2)
    # scale theory to sim near carrier
    near = np.abs(off) < 2
    scale = np.median(P[m & near]) / np.median(lor[m & near])
    lor_s = lor * scale

    fwhm = D / np.pi  # Hz

    fig, axes = plt.subplots(1, 2, figsize=(13.5, 4.8))

    # (a) lineshape: simulated vs Lorentzian vs 1/f^2 asymptote
    ax = axes[0]
    ax.loglog(off[off > 0], P[off > 0], color="tab:blue", lw=0.8, alpha=0.6,
              label="simulated $S(\\Delta f)$")
    pos = off > 0
    ax.loglog(off[pos], lor_s[pos], "k--", lw=1.5, label="Lorentzian 理論")
    # 1/f^2 asymptote: far-out Lorentzian ~ scale*D/(2 pi df)^2
    asym = scale * D / (2 * np.pi * off) ** 2
    ax.loglog(off[pos], asym[pos], color="tab:red", ls=":", lw=1.3,
              label="$1/\\Delta f^2$ 漸近（遠離載波）")
    ax.axvline(fwhm / 2, color="tab:green", lw=1, ls="-.",
               label=f"HWHM = D/2π = {fwhm/2:.2f} Hz")
    ax.set_xlim(0.05, 50)
    ax.set_xlabel("offset from carrier $\\Delta f$ (normalized)")
    ax.set_ylabel("$S(\\Delta f)$")
    ax.set_title("載波是 Lorentzian：近載波轉平（有限峰），$1/f^2$ 只是遠端漸近")
    ax.legend(fontsize=8)
    ax.grid(True, which="both", alpha=0.3)

    # (b) phase variance grows linearly (random walk) -> exponential R_x
    ax = axes[1]
    # estimate Var[phi(t)] across many short segments
    seglen = 2000
    nseg = 300
    taus = np.arange(1, seglen) / fs
    var_acc = np.zeros(seglen - 1)
    cnt = 0
    for _ in range(nseg):
        s = RNG.integers(0, n - seglen)
        seg = phi[s:s + seglen] - phi[s]
        var_acc += seg[1:] ** 2
        cnt += 1
    var_phi = var_acc / cnt
    ax.plot(taus, var_phi, color="tab:blue", lw=1.2, label="量測 Var[Δφ(τ)]")
    ax.plot(taus, 2 * D * taus, "k--", lw=1.5, label="理論 $2D\\tau$（線性）")
    ax.set_xlabel("time lag $\\tau$ (s, normalized)")
    ax.set_ylabel("Var[$\\Delta\\phi(\\tau)$] [rad$^2$]")
    ax.set_title("相位是 random walk：方差線性成長 → 載波自相關指數衰減")
    ax.legend(fontsize=9)
    print(f"    D={D} rad^2/s -> FWHM linewidth = D/pi = {fwhm:.3f} Hz")
    savefig(fig, "lorentzian_carrier_lineshape.png")


if __name__ == "__main__":
    main()
