"""
fig_htm_bandfold.py

Goal
----
Visualise the *harmonic transfer matrix (HTM)* picture of the ISF for the
appendix page docs/99_appendix/ltv_htm.md.

A periodic-LTV (LPTV) oscillator does not keep an input frequency band on the
diagonal the way an LTI system does: a single input noise band at frequency f
is *folded* (frequency-translated) to a whole comb of output bands f + k*f0,
k = ..., -1, 0, +1, ... . The complex gain of the k-th fold is exactly the
k-th complex Fourier coefficient of the ISF:

      H_k^(Gamma) = c_tilde_k ,   with
      c_tilde_0    = c0/2                      (DC band, f -> f)
      c_tilde_{+-k} = (1/2) c_k exp(+- j theta_k)   (k >= 1)

so the |gain| of each folding arrow is
      DC:   |c_tilde_0| = c0/2
      +-1:  |c_tilde_1| = c1/2
      +-2:  |c_tilde_2| = c2/2  ...

This script draws:
  (left)  a frequency-axis band-folding diagram: one input band at f, with
          arrows folding it to f + k*f0 (k = -2..2). Each arrow's height and
          label is |c_tilde_k|, computed from the ISF Fourier coefficients via
          isf_utils.compute_fourier_coefficients.
  (right) the Toeplitz HTM heatmap [H]_{m,k} = H_{m-k} = c_tilde_{m-k}.

The c_k are computed from the SAME pedagogical asymmetric ISF used in lab_05
(richer than a pure -sin so several harmonics are non-trivial), keeping the
numbers consistent across the site.

Figure produced
---------------
  static/figures/htm_band_folding.png

References
----------
ISF Fourier series: Hajimiri-Lee (1998) [P1] Eq.(12), p.183.
Per-harmonic phase response: [P1] Eq.(13), p.183.
HTM / Zadeh time-varying transfer function: external LTV-systems framework
(Zadeh 1950), NOT in the site's 5 PDFs; see docs/99_appendix/ltv_htm.md.

This is a pedagogical illustration, not a transistor-level extraction.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

from isf_utils import compute_fourier_coefficients, gamma_rms
from plot_utils import savefig


def make_isf(theta):
    """
    Same pedagogical asymmetric ISF as lab_05_fourier_isf.make_isf:
        Gamma(theta) = -sin(theta) + 0.35 sin(2 theta) + 0.18 cos(3 theta) + 0.25
    The +0.25 gives a non-zero c0 (DC band), so the H_0 fold is visible.
    """
    return (-np.sin(theta) + 0.35 * np.sin(2 * theta)
            + 0.18 * np.cos(3 * theta) + 0.25)


def htm_gains(n_harmonics=4):
    """
    Return the complex HTM gains c_tilde_k for k = -n_harmonics .. +n_harmonics.

        c_tilde_0    = c0/2
        c_tilde_{+-k} = (1/2) c_k exp(+- j theta_k)

    so |c_tilde_0| = c0/2 and |c_tilde_{+-k}| = c_k/2.

    Returns
    -------
    ks       : int array, -n_harmonics .. +n_harmonics
    ctilde   : complex array, c_tilde_k aligned with ks
    cmag     : |c_tilde_k| (the arrow heights)
    (c, ph, grms) : the underlying real magnitudes c_n, phases theta_n, Gamma_rms
    """
    theta = np.linspace(0, 2 * np.pi, 4000, endpoint=True)
    g = make_isf(theta)
    a0, a, b, c, ph = compute_fourier_coefficients(theta, g, n_harmonics)
    grms = gamma_rms(theta, g)

    ks = np.arange(-n_harmonics, n_harmonics + 1)
    ctilde = np.zeros(ks.size, dtype=complex)
    for idx, k in enumerate(ks):
        if k == 0:
            ctilde[idx] = c[0] / 2.0            # c_tilde_0 = c0/2
        else:
            n = abs(k)
            sign = 1.0 if k > 0 else -1.0
            ctilde[idx] = 0.5 * c[n] * np.exp(sign * 1j * ph[n])
    cmag = np.abs(ctilde)
    return ks, ctilde, cmag, (c, ph, grms)


def fig_htm_band_folding():
    n_h = 4               # show k = -4..+4 in the heatmap
    n_show = 2            # draw folding arrows for k = -2..+2 (per task)
    ks, ctilde, cmag, (c, ph, grms) = htm_gains(n_harmonics=n_h)

    fig, (axL, axR) = plt.subplots(
        1, 2, figsize=(12.6, 5.2),
        gridspec_kw={"width_ratios": [1.55, 1.0]},
    )

    # ---------------------------------------------------------------
    # LEFT: band-folding diagram on a frequency axis.
    # One input noise band sits at f (a fraction f_frac of f0 above an
    # arbitrary reference). The LPTV system folds it to f + k*f0.
    # ---------------------------------------------------------------
    f_frac = 0.32         # input band offset from a harmonic, as a fraction of f0
    # output band centres in units of f0:  k + f_frac, for k = -n_show..n_show
    centres = np.array([k + f_frac for k in range(-n_show, n_show + 1)])
    # arrow heights = |c_tilde_k| for k = -n_show..n_show
    show_idx = [np.where(ks == k)[0][0] for k in range(-n_show, n_show + 1)]
    heights = cmag[show_idx]

    axL.axhline(0, color="0.25", lw=1.4, zorder=2)  # the frequency axis
    hmax = heights.max()

    # input band marker (a tall slim bar at f_frac)
    axL.bar(f_frac, hmax * 1.18, width=0.06, bottom=0.0,
            color="tab:purple", alpha=0.85, zorder=3,
            label=r"input noise band @ $f$")
    axL.text(f_frac, hmax * 1.18 + 0.02 * hmax, r"$f$", ha="center",
             va="bottom", color="tab:purple", fontsize=12, fontweight="bold")

    # tick marks for the harmonics n*f0
    for k in range(-n_show, n_show + 1):
        axL.plot([k, k], [-0.03 * hmax, 0.03 * hmax], color="0.25", lw=1.2,
                 zorder=2)
        lbl = "DC" if k == 0 else (r"$%d\,f_0$" % k if k != 1 else r"$f_0$")
        if k == -1:
            lbl = r"$-f_0$"
        axL.text(k, -0.10 * hmax, lbl, ha="center", va="top",
                 color="0.25", fontsize=9)

    # output bands + folding arrows
    cmap = plt.get_cmap("viridis")
    for j, k in enumerate(range(-n_show, n_show + 1)):
        cx = centres[j]
        h = heights[j]
        col = cmap(0.15 + 0.7 * (j / (2 * n_show)))
        # output band bar
        axL.bar(cx, h, width=0.055, color=col, alpha=0.95, zorder=3)
        # folding arrow from input band top down to this output band top
        arr = FancyArrowPatch(
            (f_frac, hmax * 1.06),
            (cx, h + 0.02 * hmax),
            connectionstyle=f"arc3,rad={-0.32 if cx < f_frac else 0.32}",
            arrowstyle="-|>", mutation_scale=14, lw=1.6,
            color=col, alpha=0.9, zorder=4,
        )
        axL.add_patch(arr)
        # gain label on each output band
        gain_txt = (r"$|\tilde c_{%+d}|=%.3f$" % (k, h)) if k != 0 \
            else (r"$|\tilde c_0|=c_0/2=%.3f$" % h)
        axL.text(cx, h + 0.05 * hmax, gain_txt, ha="center", va="bottom",
                 fontsize=8.0, color=col, rotation=0)

    axL.set_xlim(-n_show - 0.55, n_show + 0.75)
    axL.set_ylim(-0.22 * hmax, hmax * 1.42)
    axL.set_xlabel(r"頻率 frequency （單位：$f_0$；DC$=0$）")
    axL.set_ylabel(r"折疊增益 $|\tilde c_k|$ (HTM gain, 無因次)")
    axL.set_title("HTM 頻帶折疊：單一輸入 band @ $f$ 被搬到 $f+k f_0$\n"
                  r"每箭頭高度/標籤 $=|\tilde c_k|$（DC$=c_0/2$，$\pm1=c_1/2$ …）")
    axL.legend(loc="upper right", fontsize=8.5)
    axL.grid(axis="y", alpha=0.25)
    axL.set_axisbelow(True)

    # ---------------------------------------------------------------
    # RIGHT: Toeplitz HTM heatmap  [H]_{m,k} = H_{m-k} = c_tilde_{m-k}.
    # Rows = output band m, cols = input band k; constant along diagonals.
    # ---------------------------------------------------------------
    mk = np.arange(-n_h, n_h + 1)
    M = mk.size
    H = np.zeros((M, M))
    ctilde_full = ctilde  # aligned with ks = -n_h..n_h
    for im, m in enumerate(mk):
        for ik, k in enumerate(mk):
            d = m - k
            if -n_h <= d <= n_h:
                H[im, ik] = np.abs(ctilde_full[np.where(ks == d)[0][0]])
            else:
                H[im, ik] = np.nan  # outside the modelled band range

    im = axR.imshow(H, origin="lower", cmap="viridis",
                    extent=[mk[0] - 0.5, mk[-1] + 0.5,
                            mk[0] - 0.5, mk[-1] + 0.5])
    axR.set_xticks(mk)
    axR.set_yticks(mk)
    axR.set_xlabel(r"輸入 band 索引 $k$")
    axR.set_ylabel(r"輸出 band 索引 $m$")
    axR.set_title(r"Toeplitz HTM：$[\mathbf{H}]_{m,k}=|H_{m-k}|=|\tilde c_{m-k}|$"
                  "\n（沿對角線常數＝只看相差幾個 $f_0$）")
    cbar = fig.colorbar(im, ax=axR, fraction=0.046, pad=0.04)
    cbar.set_label(r"$|\tilde c_{m-k}|$ (無因次)")
    # annotate each cell with its value (only finite ones)
    for iy, m in enumerate(mk):
        for ix, k in enumerate(mk):
            if np.isfinite(H[iy, ix]):
                v = H[iy, ix]
                axR.text(k, m, f"{v:.2f}", ha="center", va="center",
                         fontsize=6.5,
                         color=("white" if v < 0.6 * np.nanmax(H) else "black"))

    fig.suptitle(
        r"ISF 的傅立葉係數 $=$ 相位輸出的 HTM 列：折疊增益 $|\tilde c_k|$ "
        rf"（$c_0/2={c[0]/2:.3f}$，$\Gamma_{{rms}}={grms:.3f}$）",
        fontsize=12.5, y=1.02,
    )

    savefig(fig, "htm_band_folding.png")


def main():
    print("[fig_htm_bandfold] HTM band-folding diagram + Toeplitz heatmap ...")
    ks, ctilde, cmag, (c, ph, grms) = htm_gains(n_harmonics=4)
    # quick console sanity print of the gains and Parseval check
    print("  |c_tilde_k| (k=-2..2):",
          ", ".join(f"{int(k):+d}:{abs(v):.4f}"
                    for k, v in zip(ks, ctilde) if -2 <= k <= 2))
    # Parseval / vector-energy check:  sum_k |c_tilde_k|^2 ?= Gamma_rms^2
    energy = np.sum(np.abs(ctilde) ** 2)
    print(f"  sum_k |c_tilde_k|^2 = {energy:.5f}  vs  "
          f"Gamma_rms^2 = {grms**2:.5f}  (HTM-row energy = Parseval)")
    fig_htm_band_folding()


if __name__ == "__main__":
    main()
