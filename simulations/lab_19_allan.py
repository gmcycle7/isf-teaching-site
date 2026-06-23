"""
lab_19_allan.py

Goal
----
The time-domain companion of phase noise: the Allan deviation sigma_y(tau).
Oscillator/clock engineers quote sigma_y(tau) because plain variance of frequency
does not converge for flicker/random-walk noise. Each power-law noise type maps
to a characteristic sigma_y(tau) slope:

    white FM        S_y ~ f^0   ->  sigma_y ~ tau^{-1/2}
    flicker FM      S_y ~ f^-1  ->  sigma_y ~ tau^{0}   (flat floor)
    random-walk FM  S_y ~ f^-2  ->  sigma_y ~ tau^{+1/2}

We generate each fractional-frequency process, integrate to time error x(t), and
compute the OVERLAPPING Allan deviation, then check the slopes.

Figure
------
  static/figures/allan_deviation.png
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt
from plot_utils import savefig

RNG = np.random.default_rng(19)


def power_law_y(n, fs, alpha, rng):
    """Fractional-frequency y(t) with one-sided PSD S_y(f) ~ f^alpha."""
    w = rng.standard_normal(n)
    F = np.fft.rfft(w)
    f = np.fft.rfftfreq(n, d=1.0 / fs)
    shape = np.ones_like(f)
    nz = f > 0
    shape[nz] = f[nz] ** (alpha / 2.0)
    shape[0] = shape[nz][0] if np.any(nz) else 1.0
    y = np.fft.irfft(F * shape, n=n)
    return y / np.std(y)


def overlapping_adev(x, tau0, ms):
    """Overlapping Allan deviation from time-error samples x at spacing tau0."""
    x = np.asarray(x)
    N = len(x)
    out = []
    for m in ms:
        if N - 2 * m < 1:
            out.append(np.nan); continue
        d = x[2 * m:] - 2 * x[m:-m] + x[:-2 * m]
        avar = np.sum(d ** 2) / (2 * (N - 2 * m) * (m * tau0) ** 2)
        out.append(np.sqrt(avar))
    return np.array(out)


def main():
    print("[lab_19] Allan deviation vs noise type ...")
    fs = 1.0
    n = 2 ** 18
    tau0 = 1.0 / fs
    ms = np.unique(np.round(np.logspace(0, np.log10(n // 8), 30)).astype(int))
    taus = ms * tau0

    cases = [
        (0.0, "white FM ($S_y\\sim f^0$)", "tab:blue", -0.5),
        (-1.0, "flicker FM ($S_y\\sim f^{-1}$)", "tab:green", 0.0),
        (-2.0, "random-walk FM ($S_y\\sim f^{-2}$)", "tab:red", 0.5),
    ]

    fig, ax = plt.subplots(figsize=(8.4, 5.4))
    for alpha, label, c, slope in cases:
        y = power_law_y(n, fs, alpha, RNG)
        x = np.cumsum(y) * tau0           # time error = integral of fractional freq
        adev = overlapping_adev(x, tau0, ms)
        ax.loglog(taus, adev / adev[0], "o-", ms=3, color=c, label=label)
        # reference slope line through first point
        ref = (adev[0] / adev[0]) * (taus / taus[0]) ** slope
        ax.loglog(taus, ref, color=c, ls="--", lw=0.9, alpha=0.7)

    ax.set_xlabel(r"averaging time $\tau$ (s)")
    ax.set_ylabel(r"$\sigma_y(\tau)$ (normalized)")
    ax.set_title("Allan deviation：每種 FM 雜訊有特徵斜率（虛線 = 理論斜率）")
    ax.legend(fontsize=9)
    ax.grid(True, which="both", alpha=0.3)
    ax.text(0.02, 0.04,
            "slopes: white FM $-1/2$, flicker FM $0$, random-walk FM $+1/2$",
            transform=ax.transAxes, fontsize=8)
    savefig(fig, "allan_deviation.png")


if __name__ == "__main__":
    main()
