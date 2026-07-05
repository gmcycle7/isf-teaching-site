"""
lab_39_optimal_injection.py

Goal
----
[P3] Sec. VI (pp. 2119-2120): for a FIXED rms injection current

    I_rms = sqrt( (1/T_inj) * integral_{T_inj} i_inj(t)^2 dt )   [P3] Eq.(43), p.2119

which periodic injection waveform maximizes the injection-locking lock range?
Cauchy-Schwarz answer:

    i*_inj,0(x) = +/- (I_rms / Gt_rms) * Gt(x)        [P3] Eq.(44), p.2119
    omega_L*    = I_rms * Gt_rms                      [P3] Eq.(45), p.2120

where Gt = Gamma/q_max is the unitful ISF [rad/C] and Gt_rms its rms over one
period. This lab verifies the bound numerically on three ISFs, computing the
lock characteristic from the verified [P3] Eq.(33), p.2114,

    Omega(theta) = (1/T_inj) integral Gt(w_inj*t + theta) i_inj(t) dt

as a circular cross-correlation on a uniform phase grid.

Cases
-----
  (1) ideal-LC ISF Gamma = -sin: the matched waveform IS a sine, so a
      phase-aligned sinusoidal injection of the same I_rms is already
      optimal (ratio must print 1.0000);
  (2) the site's asymmetric toy ISF Gamma = cos(theta) + alpha (alpha = 0.3):
      matched injection gains G = sqrt(1 + 2*alpha^2) over the best sine by
      spending part of the rms budget on a DC component that couples to c0.
      The +/- sign of Eq.(44) picks WHICH lock edge you optimize: the
      + solution raises the upper edge but WORSENS the lower edge;
  (3) ring-style ISF from the [P2] App.B model (A = 1, i.e. equal rise/fall):
      two opposite-sign triangular pulses of height 1/f' and half-width
      1/f' rad, with f' = eta*N/pi from [P2] Eq.(54) (2*pi = eta*N*(1+A)/f',
      A = 1). Sanity: this reproduces Gamma_rms^2 = (2*pi^2/(3*eta^3))/N^3
      ([P2] Eq.(55), A = 1) exactly. Narrow-pulse closed form for the
      matched/sine lock-range gain:
          G = sqrt(2)*Gamma_rms/c1,  c1 ~= 2*h*w/pi  ->  G ~= sqrt(eta*N/3)
      For N = 17, eta = 0.75: G ~= 2.06 -- echoing [P3] Fig. 19 / p.2120:
      "the lock range is almost doubled compared to a sinusoidal injection
      of the same power" (17-stage single-ended ring).
      Also printed: the site's cruder gamma_triangular toy is pi-periodic
      (even harmonics only), so its c1 = 0 and a fundamental-frequency sine
      cannot lock it at all -- a toy artifact worth knowing about.

Canonical numbers: q_max = 1 pC; I_rms = 62.832 uA / sqrt(2) = 44.429 uA
(the same 62.83-uA-PEAK sine that gives f_L = 5 MHz on the ideal LC in the
injection_locking_noise page).

Figure
------
  static/figures/optimal_injection_lock_range.png

Run
---
  PYTHONPATH=<project root> python simulations/lab_39_optimal_injection.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt

from plot_utils import savefig
from isf_utils import (gamma_lc_ideal, gamma_asymmetric, gamma_triangular,
                       gamma_rms, compute_fourier_coefficients)

# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------
QMAX = 1e-12                      # q_max                       [C]
I_PK_SINE = 62.832e-6             # peak sine current (page's 5-MHz LC case) [A]
I_RMS = I_PK_SINE / np.sqrt(2)    # fixed rms budget            [A]
N_GRID = 4096                     # phase-grid points per period
ETA = 0.75                        # [P2] stage-delay proportionality constant
N_RING = 17                       # ring stages ([P3] Fig. 19 uses 17 stages)
ALPHA = 0.3                       # site toy asymmetry

# periodic grid (no endpoint) for circular correlation; endpoint-inclusive
# grid for trapz-based Fourier / rms helpers from isf_utils
X = np.arange(N_GRID) * 2 * np.pi / N_GRID
XE = np.linspace(0.0, 2 * np.pi, N_GRID + 1)


def lock_characteristic(gt, i_wave):
    """
    Omega(theta_j) = mean_k[ Gt(x_k + theta_j) * i(x_k) ]   [rad/s]
    ([P3] Eq.(33), p.2114, with x = w_inj*t; circular cross-correlation.)
    """
    n = gt.size
    Gf = np.fft.rfft(gt)
    If = np.fft.rfft(i_wave)
    # (1/n) sum_k gt[k+j] i[k]  =  (1/n) irfft( conj(rfft(i)) * rfft(gt) )
    return np.fft.irfft(np.conj(If) * Gf, n) / n


def rms(v):
    return np.sqrt(np.mean(v ** 2))


def report_case(name, gamma_e, gamma_p):
    """
    gamma_e : dimensionless ISF on the endpoint-inclusive grid XE
    gamma_p : same ISF on the periodic grid X
    Returns dict of the numbers we print.
    """
    gt_p = gamma_p / QMAX                              # unitful ISF [rad/C]
    g_rms = gamma_rms(XE, gamma_e)                     # dimensionless
    gt_rms = g_rms / QMAX                              # [rad/C]

    # ISF fundamental (for the best sine of the same I_rms)
    a0, a, b, c, _ = compute_fourier_coefficients(XE, gamma_e, 8)
    c1 = c[1]

    # --- sine injection, same I_rms (peak = sqrt(2)*I_rms) ----------------
    i_sine = np.sqrt(2) * I_RMS * np.cos(X)
    om_sine = lock_characteristic(gt_p, i_sine)
    wl_sine = om_sine.max()                            # upper lock edge [rad/s]

    # --- matched injection, [P3] Eq.(44) with the + sign ------------------
    i_star = +(I_RMS / gt_rms) * gt_p
    om_star = lock_characteristic(gt_p, i_star)
    wl_star = om_star.max()

    bound = I_RMS * gt_rms                             # [P3] Eq.(45) [rad/s]

    print(f"  [{name}]")
    print(f"    Gamma_rms = {g_rms:.5f}   c1 = {c1:.5f}   (dimensionless)")
    print(f"    I_rms check: sine {rms(i_sine)*1e6:.3f} uA, "
          f"matched {rms(i_star)*1e6:.3f} uA  (budget {I_RMS*1e6:.3f} uA)")
    print(f"    f_L sine    = {wl_sine/2/np.pi/1e6:.4f} MHz")
    print(f"    f_L matched = {wl_star/2/np.pi/1e6:.4f} MHz")
    print(f"    bound I_rms*Gt_rms = {bound/2/np.pi/1e6:.4f} MHz "
          f"-> matched/bound = {wl_star/bound:.4f}")
    print(f"    gain matched/sine = {wl_star/wl_sine:.4f}   "
          f"(analytic sqrt(2)*Gamma_rms/c1 = {np.sqrt(2)*g_rms/c1:.4f})")
    return dict(g_rms=g_rms, c1=c1, om_sine=om_sine, om_star=om_star,
                wl_sine=wl_sine, wl_star=wl_star, bound=bound)


def gamma_ring_p2(x, n_stages, eta=ETA):
    """
    Ring-style toy ISF from the [P2] App.B construction with A = 1
    (symmetric rise/fall): two opposite-sign triangular pulses, height 1/f',
    half-width 1/f' [rad], where f' = eta*N/pi ([P2] Eq.(54) with A = 1).
    Reproduces [P2] Eq.(55) at A = 1: Gamma_rms^2 = (2*pi^2/(3*eta^3))/N^3.
    Rising-edge pulse (+) at x = pi/2, falling-edge pulse (-) at x = 3*pi/2.
    TOY MODEL (pedagogical), not an extracted transistor-level ISF.
    """
    fp = eta * n_stages / np.pi        # normalized transition slope [1/rad]
    h = 1.0 / fp                       # pulse height
    w = 1.0 / fp                       # pulse half-width [rad]

    def tri(center):
        d = np.angle(np.exp(1j * (x - center)))     # wrapped distance [rad]
        return np.clip(1.0 - np.abs(d) / w, 0.0, None)

    return h * (tri(np.pi / 2) - tri(3 * np.pi / 2))


def main():
    print("[lab_33] optimal injection waveform: Cauchy-Schwarz lock-range "
          "bound ([P3] Eq.(43)-(45)) ...")
    print(f"  budget: I_rms = {I_RMS*1e6:.3f} uA "
          f"(= {I_PK_SINE*1e6:.3f} uA peak sine), q_max = {QMAX*1e12:.0f} pC")

    # ------------------------------------------------------------------ (1)
    lc = report_case("ideal LC, Gamma = -sin",
                     gamma_lc_ideal(XE), gamma_lc_ideal(X))

    # ------------------------------------------------------------------ (2)
    asym = report_case(f"asymmetric toy, Gamma = cos + {ALPHA}",
                       gamma_asymmetric(XE, ALPHA), gamma_asymmetric(X, ALPHA))
    print(f"    analytic gain sqrt(1+2*alpha^2) = {np.sqrt(1+2*ALPHA**2):.4f}")
    # the +/- of Eq.(44): + optimizes the UPPER edge, worsens the LOWER edge
    up_star = asym['om_star'].max() / (I_RMS / QMAX)
    lo_star = asym['om_star'].min() / (I_RMS / QMAX)
    up_sine = asym['om_sine'].max() / (I_RMS / QMAX)
    print(f"    edges in units of I_rms/q_max: matched(+) upper {up_star:+.4f}"
          f" / lower {lo_star:+.4f}; sine +/-{up_sine:.4f}")

    # ------------------------------------------------------------------ (3)
    ring = report_case(f"ring pulses [P2] App.B A=1, N={N_RING}, eta={ETA}",
                       gamma_ring_p2(XE, N_RING), gamma_ring_p2(X, N_RING))
    g_rms_formula = np.sqrt(2 * np.pi ** 2 / (3 * ETA ** 3)) / N_RING ** 1.5
    print(f"    Gamma_rms vs [P2] Eq.(55) closed form "
          f"sqrt(2pi^2/3eta^3)/N^1.5 = {g_rms_formula:.5f}")
    print(f"    narrow-pulse closed-form gain sqrt(eta*N/3) = "
          f"{np.sqrt(ETA*N_RING/3):.4f}")

    # site's cruder triangular toy: pi-periodic -> c1 = 0 (fundamental sine
    # cannot lock it at all; toy artifact worth knowing)
    _, _, _, c_tri, _ = compute_fourier_coefficients(
        XE, gamma_triangular(XE, 5), 8)
    print(f"    site gamma_triangular(N=5) c1 = {c_tri[1]:.6f} "
          f"(pi-periodic toy: even harmonics only), c2 = {c_tri[2]:.4f}")

    # ------------------------------------------------------------- figure
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.6))

    ax = axes[0]
    gt_ring_p = gamma_ring_p2(X, N_RING) / QMAX
    i_star = (I_RMS / (ring['g_rms'] / QMAX)) * gt_ring_p
    i_sine = np.sqrt(2) * I_RMS * np.cos(X - np.pi / 2)  # peak aligned on pulse
    ax.plot(X / np.pi, i_star / I_RMS, color="tab:red", lw=2.0,
            label=r"匹配注入 $i^*\propto\tilde\Gamma$（[P3] Eq.(44)）")
    ax.plot(X / np.pi, i_sine / I_RMS, color="tab:blue", ls="--", lw=1.6,
            label=r"正弦注入（同一個 $I_{rms}$，相位對齊）")
    ax.axhline(0, color="gray", lw=0.8)
    ax.set_xlabel(r"注入相位 $x/\pi$  [rad/$\pi$]")
    ax.set_ylabel(r"$i_{inj}(x)/I_{rms}$  [—]")
    ax.set_title(f"(a) 同一個 rms 預算的兩種花法（ring 型 ISF, N={N_RING}）\n"
                 "匹配波形把電流全押在 ISF 脈衝上；正弦把大半電流\n"
                 r"花在 $\tilde\Gamma\approx0$ 的相位（買不到 lock range）")
    ax.legend(fontsize=8, loc="lower left")

    ax = axes[1]
    f_scale = 1 / (2 * np.pi * 1e3)   # rad/s -> kHz
    ax.plot(X / np.pi, ring['om_star'] * f_scale, color="tab:red", lw=2.0,
            label=r"匹配注入的 $\Omega(\theta)/2\pi$")
    ax.plot(X / np.pi, ring['om_sine'] * f_scale, color="tab:blue", ls="--",
            lw=1.6, label=r"正弦注入的 $\Omega(\theta)/2\pi$")
    ax.axhline(ring['bound'] * f_scale, color="k", ls=":", lw=1.4,
               label=r"上限 $\pm\,I_{rms}\tilde\Gamma_{rms}/2\pi$（[P3] Eq.(45)）")
    ax.axhline(-ring['bound'] * f_scale, color="k", ls=":", lw=1.4)
    ax.annotate(f"{ring['wl_star']*f_scale:.0f} kHz",
                xy=(0.02, ring['wl_star'] * f_scale),
                xytext=(0.25, ring['wl_star'] * f_scale * 0.82),
                color="tab:red", fontsize=9,
                arrowprops=dict(arrowstyle="->", color="tab:red", lw=1.0))
    ax.annotate(f"{ring['wl_sine']*f_scale:.0f} kHz",
                xy=(1.52, ring['wl_sine'] * f_scale),
                xytext=(1.30, ring['wl_sine'] * f_scale * 1.55),
                color="tab:blue", fontsize=9,
                arrowprops=dict(arrowstyle="->", color="tab:blue", lw=1.0))
    ax.set_xlabel(r"相位差 $\theta/\pi$  [rad/$\pi$]")
    ax.set_ylabel(r"$\Omega(\theta)/2\pi$  [kHz]")
    ax.set_title("(b) lock characteristic（[P3] Eq.(33)）：極值＝lock edge\n"
                 f"匹配注入恰好碰到 Cauchy–Schwarz 上限，"
                 f"增益 ×{ring['wl_star']/ring['wl_sine']:.2f}"
                 r"（$\approx\sqrt{\eta N/3}$）")
    ax.legend(fontsize=8, loc="lower left")

    fig.suptitle(r"注入波形設計：固定 $I_{rms}$ 下 lock range 的上限 "
                 r"$\omega_L^*=I_{rms}\tilde\Gamma_{rms}$"
                 f"（[P3] Eq.(43)–(45)；$I_{{rms}}$={I_RMS*1e6:.1f} μA, "
                 f"$q_{{max}}$=1 pC；toy ISF）", fontsize=11)
    savefig(fig, "optimal_injection_lock_range.png")


if __name__ == "__main__":
    main()
