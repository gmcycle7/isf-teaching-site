"""
fig_impulse_decomp.py

Goal
----
Make Gamma(theta) = -sin(theta) feel *visually inevitable* for the ideal LC
oscillator, by drawing the geometry of Step 3 in
docs/03_isf_core_theory/impulse_to_phase_shift.md:

  * the limit cycle drawn as the unit circle (state z = (v, w) = A(cos th, sin th)),
  * a charge impulse Delta q kicks ONLY the capacitor-voltage axis, so on the
    state plane it is a HORIZONTAL step  Delta V = Delta q / C  (the inductor
    current cannot change instantaneously),
  * that horizontal step is decomposed by dashed construction lines into
      - a TANGENTIAL component (along the cycle) -> permanent phase shift  Delta phi,
      - a RADIAL component (off the cycle)       -> amplitude error  Delta A (decays away).

The SAME Delta V is applied at two operating phases:
  * a zero crossing (theta = 90 deg): the horizontal kick is almost purely
    TANGENTIAL  -> nearly all phase, |Gamma| is maximal,
  * a peak (theta = 0 deg): the horizontal kick is purely RADIAL
    -> nearly all amplitude, Gamma ~ 0.

Seeing the tangential share follow -sin(theta) makes the ideal-LC ISF
Gamma(theta) = -sin(theta) obvious. (Hajimiri-Lee 1998: Eq.(9) charge->voltage
step; Eq.(10)-(11) phase impulse response; the -sin(theta) form is derived in
docs/03_isf_core_theory/isf_definition.md.)

Figure produced
---------------
  static/figures/impulse_phase_decomposition.png

This is a pedagogical geometric figure (ideal lossless LC, small-signal limit),
NOT a transistor-level extraction.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt

from plot_utils import savefig
from isf_utils import gamma_lc_ideal


# Colours reused consistently with the rest of the site:
#   green = tangential / phase (persists),  red = radial / amplitude (decays).
C_CYCLE = "black"
C_DV = "tab:blue"
C_TANG = "tab:green"
C_RAD = "tab:red"


def _draw_panel(ax, theta, title, dv=0.7):
    """
    Draw one operating point on the unit-circle limit cycle, apply a horizontal
    Delta V kick, and decompose it into tangential / radial components.

    theta : injection phase (rad), measured so that z = (cos theta, sin theta).
    dv    : magnitude of the horizontal voltage step (state-plane units).
    """
    # --- limit cycle (unit circle) ---
    th = np.linspace(0, 2 * np.pi, 400)
    ax.plot(np.cos(th), np.sin(th), "--", color=C_CYCLE, lw=1.4,
            label="limit cycle (極限環, 穩態軌跡)")

    # --- operating point on the cycle ---
    p = np.array([np.cos(theta), np.sin(theta)])
    ax.plot(*p, "o", color=C_CYCLE, ms=8, zorder=6)

    # --- the charge kick: a HORIZONTAL Delta V = Delta q / C step ---
    # A current impulse only moves the capacitor voltage (the x axis here);
    # the inductor current (y axis) cannot change instantaneously.
    dv_vec = np.array([dv, 0.0])
    q = p + dv_vec
    ax.annotate("", xy=q, xytext=p,
                arrowprops=dict(arrowstyle="->", color=C_DV, lw=2.8), zorder=5)

    # --- local unit vectors at the operating point ---
    # On the unit circle the outward RADIAL direction is p itself (||p||=1);
    # the TANGENTIAL direction (direction of increasing phase) is (-sin, cos).
    r_hat = p.copy()                       # radial (outward) unit vector
    t_hat = np.array([-p[1], p[0]])        # tangential unit vector

    # Decompose the horizontal kick onto the local (tangential, radial) frame.
    tang_amt = float(np.dot(dv_vec, t_hat))   # -> Delta phi  (note: == -sin(theta)*dv)
    rad_amt = float(np.dot(dv_vec, r_hat))    # -> Delta A

    tang_vec = tang_amt * t_hat
    rad_vec = rad_amt * r_hat

    # tangential component (phase, persists) -- offset slightly so a zero-length
    # arrow is not drawn (annotate dislikes xy == xytext)
    if np.hypot(*tang_vec) > 1e-6:
        ax.annotate("", xy=p + tang_vec, xytext=p,
                    arrowprops=dict(arrowstyle="->", color=C_TANG, lw=2.8),
                    zorder=5)
    if np.hypot(*rad_vec) > 1e-6:
        ax.annotate("", xy=p + rad_vec, xytext=p,
                    arrowprops=dict(arrowstyle="->", color=C_RAD, lw=2.8),
                    zorder=5)

    # dashed construction lines completing the parallelogram from p -> q
    if np.hypot(*tang_vec) > 1e-6:
        ax.plot([(p + tang_vec)[0], q[0]], [(p + tang_vec)[1], q[1]],
                ":", color=C_RAD, lw=1.2, zorder=4)
    if np.hypot(*rad_vec) > 1e-6:
        ax.plot([(p + rad_vec)[0], q[0]], [(p + rad_vec)[1], q[1]],
                ":", color=C_TANG, lw=1.2, zorder=4)

    ax.set_aspect("equal")
    ax.set_xlim(-1.8, 2.05)
    ax.set_ylim(-1.85, 1.85)
    ax.axhline(0, color="0.85", lw=0.6, zorder=0)
    ax.axvline(0, color="0.85", lw=0.6, zorder=0)
    ax.set_xlabel(r"state $v$ (電容電壓, normalized)")
    ax.set_ylabel(r"state $w$ ($\propto$ 電感電流, normalized)")
    ax.set_title(title, fontsize=11)

    return p, q, dv_vec, tang_vec, rad_vec


def _gamma_box(ax, theta):
    """Bottom-left numeric annotation: the tangential SHARE is exactly -sin(theta)."""
    g = gamma_lc_ideal(theta)   # = -sin(theta)
    deg = int(round(np.degrees(theta)))
    # avoid '-0.00'
    gtxt = f"{g:+.2f}" if abs(g) > 5e-3 else "0.00"
    ax.text(0.03, 0.03,
            f"θ = {deg}°\n"
            r"$\Gamma(\theta)=-\sin\theta=$" + f" {gtxt}\n"
            r"切向佔比 $=\Gamma(\theta)$",
            transform=ax.transAxes, fontsize=9.5, va="bottom", ha="left",
            bbox=dict(boxstyle="round", fc="white", ec="0.7", alpha=0.95),
            zorder=7)


def fig_impulse_decomp():
    fig, axes = plt.subplots(1, 2, figsize=(13.0, 6.8))

    # We pick injection phases slightly OFF the exact extremes so that BOTH the
    # tangential and the radial component are visible and the dashed decomposition
    # parallelogram is legible. The numeric box still reports Gamma=-sin(theta),
    # and the dominant share matches the "almost all tangential / almost all
    # radial" message exactly.
    th_zc = np.radians(108)   # near a zero crossing  -> tangential dominates
    th_pk = np.radians(20)    # near the peak         -> radial dominates

    # ---------------------------------------------------------------------
    # Left: near zero crossing -> horizontal kick is ALMOST ALL tangential.
    # ---------------------------------------------------------------------
    p, q, dv_vec, tang_vec, rad_vec = _draw_panel(
        axes[0], th_zc,
        "在 zero-crossing 附近注入：水平踢幾乎全是切向 → 幾乎純相位")
    axes[0].text(p[0] + 0.04, p[1] + 0.30,
                 r"$\Delta V=\Delta q/C$" + "\n(水平踢電容電壓軸)",
                 color=C_DV, fontsize=9.5, ha="center", va="bottom", zorder=7)
    axes[0].text((p + tang_vec)[0] - 0.02, (p + tang_vec)[1] - 0.40,
                 r"切向 (大)" + "\n" + r"$\to\ \Delta\varphi$, 永久相位",
                 color=C_TANG, fontsize=9.5, ha="center", va="top", zorder=7)
    axes[0].text((p + rad_vec)[0] - 0.62, (p + rad_vec)[1] + 0.02,
                 r"徑向 (小)" + "\n" + r"$\to\ \Delta A$, 會衰減",
                 color=C_RAD, fontsize=9.5, ha="right", va="center", zorder=7)
    _gamma_box(axes[0], th_zc)

    # ---------------------------------------------------------------------
    # Right: near the peak -> horizontal kick is ALMOST ALL radial (Gamma ~ 0).
    # ---------------------------------------------------------------------
    p, q, dv_vec, tang_vec, rad_vec = _draw_panel(
        axes[1], th_pk,
        "在 peak 附近注入：水平踢幾乎全是徑向 → 幾乎純振幅 (Γ≈0)")
    axes[1].text((p + dv_vec)[0] + 0.04, (p + dv_vec)[1] + 0.34,
                 r"$\Delta V=\Delta q/C$" + "\n(水平踢電容電壓軸)",
                 color=C_DV, fontsize=9.5, ha="center", va="bottom", zorder=7)
    axes[1].text((p + rad_vec)[0] + 0.02, (p + rad_vec)[1] - 0.50,
                 r"徑向 (大)" + "\n" + r"$\to\ \Delta A$, 會衰減",
                 color=C_RAD, fontsize=9.5, ha="center", va="top", zorder=7)
    axes[1].text((p + tang_vec)[0] - 0.55, (p + tang_vec)[1] - 0.28,
                 r"切向 (小)" + "\n" + r"$\to\ \Delta\varphi$, 永久相位",
                 color=C_TANG, fontsize=9.5, ha="right", va="top", zorder=7)
    _gamma_box(axes[1], th_pk)

    # single shared legend (limit cycle line)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=1,
               fontsize=9.5, frameon=False, bbox_to_anchor=(0.5, 0.995))

    fig.suptitle(
        r"同一個 $\Delta V=\Delta q/C$，注入相位不同 → 切向佔比 $=\Gamma(\theta)=-\sin\theta$",
        y=1.05, fontsize=13)

    savefig(fig, "impulse_phase_decomposition.png")


def main():
    print("[fig_impulse_decomp] ISF Step-3 geometric decomposition ...")
    fig_impulse_decomp()


if __name__ == "__main__":
    main()
