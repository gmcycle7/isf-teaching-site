"""
fig_isf_three_methods.py

Goal
----
Stage the "three-method duel" of [P1]'s Appendix, "Calculation of the
Impulse Sensitivity Function" (pp. 192-193), on one oscillator:

  Method A -- direct measurement of the impulse response (p. 192):
              inject a small impulse at many phases, measure the persistent
              time shift Delta t, use Delta phi = 2*pi*Delta t / T.
              Paper's own verdict: "the most accurate of the three methods".
  Method B -- closed form from the waveform (pp. 192-193):
              tangent projection Eqs. (31)-(33); node-voltage case Eq. (34);
              normalized-waveform forms Eqs. (35)-(36); and for a
              second-order system, Eq. (37):
                  Gamma(x) = f' / (f'^2 + f''^2).
  Method C -- first-derivative approximation, Eq. (38) (p. 193):
                  Gamma_i(x) = f_i'(x) / f'^2_max
              (denominator of (36) assumed ~ constant; meant for a ring
              with N identical stages).

Test oscillator: van der Pol (same toy as lab_15 / lab_25),

    x'' - mu (1 - x^2) x' + x = 0,   state (x, y = x').

The impulse is kicked on the x axis (the "node voltage" of the toy), so
Method B's second-order closed form Eq. (37) applies literally with the
normalized waveform f(theta) = x(theta)/A, A = max|x|:

    f'  = dx/dtheta / A = y  / (omega0   * A)
    f'' = dy/dtheta / A = y' / (omega0^2 * A)

and the dimensionless Gamma uses q_max <-> A (kick axis swing), i.e.
Gamma_A(theta) = A * (Delta phi / Delta x) for the impulse method.

Two cases:
  * mu = 0.2 (near-harmonic): all three methods agree with each other and
    with the -sin(theta) harmonic limit;
  * mu = 2.0 (distorted cycle): Method B degrades, because Eq. (31)'s
    ORTHOGONAL projection onto the unit tangent is only the true phase
    projection when the amplitude-decay (Floquet) direction is
    perpendicular to the tangent -- on a distorted cycle the exact
    projection is the OBLIQUE adjoint/PPV one (lab_25, [E2] Demir 2000,
    external literature, not among the site's 5 PDFs).  Method C collapses
    even harder (its "constant denominator" assumption needs an N-stage
    ring).  The rms numbers are printed honestly below.

Machinery reuse (read-only):
  * mu = 0.2: lab_25_floquet_numeric.find_limit_cycle / ppv_pipeline /
    extract_isf_impulse_axis are imported and used as-is (they are
    hardwired to MU = 0.2 through their integrator defaults).
  * mu = 2.0: the same algorithms are replicated below with an explicit
    `mu` argument (lab_25's helpers cannot be re-parameterized without
    editing that file, which stays untouched).

Phase convention: injections and states are indexed from the rising zero
crossing of x (lab_25's convention); for plotting/reference we re-zero the
phase at the WAVEFORM MAXIMUM so the harmonic limit reads f = cos(theta),
Gamma = -sin(theta) (site canonical, [P1] Eq. (37) sanity check p. 193).

All quantities are in normalized (dimensionless) units.  Pedagogical toy
model, not transistor-level.

Figure
------
    static/figures/isf_three_methods.png

Run
---
    PYTHONPATH=. python simulations/fig_isf_three_methods.py   (< 90 s)
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)                          # sibling lab modules
sys.path.insert(0, os.path.join(_HERE, "common"))  # shared utilities

import numpy as np

# read-only reuse of lab_25's machinery (fixed at its MU = 0.2)
from lab_25_floquet_numeric import (MU as MU_LAB25, find_limit_cycle,
                                    ppv_pipeline, extract_isf_impulse_axis)

MU_SMALL = 0.2   # near-harmonic (must equal lab_25's MU; asserted in main)
MU_LARGE = 2.0   # distorted / relaxation-leaning cycle


# ---------------------------------------------------------------------------
# mu-parameterized van der Pol helpers (replicate lab_25's algorithms; that
# file's integrators default to MU=0.2 and are reused untouched for that case)
# ---------------------------------------------------------------------------
def vdp_deriv(x, y, mu):
    """State derivative of x'' - mu (1 - x^2) x' + x = 0 as (x', y')."""
    return y, mu * (1.0 - x * x) * y - x


def rk4_state(x, y, dt, mu):
    k1x, k1y = vdp_deriv(x, y, mu)
    k2x, k2y = vdp_deriv(x + 0.5 * dt * k1x, y + 0.5 * dt * k1y, mu)
    k3x, k3y = vdp_deriv(x + 0.5 * dt * k2x, y + 0.5 * dt * k2y, mu)
    k4x, k4y = vdp_deriv(x + dt * k3x, y + dt * k3y, mu)
    return (x + dt / 6.0 * (k1x + 2 * k2x + 2 * k3x + k4x),
            y + dt / 6.0 * (k1y + 2 * k2y + 2 * k3y + k4y))


def find_cycle_mu(mu, t_settle=250.0, dt=1e-3, n_periods_avg=5):
    """Settle onto the cycle, then measure T from Newton-refined rising zero
    crossings of x (Poincare section x = 0, y > 0).  Same algorithm as
    lab_25.find_limit_cycle, with `mu` threaded through."""
    x, y = 2.0, 0.0
    for _ in range(int(round(t_settle / dt))):
        x, y = rk4_state(x, y, dt, mu)
    while True:
        xn, yn = rk4_state(x, y, dt, mu)
        if x < 0.0 <= xn and yn > 0.0:
            for _ in range(20):                     # Newton onto x = 0
                if abs(xn) < 1e-13:
                    break
                xn, yn = rk4_state(xn, yn, -xn / yn, mu)
            x, y = xn, yn
            break
        x, y = xn, yn
    t_acc, crossings = 0.0, 0
    while crossings < n_periods_avg:
        xn, yn = rk4_state(x, y, dt, mu)
        t_acc += dt
        if x < 0.0 <= xn and yn > 0.0:
            crossings += 1
        x, y = xn, yn
    for _ in range(20):
        if abs(x) < 1e-13:
            break
        step = -x / y
        x, y = rk4_state(x, y, step, mu)
        t_acc += step
    return (x, y), t_acc / n_periods_avg


def cycle_states(s0, T, mu, n=6000):
    """One period of the settled cycle on a uniform grid: theta measured
    from the rising zero crossing of x.  Returns (theta, x, y, ydot)."""
    h = T / n
    x, y = s0
    xs = np.empty(n + 1)
    ys = np.empty(n + 1)
    xs[0], ys[0] = x, y
    for k in range(n):
        x, y = rk4_state(x, y, h, mu)
        xs[k + 1], ys[k + 1] = x, y
    theta = np.linspace(0.0, 2.0 * np.pi, n + 1)
    ydot = mu * (1.0 - xs * xs) * ys - xs
    return theta, xs, ys, ydot


def impulse_isf_x(mu, s0, T, n_points=24, dq=0.02, dt=2.5e-3):
    """Method A on the x axis for arbitrary mu (same algorithm as
    lab_25.extract_isf_impulse_axis(axis=0)): kick x by dq at n_points
    phases, measure the persistent shift of a late rising zero crossing
    against an unkicked reference run; Gamma/q_max = -w0*dt_shift/dq."""
    w0 = 2.0 * np.pi / T
    t_late, t_end = 12.0 * T, 15.0 * T
    n = int(round(t_end / dt))

    def run(k_inj=-1):
        x, y = s0
        xs = np.empty(n + 1)
        xs[0] = x
        for k in range(n):
            if k == k_inj:
                x += dq
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

    z_ref = first_late_zc(run())
    thetas = np.linspace(0.0, 2.0 * np.pi, n_points, endpoint=False)
    isf = np.empty(n_points)
    for i, th in enumerate(thetas):
        t_inj = T + (th / (2.0 * np.pi)) * T
        z_p = first_late_zc(run(int(round(t_inj / dt))))
        dt_shift = (z_p - z_ref + T / 2.0) % T - T / 2.0
        isf[i] = -w0 * dt_shift / dq
    return thetas, isf


# ---------------------------------------------------------------------------
# Methods B and C from the stored waveform (no impulses, one cycle only)
# ---------------------------------------------------------------------------
def methods_b_c(theta, xs, ys, ydot, T):
    """[P1] Eq. (37) and Eq. (38) from the waveform.

    Normalized waveform f(theta) = x/A with A = max|x| ([P1] Eq. (1));
    derivatives are with respect to x = omega0*t (the paper's argument):
        f'  = y / (omega0 * A),      f'' = ydot / (omega0^2 * A).
    Returns (gamma_B, gamma_C, A):
        gamma_B = f'/(f'^2 + f''^2)     Eq. (37)  (dimensionless Gamma for a
                                        unit-charge kick on x, q_max <-> A)
        gamma_C = f'/max(f'^2)          Eq. (38)
    """
    w0 = 2.0 * np.pi / T
    A = float(np.max(np.abs(xs)))
    fp = ys / (w0 * A)
    fpp = ydot / (w0 * w0 * A)
    gamma_B = fp / (fp * fp + fpp * fpp)
    gamma_C = fp / float(np.max(fp * fp))
    return gamma_B, gamma_C, A


def rezero_at_peak(theta, xs):
    """Phase shift that puts theta = 0 at the waveform maximum of x, so the
    harmonic limit reads f ~ cos(theta), Gamma ~ -sin(theta)."""
    return theta[int(np.argmax(xs))]


def wrap_pi(th):
    return (th + np.pi) % (2.0 * np.pi) - np.pi


def rms(a):
    return float(np.sqrt(np.mean(np.asarray(a) ** 2)))


def duel(mu, use_lab25=False, n_points=24):
    """Run methods A/B/C for one mu.  Returns a dict of curves + metrics."""
    if use_lab25:
        s0, T = find_limit_cycle()                     # lab_25, MU = 0.2
    else:
        s0, T = find_cycle_mu(mu)
    theta, xs, ys, ydot = cycle_states(s0, T, mu)
    gamma_B, gamma_C, A = methods_b_c(theta, xs, ys, ydot, T)
    th_pk = rezero_at_peak(theta, xs)

    if use_lab25:
        th_imp, isf_imp = extract_isf_impulse_axis(s0, T, axis=0,
                                                   n_points=n_points)
    else:
        th_imp, isf_imp = impulse_isf_x(mu, s0, T, n_points=n_points)
    gamma_A = A * isf_imp                              # dimensionless Gamma

    # rms mismatches, all in the SAME dimensionless-Gamma units, evaluated
    # at the impulse phases (theta measured from the rising ZC of x)
    gB_on_imp = np.interp(th_imp, theta, gamma_B)
    gC_on_imp = np.interp(th_imp, theta, gamma_C)
    ref_sin = -np.sin(th_imp - th_pk)                  # harmonic reference
    out = dict(mu=mu, s0=s0, T=T, A=A, theta=theta, xs=xs,
               gamma_B=gamma_B, gamma_C=gamma_C, th_pk=th_pk,
               th_imp=th_imp, gamma_A=gamma_A,
               rms_B_vs_A=rms(gB_on_imp - gamma_A),
               rms_C_vs_A=rms(gC_on_imp - gamma_A),
               rms_B_vs_sin=rms(gB_on_imp - ref_sin),
               rms_A_vs_sin=rms(gamma_A - ref_sin))
    return out


def main():
    import matplotlib.pyplot as plt
    from plot_utils import savefig
    from isf_utils import gamma_rms

    assert MU_SMALL == MU_LAB25, "lab_25 machinery is hardwired to MU=0.2"
    print("[fig_isf_three_methods] [P1] Appendix three-method duel "
          "on van der Pol ...")

    # ---- closed-form sanity check on f = cos(x): Gamma = -sin exactly ----
    xg = np.linspace(0.0, 2.0 * np.pi, 2001)
    f, fp, fpp = np.cos(xg), -np.sin(xg), -np.cos(xg)
    err_cos = float(np.max(np.abs(fp / (fp ** 2 + fpp ** 2) - (-np.sin(xg)))))
    print("max |Eq.(37) on cos - (-sin)| =", "{:.1e}".format(err_cos))
    # -> 2.2e-16  (machine precision: sin^2+cos^2=1 makes Eq.(37) EXACT on cos)

    results = {}
    for mu in (MU_SMALL, MU_LARGE):
        print(f"--- mu = {mu} ---")
        r = duel(mu, use_lab25=(mu == MU_SMALL))
        results[mu] = r
        print("T  =", round(r["T"], 4))
        # -> 6.2989 / 7.6299  (mu=0.2 / mu=2.0)
        print("A  =", round(r["A"], 4))
        # -> 2.0004 / 2.0199  (mu=0.2 / mu=2.0; harmonic limit A=2)
        print("Gamma_rms (Method B) =",
              round(float(gamma_rms(r["theta"], r["gamma_B"])), 4))
        # -> 0.7097 / 1.9898  (mu=0.2 value ~ true-LC 1/sqrt2 = 0.7071)
        print("Gamma_rms (Method A points) =",
              round(rms(r["gamma_A"]), 4))
        # -> 0.7777 / 3.2151  (B underestimates by 9% / 38%)
        print("peak |Gamma_B| =", round(float(np.max(np.abs(r["gamma_B"]))), 4))
        # -> 0.9762 / 3.8496
        print("peak |Gamma_A| =", round(float(np.max(np.abs(r["gamma_A"]))), 4))
        # -> 1.0144 / 5.0011
        print("rms |B - A(impulse)| =", round(r["rms_B_vs_A"], 4))
        # -> 0.2365 / 2.072  (closed form vs impulse truth)
        print("rms |C - A(impulse)| =", round(r["rms_C_vs_A"], 4))
        # -> 0.3219 / 3.1803  (Eq.(38) is worse still: single node, no N-stage sum)
        print("rms |B - (-sin)|     =", round(r["rms_B_vs_sin"], 4))
        # -> 0.078 / 1.5657
        print("rms |A - (-sin)|     =", round(r["rms_A_vs_sin"], 4))
        # -> 0.28 / 2.8178  (truth leaves -sin long before the closed form does)

    # error-scaling check: the tangent-projection error of Method B should
    # shrink roughly like O(mu) as the cycle becomes circular (harmonic)
    r005 = duel(0.05, n_points=12)
    print("rms |B - A(impulse)| at mu=0.05 =", round(r005["rms_B_vs_A"], 4))
    # -> 0.0586  (0.2365 at mu=0.2: ratio 4.0 for 4x mu -- error ~ O(mu))

    # PPV (exact adjoint) overlay for the near-harmonic case, from lab_25:
    # one adjoint solve -> Gamma for the x kick axis = omega0 * v1_x
    res25 = ppv_pipeline()
    g_ppv = res25["amp_x"] * res25["omega0"] * res25["v1"][:, 0]
    r = results[MU_SMALL]
    g_ppv_on_imp = np.interp(r["th_imp"], res25["theta"], g_ppv)
    rms_B_vs_ppv = rms(np.interp(r["th_imp"], r["theta"], r["gamma_B"])
                       - g_ppv_on_imp)
    print("rms |B - PPV| (mu=0.2) =", round(rms_B_vs_ppv, 4))
    # -> 0.237  (impulse == PPV to ~0.002, so B's gap is the projection error)

    # ---- figure ------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(13.2, 4.9))
    for ax, mu in zip(axes, (MU_SMALL, MU_LARGE)):
        r = results[mu]
        # common x axis: phase re-zeroed at the waveform maximum, in [-pi,pi)
        thB = wrap_pi(r["theta"] - r["th_pk"])
        order = np.argsort(thB)
        thA = wrap_pi(r["th_imp"] - r["th_pk"])
        oA = np.argsort(thA)
        frac = thB[order] / (2 * np.pi)
        ax.plot(frac, r["gamma_B"][order], color="tab:blue", lw=2.0,
                label=r"法 B：closed form Eq.(37) $f'/(f'^2+f''^2)$")
        ax.plot(frac, r["gamma_C"][order], color="tab:green", lw=1.4,
                label=r"法 C：Eq.(38) $f'/f_{max}'^{\,2}$")
        if mu == MU_SMALL:
            thP = wrap_pi(res25["theta"] - r["th_pk"])
            oP = np.argsort(thP)
            ax.plot(thP[oP] / (2 * np.pi), g_ppv[oP], color="tab:purple",
                    lw=1.0, ls="-.",
                    label="嚴格 adjoint/PPV（lab_25，外部文獻）")
        ax.plot(thA[oA] / (2 * np.pi), r["gamma_A"][oA], "o", ms=5,
                color="tab:red", mfc="none",
                label="法 A：打脈衝實測（24 相位）")
        xg = np.linspace(-np.pi, np.pi, 400)
        ax.plot(xg / (2 * np.pi), -np.sin(xg), "k--", lw=1.0,
                label=r"諧波極限 $-\sin\theta$")
        ax.axhline(0, color="gray", lw=0.6)
        ax.set_xlabel(r"注入相位 $\theta/2\pi$（$\theta=0$ 對齊波形峰值，無因次）")
        ax.set_ylabel(r"$\Gamma(\theta)$（無因次，$q_{max}=A$）")
        tag = ("近諧波：形狀吻合，但峰值附近差 O(μ)" if mu == MU_SMALL
               else "強非線性：closed form 失準")
        ax.set_title(f"van der Pol μ={mu}（{tag}）\n"
                     f"rms差：B vs A={r['rms_B_vs_A']:.3f}，"
                     f"C vs A={r['rms_C_vs_A']:.3f}")
        ax.legend(fontsize=7.5,
                  loc=("upper right" if mu == MU_SMALL else "lower left"))

    savefig(fig, "isf_three_methods.png")


if __name__ == "__main__":
    main()
