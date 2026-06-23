"""
lab_16_leeson_vs_isf.py

Goal
----
Overlay the empirical Leeson model and the ISF-based model on one phase-noise
plot, showing they share the same three regions (1/f^3, 1/f^2, flat floor) and
that the ISF model gives physical meaning to Leeson's fitting parameters.

Leeson (1966), reference model (NOT in the 5 source PDFs; standard literature):
  L(dw) = 10 log[ (2 F kT / Ps) (1 + (w0/(2 Q dw))^2)(1 + w_c/|dw|) ]

ISF model (built from [P1] Eq.(21),(23) + a white noise floor):
  L(dw) = 10 log[ Grms^2/qmax^2 * (in2/df)/(4 dw^2)         # 1/f^2
                + c0^2/qmax^2 * (in2/df)/(8 dw^2) * w1f/dw   # 1/f^3
                + floor ]

Figure
------
  static/figures/leeson_vs_isf_overlay.png
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt
from plot_utils import savefig

k = 1.380649e-23
T = 300.0


def main():
    print("[lab_16] Leeson vs ISF overlay ...")
    f = np.logspace(3, 8, 2000)         # 1 kHz .. 100 MHz offset
    dw = 2 * np.pi * f
    f0 = 5e9
    w0 = 2 * np.pi * f0

    # --- Leeson ---
    F = 5.0; Ps = 1e-3; Q = 10.0; fc = 1e5     # flicker corner 100 kHz
    leeson = (2 * F * k * T / Ps) * (1 + (w0 / (2 * Q * dw)) ** 2) * (1 + 2 * np.pi * fc / dw)
    L_leeson = 10 * np.log10(leeson)

    # --- ISF model (tuned to land near Leeson for teaching overlay) ---
    qmax = 1e-12
    in2_df = 1e-20
    Grms = 0.5
    c0 = 0.2
    w1f = 2 * np.pi * fc
    floor = 10 ** (-160 / 10)
    isf = (Grms ** 2 / qmax ** 2) * in2_df / (4 * dw ** 2) \
        + (c0 ** 2 / qmax ** 2) * in2_df / (8 * dw ** 2) * (w1f / dw) \
        + floor
    L_isf = 10 * np.log10(isf)

    fig, ax = plt.subplots(figsize=(8.4, 5.2))
    ax.semilogx(f, L_leeson, color="tab:blue", lw=1.8, label="Leeson（經驗模型）")
    ax.semilogx(f, L_isf, color="tab:red", lw=1.8, ls="--", label="ISF 模型（[P1] Eq.21,23＋floor）")
    # region guides
    ax.axvline(fc, color="gray", ls=":", lw=1)
    ax.text(fc * 1.1, -60, r"$1/f^3$ corner", fontsize=8, color="gray")
    ax.set_xlabel("offset frequency $\\Delta f$ [Hz]")
    ax.set_ylabel("$\\mathcal{L}(\\Delta f)$ [dBc/Hz]")
    ax.set_title("Leeson vs ISF：同樣的 $1/f^3$ / $1/f^2$ / floor 三段")
    ax.legend()
    ax.grid(True, which="both", alpha=0.3)
    savefig(fig, "leeson_vs_isf_overlay.png")


if __name__ == "__main__":
    main()
