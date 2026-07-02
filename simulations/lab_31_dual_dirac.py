"""
lab_31_dual_dirac.py

Goal
----
The industry-standard *dual-Dirac* jitter model, end to end:

  1. Synthesize total jitter TJ = RJ (Gaussian, sigma = 1 ps, unbounded — the
     part that comes from oscillator phase noise) + DJ (bounded: here a
     sinusoidal / power-supply-spur type deterministic jitter, amplitude
     A = 2 ps, i.e. DJ_pp = 4 ps).
  2. Histogram the composite PDF and compare with the fitted dual-Dirac PDF
     (two Gaussians of the SAME sigma separated by DJ_dd).
  3. Extract (DJ_dd, sigma) the way instruments do: straight-line fit of the
     deep tail on the "Q-scale"  q = Qinv(2*T(x))  vs x, where
     T(x) = P(jitter > x) is the tail (1 - CDF) of the composite jitter.
     Dual-Dirac tail:  T_dd(x) ~= (1/2) Q((x - DJ_dd/2)/sigma)  for x deep in
     the right tail  =>  Qinv(2*T) is a straight line with slope 1/sigma and
     x-intercept DJ_dd/2.
  4. Bathtub  BER(t) = 1/2 [T(UI/2 - t) + T(UI/2 + t)]  (transition density
     rho_T = 1/2, same convention as lab_12 / serdes_utils) for the exact
     composite vs the dual-Dirac extrapolation.
  5. TJ@BER = DJ_dd + 2*Qinv(BER)*sigma  with Qinv(1e-12) = 7.034 ("7.03",
     the site's canonical value) — plus an explicit factor-of-2 convention
     audit (per-Gaussian tail vs per-side tail vs rho_T = 1/2 bathtub).

Key honesty point demonstrated numerically
------------------------------------------
DJ_dd (a *model parameter*) < DJ_pp (the actual bounded peak-to-peak, here
4 ps).  The Q-scale fit anchors the straight line to the TRUE deep tail, so
the extrapolated TJ(BER) is accurate; forcing the Diracs out to +-DJ_pp/2
would overstate the tail and waste margin.

Figure
------
  static/figures/dual_dirac_bathtub.png

External-source note: the dual-Dirac methodology is industry standard, NOT
from the site's five PDFs.  See Fibre Channel MJSQ (INCITS T11.2, Technical
Report Rev 14, 2005) and modern SerDes specs (PCIe/OIF-CEI).
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfcinv

from serdes_utils import Q
from plot_utils import savefig

RNG = np.random.default_rng(31)

# ---------------------------------------------------------------------------
# Model pieces (reusable; the doc page imports these)
# ---------------------------------------------------------------------------


def q_inv(p):
    """Inverse Gaussian tail: x such that Q(x) = p.   Q(x)=0.5*erfc(x/sqrt2)."""
    return np.sqrt(2.0) * erfcinv(2.0 * np.asarray(p, dtype=float))


def composite_tail(x, a_dj, sigma_rj, n_theta=4096):
    """
    Exact tail T(x) = P(jitter > x) of  x_tot = a_dj*sin(theta) + N(0, sigma_rj^2)
    with theta uniform in [0, 2pi)  (sinusoidal DJ convolved with Gaussian RJ).

    T(x) = <Q((x - a_dj*sin(theta))/sigma_rj)>_theta ; the uniform midpoint
    average over one period converges spectrally (periodic analytic integrand),
    so this reaches 1e-15 tail depths with no Monte-Carlo noise.

    x, a_dj, sigma_rj in seconds. Returns array shaped like x.
    """
    theta = (np.arange(n_theta) + 0.5) * (2.0 * np.pi / n_theta)
    u = a_dj * np.sin(theta)
    xx = np.atleast_1d(np.asarray(x, dtype=float))
    T = Q((xx[:, None] - u[None, :]) / sigma_rj).mean(axis=1)
    return T if np.ndim(x) else float(T[0])


def composite_pdf(x, a_dj, sigma_rj, n_theta=4096):
    """Exact PDF of the same composite jitter [1/s]."""
    theta = (np.arange(n_theta) + 0.5) * (2.0 * np.pi / n_theta)
    u = a_dj * np.sin(theta)
    xx = np.atleast_1d(np.asarray(x, dtype=float))
    z = (xx[:, None] - u[None, :]) / sigma_rj
    p = (np.exp(-0.5 * z**2) / (sigma_rj * np.sqrt(2.0 * np.pi))).mean(axis=1)
    return p if np.ndim(x) else float(p[0])


def dual_dirac_tail(x, dj_dd, sigma):
    """Dual-Dirac model tail: T_dd(x) = 0.5*[Q((x-mu)/s) + Q((x+mu)/s)], mu=DJ_dd/2."""
    mu = dj_dd / 2.0
    return 0.5 * (Q((np.asarray(x, dtype=float) - mu) / sigma)
                  + (Q((np.asarray(x, dtype=float) + mu) / sigma)))


def fit_dual_dirac(a_dj, sigma_rj, t_deep=1e-10, t_shallow=1e-6, n_theta=4096):
    """
    Extract (DJ_dd, sigma) from the composite tail by a Q-scale straight-line
    fit, exactly like a TIE-based jitter-decomposition instrument:

        q(x) = Qinv(2*T(x))  ~  (x - DJ_dd/2)/sigma   in the Gaussian region,

    fitted where T(x) is between t_shallow and t_deep (default 1e-6 .. 1e-10).
    The factor 2 inside Qinv accounts for the 1/2 weight of each Dirac.
    Symmetric DJ assumed -> DJ_dd = 2*mu_fit.

    Returns (dj_dd [s], sigma_fit [s], info dict).
    """
    x = np.linspace(0.0, a_dj + 12.0 * sigma_rj, 6001)
    T = composite_tail(x, a_dj, sigma_rj, n_theta=n_theta)
    m = (T <= t_shallow) & (T >= t_deep)
    slope, intercept = np.polyfit(x[m], q_inv(2.0 * T[m]), 1)
    sigma_fit = 1.0 / slope
    mu_fit = -intercept / slope
    info = {"x_fit": x[m], "q_fit": q_inv(2.0 * T[m]),
            "slope": slope, "intercept": intercept, "mu_fit": mu_fit}
    return 2.0 * mu_fit, sigma_fit, info


def bathtub_from_tail(t_offsets, ui, tail_func):
    """BER(t) = 0.5*[T(UI/2 - t) + T(UI/2 + t)]  (transition density 1/2)."""
    t = np.asarray(t_offsets, dtype=float)
    ber = 0.5 * (tail_func(ui / 2.0 - t) + tail_func(ui / 2.0 + t))
    return np.maximum(ber, 1e-300)


def _crossing(t, ber, level):
    """Largest |t| (right side) where BER(t) <= level, by log interpolation."""
    lb = np.log10(ber)
    # right half: BER increases with t; find t where lb crosses log10(level)
    m = t >= 0
    return float(np.interp(np.log10(level), lb[m], t[m]))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("[lab_31] dual-Dirac model: RJ+DJ synthesis, tail fit, bathtub ...")
    ui = 100e-12          # 10 Gb/s -> UI = 100 ps  (same as lab_12)
    sigma_rj = 1e-12      # RJ: 1 ps rms (Gaussian, unbounded)
    a_dj = 2e-12          # DJ: sinusoidal amplitude 2 ps -> DJ_pp = 4 ps (bounded)
    ber_target = 1e-12

    # --- sanity: the site's canonical Q table -------------------------------
    print("Q table check: Qinv(1e-9) =", round(float(q_inv(1e-9)), 3),
          "  # -> 5.998")
    print("Q table check: Qinv(1e-12) =", round(float(q_inv(1e-12)), 3),
          "  # -> 7.034")
    print("Q table check: Qinv(1e-15) =", round(float(q_inv(1e-15)), 3),
          "  # -> 7.941")

    # --- 1) Monte-Carlo synthesis (for the histogram panel) -----------------
    n_mc = 2_000_000
    x_mc = (a_dj * np.sin(2.0 * np.pi * RNG.random(n_mc))
            + sigma_rj * RNG.standard_normal(n_mc))
    print("MC DJ_pp (true bounded part) =", round(2 * a_dj * 1e12, 1),
          "ps   # -> 4.0")

    # --- 2) dual-Dirac extraction (deterministic, tail fit on exact T) ------
    dj_dd, sigma_fit, info = fit_dual_dirac(a_dj, sigma_rj)
    print("extracted DJ_dd =", round(dj_dd * 1e12, 2),
          "ps   # -> 3.16 (< DJ_pp = 4.0: model under-reports DJ on purpose)")
    print("extracted sigma =", round(sigma_fit * 1e12, 3),
          "ps   # -> 1.03 (true RJ rms 1.0; residual DJ curvature leaks in)")

    # --- 3) TJ@BER: the standard formula ------------------------------------
    q12 = float(q_inv(ber_target))
    tj_formula = dj_dd + 2.0 * q12 * sigma_fit
    print("TJ@1e-12 (dual-Dirac formula DJ_dd + 2*7.034*sigma) =",
          round(tj_formula * 1e12, 2), "ps   # -> 17.65")

    # --- 4) convention audit: three ways to read the 'true' TJ --------------
    tail = lambda xx: composite_tail(xx, a_dj, sigma_rj)
    # (a) per-side tail convention: T(x*) = BER on the exact composite
    xgrid = np.linspace(0.0, a_dj + 12.0 * sigma_rj, 6001)
    Tg = np.maximum(tail(xgrid), 1e-300)
    x_star = float(np.interp(np.log10(ber_target), np.log10(Tg)[::-1],
                             xgrid[::-1]))
    tj_tailconv = 2.0 * x_star
    print("TJ@1e-12 (exact composite, per-side tail T=BER) =",
          round(tj_tailconv * 1e12, 2), "ps   # -> 17.43")
    # (b) bathtub convention with transition density 1/2 (site's lab_12 form)
    toff = np.linspace(0.0, ui / 2.0 * 0.999, 4001)
    ber_comp = bathtub_from_tail(toff, ui, tail)
    t_edge = _crossing(toff, ber_comp, ber_target)
    tj_bathtub = ui - 2.0 * t_edge
    print("TJ@1e-12 (exact composite, bathtub rho_T=1/2) =",
          round(tj_bathtub * 1e12, 2), "ps   # -> 17.23")
    print("convention spread Qinv(1e-12)-Qinv(4e-12) =",
          round(float(q_inv(1e-12) - q_inv(4e-12)), 3),
          "sigma   # -> 0.196 (the whole formula-vs-bathtub gap)")

    # eye openings at BER=1e-12 (bathtub view)
    eye_open_comp = 2.0 * t_edge
    ber_dd = bathtub_from_tail(toff, ui, lambda xx: dual_dirac_tail(xx, dj_dd, sigma_fit))
    t_edge_dd = _crossing(toff, ber_dd, ber_target)
    print("eye opening @1e-12: composite =", round(eye_open_comp * 1e12, 2),
          "ps   # -> 82.77")
    print("eye opening @1e-12: dual-Dirac extrapolation =",
          round(2 * t_edge_dd * 1e12, 2),
          "ps   # -> 82.76 (matches composite: that is the model's whole job)")

    # ------------------------------------------------------------------ plot
    fig, axes = plt.subplots(1, 3, figsize=(15.0, 4.6))

    # (a) histogram + exact PDF + dual-Dirac PDF
    ax = axes[0]
    xs = np.linspace(-(a_dj + 5 * sigma_rj), a_dj + 5 * sigma_rj, 801)
    ax.hist(x_mc * 1e12, bins=161, density=True, alpha=0.35, color="tab:blue",
            label="MC 直方圖 (RJ 1 ps ⊛ 弦波 DJ 2 ps)")
    ax.plot(xs * 1e12, composite_pdf(xs, a_dj, sigma_rj) / 1e12, color="tab:blue",
            lw=1.8, label="精確複合 PDF")
    mu = dj_dd / 2.0
    pdf_dd = 0.5 * (np.exp(-0.5 * ((xs - mu) / sigma_fit) ** 2)
                    + np.exp(-0.5 * ((xs + mu) / sigma_fit) ** 2)) \
        / (sigma_fit * np.sqrt(2 * np.pi))
    ax.plot(xs * 1e12, pdf_dd / 1e12, color="tab:red", ls="--", lw=1.8,
            label=fr"dual-Dirac 模型 (DJ$_{{\delta\delta}}$={dj_dd*1e12:.2f} ps)")
    for s, c, lb in [(a_dj, "gray", r"真 DJ 極值 $\pm$2 ps"),
                     (mu, "tab:red", r"Dirac 位置 $\pm\mu$")]:
        ax.axvline(+s * 1e12, color=c, ls=":", lw=1.2, label=lb)
        ax.axvline(-s * 1e12, color=c, ls=":", lw=1.2)
    ax.set_xlabel("jitter [ps]")
    ax.set_ylabel("probability density [1/ps]")
    ax.set_title("(a) TJ 的 PDF：dual-Dirac 的 Dirac 在真極值內側")
    ax.legend(fontsize=7.5, loc="upper right")

    # (b) Q-scale tail fit
    ax = axes[1]
    xq = np.linspace(0.0, a_dj + 9.0 * sigma_rj, 1200)
    Tq = np.maximum(composite_tail(xq, a_dj, sigma_rj), 1e-300)
    ok = Tq < 0.49
    ax.plot(xq[ok] * 1e12, q_inv(2 * Tq[ok]), color="tab:blue", lw=1.8,
            label=r"精確尾巴 $Q^{-1}(2T(x))$")
    ax.plot(xq * 1e12, (xq - mu) / sigma_fit, color="tab:red", ls="--", lw=1.6,
            label=fr"擬合直線：$\sigma$={sigma_fit*1e12:.2f} ps, $\mu$={mu*1e12:.2f} ps")
    ax.plot(xq * 1e12, (xq - a_dj) / sigma_rj, color="gray", ls=":", lw=1.4,
            label=r"若 Dirac 硬放在真極值 $A$=2 ps → 尾巴被高估（悲觀）")
    xf = info["x_fit"]
    ax.axvspan(xf.min() * 1e12, xf.max() * 1e12, color="tab:orange", alpha=0.15,
               label=r"擬合窗 $T\in[10^{-10},10^{-6}]$")
    ax.set_xlabel("jitter x [ps]")
    ax.set_ylabel(r"Q-scale $Q^{-1}(2T)$ [$\sigma$]")
    ax.set_ylim(0, 9.5)
    ax.set_xlim(0, (a_dj + 9 * sigma_rj) * 1e12)
    ax.set_title("(b) Q-scale 尾巴擬合 → 取出 $\\mu$ 與 $\\sigma$")
    ax.legend(fontsize=7.5, loc="upper left")

    # (c) bathtub: composite vs dual-Dirac extrapolation
    ax = axes[2]
    tt = np.linspace(-ui / 2 * 0.999, ui / 2 * 0.999, 3001)
    ber_c = bathtub_from_tail(tt, ui, tail)
    ber_d = bathtub_from_tail(tt, ui, lambda xx: dual_dirac_tail(xx, dj_dd, sigma_fit))
    ber_rj = bathtub_from_tail(tt, ui, lambda xx: Q(np.asarray(xx) / sigma_rj))
    ax.semilogy(tt / ui, ber_c, color="tab:blue", lw=2.0, label="精確複合 (RJ⊛DJ)")
    ax.semilogy(tt / ui, ber_d, color="tab:red", ls="--", lw=1.8,
                label="dual-Dirac 外插")
    ax.semilogy(tt / ui, ber_rj, color="tab:green", ls=":", lw=1.6,
                label=r"RJ-only ($\sigma_t$=1 ps，無 DJ)")
    ax.axhline(ber_target, color="gray", ls="--", lw=1.0, label="BER = $10^{-12}$")
    ax.plot([-t_edge / ui, t_edge / ui], [ber_target] * 2, "o", color="tab:blue",
            ms=5)
    ax.annotate(fr"opening={eye_open_comp*1e12:.1f} ps",
                xy=(0, ber_target), xytext=(-0.28, 3e-10), fontsize=8,
                color="tab:blue")
    ax.set_xlabel("sampling offset [UI]")
    ax.set_ylabel("BER")
    ax.set_ylim(1e-16, 1)
    ax.set_title("(c) BER bathtub：DJ 把兩壁往內推，RJ 決定壁的斜率")
    ax.legend(fontsize=7.5, loc="lower center")

    savefig(fig, "dual_dirac_bathtub.png")


if __name__ == "__main__":
    main()
