"""
lab_33_asymmetry_corner.py

Goal
----
Numerically verify the [P2] Appendix B closed forms for the ASYMMETRIC
triangular ring-oscillator ISF (Fig. 18, p.803), and turn Eq.(57) into two
design curves:

  Eq.(52), p.803 : Gamma_rms^2 = (1/3pi) * (1/f'_rise)^3 * (1 + A^3)
  Eq.(53), p.803 : A = f'_rise / f'_fall     (waveform asymmetry ratio)
  Eq.(54), p.803 : 2pi = eta*N*(1/f'_rise + 1/f'_fall) = (eta*N/f'_rise)(1+A)
  Eq.(55), p.803 : Gamma_rms^2 = (2pi^2/(3 eta^3)) * (1/N^3) * [4(1+A^3)/(1+A)^3]
  Eq.(56), p.803 : Gamma_dc    = (2pi/eta^2) * (1/N^2) * (1-A)/(1+A)
  Eq.(57), p.803 : f_{1/f^3}   = f_{1/f} * (3/(2 eta N)) * (1-A)^2/(1-A+A^2)
  Eq.(7),  p.792 : f_{1/f^3}   = f_{1/f} * Gamma_dc^2 / Gamma_rms^2
                   (the corner relation Eq.(57) is derived from; NOTE it is
                   exactly HALF of [P1] Eq.(24) once c0 = 2*Gamma_dc is
                   substituted -- a bookkeeping/convention factor 2, flagged
                   in the teaching page.)

Model (exactly Fig. 18, p.803): one positive triangular lobe of height
1/f'_rise and base width 2/f'_rise (unit slopes in x), one negative lobe of
depth 1/f'_fall and base width 2/f'_fall.  Lobe POSITION along x does not
enter Gamma_rms / Gamma_dc, so we place the positive lobe at x=0..w_r and the
negative lobe at x = 2pi-w_f .. 2pi (no overlap needs w_r + w_f <= 2pi, i.e.
N >= 2/eta -- satisfied by the whole grid).

Checks
------
1. (N, A) grid: numeric trapezoid Gamma_rms^2 / Gamma_dc vs Eq.(55)/(56),
   and c0 from compute_fourier_coefficients vs 2*Gamma_dc  -> all < 0.5 %.
2. A = 1 reduces Eq.(55) to Eq.(16) p.794 (v7 form: bracket -> 1).
3. Worked numbers N=5, eta=1, f_1/f = 1 MHz, A = 1.5 and A = 3
   (both Eq.(57) and the [P1] Eq.(24) convention = 2x), corner ratio = 4.
4. Corner sweeps: V-curve vs A (Fig.17-style symmetry dip, log-A symmetric
   because (1-A)^2/(1-A+A^2) is invariant under A -> 1/A) and 1/N law vs N.

This is the [P2] triangular APPROXIMATION of a ring ISF (linear-ramp edges,
eta ~ 1), NOT a transistor-level extraction -- lab_32 shows how far a real
(Level-1) 3-stage ring deviates from it.

Figure
------
  static/figures/asymmetry_corner.png
    (a) Gamma(x) for N=5, A = 1 / 1.5 / 3, (b) f_{1/f^3} vs A (V-curve),
    (c) f_{1/f^3} vs N (log-log, 1/N guide).

Run
---
    PYTHONPATH=. python simulations/lab_33_asymmetry_corner.py   (~5 s)
"""
import os
import sys
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.join(_HERE, "common"))

import numpy as np

ETA = 1.0            # stage-delay proportionality constant ([P2] Eq.(14)), ~1
F_1F = 1e6           # device 1/f corner [Hz] (site-canonical 1 MHz)
N_TH = 400_001       # theta grid points over one period [0, 2pi]
N_HARM = 40          # harmonics for the Fourier cross-check


# ---------------------------------------------------------------------------
# The Fig. 18 piecewise-triangular ISF (unit slopes; heights/widths from
# Eq.(53)+(54):  1/f'_rise = 2pi/(eta*N*(1+A)),  1/f'_fall = A/f'_rise^-1... )
# ---------------------------------------------------------------------------
def lobe_heights(n_stages, a_ratio, eta=ETA):
    """Peak heights h_r = 1/f'_rise, h_f = 1/f'_fall from Eq.(54)+(53)."""
    h_r = 2.0 * np.pi / (eta * n_stages * (1.0 + a_ratio))
    return h_r, a_ratio * h_r


def gamma_fig18(theta, n_stages, a_ratio, eta=ETA):
    """Piecewise triangular Gamma(x) of [P2] Fig. 18, p.803 (unit slopes:
    each lobe's height equals its half-width, so 'peak = 1/f', width = 2/f''
    holds automatically).  theta in [0, 2pi]."""
    h_r, h_f = lobe_heights(n_stages, a_ratio, eta)
    pos = np.maximum(h_r - np.abs(theta - h_r), 0.0)              # [0, 2h_r]
    neg = np.maximum(h_f - np.abs(theta - (2.0 * np.pi - h_f)), 0.0)
    return pos - neg


# ---------------------------------------------------------------------------
# Closed forms (verbatim [P2] App. B, p.803)
# ---------------------------------------------------------------------------
def grms2_eq52(n_stages, a_ratio, eta=ETA):
    h_r, _ = lobe_heights(n_stages, a_ratio, eta)
    return (1.0 / (3.0 * np.pi)) * h_r ** 3 * (1.0 + a_ratio ** 3)


def grms2_eq55(n_stages, a_ratio, eta=ETA):
    return (2.0 * np.pi ** 2 / (3.0 * eta ** 3)) / n_stages ** 3 \
        * 4.0 * (1.0 + a_ratio ** 3) / (1.0 + a_ratio) ** 3


def gdc_eq56(n_stages, a_ratio, eta=ETA):
    return (2.0 * np.pi / eta ** 2) / n_stages ** 2 \
        * (1.0 - a_ratio) / (1.0 + a_ratio)


def corner_eq57(f_1f, n_stages, a_ratio, eta=ETA):
    return f_1f * (3.0 / (2.0 * eta * n_stages)) \
        * (1.0 - a_ratio) ** 2 / (1.0 - a_ratio + a_ratio ** 2)


# ---------------------------------------------------------------------------
def main():
    import matplotlib.pyplot as plt
    from plot_utils import savefig
    from isf_utils import compute_fourier_coefficients, gamma_rms

    t_start = time.time()
    print("[lab_33] [P2] App.B asymmetric triangular ISF closed forms "
          "(Fig.18 + Eq.(52)-(57), p.803) vs numeric integration ...")

    theta = np.linspace(0.0, 2.0 * np.pi, N_TH)

    # ---- 1) (N, A) grid: numeric vs closed forms --------------------------
    n_grid = [3, 4, 5, 7, 9, 12, 15]
    a_grid = [1.0, 1.25, 1.5, 2.0, 3.0, 4.0]
    err_rms = 0.0
    err_dc = 0.0
    err_c0 = 0.0
    err_52_55 = 0.0
    for n_st in n_grid:
        for a_r in a_grid:
            g = gamma_fig18(theta, n_st, a_r)
            # numeric Gamma_rms^2 and Gamma_dc (trapezoid over one period)
            g2_num = float(gamma_rms(theta, g)) ** 2
            gdc_num = float(np.trapezoid(g, theta) / (2.0 * np.pi))
            g2_ref = grms2_eq55(n_st, a_r)
            gdc_ref = gdc_eq56(n_st, a_r)
            err_rms = max(err_rms, abs(g2_num - g2_ref) / g2_ref)
            err_52_55 = max(err_52_55, abs(grms2_eq52(n_st, a_r) - g2_ref)
                            / g2_ref)
            # c0 from the site's Fourier helper: a0 = c0, DC value = c0/2
            a0, _, _, _, _ = compute_fourier_coefficients(theta, g, 2)
            if a_r != 1.0:
                err_dc = max(err_dc, abs(gdc_num - gdc_ref) / abs(gdc_ref))
                err_c0 = max(err_c0, abs(float(a0) - 2.0 * gdc_ref)
                             / abs(2.0 * gdc_ref))
            else:  # Gamma_dc = 0 exactly: absolute check vs peak height
                h_r, _ = lobe_heights(n_st, a_r)
                assert abs(gdc_num) < 1e-9 * h_r and abs(float(a0)) < 1e-9 * h_r
    print("grid: N in", n_grid, ", A in", a_grid, "->",
          len(n_grid) * len(a_grid), "cases")
    print("max |Gamma_rms^2 numeric - Eq.(55)| / Eq.(55) =",
          "{:.2e}".format(err_rms))
    # -> 1.17e-09（42 組全部遠低於 0.5% 門檻：Eq.(55) 與數值積分一致）
    print("max |Gamma_dc  numeric - Eq.(56)| / Eq.(56)  =",
          "{:.2e}".format(err_dc))
    # -> 1.60e-09（Eq.(56) 與數值平均一致）
    print("max |c0 (Fourier a0) - 2*Gamma_dc| / |2*Gamma_dc| =",
          "{:.2e}".format(err_c0))
    # -> 1.60e-09（compute_fourier_coefficients 的 a0 = c0 = 2*Gamma_dc）
    print("max |Eq.(52) - Eq.(55)| / Eq.(55) (pure algebra) =",
          "{:.2e}".format(err_52_55))
    # -> 4.28e-16（Eq.(52)+(54) 代數合併 = Eq.(55)，機器精度）
    assert err_rms < 5e-3 and err_dc < 5e-3 and err_c0 < 5e-3

    # ---- 2) A = 1 reduces Eq.(55) to Eq.(16) p.794 (v7 form) --------------
    g_rms_a1 = np.sqrt(grms2_eq55(5, 1.0))
    g_rms_16 = np.sqrt(2.0 * np.pi ** 2 / (3.0 * ETA ** 3)) / 5 ** 1.5
    print("A=1, N=5: sqrt(Eq.55) =", round(float(g_rms_a1), 6),
          "; Eq.(16) sqrt(2pi^2/(3 eta^3))/N^1.5 =",
          round(float(g_rms_16), 6),
          "; bracket 4(1+A^3)/(1+A)^3 =",
          round(4.0 * 2.0 / 8.0, 6))
    # -> 0.229429 = 0.229429（A=1 時括號 = 1，Eq.(55) 精確退化為 Eq.(16) v7 形）

    # ---- 3) worked numbers: N=5, eta=1, f_1/f = 1 MHz ---------------------
    print("worked numbers (N=5, eta=1, f_1/f = 1 MHz):")
    stash = {}
    for a_r in (1.5, 3.0):
        g_rms = float(np.sqrt(grms2_eq55(5, a_r)))
        g_dc = float(gdc_eq56(5, a_r))
        c0 = 2.0 * g_dc
        fc57 = float(corner_eq57(F_1F, 5, a_r))
        fc7 = F_1F * g_dc ** 2 / g_rms ** 2          # [P2] Eq.(7) direct
        fc_p1 = F_1F * c0 ** 2 / (2.0 * g_rms ** 2)  # [P1] Eq.(24) convention
        stash[a_r] = fc57
        print(f"  A={a_r}: Gamma_rms =", round(g_rms, 4),
              "; Gamma_dc =", round(g_dc, 5),
              "; c0 = 2*Gamma_dc =", round(c0, 4))
        print(f"        f_1/f3 Eq.(57) =", round(fc57 / 1e3, 2),
              "kHz ; via Eq.(7) =", round(fc7 / 1e3, 2),
              "kHz ; [P1] Eq.(24) c0^2/(2 Grms^2) =",
              round(fc_p1 / 1e3, 2), "kHz (= 2x, convention)")
    # -> A=1.5: Gamma_rms 0.2428, Gamma_dc -0.05027, c0 -0.1005;
    #    corner 42.86 kHz（Eq.(57) = Eq.(7)）; [P1] Eq.(24) 慣例 85.71 kHz
    # -> A=3.0: Gamma_rms 0.3035, Gamma_dc -0.12566, c0 -0.2513;
    #    corner 171.43 kHz（Eq.(57) = Eq.(7)）; [P1] Eq.(24) 慣例 342.86 kHz
    print("corner ratio (A: 1.5 -> 3) =",
          round(stash[3.0] / stash[1.5], 4),
          "(convention-free: the factor 2 cancels)")
    # -> 4.0（NumericQuiz 用；兩種慣例的 2 倍在比值中相消）
    # closed-form ratio: [4/7] / [1/7] = 4 exactly
    print("closed-form ratio check: ((1-3)^2/(1-3+9)) / ((1-1.5)^2/(1-1.5+2.25)) =",
          round(((4.0 / 7.0) / (0.25 / 1.75)), 4))
    # -> 4.0（(1-A)^2/(1-A+A^2)：A=3 給 4/7、A=1.5 給 1/7）

    # corner -> 0 as A -> 1 (from both sides), and A <-> 1/A symmetry
    print("corner(A)/f_1/f at N=5: A=1.01 ->",
          "{:.2e}".format(float(corner_eq57(1.0, 5, 1.01))),
          "; A=1.10 ->", "{:.2e}".format(float(corner_eq57(1.0, 5, 1.10))),
          "; A=2 ->", "{:.2e}".format(float(corner_eq57(1.0, 5, 2.0))))
    # -> 2.97e-05 / 2.70e-03 / 1.00e-01（A→1 時 corner→0：(1-A)^2 二次趨零）
    print("A <-> 1/A symmetry: corner(A=2) =",
          "{:.6e}".format(float(corner_eq57(1.0, 5, 2.0))),
          "= corner(A=0.5) =",
          "{:.6e}".format(float(corner_eq57(1.0, 5, 0.5))))
    # -> 1.000000e-01 = 1.000000e-01（V 形谷對 log A 左右對稱）

    # 1/N law at fixed A ([P2]'s own sentence, p.803)
    print("corner vs N at A=1.5: N=3 ->",
          round(float(corner_eq57(F_1F, 3, 1.5)) / 1e3, 2), "kHz ; N=5 ->",
          round(float(corner_eq57(F_1F, 5, 1.5)) / 1e3, 2), "kHz ; N=9 ->",
          round(float(corner_eq57(F_1F, 9, 1.5)) / 1e3, 2), "kHz ; N=15 ->",
          round(float(corner_eq57(F_1F, 15, 1.5)) / 1e3, 2), "kHz")
    # -> 71.43 / 42.86 / 23.81 / 14.29 kHz（corner ∝ 1/N：級數越少 corner 越高）
    print("N=3 / N=15 corner ratio =",
          round(float(corner_eq57(F_1F, 3, 1.5) / corner_eq57(F_1F, 15, 1.5)),
                4), "(expect 5 = 15/3)")
    # -> 5.0（1/N 律精確成立）

    # ------------------------------------------------------------------ fig
    fig, axes = plt.subplots(1, 3, figsize=(14.5, 4.4))

    # (a) Gamma(x) for N=5, A = 1 / 1.5 / 3
    ax = axes[0]
    frac = theta / (2.0 * np.pi)
    for a_r, col in [(1.0, "tab:gray"), (1.5, "tab:blue"), (3.0, "tab:red")]:
        g = gamma_fig18(theta, 5, a_r)
        gdc = gdc_eq56(5, a_r)
        ax.plot(frac, g, color=col, lw=1.8,
                label=fr"$A$={a_r:g}: $\Gamma_{{dc}}$={gdc:+.3f}")
        ax.axhline(gdc, color=col, lw=0.9, ls=":")
    ax.axhline(0.0, color="k", lw=0.6)
    ax.set_xlabel(r"注入相位 $x/2\pi$（$x=\omega_0\tau$ [rad]）")
    ax.set_ylabel(r"$\Gamma(x)$ [無因次]")
    ax.set_title("(a) [P2] Fig.18 非對稱三角 ISF（$N$=5, $\\eta$=1）\n"
                 "正葉 $1/f'_{rise}$、負葉 $1/f'_{fall}$，虛線 = $\\Gamma_{dc}$"
                 "（Eq.(56)）")
    ax.legend(fontsize=8, loc="lower left")

    # (b) V-curve: corner vs A (log-x), N = 3 / 5 / 9
    ax = axes[1]
    a_sweep = np.logspace(np.log10(0.25), np.log10(4.0), 401)
    for n_st, col in [(3, "tab:green"), (5, "tab:blue"), (9, "tab:purple")]:
        ax.plot(a_sweep, corner_eq57(F_1F, n_st, a_sweep) / 1e3, color=col,
                lw=1.8, label=fr"$N$={n_st}")
    for a_r in (1.5, 3.0):
        ax.plot(a_r, corner_eq57(F_1F, 5, a_r) / 1e3, "o", ms=6,
                color="tab:blue")
        ax.annotate(f"{corner_eq57(F_1F, 5, a_r)/1e3:.1f} kHz",
                    (a_r, corner_eq57(F_1F, 5, a_r) / 1e3),
                    textcoords="offset points", xytext=(6, -12), fontsize=8)
    ax.axvline(1.0, color="gray", lw=0.9, ls="--")
    ax.set_xscale("log")
    ax.set_xticks([0.25, 0.5, 1, 2, 4])
    ax.set_xticklabels(["0.25", "0.5", "1", "2", "4"])
    ax.set_xlabel(r"不對稱比 $A=f'_{rise}/f'_{fall}$ [無因次]（log 軸）")
    ax.set_ylabel(r"$f_{1/f^3}$ [kHz]（$f_{1/f}$=1 MHz）")
    ax.set_title("(b) Eq.(57)：對稱點 $A$=1 的 V 形谷底\n"
                 "（[P2] Fig.17 對稱電壓碗底的解析版；對 $A\\to1/A$ 對稱）")
    ax.legend(fontsize=8)

    # (c) corner vs N (log-log) at A = 1.5 / 2 / 3 + 1/N guide
    ax = axes[2]
    n_sweep = np.arange(3, 16)
    for a_r, col in [(1.5, "tab:blue"), (2.0, "tab:orange"),
                     (3.0, "tab:red")]:
        ax.plot(n_sweep, corner_eq57(F_1F, n_sweep, a_r) / 1e3, "o-",
                color=col, ms=4, lw=1.6, label=fr"$A$={a_r:g}")
    guide = corner_eq57(F_1F, 3, 3.0) / 1e3 * 3.0 / n_sweep
    ax.plot(n_sweep, guide, "k--", lw=1.0, label=r"$\propto 1/N$ 參考線")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xticks([3, 5, 7, 9, 12, 15])
    ax.set_xticklabels(["3", "5", "7", "9", "12", "15"])
    ax.xaxis.set_minor_formatter(plt.NullFormatter())
    ax.set_xlabel(r"級數 $N$ [無因次]（log 軸）")
    ax.set_ylabel(r"$f_{1/f^3}$ [kHz]（$f_{1/f}$=1 MHz，log 軸）")
    ax.set_title("(c) Eq.(57)：固定 $A$ 下 corner $\\propto 1/N$\n"
                 "（級數越少 → 1/f$^3$ corner 越高；[P2] p.803 原句）")
    ax.legend(fontsize=8)

    savefig(fig, "asymmetry_corner.png")
    print("runtime =", round(time.time() - t_start, 1), "s")


if __name__ == "__main__":
    main()
