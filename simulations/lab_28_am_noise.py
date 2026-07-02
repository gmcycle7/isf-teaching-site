"""
lab_28_am_noise.py

振幅雜訊的「完整頻譜」：OU（Ornstein-Uhlenbeck）過程 vs Wiener 相位。

Physics
-------
[P4] Sec. III-F, p.2128（本站已核實）：單一振幅擾動以 d(t)=exp(-t/tau0) 衰減，
tau0 = 2Q/omega0。把「白噪連續驅動 + 指數恢復力」合起來就是 OU 過程
（標準隨機過程數學，外部文獻：G. E. Uhlenbeck and L. S. Ornstein,
"On the theory of the Brownian motion," Phys. Rev., vol. 36, pp. 823-841, 1930）：

    da   = -(a/tau0) dt + sqrt(c) dW   ->  S_a,2s(w)   = c*tau0^2/(1+w^2*tau0^2)
    dphi =               sqrt(c) dW    ->  S_phi,2s(w) = c/w^2

（振幅無恢復力的相位是同一顆白噪源、拿掉 -(a/tau0)dt 項。）

Conventions（factor-of-2 紀律）
------------------------------
* 上面兩式是「雙邊 (two-sided)」PSD；scipy welch 回傳「單邊 (one-sided)」
  = 2x 雙邊，所以圖上理論線畫 2c/w^2 與 2c*tau0^2/(1+w^2 tau0^2)。
* 轉角頻率 f_c、PM/AM 交叉頻率、PM/AM 比值都是「比出來的」，
  對單邊/雙邊、L=S/2 或 /4 慣例完全不敏感。

Key closed-form results (Q=10, f0=5 GHz)
----------------------------------------
tau0 = 2Q/omega0 = 0.6366 ns
f_c  = 1/(2*pi*tau0) = f0/(2Q) = 250 MHz     (AM corner, Hz form)
Var[a] = c*tau0/2  (有限)  vs  Var[phi] = c*t (發散)
equal drive:   PM skirt 漸近線 c/w^2 與 AM 平頂 c*tau0^2 恰在 f_c 相交；
               實際曲線不相交（S_a < S_phi，w>>w_c 時比值 -> 1，AM 最多 +3 dB）。
R = c_a/c_phi > 1:  crossover  f_x = f_c/sqrt(R-1)；R=10 -> 83.3 MHz。

Figure
------
static/figures/am_noise_spectrum.png
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch, lfilter
from plot_utils import savefig

RNG = np.random.default_rng(28)


def smooth_log(y, nbin=15):
    """Simple moving-average smoother (for locating corners/crossings in noisy PSDs)."""
    k = np.ones(nbin) / nbin
    return np.convolve(y, k, mode="same")


def main():
    print("[lab_28] AM noise spectrum: OU process vs Wiener phase ...")

    # ---------------- physical parameters (canonical numbers) ----------------
    f0 = 5e9                    # carrier [Hz]
    Q = 10.0                    # loaded Q [-]
    omega0 = 2 * np.pi * f0     # [rad/s]
    tau0 = 2 * Q / omega0       # [P4] Sec. III-F p.2128: amplitude decay time [s]
    fc = 1.0 / (2 * np.pi * tau0)  # = f0/(2Q), AM corner [Hz]
    c = 0.5                     # common white drive, two-sided level
    #                             [rad^2/s] for phase, [1/s] for fractional amp.
    #                             c = 2D with the site's true-LC D = 0.25 rad^2/s.

    # ---------------- simulation grid ----------------
    fs = 20e9                   # sample rate [Hz] (>> f_c = 250 MHz)
    dt = 1.0 / fs               # [s]
    n = 2 ** 22                 # ~4.2e6 samples, T = 210 us >> tau0

    xi = RNG.standard_normal(n)         # THE single white source
    dW = xi * np.sqrt(dt)               # Wiener increments [sqrt(s)]

    # Wiener phase: no restoring force -> pure integration
    phi = np.cumsum(np.sqrt(c) * dW)    # [rad]

    # OU amplitude: exact discretization a[k+1] = alpha a[k] + sigma_step xi[k]
    alpha = np.exp(-dt / tau0)
    sig_step = np.sqrt(c * tau0 / 2.0 * (1.0 - alpha ** 2))
    a = lfilter([sig_step], [1.0, -alpha], xi)          # equal drive  (R = 1)
    a10 = lfilter([np.sqrt(10.0) * sig_step], [1.0, -alpha], xi)  # R = 10

    # ---------------- time-domain checks ----------------
    var_a_theory = c * tau0 / 2.0
    var_a_sim = np.var(a)
    print(f"    tau0 [ns]                    = {tau0 * 1e9:.4f}")
    print(f"    f_c = f0/(2Q) [MHz]          = {fc / 1e6:.1f}")
    print(f"    Var[a] theory c*tau0/2       = {var_a_theory:.3e}")
    print(f"    Var[a] simulated             = {var_a_sim:.3e}")

    # measure tau0 from the autocorrelation: first lag with R_a < e^-1 * R_a(0)
    lags = np.arange(0, 41)
    R = np.array([np.dot(a[: n - m], a[m:]) / (n - m) for m in lags])
    Rn = R / R[0]
    idx = np.argmax(Rn < np.exp(-1.0))
    # linear interpolation between idx-1 and idx
    t_lo, t_hi = (idx - 1) * dt, idx * dt
    r_lo, r_hi = Rn[idx - 1], Rn[idx]
    tau0_meas = t_lo + (r_lo - np.exp(-1.0)) / (r_lo - r_hi) * (t_hi - t_lo)
    print(f"    tau0 from R_a(tau)=e^-1 [ns] = {tau0_meas * 1e9:.4f}")

    # ---------------- PSDs (welch one-sided = 2 x two-sided) ----------------
    nperseg = 2 ** 16
    f, S_phi = welch(phi, fs=fs, nperseg=nperseg, scaling="density")
    _, S_a = welch(a, fs=fs, nperseg=nperseg, scaling="density")
    _, S_a10 = welch(a10, fs=fs, nperseg=nperseg, scaling="density")
    pos = f > 0
    f, S_phi, S_a, S_a10 = f[pos], S_phi[pos], S_a[pos], S_a10[pos]
    w = 2 * np.pi * f

    S_phi_th = 2 * c / w ** 2                              # one-sided theory
    S_a_th = 2 * c * tau0 ** 2 / (1 + (w * tau0) ** 2)     # one-sided theory
    S_a10_th = 10 * S_a_th

    # plateau: average well below the corner (2..20 MHz)
    band = (f > 2e6) & (f < 20e6)
    plateau_sim = np.mean(S_a[band])
    plateau_th = 2 * c * tau0 ** 2
    print(f"    AM plateau theory 2c*tau0^2  = {plateau_th:.3e}  [1/Hz]")
    print(f"    AM plateau simulated         = {plateau_sim:.3e}  [1/Hz]")

    # measured -3 dB corner of S_a
    S_a_sm = smooth_log(S_a)
    above = f > 20e6
    i3 = np.argmax(S_a_sm[above] < plateau_sim / 2.0)
    fc_meas = f[above][i3]
    print(f"    AM corner measured [MHz]     = {fc_meas / 1e6:.1f}")

    # PM/AM ratio at 10 f_c (theory: (w tau0)^2/(1+(w tau0)^2) = 100/101)
    i10 = np.argmin(np.abs(f - 10 * fc))
    ratio_th = (10.0 ** 2) / (1 + 10.0 ** 2)
    ratio_sim = np.mean(S_a[i10 - 8: i10 + 8] / S_phi[i10 - 8: i10 + 8])
    print(f"    S_a/S_phi @ 2.5 GHz theory   = {ratio_th:.3f}")
    print(f"    S_a/S_phi @ 2.5 GHz sim      = {ratio_sim:.3f}")

    # equal-drive: intersection of ASYMPTOTES (skirt c/w^2 vs plateau c*tau0^2)
    f_cross_equal = 1.0 / (2 * np.pi * tau0)
    print(f"    equal-drive asymptote cross  = {f_cross_equal / 1e6:.1f} MHz (= f_c)")

    # R=10 crossover: S_phi = S_a10  ->  f_x = f_c/sqrt(R-1)
    R_drive = 10.0
    fx_th = fc / np.sqrt(R_drive - 1.0)
    ratio10 = smooth_log(S_a10 / S_phi)
    valid = (f > 5e6) & (f < 1e9)
    ix = np.argmax(ratio10[valid] >= 1.0)
    fx_meas = f[valid][ix]
    print(f"    R=10 crossover theory [MHz]  = {fx_th / 1e6:.2f}")
    print(f"    R=10 crossover sim [MHz]     = {fx_meas / 1e6:.2f}")

    # ---------------- dBc/Hz illustration numbers (canonical anchor) --------
    # PM skirt anchored at L(1 MHz) = -148 dBc/Hz ([P1] Eq.(21), SSB /4 convention)
    L_pm_at_fc = -148.0 - 20 * np.log10(fc / 1e6)
    R_dB = 40.0
    plateau_dBc = L_pm_at_fc + R_dB
    fx_40dB = fc / np.sqrt(10 ** (R_dB / 10) - 1.0)
    floor_dB = -170.0
    f_floor_pm = 1e6 * 10 ** ((-148.0 - floor_dB) / 20.0)
    print(f"    L_PM extrapolated @250 MHz   = {L_pm_at_fc:.2f} dBc/Hz  (anchor -148@1MHz, [P1] Eq.21 /4)")
    print(f"    R=40dB AM plateau [dBc/Hz]   = {plateau_dBc:.2f}")
    print(f"    R=40dB crossover [MHz]       = {fx_40dB / 1e6:.2f}")
    print(f"    PM skirt hits -170 floor at  = {f_floor_pm / 1e6:.2f} MHz")

    # ---------------- figure ----------------
    fig, axes = plt.subplots(1, 2, figsize=(13.5, 5.0))

    # (a) simulated PSDs vs theory
    ax = axes[0]
    ax.loglog(f, S_phi, color="tab:blue", lw=0.7, alpha=0.45,
              label=r"模擬 $S_\phi$（Wiener 相位）")
    ax.loglog(f, S_a, color="tab:orange", lw=0.7, alpha=0.55,
              label=r"模擬 $S_a$（OU，等驅動）")
    ax.loglog(f, S_a10, color="tab:green", lw=0.7, alpha=0.45,
              label=r"模擬 $S_a$（OU，驅動 $\times10$）")
    ax.loglog(f, S_phi_th, "k--", lw=1.6,
              label=r"$S_\phi=2c/\omega^2$（相位：無恢復力）")
    ax.loglog(f, S_a_th, color="tab:red", ls="--", lw=1.6,
              label=r"$S_a=2c\tau_0^2/(1+\omega^2\tau_0^2)$（OU，等驅動）")
    ax.loglog(f, S_a10_th, color="tab:purple", ls=":", lw=1.6,
              label=r"OU，AM 驅動 $\times 10$")
    ax.axvline(fc, color="gray", lw=1.0, ls="-.")
    ax.text(fc * 1.15, 2e-13, r"$f_c=f_0/2Q$" + f"\n= {fc/1e6:.0f} MHz",
            fontsize=8, color="gray")
    ax.plot([fx_th], [np.interp(fx_th, f, S_phi_th)], "v", color="tab:purple",
            ms=8, label=f"R=10 交叉 = {fx_th/1e6:.1f} MHz")
    ax.set_xlim(1e6, 1e10)
    ax.set_ylim(1e-21, 1e-11)
    ax.set_xlabel(r"頻率 $f$ [Hz]（= 對載波 offset $\Delta f$）")
    ax.set_ylabel(r"單邊 PSD  [rad$^2$/Hz 或 1/Hz]")
    ax.set_title("同一顆白噪：相位積分成 $1/f^2$，振幅被恢復力鎖成平頂 Lorentzian")
    ax.legend(fontsize=8, loc="lower left")
    ax.grid(True, which="both", alpha=0.3)

    # (b) dBc/Hz composite: why measured spectra flatten BEFORE the floor
    ax = axes[1]
    fb = np.logspace(5, 10, 600)
    L_pm = -148.0 - 20 * np.log10(fb / 1e6)
    L_am_lin = 10 ** (plateau_dBc / 10) / (1 + (fb / fc) ** 2)
    L_am = 10 * np.log10(L_am_lin)
    L_tot = 10 * np.log10(10 ** (L_pm / 10) + L_am_lin)
    ax.semilogx(fb, L_pm, color="tab:blue", lw=1.4, ls="--",
                label="PM skirt（-148 dBc/Hz @1 MHz，$-20$ dB/dec）")
    ax.semilogx(fb, L_am, color="tab:orange", lw=1.4, ls="--",
                label=f"AM 平頂 Lorentzian（驅動比 R = {R_dB:.0f} dB）")
    ax.semilogx(fb, L_tot, color="k", lw=2.0, label="量測到的總邊帶 = PM + AM")
    ax.axhline(floor_dB, color="tab:red", lw=1.2, ls=":",
               label=f"儀器/加性底線 {floor_dB:.0f} dBc/Hz")
    ax.axvline(fc, color="gray", lw=1.0, ls="-.")
    ax.text(fc * 1.2, -120, f"$f_c$ = {fc/1e6:.0f} MHz", fontsize=8, color="gray")
    ax.axvline(fx_40dB, color="tab:purple", lw=1.0, ls="-.")
    ax.text(fx_40dB * 1.2, -100, f"交叉 {fx_40dB/1e6:.1f} MHz", fontsize=8,
            color="tab:purple")
    ax.annotate("AM 平頂主導：頻譜在底線之前就變平",
                xy=(3e7, plateau_dBc), xytext=(1.5e8, -125), fontsize=9,
                arrowprops=dict(arrowstyle="->", color="tab:orange"))
    ax.set_xlim(1e5, 1e10)
    ax.set_ylim(-200, -80)
    ax.set_xlabel(r"offset $\Delta f$ [Hz]")
    ax.set_ylabel(r"$\mathcal{L}(\Delta f)$ [dBc/Hz]")
    ax.set_title("量測頻譜變平的第二個原因：AM 平頂（示意，錨定 canonical 例 B）")
    ax.legend(fontsize=8, loc="upper right")
    ax.grid(True, which="both", alpha=0.3)

    savefig(fig, "am_noise_spectrum.png")


if __name__ == "__main__":
    main()
