"""
fig_device_noise_bands.py

Goal
----
Make ONE teaching figure for the "ISF harmonics are the receive channels"
discussion in docs/06_design_insights/device_noise_mapping.md.

The figure has two stacked panels sharing a frequency axis:

  TOP panel  — the device current-noise PSD S_i(f) vs frequency: a 1/f flicker
               bump near DC plus a white plateau (thermal/shot). Three shaded
               vertical bands mark the spectral neighbourhoods that the ISF
               harmonics actually "listen to": DC (flicker), f0, and 2*f0.

  BOTTOM panel — a stem/bar plot of the ISF Fourier-coefficient magnitudes
               |c_n| at n = 0,1,2,... aligned underneath those same bands, with
               arrows showing each band folding down to the carrier, weighted by
               its c_n:  c0 up-converts near-DC flicker into close-in 1/f^3,
               while c1, c2 fold the white noise near f0, 2*f0 down to the
               carrier (the 1/f^2 region).

This is the visual statement of Hajimiri-Lee (1998) Eqs. (12)-(13): the ISF's
Fourier coefficients are the channel gains of a frequency-converting (LTV)
"receiver" that maps device noise around n*f0 onto the output phase.

The |c_n| values come from compute_fourier_coefficients() applied to a toy
asymmetric ISF (NOT a transistor-level extraction) so that c0 != 0 and a few
harmonics are visible.

Figure produced
---------------
  static/figures/device_noise_isf_bands.png

Corresponds to: Hajimiri-Lee (1998) Eqs. (12),(13),(19),(23).
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

from isf_utils import compute_fourier_coefficients
from plot_utils import savefig


def toy_isf(theta):
    """
    A toy *asymmetric* ISF so that c0 != 0 (flicker up-conversion channel is
    open) and c1, c2 are both visible. NOT extracted from a real transistor
    oscillator — purely pedagogical, matching the asymmetric ISFs used in the
    rest of the site (isf_utils.gamma_asymmetric family).

        Gamma(theta) = -sin(theta) + 0.35*sin(2*theta) + 0.25
                       ^ c1 (LC-like)  ^ c2 (2nd harmonic)  ^ sets c0 = 0.5
    """
    return -np.sin(theta) + 0.35 * np.sin(2 * theta) + 0.25


def device_noise_psd(f, f0, white_floor=1.0, f_1f=None):
    """
    Toy device current-noise PSD model S_i(f) [arb. A^2/Hz], normalized so the
    white plateau = white_floor:

        S_i(f) = white_floor * ( 1 + f_1f / f )

    i.e. a flat thermal/shot plateau plus a 1/f flicker bump that crosses the
    plateau at the device 1/f corner f_1f. Matches the two-segment split in
    docs (white + flicker), Hajimiri-Lee Eqs.(19),(22).
    """
    if f_1f is None:
        f_1f = 0.05 * f0  # device 1/f corner well below f0 (typical)
    return white_floor * (1.0 + f_1f / f)


def main():
    print("[fig_device_noise_bands] device noise -> ISF harmonic channels ...")

    f0 = 1.0           # normalize the carrier to f0 = 1 (frequency axis in f/f0)
    n_harm = 5         # show c0..c5
    band_halfwidth = 0.13 * f0   # linear half-width of the f0 / 2f0 receive bands
    # The DC/flicker channel is a *low-frequency* neighbourhood; on a log axis we
    # draw it as a narrow band sitting at the low edge (the close-in offset
    # region Delta_omega << omega0 where flicker lives).
    f_dc = 2.2e-2 * f0                     # representative close-in offset for c0
    dc_lo, dc_hi = f_dc / 1.7, f_dc * 1.7  # narrow log-width DC band

    # ---- ISF Fourier coefficients |c_n| (the channel gains) ----------------
    theta = np.linspace(0, 2 * np.pi, 4096, endpoint=True)
    gamma = toy_isf(theta)
    a0, a, b, c, ph = compute_fourier_coefficients(theta, gamma, n_harm)
    # c[0] = |c0| (DC coeff); c[n] = sqrt(a_n^2 + b_n^2).

    # ---- device current-noise PSD ------------------------------------------
    f = np.logspace(-2.3, np.log10(3.2 * f0), 2000)  # 0.005*f0 .. ~3.2*f0
    Si = device_noise_psd(f, f0)

    # The three receive-band center frequencies the figure highlights: DC, f0,
    # 2 f0.  band_span[i] = (lo, hi) on the frequency axis for shading.
    band_centers = [0.0, 1.0 * f0, 2.0 * f0]
    band_spans = [
        (dc_lo, dc_hi),
        (1.0 * f0 - band_halfwidth, 1.0 * f0 + band_halfwidth),
        (2.0 * f0 - band_halfwidth, 2.0 * f0 + band_halfwidth),
    ]
    band_labels = [r"DC 附近 (flicker)", r"$f_0$ 附近 (white)", r"$2f_0$ 附近 (white)"]
    band_colors = ["tab:red", "tab:blue", "tab:purple"]
    # which c_n weights each band:  DC->c0, f0->c1, 2f0->c2
    band_coeff_idx = [0, 1, 2]

    # ------------------------------------------------------------------ figure
    fig, (ax_top, ax_bot) = plt.subplots(
        2, 1, figsize=(8.6, 7.0), sharex=True,
        gridspec_kw={"height_ratios": [1.55, 1.0], "hspace": 0.12})
    fig.patch.set_facecolor("white")  # readable on a white card in dark mode
    # We hand-tune hspace + arrow patches, so disable the global autolayout
    # (plot_utils sets figure.autolayout=True) to avoid a tight_layout warning.
    fig.set_layout_engine("none")

    # ============ TOP: device current-noise PSD vs frequency ================
    ax_top.loglog(f, Si, color="black", lw=2.0, zorder=5,
                  label=r"device $S_i(f)$ = white + flicker")
    # decompose for teaching: dashed white plateau + dotted 1/f bump
    ax_top.loglog(f, np.ones_like(f), color="tab:green", ls="--", lw=1.1,
                  zorder=3, label=r"white plateau (thermal/shot)")
    ax_top.loglog(f, 0.05 * f0 / f, color="tab:orange", ls=":", lw=1.3,
                  zorder=3, label=r"flicker $1/f$ bump")

    # shaded receive bands
    for (lo, hi), lab, col in zip(band_spans, band_labels, band_colors):
        ax_top.axvspan(lo, hi, color=col, alpha=0.18, zorder=1)
        # label near top of the panel (geo-mean for nice placement on log axis)
        x_lab = np.sqrt(lo * hi)
        ax_top.text(x_lab, Si.max() * 0.62, lab, rotation=90,
                    ha="center", va="top", fontsize=8.5, color=col, zorder=6)

    ax_top.set_ylabel(r"電流雜訊 PSD  $S_i(f)$ [A$^2$/Hz, arb.]")
    ax_top.set_title("Device noise 的頻譜，與 ISF 諧波接收的三個頻段 (DC, $f_0$, $2f_0$)")
    ax_top.set_ylim(0.4, Si.max() * 1.5)
    ax_top.grid(True, which="both", alpha=0.3)
    ax_top.legend(loc="upper right", fontsize=8.5, framealpha=0.95)

    # ============ BOTTOM: |c_n| stems aligned under the bands ===============
    # Map harmonic n to a frequency position n*f0 on the shared log axis. n = 0
    # (the c0 channel) sits at the DC band; n = 1 at f0; n = 2 at 2 f0; etc.
    n_idx = np.arange(len(c))
    # place c0 at the DC band center; c1..cN at n*f0
    n_pos = np.array([f_dc] + [float(n) * f0 for n in n_idx[1:]])

    markerline, stemlines, baseline = ax_bot.stem(
        n_pos, c, basefmt=" ")
    plt.setp(stemlines, color="0.35", lw=1.6)
    plt.setp(markerline, color="0.15", markersize=6)

    # color & annotate the three "listening" channels c0, c1, c2
    for bi, ((lo, hi), col, ci) in enumerate(zip(band_spans, band_colors, band_coeff_idx)):
        xpos = n_pos[ci]
        # shade the same band behind the stem for visual alignment
        ax_bot.axvspan(lo, hi, color=col, alpha=0.18, zorder=0)
        ax_bot.plot([xpos], [c[ci]], "o", color=col, markersize=9, zorder=6)
        # The c1 channel sits exactly at the carrier, where the folding
        # arrowheads (zorder 8) converge; nudge its label to the right and
        # raise its zorder so the arrows don't occlude the value.
        at_carrier = abs(xpos - 1.0 * f0) < 1e-6
        ax_bot.text(xpos * (1.04 if at_carrier else 1.0), c[ci] + 0.04,
                    fr"$c_{ci}$={c[ci]:.2f}",
                    ha="left" if at_carrier else "center", va="bottom",
                    fontsize=9, color=col, fontweight="bold", zorder=9)

    ax_bot.set_ylim(0, max(c) * 1.45)
    ax_bot.set_xlabel(r"頻率 $f / f_0$  (下面 stem 的 $n$ 對齊 $n f_0$)")
    ax_bot.set_ylabel(r"ISF 諧波增益 $|c_n|$")
    ax_bot.grid(True, which="both", axis="y", alpha=0.3)

    # ---- folding arrows: each band folds down to the carrier, weighted c_n --
    # Draw curved arrows from each band (bottom panel) toward the carrier
    # position (n=1 -> f0 is the carrier reference) to evoke "fold to carrier".
    y_arrow = max(c) * 1.18
    carrier_x = 1.0 * f0  # the carrier lives at f0 on this f/f0 axis
    fold_notes = [
        (n_pos[0], r"$c_0$: flicker 上轉 $\to$ 1/f$^3$"),
        (n_pos[1], r"$c_1$: white 下轉 $\to$ 1/f$^2$"),
        (n_pos[2], r"$c_2$: white 下轉 $\to$ 1/f$^2$"),
    ]
    for (x0, note), col in zip(fold_notes, band_colors):
        if abs(x0 - carrier_x) < 1e-6:
            continue  # c1 already sits at the carrier; no arrow needed
        arr = FancyArrowPatch(
            (x0, y_arrow), (carrier_x, y_arrow),
            connectionstyle="arc3,rad=-0.35",
            arrowstyle="-|>", mutation_scale=14,
            lw=1.6, color=col, zorder=8)
        ax_bot.add_patch(arr)

    # mark the carrier
    ax_bot.axvline(carrier_x, color="0.5", ls="--", lw=0.9, zorder=2)
    ax_bot.text(carrier_x * 1.18, max(c) * 1.40, r"載波 (carrier)",
                ha="left", va="top", fontsize=8.5, color="0.4")

    # a compact legend-as-text for the folding story
    ax_bot.text(
        0.012, 0.96,
        "每個頻段折回載波，權重 = 該諧波的 $|c_n|$\n"
        r"$c_0$:flicker$\to$1/f$^3$    $c_1,c_2$:white$\to$1/f$^2$",
        transform=ax_bot.transAxes, ha="left", va="top", fontsize=8.2,
        bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="0.7", alpha=0.95),
        zorder=9)

    ax_bot.set_xlim(f[0], f[-1])

    savefig(fig, "device_noise_isf_bands.png")
    print(f"[fig_device_noise_bands] c0={c[0]:.3f} c1={c[1]:.3f} "
          f"c2={c[2]:.3f}  (toy asymmetric ISF; pedagogical, not transistor-level)")


if __name__ == "__main__":
    main()
