"""
lab_37_ilfd_lock.py

Goal
----
Numerically verify [P4]'s M:N sub-/super-harmonic locking math -- the formal
theory behind the injection-locked frequency divider (ILFD):

  * [P4] Eq.(28), p.2129 : phi(t) = (M/N)*omega_inj*t + theta(t),
                           M, N positive COPRIME integers (M*w_inj = N*w_osc).
  * [P4] Eq.(29), p.2129 : dtheta/dt = omega0 - (M/N)*omega_inj
                           + (1/(N*T_inj)) * int_{N T_inj}
                             Gamma_tilde((M/N)*omega_inj*t + theta) i_inj(t) dt
  * [P4] Eq.(30), p.2129 : Omega(theta) = (1/2) I_inj |G_N| cos(N*theta + ang G_N)
                           (sinusoidal injection at the N-th superharmonic, M=1;
                            G_N = N-th Fourier phasor of Gamma_tilde = Gamma/qmax)
  * [P4] p.2130  (text)  : omega_L = I_inj * |G_N| / 2       <-- THE formula
  * [P4] Eq.(34), p.2130 : omega_b = N*sqrt(Dw^2 - omega_L^2); outside the lock
                           range theta drifts at the average rate omega_b / N.

What is simulated (and why it is a real test)
---------------------------------------------
We do NOT integrate the already-averaged Adler equation (that would verify the
theory "by construction").  We integrate the UNAVERAGED time-synchronous phase
ODE ([P3] Eq.(28)-(30) generalized per [P4] Eq.(28), M=1):

    dtheta/dt = (omega0 - omega_inj/N)
                + Gamma_tilde((omega_inj/N)*t + theta) * I_inj*cos(omega_inj*t)

with a 3-harmonic ISF (controllable c1, c2, c3, all with angle +90 deg):

    Gamma_tilde(x) = -( c1*sin(x) + c2*sin(2x) + c3*sin(3x) ) / qmax
                   =  ( c1*cos(x+90d) + c2*cos(2x+90d) + c3*cos(3x+90d) )/qmax

so |G_N| = c_N/qmax and ang G_N = +90 deg.  If [P4]'s time-synchronous
averaging is right, ONLY the resonant N-th ISF harmonic survives and the
measured half lock range (in Dw := omega_inj/N - omega0) equals
omega_L = (1/2)*I_inj*c_N/qmax.  A half-wave-symmetric ISF (c2 = 0,
Gamma(x+pi) = -Gamma(x)) must therefore NOT lock at 2*f0 (no divide-by-2).

Checks printed
--------------
  (1) Averaging identity: Omega(theta) computed by brute-force integration of
      Eq.(29)'s average vs the closed form Eq.(30), N = 2 and 3.
  (2) Lock-range sweep around 2*f0 and 3*f0: measured/predicted omega_L ~ 1.
  (3) Half-wave-symmetric ISF (c2=0): lock range at 2*f0 collapses.
  (4) Lock-range map vs c2 and vs c3: measured/predicted ratios ~ 1 (linear).
  (5) Out-of-lock drift rate vs [P4] Eq.(34) (omega_b/N): ratios ~ 1.
  (6) Locked phases 2*pi/N apart are indistinguishable ([P4] p.2129).

Canonical site values: f0 = 5 GHz, qmax = 1 pC, I_inj = 0.5 mA
  -> Imax := omega0*qmax = 31.4 mA ([P4] footnote 11, p.2130),
     I_inj/Imax = 1.6 % (weak injection: first-order model applies).

Figure
------
  static/figures/ilfd_lock_ranges.png

Run
---
  PYTHONPATH=<project root> python simulations/lab_37_ilfd_lock.py
  (runtime ~30-60 s)
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt

from plot_utils import savefig

# ---------------------------------------------------------------------------
# Canonical parameters
# ---------------------------------------------------------------------------
F0 = 5.0e9                      # free-running frequency        [Hz]
W0 = 2.0 * np.pi * F0           # omega0                        [rad/s]
QMAX = 1.0e-12                  # q_max                         [C]
IINJ = 0.5e-3                   # injection amplitude I_inj     [A]
ITILDE = IINJ / QMAX            # I_inj/qmax                    [rad/s] scale
C_BASE = (1.0, 0.5, 0.2)        # ISF harmonics c1, c2, c3      [dimensionless]

DT = 1.0e-12                    # ODE step (200 pts / carrier cycle)   [s]
T_TOTAL = 600.0e-9              # integration time                     [s]
N_STEPS = int(round(T_TOTAL / DT))
DEC = 200                       # store theta every DEC steps
LOCK_TOL = 0.1                  # |theta(T)-theta(T/2)| < tol -> locked [rad]


def omega_lock(c_n):
    """[P4] p.2130: omega_L = I_inj*|G_N|/2 with |G_N| = c_N/qmax  [rad/s]."""
    return 0.5 * ITILDE * c_n


def gamma_tilde(x, c1, c2, c3):
    """3-harmonic ISF/qmax; all harmonic angles +90 deg  [rad/C]."""
    sx, cx = np.sin(x), np.cos(x)
    s2 = 2.0 * sx * cx                    # sin(2x)
    s3 = sx * (3.0 - 4.0 * sx * sx)       # sin(3x)
    return -(c1 * sx + c2 * s2 + c3 * s3) / QMAX


# ---------------------------------------------------------------------------
# (1) Averaging identity: brute-force Eq.(29) average vs closed form Eq.(30)
# ---------------------------------------------------------------------------
def check_averaging(n_div, c1, c2, c3, dw_frac=0.5):
    """
    Omega(theta) = (1/(N*T_inj)) * int_0^{N*T_inj}
                     Gamma_tilde((w_inj/N)*t + theta) * I_inj*cos(w_inj*t) dt
    computed by trapezoid vs Eq.(30) = (1/2)*I_inj*(c_N/qmax)*cos(N*theta+90d).
    The window N*T_inj holds an integer number of BOTH periods (that is the
    whole point of time-synchronous averaging), for any detuning dw.
    """
    c_n = (c1, c2, c3)[n_div - 1]
    wq = W0 + dw_frac * omega_lock(c_n)      # omega_inj/N
    w_inj = n_div * wq
    t_win = n_div * 2.0 * np.pi / w_inj      # N*T_inj
    t = np.linspace(0.0, t_win, 200001)
    thetas = np.linspace(0.0, 2.0 * np.pi, 181)
    om_num = np.empty_like(thetas)
    for k, th in enumerate(thetas):
        integrand = gamma_tilde(wq * t + th, c1, c2, c3) * IINJ * np.cos(w_inj * t)
        om_num[k] = np.trapezoid(integrand, t) / t_win
    om_th = 0.5 * ITILDE * c_n * np.cos(n_div * thetas + np.pi / 2.0)
    err = np.max(np.abs(om_num - om_th)) / (0.5 * ITILDE * c_n)
    return thetas, om_num, om_th, err


# ---------------------------------------------------------------------------
# (2)-(6) Vectorized RK2 integration of the UNAVERAGED phase ODE
# ---------------------------------------------------------------------------
def integrate_batch(wq, n_div, c1, c2, c3, theta0):
    """
    Integrate dtheta/dt = (W0 - wq) + Gamma_tilde(wq*t + theta)*I*cos(N*wq*t)
    for a batch of columns.  wq = omega_inj/N per column.

    Returns theta history decimated by DEC:  shape (N_STEPS//DEC + 1, n_cols).
    """
    n_cols = wq.size
    theta = theta0.astype(float).copy()
    hist = np.empty((N_STEPS // DEC + 1, n_cols))
    hist[0] = theta
    detune = W0 - wq                                     # [rad/s]
    w_inj = n_div * wq                                   # [rad/s]

    def deriv(t, th):
        return detune + gamma_tilde(wq * t + th, c1, c2, c3) \
            * IINJ * np.cos(w_inj * t)

    t = 0.0
    for k in range(1, N_STEPS + 1):
        k1 = deriv(t, theta)
        k2 = deriv(t + 0.5 * DT, theta + 0.5 * DT * k1)  # midpoint RK2
        theta += DT * k2
        t += DT
        if k % DEC == 0:
            hist[k // DEC] = theta
    return hist


def lock_and_drift(hist):
    """
    locked : |theta(T) - theta(T/2)| < LOCK_TOL
    drift  : least-squares slope of theta over the last half  [rad/s]
    """
    n = hist.shape[0]
    half = hist[n // 2:]
    dtheta = np.abs(half[-1] - half[0])
    tt = np.arange(half.shape[0]) * (DEC * DT)
    tt = tt - tt.mean()
    slope = (tt[:, None] * (half - half.mean(axis=0))).sum(axis=0) / (tt ** 2).sum()
    return dtheta < LOCK_TOL, slope


def edge_from_grid(dw_grid, locked):
    """Half lock range = midpoint between outermost locked and first unlocked
    grid point, averaged over the two sides (grid must be sorted)."""
    edges = []
    for sgn in (+1, -1):
        side = dw_grid * sgn
        sel = side > 0
        d = side[sel]
        lk = locked[sel]
        order = np.argsort(d)
        d, lk = d[order], lk[order]
        idx = np.where(lk)[0]
        if idx.size == 0:
            edges.append(0.0)
            continue
        i_last = idx[-1]
        if i_last + 1 < d.size:
            edges.append(0.5 * (d[i_last] + d[i_last + 1]))
        else:
            edges.append(d[i_last])
    return 0.5 * (edges[0] + edges[1])


def main():
    print("[lab_37] ILFD M:N locking -- omega_L = (1/2) I_inj |Gamma_N| ...")
    c1, c2, c3 = C_BASE
    wl2 = omega_lock(c2)            # N=2 half lock range [rad/s]
    wl3 = omega_lock(c3)            # N=3 half lock range [rad/s]
    print(f"  params  : f0 = {F0/1e9:.0f} GHz, qmax = {QMAX*1e12:.0f} pC, "
          f"I_inj = {IINJ*1e3:.1f} mA, (c1,c2,c3) = {C_BASE}")
    print(f"  weak-inj: Imax = w0*qmax = {W0*QMAX*1e3:.1f} mA "
          f"([P4] fn.11 p.2130) -> I_inj/Imax = {IINJ/(W0*QMAX)*100:.1f} %")
    print(f"  theory  : omega_L(N=2, c2={c2}) = {wl2:.4g} rad/s "
          f"-> f_L = {wl2/2/np.pi/1e6:.2f} MHz")
    print(f"  theory  : omega_L(N=3, c3={c3}) = {wl3:.4g} rad/s "
          f"-> f_L = {wl3/2/np.pi/1e6:.2f} MHz")

    # ---------------- (1) averaging identity ---------------------------
    th_g2, om_n2, om_t2, err2 = check_averaging(2, c1, c2, c3)
    th_g3, om_n3, om_t3, err3 = check_averaging(3, c1, c2, c3)
    print(f"  avg-id  : max|Omega_num - Eq.(30)|/omega_L  N=2: {err2:.2e}  "
          f"N=3: {err3:.2e}   (time-synchronous window kills all other terms)")

    # ---------------- build the big batch -------------------------------
    cols_wq, cols_N, cols_c, cols_th0, tags = [], [], [], [], []

    def add(dw_arr, n_div, cvec, wl_pred, tag):
        for dw in dw_arr:
            cols_wq.append(W0 + dw)
            cols_N.append(n_div)
            cols_c.append(cvec)
            if wl_pred > 0:
                th_ss = -np.arcsin(np.clip(dw / wl_pred, -1, 1)) / n_div
            else:
                th_ss = 0.0
            cols_th0.append(th_ss + 0.15)
            tags.append(tag)

    # A: sweep around 2*f0, baseline ISF
    grid_A = np.linspace(-2.0, 2.0, 61) * wl2
    add(grid_A, 2, C_BASE, wl2, "A")
    # B: sweep around 3*f0, baseline ISF
    grid_B = np.linspace(-2.0, 2.0, 61) * wl3
    add(grid_B, 3, C_BASE, wl3, "B")
    # C: half-wave-symmetric ISF (c2 = 0) at 2*f0, same absolute grid as A
    add(grid_A, 2, (c1, 0.0, c3), 0.0, "C")
    # maps: lock range vs c2 (N=2) and vs c3 (N=3), positive edge only
    ratio_grid = np.linspace(0.9, 1.1, 41)
    c2_vals = np.array([0.15, 0.30, 0.45, 0.60])
    for c2v in c2_vals:
        add(ratio_grid * omega_lock(c2v), 2, (c1, c2v, c3), omega_lock(c2v),
            f"M2:{c2v:.2f}")
    c3_vals = np.array([0.10, 0.15, 0.20, 0.30])
    for c3v in c3_vals:
        add(ratio_grid * omega_lock(c3v), 3, (c1, c2, c3v), omega_lock(c3v),
            f"M3:{c3v:.2f}")
    # degeneracy: N=2, two starts pi apart; N=3, three starts 2pi/3 apart
    for th0 in (0.2, 0.2 + np.pi):
        cols_wq.append(W0 + 0.3 * wl2); cols_N.append(2)
        cols_c.append(C_BASE); cols_th0.append(th0); tags.append("D2")
    for th0 in (0.2, 0.2 + 2 * np.pi / 3, 0.2 + 4 * np.pi / 3):
        cols_wq.append(W0 + 0.3 * wl3); cols_N.append(3)
        cols_c.append(C_BASE); cols_th0.append(th0); tags.append("D3")

    wq = np.array(cols_wq)
    n_div = np.array(cols_N, dtype=float)
    carr = np.array(cols_c)
    th0 = np.array(cols_th0)
    tags = np.array(tags)
    print(f"  batch   : {wq.size} ODE columns x {N_STEPS} RK2 steps "
          f"(dt = {DT*1e12:.0f} ps, T = {T_TOTAL*1e9:.0f} ns) ...")

    hist = integrate_batch(wq, n_div, carr[:, 0], carr[:, 1], carr[:, 2], th0)
    locked, drift = lock_and_drift(hist)

    # ---------------- (2) sweeps A and B --------------------------------
    mA, mB, mC = tags == "A", tags == "B", tags == "C"
    edge_A = edge_from_grid(wq[mA] - W0, locked[mA])
    edge_B = edge_from_grid(wq[mB] - W0, locked[mB])
    print(f"  sweep 2f0: measured omega_L = {edge_A:.4g} rad/s vs theory "
          f"{wl2:.4g}  -> ratio {edge_A/wl2:.3f}")
    print(f"  sweep 3f0: measured omega_L = {edge_B:.4g} rad/s vs theory "
          f"{wl3:.4g}  -> ratio {edge_B/wl3:.3f}")
    print(f"  locked pts: A {int(np.sum(locked[mA]))}/61, "
          f"B {int(np.sum(locked[mB]))}/61")

    # ---------------- (3) half-wave-symmetric ISF -----------------------
    nlockC = int(np.sum(locked[mC]))
    edge_C = np.max(np.abs((wq[mC] - W0)[locked[mC]])) if nlockC else 0.0
    print(f"  c2=0 ISF : locked points {nlockC}/61 on the same +/-2*omega_L "
          f"grid; measured half range = {edge_C:.3g} rad/s "
          f"({edge_C/wl2*100:.1f} % of the c2={c2} lock range) -> no /2 lock")

    # ---------------- (4) lock-range maps vs c2, c3 ----------------------
    ratios2, ratios3 = [], []
    for c2v in c2_vals:
        m = tags == f"M2:{c2v:.2f}"
        r = (wq[m] - W0) / omega_lock(c2v)
        lk = locked[m]
        idx = np.where(lk)[0]
        edge = 0.5 * (r[idx[-1]] + r[idx[-1] + 1]) if idx.size and \
            idx[-1] + 1 < r.size else (r[idx[-1]] if idx.size else 0.0)
        ratios2.append(edge)
    for c3v in c3_vals:
        m = tags == f"M3:{c3v:.2f}"
        r = (wq[m] - W0) / omega_lock(c3v)
        lk = locked[m]
        idx = np.where(lk)[0]
        edge = 0.5 * (r[idx[-1]] + r[idx[-1] + 1]) if idx.size and \
            idx[-1] + 1 < r.size else (r[idx[-1]] if idx.size else 0.0)
        ratios3.append(edge)
    ratios2, ratios3 = np.array(ratios2), np.array(ratios3)
    print("  map N=2 : c2 =", np.array2string(c2_vals, precision=2),
          " measured/theory =", np.array2string(ratios2, precision=3))
    print("  map N=3 : c3 =", np.array2string(c3_vals, precision=2),
          " measured/theory =", np.array2string(ratios3, precision=3))
    print(f"  map mean: <ratio> N=2 {np.mean(ratios2):.3f} , "
          f"N=3 {np.mean(ratios3):.3f}   (omega_L linear in c_N)")

    # ---------------- (5) out-of-lock drift = omega_b/N ------------------
    dwA = wq[mA] - W0
    far = np.abs(dwA) >= 1.2 * wl2
    th_drift = -np.sign(dwA[far]) * np.sqrt(dwA[far] ** 2 - wl2 ** 2)
    ratio_beat = np.median(drift[mA][far] / th_drift)
    print(f"  beat     : median drift/(omega_b/N) over |dw|>=1.2 omega_L = "
          f"{ratio_beat:.3f}   ([P4] Eq.(34) p.2130)")

    # ---------------- (6) 2pi/N phase degeneracy -------------------------
    thD2 = hist[-1][tags == "D2"]
    thD3 = hist[-1][tags == "D3"]
    gap2 = np.mod(thD2[1] - thD2[0], 2 * np.pi)
    gaps3 = np.sort(np.mod(thD3 - thD3[0], 2 * np.pi))
    print(f"  degeneracy: N=2 final-theta gap = {gap2:.4f} rad "
          f"(2pi/2 = {np.pi:.4f}); N=3 gaps = "
          f"{gaps3[1]:.4f}, {gaps3[2]:.4f} rad "
          f"(2pi/3 = {2*np.pi/3:.4f}, 4pi/3 = {4*np.pi/3:.4f})")

    # ---------------- figure ---------------------------------------------
    fig, axes = plt.subplots(1, 3, figsize=(16.5, 5.2))

    # (a) normalized drift-rate "V" curves
    ax = axes[0]
    xA = dwA / wl2
    ax.plot(xA, -drift[mA] / wl2, "o", ms=4, color="tab:blue",
            label=r"$N=2$，$c_2=0.5$（量測）")
    dwB = wq[mB] - W0
    ax.plot(dwB / wl3, -drift[mB] / wl3, "s", ms=4, color="tab:green",
            label=r"$N=3$，$c_3=0.2$（量測，各自以 $\omega_L$ 正規化）")
    ax.plot(xA, -drift[mC] / wl2, "x", ms=5, color="tab:red",
            label=r"$N=2$，半波對稱 $c_2=0$：永不鎖定")
    xx = np.linspace(-2, 2, 400)
    yy = np.where(np.abs(xx) > 1, np.sign(xx) * np.sqrt(
        np.maximum(xx ** 2 - 1, 0)), 0.0)
    ax.plot(xx, yy, "k--", lw=1.4,
            label=r"理論 $\mathrm{sgn}(\Delta\omega)\sqrt{\Delta\omega^2-\omega_L^2}/\omega_L$")
    ax.plot(xx, xx, ":", color="gray", lw=1.2, label=r"無鎖定漸近線（漂移 $=\Delta\omega$）")
    ax.set_xlabel(r"正規化失諧 $\Delta\omega/\omega_L$，$\Delta\omega\equiv\omega_{inj}/N-\omega_0$")
    ax.set_ylabel(r"$\theta$ 平均漂移率 $/\,\omega_L$（$=\omega_b/(N\omega_L)$）")
    ax.set_title("(a) 鎖定平台與 lock range\n"
                 r"平台寬 $=2\omega_L=I_{inj}\vert\tilde\Gamma_N\vert$；$c_2=0$ 無平台（無 ÷2）")
    ax.legend(fontsize=8, loc="upper left")
    ax.set_xlim(-2.05, 2.05)

    # (b) lock range vs c_N
    ax = axes[1]
    cc = np.linspace(0, 0.65, 100)
    ax.plot(cc, 0.5 * ITILDE * cc / (2 * np.pi) / 1e6, "k--", lw=1.4,
            label=r"理論 $f_L=\frac{1}{2}I_{inj}\,c_N/(2\pi q_{max})$（與 $N$ 無關）")
    ax.plot(c2_vals, ratios2 * omega_lock(c2_vals) / (2 * np.pi) / 1e6, "o",
            ms=7, color="tab:blue", label=r"量測 $N=2$（$f_{inj}\approx2f_0$）")
    ax.plot(c3_vals, ratios3 * omega_lock(c3_vals) / (2 * np.pi) / 1e6, "s",
            ms=7, color="tab:green", label=r"量測 $N=3$（$f_{inj}\approx3f_0$）")
    ax.plot([0.0], [0.0], "x", ms=9, color="tab:red",
            label=r"$c_2=0$：lock range $\to 0$")
    ax.set_xlabel(r"ISF 第 $N$ 諧波大小 $c_N$（$\vert\tilde\Gamma_N\vert=c_N/q_{max}$）")
    ax.set_ylabel(r"量測半鎖定範圍 $f_L=\omega_L/2\pi$  [MHz]")
    ax.set_title("(b) ÷$N$ lock range 騎在 $c_N$ 上\n"
                 r"[P4] p.2130：$\omega_L=I_{inj}\vert\tilde\Gamma_N\vert/2$，對 $c_N$ 線性")
    ax.legend(fontsize=8, loc="upper left")
    ax.set_xlim(-0.03, 0.67)

    # (c) lock characteristic Omega(theta): numeric average vs Eq.(30)
    ax = axes[2]
    ax.plot(th_g2, om_t2 / (2 * np.pi) / 1e6, "-", color="tab:blue", lw=1.6,
            label=r"Eq.(30) $N=2$：$\frac{1}{2}I_{inj}\vert\tilde\Gamma_2\vert\cos(2\theta+\angle\tilde\Gamma_2)$")
    ax.plot(th_g2[::12], om_n2[::12] / (2 * np.pi) / 1e6, "o", ms=4,
            color="navy", label=r"數值平均 Eq.(29)，$N=2$")
    ax.plot(th_g3, om_t3 / (2 * np.pi) / 1e6, "-", color="tab:green", lw=1.6,
            label=r"Eq.(30) $N=3$")
    ax.plot(th_g3[::12], om_n3[::12] / (2 * np.pi) / 1e6, "s", ms=4,
            color="darkgreen", label=r"數值平均 Eq.(29)，$N=3$")
    ax.axhline(0.0, color="gray", lw=0.6)
    ax.set_xlabel(r"相對相位 $\theta$  [rad]")
    ax.set_ylabel(r"lock characteristic $\Omega(\theta)/2\pi$  [MHz]")
    ax.set_title("(c) 時間同步平均只留下第 $N$ 諧波\n"
                 r"$\Omega(\theta)$ 週期 $=2\pi/N$（$N$ 個不可分辨的鎖定相位）")
    ax.set_xticks([0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi])
    ax.set_xticklabels(["0", r"$\pi/2$", r"$\pi$", r"$3\pi/2$", r"$2\pi$"])
    ax.legend(fontsize=8, loc="upper right")

    fig.suptitle(r"ILFD 的 M:N 次諧波鎖定（[P4] Eq.(28)–(30), p.2129；"
                 r"$\omega_L=\frac{1}{2}I_{inj}\vert\tilde\Gamma_N\vert$, p.2130）"
                 f"— $f_0$={F0/1e9:.0f} GHz, $q_{{max}}$=1 pC, "
                 f"$I_{{inj}}$={IINJ*1e3:.1f} mA", fontsize=11)
    savefig(fig, "ilfd_lock_ranges.png")


if __name__ == "__main__":
    main()
