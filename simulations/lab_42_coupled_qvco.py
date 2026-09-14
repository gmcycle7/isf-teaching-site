"""
lab_42_coupled_qvco.py

Goal
----
Numerically verify Section 4 of docs/06_design_insights/quadrature_and_coupled_
oscillators.md: a coupled quadrature VCO (QVCO) is TWO copies of the [P3]
generalized Adler ("pulling") equation injecting into each other.

  * [P3] Eq.(30), p.2113 : dtheta/dt = w0 - w_inj
                           + (1/T_inj) int_{T_inj} Gamma_tilde(w_inj t + theta) i_inj(t) dt
  * [P3] Eq.(33), p.2114 : Omega(theta) = (1/T_inj) int_{T_inj} Gamma_tilde(w_inj t + theta) i_inj(t) dt
  * [P3] Eq.(34), p.2114 : sinusoidal injection I_inj cos(w_inj t):
                           Omega(theta) = (1/2) I_inj |G_1| cos(theta + ang G_1)
  * [P3] Eq.(35), p.2114 : w_L = (1/2) I_inj |G_1|      (G_1 = fundamental phasor of
                           Gamma_tilde = Gamma/q_max, [P3] Eq.(26), p.2113)

Model (mutual injection, ideal-LC ISF Gamma_tilde(x) = -sin(x)/q_max, so
|G_1| = 1/q_max and ang G_1 = +90 deg)
-----------------------------------------------------------------------------
Oscillator A (free-running w0A) and B (w0B) run in a common reference frame
w_ref; theta_A, theta_B are their phases relative to w_ref t.  The coupling
devices inject A's output into B and B's output INVERTED into A (the QVCO
sign convention of the page), with an optional coupling-path phase shift
phi_c:

    i_{A->B}(t) = +I_c cos(w_ref t + theta_A + phi_c)
    i_{B->A}(t) = -I_c cos(w_ref t + theta_B + phi_c)

UNAVERAGED pair ([P3] Eq.(29) form, integrated as-is -- this is the real test,
nothing is assumed about averaging):

    dtheta_A/dt = (w0A - w_ref) + Gamma_tilde(w_ref t + theta_A) i_{B->A}(t)
    dtheta_B/dt = (w0B - w_ref) + Gamma_tilde(w_ref t + theta_B) i_{A->B}(t)

AVERAGED pair ([P3] Eq.(30)/(33)/(34) applied to each oscillator), with
psi = theta_A - theta_B (the I/Q phase difference) and w_L = I_c/(2 q_max):

    Omega_A(psi) = w_L sin(psi - phi_c),   Omega_B(psi) = w_L sin(psi + phi_c)
    dpsi/dt = (w0A - w0B) - 2 w_L sin(phi_c) cos(psi)                   (*)

Steady state of (*):  cos(psi*) = Dw0 / (2 w_L sin phi_c).
  - phi_c = 90 deg (coupling aligned with the ISF fundamental):
        psi* = -90 deg + delta,   sin(delta) = Dw0/(2 w_L)  ->  EXACT
        delta ~= Dw0/(2 w_L) = (Q/m) (Dw0/w0)                ->  page's formula
    (the "2" is the MUTUAL-injection factor: both oscillators pull).
  - phi_c = 0 (plain parallel QVCO, pure -sin ISF): the restoring term
    vanishes -> the phase-only model is DEGENERATE (psi is not selected by
    Adler alone; the amplitude channel of [P4] decides).  Honest caveat.

Coupling factor m = I_c/I_core and tank Q enter only through
    w_L = m w0/(2Q)     (page Section 2; from I_core = q_max w0/Q for an LC tank)

Figure
------
  static/figures/coupled_qvco.png   (3 panels)
    (a) transient psi(t) from the UNAVERAGED pair, several starts -> lock to
        -90 deg + delta; the plain P-QVCO (phi_c = 0) drifts (no lock)
    (b) I/Q error delta vs tank mismatch Dw0/w0 for m = 0.1, 0.3, 1.0 (Q = 10):
        numeric steady state vs arcsin exact vs linear (Q/m)(Dw0/w0); unlock at m/Q
    (c) delta vs m at fixed mismatch: 1/m law, worked point (m=0.3 -> 1.91 deg)

Run
---
  PYTHONPATH=<project root> python simulations/lab_42_coupled_qvco.py
"""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt

from plot_utils import savefig

# ---------------------------------------------------------------------------
# canonical anchors (site spec section 8) + the page's worked example
# ---------------------------------------------------------------------------
F0 = 5.0e9                      # [Hz]  carrier
OMEGA0 = 2.0 * np.pi * F0       # [rad/s]
Q_TANK = 10.0                   # tank Q of the page's worked example
Q_MAX = 1.0e-12                 # [C]   canonical q_max = 1 pC
M_WORKED = 0.3                  # coupling factor m = I_c / I_core
DETUNE_WORKED = 1.0e-3          # Dw0/w0 = 0.1 % tank mismatch
PHI_C_ALIGNED = np.pi / 2.0     # coupling-path phase that aligns with -sin ISF


def omega_lock(m, Q=Q_TANK, omega0=OMEGA0):
    """Half lock range of the mutual injection, w_L = m*w0/(2Q) [rad/s].

    Derivation: LC tank fundamental current I_core = q_max*w0/Q (q_max = C*V,
    I_core = V/R_p, Q = w0*R_p*C); I_c = m*I_core; [P3] Eq.(35) with
    |G_1| = 1/q_max gives w_L = I_c/(2 q_max) = m*w0/(2Q).
    """
    return m * omega0 / (2.0 * Q)


def gamma_tilde(x, q_max=Q_MAX):
    """Ideal-LC unit-bearing ISF, [P3] Eq.(26): Gamma/q_max = -sin(x)/q_max [rad/C]."""
    return -np.sin(x) / q_max


# ---------------------------------------------------------------------------
# [P3] Eq.(33): lock characteristic by explicit period averaging, checked
# against the sinusoidal closed form Eq.(34)
# ---------------------------------------------------------------------------
def lock_characteristic_numeric(theta, I_inj, q_max=Q_MAX, n_pts=4096):
    """Omega(theta) = (1/T) int_T Gamma_tilde(w t + theta) * I_inj cos(w t) dt (Eq.33)."""
    x = np.linspace(0.0, 2.0 * np.pi, n_pts, endpoint=False)
    theta = np.atleast_1d(theta)
    out = np.empty_like(theta, dtype=float)
    for k, th in enumerate(theta):
        out[k] = np.mean(gamma_tilde(x + th, q_max) * I_inj * np.cos(x))
    return out


def lock_characteristic_eq34(theta, I_inj, q_max=Q_MAX):
    """[P3] Eq.(34) for Gamma_tilde = -sin/q_max: |G_1| = 1/q_max, ang G_1 = +90 deg."""
    return 0.5 * I_inj * (1.0 / q_max) * np.cos(theta + np.pi / 2.0)


# ---------------------------------------------------------------------------
# UNAVERAGED mutual-injection pair ([P3] Eq.(29) form), RK4 in s = w_ref t
# ---------------------------------------------------------------------------
def integrate_unaveraged(m, detune, phi_c=PHI_C_ALIGNED, Q=Q_TANK, psi0=-0.5,
                         n_cycles=60, steps_per_cycle=200):
    """Return (t [s], theta_A, theta_B, psi) for w0A = w_ref(1+detune/2),
    w0B = w_ref(1-detune/2); w_ref = OMEGA0.  Starts with theta_A - theta_B = psi0."""
    wl = omega_lock(m, Q) / OMEGA0          # w_L / w_ref  (dimensionless)
    dA = +0.5 * detune                      # (w0A - w_ref)/w_ref
    dB = -0.5 * detune
    ic = 2.0 * wl                           # I_c/(q_max*w_ref) = 2 w_L/w_ref

    def rhs(s, y):
        thA, thB = y
        # Gamma_tilde(w t + theta_A) * i_{B->A}(t), i_{B->A} = -I_c cos(w t + theta_B + phi_c)
        fA = dA + (-np.sin(s + thA)) * (-ic * np.cos(s + thB + phi_c))
        # Gamma_tilde(w t + theta_B) * i_{A->B}(t), i_{A->B} = +I_c cos(w t + theta_A + phi_c)
        fB = dB + (-np.sin(s + thB)) * (+ic * np.cos(s + thA + phi_c))
        return np.array([fA, fB])

    n = n_cycles * steps_per_cycle
    h = 2.0 * np.pi / steps_per_cycle
    s = 0.0
    y = np.array([psi0, 0.0])
    out = np.empty((n + 1, 2))
    out[0] = y
    for i in range(n):
        k1 = rhs(s, y)
        k2 = rhs(s + 0.5 * h, y + 0.5 * h * k1)
        k3 = rhs(s + 0.5 * h, y + 0.5 * h * k2)
        k4 = rhs(s + h, y + h * k3)
        y = y + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        s += h
        out[i + 1] = y
    t = np.arange(n + 1) * h / OMEGA0
    return t, out[:, 0], out[:, 1], out[:, 0] - out[:, 1]


# ---------------------------------------------------------------------------
# AVERAGED pair: dpsi/dtau = r - 2 sin(phi_c) cos(psi), tau = w_L t, r = Dw0/w_L
# vectorized RK4 -> steady-state I/Q error (NaN when unlocked)
# ---------------------------------------------------------------------------
def steady_state_iq_error(m, detune, phi_c=PHI_C_ALIGNED, Q=Q_TANK, omega0=OMEGA0,
                          tau_max=60.0, dtau=0.01):
    """I/Q phase error delta = psi* + 90 deg [rad] of the averaged Adler pair.

    m, detune may be arrays (broadcast).  Returns (delta_numeric, delta_exact,
    delta_linear): numeric = RK4 steady state, exact = arcsin(Dw0/(2 w_L sin phi_c)),
    linear = Dw0/(2 w_L sin phi_c) = (Q/m)(Dw0/w0)/sin phi_c.  NaN where unlocked.
    """
    m = np.asarray(m, dtype=float)
    detune = np.asarray(detune, dtype=float)
    m, detune = np.broadcast_arrays(m, detune)
    wl = omega_lock(m, Q, omega0)
    r = detune * omega0 / wl                     # Dw0 / w_L
    g = 2.0 * np.sin(phi_c)                      # restoring strength (mutual: 2x)
    f = lambda p: r - g * np.cos(p)
    psi = np.full(m.shape, -np.pi / 2.0 + 0.3)   # start inside the stable basin
    n = int(tau_max / dtau)
    for _ in range(n):
        k1 = f(psi)
        k2 = f(psi + 0.5 * dtau * k1)
        k3 = f(psi + 0.5 * dtau * k2)
        k4 = f(psi + dtau * k3)
        psi = psi + (dtau / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
    locked = np.abs(f(psi)) < 1e-6
    delta_num = np.where(locked, psi + np.pi / 2.0, np.nan)
    arg = r / g
    delta_exact = np.where(np.abs(arg) <= 1.0, np.arcsin(np.clip(arg, -1, 1)), np.nan)
    delta_lin = arg
    return delta_num, delta_exact, delta_lin


# ---------------------------------------------------------------------------
def main():
    t0 = time.time()
    deg = np.degrees
    wl = omega_lock(M_WORKED)
    dw0 = DETUNE_WORKED * OMEGA0
    ic = 2.0 * Q_MAX * wl                    # [P3] Eq.(35): I_c = 2 q_max w_L
    icore = ic / M_WORKED
    print("=== worked example: m=%.1f, Q=%.0f, Dw0/w0=%.1e, f0=%.0f GHz, q_max=%.0f pC ===" %
          (M_WORKED, Q_TANK, DETUNE_WORKED, F0 / 1e9, Q_MAX * 1e12))
    print("w_L = m*w0/(2Q)      = %.4e rad/s  (f_L = %.1f MHz)" % (wl, wl / 2 / np.pi / 1e6))
    print("I_c = 2 q_max w_L    = %.3f mA   [P3] Eq.(35)" % (ic * 1e3))
    print("I_core = I_c/m       = %.3f mA   (check q_max*w0/Q = %.3f mA)" %
          (icore * 1e3, Q_MAX * OMEGA0 / Q_TANK * 1e3))
    print("Dw0 = 0.1%% of w0     = %.4e rad/s  (Df0 = %.1f MHz)" % (dw0, dw0 / 2 / np.pi / 1e6))
    print("Dw0/(2 w_L)          = %.6f  (= (Q/m)(Dw0/w0))" % (dw0 / (2 * wl)))

    # --- Eq.(33) numeric averaging vs Eq.(34) closed form -------------------
    th = np.linspace(-np.pi, np.pi, 181)
    om_num = lock_characteristic_numeric(th, ic)
    om_34 = lock_characteristic_eq34(th, ic)
    err33 = np.max(np.abs(om_num - om_34)) / np.max(np.abs(om_34))
    print("Eq.(33) period-average vs Eq.(34) closed form: max rel err = %.1e ; "
          "max Omega = %.4e rad/s (= w_L: %s)" % (err33, om_num.max(), np.isclose(om_num.max(), wl, rtol=1e-6)))

    # --- steady state: numeric vs exact vs linear ------------------------------
    d_num, d_ex, d_lin = steady_state_iq_error(M_WORKED, DETUNE_WORKED)
    print("delta linear (Q/m)(Dw0/w0) = %.6f rad = %.4f deg" % (d_lin, deg(d_lin)))
    print("delta exact  arcsin        = %.6f rad = %.4f deg" % (d_ex, deg(d_ex)))
    print("delta numeric averaged pair= %.6f rad = %.4f deg" % (d_num, deg(d_num)))
    print("linear-vs-exact rel error  = %.3e  (%.4f %%)" % ((d_lin - d_ex) / d_ex, 100 * (d_lin - d_ex) / d_ex))

    # --- unaveraged pair at the worked point ----------------------------------
    t, thA, thB, psi = integrate_unaveraged(M_WORKED, DETUNE_WORKED, psi0=-0.5)
    tail = psi[-10 * 200:]                      # last 10 cycles
    d_unavg = np.mean(tail) + np.pi / 2.0
    ripple = 0.5 * (tail.max() - tail.min())
    print("delta unaveraged pair (mean of last 10 cycles) = %.6f rad = %.4f deg ; "
          "2w ripple +/- %.4f deg" % (d_unavg, deg(d_unavg), deg(ripple)))
    tau_lock = 1.0 / (2.0 * wl)
    print("lock time constant 1/(2 w_L) = %.3f ns = %.1f cycles" % (tau_lock * 1e9, tau_lock * F0))
    print("unlock limit Dw0/w0 = m/Q = %.1f %%  (Df0 = %.0f MHz)" %
          (100 * M_WORKED / Q_TANK, M_WORKED / Q_TANK * F0 / 1e6))
    print("m needed for 0.5 deg at 0.1%% mismatch: m >= Q*Dw0/w0/sin(0.5deg) = %.3f" %
          (Q_TANK * DETUNE_WORKED / np.sin(np.radians(0.5))))
    print("plain P-QVCO (phi_c=0) frequency pull from tank peak: -w_L/w0 = -m/(2Q) = %.2f %% = %.0f MHz ;"
          " aligned (phi_c=90deg): Omega_A(psi*) = %.1f MHz = -Df0/2 (A and B just meet at the mean frequency)" %
          (-100 * M_WORKED / 2 / Q_TANK, -wl / 2 / np.pi / 1e6,
           wl * np.sin(-np.pi / 2 + d_ex - np.pi / 2) / 2 / np.pi / 1e6))

    # --- panel (a) trajectories ------------------------------------------------
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.6))
    ax = axes[0]
    wrap = lambda p: (p + np.pi) % (2 * np.pi) - np.pi
    for p0 in np.radians([-170.0, -30.0, 60.0, 150.0]):
        t, _, _, ps = integrate_unaveraged(M_WORKED, DETUNE_WORKED, psi0=p0, n_cycles=60)
        ax.plot(t * 1e9, deg(wrap(ps)), lw=1.3, label=r"$\psi_0=%+.0f^\circ$" % deg(p0))
    t, _, _, ps = integrate_unaveraged(M_WORKED, DETUNE_WORKED, phi_c=0.0, psi0=np.radians(-30.0), n_cycles=60)
    ax.plot(t * 1e9, deg(wrap(ps)), "k--", lw=1.2, label=r"plain P-QVCO ($\phi_c=0$): no lock")
    ax.axhline(deg(-np.pi / 2 + d_ex), color="crimson", lw=1.0, ls=":",
               label=r"Adler steady state $-90^\circ+%.2f^\circ$" % deg(d_ex))
    ax.set_xlabel("t [ns]  (f0 = 5 GHz, 1 ns = 5 cycles)")
    ax.set_ylabel(r"I/Q phase difference $\psi=\theta_A-\theta_B$ [deg]")
    ax.set_title(r"(a) unaveraged pair, m=%.1f, Q=%.0f, $\Delta\omega_0/\omega_0$=0.1%%" % (M_WORKED, Q_TANK))
    ax.set_ylim(-185, 185)
    ax.legend(loc="upper right", fontsize=8)

    # --- panel (b) delta vs mismatch for several m -------------------------------
    ax = axes[1]
    det = np.linspace(0.0, 0.045, 46)
    colors = ["tab:blue", "tab:green", "tab:orange"]
    for mm, c in zip([0.1, 0.3, 1.0], colors):
        dn, de, dl = steady_state_iq_error(mm, det)
        ax.plot(100 * det, deg(de), color=c, lw=1.6, label="m=%.1f exact arcsin" % mm)
        ax.plot(100 * det, deg(dl), color=c, lw=1.0, ls="--")
        ax.plot(100 * det[::3], deg(dn[::3]), "o", color=c, ms=4, mfc="none")
        ax.axvline(100 * mm / Q_TANK, color=c, lw=0.8, ls=":")
    ax.plot([], [], "k--", lw=1.0, label=r"linear $(Q/m)\,\Delta\omega_0/\omega_0$")
    ax.plot([], [], "ko", ms=4, mfc="none", label="numeric steady state")
    ax.plot(100 * DETUNE_WORKED, deg(d_ex), "r*", ms=12, label="worked: 0.1%% -> %.2f deg" % deg(d_ex))
    ax.set_xlabel(r"tank mismatch $\Delta\omega_0/\omega_0$ [%]")
    ax.set_ylabel(r"I/Q phase error $\Delta\phi_{IQ}$ [deg]")
    ax.set_title("(b) error vs mismatch (dotted: unlock at m/Q)")
    ax.set_xlim(0, 4.6)
    ax.set_ylim(0, 60)
    ax.legend(fontsize=8, loc="upper left")

    # --- panel (c) delta vs m -------------------------------------------------
    ax = axes[2]
    ms = np.logspace(np.log10(0.05), np.log10(3.0), 60)
    for dd, c in zip([0.001, 0.005, 0.01], ["tab:red", "tab:purple", "tab:brown"]):
        dn, de, dl = steady_state_iq_error(ms, dd)
        ax.loglog(ms, deg(de), color=c, lw=1.6, label=r"$\Delta\omega_0/\omega_0$=%.1f%% exact" % (100 * dd))
        ax.loglog(ms, deg(dl), color=c, lw=1.0, ls="--")
        ax.loglog(ms[::4], deg(dn[::4]), "o", color=c, ms=4, mfc="none")
    ax.plot([], [], "k--", lw=1.0, label=r"linear $\propto 1/m$")
    ax.loglog(M_WORKED, deg(d_ex), "r*", ms=12, label="worked: m=0.3 -> %.2f deg" % deg(d_ex))
    ax.axhline(0.5, color="gray", lw=0.8, ls=":")
    ax.text(0.5, 50.0, r"dotted: $0.5^\circ$ spec -> m >= 1.15 at 0.1%", fontsize=8, color="gray")
    ax.set_xlabel("coupling factor m = I_c / I_core")
    ax.set_ylabel(r"I/Q phase error $\Delta\phi_{IQ}$ [deg]")
    ax.set_title("(c) error vs coupling (Q=10)")
    ax.legend(fontsize=8, loc="lower left")

    fig.suptitle("Coupled QVCO as two mutually injecting [P3] Adler equations "
                 r"(ideal LC $\tilde\Gamma=-\sin/q_{max}$, coupling aligned $\phi_c=90^\circ$; toy model)",
                 fontsize=11)
    savefig(fig, "coupled_qvco.png")
    print("runtime %.1f s" % (time.time() - t0))


if __name__ == "__main__":
    main()
