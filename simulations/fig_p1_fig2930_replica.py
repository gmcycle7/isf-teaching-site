"""
fig_p1_fig2930_replica.py

Goal
----
Conceptual replica (NOT a digitization) of two figures from [P1]'s Appendix
"Calculation of the Impulse Sensitivity Function":

  * [P1] Fig. 29, p.192 -- caption (verbatim):
        "State-space trajectory of an n th-order oscillator."
    A schematic n-dimensional sketch in the paper: axes X1, X2, Xn, a thick
    closed limit-cycle trajectory, the state vector X, a perturbation vector
    Delta X pushing the state off the cycle, the velocity vector Xdot tangent
    to the trajectory, a thin perturbed trajectory rejoining the cycle, and
    the resulting phase shift Delta phi.

  * [P1] Fig. 30, p.193 -- caption (verbatim):
        "ISF's obtained from different methods."
    Plot title "Calculation of Impulse Sensitivity Function"; y axis "ISF"
    (-1.0 .. 1.0), x axis "x (radians)" (0 .. 2*pi); three monochrome curves:
    solid "1st Method" (direct impulse response), dotted "2nd Method"
    (state-space closed form), dashed "3rd Method" (first-derivative
    approximation).  In the paper the 1st and 2nd methods nearly coincide
    while the dashed 3rd method overshoots the positive lobe.

Replica scope (honest)
----------------------
The paper's Fig. 29 is a hand-drawn schematic and Fig. 30's oscillator is
not specified in the figure.  Here BOTH panels are computed from the site's
van der Pol toy (x'' - mu(1-x^2)x' + x = 0), reusing existing machinery:

  * Left  (Fig. 29 replica): mu = 2.0 cycle from fig_isf_three_methods'
    mu-parameterized helpers (find_cycle_mu / cycle_states / rk4_state).
    The thick loop, the thin perturbed trajectory and the Delta phi gap are
    REAL integrated dynamics (kick Delta x on the x axis, then relax), drawn
    in an oblique 2D projection of an (X1, X2, Xn) frame to echo the paper's
    axonometric look.  Delta phi is also measured numerically (late
    zero-crossing shift, same algorithm as the impulse method).
  * Right (Fig. 30 replica): mu = 0.2 duel from lab_25's machinery
    (find_limit_cycle, extract_isf_impulse_axis) + fig_isf_three_methods'
    methods_b_c: Method A (impulse, solid), Method B (Eq.(37), dotted),
    Method C (Eq.(38), dashed), styled after the paper's monochrome plot.
    Phase zero is placed at the waveform MINIMUM so the positive lobe
    precedes the negative trough, matching the paper's lobe ordering
    (harmonic limit f ~ -cos x  =>  Gamma ~ +sin x).

Known, disclosed difference from the original: in the paper the 1st/2nd
methods coincide and the 3rd deviates (an N-stage ring keeps Eq.(36)'s
denominator constant); on a single-node van der Pol it is B and C that
nearly coincide while the impulse truth A departs near the lobes (AM->PM,
see fig_isf_three_methods / derivation_floquet_ppv).  The page caption says
so explicitly.  All quantities are normalized/dimensionless; pedagogical toy
model, not transistor-level.

Figure
------
    static/figures/p1_fig2930_replica.png

Run
---
    PYTHONPATH=. python simulations/fig_p1_fig2930_replica.py   (< 60 s)
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)                          # sibling fig/lab modules
sys.path.insert(0, os.path.join(_HERE, "common"))  # shared utilities

import numpy as np

# read-only reuse of existing machinery
from fig_isf_three_methods import (find_cycle_mu, cycle_states, rk4_state,
                                   vdp_deriv, methods_b_c, rms)
from lab_25_floquet_numeric import (MU as MU_LAB25, find_limit_cycle,
                                    extract_isf_impulse_axis)

MU_SKETCH = 2.0    # left panel: distorted loop, fast amplitude relaxation
MU_DUEL = 0.2      # right panel: lab_25's near-harmonic case
DQ_SKETCH = 0.45   # visible (exaggerated) kick for the Fig. 29 sketch
N_PHASES = 24      # impulse phases for Method A (right panel)


# ---------------------------------------------------------------------------
# Fig. 29 replica helpers: oblique projection of an (X1, X2, Xn) frame
# ---------------------------------------------------------------------------
# 2D screen directions of the three axes (axonometric, echoing the paper:
# X1 to the lower left, X2 to the right, Xn up)
E1 = np.array([-0.55, -0.40])
E2 = np.array([1.00, 0.05])
EN = np.array([0.06, 1.00])
Z0 = 1.60              # lift of the cycle plane above the origin


def embed(x, y):
    """Map a van der Pol state (x, y) into the sketch's 3D frame and project.

    The cycle is placed in a tilted plane: u1 (depth) follows y, u2
    (horizontal) follows x, un (height) = Z0 + tilt terms.  Returns the
    projected screen coordinates (px, py)."""
    u1 = 0.42 * y
    u2 = 1.05 * x
    un = Z0 + 0.30 * y + 0.10 * x
    px = u1 * E1[0] + u2 * E2[0] + un * EN[0]
    py = u1 * E1[1] + u2 * E2[1] + un * EN[1]
    return px, py


def integrate(state, t_total, dt, mu):
    """RK4 trajectory from `state`; returns arrays (xs, ys)."""
    n = int(round(t_total / dt))
    x, y = state
    xs = np.empty(n + 1)
    ys = np.empty(n + 1)
    xs[0], ys[0] = x, y
    for k in range(n):
        x, y = rk4_state(x, y, dt, mu)
        xs[k + 1], ys[k + 1] = x, y
    return xs, ys


def measure_dphi(state, dq, T, mu, dt=2.5e-3):
    """Asymptotic phase shift of a kick Delta x = dq applied at `state`:
    compare a late rising zero crossing of x against the unkicked run
    (same algorithm as the impulse method; Delta phi = -2*pi*dt_shift/T
    with the site's sign convention Gamma = -w0*dt_shift/dq)."""
    t_late, t_end = 9.0 * T, 12.0 * T
    n = int(round(t_end / dt))

    def run(kick):
        x, y = state
        if kick:
            x += dq
        xs = np.empty(n + 1)
        xs[0] = x
        for k in range(n):
            x, y = rk4_state(x, y, dt, mu)
            xs[k + 1] = x
        return xs

    def first_late_zc(xs):
        neg = xs < 0
        idx = np.where(neg[:-1] & ~neg[1:])[0]
        for i in idx:
            tc = i * dt + dt * (0.0 - xs[i]) / (xs[i + 1] - xs[i])
            if tc > t_late:
                return tc
        raise RuntimeError("no late zero crossing found")

    dt_shift = (first_late_zc(run(True)) - first_late_zc(run(False))
                + T / 2.0) % T - T / 2.0
    return -2.0 * np.pi * dt_shift / T


def draw_fig29(ax):
    """Left panel: conceptual replica of [P1] Fig. 29 with real vdP dynamics."""
    mu = MU_SKETCH
    s0, T = find_cycle_mu(mu)
    print("T (mu=2.0 sketch cycle) =", round(T, 4))
    # -> 7.6299  (same cycle as fig_isf_three_methods' mu=2.0 case)
    theta, xs, ys, _ = cycle_states(s0, T, mu, n=3000)

    # thick limit cycle
    px, py = embed(xs, ys)
    ax.plot(px, py, color="black", lw=2.6, solid_capstyle="round", zorder=3)

    # traversal arrowhead on the loop, pointing ALONG the motion (drawn on
    # the fast-falling branch at the bottom, away from the perturbation zone)
    k_bot = int(np.argmin(py))
    ax.annotate("", xy=(px[k_bot + 60], py[k_bot + 60]),
                xytext=(px[k_bot], py[k_bot]),
                arrowprops=dict(arrowstyle="-|>", color="black", lw=2.0),
                zorder=4)

    # injection point on the cycle + perturbed trajectory (real dynamics):
    # on the fast-rising branch heading right (echoing the paper's sketch,
    # where the velocity vector points toward X2)
    half = (len(xs) - 1) // 2
    k_inj = int(np.argmin((xs[:half] - 1.2) ** 2 + (ys[:half] - 2.5) ** 2))
    x0, y0 = xs[k_inj], ys[k_inj]
    xp, yp = integrate((x0 + DQ_SKETCH, y0), 1.75 * T, T / 4000.0, mu)
    ppx, ppy = embed(xp, yp)
    ax.plot(ppx, ppy, color="black", lw=0.9, zorder=2)

    p_inj = np.array(embed(x0, y0))
    p_kick = np.array(embed(x0 + DQ_SKETCH, y0))

    # measured asymptotic phase shift of this kick
    dphi = measure_dphi((x0, y0), DQ_SKETCH, T, mu)
    print("Delta phi of the sketched kick =", round(dphi, 4), "rad",
          "(", round(dphi / (2 * np.pi), 4), "cycles )")
    # -> -0.7681 rad ( -0.1223 cycles )
    # (real dynamics; deliberately exaggerated dq = 0.45 for legibility)

    # Delta phi gap: reference vs perturbed state at the SAME time, marked
    # where the reference sits on the upper-right slow branch -- there both
    # points crawl, so the (real, measured) time shift shows up as a short
    # arrow along the trajectory, like the paper's small Delta phi marker
    xr, yr = integrate((x0, y0), 1.75 * T, T / 4000.0, mu)
    k_lo, k_hi = int(0.15 * 4000), int(0.60 * 4000)
    k_mark = k_lo + int(np.argmin((xr[k_lo:k_hi] - 1.55) ** 2
                                  + (yr[k_lo:k_hi] + 0.4) ** 2))
    p_ref = np.array(embed(xr[k_mark], yr[k_mark]))
    p_per = np.array(embed(xp[k_mark], yp[k_mark]))
    ax.annotate("", xy=tuple(p_per), xytext=tuple(p_ref),
                arrowprops=dict(arrowstyle="<->", color="black", lw=1.1),
                zorder=5)
    mid = 0.5 * (p_ref + p_per)
    ax.text(mid[0] - 0.02, mid[1] - 0.42, r"$\Delta\phi$",
            fontsize=13, ha="center", zorder=6)

    # axes of the (X1, X2, Xn) frame
    for e, L, lab, off in ((E1, 2.1, r"$X_1$", (-0.14, -0.18)),
                           (E2, 3.3, r"$X_2$", (0.14, -0.02)),
                           (EN, 3.3, r"$X_n$", (0.02, 0.12))):
        ax.annotate("", xy=tuple(e * L), xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", color="black", lw=1.2))
        ax.text(e[0] * L + off[0], e[1] * L + off[1], lab, fontsize=13)

    # state vector X (origin -> injection point)
    ax.annotate("", xy=tuple(p_inj), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color="black", lw=1.8),
                zorder=4)
    ax.text(p_inj[0] * 0.50 + 0.16, p_inj[1] * 0.50 - 0.16, r"$\vec X$",
            fontsize=13)

    # perturbation vector Delta X (injection point -> kicked state)
    ax.annotate("", xy=tuple(p_kick), xytext=tuple(p_inj),
                arrowprops=dict(arrowstyle="-|>", color="black", lw=1.6),
                zorder=5)
    ax.text(p_kick[0] - 0.10, p_kick[1] + 0.14, r"$\Delta\vec X$",
            fontsize=12)

    # velocity vector Xdot (tangent at the injection point)
    dx, dy = vdp_deriv(x0, y0, mu)
    tx, ty = embed(np.array([x0, x0 + dx]), np.array([y0, y0 + dy]))
    tvec = np.array([tx[1] - tx[0], ty[1] - ty[0]])
    tvec = 1.15 * tvec / np.hypot(*tvec)
    ax.annotate("", xy=tuple(p_inj + tvec), xytext=tuple(p_inj),
                arrowprops=dict(arrowstyle="-|>", color="black", lw=1.4),
                zorder=5)
    ax.text(p_inj[0] + tvec[0] + 0.08, p_inj[1] + tvec[1] - 0.28,
            r"$\dot{\vec X}$", fontsize=13)

    # dotted "isochron sheet" diamonds around the perturbation region,
    # echoing the paper's dotted plane patches (drawn in the cycle plane)
    for cx, cy in ((x0, y0), (x0 + DQ_SKETCH, y0)):
        ux = np.array([0.55, 0.0])          # in-plane state offsets
        uy = np.array([0.0, 1.35])
        corners = [(cx + sx * ux[0] + sy * uy[0],
                    cy + sx * ux[1] + sy * uy[1])
                   for sx, sy in ((1, 0), (0, 1), (-1, 0), (0, -1), (1, 0))]
        gx, gy = embed(np.array([c[0] for c in corners]),
                       np.array([c[1] for c in corners]))
        ax.plot(gx, gy, ls=":", lw=0.7, color="gray", zorder=1)

    ax.set_aspect("equal")
    ax.set_xlim(-3.3, 3.9)
    ax.set_ylim(-1.35, 3.65)
    ax.axis("off")
    ax.grid(False)
    ax.set_title("[P1] Fig. 29 概念復刻：n 階振盪器的 state-space 軌跡\n"
                 "（van der Pol μ=2.0 實算：細線＝踢一下後真的重新收斂）",
                 fontsize=11)


# ---------------------------------------------------------------------------
# Fig. 30 replica: three methods on lab_25's mu = 0.2 van der Pol
# ---------------------------------------------------------------------------
def draw_fig30(ax):
    s0, T = find_limit_cycle()                    # lab_25, MU = 0.2
    theta, xs, ys, ydot = cycle_states(s0, T, MU_DUEL)
    gamma_B, gamma_C, A = methods_b_c(theta, xs, ys, ydot, T)
    th_imp, isf_imp = extract_isf_impulse_axis(s0, T, axis=0,
                                               n_points=N_PHASES)
    gamma_A = A * isf_imp

    # phase zero at the waveform MINIMUM: harmonic limit f ~ -cos(x),
    # Gamma ~ +sin(x) -> positive lobe first, trough second (paper's ordering)
    th_min = theta[int(np.argmin(xs))]
    thBC = (theta - th_min) % (2.0 * np.pi)
    oBC = np.argsort(thBC)
    thA = (th_imp - th_min) % (2.0 * np.pi)
    oA = np.argsort(thA)

    ax.plot(thA[oA], gamma_A[oA], color="black", ls="-", lw=1.7,
            marker="o", ms=4, mfc="none",
            label="1st Method（法 A 打脈衝，24 相位）")
    ax.plot(thBC[oBC], gamma_B[oBC], color="black", ls=":", lw=1.6,
            label="2nd Method（法 B closed form Eq.(37)）")
    ax.plot(thBC[oBC], gamma_C[oBC], color="black", ls="--", lw=1.2,
            label="3rd Method（法 C Eq.(38)）")
    ax.axhline(0.0, color="gray", lw=0.6)

    ax.set_xlim(0.0, 2.0 * np.pi)
    ax.set_ylim(-1.25, 1.25)
    ax.set_xticks([0.0, 2.0, 4.0, 6.0])
    ax.set_xticklabels(["0.0", "2.0", "4.0", "6.0"])
    ax.set_xlabel("x (radians)（θ=0 對齊波形谷值）")
    ax.set_ylabel("ISF")
    ax.legend(fontsize=8, loc="lower left")
    ax.set_title("[P1] Fig. 30 概念復刻：Calculation of Impulse "
                 "Sensitivity Function\n（van der Pol μ=0.2；原圖振盪器未載明）",
                 fontsize=11)

    # honest numbers (evaluated at the impulse phases, dimensionless Gamma)
    from isf_utils import gamma_rms
    gB_on_imp = np.interp(th_imp, theta, gamma_B)
    gC_on_imp = np.interp(th_imp, theta, gamma_C)
    print("Gamma_rms (Method A points) =", round(rms(gamma_A), 4))
    # -> 0.7777
    print("Gamma_rms (Method B) =",
          round(float(gamma_rms(theta, gamma_B)), 4))
    # -> 0.7097
    print("Gamma_rms (Method C) =",
          round(float(gamma_rms(theta, gamma_C)), 4))
    # -> 0.6758
    print("rms |B - A(impulse)| =", round(rms(gB_on_imp - gamma_A), 4))
    # -> 0.2365  (identical machinery to fig_isf_three_methods, same number)
    print("rms |C - A(impulse)| =", round(rms(gC_on_imp - gamma_A), 4))
    # -> 0.3219
    print("rms |C - B|          =", round(rms(gC_on_imp - gB_on_imp), 4))
    # -> 0.1336  (on a single-node vdP it is B and C that nearly coincide --
    #             disclosed difference vs the paper, where 1st ~= 2nd)


def main():
    import matplotlib.pyplot as plt
    from plot_utils import savefig

    assert MU_DUEL == MU_LAB25, "lab_25 machinery is hardwired to MU=0.2"
    print("[fig_p1_fig2930_replica] conceptual replica of [P1] "
          "Fig. 29 / Fig. 30 ...")

    fig, axes = plt.subplots(1, 2, figsize=(12.6, 5.2))
    draw_fig29(axes[0])
    draw_fig30(axes[1])
    fig.text(0.5, 0.012,
             "概念復刻，非原圖數位化：兩面板皆以本站 van der Pol toy 實算"
             "（原 Fig.29 為示意手繪、原 Fig.30 未載明振盪器）。",
             ha="center", fontsize=9, style="italic")
    fig.subplots_adjust(bottom=0.16)
    savefig(fig, "p1_fig2930_replica.png")


if __name__ == "__main__":
    main()
