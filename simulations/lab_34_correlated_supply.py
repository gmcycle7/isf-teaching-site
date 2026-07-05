"""
lab_34_correlated_supply.py

Goal
----
[P2] Hajimiri-Limotyrakis-Lee (1999) Sec. VI, p.797, Eqs. (37)-(38):
supply/substrate noise is CORRELATED across all N ring-oscillator nodes.
For identical sources on all N nodes, the effective ISF is the SUM of N
phase-shifted per-stage ISFs, and a finite geometric sum kills every Fourier
component except n = 0 (mod N).  Consequence: correlated noise upconverts
into phase only from bands near k*N*f0 (and near DC, via the summed ISF's
c0); uncorrelated per-stage noise sees no such selection rule.

Three demonstrations (one figure, three panels):
  (a) per-stage ISFs (N=5 shifted copies of a dual-lobe toy ring ISF) and
      their sum Gamma_Sigma;
  (b) |c_n| spectrum of the single-stage vs the summed ISF -> comb at
      n = 0, 5, 10, 15 (everything else at the numeric floor);
  (c) time domain: inject a common sinusoidal "supply" current at
      f_inj = n*f0 + df into all 5 nodes (correlated) vs into 1 node only;
      the measured phase response peaks only near multiples of N*f0 in the
      correlated case (cf. [P2] Fig. 11 -- their bench version used 10 uA
      sinusoidal currents into all five nodes of a 5-stage ring).

The per-stage ISF here is a *pedagogical toy* (triangular dual lobe with a
deliberate rise/fall asymmetry so that c0 != 0, echoing [P2] App. B
Eqs. (52)-(56) where A = f'_rise/f'_fall controls Gamma_dc).  It is NOT
extracted from a transistor-level circuit (lab_32 does that exercise).

Figure -> static/figures/correlated_supply_selection.png
Runtime: a few seconds.  Deterministic (no RNG).
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt

from isf_utils import compute_fourier_coefficients, wrap_phase
from plot_utils import savefig

# ----------------------------------------------------------------------------
# Site-canonical parameters
# ----------------------------------------------------------------------------
N_STAGES = 5              # ring stages
F0 = 5e9                  # oscillation frequency [Hz] (site canonical)
QMAX = 1e-12              # q_max [C] = 1 pC (site canonical)
I0 = 10e-6                # injected sinusoid amplitude [A] (same as [P2] Fig. 11: 10 uA)
DF = 10e6                 # offset from n*f0 [Hz]
N_HARM = 15               # harmonics shown in panel (b)
N_INJ_MAX = 12            # highest harmonic index n for injection sweep

W0 = 2 * np.pi * F0
DW = 2 * np.pi * DF


# ----------------------------------------------------------------------------
# Toy per-stage ring ISF: dual-lobe (positive lobe at rising edge, negative at
# falling edge), asymmetric heights so c0 != 0 ([P2] App.B: A != 1 -> Gamma_dc != 0).
# ----------------------------------------------------------------------------
H_RISE = 1.0              # peak of the rising-edge lobe (dimensionless)
H_FALL = 0.6              # |peak| of the falling-edge lobe (asymmetry: 0.6 != 1.0)
W_LOBE = 0.5              # half-width of each triangular lobe [rad]


def _tri(x, half_width):
    """Unit triangular bump centred at 0: 1 - |x|/w for |x|<w, else 0."""
    return np.clip(1.0 - np.abs(x) / half_width, 0.0, None)


def gamma_stage(theta):
    """Per-stage toy ring ISF, 2*pi periodic.

    +H_RISE triangular lobe centred on the rising edge (theta = 0)
    -H_FALL triangular lobe centred on the falling edge (theta = pi)
    """
    th = wrap_phase(theta)
    # distance to nearest image of 0 (rising edge) and of pi (falling edge)
    d_rise = np.minimum(th, 2 * np.pi - th)
    d_fall = np.abs(th - np.pi)
    return H_RISE * _tri(d_rise, W_LOBE) - H_FALL * _tri(d_fall, W_LOBE)


def gamma_summed(theta):
    """Sum of N phase-shifted per-stage ISFs ([P2] Eq. (37) bracket)."""
    acc = np.zeros_like(np.asarray(theta, dtype=float))
    for n in range(N_STAGES):
        acc += gamma_stage(theta + 2 * np.pi * n / N_STAGES)
    return acc


# ----------------------------------------------------------------------------
# Part 1 -- exact phasor cancellation (finite geometric sum)
# ----------------------------------------------------------------------------
def phasor_check():
    print("  [phasor] S_m = |sum_{n=0}^{N-1} exp(j*2*pi*m*n/N)|, N=5:")
    for m in range(0, 11):
        s = np.abs(np.sum(np.exp(1j * 2 * np.pi * m * np.arange(N_STAGES) / N_STAGES)))
        print(f"    m={m:2d}: S_m = {s:.3e}")


# ----------------------------------------------------------------------------
# Part 2 -- Fourier comb of the summed ISF
# ----------------------------------------------------------------------------
def fourier_comb():
    theta = np.linspace(0.0, 2 * np.pi, 2 ** 16 + 1, endpoint=True)
    g1 = gamma_stage(theta)
    gN = gamma_summed(theta)

    a0_1, _, _, c1, _ = compute_fourier_coefficients(theta, g1, N_HARM)
    a0_N, _, _, cN, _ = compute_fourier_coefficients(theta, gN, N_HARM)

    print(f"  [fourier] single-stage: c0={c1[0]:.6f}  c1={c1[1]:.6f}  "
          f"c5={c1[5]:.6f}  c10={c1[10]:.6f}")
    print(f"  [fourier] summed (N=5): c0={cN[0]:.6f}  c5={cN[5]:.6f}  "
          f"c10={cN[10]:.6f}  c15={cN[15]:.6f}")
    for n in (0, 5, 10, 15):
        print(f"    survive n={n:2d}: c_sum/c_single = {cN[n] / c1[n]:.6f}  (theory: N=5)")
    forbidden = [n for n in range(N_HARM + 1) if n % N_STAGES != 0]
    floor = max(cN[n] for n in forbidden)
    sel_db = 20 * np.log10(cN[5] / floor)
    print(f"    forbidden bins max |c_n| = {floor:.3e} (numeric floor)")
    print(f"    Fourier selection ratio c5/floor = {sel_db:.1f} dB")
    return theta, g1, gN, c1, cN


# ----------------------------------------------------------------------------
# Part 3 -- time-domain injection sweep (cf. [P2] Fig. 11)
# ----------------------------------------------------------------------------
def injection_sweep(c1, cN):
    fs = 256 * F0                      # sample rate [Hz]
    dt = 1.0 / fs                      # [s]
    n_samp = int(round(4 * fs / DF))   # 4 full periods of the slow response
    t = np.arange(n_samp) * dt         # [s]

    g_single_t = gamma_stage(W0 * t)
    g_summed_t = gamma_summed(W0 * t)
    proj = np.exp(-1j * 2 * np.pi * DF * t)   # projection bin at df

    def response(n_h, g_t):
        """Inject i(t)=I0*cos(2pi(n_h*f0+df)t) against ISF samples g_t.

        phi(t) = (1/qmax) * int i(tau) Gamma(w0 tau) dtau  ([P1] Eq.(11) machinery);
        return the amplitude [rad] of the phi component at df.
        """
        i_inj = I0 * np.cos(2 * np.pi * (n_h * F0 + DF) * t)
        phi = np.cumsum(i_inj * g_t) * dt / QMAX
        return 2.0 * np.abs(np.mean(phi * proj))

    ns = np.arange(N_INJ_MAX + 1)
    amp_corr = np.array([response(n, g_summed_t) for n in ns])
    amp_single = np.array([response(n, g_single_t) for n in ns])
    # theory: amp = I0 * c_n / (2 qmax dw)   ([P1] Eqs.(15)/(16) with the summed ISF)
    th_corr = I0 * cN[: N_INJ_MAX + 1] / (2 * QMAX * DW)
    th_single = I0 * c1[: N_INJ_MAX + 1] / (2 * QMAX * DW)

    print("  [time-domain] injection at n*f0 + 10 MHz, amplitude of phi at 10 MHz [rad]:")
    print("     n | corr (5 nodes) | single node | theory corr")
    for n in ns:
        print(f"    {n:2d} |  {amp_corr[n]:.4e}  | {amp_single[n]:.4e} | {th_corr[n]:.4e}")

    surv = [n for n in ns if n % N_STAGES == 0]
    forb = [n for n in ns if n % N_STAGES != 0]
    floor_td = max(amp_corr[n] for n in forb)
    sel_td_db = 20 * np.log10(amp_corr[5] / floor_td)
    print(f"    time-domain selection: corr amp(n=5)/max(forbidden n) = {sel_td_db:.1f} dB")
    print(f"    coherent gain at n=5: corr/single = {amp_corr[5] / amp_single[5]:.4f} (theory: N=5)")
    print(f"    theory match at n=5: measured/theory = {amp_corr[5] / th_corr[5]:.6f}")
    print(f"    theory match at n=0: measured/theory = {amp_corr[0] / th_corr[0]:.6f}")
    spur_dbc = 20 * np.log10(amp_corr[5] / 2.0)
    print(f"    PM sideband (spur) at n=5 injection: 20*log10(phi_p/2) = {spur_dbc:.1f} dBc")
    return ns, amp_corr, amp_single, th_corr, th_single


# ----------------------------------------------------------------------------
# Figure
# ----------------------------------------------------------------------------
def make_figure(theta, g1, gN, c1, cN, ns, amp_corr, amp_single, th_corr):
    fig, axes = plt.subplots(1, 3, figsize=(13.6, 4.3))

    # (a) per-stage ISFs + sum
    ax = axes[0]
    x = theta / (2 * np.pi)
    for n in range(N_STAGES):
        ax.plot(x, gamma_stage(theta + 2 * np.pi * n / N_STAGES),
                color="gray", lw=0.9, alpha=0.55,
                label="per-stage ISF ×5" if n == 0 else None)
    ax.plot(x, gN, color="tab:red", lw=2.2, label=r"summed $\Gamma_\Sigma$ ([P2] Eq.37)")
    ax.axhline(np.mean(gN), color="tab:blue", ls="--", lw=1.2,
               label=fr"mean $=N c_0/2={np.mean(gN):.4f}$")
    ax.set_xlabel(r"phase $\theta/2\pi$ [—]")
    ax.set_ylabel(r"$\Gamma(\theta)$ [dimensionless]")
    ax.set_title("(a) N=5 各級 ISF（灰）與總和（紅）")
    ax.legend(fontsize=8, loc="lower right")

    # (b) |c_n| comb
    ax = axes[1]
    nn = np.arange(N_HARM + 1)
    floor_clip = 1e-12
    ax.semilogy(nn - 0.12, np.maximum(c1, floor_clip), "o", color="gray",
                ms=5, label=r"single stage $|c_n|$")
    (ml, sl, bl) = ax.stem(nn + 0.12, np.maximum(cN, floor_clip),
                           basefmt=" ", linefmt="tab:red", markerfmt="D")
    plt.setp(ml, color="tab:red", ms=5)
    plt.setp(sl, lw=1.6)
    ml.set_label(r"summed $|c_n|$ ([P2] Eq.38)")
    ax.axhline(floor_clip, color="k", lw=0.8, ls=":")
    ax.text(0.3, floor_clip * 1.6, "numeric floor (clipped)", fontsize=7.5)
    ax.set_xticks(nn)
    ax.set_xlabel(r"harmonic index $n$ [—]")
    ax.set_ylabel(r"$|c_n|$ [dimensionless]")
    ax.set_title("(b) 只有 $n\\equiv0\\ (\\mathrm{mod}\\ 5)$ 存活")
    ax.legend(fontsize=8, loc="upper right")

    # (c) injection response
    ax = axes[2]
    ax.semilogy(ns, amp_corr, "o-", color="tab:red", ms=6,
                label="correlated: all 5 nodes")
    ax.semilogy(ns, amp_single, "s--", color="gray", ms=5,
                label="single node (no selection)")
    ax.semilogy(ns, np.maximum(th_corr, 1e-30), "x", color="k", ms=7,
                label=r"theory $I_0 c_{\Sigma,n}/(2q_{max}\Delta\omega)$")
    for n in (0, 5, 10):
        ax.axvline(n, color="tab:red", lw=0.7, alpha=0.25)
    ax.set_ylim(1e-9, 1.0)
    ax.set_xticks(ns)
    ax.set_xlabel(r"injection at $n f_0+\Delta f$,  $\Delta f=10$ MHz  ($n$) [—]")
    ax.set_ylabel(r"phase response at $\Delta f$ [rad]")
    ax.set_title("(c) 共同注入只在 $n=0,5,10$ 有響應")
    ax.legend(fontsize=8, loc="upper right")

    fig.suptitle(
        r"[P2] Sec.VI Eqs.(37)-(38)：相關供電/基板雜訊的 $N\cdot f_0$ 選擇律"
        fr"（toy ring, $N$={N_STAGES}, $f_0$=5 GHz, $q_{{max}}$=1 pC, $I_0$=10 µA）",
        fontsize=11)
    savefig(fig, "correlated_supply_selection.png")


def main():
    print("[lab_34] correlated supply/substrate noise: N*f0 selection rule ...")
    print(f"  params: N={N_STAGES}, f0={F0:.3e} Hz, qmax={QMAX:.1e} C, "
          f"I0={I0:.1e} A, df={DF:.1e} Hz")
    phasor_check()
    theta, g1, gN, c1, cN = fourier_comb()
    ns, amp_corr, amp_single, th_corr, th_single = injection_sweep(c1, cN)
    make_figure(theta, g1, gN, c1, cN, ns, amp_corr, amp_single, th_corr)
    print("[lab_34] done.")


if __name__ == "__main__":
    main()
