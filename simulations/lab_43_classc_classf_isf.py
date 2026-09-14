"""
lab_43_classc_classf_isf.py

Goal
----
Waveform engineering told with the ISF (site page: real_oscillator_topologies §(d)):

  (a) class-C LC oscillator  — each transistor conducts only a NARROW current
      pulse centred on a tank-voltage extremum, i.e. on a NULL of the ideal
      tank ISF Gamma = -sin(theta).  With the [P1] Eq.(27) noise-modulating
      function alpha (alpha = 1 while the device conducts, 0 otherwise) the
      effective ISF Gamma_eff = Gamma*alpha shrinks with the conduction angle.
      Closed form for a differential pair (two windows of half-width phi,
      centred on theta = 0 and theta = pi):
          Gamma_eff,rms^2 = (1/pi) * (phi - sin(phi) cos(phi))
      -> 1/2 at 2*phi = 180 deg (class-B, = stationary value), -> 0 as phi -> 0.
      The same figure also shows the WORST alignment (windows centred on the
      zero crossings, where |Gamma| = 1).

  (b) class-F LC oscillator — the tank resonates at omega0 AND 3*omega0, so
      the tank voltage is a pseudo-square wave
          f(theta) = sin(theta) + zeta * sin(3 theta)        (zeta = V_p3/V_p1)
      The ISF is derived FROM THE WAVEFORM with the [P1] Appendix-B/C
      closed forms (Eq.(37): Gamma = f'/(f'^2+f''^2); Eq.(38): Gamma ∝ f')
      and its rms is compared with the slope-normalised closed form of
      Babaie-Staszewski (JSSC 48(12) 2013, Sec. II; that PDF is not among the
      site's five source papers, so the original equation number is unverified):
          Gamma_rms^2 = (1/2) (1 + 9 zeta^2) / (1 + 3 zeta)^2 ,
      minimum 1/4 at zeta = 1/3 (3.0 dB below the sinusoidal 1/2).
      A zero-crossing noise window (the switching pair injects its noise at
      the zero crossings) is then applied to get Gamma_eff for both waveforms.

Everything here is a pedagogical toy at the TOPOLOGY level (no PDK, no
transistor netlist): the ideal-LC tank ISF -sin is exact; the class-F ISF is
the [P1] waveform closed form (method B/C of isf_from_waveform), which is an
approximation for a 4th-order tank.

Figure
------
  static/figures/classc_classf_isf.png

Run
---
  PYTHONPATH=. python3 simulations/lab_43_classc_classf_isf.py     (~2 s)
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt

from isf_utils import gamma_rms, effective_isf
from plot_utils import savefig

THETA = np.linspace(0.0, 2.0 * np.pi, 20001, endpoint=True)


# ---------------------------------------------------------------------------
# class-C helpers
# ---------------------------------------------------------------------------
def window_alpha(theta, centres, half_width):
    """[P1] Eq.(27)-style NMF: alpha = 1 inside |theta - centre| < half_width
    (mod 2pi), 0 elsewhere. alpha is dimensionless, 0 <= alpha <= 1."""
    a = np.zeros_like(theta)
    for c in centres:
        d = np.angle(np.exp(1j * (theta - c)))  # wrapped distance in (-pi, pi]
        a[np.abs(d) < half_width] = 1.0
    return a


def classc_geff2_closed(phi):
    """Gamma_eff,rms^2 for Gamma = -sin, two windows (centres 0 and pi) of
    half-width phi: (1/2pi) * 2 * int_{-phi}^{phi} sin^2 = (phi - sin phi cos phi)/pi."""
    return (phi - np.sin(phi) * np.cos(phi)) / np.pi


def classc_geff2_worst_closed(phi):
    """Same windows but centred on the zero crossings (pi/2, 3pi/2):
    (1/2pi) * 2 * int_{-phi}^{phi} cos^2 = (phi + sin phi cos phi)/pi."""
    return (phi + np.sin(phi) * np.cos(phi)) / np.pi


# ---------------------------------------------------------------------------
# class-F helpers
# ---------------------------------------------------------------------------
def classf_wave(theta, zeta):
    """Pseudo-square tank voltage f = sin(theta) + zeta sin(3 theta) and its
    first two derivatives w.r.t. theta (all dimensionless)."""
    f = np.sin(theta) + zeta * np.sin(3 * theta)
    f1 = np.cos(theta) + 3 * zeta * np.cos(3 * theta)
    f2 = -np.sin(theta) - 9 * zeta * np.sin(3 * theta)
    return f, f1, f2


def isf_slope_normalised(theta, zeta):
    """Gamma = f'/f'_max  (slope normalised to its own maximum — the
    convention behind the Babaie-Staszewski closed form and the site's IsfSandbox)."""
    _, f1, _ = classf_wave(theta, zeta)
    return f1 / np.max(np.abs(f1))


def isf_p1_eq37(theta, zeta):
    """[P1] Eq.(37): Gamma = f'/(f'^2 + f''^2) with f normalised to unit peak
    (so q_max = C*V_max keeps its meaning). Exact for a 2nd-order system;
    an approximation for the 4th-order class-F tank."""
    f, f1, f2 = classf_wave(theta, zeta)
    vmax = np.max(np.abs(f))
    f1n, f2n = f1 / vmax, f2 / vmax
    den = f1n ** 2 + f2n ** 2
    # Pathology documented on isf_from_waveform (Eq.(37) "病點"): at zeta = 1/9 the
    # flat top has f' = f'' = 0 simultaneously (maximally flat), the denominator
    # collapses and Gamma spikes. 0/0 is mapped to 0; the spike near 1/9 is real.
    with np.errstate(divide="ignore", invalid="ignore"):
        g = np.where(den > 0, f1n / den, 0.0)
    return g


def babaie_eq3(zeta):
    """Babaie-Staszewski JSSC 2013 (Sec. II) closed form: Gamma_rms^2 = (1/2)(1+9z^2)/(1+3z)^2."""
    return 0.5 * (1 + 9 * zeta ** 2) / (1 + 3 * zeta) ** 2


def main():
    print("[lab_43] class-C / class-F ISF waveform engineering ...")
    th = THETA
    gamma_lc = -np.sin(th)

    # ---------------- (a) class-C: numeric vs closed form -----------------
    print("\n-- class-C: Gamma_eff,rms^2 vs conduction angle (alpha=1 while on) --")
    cond_deg = np.array([180.0, 120.0, 90.0, 60.0, 40.0, 30.0])
    for cd in cond_deg:
        phi = np.deg2rad(cd) / 2
        a_null = window_alpha(th, [0.0, np.pi], phi)          # pulses on tank-V extrema
        a_zc = window_alpha(th, [np.pi / 2, 3 * np.pi / 2], phi)  # worst: on zero crossings
        g2_null = gamma_rms(th, effective_isf(gamma_lc, a_null)) ** 2
        g2_zc = gamma_rms(th, effective_isf(gamma_lc, a_zc)) ** 2
        print(f"  conduction {cd:5.0f} deg : null-aligned {g2_null:.4f} "
              f"(closed {classc_geff2_closed(phi):.4f}, "
              f"{10*np.log10(0.5/g2_null):5.2f} dB below 0.5) | "
              f"ZC-aligned {g2_zc:.4f} (closed {classc_geff2_worst_closed(phi):.4f})")

    # fundamental-current bookkeeping (same I_bias): class-B square 0/I_bias
    # per device -> 2 I_bias/pi ; class-C impulse train (area I_bias*T/2) -> I_bias
    ratio = 1.0 / (2.0 / np.pi)
    dL = -20 * np.log10(ratio)
    print(f"\n  fundamental ratio class-C/class-B = pi/2 = {ratio:.4f}  ->  "
          f"delta L = -20log10(pi/2) = {dL:.2f} dB")
    print(f"  example B  -148.0 dBc/Hz (SSB /4)  -> {-148.0 + dL:.1f} dBc/Hz ; "
          f"time-domain /2 convention -145.0 -> {-145.0 + dL:.1f} dBc/Hz")

    # ---------------- (b) class-F: ISF from the waveform ------------------
    print("\n-- class-F: Gamma_rms^2 of the pseudo-square waveform --")
    zetas = np.linspace(0.0, 0.6, 121)
    g2_slope = np.array([gamma_rms(th, isf_slope_normalised(th, z)) ** 2 for z in zetas])
    g2_eq37 = np.array([gamma_rms(th, isf_p1_eq37(th, z)) ** 2 for z in zetas])
    g2_eq3 = babaie_eq3(zetas)
    i_min = int(np.argmin(g2_slope))
    print(f"  slope-normalised numeric minimum: zeta = {zetas[i_min]:.3f}, "
          f"Gamma_rms^2 = {g2_slope[i_min]:.4f}")
    for z in (0.0, 1.0 / 9.0, 1.0 / 3.0):
        gs = gamma_rms(th, isf_slope_normalised(th, z)) ** 2
        g7 = gamma_rms(th, isf_p1_eq37(th, z)) ** 2
        e37 = (f"{g7:.4f} ({10*np.log10(0.5/g7):.2f} dB)" if g7 < 10
               else "diverges (flat top has f'=f''=0: the Eq.(37) pathology)")
        print(f"  zeta = {z:.3f}: slope-normalised {gs:.4f} "
              f"({10*np.log10(0.5/gs):.2f} dB below 1/2) | Babaie closed form {babaie_eq3(z):.4f} | "
              f"[P1] Eq.(37) unit-peak {e37}")
    print(f"  max |numeric - Babaie closed form| over the sweep = "
          f"{np.max(np.abs(g2_slope - g2_eq3)):.1e}")

    # zero-crossing noise window (switching pair injects at the ZCs of sin: theta = 0, pi)
    print("\n-- class-F: zero crossing and Gamma_eff (alpha=1 in a +/-30 deg ZC window, slope-normalised) --")
    a_zc30 = window_alpha(th, [0.0, np.pi], np.deg2rad(30.0))
    ge2 = {}
    for z in (0.0, 1.0 / 3.0):
        g = isf_slope_normalised(th, z)
        ge2[z] = gamma_rms(th, effective_isf(g, a_zc30)) ** 2
        f, f1, _ = classf_wave(th, z)
        slope_zc = f1[0] / np.max(np.abs(f))       # ZC slope of the unit-peak waveform
        print(f"  zeta = {z:.3f}: unit-peak ZC slope f'(0) = {slope_zc:.3f} -> physical 1/slope "
              f"|Gamma(ZC)| = {1/slope_zc:.3f} (same V_max, [P1] Eq.(35)/(37) at f''=0) ; "
              f"Gamma_eff,rms^2 (window) = {ge2[z]:.4f}")
    r = ge2[0.0] / ge2[1.0 / 3.0]
    print(f"  Gamma_eff ratio sin/class-F (window, slope-normalised) = {r:.3f} -> {10*np.log10(r):.2f} dB")
    print("  NOTE: Eq.(37) is a 2nd-order closed form; on the 4th-order class-F tank it shows spurious"
          " |Gamma|~1.7 bumps at the flat-top inflection points (denominator lacks the 2nd resonator)."
          " It is kept only as a cross-check in panel (d).")

    # ---------------------------- figure ---------------------------------
    fig, axes = plt.subplots(2, 2, figsize=(13.5, 9.0))

    # (a) class-C: -sin, alpha windows, Gamma_eff
    ax = axes[0, 0]
    phi60 = np.deg2rad(60.0) / 2
    a60 = window_alpha(th, [0.0, np.pi], phi60)
    ax.plot(th / (2 * np.pi), np.cos(th), color="gray", lw=1.0, ls="--",
            label=r"tank 電壓 $\cos\theta$")
    ax.plot(th / (2 * np.pi), gamma_lc, color="tab:blue", label=r"tank ISF $\Gamma=-\sin\theta$")
    ax.fill_between(th / (2 * np.pi), 0, a60, color="tab:orange", alpha=0.25,
                    label=r"class-C 導通窗 $\alpha$（導通角 60°，對準電壓極值）")
    ax.plot(th / (2 * np.pi), effective_isf(gamma_lc, a60), color="tab:red", lw=2.2,
            label=fr"$\Gamma_{{eff}}=\Gamma\alpha$（$\Gamma_{{eff,rms}}^2$={classc_geff2_closed(phi60):.3f}）")
    ax.axhline(0, color="k", lw=0.5)
    ax.set_xlabel(r"phase $\theta/2\pi$")
    ax.set_ylabel(r"$\Gamma$, $\alpha$, $V$")
    ax.set_title("(a) class-C：電流脈衝落在 ISF 零點（tank 電壓極值）")
    ax.legend(fontsize=7.5, loc="lower left")

    # (b) class-C Gamma_eff,rms^2 vs conduction angle
    ax = axes[0, 1]
    cd_sweep = np.linspace(5.0, 180.0, 176)
    phi_sweep = np.deg2rad(cd_sweep) / 2
    ax.plot(cd_sweep, classc_geff2_closed(phi_sweep), color="tab:red",
            label=r"對準極值（ISF 零點）：$(\phi-\sin\phi\cos\phi)/\pi$")
    ax.plot(cd_sweep, classc_geff2_worst_closed(phi_sweep), color="tab:purple", ls="--",
            label=r"對準零交越（最糟）：$(\phi+\sin\phi\cos\phi)/\pi$")
    num_null = [gamma_rms(th, effective_isf(gamma_lc, window_alpha(th, [0, np.pi], np.deg2rad(c) / 2))) ** 2
                for c in cond_deg]
    ax.plot(cond_deg, num_null, "o", color="tab:red", ms=5, label="數值（lab_43）")
    ax.axhline(0.5, color="gray", lw=0.8, ls=":", label=r"stationary $\Gamma_{rms}^2=1/2$（class-B）")
    ax.set_xlabel(r"導通角 $2\phi$ (deg)")
    ax.set_ylabel(r"$\Gamma_{eff,rms}^2$")
    ax.set_title(r"(b) class-C：$\Gamma_{eff,rms}^2$ 隨導通角（$\alpha=1$ 導通時，幾何窗因子）")
    ax.legend(fontsize=7.5)

    # (c) class-F waveform and ISF
    ax = axes[1, 0]
    for z, col in ((0.0, "tab:blue"), (1.0 / 3.0, "tab:red")):
        f, _, _ = classf_wave(th, z)
        ax.plot(th / (2 * np.pi), f, color=col, lw=1.0, ls="--",
                label=fr"tank 電壓 $\zeta$={z:.2f}")
        ax.plot(th / (2 * np.pi), isf_slope_normalised(th, z), color=col, lw=2.0,
                label=fr"ISF $f'/f'_{{max}}$，$\zeta$={z:.2f}（$\Gamma_{{rms}}^2$={gamma_rms(th, isf_slope_normalised(th, z))**2:.3f}）")
    ax.fill_between(th / (2 * np.pi), -1.1, 1.1, where=a_zc30 > 0, color="tab:orange", alpha=0.15,
                    label="switching pair 注入窗（零交越 ±30°）")
    ax.axhline(0, color="k", lw=0.5)
    ax.set_ylim(-1.1, 1.1)
    ax.set_xlabel(r"phase $\theta/2\pi$")
    ax.set_ylabel(r"$f$, $\Gamma$")
    ax.set_title(r"(c) class-F：$\omega_0$+$3\omega_0$ 諧振 → 準方波 → ISF 峰變窄、平頂處 ISF≈0（斜率歸一）")
    ax.legend(fontsize=7.5, loc="lower left")

    # (d) class-F Gamma_rms^2 vs zeta
    ax = axes[1, 1]
    ax.plot(zetas, g2_slope, color="tab:red", lw=2.2, label=r"數值：$\Gamma=f'/f'_{max}$（lab_43）")
    ax.plot(zetas, g2_eq3, color="k", ls=":", lw=1.4,
            label=r"Babaie–Staszewski 2013 閉式：$\frac{1}{2}\frac{1+9\zeta^2}{(1+3\zeta)^2}$")
    ax.plot(zetas, g2_eq37, color="tab:green", lw=1.4, ls="--",
            label=r"[P1] Eq.(37) 二階閉式，單位峰值歸一（交叉檢查；$\zeta$=1/9 病點、四階 tank 上偏離）")
    ax.set_ylim(0, 0.6)
    ax.axvline(1 / 3, color="gray", lw=0.8, ls=":")
    ax.text(1 / 3 + 0.01, 0.47, r"$\zeta=1/3$", fontsize=8)
    ax.set_xlabel(r"三次諧波比 $\zeta=V_{p3}/V_{p1}$")
    ax.set_ylabel(r"$\Gamma_{rms}^2$")
    ax.set_title(r"(d) class-F：$\Gamma_{rms}^2$ 隨 $\zeta$（$\zeta=1/3$ 時 1/2→1/4，−3.0 dB）")
    ax.legend(fontsize=7.5)

    savefig(fig, "classc_classf_isf.png")


if __name__ == "__main__":
    main()
