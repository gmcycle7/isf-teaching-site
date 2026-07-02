"""
lab_27_pulling_spectrum.py

Goal
----
Show the classic INJECTION-PULLED oscillator spectrum: when the detuning is
outside the lock range (|Dw| > omega_L), the phase difference theta(t) slips
forever, dwelling near the quasi-lock phase and then slipping fast
("sawtooth"), and the output spectrum becomes an ASYMMETRIC comb of sidebands
spaced by the beat frequency

    omega_b = sqrt(Dw^2 - omega_L^2)        ([P4] Eq.(34), p.2130, N = 1)

on ONE side of the injection tone, with one edge tone exactly AT the
injection frequency ([P4] Sec. V-B, p.2130).

Model
-----
Unlocked sinusoidal-injection Adler equation (reduction of the [P3]
generalized Adler Eq. (30), p.2113, for i_inj = I_inj*cos(omega_inj*t) into
the ideal-LC ISF Gamma_tilde = -sin/q_max; see lab_26 for the mapping):

    dtheta/dt = Dw - omega_L*sin(theta),   Dw = omega0 - omega_inj,  |Dw| > omega_L

integrated with RK4 (deterministic; noise is switched off to isolate the
pulling comb). Output voltage V(t) = cos(omega_inj*t + theta(t)); Hann-
windowed FFT reveals the comb. Because theta(t) = omega_b*t + p(t) with p(t)
periodic (period 2*pi/omega_b), the lines sit at omega_inj + k*omega_b.
For the ideal Adler model the comb is EXACTLY one-sided (k >= 0 for Dw > 0)
with geometrically decaying line amplitudes of ratio

    r = omega_L / (Dw + omega_b)

(standard external result, Armand 1969, verified numerically here).

Numbers (chosen as a 3-4-5 triangle so the theory is mentally checkable):
  f_inj = 1.0 MHz, Dw/2pi = +100 kHz (f0 = 1.1 MHz), f_L = 60 kHz
  -> f_b = sqrt(100^2 - 60^2) kHz = 80 kHz,  r = 60/(100+80) = 1/3
     (power drops 20*log10(3) = 9.54 dB per line)
  mean oscillator frequency = f_inj + f_b = 1.08 MHz (pulled 20 kHz from f0
  toward the injection).

Figure
------
  static/figures/pulling_spectrum.png

Run
---
  PYTHONPATH=<project root> python simulations/lab_27_pulling_spectrum.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt

from plot_utils import savefig

# ---------------------------------------------------------------------------
# Parameters (3-4-5 triangle: Dw = 100 kHz, f_L = 60 kHz -> f_b = 80 kHz)
# ---------------------------------------------------------------------------
F_INJ = 1.0e6                     # injection frequency        [Hz]
DF = 100.0e3                      # detuning Dw/2pi = f0-f_inj [Hz]
F_L = 60.0e3                      # half lock range omega_L/2pi [Hz]
FS = 16.0e6                       # sample rate                [Hz]
N_SAMP = 2 ** 21                  # 131 ms -> ~10486 beat periods

OMEGA_INJ = 2 * np.pi * F_INJ
DW = 2 * np.pi * DF
OMEGA_L = 2 * np.pi * F_L
F0 = F_INJ + DF                   # free-running frequency [Hz]


def adler_rhs(theta):
    """dtheta/dt = Dw - omega_L*sin(theta)   [rad/s]"""
    return DW - OMEGA_L * np.sin(theta)


def integrate_theta(n, dt, theta0=0.0):
    """RK4 integration of the (deterministic) unlocked Adler equation."""
    theta = np.empty(n)
    th = theta0
    for k in range(n):
        k1 = adler_rhs(th)
        k2 = adler_rhs(th + 0.5 * dt * k1)
        k3 = adler_rhs(th + 0.5 * dt * k2)
        k4 = adler_rhs(th + dt * k3)
        th += (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        theta[k] = th
    return theta


def line_power(f, pxx, f_center, half_bins=4):
    """Sum spectrum bins within +/-half_bins of f_center (captures leakage)."""
    i = int(np.argmin(np.abs(f - f_center)))
    lo, hi = max(0, i - half_bins), i + half_bins + 1
    return np.sum(pxx[lo:hi])


def main():
    print("[lab_27] injection-pulling spectrum (asymmetric sideband comb) ...")
    dt = 1.0 / FS
    t = np.arange(N_SAMP) * dt
    T_total = N_SAMP * dt

    # ---------------- integrate the unlocked Adler ODE ------------------
    theta = integrate_theta(N_SAMP, dt)

    # beat frequency, method 1: mean slip rate of theta
    f_b_theory = np.sqrt(DF ** 2 - F_L ** 2)                # 80 kHz by 3-4-5
    f_b_time = (theta[-1] - theta[0]) / (2 * np.pi * (t[-1] - t[0]))
    print(f"  f_b theory : sqrt(Dw^2-wL^2)/2pi = {f_b_theory/1e3:.3f} kHz")
    print(f"  f_b (mean dtheta/dt)             = {f_b_time/1e3:.3f} kHz  "
          f"->  ratio {f_b_time/f_b_theory:.4f}")

    # ---------------- build V(t) and its spectrum -----------------------
    V = np.cos(OMEGA_INJ * t + theta)
    win = np.hanning(N_SAMP)
    spec = np.abs(np.fft.rfft(V * win)) ** 2
    fax = np.fft.rfftfreq(N_SAMP, d=dt)
    spec_db = 10 * np.log10(spec / spec.max() + 1e-30)

    # beat frequency, method 2: spacing of the strongest spectral lines
    from scipy.signal import find_peaks
    sel = (fax > 0.7e6) & (fax < 1.6e6)
    pk, _ = find_peaks(spec_db[sel], height=-70,
                       distance=int(30e3 / (fax[1] - fax[0])))
    pk_f = fax[sel][pk]
    pk_db = spec_db[sel][pk]
    order = np.argsort(pk_db)[::-1]
    top_f = np.sort(pk_f[order[:6]])
    spacings = np.diff(top_f)
    f_b_fft = np.mean(spacings)
    print(f"  f_b (FFT line spacing)           = {f_b_fft/1e3:.3f} kHz  "
          f"->  ratio {f_b_fft/f_b_theory:.4f}")
    print("  top lines [MHz / dBc]:")
    for ff, dd in sorted(zip(pk_f, pk_db), key=lambda z: -z[1])[:6]:
        print(f"    {ff/1e6:.4f} MHz   {dd:+7.2f} dB")

    # one edge tone exactly at the injection frequency ([P4] Sec. V-B)
    p_inj = line_power(fax, spec, F_INJ)
    p_k1 = line_power(fax, spec, F_INJ + f_b_theory)
    p_k2 = line_power(fax, spec, F_INJ + 2 * f_b_theory)
    p_k3 = line_power(fax, spec, F_INJ + 3 * f_b_theory)
    p_km1 = line_power(fax, spec, F_INJ - f_b_theory)      # mirror side
    r_pred = OMEGA_L / (DW + 2 * np.pi * f_b_theory)       # = 1/3 here
    print(f"  geometric ratio r = wL/(Dw+wb) = {r_pred:.4f} "
          f"(power step {20*np.log10(r_pred):+.2f} dB/line)")
    print(f"  measured line-power steps: k1->k2 {10*np.log10(p_k2/p_k1):+.2f} dB, "
          f"k2->k3 {10*np.log10(p_k3/p_k2):+.2f} dB")
    print(f"  asymmetry: line at f_inj - f_b vs f_inj + f_b = "
          f"{10*np.log10(p_km1/p_k1):+.1f} dB  (one-sided comb)")
    print(f"  edge tone P(f_inj)/P(f_inj+f_b) = {10*np.log10(p_inj/p_k1):+.2f} dB")

    # mean oscillator frequency: pulled toward the injection
    f_mean = F_INJ + f_b_time
    print(f"  mean oscillator freq = f_inj + f_b = {f_mean/1e6:.4f} MHz "
          f"(free-run f0 = {F0/1e6:.3f} MHz -> pulled by "
          f"{(F0-f_mean)/1e3:.1f} kHz toward the injection)")

    # ---------------- figure --------------------------------------------
    fig = plt.figure(figsize=(13.5, 8.2))
    fig.set_layout_engine("none")  # gridspec + suptitle: manual spacing below
    gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.25], hspace=0.42,
                          wspace=0.25, top=0.90, bottom=0.08,
                          left=0.07, right=0.97)

    # (a) theta(t): dwell + slip staircase
    T_b = 1.0 / f_b_theory
    n_show = int(5 * T_b * FS)
    ax = fig.add_subplot(gs[0, 0])
    ax.plot(t[:n_show] * 1e6, theta[:n_show] / (2 * np.pi), color="tab:blue",
            label=r"$\theta(t)/2\pi$（數值積分）")
    ax.plot(t[:n_show] * 1e6, f_b_theory * t[:n_show], "k--", lw=1.2,
            label=r"平均斜率 $=\omega_b/2\pi$")
    ax.set_xlabel(r"時間 $t$  [$\mu$s]")
    ax.set_ylabel(r"$\theta/2\pi$  [cycle]")
    ax.set_title("(a) 未鎖定：$\\theta(t)$ 每拍滑一圈\n"
                 "平緩段＝「準鎖定」逗留、陡段＝快速滑相（鋸齒狀）")
    ax.legend(fontsize=8, loc="upper left")

    # (b) instantaneous frequency: dwells just above the injection
    ax = fig.add_subplot(gs[0, 1])
    f_inst = (OMEGA_INJ + adler_rhs(theta[:n_show])) / (2 * np.pi)
    ax.plot(t[:n_show] * 1e6, f_inst / 1e6, color="tab:purple")
    ax.axhline(F_INJ / 1e6, color="tab:red", ls="--", lw=1.0,
               label=r"$f_{inj}$ = 1.000 MHz")
    ax.axhline(F0 / 1e6, color="gray", ls="--", lw=1.0,
               label=r"自由跑 $f_0$ = 1.100 MHz")
    ax.axhline((F_INJ + DF - F_L) / 1e6, color="tab:green", ls=":", lw=1.2,
               label=r"逗留頻率 $f_{inj}+\Delta f-f_L$ = 1.040 MHz")
    ax.set_xlabel(r"時間 $t$  [$\mu$s]")
    ax.set_ylabel(r"瞬時頻率  [MHz]")
    ax.set_ylim(0.95, 1.21)
    ax.set_title("(b) 瞬時頻率 $f_{inj}+\\dot\\theta/2\\pi$：\n"
                 "大部分時間逗留在injection側、短暫掃過高頻側")
    ax.legend(fontsize=8, loc="upper right")

    # (c) the pulled spectrum: one-sided comb spaced f_b
    ax = fig.add_subplot(gs[1, :])
    m = (fax > 0.72e6) & (fax < 1.55e6)
    ax.plot(fax[m] / 1e6, spec_db[m], color="tab:blue", lw=0.9)
    ax.axvline(F_INJ / 1e6, color="tab:red", ls="--", lw=1.2)
    ax.text(F_INJ / 1e6 - 0.005, -5, "注入 $f_{inj}$（頻譜一端的邊緣線）",
            color="tab:red", fontsize=9, rotation=90, va="top", ha="right")
    ax.axvline(F0 / 1e6, color="gray", ls="--", lw=1.2)
    ax.text(F0 / 1e6 + 0.005, -5, "自由跑 $f_0$（已被拉離）", color="gray",
            fontsize=9, rotation=90, va="top")
    for k in range(0, 6):
        fk = (F_INJ + k * f_b_theory) / 1e6
        ax.plot([fk], [2.5], marker="v", color="tab:green", ms=7, clip_on=False)
    ax.annotate("", xy=((F_INJ + 2 * f_b_theory) / 1e6, -18),
                xytext=((F_INJ + f_b_theory) / 1e6, -18),
                arrowprops=dict(arrowstyle="<->", color="tab:green", lw=1.2))
    ax.text((F_INJ + 1.5 * f_b_theory) / 1e6, -16,
            r"$\omega_b/2\pi$ = " + f"{f_b_fft/1e3:.1f} kHz",
            color="tab:green", ha="center", fontsize=9)
    ax.set_xlabel("頻率  [MHz]")
    ax.set_ylabel("相對功率  [dB re. max]")
    ax.set_ylim(-75, 4)
    ax.set_title("(c) 被拉扯振盪器的頻譜：間距 $\\omega_b=\\sqrt{\\Delta\\omega^2-\\omega_L^2}$ 的『單邊』sideband comb"
                 "（綠色▽＝理論位置 $f_{inj}+k\\,\\omega_b/2\\pi$；一端貼著注入頻率，"
                 "低頻側幾乎沒有線）[P4] Eq.(34)")

    fig.suptitle("injection pulling：$|\\Delta\\omega| > \\omega_L$ 鎖不住 → 相位鋸齒滑動 → 不對稱梳狀頻譜"
                 "（[P3] Sec. V-G + [P4] Eq.(33)-(34)，toy Adler model）",
                 fontsize=11)
    savefig(fig, "pulling_spectrum.png")

    print(f"  params : f_inj = {F_INJ/1e6} MHz, f0 = {F0/1e6} MHz, "
          f"f_L = {F_L/1e3} kHz, fs = {FS/1e6} MHz, T = {T_total*1e3:.0f} ms")


if __name__ == "__main__":
    main()
