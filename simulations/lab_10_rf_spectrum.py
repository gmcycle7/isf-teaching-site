"""
lab_10_rf_spectrum.py

Goal
----
Connect the phase-noise PSD S_phi(f) to the ACTUAL RF spectrum you see on a
spectrum analyzer: an ideal carrier is a single line; phase noise smears it into
a skirt of sidebands. This is the time-domain picture behind [P1] Fig. 8 and the
meaning of dBc/Hz.

Model
-----
  v(t) = cos(2 pi f0 t + phi(t)),  phi(t) = 1/f^2 phase noise (white -> integrate)
  RF spectrum = |FFT{v}|^2, plotted in dB relative to the carrier peak.

Figure
------
  static/figures/rf_spectrum_phase_noise_sidebands.png
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt
from plot_utils import savefig

RNG = np.random.default_rng(10)


def main():
    print("[lab_10] RF spectrum: phase noise -> carrier skirt ...")
    fs = 8192.0
    n = 2 ** 18
    t = np.arange(n) / fs
    f0 = 512.0  # carrier (normalized units), 16 samples/cycle

    # 1/f^2 phase noise: integrate white noise, scale to a visible (small) rms
    white = RNG.standard_normal(n)
    phi = np.cumsum(white) / fs
    phi -= phi.mean()
    phi *= 0.03 / np.std(phi)  # ~0.03 rad rms -> small-angle regime

    v_clean = np.cos(2 * np.pi * f0 * t)
    v_noisy = np.cos(2 * np.pi * f0 * t + phi)

    win = np.hanning(n)
    def spec(x):
        X = np.fft.rfft(x * win)
        P = np.abs(X) ** 2
        return P / P.max()
    f = np.fft.rfftfreq(n, 1 / fs)
    Pc = spec(v_clean)
    Pn = spec(v_noisy)

    off = f - f0  # offset from carrier
    m = (off > 1.0) & (off < 2000)

    # The skirt of the noisy spectrum decays into the floor near offset ~ 35;
    # set the x-axis to roughly that data extent so the sidebands fill the panel
    # (the previous default ran out to ~3000 and left most of the axis empty).
    x_lo, x_hi = 1.0, 50.0

    fig, ax = plt.subplots(figsize=(8.2, 5.0))
    ax.semilogx(off[m], 10 * np.log10(Pn[m]), color="tab:red", lw=1.0,
                label="有 phase noise（裙帶 sidebands）")
    # Pc is essentially a single line AT the carrier (offset 0), which is off the
    # log x-axis, so there is no curve to draw. Mark it as a single line near
    # Delta f -> 0 (the left edge) with an annotation instead of a phantom legend
    # entry that has no visible curve.
    ax.axvline(x_lo, color="tab:blue", lw=1.4, alpha=0.85)
    ax.annotate("理想載波：$\\Delta f\\to 0$ 的單一譜線\n(ideal carrier = single line)",
                xy=(x_lo, 2.0), xytext=(2.0, -18),
                color="tab:blue", fontsize=9,
                arrowprops=dict(arrowstyle="->", color="tab:blue", lw=1.2))
    ax.set_xlabel("offset from carrier $\\Delta f$ (normalized)")
    ax.set_ylabel("relative power [dB]（dBc）")
    ax.set_title("Phase noise 把載波塗成裙帶：時域 PM → RF 頻譜（[P1] Fig.8 的圖像）")
    ax.set_xlim(x_lo, x_hi)
    ax.set_ylim(-90, 5)
    ax.legend(loc="upper right")
    ax.grid(True, which="both", alpha=0.3)
    savefig(fig, "rf_spectrum_phase_noise_sidebands.png")


if __name__ == "__main__":
    main()
