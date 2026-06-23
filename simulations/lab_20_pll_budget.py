"""
lab_20_pll_budget.py

Goal
----
A full PLL output phase-noise BUDGET: every source (reference, PFD/charge-pump,
divider, loop filter, VCO) is shaped by its own transfer function and summed.
Then sweep the loop bandwidth to find the value that MINIMIZES integrated jitter
(the classic trade: low BW lets VCO noise through, high BW lets reference/CP
noise through).

Model (type-II 2nd-order PLL, all PSDs referred to the output, rad^2/Hz)
  S_out = (S_ref*N^2 + S_cp) * |H_lp|^2  +  S_vco * |H_hp|^2
  (reference is multiplied up by the divide ratio N before the loop low-pass)

Figures
-------
  static/figures/pll_noise_budget.png
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt
from pll_utils import H_lowpass_mag2, H_highpass_mag2
from plot_utils import savefig


def output_psd(f, fn, N, zeta=0.707):
    lp = H_lowpass_mag2(f, fn, zeta)
    hp = H_highpass_mag2(f, fn, zeta)
    # source PSDs (representative levels, rad^2/Hz). Reference is referred to its
    # own output then multiplied by N^2 by the loop; CP/divider ~flat in-band;
    # VCO ~ -100 dBc/Hz @ 1 MHz (S_vco = 2*1e-10 there).
    S_ref = 1e-16 + 1e-18 * (1e6 / f)        # clean xtal: low flat + slight 1/f
    S_cp = 5e-13 * np.ones_like(f)           # charge-pump/PFD/divider: ~flat in-band
    S_vco = 2e-10 * (1e6 / f) ** 2           # ring VCO: -100 dBc/Hz @ 1 MHz, 1/f^2
    in_band = (S_ref * N ** 2 + S_cp) * lp
    out_band = S_vco * hp
    return in_band + out_band, in_band, out_band


def integ_jitter(f, S_out, f0):
    sigphi = np.sqrt(np.trapezoid(S_out, f)) if hasattr(np, "trapezoid") else np.sqrt(np.trapz(S_out, f))
    return sigphi / (2 * np.pi * f0)


def main():
    print("[lab_20] PLL phase-noise budget + optimal loop BW ...")
    f = np.logspace(3, 9, 3000)
    f0 = 5e9
    N = 100

    # (b) first: sweep loop BW and find the optimum, so panel (a) can be drawn
    # AT that optimum (keeps the two panels self-consistent).
    fns = np.logspace(4.5, 7.5, 60)
    jit = []
    for fnx in fns:
        So, _, _ = output_psd(f, fnx, N)
        jit.append(integ_jitter(f, So, f0))
    jit = np.array(jit)
    kopt = np.argmin(jit)
    fn_opt = fns[kopt]

    # panel (a) is now rendered at the optimal loop BW found above
    fn = fn_opt
    S_out, inb, outb = output_psd(f, fn, N)

    fig, axes = plt.subplots(1, 2, figsize=(13.5, 4.8))

    # (a) budget at the optimal loop BW (matches the red dot in (b))
    ax = axes[0]
    ax.loglog(f, inb, color="tab:blue", ls=":", lw=1.1, label="ref×N² + CP/PFD（低通）")
    ax.loglog(f, outb, color="tab:red", ls=":", lw=1.1, label="VCO（高通）")
    ax.loglog(f, S_out, color="black", lw=2, label="輸出總和 $S_\\phi$")
    ax.axvline(fn, color="gray", ls="--", lw=1,
               label=f"最佳 loop BW $f_n$≈{fn/1e6:.2f} MHz")
    ax.set_xlabel("offset frequency [Hz]")
    ax.set_ylabel(r"$S_\phi$ [rad$^2$/Hz]")
    ax.set_title("(a) PLL 輸出雜訊預算（畫在最佳 loop BW）：in-band 跟 ref/CP、out-of-band 跟 VCO")
    ax.legend(fontsize=8)

    # (b) integrated jitter vs loop BW -> optimum
    ax = axes[1]
    ax.loglog(fns, jit / 1e-15, color="tab:purple", lw=2)
    ax.plot(fns[kopt], jit[kopt] / 1e-15, "o", color="tab:red", ms=8,
            label="最佳 $f_n$≈%.2f MHz\n$\\sigma_t$≈%d fs" % (fns[kopt] / 1e6, jit[kopt] / 1e-15))
    ax.set_xlabel("loop bandwidth $f_n$ [Hz]")
    ax.set_ylabel(r"integrated rms jitter $\sigma_t$ [fs]")
    ax.set_title("(b) 存在最佳 loop BW：太窄→VCO 漏出、太寬→ref/CP 漏出")
    ax.legend(fontsize=9)
    ax.grid(True, which="both", alpha=0.3)
    print(f"    optimal fn ~ {fns[kopt]/1e6:.2f} MHz, sigma_t ~ {jit[kopt]*1e15:.0f} fs")
    savefig(fig, "pll_noise_budget.png")


if __name__ == "__main__":
    main()
