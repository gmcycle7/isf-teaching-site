"""
lab_26_injlock_noise.py

Goal
----
Show that an injection-LOCKED oscillator behaves like a FIRST-ORDER PLL for
its own phase noise: the free-running 1/f^2 phase-noise skirt is HIGH-PASSED
(suppressed below a corner omega_c, untouched above it), and the corner is

    omega_c = omega_L * cos(theta_ss) = sqrt(omega_L^2 - Dw^2)  <=  omega_L .

Model (phase-domain, already time-averaged)
-------------------------------------------
Start from the [P3] generalized Adler equation (Eq. (30), p.2113, averaged
term with a PLUS sign):

    dtheta/dt = (omega0 - omega_inj) + (1/T_inj) *
                integral_{T_inj} Gamma_tilde(omega_inj*t + theta) i_inj(t) dt

For a sinusoidal injection i_inj = I_inj*cos(omega_inj*t) into the ideal-LC
ISF Gamma_tilde(x) = -sin(x)/q_max, the average evaluates to
Omega(theta) = -omega_L*sin(theta) with omega_L = I_inj/(2*q_max)
(consistent with [P3] Eq. (34)-(35), p.2114: omega_L = 0.5*I_inj*|Gamma1_tilde|).
Adding the oscillator's own white-FM noise drive n(t) (the same drive that
gives the free-runner its 1/f^2 skirt) gives the two simulated SDEs:

    free-running :  dphi/dt   = n(t)
    locked       :  dtheta/dt = Dw - omega_L*sin(theta) + n(t),  Dw = omega0-omega_inj

Locked point theta_ss = asin(Dw/omega_L) (stable branch cos(theta_ss)>0,
[P3] Eq. (38)-(40), p.2115). Linearizing theta = theta_ss + dtheta:

    d(dtheta)/dt = -omega_c*dtheta + n(t),   omega_c = omega_L*cos(theta_ss)

which is an Ornstein-Uhlenbeck process with the Lorentzian PSD

    S_theta(f) = S_n / (omega_c^2 + omega^2),   omega = 2*pi*f
    (one-sided in -> one-sided out; the suppression RATIO
     omega^2/(omega_c^2+omega^2) is bookkeeping-convention-free)

versus the free-runner S_phi(f) = S_n / omega^2.

NOTE on scope: [P3] derives the deterministic pulling equation and its
linearization (pull-in frequency omega_p = -Omega'(theta0), Eq. (40) p.2115 =
our omega_c); driving it with NOISE and reading off the shaped PSD is the
classic injection-locking noise result (Kurokawa 1973, external reference,
not among the site's 5 PDFs). Simulation checks the theory line numerically.

Cases
-----
  A: Dw = 0            -> omega_c = omega_L           (full suppression)
  B: Dw = 0.95*omega_L -> omega_c = 0.312*omega_L     (lock-edge degradation)

Figure
------
  static/figures/injlock_noise_shaping.png

Run
---
  PYTHONPATH=<project root> python simulations/lab_26_injlock_noise.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt

from noise_utils import white_noise, estimate_psd
from plot_utils import savefig

RNG = np.random.default_rng(26)


# ---------------------------------------------------------------------------
# Simulation parameters (representative 5-GHz oscillator locked to a clean
# reference; only the SLOW averaged phase dynamics are integrated, so the
# sample rate needs to cover the lock range, not the carrier).
# ---------------------------------------------------------------------------
F_LOCK = 5.0e6                    # f_L = omega_L/2pi  [Hz]  (half lock range)
OMEGA_L = 2.0 * np.pi * F_LOCK    # omega_L            [rad/s]
S_N = 0.5                         # one-sided PSD of white-FM drive n(t) [rad^2/s]
FS = 400.0e6                      # sample rate of the phase SDE [Hz]
N_SAMP = 2 ** 22                  # ~10.5 ms of data
N_TRANS = 2 ** 18                 # transient samples discarded (~0.66 ms)
NPERSEG = 2 ** 15                 # Welch segment (df = 12.2 kHz, 256 averages)


def simulate_locked(dw, omega_l, noise, fs, theta0=0.0):
    """
    Euler-Maruyama integration of the noisy Adler equation

        dtheta/dt = dw - omega_l*sin(theta) + n(t)

    Parameters
    ----------
    dw      : detuning Dw = omega0 - omega_inj                [rad/s]
    omega_l : half lock range omega_L                         [rad/s]
    noise   : pre-generated white-FM samples n_k              [rad/s]
              (var = S_n*fs/2 so that n_k*dt has variance (S_n/2)*dt)
    fs      : sample rate                                     [Hz]

    Returns
    -------
    theta : ndarray [rad]
    """
    dt = 1.0 / fs
    theta = np.empty_like(noise)
    th = theta0
    for k in range(noise.size):
        th += (dw - omega_l * np.sin(th) + noise[k]) * dt
        theta[k] = th
    return theta


def measure_corner_from_ratio(f, ratio, smooth_bins=7):
    """
    The measured high-pass transfer |H|^2 = S_lock/S_free crosses 1/2 exactly
    at f = f_c (since |H|^2 = f^2/(f_c^2+f^2)). Smooth the ratio and find the
    first upward 1/2-crossing by linear interpolation.
    """
    kern = np.ones(smooth_bins) / smooth_bins
    r = np.convolve(ratio, kern, mode="same")
    idx = np.where((r[1:] >= 0.5) & (r[:-1] < 0.5))[0]
    if idx.size == 0:
        return np.nan
    i = idx[0]
    # linear interpolation between bins i and i+1
    f_c = f[i] + (0.5 - r[i]) * (f[i + 1] - f[i]) / (r[i + 1] - r[i])
    return f_c


def main():
    print("[lab_26] injection-locked noise shaping (first-order-PLL behaviour) ...")
    dt = 1.0 / FS
    t_total = N_SAMP * dt

    # One common white-FM drive for all runs -> identical far-out skirts,
    # so the suppression ratio S_lock/S_free divides out estimator noise.
    n = white_noise(N_SAMP, S_N, FS, RNG)   # var = S_N*FS/2  [rad/s]^2

    # ---------------- free-running oscillator --------------------------
    phi_free = np.cumsum(n) * dt                       # [rad]

    # ---------------- locked, case A: Dw = 0 ---------------------------
    dw_a = 0.0
    theta_a = simulate_locked(dw_a, OMEGA_L, n, FS)
    wc_a = np.sqrt(OMEGA_L ** 2 - dw_a ** 2)           # = omega_L
    fc_a = wc_a / (2 * np.pi)

    # ---------------- locked, case B: Dw = 0.95*omega_L ----------------
    dw_b = 0.95 * OMEGA_L
    theta_ss_b = np.arcsin(dw_b / OMEGA_L)             # stable locked phase
    theta_b = simulate_locked(dw_b, OMEGA_L, n, FS, theta0=theta_ss_b)
    wc_b = np.sqrt(OMEGA_L ** 2 - dw_b ** 2)           # = omega_L*cos(theta_ss)
    fc_b = wc_b / (2 * np.pi)

    # sanity: no cycle slips (noise barrier is huge for these parameters)
    slip_a = np.max(np.abs(theta_a[N_TRANS:] - np.mean(theta_a[N_TRANS:])))
    slip_b = np.max(np.abs(theta_b[N_TRANS:] - theta_ss_b))
    print(f"  sanity   : max|theta-theta_ss| = {slip_a:.2e} / {slip_b:.2e} rad "
          f"(both << pi -> no cycle slips)")
    th_mean_b = np.mean(theta_b[N_TRANS:])
    print(f"  locked phase B: mean(theta) = {th_mean_b:.4f} rad ; "
          f"theta_ss = asin(0.95) = {theta_ss_b:.4f} rad")

    # ---------------- PSDs ---------------------------------------------
    f, S_free = estimate_psd(phi_free[N_TRANS:], FS, nperseg=NPERSEG)
    _, S_la = estimate_psd(theta_a[N_TRANS:] - np.mean(theta_a[N_TRANS:]), FS,
                           nperseg=NPERSEG)
    _, S_lb = estimate_psd(theta_b[N_TRANS:] - np.mean(theta_b[N_TRANS:]), FS,
                           nperseg=NPERSEG)
    f, S_free, S_la, S_lb = f[1:], S_free[1:], S_la[1:], S_lb[1:]  # drop DC bin
    w = 2 * np.pi * f

    # theory (one-sided everywhere, same convention as the generator/Welch)
    Tfree = S_N / w ** 2
    Ta = S_N / (wc_a ** 2 + w ** 2)
    Tb = S_N / (wc_b ** 2 + w ** 2)

    # ---------------- numeric checks -----------------------------------
    # (1) free-run skirt matches S_n/omega^2
    band = (f > 0.5e6) & (f < 5e6)
    r_free = np.mean(S_free[band] / Tfree[band])
    print(f"  free-run : <S_meas/S_theory> (0.5-5 MHz) = {r_free:.3f}  (expect ~1)")

    # (2) locked plateau matches S_n/omega_c^2
    plat_band_a = (f > fc_a / 20) & (f < fc_a / 5)
    plat_meas_a = np.mean(S_la[plat_band_a])
    plat_th_a = S_N / wc_a ** 2
    plat_band_b = (f > fc_b / 20) & (f < fc_b / 5)
    plat_meas_b = np.mean(S_lb[plat_band_b])
    plat_th_b = S_N / wc_b ** 2
    print(f"  plateau A: {plat_meas_a:.3e} rad^2/Hz  vs  S_n/wc^2 = {plat_th_a:.3e} "
          f"(ratio {plat_meas_a / plat_th_a:.3f})")
    print(f"  plateau B: {plat_meas_b:.3e} rad^2/Hz  vs  S_n/wc^2 = {plat_th_b:.3e} "
          f"(ratio {plat_meas_b / plat_th_b:.3f})")
    print(f"  edge penalty: plateau B / plateau A = "
          f"{plat_meas_b / plat_meas_a:.2f}  (theory 1/cos^2(theta_ss) = "
          f"{1.0 / np.cos(theta_ss_b) ** 2:.2f}, i.e. "
          f"{10 * np.log10(1.0 / np.cos(theta_ss_b) ** 2):.1f} dB)")

    # (3) corner frequency from the measured high-pass ratio
    ratio_a = S_la / S_free
    ratio_b = S_lb / S_free
    fc_meas_a = measure_corner_from_ratio(f, ratio_a)
    fc_meas_b = measure_corner_from_ratio(f, ratio_b)
    print(f"  corner A : measured {fc_meas_a / 1e6:.3f} MHz  vs  "
          f"omega_c/2pi = {fc_a / 1e6:.3f} MHz  ->  ratio "
          f"{fc_meas_a / fc_a:.3f}")
    print(f"  corner B : measured {fc_meas_b / 1e6:.3f} MHz  vs  "
          f"omega_c/2pi = {fc_b / 1e6:.3f} MHz  ->  ratio "
          f"{fc_meas_b / fc_b:.3f}")

    # (4) suppression at a spot frequency (100 kHz), case A
    i100 = np.argmin(np.abs(f - 1.0e5))
    sup_meas = 10 * np.log10(np.mean(ratio_a[max(0, i100 - 3):i100 + 4]))
    sup_th = 10 * np.log10((w[i100] ** 2) / (wc_a ** 2 + w[i100] ** 2))
    print(f"  suppression @100 kHz (A): measured {sup_meas:.1f} dB, "
          f"theory {sup_th:.1f} dB")

    # ---------------- figure --------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(13.5, 5.0))

    ax = axes[0]
    ax.loglog(f, S_free, color="0.55", lw=1.0, label="自由跑 $S_\\phi$（量測）")
    ax.loglog(f, S_la, color="tab:blue", lw=1.0,
              label=r"鎖定 $\Delta\omega=0$（量測）")
    ax.loglog(f, S_lb, color="tab:orange", lw=1.0,
              label=r"鎖定 $\Delta\omega=0.95\,\omega_L$（量測）")
    ax.loglog(f, Tfree, "k--", lw=1.2, label=r"理論 $S_n/\omega^2$")
    ax.loglog(f, Ta, "--", color="navy", lw=1.4,
              label=r"理論 $S_n/(\omega_c^2+\omega^2)$")
    ax.loglog(f, Tb, "--", color="darkred", lw=1.4)
    ax.axvline(fc_a, color="navy", ls=":", lw=1.0)
    ax.axvline(fc_b, color="darkred", ls=":", lw=1.0)
    ax.text(fc_a * 1.1, 3e-13, r"$f_c=\omega_c/2\pi$" + f"\n= {fc_a/1e6:.2f} MHz",
            fontsize=8, color="navy")
    ax.text(fc_b * 0.11, 2e-14, f"$f_c$ = {fc_b/1e6:.2f} MHz\n(鎖定邊緣，抑制縮水)",
            fontsize=8, color="darkred")
    ax.set_xlabel("offset 頻率 $f$  [Hz]")
    ax.set_ylabel(r"$S_\theta(f)$  [rad$^2$/Hz]")
    ax.set_title("(a) 鎖定振盪器自身相位雜訊被「高通整形」\n"
                 r"低於 $\omega_c$ 壓平成 $S_n/\omega_c^2$，高於 $\omega_c$ 回到自由跑 $1/f^2$")
    ax.set_xlim(2e4, 2e8)
    ax.legend(fontsize=8, loc="lower left")

    ax = axes[1]
    wth = 2 * np.pi * f
    ax.semilogx(f, 10 * np.log10(ratio_a), color="tab:blue", lw=1.0,
                label=r"量測 $S_{lock}/S_{free}$，$\Delta\omega=0$")
    ax.semilogx(f, 10 * np.log10(ratio_b), color="tab:orange", lw=1.0,
                label=r"量測 $S_{lock}/S_{free}$，$\Delta\omega=0.95\,\omega_L$")
    ax.semilogx(f, 10 * np.log10(wth ** 2 / (wc_a ** 2 + wth ** 2)), "--",
                color="navy", lw=1.4, label=r"理論 $\omega^2/(\omega_c^2+\omega^2)$")
    ax.semilogx(f, 10 * np.log10(wth ** 2 / (wc_b ** 2 + wth ** 2)), "--",
                color="darkred", lw=1.4)
    ax.axhline(-3.0, color="gray", ls=":", lw=0.8)
    ax.plot([fc_meas_a], [-3.0], "o", color="navy", ms=6,
            label=f"量到的 corner A = {fc_meas_a/1e6:.2f} MHz")
    ax.plot([fc_meas_b], [-3.0], "s", color="darkred", ms=6,
            label=f"量到的 corner B = {fc_meas_b/1e6:.2f} MHz")
    ax.set_xlabel("offset 頻率 $f$  [Hz]")
    ax.set_ylabel(r"suppression  $10\log_{10}(S_{lock}/S_{free})$  [dB]")
    ax.set_title("(b) 抑制量＝一階高通 $|H_{hp}|^2$（與記帳慣例無關）\n"
                 r"corner $\omega_c=\sqrt{\omega_L^2-\Delta\omega^2}$：越靠近鎖定邊緣越小")
    ax.set_xlim(2e4, 2e8)
    ax.set_ylim(-45, 5)
    ax.legend(fontsize=8, loc="lower right")

    fig.suptitle("注入鎖定＝一階 PLL：自身雜訊高通、參考雜訊低通（此處參考乾淨）"
                 "；[P3] Eq.(30)/(35)/(40) + 白噪 FM 驅動", fontsize=11)
    savefig(fig, "injlock_noise_shaping.png")

    print(f"  params   : f_L = {F_LOCK/1e6:.1f} MHz, S_n = {S_N} rad^2/s, "
          f"fs = {FS/1e6:.0f} MHz, T = {t_total*1e3:.1f} ms")


if __name__ == "__main__":
    main()
