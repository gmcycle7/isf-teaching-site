"""
lab_40_subharmonic_injection.py

Goal
----
Sub-harmonic (x N) injection locking with a PULSE train, i.e. the phase-domain
model of an injection-locked clock multiplier (ILCM): a reference at
f_ref = f0/N dumps a rectangular current pulse (charge q_inj, width tau_p)
into the oscillator once every T_inj = N*T0.  Everything is first order in
q_inj/q_max (the linear ISF theory of [P1]/[P3]); no amplitude dynamics.

Model (two engines, one theory)
-------------------------------
[P4] Eq.(28)-(29), p.2129, with (M, N)_[P4] = (N, 1) in our notation
(f_osc = N*f_inj, averaging window N*T0 = T_inj):

    dtheta/dt = (omega0 - N*omega_inj)
                + Gamma_tilde(N*omega_inj*t + theta) * i_inj(t)      (unaveraged)

  * ENGINE 1 - impulse-train MAP (first-order exact for an impulsive pulse):
        theta_{k+1} = theta_k + A + (q_inj/q_max)*Gbar(theta_k) + n_k,
        A   = Dw*T_inj                       [rad per period]
        Gbar = ISF averaged over the pulse   (rectangular window of width
               W = omega0*tau_p  <=>  k-th ISF harmonic x sinc(k*tau_p/T0)),
        n_k ~ N(0, kappa^2*T_inj)            white-FM noise, site convention
              Var[dphi(t)] = kappa^2*|t|, kappa^2 = 0.125 rad^2/s.
    Lock range (half):  omega_L = (q_inj/q_max)*max|Gbar| / T_inj
    Realignment factor: beta = -(q_inj/q_max)*Gbar'(theta*)   [dimensionless]
    Linear loop:        d(theta)_{k+1} = (1-beta) d(theta)_k + n_k
                        -> first-order discrete high-pass for the oscillator's
                           own noise, corner omega_c = beta/T_inj = beta*f_ref
  * ENGINE 2 - the UNAVERAGED time-synchronous ODE above, integrated with
    RK4 sub-steps through the finite-width pulse (free-run analytically in
    between) or, for a sinusoidal injection at f0/N, RK4 throughout.  It is
    used to test the map non-trivially (lock range vs N and vs tau_p, the
    realignment factor beta, and the "a pure sine at f0/N cannot lock to first
    order" statement).

Two site toy ISFs (dimensionless Gamma):
  * ideal LC        Gamma = -sin(theta)                (isf_utils.gamma_lc_ideal)
  * [P2] App.B ring  two opposite-sign triangles, height = half-width = 1/f',
                     f' = eta*N_st/pi (A = 1), eta = 0.75, N_st = 17
                     (same construction as lab_39; TOY, not transistor-level)

Experiments (all numbers printed with the page's `# ->` markers)
  (a) lock range vs N (2, 4, 8, 16, 20) at fixed q_inj    -> exponent -1
  (b) lock range vs pulse width tau_p at fixed q_inj      -> sinc(tau_p/T0)
      (= the N-th Fourier coefficient of the pulse train) for the LC ISF;
      for the ring ISF every k*N-th pulse harmonic weights the ISF's k-th
      harmonic, so the plain sinc is NOT enough (box-average is)
  (c) pure sinusoidal injection at f0/N with the SAME rms current: no lock
      anywhere inside the pulse-train lock range (first order)
  (d) realignment factor beta from the step response (ODE) vs the map's
      prediction -(q_inj/q_max)*Gbar'(theta*): ratio ~ 1 - beta/2 (second-
      order effect of the phase moving during the pulse; -> 1 as q_inj -> 0)
  (e) PSD of the locked phase vs free-run, discrete first-order transfer,
      corner beta*f_ref/(2*pi)
  (f) output jitter vs N at fixed beta (sqrt(N) growth) and reference-spur
      level at f_ref for a detuned lock (20*log10(Delta f/f_ref) dBc)

Canonical parameter set (shared with the subharmonic_injection page):
  f0 = 5 GHz (T0 = 200 ps normalized to 1), q_max = 1 pC, q_inj = 50 fC,
  tau_p = 10 ps, headline N = 20 (f_ref = 250 MHz, T_inj = 4 ns),
  kappa^2 = 0.125 rad^2/s -> per-cycle variance kappa^2*T0 = 2.5e-11 rad^2.

Figure
------
  static/figures/subharmonic_injection.png   (2 x 3 panels)

Run
---
  PYTHONPATH=<project root> python simulations/lab_40_subharmonic_injection.py
  (runtime ~40 s single core; seed default_rng(40))
"""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch
from scipy.optimize import brentq

from plot_utils import savefig
from isf_utils import gamma_lc_ideal

RNG = np.random.default_rng(40)
TWO_PI = 2.0 * np.pi

# ---------------------------------------------------------------------------
# Canonical parameters (real units) and the normalized mapping (T0 = 1)
# ---------------------------------------------------------------------------
F0 = 5.0e9                       # free-running frequency            [Hz]
T0 = 1.0 / F0                    # oscillation period = time unit    [s]
QMAX = 1.0e-12                   # q_max                             [C]
QINJ = 50.0e-15                  # charge per reference pulse        [C]
QT = QINJ / QMAX                 # q_inj/q_max (dimensionless)       = 0.05
TAUP = 10.0e-12                  # pulse width                       [s]
TP = TAUP / T0                   # tau_p/T0                          = 0.05
N_HEAD = 20                      # headline multiplication ratio
FREF = F0 / N_HEAD               # 250 MHz
TINJ = N_HEAD * T0               # 4 ns
KAPPA2 = 0.125                   # Var[dphi(t)] = KAPPA2*|t|  [rad^2/s]  (site
                                 # convention 甲; = 2*D_乙; S_n = 2*KAPPA2)
KAPPA2_N = KAPPA2 * T0           # per-cycle phase-increment variance [rad^2]
ETA, NST = 0.75, 17              # [P2] ring toy: eta, number of stages
FP_RING = ETA * NST / np.pi      # normalized transition slope f'  [1/rad]
H_RING = 1.0 / FP_RING           # triangle height = half-width [rad]


def gamma_ring(x):
    """[P2] App.B (A = 1) ring toy ISF, identical to lab_39's gamma_ring_p2:
    + triangle at pi/2 (rising edge), - triangle at 3pi/2 (falling edge),
    height = half-width = 1/f'.  Fast implementation: one wrap; the distance
    to the second (antipodal) centre is pi - |d1|."""
    d1 = np.abs(np.mod(x - np.pi / 2 + np.pi, TWO_PI) - np.pi)
    return H_RING * (np.clip(1.0 - d1 / H_RING, 0.0, None)
                     - np.clip(1.0 - (np.pi - d1) / H_RING, 0.0, None))


ISFS = {"LC": gamma_lc_ideal, "ring": gamma_ring}

# ---------------------------------------------------------------------------
# Pulse-averaged ISF tables:  Gbar(theta) = (1/W) int_{-W/2}^{W/2} Gamma(theta+x) dx
# In Fourier space the box multiplies harmonic k by sinc(k*tau_p/T0)  (numpy
# sinc = sin(pi x)/(pi x)); that is exactly the k*N-th Fourier coefficient of
# the rectangular pulse train relative to its impulse limit.
# ---------------------------------------------------------------------------
NG = 8192
XG = np.arange(NG) * TWO_PI / NG


def isf_tables(gamma_func, tp):
    g = gamma_func(XG)
    G = np.fft.rfft(g)
    k = np.arange(G.size)
    Gb = G * np.sinc(k * tp)
    gbar = np.fft.irfft(Gb, NG)
    gbar_p = np.fft.irfft(1j * k * Gb, NG)          # d Gbar / d theta
    return gbar, gbar_p


def pinterp(table, theta):
    """Periodic linear interpolation of a table sampled on XG."""
    x = np.mod(theta, TWO_PI) * (NG / TWO_PI)
    i0 = np.floor(x).astype(np.int64)
    f = x - i0
    i1 = (i0 + 1) % NG
    return table[i0] * (1.0 - f) + table[i1] * f


# ---------------------------------------------------------------------------
# ENGINE 2: one injection period of the UNAVERAGED ODE with a rectangular pulse
#   dtheta/dt = dw + Gamma(2*pi*t + theta) * (qt/tp)   during the pulse
#   (t in [-tp/2, tp/2], centred on the reference edge = grid instant),
#   dtheta/dt = dw                                       for the rest (analytic)
# theta is sampled just BEFORE each pulse.  All rates in rad per T0.
# ---------------------------------------------------------------------------
def pulse_period_step(theta, dw, n_div, qt, gamma_func, tp, nsub):
    h = tp / nsub
    amp = qt / tp
    t = -tp / 2.0
    for _ in range(nsub):
        k1 = dw + amp * gamma_func(TWO_PI * t + theta)
        k2 = dw + amp * gamma_func(TWO_PI * (t + 0.5 * h) + theta + 0.5 * h * k1)
        k3 = dw + amp * gamma_func(TWO_PI * (t + 0.5 * h) + theta + 0.5 * h * k2)
        k4 = dw + amp * gamma_func(TWO_PI * (t + h) + theta + h * k3)
        theta = theta + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        t += h
    return theta + dw * (n_div - tp)


def gbar_prime_exact(gamma_func, theta, tp):
    """Exact derivative of the pulse-averaged ISF: d/dtheta of the box average
    is the difference of the raw ISF at the two box ends over the box width
    W = 2*pi*tau_p/T0 (no Fourier ringing at the ring ISF's kinks)."""
    half_w = np.pi * tp
    return (gamma_func(theta + half_w) - gamma_func(theta - half_w)) / (2.0 * half_w)


def ode_jump_edges(gamma_func, tp, qt, name, n_th=4096):
    """
    Lock characteristic of the UNAVERAGED ODE measured directly: integrate one
    injection period from every pre-pulse phase theta on a fine grid and read
    the net phase correction J(theta) = theta_after - theta_before (Dw = 0).
    The oscillator can lock iff the per-period drift A = Dw*T_inj can be
    cancelled: A+ = -min J (oscillator fast), A- = max J (oscillator slow).
    """
    th = np.arange(n_th) * TWO_PI / n_th
    J = pulse_period_step(th, 0.0, N_HEAD, qt, gamma_func, tp,
                          nsub_for(tp, name)) - th
    return -J.min(), J.max()


def nsub_for(tp, name):
    """RK4 sub-steps through the pulse.  The ISF argument advances by
    2*pi*tau_p/T0 during the pulse; the smooth LC ISF is fine with <= 0.2 rad
    per sub-step, the kinked ring triangles need <= 0.05 rad (<= 0.08 rad for
    the widest pulses, where the pulse-averaged ISF is already very smooth):
    checked against a 512-sub-step reference, error <= 0.4 % / 0.85 %."""
    if name == "LC":
        return max(4, int(np.ceil(TWO_PI * tp / 0.2)))
    step = 0.05 if tp <= 0.25 else 0.08
    return max(4, int(np.ceil(TWO_PI * tp / step)))


# ---------------------------------------------------------------------------
# Lock-edge finder (works for the map and for the ODE period step)
# ---------------------------------------------------------------------------
def measure_edges(period_step, a_pred, theta_min, theta_max, n_periods=2500,
                  n_tail=800, tol=5e-3, span=0.03, n_grid=31):
    """
    Sweep the per-period drift A around the predicted edge a_pred (both signs)
    and return (A_edge_plus, A_edge_minus) as the midpoint between the last
    locked and first unlocked grid point.  'locked' = at least one initial
    phase shows |theta(end) - theta(end - n_tail)| < tol.
    Initial phases sit around the ISF extremum that carries the edge
    (theta_min for A > 0, theta_max for A < 0), offsets -0.3/0/+0.3 rad.
    """
    rel = np.linspace(1.0 - span, 1.0 + span, n_grid)
    offs = np.array([-0.3, 0.0, 0.3])
    a_plus = a_pred * rel
    a_minus = -a_pred * rel
    A = np.concatenate([a_plus, a_minus])[:, None]
    th0 = np.concatenate([np.full(n_grid, theta_min), np.full(n_grid, theta_max)])
    th = th0[:, None] + offs[None, :]
    th_mid = None
    for p in range(n_periods):
        if p == n_periods - n_tail:
            th_mid = th.copy()
        th = period_step(th, A)
    drift = np.abs(th - th_mid).min(axis=1)
    locked = drift < tol

    def edge(lk, grid):
        unl = np.where(~lk)[0]
        if unl.size == 0:
            return grid[-1], "all-locked"
        if unl[0] == 0:
            return grid[0], "none-locked"
        return 0.5 * (grid[unl[0] - 1] + grid[unl[0]]), "ok"

    ep, fp = edge(locked[:n_grid], a_plus)
    em, fm = edge(locked[n_grid:], -a_minus)
    return ep, em, fp, fm


# ---------------------------------------------------------------------------
def main():
    t_start = time.time()
    print("[lab_40] sub-harmonic (x N) pulse injection: impulse-train map vs "
          "unaveraged ODE ...")
    print(f"  canonical: f0 = {F0/1e9:.0f} GHz, q_max = {QMAX*1e12:.0f} pC, "
          f"q_inj = {QINJ*1e15:.0f} fC (q_inj/q_max = {QT:.2f}), tau_p = "
          f"{TAUP*1e12:.0f} ps (tau_p/T0 = {TP:.2f}), N = {N_HEAD} -> f_ref = "
          f"{FREF/1e6:.0f} MHz, T_inj = {TINJ*1e9:.0f} ns")
    print(f"  noise    : kappa^2 = {KAPPA2} rad^2/s (Var[dphi] = kappa^2|t|) -> "
          f"per cycle {KAPPA2_N:.3e} rad^2, per T_inj {KAPPA2*TINJ:.3e} rad^2; "
          f"S_n = 2 kappa^2 = {2*KAPPA2} rad^2/s")
    print(f"  ring toy : [P2] App.B A=1, eta = {ETA}, N_st = {NST}: f' = "
          f"{FP_RING:.4f} 1/rad, h = w = {H_RING:.4f}")

    # pulse-averaged tables for the canonical pulse
    tabs = {name: isf_tables(g, TP) for name, g in ISFS.items()}
    sinc0 = np.sinc(TP)
    err_lc = np.max(np.abs(tabs["LC"][0] - (-sinc0 * np.sin(XG))))
    print(f"  Gbar check (LC): max|table - (-sinc(tau_p/T0) sin)| = {err_lc:.1e}"
          f"   sinc(tau_p/T0) = {sinc0:.5f}")
    gmax = {name: float(np.max(np.abs(tabs[name][0]))) for name in ISFS}
    gmax_raw = {name: float(np.max(np.abs(ISFS[name](XG)))) for name in ISFS}
    th_min = {name: float(XG[np.argmin(tabs[name][0])]) for name in ISFS}
    th_max = {name: float(XG[np.argmax(tabs[name][0])]) for name in ISFS}
    slope_max = {name: float(np.max(-tabs[name][1])) for name in ISFS}
    for name in ISFS:
        print(f"  {name:4s}: max|Gamma| = {gmax_raw[name]:.4f} -> pulse-averaged "
              f"max|Gbar| = {gmax[name]:.4f}; max(-Gbar') = {slope_max[name]:.4f}")

    # headline predictions (N = 20)
    A_edge_pred = {name: QT * gmax[name] for name in ISFS}          # rad/period
    fL_pred = {name: A_edge_pred[name] / TINJ / TWO_PI for name in ISFS}
    beta_lc = QT * sinc0                                          # at Dw = 0
    I_N = 2 * QINJ / TINJ * np.sinc(N_HEAD * TAUP / TINJ)         # N-th harmonic
    I_rms = QINJ / np.sqrt(TAUP * TINJ)
    print(f"  N = 20 predictions: A_edge = q_t*max|Gbar| = {A_edge_pred['LC']:.5f} "
          f"rad/period (LC), {A_edge_pred['ring']:.5f} (ring)")
    print(f"    f_L(LC)   = {fL_pred['LC']/1e6:.4f} MHz  "
          f"[= (1/2) I_N |Gt_1|/2pi with I_N = 2 q_inj sinc(N tau_p/T_inj)/T_inj "
          f"= {I_N*1e6:.2f} uA]")
    print(f"    f_L(ring) = {fL_pred['ring']/1e6:.4f} MHz")
    print(f"    beta(LC, Dw=0) = q_t sinc = {beta_lc:.5f};  f_c = beta f_ref/2pi = "
          f"{beta_lc*FREF/TWO_PI/1e6:.4f} MHz;  I_rms(pulse) = {I_rms*1e6:.1f} uA; "
          f"I_max = w0 q_max = {TWO_PI*F0*QMAX*1e3:.1f} mA")

    # =====================================================================
    # (a) lock range vs N  (ENGINE 2, canonical pulse)
    # =====================================================================
    print("  --- (a) lock range vs N (unaveraged ODE, tau_p = 10 ps) ---")
    N_list = np.array([2, 4, 8, 16, 20])
    fL_meas = {name: [] for name in ISFS}
    asym = {name: [] for name in ISFS}
    t_a = time.time()
    for name, g in ISFS.items():
        nsub = nsub_for(TP, name)
        for n_div in N_list:
            step = lambda th, A, g=g, n=n_div, ns=nsub: pulse_period_step(
                th, A / n, n, QT, g, TP, ns)
            ep, em, fp, fm = measure_edges(step, A_edge_pred[name],
                                           th_min[name], th_max[name])
            wl = 0.5 * (ep + em) / (n_div * T0)                   # rad/s
            fL_meas[name].append(wl / TWO_PI)
            asym[name].append((ep - em) / (ep + em))
            flag = "" if (fp == "ok" and fm == "ok") else f"  [{fp}/{fm}]"
            print(f"    {name:4s} N={n_div:2d}: A+ = {ep:.5f}, A- = {em:.5f} rad/period "
                  f"(pred {A_edge_pred[name]:.5f}) -> f_L = {wl/TWO_PI/1e6:.4f} MHz"
                  f"{flag}")
        fL_meas[name] = np.array(fL_meas[name])
        asym[name] = np.array(asym[name])
    print(f"    edge asymmetry (A+ - A-)/(A+ + A-): LC {np.mean(asym['LC'])*100:+.2f} %, "
          f"ring {np.mean(asym['ring'])*100:+.2f} %  (second order in q_inj/q_max: the "
          f"phase moves during the pulse; first-order edges are symmetric)")
    print(f"    [(a) took {time.time()-t_a:.1f} s]")
    slope_N = {name: np.polyfit(np.log(N_list), np.log(fL_meas[name]), 1)[0]
               for name in ISFS}
    ratio_N = {name: fL_meas[name] / (A_edge_pred[name] / (N_list * T0) / TWO_PI)
               for name in ISFS}
    print(f"    fitted exponent d ln f_L / d ln N: LC {slope_N['LC']:.3f}, "
          f"ring {slope_N['ring']:.3f}   (expect -1)")
    print(f"    measured/theory f_L: LC {ratio_N['LC'].min():.4f}..{ratio_N['LC'].max():.4f}, "
          f"ring {ratio_N['ring'].min():.4f}..{ratio_N['ring'].max():.4f}")

    # =====================================================================
    # (b) lock range vs pulse width tau_p  (ENGINE 2, N = 20)
    # =====================================================================
    print("  --- (b) lock range vs pulse width (unaveraged ODE, N = 20) ---")
    tp_list = np.array([2, 10, 25, 50, 75, 100, 125, 150, 175]) * 1e-12 / T0
    fL_tp = {name: [] for name in ISFS}          # from the ODE lock characteristic J(theta)
    fL_td = {name: [] for name in ISFS}          # time-domain lock/unlock sweep (where beta allows)
    pred_tp = {name: [] for name in ISFS}
    asym_tp = {name: [] for name in ISFS}
    t_b = time.time()
    for name, g in ISFS.items():
        for tp in tp_list:
            gb, _ = isf_tables(g, tp)
            a_pred = QT * np.max(np.abs(gb))
            ap, am = ode_jump_edges(g, tp, QT, name)
            fL_tp[name].append(0.5 * (ap + am) / TINJ / TWO_PI)
            asym_tp[name].append((ap - am) / (ap + am))
            pred_tp[name].append(a_pred / TINJ / TWO_PI)
            # time-domain confirmation only where the realignment factor is
            # large enough for a 4000-period sweep to resolve the edge
            # (critical slowing near the edge scales as 1/(beta*sqrt(1-r)))
            beta_est = QT * np.max(np.abs(gbar_prime_exact(g, XG, tp)))
            if beta_est > 3e-3:
                thmin, thmax = XG[np.argmin(gb)], XG[np.argmax(gb)]
                ns = nsub_for(tp, name)
                step = lambda th, A, g=g, tp=tp, ns=ns: pulse_period_step(
                    th, A / N_HEAD, N_HEAD, QT, g, tp, ns)
                n_per = 2500 if beta_est > 0.02 else 4000
                ep, em, fp, fm = measure_edges(step, a_pred, thmin, thmax,
                                               n_periods=n_per, n_tail=n_per // 3)
                fL_td[name].append(0.5 * (ep + em) / TINJ / TWO_PI)
            else:
                fL_td[name].append(np.nan)
        for dct in (fL_tp, fL_td, pred_tp, asym_tp):
            dct[name] = np.array(dct[name])
    print(f"    [(b) took {time.time()-t_b:.1f} s]")
    fL0 = {name: QT * gmax_raw[name] / TINJ / TWO_PI for name in ISFS}   # impulse limit
    sinc_tp = np.sinc(tp_list)
    print("    tau_p [ps] | sinc=I_N/I_N(0) | LC ODE/f_L(0) [time-domain] | ring ODE/f_L(0) [time-domain] | ring box-avg/f_L(0) | ring ODE/box-avg")
    for i, tp in enumerate(tp_list):
        td_lc = f"{fL_td['LC'][i]/fL0['LC']:.4f}" if np.isfinite(fL_td['LC'][i]) else "  -   "
        td_rg = f"{fL_td['ring'][i]/fL0['ring']:.4f}" if np.isfinite(fL_td['ring'][i]) else "  -   "
        print(f"    {tp*T0*1e12:6.0f}     | {sinc_tp[i]:.4f}   | {fL_tp['LC'][i]/fL0['LC']:.4f} [{td_lc}]   | "
              f"{fL_tp['ring'][i]/fL0['ring']:.4f} [{td_rg}]   | {pred_tp['ring'][i]/fL0['ring']:.4f}   | "
              f"{fL_tp['ring'][i]/pred_tp['ring'][i]:.4f}")
    dev_lc_sinc = np.max(np.abs(fL_tp["LC"] / fL0["LC"] - sinc_tp))
    dev_ring_box = np.max(np.abs(fL_tp["ring"] / pred_tp["ring"] - 1.0))
    dev_ring_sinc = np.max(np.abs(fL_tp["ring"] / fL0["ring"] - sinc_tp))
    ok_td = {name: np.isfinite(fL_td[name]) for name in ISFS}
    dev_td = {name: np.max(np.abs(fL_td[name][ok_td[name]] / fL_tp[name][ok_td[name]] - 1.0))
              for name in ISFS}
    print(f"    LC: max|ODE/f_L(0) - sinc| = {dev_lc_sinc:.4f};  ring: max|ODE/box-avg - 1| "
          f"= {dev_ring_box:.4f}, but max|ODE/f_L(0) - sinc| = {dev_ring_sinc:.4f}")
    print(f"    time-domain sweep vs J(theta) edges: LC max dev {dev_td['LC']:.4f} "
          f"({ok_td['LC'].sum()} widths), ring {dev_td['ring']:.4f} ({ok_td['ring'].sum()} widths)")
    print(f"    ring edge asymmetry vs tau_p [%]: " +
          ", ".join(f"{a*100:+.2f}" for a in asym_tp['ring']))

    # =====================================================================
    # (c) pulse train vs pure sine at f0/N, same rms current (ENGINE 2, N = 20)
    # =====================================================================
    print("  --- (c) pulse train vs sinusoid at f0/N, equal I_rms (unaveraged ODE) ---")
    r_grid = np.linspace(-1.5, 1.5, 25)
    I_sine_n = np.sqrt(2.0) * QT / np.sqrt(TP * N_HEAD)   # peak, in q_max per T0
    print(f"    sine amplitude for equal rms: I_pk = {I_sine_n*QMAX/T0*1e6:.1f} uA "
          f"(I_rms = {I_rms*1e6:.1f} uA), I_pk/I_max = "
          f"{I_sine_n*QMAX/T0/(TWO_PI*F0*QMAX)*100:.2f} %")
    drift_pulse, drift_sine, dw_c, push_fit = {}, {}, {}, {}
    t_c = time.time()
    # second-order "pushing" by a sinusoid at omega_inj = omega0/N acting on the
    # LC ISF -sin (derived in the page): the injection-induced ripple d(theta)
    # multiplies Gamma' and averages to a constant frequency shift
    #   Dw_push = -(I/q_max)^2 * omega0 / (4 (omega0^2 - omega_inj^2))
    push_lc_n = -I_sine_n ** 2 * TWO_PI / (4 * (TWO_PI ** 2 - (TWO_PI / N_HEAD) ** 2))
    for name, g in ISFS.items():
        wl_n = A_edge_pred[name] / N_HEAD                      # rad per T0
        dw = r_grid * wl_n
        dw_c[name] = dw
        nsub = nsub_for(TP, name)
        # pulse train: start on the stable flank of the edge extremum
        th = np.where(dw >= 0, th_min[name] - 0.1, th_max[name] + 0.1)
        n_per = 4000
        th_mid = None
        for p in range(n_per):
            if p == n_per // 2:
                th_mid = th.copy()
            th = pulse_period_step(th, dw, N_HEAD, QT, g, TP, nsub)
        drift_pulse[name] = (th - th_mid) / (n_per // 2 * N_HEAD)   # rad per T0
        # sinusoid: RK4, dt = T0/40, T = 150 T_inj = 3000 T0
        dt = 1.0 / 40.0
        n_steps = 150 * N_HEAD * 40
        th = np.zeros_like(dw)
        rec = np.empty((n_steps // 40, dw.size))

        def f_sine(t, x):
            return dw + g(TWO_PI * t + x) * I_sine_n * np.cos(TWO_PI * t / N_HEAD)

        t = 0.0
        for k in range(n_steps):
            k1 = f_sine(t, th)
            k2 = f_sine(t + 0.5 * dt, th + 0.5 * dt * k1)
            k3 = f_sine(t + 0.5 * dt, th + 0.5 * dt * k2)
            k4 = f_sine(t + dt, th + dt * k3)
            th = th + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
            t += dt
            if (k + 1) % 40 == 0:
                rec[(k + 1) // 40 - 1] = th
        half = rec[rec.shape[0] // 2:]
        tt = np.arange(half.shape[0], dtype=float)
        tt -= tt.mean()
        drift_sine[name] = (tt[:, None] * (half - half.mean(axis=0))).sum(axis=0) \
            / (tt ** 2).sum()                                     # rad per T0
        inside = np.abs(r_grid) < 1.0
        n_lock_pulse = int(np.sum(np.abs(drift_pulse[name][inside]) < 1e-3 * wl_n))
        n_plateau_sine = int(np.sum(np.abs(drift_sine[name][inside]) < 1e-3 * wl_n))
        slope_s, off_s = np.polyfit(dw[inside], drift_sine[name][inside], 1)
        push_fit[name] = off_s
        print(f"    {name:4s}: pulse train locked at {n_lock_pulse}/{inside.sum()} points "
              f"inside |Dw| < omega_L; sine: {n_plateau_sine}/{inside.sum()} plateau points, "
              f"linear fit drift = {slope_s:.4f} Dw + ({off_s/wl_n:+.4f} omega_L)")
        far = np.abs(r_grid) >= 1.25
        beat_adler = np.sign(dw[far]) * np.sqrt(dw[far] ** 2 - wl_n ** 2)
        # general continuous-limit beat 2pi / int dtheta/(Dw + q_t Gbar/N)
        gb_tab = tabs[name][0]
        beat_gen = np.array([TWO_PI / np.sum(TWO_PI / NG / (d + QT * gb_tab / N_HEAD))
                             for d in dw[far]])
        print(f"          out-of-lock pulse drift / Adler sqrt(Dw^2-omega_L^2): median "
              f"{np.median(drift_pulse[name][far]/beat_adler):.3f};  / general "
              f"2pi/oint dtheta/(Dw+Omega): median {np.median(drift_pulse[name][far]/beat_gen):.3f}")
    print(f"    sine pushing (LC): fitted offset {push_fit['LC']/(A_edge_pred['LC']/N_HEAD):+.4f} "
          f"omega_L = {push_fit['LC']/T0/TWO_PI/1e3:+.1f} kHz vs analytic "
          f"-(I/q_max)^2 w0/(4(w0^2-w_inj^2)) = {push_lc_n/(A_edge_pred['LC']/N_HEAD):+.4f} omega_L "
          f"= {push_lc_n/T0/TWO_PI/1e3:+.1f} kHz (ratio {push_fit['LC']/push_lc_n:.3f}); "
          f"ring offset {push_fit['ring']/(A_edge_pred['ring']/N_HEAD):+.4f} omega_L,ring")
    print(f"    [(c) took {time.time()-t_c:.1f} s]")

    # =====================================================================
    # (d) realignment factor beta: ODE step response vs map prediction
    # =====================================================================
    print("  --- (d) realignment factor beta from the ODE step response (N = 20) ---")
    beta_rows = []
    DELTA = 0.005                                               # perturbation [rad]
    t_d = time.time()
    for name, g in ISFS.items():
        nsub_d = 8 if name == "LC" else 16
        r_list = (0.0, 0.5, 0.9) if name == "LC" else (0.3, 0.6, 0.9)
        qt_arr = np.array([QT] * 3 + [QT / 5.0] * 3)
        r_arr = np.array(r_list * 2)
        dw = r_arr * qt_arr * gmax[name] / N_HEAD               # rad per T0
        th = np.full(6, th_min[name] - 0.1)                     # stable flank side
        for _ in range(4500):
            th_prev = th
            th = pulse_period_step(th, dw, N_HEAD, qt_arr, g, TP, nsub_d)
        th_star = th.copy()
        conv = np.max(np.abs(th - th_prev))
        beta_map = -qt_arr * gbar_prime_exact(g, th_star, TP)
        th = th + DELTA                                         # perturb all
        rec = np.empty((800, 6))
        for k in range(800):
            th = pulse_period_step(th, dw, N_HEAD, qt_arr, g, TP, nsub_d)
            rec[k] = th
        d = rec - th_star[None, :]
        kk = np.arange(1, 801)
        for j in range(6):
            nfit = int(np.clip(1.0 / max(beta_map[j], 1e-4), 5, 400))
            slope = np.polyfit(kk[:nfit], np.log(np.abs(d[:nfit, j])), 1)[0]
            beta_ode = 1.0 - np.exp(slope)
            beta_exp = 1.0 - np.exp(-beta_map[j])
            beta_rows.append((qt_arr[j], name, r_arr[j], th_star[j], beta_map[j], beta_ode))
            print(f"    q_t={qt_arr[j]:.3f} {name:4s} r={r_arr[j]:.1f}: theta* = "
                  f"{np.mod(th_star[j], TWO_PI):.4f} rad, beta_ODE = {beta_ode:.5f}, "
                  f"map -q_t Gbar'(theta*) = {beta_map[j]:.5f} -> ratio {beta_ode/beta_map[j]:.4f}  "
                  f"(1-exp(-beta_map) = {beta_exp:.5f}, ratio {beta_ode/beta_exp:.4f})")
        print(f"      ({name}: max |theta change| in the last pre-perturbation period {conv:.1e} rad)")
    nsub_d = 16
    # ring at Dw = 0: the pulse lands in the ISF dead zone -> no restoring force
    th = np.array([np.pi])                                     # dead zone (Gamma = 0)
    for _ in range(200):
        th = pulse_period_step(th, 0.0, N_HEAD, QT, gamma_ring, TP, nsub_d)
    th_dz = float(th[0])
    th = th + DELTA
    for _ in range(400):
        th = pulse_period_step(th, 0.0, N_HEAD, QT, gamma_ring, TP, nsub_d)
    print(f"    ring, Dw = 0, pulse in the dead zone: perturbation {DELTA} rad after 400 periods = "
          f"{float(th[0]) - th_dz:.5f} rad -> beta = {1 - (float(th[0]) - th_dz)/DELTA:.1e} "
          f"(no realignment; the LC value would be {beta_lc:.4f})")
    print(f"    [(d) took {time.time()-t_d:.1f} s]")
    br = np.array([(row[0], row[4], row[5]) for row in beta_rows])
    sel05 = br[:, 0] == QT
    sel01 = br[:, 0] == QT / 5.0
    rat05 = br[sel05, 2] / br[sel05, 1]
    rat01 = br[sel01, 2] / br[sel01, 1]
    print(f"    ratio beta_ODE/beta_map: q_t=0.05 -> {rat05.min():.4f}..{rat05.max():.4f} "
          f"(LC centre: 1-beta/2 = {1-beta_lc/2:.4f}); q_t=0.01 -> {rat01.min():.4f}..{rat01.max():.4f}")
    rat_exp = br[:, 2] / (1.0 - np.exp(-br[:, 1]))
    print(f"    ratio beta_ODE/(1-exp(-beta_map)), all 12 cases: {rat_exp.min():.4f}.."
          f"{rat_exp.max():.4f}")
    print(f"    max |ratio - 1| : q_t=0.05 {np.max(np.abs(rat05-1)):.4f}, q_t=0.01 "
          f"{np.max(np.abs(rat01-1)):.4f}  (first-order theory: O(q_inj/q_max) accuracy)")
    beta_c_lc = [row for row in beta_rows if row[0] == QT and row[1] == "LC" and row[2] == 0.0][0]
    print(f"    headline beta (LC, Dw=0, q_inj=50 fC): ODE {beta_c_lc[5]:.5f}, first-order "
          f"{beta_c_lc[4]:.5f}; 1/beta = {1/beta_c_lc[4]:.1f} periods = "
          f"{TINJ/beta_c_lc[4]*1e9:.0f} ns settling time constant")

    # =====================================================================
    # (e) noise: PSD of locked phase vs free-run (ENGINE 1, LC, N = 20, Dw = 0)
    # =====================================================================
    print("  --- (e) locked-phase PSD vs free-run (map + white FM noise, LC, N = 20) ---")
    t_e = time.time()
    M_W = 32
    K_PSD = 2 ** 18
    sig_n = np.sqrt(KAPPA2 * TINJ)                       # per-period noise [rad]
    nz = RNG.standard_normal((K_PSD, M_W)) * sig_n
    th = np.zeros(M_W)
    th_rec = np.empty((K_PSD, M_W))
    b_lc = -sinc0                                        # Gbar = b_lc * sin
    for k in range(K_PSD):
        th_rec[k] = th                                   # pre-kick sample
        th = th + QT * b_lc * np.sin(th) + nz[k]
    phi_free = np.cumsum(nz, axis=0)
    K_TR = 2 ** 14
    NPS = 2 ** 14
    f, S_lock = welch(th_rec[K_TR:] - th_rec[K_TR:].mean(axis=0), fs=FREF,
                      nperseg=NPS, axis=0, scaling="density")
    _, S_free = welch(phi_free[K_TR:], fs=FREF, nperseg=NPS, axis=0,
                      scaling="density")
    S_lock, S_free = S_lock.mean(axis=1), S_free.mean(axis=1)
    f, S_lock, S_free = f[1:], S_lock[1:], S_free[1:]
    wT = TWO_PI * f * TINJ
    beta = beta_lc
    S_free_th = 2 * sig_n ** 2 * TINJ / (2 - 2 * np.cos(wT))
    S_lock_th = 2 * sig_n ** 2 * TINJ / (beta ** 2 + 2 * (1 - beta) * (1 - np.cos(wT)))
    H2_disc = (2 - 2 * np.cos(wT)) / (beta ** 2 + 2 * (1 - beta) * (1 - np.cos(wT)))
    wc = beta / TINJ
    H2_cont = (TWO_PI * f) ** 2 / (wc ** 2 + (TWO_PI * f) ** 2)
    band_lo = (f > 5e4) & (f < 1e6)                     # plateau region (f << f_c)
    band_hi = (f > 2e7) & (f < 6e7)
    r_plateau = np.mean(S_lock[band_lo] / S_lock_th[band_lo])
    r_free = np.mean(S_free[band_hi] / S_free_th[band_hi])
    r_hi = np.mean(S_lock[band_hi] / S_lock_th[band_hi])
    ratio = S_lock / S_free
    kern = np.ones(7) / 7
    rs = np.convolve(ratio, kern, mode="same")
    idx = np.where((rs[1:] >= 0.5) & (rs[:-1] < 0.5))[0][0]
    fc_meas = f[idx] + (0.5 - rs[idx]) * (f[idx + 1] - f[idx]) / (rs[idx + 1] - rs[idx])
    fc_pred = beta * FREF / TWO_PI
    fc_exact = brentq(lambda ff: (2 - 2 * np.cos(TWO_PI * ff * TINJ)) /
                      (beta ** 2 + 2 * (1 - beta) * (1 - np.cos(TWO_PI * ff * TINJ))) - 0.5,
                      1e3, FREF / 2)
    var_pre_th = sig_n ** 2 / (beta * (2 - beta))
    var_pre = th_rec[K_TR:].var()
    plateau_th = 2 * sig_n ** 2 * TINJ / beta ** 2
    print(f"    sigma_n^2 = kappa^2 T_inj = {sig_n**2:.3e} rad^2; beta = {beta:.5f}")
    print(f"    free-run PSD / 2 kappa^2/omega^2 (20-60 MHz): {r_free:.3f}")
    print(f"    locked PSD / discrete theory (50 kHz-1 MHz plateau region): {r_plateau:.3f}; "
          f"plateau = {plateau_th:.3e} rad^2/Hz = S_n/omega_c^2 ({2*KAPPA2/wc**2:.3e})")
    print(f"    locked PSD / discrete theory (20-60 MHz): {r_hi:.3f}")
    print(f"    corner (ratio = 1/2): measured {fc_meas/1e6:.4f} MHz; beta f_ref/2pi = "
          f"{fc_pred/1e6:.4f} MHz (ratio {fc_meas/fc_pred:.4f}); exact discrete "
          f"{fc_exact/1e6:.4f} MHz (ratio {fc_meas/fc_exact:.4f})")
    print(f"    continuous vs discrete |H|^2 at f_ref/2: {H2_cont[-1]:.4f} vs {H2_disc[-1]:.4f}")
    print(f"    pre-kick variance: measured {var_pre:.4e} rad^2 vs sigma_n^2/(beta(2-beta)) = "
          f"{var_pre_th:.4e} (ratio {var_pre/var_pre_th:.4f}) -> sigma_theta = "
          f"{np.sqrt(var_pre)*1e6:.2f} urad = {np.sqrt(var_pre)/(TWO_PI*F0)*1e15:.3f} fs")
    print(f"    (continuous first-order estimate S_n/(4 omega_c) = {2*KAPPA2/(4*wc):.4e} rad^2)")
    print(f"    free-run for comparison: kappa sqrt(t) at t = 1 us = "
          f"{np.sqrt(KAPPA2*1e-6)/(TWO_PI*F0)*1e15:.1f} fs (unbounded)")
    fc_closed = FREF / TWO_PI * np.arccos(1 - beta ** 2 / (2 * (1 + beta)))
    print(f"    exact discrete corner closed form f_ref/2pi*acos(1-beta^2/(2(1+beta))) = "
          f"{fc_closed/1e6:.4f} MHz = beta f_ref/2pi x {fc_closed/fc_pred:.4f} (~1-beta/2)")
    print(f"    [(e) took {time.time()-t_e:.1f} s]")

    # =====================================================================
    # (f1) output jitter vs N at fixed beta (edge-level simulation, LC, Dw = 0)
    # =====================================================================
    print("  --- (f1) output jitter vs N at fixed q_inj (fixed beta), edge-level ---")
    t_f = time.time()
    N_f = np.array([2, 4, 5, 8, 10, 16, 20, 25, 32, 40, 50])
    sig_all, sig_pre_f, sig_all_th = [], [], []
    W_J = 8
    for n_div in N_f:
        K = max(4096, (2 ** 20) // int(n_div))
        w = RNG.standard_normal((K, int(n_div), W_J)) * np.sqrt(KAPPA2_N)
        s = w.sum(axis=1)                                 # per-period sums
        th = np.zeros(W_J)
        pre = np.empty((K, W_J))
        post = np.empty((K, W_J))
        for k in range(K):
            pre[k] = th
            th = th + QT * b_lc * np.sin(th)
            post[k] = th
            th = th + s[k]
        warm = K // 8
        edges = post[warm:, None, :] + np.cumsum(w[warm:], axis=1)   # all N edges
        sig_all.append(np.sqrt(edges.var()))
        sig_pre_f.append(np.sqrt(pre[warm:].var()))
        vt = KAPPA2 * n_div * T0
        sig_all_th.append(np.sqrt((1 - beta) ** 2 * vt / (beta * (2 - beta)) + vt / 2))
    sig_all, sig_pre_f, sig_all_th = map(np.array, (sig_all, sig_pre_f, sig_all_th))
    slope_j = np.polyfit(np.log(N_f), np.log(sig_all), 1)[0]
    rj = sig_all / sig_all_th
    print(f"    fitted exponent d ln sigma / d ln N = {slope_j:.3f} (expect 0.5); "
          f"all-edge sigma / theory = {rj.min():.3f}..{rj.max():.3f}")
    i20 = int(np.where(N_f == 20)[0][0])
    print(f"    N = 20: all-edge sigma_t = {sig_all[i20]/(TWO_PI*F0)*1e15:.3f} fs "
          f"(theory {sig_all_th[i20]/(TWO_PI*F0)*1e15:.3f}), pre-kick "
          f"{sig_pre_f[i20]/(TWO_PI*F0)*1e15:.3f} fs;  N = 2: {sig_all[0]/(TWO_PI*F0)*1e15:.3f} fs; "
          f"N = 50: {sig_all[-1]/(TWO_PI*F0)*1e15:.3f} fs")

    # =====================================================================
    # (f2) reference spur at f_ref for a detuned lock (deterministic map, LC)
    # =====================================================================
    print("  --- (f2) reference spur vs detuning (locked, LC, N = 20) ---")
    df_list = np.array([0.1, 0.25, 0.5, 1.0, 1.5]) * 1e6                 # Hz
    spur1, spur2, spur_th1, spur_th2 = [], [], [], []
    P_SP, OS = 1024, 64
    for df in df_list:
        A = TWO_PI * df * TINJ
        th = 0.3
        for _ in range(2000):
            th = th + A + QT * b_lc * np.sin(th)
        # locked: build phi(t) on a fine grid, P_SP periods, OS samples/period
        th_post = th + QT * b_lc * np.sin(th)
        frac = (np.arange(OS) + 0.5) / OS
        phi = (th_post + A * frac)[None, :].repeat(P_SP, axis=0).ravel()
        X = np.fft.fft(np.exp(1j * phi))
        c0 = np.abs(X[0])
        spur1.append(20 * np.log10(0.5 * (np.abs(X[P_SP]) + np.abs(X[-P_SP])) / c0))
        spur2.append(20 * np.log10(0.5 * (np.abs(X[2 * P_SP]) + np.abs(X[-2 * P_SP])) / c0))
        spur_th1.append(20 * np.log10(df / FREF))
        spur_th2.append(20 * np.log10(df / (2 * FREF)))
        th_ss = np.arcsin(A / (QT * sinc0))
        print(f"    Delta f = {df/1e6:.2f} MHz (r = {A/(QT*sinc0):.3f}, theta* = {th_ss:.4f} rad, "
              f"A = Dw T_inj = {A:.5f} rad): spur@f_ref {spur1[-1]:.2f} dBc "
              f"(theory 20log10(Df/f_ref) = {spur_th1[-1]:.2f}), @2f_ref {spur2[-1]:.2f} "
              f"(theory {spur_th2[-1]:.2f})")
    spur1, spur2, spur_th1, spur_th2 = map(np.array, (spur1, spur2, spur_th1, spur_th2))
    print(f"    max|spur - theory|: k=1 {np.max(np.abs(spur1-spur_th1)):.2f} dB, "
          f"k=2 {np.max(np.abs(spur2-spur_th2)):.2f} dB  (independent of q_inj/beta)")
    print(f"    [(f) took {time.time()-t_f:.1f} s]")

    # =====================================================================
    # Figure
    # =====================================================================
    fig, axes = plt.subplots(2, 3, figsize=(18.5, 10.8))

    # ---- (a) lock range vs N ---------------------------------------------
    ax = axes[0, 0]
    Nd = np.linspace(1.8, 24, 100)
    for name, col, mk in (("LC", "tab:blue", "o"), ("ring", "tab:green", "s")):
        ax.loglog(Nd, A_edge_pred[name] / (Nd * T0) / TWO_PI / 1e6, "--", color=col, lw=1.3,
                  label=rf"理論 $f_L=\frac{{q_{{inj}}}}{{2\pi q_{{max}}}}\frac{{\max\vert\bar\Gamma\vert}}{{N T_0}}$（{name}）")
        ax.loglog(N_list, fL_meas[name] / 1e6, mk, color=col, ms=7, mfc="none", mew=1.6,
                  label=f"未平均 ODE 量測（{name}），斜率 {slope_N[name]:.3f}")
    ax.set_xlabel("倍頻比 $N$（$f_{ref}=f_0/N$）")
    ax.set_ylabel("半鎖定範圍 $f_L$  [MHz]")
    ax.set_title("(a) 脈衝注入 lock range $\\propto 1/N$（固定 $q_{inj}$=50 fC）\n"
                 "每個脈衝最多修 $q_{inj}\\max\\vert\\bar\\Gamma\\vert/q_{max}$ rad，失諧卻累積 $N$ 個週期")
    ax.set_xticks([2, 4, 8, 16, 20])
    ax.set_xticklabels(["2", "4", "8", "16", "20"])
    ax.legend(fontsize=8, loc="upper right")

    # ---- (b) lock range vs pulse width -----------------------------------
    ax = axes[0, 1]
    tpd = np.linspace(0.0, 0.95, 200)
    ax.plot(tpd, np.abs(np.sinc(tpd)), "k--", lw=1.3,
            label=r"$\vert\mathrm{sinc}(\tau_p/T_0)\vert=I_N(\tau_p)/I_N(0)$（脈衝第 $N$ 諧波）")
    ax.plot(tp_list, fL_tp["LC"] / fL0["LC"], "o", color="tab:blue", ms=7, mfc="none", mew=1.6,
            label="LC 量測（未平均 ODE 的 lock characteristic 極值）")
    ring_box = []
    for tp in tpd:
        gb, _ = isf_tables(gamma_ring, max(tp, 1e-6))
        ring_box.append(np.max(np.abs(gb)) / gmax_raw["ring"])
    ax.plot(tpd, ring_box, "-", color="tab:green", lw=1.3,
            label=r"ring 理論：箱形平均 $\max\vert\bar\Gamma_{\tau_p}\vert$（所有 $kN$ 諧波）")
    ax.plot(tp_list, fL_tp["ring"] / fL0["ring"], "s", color="tab:green", ms=7, mfc="none", mew=1.6,
            label="ring 量測（未平均 ODE）")
    ax.axvline(TP, color="0.5", ls=":", lw=1)
    ax.text(TP + 0.01, 0.05, r"canonical $\tau_p$=10 ps", fontsize=8, color="0.4")
    ax.set_xlabel(r"脈衝寬度 $\tau_p/T_0$（$T_0$=200 ps）")
    ax.set_ylabel(r"$f_L(\tau_p)\,/\,f_L(\tau_p\to0)$")
    ax.set_title("(b) 脈衝越寬、諧波越少、lock range 越小\n"
                 "LC 只吃第 $N$ 諧波 → 正好 sinc；ring 的尖 ISF 吃所有 $kN$ 諧波 → 掉得更快")
    ax.set_ylim(0, 1.05)
    ax.legend(fontsize=8, loc="upper right")

    # ---- (c) pulse vs sine drift curves ----------------------------------
    ax = axes[0, 2]
    for name, col, mk in (("LC", "tab:blue", "o"), ("ring", "tab:green", "s")):
        wl_n = A_edge_pred[name] / N_HEAD
        ax.plot(r_grid, drift_pulse[name] / wl_n, mk, color=col, ms=5, mfc="none", mew=1.4,
                label=f"脈衝串（{name}）")
        ax.plot(r_grid, drift_sine[name] / wl_n, "x", color=col, ms=6,
                label=f"純正弦 $f_0/N$，同 $I_{{rms}}$（{name}）")
    xx = np.linspace(-1.5, 1.5, 400)
    ax.plot(xx, xx + push_lc_n / (A_edge_pred["LC"] / N_HEAD), "-.", color="tab:blue", lw=0.9,
            label=r"LC 正弦：$\Delta\omega+\Delta\omega_{push}$（二階 pushing，無平台）")
    ax.plot(xx, np.where(np.abs(xx) > 1, np.sign(xx) * np.sqrt(np.maximum(xx ** 2 - 1, 0)), 0),
            "k--", lw=1.3, label=r"Adler 連續極限 $\mathrm{sgn}\sqrt{\Delta\omega^2-\omega_L^2}/\omega_L$")
    ax.plot(xx, xx, ":", color="gray", lw=1.2, label=r"無鎖定：漂移 $=\Delta\omega$")
    ax.set_xlabel(r"正規化失諧 $\Delta\omega/\omega_L$（$\Delta\omega\equiv\omega_0-N\omega_{inj}$，各自以 $\omega_L$ 正規化）")
    ax.set_ylabel(r"$\theta$ 平均漂移率 $/\,\omega_L$")
    ax.set_title("(c) 同樣 $I_{rms}$=250 μA：脈衝串鎖定、純正弦鎖不住（一階）\n"
                 "正弦在 $f_0/N$ 沒有第 $N$ 諧波可與 ISF 基頻同步平均")
    ax.legend(fontsize=8, loc="upper left")
    ax.set_xlim(-1.55, 1.55)

    # ---- (d) beta step response ------------------------------------------
    ax = axes[1, 0]
    bmap = br[:, 1]
    bode = br[:, 2]
    ax.plot([1e-3, 0.1], [1e-3, 0.1], "k--", lw=1.2, label=r"一階預測 $\beta=-\frac{q_{inj}}{q_{max}}\bar\Gamma'(\theta^*)$")
    bb = np.logspace(-3, -1, 100)
    ax.plot(bb, 1 - np.exp(-bb), "-", color="0.5", lw=1.2,
            label=r"$1-e^{-\beta}$（脈衝期間相位自身移動的二階修正）")
    for name, col, mk in (("LC", "tab:blue", "o"), ("ring", "tab:green", "s")):
        sel = np.array([row[1] == name for row in beta_rows])
        ax.loglog(bmap[sel], bode[sel], mk, color=col, ms=7, mfc="none", mew=1.6,
                  label=f"ODE 步階響應量測（{name}，$q_{{inj}}/q_{{max}}$=0.05 與 0.01）")
    ax.set_xlabel(r"預測 $\beta$（無因次）")
    ax.set_ylabel(r"量測 $\beta$（$\delta\theta_{k+1}/\delta\theta_k=1-\beta$）")
    ax.set_title("(d) 重新對齊因子 β：ODE 步階響應 vs 一階預測 $-q_{inj}\\bar\\Gamma'(\\theta^*)/q_{max}$\n"
                 "偏差 $O(q_{inj}/q_{max})$：$q_{inj}/q_{max}$ 從 0.05 降到 0.01，比值收向 1")
    ax.set_xlim(1.5e-3, 0.08)
    ax.set_ylim(1.5e-3, 0.08)
    ax.legend(fontsize=8, loc="upper left")

    # ---- (e) PSD ----------------------------------------------------------
    ax = axes[1, 1]
    ax.loglog(f, S_free, color="0.6", lw=1.0, label="自由跑 $S_\\phi$（量測，取樣於 $f_{ref}$）")
    ax.loglog(f, S_lock, color="tab:blue", lw=1.0, label="鎖定 $S_\\theta$（量測，脈衝前取樣）")
    ax.loglog(f, S_free_th, "k--", lw=1.2, label=r"$2\kappa^2/\omega^2$（離散：$2\sigma_n^2T_{inj}/\vert1-e^{-j\omega T_{inj}}\vert^2$）")
    ax.loglog(f, S_lock_th, "--", color="navy", lw=1.4,
              label=r"一階離散迴路 $2\sigma_n^2T_{inj}/\vert e^{j\omega T_{inj}}-(1-\beta)\vert^2$")
    ax.axvline(fc_pred, color="darkred", ls=":", lw=1.0)
    ax.text(fc_pred * 1.15, S_lock_th[0] * 2, f"$f_c=\\beta f_{{ref}}/2\\pi$\n= {fc_pred/1e6:.2f} MHz\n量測 {fc_meas/1e6:.2f} MHz",
            fontsize=8, color="darkred")
    ax.set_xlabel("offset 頻率 $f$  [Hz]")
    ax.set_ylabel(r"$S(f)$  [rad$^2$/Hz]")
    ax.set_title("(e) 鎖定相位雜訊＝一階離散高通整形（LC，$N$=20，$\\Delta\\omega$=0）\n"
                 r"平台 $2\kappa^2T_{inj}^2/\beta^2=S_n/\omega_c^2$；$\omega_c=\beta/T_{inj}$")
    ax.set_xlim(1.5e4, 1.3e8)
    ax.legend(fontsize=7.5, loc="lower left")

    # ---- (f) jitter vs N + spur inset -----------------------------------
    ax = axes[1, 2]
    ax.loglog(N_f, sig_all / (TWO_PI * F0) * 1e15, "o", color="tab:blue", ms=7, mfc="none", mew=1.6,
              label=f"全部輸出邊緣 jitter（edge-level 模擬），斜率 {slope_j:.3f}")
    ax.loglog(N_f, sig_pre_f / (TWO_PI * F0) * 1e15, "s", color="tab:orange", ms=6, mfc="none", mew=1.4,
              label="脈衝前取樣點 jitter")
    Nd2 = np.linspace(1.8, 55, 100)
    vt = KAPPA2 * Nd2 * T0
    ax.loglog(Nd2, np.sqrt((1 - beta) ** 2 * vt / (beta * (2 - beta)) + vt / 2) / (TWO_PI * F0) * 1e15,
              "k--", lw=1.3, label=r"理論 $\sqrt{(1-\beta)^2\frac{\kappa^2T_{inj}}{\beta(2-\beta)}+\frac{\kappa^2T_{inj}}{2}}\ \propto\sqrt{N}$")
    ax.set_xlabel("倍頻比 $N$（固定 $q_{inj}$ → 固定 $\\beta$=0.0498）")
    ax.set_ylabel(r"輸出 rms jitter $\sigma_t$  [fs]")
    ax.set_title("(f) jitter $\\propto\\sqrt{N}$（迴路角落 $f_c=\\beta f_{ref}/2\\pi\\propto1/N$）\n"
                 "內嵌：失諧鎖定的參考 spur $=20\\log_{10}(\\Delta f/f_{ref})$，與 $q_{inj}$ 無關")
    ax.set_xticks([2, 5, 10, 20, 50])
    ax.set_xticklabels(["2", "5", "10", "20", "50"])
    ax.legend(fontsize=8, loc="upper left")
    axin = ax.inset_axes([0.55, 0.10, 0.42, 0.36])
    axin.semilogx(df_list / 1e6, spur1, "o", color="tab:red", ms=5, label="k=1 量測")
    axin.semilogx(df_list / 1e6, spur_th1, "--", color="tab:red", lw=1.0)
    axin.semilogx(df_list / 1e6, spur2, "s", color="tab:purple", ms=5, label="k=2 量測")
    axin.semilogx(df_list / 1e6, spur_th2, "--", color="tab:purple", lw=1.0)
    axin.set_xlabel(r"失諧 $\Delta f$ [MHz]（$f_L$=1.98 MHz）", fontsize=7)
    axin.set_ylabel("spur [dBc]", fontsize=7)
    axin.tick_params(labelsize=7)
    axin.legend(fontsize=6.5, loc="lower right")
    axin.grid(alpha=0.3)

    fig.suptitle("次諧波（×N）脈衝注入鎖定：impulse-train 映射 vs 未平均時間同步 ODE（[P3] Eq.(19)–(23), Eq.(28)–(30)；"
                 "[P4] Eq.(28)–(30) 取 (M,N)=(N,1)）— $f_0$=5 GHz, $q_{max}$=1 pC, $q_{inj}$=50 fC, "
                 "$\\tau_p$=10 ps, $\\kappa^2$=0.125 rad²/s", fontsize=11)
    savefig(fig, "subharmonic_injection.png")
    print(f"  runtime: {time.time() - t_start:.1f} s")


if __name__ == "__main__":
    main()
