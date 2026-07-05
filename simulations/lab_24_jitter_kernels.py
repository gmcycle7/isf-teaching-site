"""
lab_24_jitter_kernels.py

Goal
----
Close the site's last open jitter-convention TODO (worked_examples 例 C3) by
verifying, from first principles and Monte-Carlo, the three jitter kernels

    TIE (absolute)  : kernel 1
    N-period        : kernel |1 - e^{-j2 pi f N T}|^2 = 4 sin^2(pi f N T)
    cycle-to-cycle  : kernel |1 - e^{-j2 pi f T}|^4  = 16 sin^4(pi f T)

with the SINGLE convention: S_phi(f) = ONE-SIDED phase PSD [rad^2/Hz],
integrals over f in [0, inf), prefactor 1/omega0^2 (NOT 2/omega0^2 -- the
extra 2 belongs to the double-sided-PSD or L(f)=S_phi/2 bookkeeping).

Punchline verified here: for white FM (S_phi = 2 kappa^2 / (2 pi f)^2) the
kernel integral gives EXACTLY

    sigma_dphi^2(N) = kappa^2 * N*T      (phase random walk)

i.e. [P2] Eq.(8) p.792 sigma_dphi = kappa*sqrt(dt) with
[P2] Eq.(11)/(12) p.793 kappa = (Gamma_rms/qmax)*sqrt(S_i/2)  (no omega0).

Monte-Carlo
-----------
Part 1: fine-grained white current -> ISF weighting (Gamma = -sqrt(2)*0.5*sin,
        Gamma_rms = 0.5) -> cumulative integral ([P1] Eq.(11)) -> per-period
        phase increments. Verifies Var = kappa^2*T and no period-to-period
        correlation.
Part 2: long phase random walk (2e6 periods) -> TIE growth / N-period /
        period / cycle-to-cycle jitter measured in the time domain.
Part 3: numerical kernel integrals vs closed forms (white FM + flicker 1/f^3
        log formula), plus the factor-of-2 convention cross-checks.
Part 4: canonical example-C spectrum (-100 dBc/Hz @ 1 MHz, 1/f^2):
        TIE 447.9 fs, period jitter closed form 28.3 fs, and the
        band-truncated 27.6 fs of worked_examples 例 C3.
Part 5: two-regime jitter growth sigma(dt) = sqrt(kappa^2*dt + zeta^2*dt^2)
        ([P2] Fig.16 p.802; Eq.(8)/(9) p.792). White FM + flicker FM
        synthesized as per-period phase increments over 2^24 periods;
        sigma(dt) measured across 5 decades of dt; the two slopes (0.5 and
        ~1) fitted; corner dt_c = kappa^2/zeta^2 compared with the
        self-consistent log-corrected theory and mapped to the frequency-
        domain 1/f^3 corner via dt_c = 1/(2*bracket*f_{1/f^3}).

Figures
-------
  static/figures/jitter_kernels_mc.png
  static/figures/jitter_two_regime.png
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt

from plot_utils import savefig
from isf_utils import gamma_lc_ideal
from noise_utils import (white_noise, flicker_noise, estimate_psd,
                         leeson_one_over_f2, integrate_rms_jitter)

try:
    from numpy import trapezoid as _trapz
except ImportError:  # numpy < 2.0
    from numpy import trapz as _trapz

RNG = np.random.default_rng(24)

# ----------------------------------------------------------------------------
# Canonical parameters (AUTHORING SPEC section 8)
# ----------------------------------------------------------------------------
F0 = 5e9                       # oscillation frequency [Hz]
T = 1.0 / F0                   # period [s] = 200 ps
W0 = 2 * np.pi * F0            # [rad/s]
QMAX = 1e-12                   # [C]
SI = 1e-24                     # one-sided current PSD [A^2/Hz]
GRMS = 0.5                     # representative Gamma_rms [-]

KAPPA = (GRMS / QMAX) * np.sqrt(0.5 * SI)   # [rad/sqrt(s)], [P2] Eq.(11)/(12)
KAPPA2 = KAPPA ** 2                          # [rad^2/s]


def rms(x):
    """sqrt(mean(x^2)) -- rms of a zero-mean process (no mean-subtraction bias)."""
    return float(np.sqrt(np.mean(np.asarray(x) ** 2)))


# ----------------------------------------------------------------------------
# Part 1: ISF-weighted white current -> phase increments ([P1] Eq.(11) route)
# ----------------------------------------------------------------------------
def part1_isf_weighted_walk(n_per=32, n_periods=200_000):
    dt = T / n_per
    fs = 1.0 / dt
    n = n_per * n_periods
    t = np.arange(n) * dt
    i_n = white_noise(n, psd=SI, fs=fs, rng=RNG)          # one-sided PSD = SI
    gamma = np.sqrt(2.0) * GRMS * gamma_lc_ideal(W0 * t)  # rms(gamma) = GRMS
    phi = np.concatenate(([0.0], np.cumsum(gamma * i_n * dt / QMAX)))
    phi_edges = phi[::n_per]                              # phi(k*T), k = 0..n_periods
    d1 = np.diff(phi_edges)                               # per-period phase increments
    sig_mc = rms(d1)
    sig_th = KAPPA * np.sqrt(T)
    corr1 = float(np.corrcoef(d1[:-1], d1[1:])[0, 1])
    print("Part 1  ISF-weighted white current (32 samples/period, 200k periods)")
    print(f"  sigma_dphi(1T) MC     = {sig_mc:.4e} rad")
    print(f"  theory kappa*sqrt(T)  = {sig_th:.4e} rad")
    print(f"  ratio MC/theory       = {sig_mc / sig_th:.3f}")
    print(f"  lag-1 corr of period increments = {corr1:+.4f}")
    return d1


# ----------------------------------------------------------------------------
# Part 2: long random-walk MC, time-domain jitter measurements
# ----------------------------------------------------------------------------
def part2_random_walk(n_periods=2_000_000):
    # Per-period increments N(0, kappa^2*T): justified by Part 1 (exact for
    # edge-sampled ISF-weighted white noise; increments independent).
    d = RNG.normal(0.0, KAPPA * np.sqrt(T), n_periods)
    phi = np.concatenate(([0.0], np.cumsum(d)))

    print("Part 2  random-walk Monte-Carlo (2e6 periods)")
    Ns = np.unique(np.round(np.geomspace(1, 10_000, 25)).astype(int))
    sig_mc, sig_th = [], []
    for N in Ns:
        s = rms(phi[N:] - phi[:-N])
        sig_mc.append(s)
        sig_th.append(KAPPA * np.sqrt(N * T))
    sig_mc = np.array(sig_mc)
    sig_th = np.array(sig_th)
    for N in (1, 10, 100):
        i = int(np.where(Ns == N)[0][0])
        print(f"  N={N:<5d} sigma_dphi MC/theory = {sig_mc[i] / sig_th[i]:.3f}")

    sigma_p = rms(d) / W0                    # period jitter [s]
    sigma_p_th = KAPPA * np.sqrt(T) / W0
    c2c = np.diff(d)                         # second difference of phi
    sigma_c2c = rms(c2c) / W0
    sigma_c2c_th = np.sqrt(2.0) * sigma_p_th
    print(f"  period jitter sigma_P = {sigma_p * 1e15:.4f} fs "
          f"(theory {sigma_p_th * 1e15:.4f} fs, ratio {sigma_p / sigma_p_th:.3f})")
    print(f"  cycle-to-cycle sigma  = {sigma_c2c * 1e15:.4f} fs "
          f"(theory sqrt(2)*sigma_P = {sigma_c2c_th * 1e15:.4f} fs, "
          f"ratio {sigma_c2c / sigma_c2c_th:.3f})")
    return Ns, sig_mc, sig_th, d, c2c


# ----------------------------------------------------------------------------
# Part 3: numerical kernel integrals vs closed forms + convention cross-checks
# ----------------------------------------------------------------------------
def part3_kernel_integrals():
    print("Part 3  kernel integrals vs closed forms (one-sided S_phi)")
    f = np.geomspace(1e-2, 1e11, 4_000_000)
    s_phi = 2.0 * KAPPA2 / (2 * np.pi * f) ** 2          # white FM, one-sided

    # --- white FM, N-period kernel ---
    for N in (1, 10):
        kern = 4.0 * np.sin(np.pi * f * N * T) ** 2
        tail = KAPPA2 / (np.pi ** 2 * f[-1])             # int_{fhi}^inf S*2 df
        num = _trapz(s_phi * kern, f) + tail             # [rad^2]
        closed = KAPPA2 * N * T                          # THE punchline
        print(f"  white FM N={N:<3d} numeric/closed(kappa^2*N*T) = {num / closed:.4f}")

    # --- cycle-to-cycle kernel 16 sin^4 ---
    kern4 = 16.0 * np.sin(np.pi * f * T) ** 4
    tail4 = 3.0 * KAPPA2 / (np.pi ** 2 * f[-1])          # mean(16 sin^4) = 6
    num4 = _trapz(s_phi * kern4, f) + tail4
    closed4 = 2.0 * KAPPA2 * T
    print(f"  c2c 16sin^4    numeric/closed(2*kappa^2*T)   = {num4 / closed4:.4f}")

    # --- flicker FM 1/f^3 with lower cutoff: log closed form ---
    b3, f_l, N = 1.0, 100.0, 1                            # b3 [rad^2*Hz^2]
    ff = np.geomspace(f_l, 1e11, 4_000_000)
    numf = _trapz((b3 / ff ** 3) * 4.0 * np.sin(np.pi * ff * N * T) ** 2, ff) \
        + b3 / ff[-1] ** 2
    euler_gamma = 0.5772156649015329
    closedf = 4 * np.pi ** 2 * b3 * (N * T) ** 2 * \
        (1.5 - euler_gamma - np.log(2 * np.pi * N * T * f_l))
    print(f"  flicker N=1    numeric/asymptotic            = {numf / closedf:.4f}")
    r10 = 10.0 * np.sqrt((1.5 - euler_gamma - np.log(2 * np.pi * 10 * T * f_l)) /
                         (1.5 - euler_gamma - np.log(2 * np.pi * 1 * T * f_l)))
    print(f"  flicker sigma(N=10)/sigma(N=1) = {r10:.2f} (white FM would be 3.16)")

    # --- factor-of-2 convention cross-check: same physics, three bookkeepings ---
    kern1 = 4.0 * np.sin(np.pi * f * T) ** 2
    tail1 = KAPPA2 / (np.pi ** 2 * f[-1])
    one_sided = np.sqrt(_trapz(s_phi * kern1, f) + tail1) / W0
    dbl_sided = np.sqrt(2.0 * (_trapz((s_phi / 2) * kern1, f) + tail1 / 2)) / W0
    l_lin = s_phi / 2.0                                   # L = S_phi/2 (per-Hz)
    l_form = np.sqrt(8.0 * (_trapz(l_lin * np.sin(np.pi * f * T) ** 2, f)
                            + tail1 / 8)) / W0
    print(f"  sigma_P one-sided / double-sided / L-form = "
          f"{one_sided * 1e15:.4f} / {dbl_sided * 1e15:.4f} / {l_form * 1e15:.4f} fs")

    # --- the two SSB conventions of the site, from the same S_phi ---
    dw = 2 * np.pi * 1e6
    L_half = 10 * np.log10((GRMS ** 2 / QMAX ** 2) * SI / (2 * dw ** 2))
    L_quarter = 10 * np.log10((GRMS ** 2 / QMAX ** 2) * SI / (4 * dw ** 2))
    print(f"  L(1MHz) time-domain /2 convention = {L_half:.1f} dBc/Hz")
    print(f"  L(1MHz) [P1] Eq.(21) /4 convention = {L_quarter:.1f} dBc/Hz")


# ----------------------------------------------------------------------------
# Part 4: canonical example-C spectrum (-100 dBc/Hz @ 1 MHz, 1/f^2)
# ----------------------------------------------------------------------------
def part4_example_c():
    print("Part 4  example-C spectrum (-100 dBc/Hz @ 1 MHz, 1/f^2, f0=5 GHz)")
    fgrid = np.logspace(6, 8, 4000)
    L = leeson_one_over_f2(fgrid, L_ref_dbc=-100, f_ref=1e6)
    sigma_t, sigma_phi = integrate_rms_jitter(fgrid, L, f0=F0, fmin=1e6, fmax=100e6)
    print(f"  TIE 1-100 MHz: sigma_phi = {sigma_phi * 1e3:.2f} mrad ; "
          f"sigma_t = {sigma_t * 1e15:.1f} fs")

    b2 = 2e-10 * (1e6) ** 2                    # S_phi = b2/f^2, one-sided
    sigma_p_closed = np.sqrt(b2 * T ** 3 / 2)
    print(f"  period jitter closed form sqrt(b2*T^3/2) = {sigma_p_closed * 1e15:.2f} fs")

    kappa_c = 2 * np.pi * 1e6 * np.sqrt(10 ** (-100 / 10))   # = sqrt(2*pi^2*b2)
    print(f"  kappa_C = 2*pi*df*sqrt(L_lin) = {kappa_c:.2f} rad/sqrt(s) ; "
          f"kappa_C*sqrt(T)/w0 = {kappa_c * np.sqrt(T) / W0 * 1e15:.2f} fs")

    # worked_examples 例 C3 used a finite numeric band 1e3..1e10 Hz:
    fC3 = np.logspace(3, 10, 2_000_000)
    S = b2 / fC3 ** 2
    kern = np.abs(1 - np.exp(-1j * 2 * np.pi * fC3 * T)) ** 2
    sigma_c3 = np.sqrt(_trapz(S * kern, fC3)) / W0
    print(f"  period jitter numeric band 1e3..1e10 Hz = {sigma_c3 * 1e15:.1f} fs "
          f"(= worked_examples C3; band-truncated closed form)")


# ----------------------------------------------------------------------------
# Part 5: two-regime growth sigma(dt)=sqrt(kappa^2*dt + zeta^2*dt^2)
#         ([P2] Fig.16 p.802; Eq.(8) sigma=kappa*sqrt(dt), Eq.(9) sigma=zeta*dt)
# ----------------------------------------------------------------------------
EULER_GAMMA = 0.5772156649015329


def _bracket(dt, f_l):
    """Log bracket of the flicker-FM closed form: 3/2 - gamma - ln(2*pi*dt*f_l)."""
    return 1.5 - EULER_GAMMA - np.log(2 * np.pi * dt * f_l)


def part5_two_regime(n_periods=2 ** 24):
    print("Part 5  two-regime growth: white + flicker FM ([P2] Fig.16, Eq.(8)/(9))")
    fs = 1.0 / T                                  # edge sampling rate [Hz]
    t_rec = n_periods * T                         # record length [s]
    f_l = 1.0 / t_rec                             # lowest synthesized freq [Hz]

    # -- target flicker level: S_phi = b3/f^3 with spectral corner b3/b2 = 1 MHz
    b2 = KAPPA2 / (2 * np.pi ** 2)                # S_phi = b2/f^2 [rad^2*Hz]
    f3_corner = 1e6                               # target f_{1/f^3} [Hz]
    b3 = b2 * f3_corner                           # [rad^2*Hz^2]
    # per-period phase increments d_k: S_d(f) = 4*pi^2*b3*T^2 / f  [rad^2/Hz];
    # flicker_noise() delivers S = (2/fs)*k_flicker/f  =>  k = 2*pi^2*b3*T^2*fs
    k_flick = 2 * np.pi ** 2 * b3 * T ** 2 * fs

    d_fl = flicker_noise(n_periods, fs=fs, k_flicker=k_flick, rng=RNG)
    d_fl -= d_fl.mean()          # remove average-frequency error (finite record)

    # -- calibrate the actually synthesized flicker level (do not trust nominal)
    fw, Sw = estimate_psd(d_fl, fs, nperseg=2 ** 15)
    band = (fw > 1e6) & (fw < 1e9)
    b_d = float(np.median(Sw[band] * fw[band]))   # S_d = b_d/f  [rad^2]
    b3_cal = b_d / (4 * np.pi ** 2 * T ** 2)      # calibrated b3 [rad^2*Hz^2]
    print(f"  flicker calibration: S_d*f = {b_d:.3e} rad^2 "
          f"(nominal {4 * np.pi ** 2 * b3 * T ** 2:.3e})")
    print(f"  b3(calibrated) = {b3_cal:.3e} rad^2*Hz^2 ; "
          f"f_1/f3 = b3/b2 = {b3_cal / b2:.3e} Hz")
    print(f"  record 2^24 periods = {t_rec:.2e} s ; f_l = 1/T_rec = {f_l:.1f} Hz")

    # -- combined walk: independent white FM + flicker FM increments
    d_w = RNG.normal(0.0, KAPPA * np.sqrt(T), n_periods)
    phi = np.concatenate(([0.0], np.cumsum(d_w + d_fl)))

    Ns = np.unique(np.round(np.geomspace(1, 1e5, 41)).astype(int))
    dts = Ns * T
    sig_t = np.array([rms(phi[N:] - phi[:-N]) for N in Ns]) / W0   # [s]

    # -- fit the two slopes on the log-log curve
    m_w = Ns <= 32          # dt << dt_c/10 : white region
    m_f = Ns >= 3200        # dt >> 10*dt_c : flicker region
    pw = np.polyfit(np.log10(dts[m_w]), np.log10(sig_t[m_w]), 1)
    pf = np.polyfit(np.log10(dts[m_f]), np.log10(sig_t[m_f]), 1)
    print(f"  fitted slope, white   region (N<=32)   = {pw[0]:.3f} (theory 0.5)")
    print(f"  fitted slope, flicker region (N>=3200) = {pf[0]:.3f} "
          f"(clean zeta*dt would be 1.0; log-corrected < 1, see below)")

    # -- corner: MC (intersection of the two fitted lines) vs theory
    x_c = (pf[1] - pw[1]) / (pw[0] - pf[0])
    dt_c_mc = 10 ** x_c
    dt_c = 1e-8
    for _ in range(60):      # self-consistent: dt_c = kappa^2 / zeta_eff^2(dt_c)
        dt_c = KAPPA2 / (4 * np.pi ** 2 * b3_cal * _bracket(dt_c, f_l))
    print(f"  corner MC  (fit intersection)  dt_c = {dt_c_mc:.2e} s "
          f"(N_c = {dt_c_mc / T:.0f} periods)")
    print(f"  corner theory (self-consistent) dt_c = {dt_c:.2e} s "
          f"(N_c = {dt_c / T:.0f}) ; ratio MC/theory = {dt_c_mc / dt_c:.2f}")
    br_c = _bracket(dt_c, f_l)
    print(f"  dt_c * f_1/f3 = {dt_c * b3_cal / b2:.4f} ; "
          f"1/(2*bracket) = {1 / (2 * br_c):.4f} (bracket = {br_c:.2f})")

    # -- exact expected curve: kappa^2*N*T + discrete-bin flicker sum
    kbins = np.arange(1, n_periods // 2 + 1)
    fb = kbins * f_l
    Sd = b_d / fb
    s1 = np.sin(np.pi * fb * T) ** 2
    var_fl = np.empty(Ns.size)
    for i, N in enumerate(Ns):
        w = np.sin(np.pi * fb * N * T) ** 2 / s1   # |sum of N increments|^2
        var_fl[i] = np.sum(Sd * w) * f_l
    sig_exact = np.sqrt(KAPPA2 * dts + var_fl) / W0

    pw_ex = np.polyfit(np.log10(dts[m_w]), np.log10(sig_exact[m_w]), 1)
    pf_ex = np.polyfit(np.log10(dts[m_f]), np.log10(sig_exact[m_f]), 1)
    print(f"  exact-curve slopes over the same windows = "
          f"{pw_ex[0]:.3f} / {pf_ex[0]:.3f} (MC deviations from 0.5/1.0 are "
          f"physics, not noise)")

    i_chk = int(np.argmin(np.abs(Ns - 10_000)))
    var_log = 4 * np.pi ** 2 * b3_cal * dts[i_chk] ** 2 * _bracket(dts[i_chk], f_l)
    var_log2 = 4 * np.pi ** 2 * b3_cal * dts[i_chk] ** 2 \
        * _bracket(dts[i_chk], f_l / 2)
    print(f"  exact bin-sum vs log closed form at N={Ns[i_chk]}: "
          f"ratio = {var_fl[i_chk] / var_log:.3f} (f_l=1/T_rec) ; "
          f"{var_fl[i_chk] / var_log2:.3f} (half-bin f_l/2)")
    print(f"  MC vs exact curve at N={Ns[i_chk]}: "
          f"ratio = {sig_t[i_chk] / sig_exact[i_chk]:.3f}")

    # -- why the paper's clean slope-1 fit is fine on hardware: local slope
    #    1 - 1/(2*bracket) with a measurement-length f_l (~1 Hz)
    sl_hw = 1 - 1 / (2 * _bracket(1e-7, 1.0))
    print(f"  hardware-f_l check: local flicker slope at dt=1e-7 s, f_l=1 Hz "
          f"= {sl_hw:.3f}")

    # -- [P2] Fig.16 oscillator 12 numbers (kappa/zeta read off the paper)
    kappa_p, zeta_p, f0_p = 6.18e-9, 2.5e-5, 2.8e9   # [sqrt(s)], [-], [Hz]
    dt_cp = (kappa_p / zeta_p) ** 2
    br_p = _bracket(dt_cp, 1.0)
    fc_p = 1.0 / (2 * br_p * dt_cp)
    print(f"  [P2] Fig.16 osc-12: kappa=6.18e-9 sqrt(s), zeta=2.5e-5 -> "
          f"dt_c = kappa^2/zeta^2 = {dt_cp:.2e} s = {dt_cp * f0_p:.0f} periods")
    print(f"  implied f_1/f3 = 1/(2*bracket*dt_c) = {fc_p:.2e} Hz "
          f"(f_l=1 Hz, bracket={br_p:.1f})")

    return dict(Ns=Ns, dts=dts, sig_t=sig_t, sig_exact=sig_exact,
                b3_cal=b3_cal, f_l=f_l, dt_c=dt_c, dt_c_mc=dt_c_mc,
                pw=pw, pf=pf, kappa_p=kappa_p, zeta_p=zeta_p, dt_cp=dt_cp,
                br_p=br_p)


def make_figure_two_regime(r):
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.4))
    dts, sig_t, sig_ex = r["dts"], r["sig_t"], r["sig_exact"]
    dt_c, f_l, b3_cal = r["dt_c"], r["f_l"], r["b3_cal"]

    # (a) canonical-oscillator MC, like [P2] Fig.16
    ax = axes[0]
    ax.loglog(dts, sig_t * 1e15, "+", ms=9, mew=1.6, color="k", label="MC 量測")
    sig_w = KAPPA * np.sqrt(dts) / W0
    zeta_c = np.sqrt(4 * np.pi ** 2 * b3_cal * _bracket(dt_c, f_l))   # [rad/s]
    sig_z = zeta_c * dts / W0
    sig_zlog = np.sqrt(4 * np.pi ** 2 * b3_cal * dts ** 2
                       * _bracket(dts, f_l)) / W0
    ax.loglog(dts, sig_w * 1e15, "-", color="tab:blue", lw=1.4,
              label=r"$\kappa\sqrt{\Delta t}$（斜率 1/2）")
    ax.loglog(dts, sig_z * 1e15, "-", color="tab:red", lw=1.4,
              label=r"$\zeta\Delta t$（斜率 1，$\zeta$ 取角點值）")
    ax.loglog(dts, sig_zlog * 1e15, "--", color="tab:red", lw=1.2,
              label=r"log 修正 flicker（斜率 $1-\frac{1}{2[\cdot]}$）")
    ax.loglog(dts, np.sqrt(sig_w ** 2 + sig_zlog ** 2) * 1e15, ":",
              color="tab:green", lw=1.8,
              label=r"$\sqrt{\kappa^2\Delta t+\zeta_{\rm eff}^2\Delta t^2}$")
    ax.loglog(dts, sig_ex * 1e15, "-", color="0.55", lw=0.9,
              label="exact（離散 bin 和）")
    ax.axvline(dt_c, color="0.4", ls="-.", lw=1.0)
    ax.annotate(fr"$\Delta t_c$={dt_c * 1e9:.0f} ns", (dt_c, 2e-1),
                textcoords="offset points", xytext=(4, 0), fontsize=9)
    ax.set_xlabel(r"$\Delta t$ [s]")
    ax.set_ylabel(r"$\sigma_{\Delta t}$ [fs]")
    ax.set_title(r"(a) canonical 5 GHz：白噪+flicker FM，斜率 "
                 f"{r['pw'][0]:.2f}→{r['pf'][0]:.2f}")
    ax.legend(fontsize=7.5, loc="upper left")

    # (b) replot of [P2] Fig.16 asymptotes (oscillator 12, 2.8 GHz)
    ax = axes[1]
    kp, zp, dt_cp, br_p = r["kappa_p"], r["zeta_p"], r["dt_cp"], r["br_p"]
    dtg = np.geomspace(5e-10, 2e-6, 400)
    ax.loglog(dtg, kp * np.sqrt(dtg), "-", color="tab:blue", lw=1.4,
              label=r"$\kappa\sqrt{\Delta t}$, $\kappa$=6.18e-9 $\sqrt{\rm s}$")
    ax.loglog(dtg, zp * dtg, "-", color="tab:red", lw=1.4,
              label=r"$\zeta\Delta t$, $\zeta$=2.5e-5")
    ax.loglog(dtg, np.sqrt(kp ** 2 * dtg + zp ** 2 * dtg ** 2), ":",
              color="tab:green", lw=2.0,
              label=r"$\sqrt{\kappa^2\Delta t+\zeta^2\Delta t^2}$")
    b3_p = zp ** 2 / (4 * np.pi ** 2 * br_p)      # zeta_eff(dt_cp)=zp @ f_l=1 Hz
    ax.loglog(dtg, np.sqrt(kp ** 2 * dtg + 4 * np.pi ** 2 * b3_p * dtg ** 2
                           * _bracket(dtg, 1.0)), "--", color="0.45", lw=1.1,
              label=r"log 修正版（$f_l$=1 Hz）幾乎重合")
    ax.axvline(dt_cp, color="0.4", ls="-.", lw=1.0)
    ax.annotate(fr"$\Delta t_c=\kappa^2/\zeta^2$={dt_cp * 1e9:.0f} ns",
                (dt_cp, 2e-13), textcoords="offset points", xytext=(4, 0),
                fontsize=9)
    ax.set_xlabel(r"$\Delta t$ [s]")
    ax.set_ylabel(r"$\sigma_{\Delta t}$ [s]")
    ax.set_ylim(5e-14, 3e-10)
    ax.set_title("(b) [P2] Fig.16（osc 12, 2.8 GHz）之 κ/ζ 漸近線重繪")
    ax.legend(fontsize=7.5, loc="upper left")

    fig.suptitle(r"lab_24 Part 5：兩段式 jitter 成長 "
                 r"$\sigma(\Delta t)=\sqrt{\kappa^2\Delta t+\zeta^2\Delta t^2}$"
                 "（[P2] Fig.16, Eq.(8)/(9)）", y=1.02)
    savefig(fig, "jitter_two_regime.png")


# ----------------------------------------------------------------------------
# Figure
# ----------------------------------------------------------------------------
def make_figure(Ns, sig_mc, sig_th, d, c2c):
    fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.2))

    # (a) the three kernels
    ax = axes[0]
    fT = np.geomspace(1e-3, 4, 3000)
    ax.loglog(fT, np.ones_like(fT), "k--", label=r"TIE: $1$")
    ax.loglog(fT, 4 * np.sin(np.pi * fT) ** 2, color="tab:blue",
              label=r"period: $4\sin^2(\pi fT)$")
    ax.loglog(fT, 16 * np.sin(np.pi * fT) ** 4, color="tab:red",
              label=r"c2c: $16\sin^4(\pi fT)$")
    ax.loglog(fT[fT < 0.1], (2 * np.pi * fT[fT < 0.1]) ** 2, ":", color="tab:blue",
              lw=1.2, label=r"低頻 $\propto f^2$")
    ax.loglog(fT[fT < 0.1], (2 * np.pi * fT[fT < 0.1]) ** 4 / 4 * 4, ":",
              color="tab:red", lw=1.2, label=r"低頻 $\propto f^4$")
    ax.set_ylim(1e-6, 40)
    ax.set_xlabel(r"$fT$（正規化頻率, 無因次）")
    ax.set_ylabel(r"$\vert H(f)\vert^2$（無因次）")
    ax.set_title("三種 jitter 的權重核")
    ax.legend(fontsize=8, loc="lower right")

    # (b) MC accumulated phase jitter vs N with kappa*sqrt(NT) overlay
    ax = axes[1]
    ax.loglog(Ns, sig_mc * 1e6, "o", ms=4, color="tab:blue", label="MC 量測")
    ax.loglog(Ns, sig_th * 1e6, "k-", lw=1.4,
              label=r"理論 $\kappa\sqrt{NT}$ ([P2] Eq.(8))")
    ax.set_xlabel(r"$N$（相隔週期數）")
    ax.set_ylabel(r"$\sigma_{\Delta\phi}(N)$ [$\mu$rad]")
    ax.set_title(r"白噪 FM 隨機漫步：$\kappa=0.354$ rad/$\sqrt{\rm s}$")
    ax.legend(fontsize=8)

    # (c) histograms of period and cycle-to-cycle jitter (time units)
    ax = axes[2]
    p_fs = d / W0 * 1e15
    c_fs = c2c / W0 * 1e15
    bins = np.linspace(-1.0, 1.0, 160)
    ax.hist(p_fs[:400_000], bins=bins, density=True, alpha=0.45,
            color="tab:blue", label=fr"period: $\sigma$={rms(p_fs):.3f} fs")
    ax.hist(c_fs[:400_000], bins=bins, density=True, alpha=0.35,
            color="tab:red", label=fr"c2c: $\sigma$={rms(c_fs):.3f} fs")
    xx = np.linspace(-1, 1, 400)
    sp = KAPPA * np.sqrt(T) / W0 * 1e15
    for s, c in ((sp, "tab:blue"), (np.sqrt(2) * sp, "tab:red")):
        ax.plot(xx, np.exp(-xx ** 2 / (2 * s ** 2)) / (s * np.sqrt(2 * np.pi)),
                color=c, lw=1.5)
    ax.set_xlabel("jitter [fs]")
    ax.set_ylabel("機率密度 [1/fs]")
    ax.set_title(r"period vs c2c（理論 $\sigma_{c2c}=\sqrt{2}\,\sigma_P$）")
    ax.legend(fontsize=8)

    fig.suptitle("lab_24：jitter 核 Monte-Carlo 驗證（$f_0$=5 GHz, $\\Gamma_{rms}$=0.5, "
                 "$q_{max}$=1 pC, $S_i$=1e-24 A$^2$/Hz）", y=1.02)
    savefig(fig, "jitter_kernels_mc.png")


def main():
    print("[lab_24] jitter kernels: first-principles + Monte-Carlo verification")
    print(f"  kappa   = {KAPPA:.4e} rad/sqrt(s)   ([P2] Eq.(11)/(12), p.793)")
    print(f"  kappa^2 = {KAPPA2:.4e} rad^2/s")
    part1_isf_weighted_walk()
    Ns, sig_mc, sig_th, d, c2c = part2_random_walk()
    part3_kernel_integrals()
    part4_example_c()
    r5 = part5_two_regime()
    make_figure(Ns, sig_mc, sig_th, d, c2c)
    make_figure_two_regime(r5)


if __name__ == "__main__":
    main()
