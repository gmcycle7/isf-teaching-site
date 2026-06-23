"""
lab_11_monte_carlo_jitter.py

Goal
----
Show that the random (RJ) jitter accumulated by a free-running oscillator is
GAUSSIAN, and that its standard deviation matches the random-walk law
sigma = sigma_edge * sqrt(N). This closes the loop between the statistical
(time-domain) view and the spectral view of jitter.

Model
-----
  Many independent realizations of an oscillator whose each period picks up
  N(0, sigma_edge) timing noise. Accumulated error after N periods is a random
  walk; histogram it across trials.

Figure
------
  static/figures/monte_carlo_jitter_histogram.png
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt
from plot_utils import savefig

RNG = np.random.default_rng(11)


def main():
    print("[lab_11] Monte-Carlo accumulated jitter histogram ...")
    f0 = 5e9
    sigma_edge = 50e-15  # 50 fs per period
    n_trials = 200000
    lags = [25, 100, 400]  # number of periods accumulated

    fig, ax = plt.subplots(figsize=(8.2, 5.0))
    colors = ["tab:blue", "tab:orange", "tab:red"]
    for lag, c in zip(lags, colors):
        incr = sigma_edge * RNG.standard_normal((n_trials, lag))
        acc = incr.sum(axis=1)  # accumulated timing error after `lag` periods
        sigma_meas = np.std(acc)
        sigma_theory = sigma_edge * np.sqrt(lag)
        # histogram (in fs)
        ax.hist(acc / 1e-15, bins=120, density=True, alpha=0.35, color=c,
                label=fr"$\Delta N$={lag}: 量得 $\sigma$={sigma_meas/1e-15:.0f} fs "
                      fr"(理論 {sigma_theory/1e-15:.0f} fs)")
        # gaussian overlay
        xx = np.linspace(acc.min(), acc.max(), 300)
        g = np.exp(-xx ** 2 / (2 * sigma_theory ** 2)) / (sigma_theory * np.sqrt(2 * np.pi))
        ax.plot(xx / 1e-15, g * 1e-15, color=c, lw=1.6)

    ax.set_xlabel("accumulated timing error [fs]")
    ax.set_ylabel("probability density [1/fs]")
    ax.set_title(r"RJ 是高斯，且 $\sigma_{\Delta t}=\sigma_{edge}\sqrt{\Delta N}$ "
                 r"($f_0$=5 GHz, $\sigma_{edge}$=50 fs)")
    ax.legend(fontsize=8)
    savefig(fig, "monte_carlo_jitter_histogram.png")


if __name__ == "__main__":
    main()
