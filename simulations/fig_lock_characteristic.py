"""
fig_lock_characteristic.py

Goal
----
Visualise the [P3] *lock characteristic* Omega(theta) and the geometric meaning
of "lock range = the value-range (peak-to-peak swing about 0) of Omega(theta)".

[P3] B. Hong & A. Hajimiri, "A General Theory of Injection Locking and Pulling
in Electrical Oscillators -- Part I," IEEE JSSC 54(8):2109-2121, Aug. 2019.
The generalized Adler equation (Eq. (33), p.2114) is

    d(theta)/dt = (omega0 - omega_inj) + Omega(theta),
    Omega(theta) = (1/T_inj) * integral_{T_inj} Gamma_tilde(omega_inj*t + theta)
                                                 * i_inj(t) dt ,            (33)

with the *unit-bearing* ISF Gamma_tilde(x) = Gamma(x)/q_max  [rad/C]  (Eq. (26)).
Locking requires a steady state omega_inj - omega0 = Omega(theta*); the lock
range is the width of the value range of Omega(theta), and its edges are the
max/min of Omega(theta).

Two cases are contrasted:
  (i)  SINUSOIDAL injection, single-tone i_inj = I_inj*cos(omega_inj*t), into an
       ideal-LC ISF Gamma_tilde = -sin(theta)/q_max. Only the ISF fundamental
       survives the time average (Eq. (34)-(35)), so Omega(theta) is a clean
       cosine, SYMMETRIC about 0: omega_L+ = -omega_L- = omega_L.
  (ii) HARMONIC-RICH injection (a tone + its 2nd harmonic, deliberately phased)
       into a harmonic-rich ISF. Several ISF harmonics now contribute, so
       Omega(theta) is ASYMMETRIC: omega_L+ != -omega_L-. This is the
       Adler-invisible asymmetric lock range that [P3] highlights.

Omega(theta) is computed DIRECTLY from the Eq.(33) time-average integral (not a
hand-built cosine), so the figure is faithful to the paper's definition.

NOTE: pedagogical TOY model. No transistor netlist. The ideal-LC ISF -sin is
exact; the harmonic-rich ISF and the designed injection waveform are
illustrative, chosen only to expose the asymmetry mechanism.

Figure produced
---------------
  static/figures/lock_characteristic_omega.png
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt

from isf_utils import gamma_lc_ideal
from plot_utils import savefig

# NumPy 2.0 renamed np.trapz -> np.trapezoid; support both (matches isf_utils).
try:
    from numpy import trapezoid as _trapz
except ImportError:  # numpy < 2.0
    from numpy import trapz as _trapz


def lock_characteristic(gamma_tilde_func, i_inj_func, omega_inj, theta_grid,
                        n_time=4096):
    """
    Evaluate the [P3] Eq.(33) lock characteristic Omega(theta) on a grid.

        Omega(theta) = (1/T_inj) * integral_0^{T_inj}
                          Gamma_tilde(omega_inj*t + theta) * i_inj(t) dt

    Parameters
    ----------
    gamma_tilde_func : callable x -> Gamma_tilde(x)   [rad/C], 2*pi-periodic
    i_inj_func       : callable t -> i_inj(t)         [A]
    omega_inj        : injection angular frequency    [rad/s]
    theta_grid       : phase-offset samples theta     [rad]
    n_time           : samples used for the one-period time average

    Returns
    -------
    Omega : ndarray, same shape as theta_grid          [rad/s]
            (Gamma_tilde [rad/C] * i_inj [C/s = A] -> rad/s, as it must.)
    """
    T_inj = 2.0 * np.pi / omega_inj
    # endpoint=True so the trapezoid rule integrates the full closed period.
    t = np.linspace(0.0, T_inj, n_time, endpoint=True)
    i_t = i_inj_func(t)  # [A], shape (n_time,)
    out = np.empty_like(theta_grid, dtype=float)
    for k, th in enumerate(theta_grid):
        integrand = gamma_tilde_func(omega_inj * t + th) * i_t  # [rad/C * A]
        out[k] = _trapz(integrand, t) / T_inj
    return out


def main():
    print("[fig_lock_characteristic] Omega(theta): sinusoidal vs harmonic-rich injection ...")

    # ------------------------------------------------------------------
    # Normalised, dimension-consistent toy numbers.
    #   q_max = 1 C (normalised) so Gamma_tilde = Gamma/q_max has the same
    #   numbers as Gamma but carries [rad/C]; I_inj = 1 A; omega_inj ~ omega0.
    #   Then Omega has units rad/C * A = rad/s, exactly the lock-range axis.
    # ------------------------------------------------------------------
    q_max = 1.0          # C (normalised)
    I_inj = 1.0          # A
    omega_inj = 1.0      # rad/s (normalised; injection ~ free-running)

    theta = np.linspace(0.0, 2.0 * np.pi, 1000, endpoint=True)

    # ---- Case (i): sinusoidal injection into ideal-LC ISF -------------
    # Gamma_tilde(x) = -sin(x)/q_max ;  i_inj(t) = I_inj*cos(omega_inj*t)
    gamma_lc = lambda x: gamma_lc_ideal(x) / q_max          # -sin(x)/q_max
    i_sin = lambda t: I_inj * np.cos(omega_inj * t)
    Omega_sin = lock_characteristic(gamma_lc, i_sin, omega_inj, theta)

    # ---- Case (ii): harmonic-rich injection into harmonic-rich ISF ----
    # Harmonic-rich ISF: fundamental + a deliberately phased 2nd harmonic, so
    # aligning the injection's 2nd harmonic biases Omega(theta) asymmetrically.
    def gamma_rich(x):
        return (-np.sin(x) + 0.55 * np.sin(2.0 * x + 0.6)) / q_max
    # Injection waveform carrying a tone + its 2nd harmonic (designed shape).
    def i_rich(t):
        return I_inj * (np.cos(omega_inj * t)
                        + 0.7 * np.cos(2.0 * omega_inj * t + 0.3))
    Omega_rich = lock_characteristic(gamma_rich, i_rich, omega_inj, theta)

    # ---- Lock-range edges = max/min of Omega(theta) -------------------
    def edges(Om, th):
        imax, imin = int(np.argmax(Om)), int(np.argmin(Om))
        return (th[imax], Om[imax]), (th[imin], Om[imin])

    (th_p_s, wLp_s), (th_m_s, wLm_s) = edges(Omega_sin, theta)
    (th_p_r, wLp_r), (th_m_r, wLm_r) = edges(Omega_rich, theta)

    print(f"  sinusoidal : omega_L+ = {wLp_s:+.3f}, omega_L- = {wLm_s:+.3f} rad/s "
          f"(|sum| = {abs(wLp_s + wLm_s):.2e}  -> symmetric)")
    print(f"  harmonic   : omega_L+ = {wLp_r:+.3f}, omega_L- = {wLm_r:+.3f} rad/s "
          f"(|sum| = {abs(wLp_r + wLm_r):.2e}  -> asymmetric)")

    # ------------------------------------------------------------------
    # Plot. Default white figure/axes background renders correctly on the
    # white content card in both light and dark site themes.
    # ------------------------------------------------------------------
    x = theta / (2.0 * np.pi)  # plot on theta/2pi in [0,1] for readability
    fig, axes = plt.subplots(1, 2, figsize=(13.5, 4.8))

    # ---- (a) sinusoidal: clean, symmetric cosine ---------------------
    ax = axes[0]
    ax.plot(x, Omega_sin, color="tab:blue", lw=2.0,
            label=r"$\Omega(\theta)$")
    ax.axhline(0.0, color="gray", lw=0.7)
    ax.axhline(wLp_s, color="tab:green", lw=0.9, ls=":")
    ax.axhline(wLm_s, color="tab:green", lw=0.9, ls=":")
    ax.plot([th_p_s / (2 * np.pi)], [wLp_s], "^", color="tab:green", ms=9,
            label=fr"$+\omega_L = {wLp_s:+.2f}$")
    ax.plot([th_m_s / (2 * np.pi)], [wLm_s], "v", color="tab:red", ms=9,
            label=fr"$-\omega_L = {wLm_s:+.2f}$")
    # lock-range span annotation
    ax.annotate("", xy=(0.04, wLp_s), xytext=(0.04, wLm_s),
                arrowprops=dict(arrowstyle="<->", color="black", lw=1.2))
    ax.text(0.07, 0.0, "lock\nrange", fontsize=8, va="center")
    ax.set_xlabel(r"相位差 $\theta/2\pi$")
    ax.set_ylabel(r"$\Omega(\theta)$  [rad/s]")
    ax.set_title("(a) 正弦注入：$\\Omega$ 為乾淨餘弦，對稱於 0\n"
                 r"$\omega_L^+ = -\,\omega_L^-$（經典 Adler）")
    ax.legend(fontsize=8, loc="lower right")

    # ---- (b) harmonic-rich: asymmetric Omega -------------------------
    ax = axes[1]
    ax.plot(x, Omega_rich, color="tab:purple", lw=2.0,
            label=r"$\Omega(\theta)$")
    ax.axhline(0.0, color="gray", lw=0.7)
    ax.axhline(wLp_r, color="tab:green", lw=0.9, ls=":")
    ax.axhline(wLm_r, color="tab:red", lw=0.9, ls=":")
    ax.plot([th_p_r / (2 * np.pi)], [wLp_r], "^", color="tab:green", ms=9,
            label=fr"$+\omega_L^+ = {wLp_r:+.2f}$")
    ax.plot([th_m_r / (2 * np.pi)], [wLm_r], "v", color="tab:red", ms=9,
            label=fr"$\omega_L^- = {wLm_r:+.2f}$")
    ax.annotate("", xy=(0.04, wLp_r), xytext=(0.04, 0.0),
                arrowprops=dict(arrowstyle="<->", color="tab:green", lw=1.2))
    ax.annotate("", xy=(0.10, 0.0), xytext=(0.10, wLm_r),
                arrowprops=dict(arrowstyle="<->", color="tab:red", lw=1.2))
    ax.text(0.13, wLp_r * 0.5, r"$|\omega_L^+|$", fontsize=8,
            color="tab:green", va="center")
    ax.text(0.13, wLm_r * 0.5, r"$|\omega_L^-|$", fontsize=8,
            color="tab:red", va="center")
    ax.set_xlabel(r"相位差 $\theta/2\pi$")
    ax.set_ylabel(r"$\Omega(\theta)$  [rad/s]")
    ax.set_title("(b) 諧波豐富注入：$\\Omega$ 不對稱\n"
                 r"$\omega_L^+ \neq -\,\omega_L^-$（Adler 抓不到）")
    ax.legend(fontsize=8, loc="lower right")

    fig.suptitle(r"lock characteristic $\Omega(\theta)$："
                 r"lock range = $\Omega(\theta)$ 的值域（max/min 為邊緣）  "
                 r"[P3] Eq.(33)，toy model", fontsize=11)
    savefig(fig, "lock_characteristic_omega.png")


if __name__ == "__main__":
    main()
