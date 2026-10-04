"""
fig_pll_rnoise.py — loop-filter resistor noise overlaid on the lab_20 PLL budget.

Companion script for docs/06_design_insights/pll_noise_budget.md
(section "數值驗證：把 loop-filter 電阻雜訊疊上預算").

lab_20 (simulations/lab_20_pll_budget.py) is the site's canonical "ideal loop
filter" budget: reference x N^2 + CP/PFD (low-pass) + ring VCO (high-pass), with
an integrated-jitter optimum of ~259 fs at fn ~ 6.9 MHz.  It has NO loop-filter
resistor term.  This script leaves lab_20 untouched (it imports lab_20's own
output_psd / integ_jitter so the baseline is identical) and ADDS

    S_phi,R(f) = 4kTR * K_vco^2 / (2 pi f)^2 * |H_hp(f)|^2      [rad^2/Hz]

(K_vco in rad/s/V, one-sided 4kTR in V^2/Hz, one-sided S_phi) with R taken from
pll_utils.design_type2 for three charge-pump currents:

    I_cp = 100 uA  (the lab_13 worked design: fn = 1 MHz, zeta = 0.707, N = 100,
                    K_vco = 50 MHz/V  ->  C = 1.27 pF, R = 178 kohm)
    I_cp = 1 mA, 10 mA  (x10, x100: at fixed w_n, zeta -> C ~ I_cp, R ~ 1/I_cp)

Closed forms checked numerically here (ideal type-II 2nd-order loop):
    R            = 4 pi zeta N w_n / (I_cp K_vco)
    S_phi,R(fn)  = 4 pi kT N K_vco / (zeta w_n I_cp)                (peak)
    sigma_phi,R^2 = int_0^inf S_phi,R df = (kT/C)(K_vco/w_n)^2
                  = 2 pi N kT K_vco / I_cp       (independent of fn and zeta!)

Assumptions / honesty: T = 300 K; ideal series R-C filter (no 3rd pole C3, no
CP leakage/mismatch); lab_20's S_cp floor is kept FIXED while I_cp is scaled
(lab_20 does not tie S_cp to I_cp), so only the resistor term moves; all levels
are illustrative, not a silicon design.

Figure:  static/figures/pll_budget_rnoise.png
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "common"))
sys.path.insert(0, _HERE)

import numpy as np
import matplotlib.pyplot as plt
from pll_utils import H_highpass_mag2, design_type2
from plot_utils import savefig
from lab_20_pll_budget import output_psd, integ_jitter   # the untouched baseline

K_B = 1.380649e-23      # J/K
T_K = 300.0             # K
F0 = 5e9                # Hz
N_DIV = 100
ZETA = 0.707
KVCO_HZ = 50e6          # Hz/V
ICPS = (100e-6, 1e-3, 10e-3)     # A
COLORS = ("tab:orange", "tab:green", "tab:purple")


def _trapz(y, x):
    return np.trapezoid(y, x) if hasattr(np, "trapezoid") else np.trapz(y, x)


def resistor_psd(f, fn, icp, zeta=ZETA):
    """S_phi,R(f) [rad^2/Hz] and the (R, C) that realize (fn, zeta) at this I_cp."""
    R, C = design_type2(fn, zeta, N_DIV, KVCO_HZ, icp)
    kv = 2 * np.pi * KVCO_HZ                     # rad/s/V
    Sv = 4 * K_B * T_K * R                       # V^2/Hz, one-sided
    return Sv * kv ** 2 / (2 * np.pi * f) ** 2 * H_highpass_mag2(f, fn, zeta), R, C


def label_icp(icp):
    return f"{icp*1e3:g} mA" if icp >= 1e-3 else f"{icp*1e6:g} µA"


def label_r(R):
    return f"{R/1e6:.3g} MΩ" if R >= 1e6 else f"{R/1e3:.3g} kΩ"


def main():
    print("[fig_pll_rnoise] loop-filter resistor noise on top of the lab_20 budget ...")
    f = np.logspace(3, 9, 3000)                  # same grid as lab_20
    kv = 2 * np.pi * KVCO_HZ

    # ---- lab_20 baseline (identical code path): sweep fn, find optimum --------
    fns = np.logspace(4.5, 7.5, 60)
    jit0 = np.array([integ_jitter(f, output_psd(f, fnx, N_DIV)[0], F0) for fnx in fns])
    kopt = int(np.argmin(jit0))
    fn_opt = fns[kopt]
    print(f"    baseline (lab_20, no R): optimal fn = {fn_opt/1e6:.2f} MHz, "
          f"sigma_t = {jit0[kopt]*1e15:.1f} fs")

    # ---- closed forms vs numerics for the lab_13 design -----------------------
    fn13 = 1e6
    wn = 2 * np.pi * fn13
    S_R, R, C = resistor_psd(f, fn13, ICPS[0])
    i1 = int(np.argmin(abs(f - fn13)))
    peak_cf = 4 * np.pi * K_B * T_K * N_DIV * kv / (ZETA * wn * ICPS[0])
    var_cf = 2 * np.pi * N_DIV * K_B * T_K * kv / ICPS[0]
    var_ktc = K_B * T_K / C * (kv / wn) ** 2
    var_num = _trapz(S_R, f)
    print(f"    lab_13 design: R = {R/1e3:.1f} kohm, C = {C*1e12:.3f} pF")
    print(f"    peak S_R(fn): numeric {S_R[i1]:.3e}, closed form {peak_cf:.3e} rad^2/Hz "
          f"(ratio {S_R[i1]/peak_cf:.4f})")
    print(f"    sigma_phi_R^2: numeric(1k-1G) {var_num:.4e}, 2piN kT Kv/Icp {var_cf:.4e}, "
          f"kT/C form {var_ktc:.4e} rad^2 (ratio num/closed {var_num/var_cf:.4f})")
    print(f"    sigma_t_R closed form = {np.sqrt(var_cf)/(2*np.pi*F0)*1e15:.2f} fs")

    # ---- table: with / without R at fn = 1 MHz and at the optimum -------------
    rows = {}
    for fnx, tag in ((fn13, "fn=1.00MHz"), (fn_opt, f"fn={fn_opt/1e6:.2f}MHz")):
        S0 = output_psd(f, fnx, N_DIV)[0]
        s0 = integ_jitter(f, S0, F0)
        print(f"    [{tag}] without R: sigma_t = {s0*1e15:.1f} fs")
        for icp in ICPS:
            S_R, R, C = resistor_psd(f, fnx, icp)
            sR = integ_jitter(f, S_R, F0)
            s1 = integ_jitter(f, S0 + S_R, F0)
            ipk = int(np.argmin(abs(f - fnx)))
            rows[(tag, icp)] = (R, C, sR, s1, s0)
            print(f"      Icp={label_icp(icp):>7}: R={R/1e3:9.2f} kohm C={C*1e12:9.4f} pF  "
                  f"S_R(fn)={S_R[ipk]:.2e}  sigma_R={sR*1e15:6.2f} fs  "
                  f"with R={s1*1e15:6.1f} fs  (+{(s1/s0-1)*100:.2f} %)")

    # ---- sweep fn with R re-designed at every fn ------------------------------
    jitR = {}
    for icp in ICPS:
        jitR[icp] = np.array([
            integ_jitter(f, output_psd(f, fnx, N_DIV)[0] + resistor_psd(f, fnx, icp)[0], F0)
            for fnx in fns])
        k = int(np.argmin(jitR[icp]))
        print(f"    sweep Icp={label_icp(icp):>7}: optimum fn = {fns[k]/1e6:.2f} MHz, "
              f"sigma_t = {jitR[icp][k]*1e15:.1f} fs")

    # ---- I_cp that makes the resistor term 'negligible' (<1 % of sigma_t) -----
    s_opt = jit0[kopt]
    sR_max = s_opt * np.sqrt(1.01 ** 2 - 1)
    icp_1pct = var_cf / (sR_max * 2 * np.pi * F0) ** 2 * ICPS[0]
    print(f"    <1 % jitter penalty at the optimum needs sigma_R < {sR_max*1e15:.1f} fs "
          f"-> Icp > {icp_1pct*1e6:.0f} uA")

    # ---- figure ---------------------------------------------------------------
    fig, axes = plt.subplots(1, 3, figsize=(17.5, 4.9))
    for ax, fnx, ttl in ((axes[0], fn13, "(a) lab_13 的環（$f_n$=1 MHz）：電阻項 vs 預算"),
                         (axes[1], fn_opt, f"(b) 最佳 loop BW（$f_n$≈{fn_opt/1e6:.2f} MHz）")):
        S0, inb, outb = output_psd(f, fnx, N_DIV)
        ax.loglog(f, inb, color="tab:blue", ls=":", lw=1.1, label="ref×N² + CP/PFD（低通）")
        ax.loglog(f, outb, color="tab:red", ls=":", lw=1.1, label="VCO（高通）")
        ax.loglog(f, S0, color="black", lw=2, label="lab_20 總和（無電阻項）")
        for icp, col in zip(ICPS, COLORS):
            S_R, R, _ = resistor_psd(f, fnx, icp)
            ax.loglog(f, S_R, color=col, lw=1.5,
                      label=f"電阻項 $I_{{cp}}$={label_icp(icp)}（R={label_r(R)}）")
        S_R0 = resistor_psd(f, fnx, ICPS[0])[0]
        ax.loglog(f, S0 + S_R0, color="gray", ls="--", lw=1.3,
                  label=f"總和 + 電阻項（{label_icp(ICPS[0])}）")
        ax.axvline(fnx, color="gray", ls="-.", lw=0.8)
        ax.set_ylim(1e-17, 1e-8)
        ax.set_xlabel("offset frequency [Hz]")
        ax.set_ylabel(r"$S_\phi$ [rad$^2$/Hz]")
        ax.set_title(ttl)
        ax.legend(fontsize=7, loc="upper right")

    ax = axes[2]
    ax.loglog(fns, jit0 / 1e-15, color="black", lw=2, label="lab_20（無電阻項）")
    for icp, col in zip(ICPS, COLORS):
        ax.loglog(fns, jitR[icp] / 1e-15, color=col, lw=1.4, ls="--",
                  label=f"+ 電阻項 $I_{{cp}}$={label_icp(icp)}")
    ax.plot(fns[kopt], jit0[kopt] / 1e-15, "o", color="tab:red", ms=7,
            label=f"最佳點 {jit0[kopt]*1e15:.0f} fs")
    ax.axhline(np.sqrt(var_cf) / (2 * np.pi * F0) / 1e-15, color=COLORS[0], ls=":", lw=1,
               label=f"電阻項單獨 {np.sqrt(var_cf)/(2*np.pi*F0)*1e15:.0f} fs（{label_icp(ICPS[0])}，與 $f_n$ 無關）")
    ax.set_xlabel("loop bandwidth $f_n$ [Hz]")
    ax.set_ylabel(r"integrated rms jitter $\sigma_t$ [fs]")
    ax.set_title("(c) 積分 jitter：電阻項抬高整條 U 形、最佳 $f_n$ 不動")
    ax.legend(fontsize=7.5)
    ax.grid(True, which="both", alpha=0.3)
    savefig(fig, "pll_budget_rnoise.png")


if __name__ == "__main__":
    main()
