"""
lab_36_lock_acquisition.py

Goal
----
Two transient/stochastic faces of the SAME classic Adler equation

    dtheta/dt = Dw - omega_L*sin(theta)        (site convention; reduced from
                                                [P3] Eq.(30)/(33)/(35), see
                                                injection_locking_noise page)

(i)  DETERMINISTIC lock acquisition inside the lock range |Dw| < omega_L.
     Separation of variables + tan-half-angle gives the EXACT solution

         R(theta(t)) = R(theta_0) * exp(-omega_c t),
         R(theta) = (u - u_minus)/(u - u_plus),  u = tan(theta/2),
         u_minus  = tan(theta_ss/2) = (omega_L - omega_c)/Dw   (stable),
         u_plus   = tan(theta_u /2) = (omega_L + omega_c)/Dw   (unstable),
         omega_c  = sqrt(omega_L^2 - Dw^2)

     so the exact global settle rate equals the linearized pull-in frequency
     omega_p of [P3] Eq.(39)-(40), p.2115 (equivalently [P4] Eq.(31)-(32),
     p.2130, written there with tanh). Acquisition time therefore diverges as
     Dw -> omega_L (critical slowing at the lock edge): T ~ 1/omega_c.

(ii) NOISE-INDUCED CYCLE SLIPS at fixed r = Dw/omega_L = 0.8.
     With white-FM drive n(t) (one-sided PSD S_n [rad^2/s]) the Adler equation
     is an overdamped particle in the TILTED WASHBOARD potential

         U(theta) = -Dw*theta - omega_L*cos(theta)
         (so that dtheta/dt = -U'(theta) + n(t))

     forward barrier  dU = 2*omega_L*( sqrt(1-r^2) - r*acos(r) ),
     Kramers escape rate (EXTERNAL standard stochastic theory, not in the
     site's 5 PDFs: Kramers 1940; Risken, The Fokker-Planck Equation, 2nd ed.,
     Ch. 11; Ambegaokar-Halperin 1969 for the RSJ washboard):

         nu ~ (omega_c/(2*pi)) * exp(-dU/D),
         D = D_yi (convention B of diffusion_dictionary: <n n'> = 2 D delta)
           = S_n/4 = kappa^2/2 = Gamma_rms^2 * S_i / (4 q_max^2)

     Euler-Maruyama with 512 parallel walkers; slip rate vs dU/D on a
     log-linear axis; the SLOPE of ln(nu) vs 1/D is fitted and compared to the
     analytic barrier (the prefactor is compared honestly: Kramers is only
     asymptotic for dU >> D).

Everything is integrated in dimensionless time tau = omega_L*t (the Adler
dynamics depend only on r and D/omega_L), then mapped back to the site
canonical numbers f_L = 5 MHz, f0 = 5 GHz, q_max = 1 pC, S_i = 1e-24 A^2/Hz
(true-LC Gamma_rms = 1/sqrt(2) -> S_n = 0.5 rad^2/s -> D = 0.125 rad^2/s).

Figure
------
  static/figures/lock_acquisition.png   (2 panels + inset)

Run
---
  PYTHONPATH=<project root> python simulations/lab_36_lock_acquisition.py
"""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq

from noise_utils import white_noise
from plot_utils import savefig

RNG = np.random.default_rng(36)

# ---------------------------------------------------------------------------
# canonical real-unit anchors (site spec section 8 + lab_26)
# ---------------------------------------------------------------------------
F_LOCK = 5.0e6                     # f_L = omega_L/2pi [Hz] (half lock range)
OMEGA_L = 2.0 * np.pi * F_LOCK     # [rad/s]
F0 = 5.0e9                         # carrier [Hz]
S_N_TRUE_LC = 0.5                  # one-sided white-FM PSD [rad^2/s], Gamma_rms=1/sqrt2
S_N_REPR = 0.25                    # representative Gamma_rms=0.5
D_TRUE_LC = S_N_TRUE_LC / 4.0      # convention B (<nn'>=2D*delta): D = S_n/4
D_REPR = S_N_REPR / 4.0


# ---------------------------------------------------------------------------
# analytic helpers (dimensionless: omega_L = 1, tau = omega_L * t)
# ---------------------------------------------------------------------------
def barrier(r):
    """Forward washboard barrier dU/omega_L = 2*(sqrt(1-r^2) - r*acos(r))."""
    return 2.0 * (np.sqrt(1.0 - r ** 2) - r * np.arccos(r))


def acquisition_exact(r, theta0=0.0, eps=0.01):
    """
    Exact acquisition time (dimensionless) from theta0 to theta_ss - eps via
    R(theta) = (u-u_minus)/(u-u_plus), R(t) = R(0)*exp(-wc*t).
    """
    wc = np.sqrt(1.0 - r ** 2)
    um = (1.0 - wc) / r            # tan(theta_ss/2), stable
    up = (1.0 + wc) / r            # tan(theta_u/2),  unstable
    u0 = np.tan(theta0 / 2.0)
    uthr = np.tan((np.arcsin(r) - eps) / 2.0)
    R = lambda u: (u - um) / (u - up)
    return (1.0 / wc) * np.log(R(u0) / R(uthr))


def theta_exact(r, tau, theta0=0.0):
    """Exact trajectory theta(tau) from the closed form (Moebius in e^{-wc*tau})."""
    wc = np.sqrt(1.0 - r ** 2)
    um = (1.0 - wc) / r
    up = (1.0 + wc) / r
    u0 = np.tan(theta0 / 2.0)
    R0 = (u0 - um) / (u0 - up)
    rho = R0 * np.exp(-wc * tau)
    u = (um - rho * up) / (1.0 - rho)
    return 2.0 * np.arctan(u)


# ---------------------------------------------------------------------------
# Part 1 : deterministic acquisition sweep (vectorized RK4 over r)
# ---------------------------------------------------------------------------
def acquisition_sweep(r_arr, eps=0.01, dtau=0.002, tau_max=100.0):
    th = np.zeros_like(r_arr)
    thr = np.arcsin(r_arr) - eps
    t_hit = np.full(r_arr.shape, np.nan)
    f = lambda x: r_arr - np.sin(x)
    tau = 0.0
    while np.isnan(t_hit).any() and tau < tau_max:
        k1 = f(th)
        k2 = f(th + 0.5 * dtau * k1)
        k3 = f(th + 0.5 * dtau * k2)
        k4 = f(th + dtau * k3)
        th_new = th + (dtau / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        hit = np.isnan(t_hit) & (th_new >= thr)
        if hit.any():
            # linear interpolation inside the step
            t_hit[hit] = tau + dtau * (thr[hit] - th[hit]) / (th_new[hit] - th[hit])
        th = th_new
        tau += dtau
    return t_hit


# ---------------------------------------------------------------------------
# Part 2 : Euler-Maruyama cycle-slip counter (M parallel walkers)
# ---------------------------------------------------------------------------
def slip_run(r, d_dimless, m, n_steps, dtau, rng, trace_stride=0):
    """
    Integrate dtheta/dtau = r - sin(theta) + n(tau) for m walkers.
    n is white with one-sided PSD 4*D (so that <nn'> = 2*D*delta, convention B).
    Slips are counted EXACTLY as integer jumps of floor((theta-theta_u)/2pi):
    that index is constant while theta stays inside one washboard well
    (well = (theta_u - 2pi, theta_u)) and jumps by +-1 on a slip.
    """
    theta = np.full(m, np.arcsin(r))
    theta_u = np.pi - np.arcsin(r)
    k0 = np.floor((theta - theta_u) / (2 * np.pi)).astype(np.int64)
    trace = [] if trace_stride else None
    chunk = 4096
    done = 0
    while done < n_steps:
        nb = min(chunk, n_steps - done)
        # white_noise: var = psd*fs/2 = (4D)*(1/dtau)/2 = 2D/dtau  ->
        # increment n_k*dtau has variance 2*D*dtau  (convention B)  [checked]
        nz = white_noise(nb * m, 4.0 * d_dimless, 1.0 / dtau, rng).reshape(nb, m)
        for i in range(nb):
            theta += (r - np.sin(theta) + nz[i]) * dtau
            if trace_stride and (done + i) % trace_stride == 0:
                trace.append(theta[0])
        done += nb
    k1 = np.floor((theta - theta_u) / (2 * np.pi)).astype(np.int64)
    slips = int(np.sum(k1 - k0))
    tr = np.asarray(trace) if trace_stride else None
    return slips, tr


# ---------------------------------------------------------------------------
def main():
    t_start = time.time()
    print("[lab_36] lock acquisition transient + noise-induced cycle slips ...")

    # =====================================================================
    # Part 1 — acquisition time vs r = Dw/omega_L (deterministic)
    # =====================================================================
    EPS = 0.01                                     # settle threshold [rad]
    r_arr = np.array([0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80,
                      0.90, 0.95, 0.98, 0.99])
    T_ode = acquisition_sweep(r_arr, eps=EPS)
    T_ex = np.array([acquisition_exact(r, eps=EPS) for r in r_arr])
    ratio = T_ode / T_ex
    wc_arr = np.sqrt(1.0 - r_arr ** 2)

    print("  --- Part 1: acquisition (theta0=0, settle to theta_ss-0.01 rad) ---")
    print(f"  T_ode/T_exact ratio      : min {ratio.min():.4f}, max {ratio.max():.4f}")
    print(f"  omegaL*T_acq  r=0.50     : {T_ode[r_arr == 0.50][0]:.3f}")
    print(f"  omegaL*T_acq  r=0.90     : {T_ode[r_arr == 0.90][0]:.3f}")
    print(f"  omegaL*T_acq  r=0.99     : {T_ode[r_arr == 0.99][0]:.3f}")
    print(f"  omega_c*T_acq range      : {np.min(wc_arr*T_ode):.2f} .. "
          f"{np.max(wc_arr*T_ode):.2f}  (T itself spans "
          f"{T_ode.min():.2f} .. {T_ode.max():.2f} -> divergence is 1/omega_c)")

    # closed-form trajectory check at r = 0.8
    r_chk = 0.8
    tau_chk = np.arange(0.0, 15.0, 0.002)
    th_num = np.zeros_like(tau_chk)
    th = 0.0
    fscal = lambda x: r_chk - np.sin(x)
    for i in range(1, tau_chk.size):
        h = tau_chk[i] - tau_chk[i - 1]
        k1 = fscal(th); k2 = fscal(th + 0.5 * h * k1)
        k3 = fscal(th + 0.5 * h * k2); k4 = fscal(th + h * k3)
        th += (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        th_num[i] = th
    dev = np.max(np.abs(th_num - theta_exact(r_chk, tau_chk)))
    print(f"  closed-form check r=0.8  : max|theta_ODE - theta_exact| = {dev:.2e} rad")

    # real units (f_L = 5 MHz)
    T_r05 = T_ode[r_arr == 0.50][0] / OMEGA_L
    T_r099 = T_ode[r_arr == 0.99][0] / OMEGA_L
    print(f"  real units (f_L=5 MHz)   : T_acq(r=0.5)  = {T_r05*1e9:.1f} ns "
          f"(= {T_r05*F0:.0f} carrier cycles @5 GHz)")
    print(f"                             T_acq(r=0.99) = {T_r099*1e9:.1f} ns "
          f"(= {T_r099*F0:.0f} carrier cycles)")

    # =====================================================================
    # Part 2 — noise-induced cycle slips at r = 0.8
    # =====================================================================
    R_SLIP = 0.8
    DU = barrier(R_SLIP)                            # dU/omega_L
    WC = np.sqrt(1.0 - R_SLIP ** 2)                 # omega_c/omega_L = 0.6
    PREF = WC / (2 * np.pi)                         # Kramers prefactor / omega_L
    print("  --- Part 2: cycle slips at r = 0.8 (Euler-Maruyama, 512 walkers) ---")
    print(f"  barrier dU/omega_L       : {DU:.4f}   (2*(sqrt(1-r^2)-r*acos r), r=0.8)")
    print(f"  Kramers prefactor/omegaL : {PREF:.4f}   (= omega_c/2pi, omega_c=0.6*omega_L)")

    M = 512
    NSTEPS = 600_000
    DTAU = 0.02
    tau_per = NSTEPS * DTAU                          # 12000 per walker
    x_list = np.array([4.0, 5.0, 6.0, 7.0, 8.0, 9.0])   # dU/D
    d_list = DU / x_list
    counts = []
    trace = None
    for x, d in zip(x_list, d_list):
        stride = 100 if x == 5.0 else 0
        s, tr = slip_run(R_SLIP, d, M, NSTEPS, DTAU, RNG, trace_stride=stride)
        if tr is not None:
            trace = tr
        counts.append(s)
        nu = s / (M * tau_per)
        nu_k = PREF * np.exp(-x)
        print(f"    dU/D = {x:.0f} : slips = {s:6d}  ->  nu/omega_L = {nu:.3e}"
              f"   (Kramers {nu_k:.3e}, ratio {nu / nu_k:.2f})")
    counts = np.array(counts, dtype=float)
    nu_meas = counts / (M * tau_per)

    # weighted fit of ln(nu) vs 1/D  (Poisson weights: sigma_ln = 1/sqrt(N))
    inv_d = 1.0 / d_list
    coef = np.polyfit(inv_d, np.log(nu_meas), 1, w=np.sqrt(counts))
    dU_fit = -coef[0]
    A_fit = np.exp(coef[1])
    print(f"  fitted slope  -> dU_fit/omega_L = {dU_fit:.4f}  "
          f"(theory {DU:.4f}, ratio {dU_fit / DU:.3f})")
    print(f"  fitted prefactor/omega_L        = {A_fit:.4f}  "
          f"(Kramers omega_c/2pi = {PREF:.4f}, ratio {A_fit / PREF:.2f})")

    # Euler step-size honesty check at dU/D = 6 (same tau span, half step)
    s_half, _ = slip_run(R_SLIP, DU / 6.0, 256, 1_200_000, 0.01, RNG)
    nu_half = s_half / (256 * 12000.0)
    nu_ref = nu_meas[x_list == 6.0][0]
    print(f"  dt-halving check @dU/D=6 : nu(dtau=0.01)/nu(dtau=0.02) = "
          f"{nu_half / nu_ref:.3f}  (1 = no step-size bias)")

    # =====================================================================
    # Part 3 — map back to real units (canonical numbers)
    # =====================================================================
    print("  --- Part 3: real units, f_L = 5 MHz, r = 0.8 ---")
    dU_real = DU * OMEGA_L                          # [rad^2/s] (rad dimensionless)
    print(f"  dU = {DU:.4f}*omega_L = {dU_real:.3e} rad^2/s")
    for name, dd in [("true-LC   D=S_n/4=0.125", D_TRUE_LC),
                     ("representative  D=0.0625", D_REPR)]:
        expo = dU_real / dd
        log10nu = np.log10(OMEGA_L * PREF) - expo * np.log10(np.e)
        print(f"    {name} rad^2/s : dU/D = {expo:.3e} -> "
              f"log10(nu[1/s]) = {log10nu:.3e}  (never happens)")

    # r* where nu = 1/s (exact barrier, Kramers rate, brentq)
    def log_nu_real(r, d):
        wc = OMEGA_L * np.sqrt(1.0 - r ** 2)
        return np.log(wc / (2 * np.pi)) - barrier(r) * OMEGA_L / d

    for name, dd in [("true-LC  D=0.125", D_TRUE_LC),
                     ("repr     D=0.0625", D_REPR)]:
        rstar = brentq(lambda r: log_nu_real(r, dd), 0.99, 1.0 - 1e-12,
                       xtol=1e-14)
        fc_star = F_LOCK * np.sqrt(1.0 - rstar ** 2)
        print(f"    nu = 1/s at {name}: 1-r* = {1.0 - rstar:.3e}  "
              f"(r* = {rstar:.8f}, remaining shaping corner f_c = "
              f"{fc_star/1e3:.1f} kHz)")

    # =====================================================================
    # Figure (2 panels + inset)
    # =====================================================================
    fig, axes = plt.subplots(1, 2, figsize=(13.5, 5.2))

    # ---- (a) acquisition time vs r --------------------------------------
    ax = axes[0]
    r_dense = np.linspace(0.02, 0.998, 400)
    T_dense = np.array([acquisition_exact(r, eps=EPS) for r in r_dense])
    ax.semilogy(r_dense, T_dense, color="tab:blue", lw=1.8,
                label="精確閉式解（分離變數）")
    ax.semilogy(r_arr, T_ode, "o", color="tab:red", ms=6, mfc="none", mew=1.6,
                label="RK4 數值積分（量測）")
    # 1/omega_c critical-slowing reference, anchored at r = 0.99
    C99 = T_ex[r_arr == 0.99][0] * np.sqrt(1 - 0.99 ** 2)
    ax.semilogy(r_dense, C99 / np.sqrt(1 - r_dense ** 2), "--", color="0.45",
                lw=1.4, label=r"臨界慢化 $\propto 1/\omega_c=1/\sqrt{\omega_L^2-\Delta\omega^2}$")
    ax.set_xlabel(r"失諧比 $r=\Delta\omega/\omega_L$")
    ax.set_ylabel(r"捕獲時間 $\omega_L\,T_{acq}$（無因次）")
    ax.set_title("(a) 鎖定捕獲：settle 率＝pull-in 頻率 $\\omega_c$（[P3] Eq.(40)）\n"
                 r"鎖定邊緣 $r\to1$：$\omega_c\to0$，捕獲時間發散（臨界慢化）")
    ax.set_xlim(0, 1.02)
    ax.legend(loc="upper left", fontsize=9)

    # ---- (b) slip rate vs dU/D ------------------------------------------
    ax = axes[1]
    ax.errorbar(x_list, nu_meas, yerr=nu_meas / np.sqrt(counts), fmt="o",
                color="tab:red", ms=6, capsize=3, label="模擬（512 walkers，Poisson 誤差棒）")
    xg = np.linspace(3.6, 9.4, 100)
    ax.semilogy(xg, PREF * np.exp(-xg), "--", color="tab:blue", lw=1.6,
                label=r"Kramers $(\omega_c/2\pi)e^{-\Delta U/D}$（外部文獻）")
    ax.semilogy(xg, A_fit * np.exp(-(dU_fit / DU) * xg), ":", color="0.3", lw=1.6,
                label=f"擬合直線：斜率 = {dU_fit / DU:.3f} × 理論障壁 $\\Delta U$")
    ax.set_yscale("log")
    ax.set_xlabel(r"障壁／雜訊比 $\Delta U/D$（$D$＝慣例乙擴散常數）")
    ax.set_ylabel(r"cycle-slip 率 $\nu/\omega_L$（每單位 $\omega_L t$）")
    ax.set_title("(b) 雜訊誘發 cycle slips（$r=0.8$，$\\Delta U=0.1704\\,\\omega_L$）\n"
                 r"log-linear 直線＝Arrhenius 型 $e^{-\Delta U/D}$；斜率＝障壁高度")
    ax.legend(loc="upper right", fontsize=9)

    # inset: one walker's staircase at dU/D = 5
    if trace is not None:
        axin = ax.inset_axes([0.13, 0.10, 0.40, 0.34])
        tau_tr = np.arange(trace.size) * 100 * DTAU
        axin.plot(tau_tr, trace / (2 * np.pi), color="tab:purple", lw=0.9)
        axin.set_xlabel(r"$\omega_L t$", fontsize=8)
        axin.set_ylabel(r"$\theta/2\pi$", fontsize=8)
        axin.set_title(r"單一 walker（$\Delta U/D=5$）：階梯＝slips", fontsize=8)
        axin.tick_params(labelsize=7)
        axin.grid(alpha=0.3)

    fig.suptitle("鎖定捕獲暫態與 noise-induced cycle slips：同一條 Adler 方程、同一個根號 "
                 r"$\omega_c=\sqrt{\omega_L^2-\Delta\omega^2}$"
                 "（[P3] Eq.(38)–(40)；[P4] Eq.(31)–(32)；Kramers＝外部文獻）",
                 fontsize=11)
    savefig(fig, "lock_acquisition.png")

    print(f"  runtime: {time.time() - t_start:.1f} s")


if __name__ == "__main__":
    main()
