"""
lab_13_pll_cdr_transfer.py

Goal
----
Show how a PLL/CDR loop FILTERS oscillator phase noise: the VCO's own phase
noise is high-pass shaped (suppressed close in, dominant far out) while the
reference is low-pass shaped. This is why a noisy ring-VCO can still give a
usable clock when locked to a clean reference.

Model
-----
  Type-II 2nd-order PLL. S_out = S_ref*|H_lp|^2 + S_vco*|H_hp|^2.
  VCO PN ~ 1/f^2 (ring), reference PN ~ low flat-ish + small 1/f^2.

Figure
------
  static/figures/pll_cdr_jitter_transfer.png
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt
from pll_utils import H_lowpass_mag2, H_highpass_mag2, shape_output_phase_noise
from plot_utils import savefig


def main():
    print("[lab_13] PLL/CDR jitter transfer & noise shaping ...")
    f = np.logspace(3, 9, 2000)  # 1 kHz .. 1 GHz offset
    fn = 1e6  # loop natural frequency ~ 1 MHz
    zeta = 0.707

    # representative phase-noise PSDs (rad^2/Hz), anchored shapes
    S_vco = 1e-6 * (1e6 / f) ** 2          # ring VCO: strong 1/f^2 close-in
    S_ref = 1e-12 + 1e-14 * (1e6 / f) ** 2  # clean reference: low flat + slight 1/f^2

    S_out, S_ref_sh, S_vco_sh = shape_output_phase_noise(f, S_ref, S_vco, fn, zeta)

    fig, axes = plt.subplots(1, 2, figsize=(13.0, 4.8))

    # (a) transfer functions
    ax = axes[0]
    ax.loglog(f, H_lowpass_mag2(f, fn, zeta), color="tab:blue",
              label=r"$|H_{lp}|^2$（reference→輸出，低通）")
    ax.loglog(f, H_highpass_mag2(f, fn, zeta), color="tab:red",
              label=r"$|H_{hp}|^2$（VCO→輸出，高通）")
    ax.axvline(fn, color="gray", ls="--", lw=1, label=fr"loop BW $f_n$={fn/1e6:.0f} MHz")
    ax.set_xlabel("offset frequency [Hz]")
    ax.set_ylabel("power transfer")
    ax.set_title("(a) PLL 把 VCO noise 高通、reference 低通")
    ax.set_ylim(1e-6, 5)
    ax.legend(fontsize=8)

    # (b) shaped output phase noise
    ax = axes[1]
    ax.loglog(f, S_vco, color="tab:red", ls=":", lw=1, label="VCO PN（未鎖定）")
    ax.loglog(f, S_ref, color="tab:blue", ls=":", lw=1, label="reference PN")
    ax.loglog(f, S_out, color="black", lw=2, label="鎖定後輸出 PN")
    ax.axvline(fn, color="gray", ls="--", lw=1)
    ax.set_xlabel("offset frequency [Hz]")
    ax.set_ylabel(r"$S_\phi$ [rad$^2$/Hz]")
    ax.set_title(r"(b) 結果：close-in 跟 reference、far-out 跟 VCO（交越在 $f_n$）")
    ax.legend(fontsize=8)
    savefig(fig, "pll_cdr_jitter_transfer.png")


if __name__ == "__main__":
    main()
