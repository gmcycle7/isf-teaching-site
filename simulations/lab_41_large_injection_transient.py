"""
lab_41_large_injection_transient.py

Goal
----
Numerically back the [P4] deep-dive page "large-injection LC model and transient
behaviour" (docs/05_paper_deep_dives/paper_004_large_injection_transient.md):

  * [P4] Eq.(31)-(32), p.2130 : exact pull-in transient (tan half-angle / tanh)
                                 and the Pythagorean pull-in frequency
                                 omega_p = N*sqrt(omega_L^2 - Dw^2)   (N = 1 here)
  * [P4] Eq.(33)-(34), p.2130 : exact pulled (quasi-lock) transient (tan / tan)
                                 and the beat frequency
                                 omega_b = N*sqrt(Dw^2 - omega_L^2)
  * [P4] Eq.(27), p.2128      : ideal-LC amplitude-augmented Adler equation
                                 (ISF/(1+A) with the APF-driven amplitude A)
  * [P4] Eq.(9)/(23)          : large-injection lock range omega_L0/sqrt(1-a^2)
  * [P4] Table I footnote     : pull-in time from the SLOPE of the augmented
                                 lock characteristic instead of Eq.(32)
  * [P4] p.2131 (text)        : amplitude-conscious v_osc ~ [1+A(t)] cos[w_inj t + theta(t)]
                                 for the pulled spectrum (Fig. 14(c) idea)

Site conventions (same as injection_locking_noise / lab_36)
-----------------------------------------------------------
    dtheta/dt = Dw - omega_L0 * sin(theta)                      (ISF only)
    dtheta/dt = Dw - omega_L0 * sin(theta) / (1 + A)            (augmented, [P4] Eq.(27))
    A_qs(theta) = a * cos(theta),   a := I_inj/I_osc = (1/2) tau0 I_inj / q_max0
    tau0 * dA/dt = A_qs(theta) - A                              (site extension: first-order
                                                                 lag implied by [P4] Eq.(18)-(19)
                                                                 with d = exp(-t/tau0))
with Dw = omega_0 - omega_inj (site sign; [P4] uses omega_inj/N - omega_0),
omega_L0 = I_inj/(2 q_max0), tau0 = 2Q/omega_0, and the identity
tau0*omega_L0 = a (exact, using omega_0 q_max0 = Q I_osc, [P3] Eq.(22)).

Everything is integrated in dimensionless time tau = omega_L0 * t; the ideal-LC
dynamics depend only on r0 = Dw/omega_L0 and a. Real units are restored with the
site canonical numbers f0 = 5 GHz, q_max = 1 pC, Q = 10, I_inj = 1.5 mA.

Figure
------
  static/figures/large_injection_transient.png   (2 x 2 panels)

Run
---
  PYTHONPATH=<project root> python simulations/lab_41_large_injection_transient.py
"""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq

from plot_utils import savefig

# ---------------------------------------------------------------------------
# canonical real-unit anchors (site spec section 8; Q = 10 per tank_Q page)
# ---------------------------------------------------------------------------
F0 = 5.0e9                          # [Hz]
W0 = 2.0 * np.pi * F0               # [rad/s]
QMAX = 1.0e-12                      # [C]  free-running charge swing q_max0
Q = 10.0                            # tank quality factor
I_INJ = 1.5e-3                      # [A]  "large" injection amplitude (peak)

I_MAX = W0 * QMAX                   # [A]  [P3] Eq.(36)/[P4] fn.11 : oscillation current
I_OSC = I_MAX / Q                   # [A]  [P4] p.2132 : I_osc = I_max/Q  (= omega0 qmax/Q)
A_STR = I_INJ / I_OSC               # a = I_inj/I_osc = (1/2) tau0 I_inj/qmax0 (dimensionless)
WL0 = I_INJ / (2.0 * QMAX)          # [rad/s] ISF-only half lock range ([P3] Eq.(35))
TAU0 = 2.0 * Q / W0                 # [s]  amplitude decay time constant ([P4] Sec. II-B / III-F)
WL_APF = WL0 / np.sqrt(1.0 - A_STR ** 2)   # [rad/s] [P4] Eq.(9) == Eq.(23) at beta = 90 deg
T_UNIT = 1.0 / WL0                  # [s] one dimensionless time unit


# ---------------------------------------------------------------------------
# generic RK4 (vector state), fixed step, returns full trajectory
# ---------------------------------------------------------------------------
def rk4(f, y0, dt, n):
    y = np.array(y0, dtype=float)
    out = np.empty((n + 1, y.size))
    out[0] = y
    for k in range(n):
        k1 = f(y)
        k2 = f(y + 0.5 * dt * k1)
        k3 = f(y + 0.5 * dt * k2)
        k4 = f(y + dt * k3)
        y = y + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        out[k + 1] = y
    return out


# ---------------------------------------------------------------------------
# models (dimensionless tau = omega_L0 t)
# ---------------------------------------------------------------------------
def rhs_isf(r0):
    return lambda y: np.array([r0 - np.sin(y[0])])


def rhs_apf_qs(r0, a):
    return lambda y: np.array([r0 - np.sin(y[0]) / (1.0 + a * np.cos(y[0]))])


def rhs_apf_lag(r0, a):
    # y = [theta, A];  tau0*omega_L0 = a  =>  dA/dtau = (a cos(theta) - A)/a
    def f(y):
        th, A = y
        return np.array([r0 - np.sin(th) / (1.0 + A), (a * np.cos(th) - A) / a])
    return f


def locked_phase_apf(r0, a):
    """stable locked phase of the augmented model: sin(th)/(1+a cos th) = r0,
    on the branch cos(th) + a > 0 (negative lock-characteristic slope)."""
    g = lambda th: np.sin(th) / (1.0 + a * np.cos(th)) - r0
    th_max = np.arccos(-a)             # where g' = 0 (peak of the characteristic)
    return brentq(g, -th_max, th_max)


def pullin_apf(th0, a):
    """omega_p/omega_L0 = -Omega'(theta_0) for the augmented characteristic
    (the [P4] Table I footnote recipe: slope of the theoretical lock characteristic)."""
    c = np.cos(th0)
    return (c + a) / (1.0 + a * c) ** 2


def fit_decay_rate(tau, dev, lo=1e-3, hi=1e-1):
    """slope of ln|dev| over the window lo < |dev| < hi (like [P4] Fig. 13 fits)."""
    m = (np.abs(dev) > lo) & (np.abs(dev) < hi)
    p = np.polyfit(tau[m], np.log(np.abs(dev[m])), 1)
    return -p[0]


def main():
    t_start = time.time()
    a = A_STR
    print("[lab_41] large-injection LC model + transients ([P4] Sec. III-E/F, V)")
    print(f"  canonical: f0 = {F0/1e9:.0f} GHz, qmax = {QMAX*1e12:.0f} pC, Q = {Q:.0f}, "
          f"I_inj = {I_INJ*1e3:.1f} mA")
    print(f"  I_max = w0*qmax = {I_MAX*1e3:.2f} mA ; I_osc = I_max/Q = {I_OSC*1e3:.4f} mA ; "
          f"I_inj/I_max = {I_INJ/I_MAX:.4f}")
    print(f"  a = I_inj/I_osc = {a:.4f}   (injection strength that matters for LC)")
    print(f"  omega_L0 = I_inj/(2 qmax) = {WL0:.4e} rad/s  ->  f_L0 = {WL0/2/np.pi/1e6:.2f} MHz")
    print(f"  omega_L  = omega_L0/sqrt(1-a^2) = {WL_APF:.4e} rad/s  ->  f_L = "
          f"{WL_APF/2/np.pi/1e6:.2f} MHz  (ratio {WL_APF/WL0:.4f})")
    print(f"  tau0 = 2Q/w0 = {TAU0*1e9:.4f} ns = {TAU0*F0:.2f} cycles ; tau0*omega_L0 = {TAU0*WL0:.4f} (= a)")

    # numerical lock edge of the augmented characteristic
    th = np.linspace(-np.pi, np.pi, 200001)
    char = np.sin(th) / (1.0 + a * np.cos(th))
    edge_num = char.max()
    print(f"  edge check: max_theta sin/(1+a cos) = {edge_num:.5f} vs 1/sqrt(1-a^2) = "
          f"{1/np.sqrt(1-a**2):.5f}  (ratio {edge_num*np.sqrt(1-a**2):.5f})")
    a_big = 1.2
    th110 = th[np.abs(th) <= np.deg2rad(110.0)]
    char_big = np.sin(th110) / (1.0 + a_big * np.cos(th110))
    print(f"  a = {a_big}: characteristic unbounded (1 + a cos = 0 at "
          f"{np.rad2deg(np.arccos(-1/a_big)):.1f} deg); max over |theta|<=110 deg = "
          f"{char_big.max():.3f} omega_L0  ([P4] p.2127 empirical restriction)")

    # ------------------------------------------------------------------
    # (a) pull-in: ISF-only exact Eq.(31) vs RK4 ; augmented RK4 vs slope formula
    # ------------------------------------------------------------------
    r0 = 0.5                                     # Dw = 0.5 omega_L0
    dtau, n = 0.002, 12000                       # tau_max = 24
    tau = dtau * np.arange(n + 1)
    th_isf = rk4(rhs_isf(r0), [0.0], dtau, n)[:, 0]
    th_ss = np.arcsin(r0)                        # ISF-only locked phase
    wp_isf = np.sqrt(1.0 - r0 ** 2)              # [P4] Eq.(32), N = 1, units omega_L0

    # exact [P4] Eq.(31) in site variables: psi = theta + pi/2 (ideal LC, ang G1 = 90 deg)
    psi0 = th_ss + np.pi / 2.0
    alpha = np.tan(psi0 / 2.0)                   # tan(N theta~_0 / 2)
    x0 = np.tan((0.0 + np.pi / 2.0) / 2.0) / alpha
    phi0 = 2.0 * np.arctanh(x0)
    th_exact = 2.0 * np.arctan(alpha * np.tanh((wp_isf * tau + phi0) / 2.0)) - np.pi / 2.0
    dev_exact = np.max(np.abs(th_exact - th_isf))
    print(f"\n  (a) pull-in, r0 = Dw/omega_L0 = {r0}")
    print(f"      Eq.(31) closed form vs RK4: max |diff| = {dev_exact:.2e} rad")

    # lock time closed form from Eq.(31) (site threshold theta_ss - eps, eps = 0.01 rad)
    eps = 0.01
    x_thr = np.tan((psi0 - eps) / 2.0) / alpha
    T_lock = (2.0 / wp_isf) * (np.arctanh(x_thr) - np.arctanh(x0))
    k_thr = np.argmax(th_isf >= th_ss - eps)
    T_meas = tau[k_thr - 1] + dtau * (th_ss - eps - th_isf[k_thr - 1]) / (th_isf[k_thr] - th_isf[k_thr - 1])
    print(f"      lock time omega_L0*T (theta0 = 0 -> theta_ss - 0.01): closed form {T_lock:.3f} "
          f"vs RK4 {T_meas:.3f}  (lab_36 quotes 4.435)")

    # augmented model at the same Dw
    th0_apf = locked_phase_apf(r0, a)
    wp_apf = pullin_apf(th0_apf, a)
    y_apf = rk4(rhs_apf_qs(r0, a), [0.0], dtau, n)[:, 0]
    rate_isf = fit_decay_rate(tau, th_isf - th_ss)
    rate_apf = fit_decay_rate(tau, y_apf - th0_apf)
    print(f"      ISF-only : theta_ss = {np.rad2deg(th_ss):.2f} deg, omega_p/omega_L0 = "
          f"{wp_isf:.4f} (Eq.32) ; fitted decay {rate_isf:.4f} (ratio {rate_isf/wp_isf:.4f})")
    print(f"      augmented: theta_0 = {np.rad2deg(th0_apf):.2f} deg, omega_p/omega_L0 = "
          f"{wp_apf:.4f} (slope of augmented characteristic) ; fitted decay {rate_apf:.4f} "
          f"(ratio {rate_apf/wp_apf:.4f})")
    print(f"      amplitude at lock: 1 + a cos(theta_0) = {1 + a*np.cos(th0_apf):.4f} (stable = larger)")
    # centre-of-lock-range slowdown factor
    wp_c_isf = 1.0
    wp_c_apf = pullin_apf(0.0, a)
    print(f"      Dw = 0: tau_p(APF)/tau_p(ISF) = {wp_c_isf/wp_c_apf:.4f}  (= 1 + a = {1+a:.4f})")
    print(f"      real units: tau_p(ISF, Dw=0) = {T_UNIT*1e9:.3f} ns ; tau_p(APF, Dw=0) = "
          f"{T_UNIT/wp_c_apf*1e9:.3f} ns = {T_UNIT/wp_c_apf*F0:.1f} cycles")

    # [P4] Table I / Fig. 13(c) reconstruction from Fig. 8 caption numbers (estimate!)
    Qp, f0p, Iosc_p, Iinj_p = 15.0, 1.0e9, (4.0 / np.pi) * 1e-3, 0.5e-3
    a_p = Iinj_p / 1.25e-3                       # a = I_inj |Delta_1| / 2 = 0.5/1.25
    qmax_p = Qp * Iosc_p / (2 * np.pi * f0p)     # omega0 qmax0 = Q I_osc
    wl0_p = Iinj_p / (2 * qmax_p)
    tp_isf_cycles = f0p / wl0_p                  # tau_p/T_inj at Dw = 0 (ISF only)
    tp_apf_cycles = tp_isf_cycles * (1 + a_p)
    print(f"      Table I(c) reconstruction: qmax0 = {qmax_p*1e12:.2f} pC, a = {a_p:.2f}, "
          f"tau_p/T_inj: ISF-only {tp_isf_cycles:.1f} -> x(1+a) = {tp_apf_cycles:.1f} "
          f"(paper: 17.4*, simulated 16.9)")

    # ------------------------------------------------------------------
    # (b) amplitude transient during acquisition: quasi-static vs lagged
    # ------------------------------------------------------------------
    th_init = -2.0
    nb = 12000
    taub = dtau * np.arange(nb + 1)
    y_qs = rk4(rhs_apf_qs(r0, a), [th_init], dtau, nb)[:, 0]
    A_qs = a * np.cos(y_qs)
    y_lag = rk4(rhs_apf_lag(r0, a), [th_init, 0.0], dtau, nb)     # A(0) = 0: injection switched on
    th_lag, A_lag = y_lag[:, 0], y_lag[:, 1]
    A_final = a * np.cos(th0_apf)
    print(f"\n  (b) amplitude transient, r0 = {r0}, theta(0) = {th_init} rad, A(0) = 0")
    print(f"      quasi-static: A_min = {A_qs.min():+.4f}, A_max = {A_qs.max():+.4f} at omega_L0 t = "
          f"{taub[np.argmax(A_qs)]:.2f}, A_final = {A_final:+.4f}  (overshoot {A_qs.max()-A_final:.4f})")
    print(f"      lagged (tau0): A_min = {A_lag.min():+.4f}, A_max = {A_lag.max():+.4f} at omega_L0 t = "
          f"{taub[np.argmax(A_lag)]:.2f}, A_final = {A_lag[-1]:+.4f}")
    print(f"      adiabaticity omega_p*tau0 = a*omega_p/omega_L0 = {a*wp_apf:.3f} ; "
          f"lag of the amplitude peak = {(taub[np.argmax(A_lag)]-taub[np.argmax(A_qs)])*T_UNIT*1e9:.3f} ns")
    print(f"      phase settle (lagged vs quasi-static) at omega_L0 t = 24: "
          f"{th_lag[-1]:.5f} vs {y_qs[-1]:.5f} rad (locked {th0_apf:.5f})")

    # ------------------------------------------------------------------
    # (d) pulled: Eq.(33) vs RK4 ; beat frequencies ; AM-conscious spectrum
    # ------------------------------------------------------------------
    r0p = 2.0 * (WL_APF / WL0)                   # Dw = 2 omega_L (outside for both models)
    wb_isf = np.sqrt(r0p ** 2 - 1.0)             # [P4] Eq.(34), units omega_L0
    dtp, npn = 0.01, 2 ** 17
    taup = dtp * np.arange(npn + 1)
    th_p_isf = rk4(rhs_isf(r0p), [0.0], dtp, npn)[:, 0]
    th_p_apf = rk4(rhs_apf_qs(r0p, a), [0.0], dtp, npn)[:, 0]

    # exact Eq.(33) in site variables (psi = theta + pi/2, Dw_P4 = -r0p)
    b = np.sqrt((r0p + 1.0) / (r0p - 1.0))       # = (omega_b/N)/|omega_L + Dw_P4|
    z0 = np.arctan(np.tan(np.pi / 4.0) / b)      # psi(0) = pi/2
    z = (wb_isf * taup) / 2.0 + z0
    m = np.floor((z + np.pi / 2.0) / np.pi)
    zz = z - m * np.pi
    psi_exact = 2.0 * (np.arctan(b * np.tan(zz)) + m * np.pi)
    th_exact_p = psi_exact - np.pi / 2.0
    dev33 = np.max(np.abs(th_exact_p - th_p_isf))
    # measured beat frequency from the mean drift (theta advances 2 pi per beat)
    wb_meas_isf = (th_p_isf[-1] - th_p_isf[0]) / (taup[-1] - taup[0])
    wb_meas_apf = (th_p_apf[-1] - th_p_apf[0]) / (taup[-1] - taup[0])
    # site closed form for the augmented beat frequency
    S = np.sqrt((1 - a ** 2) * r0p ** 2 - 1.0)
    R2 = a ** 2 * r0p ** 2 + 1.0
    wb_apf_closed = R2 * S / (1.0 + a ** 2 * r0p * S)
    wb_apf_naive = np.sqrt(r0p ** 2 - (WL_APF / WL0) ** 2)   # Eq.(34) with Eq.(9)'s omega_L
    print(f"\n  (d) pulled, Dw = 2 omega_L (r0 = Dw/omega_L0 = {r0p:.4f})")
    print(f"      Eq.(33) closed form vs RK4 (ISF-only): max |diff| = {dev33:.2e} rad over "
          f"{taup[-1]*wb_isf/2/np.pi:.0f} beats")
    print(f"      ISF-only : omega_b/omega_L0 = {wb_isf:.4f} (Eq.34) ; measured drift {wb_meas_isf:.4f} "
          f"(ratio {wb_meas_isf/wb_isf:.4f})")
    print(f"      augmented: measured drift {wb_meas_apf:.4f} ; site closed form {wb_apf_closed:.4f} "
          f"(ratio {wb_meas_apf/wb_apf_closed:.4f}) ; naive Eq.(34) with Eq.(9) omega_L {wb_apf_naive:.4f} "
          f"(ratio {wb_meas_apf/wb_apf_naive:.4f})")
    print(f"      real units: f_b ISF-only = {wb_isf*WL0/2/np.pi/1e6:.1f} MHz ; augmented = "
          f"{wb_meas_apf*WL0/2/np.pi/1e6:.1f} MHz ; Df = {r0p*WL0/2/np.pi/1e6:.1f} MHz")

    # [P4] Table II reconstruction (17-stage ring, pure arithmetic)
    fL_a = np.sqrt(40.0 ** 2 - 30.6 ** 2)
    fL_b = np.sqrt(30.0 ** 2 - 6.6 ** 2)
    print(f"      Table II: f_L from Df, f_b : (a) 1.04 GHz inj: sqrt(40^2-30.6^2) = {fL_a:.1f} MHz ; "
          f"(b) 0.97 GHz inj: sqrt(30^2-6.6^2) = {fL_b:.1f} MHz -> Df - f_L = {30.0-fL_b:.1f} MHz "
          f"(paper: 'only 0.7 MHz below the lower edge')")

    # spectra of the complex envelope relative to omega_inj (lines at k*omega_b).
    # Exact Fourier coefficients over an integer number M of beats (theta advances
    # 2*pi per beat, so theta(t+T_b) = theta(t) + 2*pi exactly -> no leakage/scalloping).
    def fourier_lines(env, tau_, theta, ks, M=400):
        base = theta[0]
        t_cross = [tau_[0]]
        for m_ in range(1, M + 1):
            target = base + 2 * np.pi * m_
            i = int(np.argmax(theta >= target))
            t_cross.append(tau_[i - 1] + (target - theta[i - 1]) / (theta[i] - theta[i - 1]) * (tau_[i] - tau_[i - 1]))
        t0, t1 = t_cross[0], t_cross[-1]
        wb_ = 2 * np.pi * M / (t1 - t0)
        sel = (tau_ >= t0) & (tau_ <= t1)
        tt, ee = tau_[sel], env[sel]
        return {k: abs(np.trapezoid(ee * np.exp(-1j * k * wb_ * tt), tt) / (t1 - t0)) for k in ks}, wb_

    def spectrum_for_plot(env, dt_):
        w = np.hanning(env.size)
        X = np.fft.fft(env * w, n=4 * env.size)             # 4x zero padding: scalloping < 0.1 dB
        f = np.fft.fftfreq(4 * env.size, d=dt_) * 2 * np.pi  # [omega_L0 units]
        return f, np.abs(X)

    env_isf = np.exp(1j * th_p_isf)
    env_apf = (1.0 + a * np.cos(th_p_apf)) * np.exp(1j * th_p_apf)
    ks = [-2, -1, 0, 1, 2, 3]
    lv_i, wb_fi = fourier_lines(env_isf, taup, th_p_isf, ks)
    lv_a, wb_fa = fourier_lines(env_apf, taup, th_p_apf, ks)
    f_i, X_i = spectrum_for_plot(env_isf, dtp)
    f_a, X_a = spectrum_for_plot(env_apf, dtp)
    db = lambda x, ref: 20 * np.log10(max(x, 1e-300) / ref)
    print(f"      beat from crossings: ISF-only {wb_fi:.4f}, augmented {wb_fa:.4f} (omega_L0 units)")
    print("      comb lines relative to the main (k=1) line [dB], k = 0 (at f_inj), 2, 3, -1 (mirror):")
    print(f"        ISF-only : k0 {db(lv_i[0], lv_i[1]):+.2f}, k2 {db(lv_i[2], lv_i[1]):+.2f}, "
          f"k3 {db(lv_i[3], lv_i[1]):+.2f}, mirror {db(lv_i[-1], lv_i[1]):+.1f}")
    print(f"        ISF+APF  : k0 {db(lv_a[0], lv_a[1]):+.2f}, k2 {db(lv_a[2], lv_a[1]):+.2f}, "
          f"k3 {db(lv_a[3], lv_a[1]):+.2f}, mirror {db(lv_a[-1], lv_a[1]):+.1f}")
    geo = 1.0 / (r0p + wb_isf)                   # Armand geometric ratio omega_L/(Dw + omega_b)
    print(f"      ISF-only geometric ratio omega_L0/(Dw+omega_b) = {geo:.4f} -> per-line step "
          f"{20*np.log10(geo):+.2f} dB ; measured k2-k1 {db(lv_i[2], lv_i[1]):+.2f} dB, "
          f"k3-k2 {db(lv_i[3], lv_i[2]):+.2f} dB")
    print(f"      APF-added DC term a/2 = {a/2:.4f} -> k0 line (ISF+APF) / k0 line (ISF-only) = "
          f"{lv_a[0]/lv_i[0]:.3f} ; k2 ratio = {lv_a[2]/lv_i[2]:.3f}")
    # attribution: is the augmented model's mirror line from the AM factor or from theta(t) itself?
    lv_e, _ = fourier_lines(np.exp(1j * th_p_apf), taup, th_p_apf, ks)
    print(f"      augmented e^(j theta) alone (no AM factor): k0 {db(lv_e[0], lv_e[1]):+.2f}, "
          f"k2 {db(lv_e[2], lv_e[1]):+.2f}, mirror {db(lv_e[-1], lv_e[1]):+.1f} dB  "
          f"(mirror line comes from the non-Adler theta(t), not from the AM factor)")
    wb_meas_isf, wb_meas_apf = wb_fi, wb_fa

    # ------------------------------------------------------------------
    # figure
    # ------------------------------------------------------------------
    fig, ax = plt.subplots(2, 2, figsize=(12.5, 9.2))

    # (a) pull-in (semilog normalized deviation, like [P4] Fig. 13)
    axa = ax[0, 0]
    dev_i = np.abs(th_isf - th_ss) / abs(0.0 - th_ss)
    dev_a = np.abs(y_apf - th0_apf) / abs(0.0 - th0_apf)
    axa.semilogy(tau, dev_i, color="C0", lw=2, label=r"ISF-only RK4，$\Delta\omega=0.5\,\omega_{L0}$")
    axa.semilogy(tau[::400], np.abs(th_exact[::400] - th_ss) / th_ss, "o", ms=5, mfc="none",
                 color="C0", label="[P4] Eq.(31) 閉式（tanh）")
    axa.semilogy(tau, np.exp(-wp_isf * tau) * dev_i[0] * 1.0, "--", color="C0", lw=1,
                 label=r"$e^{-\omega_p t}$，$\omega_p=\sqrt{\omega_{L0}^2-\Delta\omega^2}$ (Eq.32)")
    axa.semilogy(tau, dev_a, color="C3", lw=2, label=rf"ISF+APF RK4（$a={a:.3f}$）")
    axa.semilogy(tau, np.exp(-wp_apf * tau) * dev_a[0], "--", color="C3", lw=1,
                 label=r"$e^{-\omega_p t}$，$\omega_p=-\Omega'(\theta_0)$（augmented 斜率）")
    axa.set_ylim(1e-6, 2)
    axa.set_xlim(0, 20)
    axa.set_xlabel(r"$\omega_{L0}\,t$（無因次時間）")
    axa.set_ylabel(r"$|\hat\theta(t)|/|\hat\theta(0)|$（歸一化相位偏差）")
    axa.set_title("(a) 鎖定捕獲：精確 tanh 解與 APF 修正的 pull-in 率")
    axa.legend(loc="lower left", fontsize=8)

    # (b) amplitude transient
    axb = ax[0, 1]
    tb_ns = taub * T_UNIT * 1e9
    axb.plot(tb_ns, 1 + A_qs, color="C1", lw=2, label=r"quasi-static：$1+a\cos\theta(t)$（[P4] Eq.20）")
    axb.plot(tb_ns, 1 + A_lag, color="C2", lw=2, label=r"一階遲滯：$\tau_0\dot A=a\cos\theta-A$（本站延伸）")
    axb.axhline(1 + A_final, color="k", ls=":", lw=1, label=r"鎖定振幅 $1+a\cos\theta_0$")
    axb.axhline(1.0, color="gray", ls="--", lw=1, label="自由跑振幅")
    axb2 = axb.twinx()
    axb2.plot(tb_ns, np.rad2deg(th_lag), color="C4", lw=1.2, alpha=0.8)
    axb2.set_ylabel(r"$\theta(t)$ [deg]（紫）")
    axb.set_xlabel("t [ns]（$f_0$=5 GHz、$I_{inj}$=1.5 mA、$Q$=10）")
    axb.set_ylabel(r"振幅 $V_{osc}/V_{osc,0}=1+A(t)$")
    axb.set_title(r"(b) 捕獲期間的振幅暫態：dip → overshoot → settle（$\theta(0)=-2$ rad）")
    axb.legend(loc="lower right", fontsize=8)
    axb.set_xlim(0, 20)

    # (c) lock characteristics
    axc = ax[1, 0]
    thd = np.rad2deg(th)
    for aa, col, lab in [(0.0, "C0", "ISF-only（Adler）"), (a, "C3", rf"ISF+APF，$a={a:.3f}$"),
                         (0.9, "C5", "ISF+APF，$a=0.9$")]:
        ch = np.sin(th) / (1 + aa * np.cos(th))
        stable = (np.cos(th) + aa) > 0
        axc.plot(thd, np.where(stable, ch, np.nan), color=col, lw=2, label=lab)
        axc.plot(thd, np.where(~stable, ch, np.nan), color=col, lw=1, ls="--")
        axc.axhline(1 / np.sqrt(1 - aa ** 2), color=col, ls=":", lw=1)
    chb = np.sin(th) / (1 + a_big * np.cos(th))
    chb[np.abs(th) > np.deg2rad(110)] = np.nan
    axc.plot(thd, chb, color="C7", lw=1.2, ls="-.", label=r"$a=1.2$（無界；只畫 $|\theta|\leq 110$ deg）")
    axc.set_ylim(-3.2, 3.2)
    axc.set_xlim(-180, 180)
    axc.set_xlabel(r"相對相位 $\theta$ [deg]")
    axc.set_ylabel(r"鎖定失諧 $\Delta\omega/\omega_{L0}=\sin\theta/(1+a\cos\theta)$")
    axc.set_title(r"(c) 大注入 lock characteristic：$\omega_L=\omega_{L0}/\sqrt{1-a^2}$（[P4] Eq.9/23）")
    axc.legend(loc="upper left", fontsize=8)

    # (d) pulled spectra
    axd = ax[1, 1]
    order = np.argsort(f_i)
    ref_i, ref_a = lv_i[1], lv_a[1]
    axd.plot(f_i[order] / wb_meas_isf, 20 * np.log10(X_i[order] / ref_i + 1e-12), color="C0", lw=1,
             label=r"ISF-only：$e^{j\theta}$，梳距 $\omega_b$（Eq.34）")
    axd.plot(f_a[order] / wb_meas_apf, 20 * np.log10(X_a[order] / ref_a + 1e-12), color="C3", lw=1,
             alpha=0.85, label=r"ISF+APF：$[1+a\cos\theta]e^{j\theta}$（[P4] p.2131 形式）")
    axd.set_xlim(-2.5, 4.5)
    axd.set_ylim(-70, 5)
    axd.set_xlabel(r"$(\omega-\omega_{inj})/\omega_b$（k=0 即注入頻率）")
    axd.set_ylabel("相對主線 (k=1) [dB]")
    axd.set_title(rf"(d) pulled 頻譜（$\Delta\omega=2\omega_L$）：APF 把 k=0 與 k=2 線抬高")
    axd.legend(loc="upper right", fontsize=8)

    fig.suptitle("lab_41：[P4] 大注入 LC 模型（ISF/(1+A)）的鎖定捕獲、振幅暫態與 pulling 頻譜", fontsize=13)
    savefig(fig, "large_injection_transient.png")
    print(f"\n  runtime {time.time()-t_start:.1f} s")


if __name__ == "__main__":
    main()
