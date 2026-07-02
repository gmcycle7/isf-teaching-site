"""
lab_29_flicker_lineshape.py

Goal
----
Beyond the Lorentzian: what does the oscillator LINE look like when the FM
noise is flicker (1/f) instead of white?  Two oscillators are synthesized with
the SAME SSB phase noise at 10 kHz offset (time-domain /2 convention):

  (i)  white-FM oscillator:
         phase increments ~ N(0, 2 D dt)  ->  Var[dphi(t)] = 2 D |t|  (linear)
         one-sided S_phi(f) = 4D/(2 pi f)^2   [two-sided: 2D/(2 pi f)^2]
         carrier line = Lorentzian, FWHM = D/pi.
  (ii) flicker-FM oscillator:
         S_phidot(f) = K/f  (one-sided)  <=>  S_phi(f) = b3/f^3, b3 = K/(4 pi^2)
         with low-frequency cutoff f_l (here the record length sets it):
         Var[dphi(t)] = 4 pi^2 b3 t^2 [ ln(1/(2 pi f_l t)) + 3/2 - gamma_E ]
         (t^2-times-log growth) -> characteristic function exp(-Var/2) is a
         near-GAUSSIAN envelope -> near-Gaussian line CORE, not Lorentzian.

Matched design: K = W0 * f_match with W0 = 4D the one-sided phidot PSD of the
white case, so both lines have S_phi(f_match) = 4D/(2 pi f_match)^2 and hence
the same L(f_match) = S_phi/2.

Shape metric: ratio of the -10 dB to -3 dB half-widths.
  Lorentzian: S ~ 1/(1+x^2), x = df/HWHM -> -3 dB at x=1, -10 dB at x=3
              => ratio = 3.00 exactly.
  Gaussian  : S ~ exp(-ln2 * x^2)        -> -10 dB at x = sqrt(ln10/ln2)
              => ratio = 1.8226.

Figure
------
  static/figures/flicker_lineshape.png   (2x2 panels)

Conventions (factor-of-2 discipline)
------------------------------------
* All PSDs handled here are ONE-SIDED densities (scipy.signal.welch default).
* L(df) is measured directly from the V(t) spectrum as
  L = S_V(f0+df)/P_carrier, which for offsets >> linewidth equals S_phi/2
  (the site's "time-domain /2" convention).  The [P1] Eq.(21) SSB "/4"
  bookkeeping would quote the same physics 3 dB lower.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
from scipy.signal import welch
from scipy.optimize import curve_fit
from scipy.ndimage import uniform_filter1d
import matplotlib.pyplot as plt

from plot_utils import savefig
from noise_utils import estimate_psd

RNG = np.random.default_rng(29)
EULER_GAMMA = 0.5772156649015329


# ---------------------------------------------------------------------------
# Calibrated one-sided-PSD synthesis (frequency-domain shaping)
# ---------------------------------------------------------------------------
def synth_from_one_sided_psd(n, fs, psd_func, rng):
    """
    Generate n real samples whose one-sided PSD is exactly psd_func(f)
    [units^2/Hz] on the FFT grid f_m = m*fs/n (m = 1..n/2).  DC bin is zeroed,
    so the lowest represented frequency is fs/n (the record length sets the
    low-frequency cutoff).

    Calibration: E|X_m|^2 = S(f_m) * fs * n / 2  makes welch(scaling='density')
    recover S(f) as a one-sided density (checked numerically in main()).
    """
    freqs = np.fft.rfftfreq(n, d=1.0 / fs)
    amp = np.zeros_like(freqs)
    nz = freqs > 0
    amp[nz] = np.sqrt(psd_func(freqs[nz]) * fs * n / 2.0)
    X = amp * (rng.standard_normal(freqs.size) + 1j * rng.standard_normal(freqs.size)) / np.sqrt(2.0)
    X[0] = 0.0
    if n % 2 == 0:
        X[-1] = amp[-1] * rng.standard_normal()  # Nyquist bin must be real
    return np.fft.irfft(X, n=n)


# ---------------------------------------------------------------------------
# Theory helpers
# ---------------------------------------------------------------------------
def flicker_var_closed_form(tau, b3, fl_eff):
    """Var[dphi(tau)] = 4 pi^2 b3 tau^2 [ln(1/(2 pi fl_eff tau)) + 3/2 - gamma_E]."""
    tau = np.asarray(tau, dtype=float)
    lg = np.log(1.0 / (2 * np.pi * fl_eff * tau)) + 1.5 - EULER_GAMMA
    return 4 * np.pi ** 2 * b3 * tau ** 2 * lg


def flicker_envelope(tau, b3, fl_eff):
    """Characteristic-function envelope E(tau) = exp(-Var/2) (E(0)=1)."""
    tau = np.asarray(tau, dtype=float)
    E = np.ones_like(tau)
    pos = tau > 0
    E[pos] = np.exp(-0.5 * flicker_var_closed_form(tau[pos], b3, fl_eff))
    return E


def line_from_envelope(dfreqs, tau, E):
    """
    L_lin(df) = 2 * Int_0^inf E(tau) cos(2 pi df tau) dtau.
    (Because S_V(f0+df) = 0.5*FT[E] and P_carrier = 1/2 => L = FT[E].)
    White check: E = exp(-D|tau|) gives L = 2D/(D^2 + (2 pi df)^2). exact.
    """
    out = np.empty(len(dfreqs))
    for i, df in enumerate(dfreqs):
        out[i] = 2.0 * np.trapezoid(E * np.cos(2 * np.pi * df * tau), tau)
    return out


def var_exact_discrete(lags_s, fs, n, psd_func):
    """
    Exact expected increment variance of phi = cumsum(y)/fs for y synthesized
    on the discrete one-sided grid f_m = m*fs/n with PSD psd_func:
      Var(L) = sum_m S(f_m) * df * dt^2 * sin^2(pi f_m L dt) / sin^2(pi f_m dt)
    (window-sum Dirichlet kernel; independent bins).
    """
    freqs = np.fft.rfftfreq(n, d=1.0 / fs)[1:]  # skip DC
    S = psd_func(freqs)
    df = fs / n
    dt = 1.0 / fs
    out = []
    for lag in lags_s:
        L = int(round(lag * fs))
        num = np.sin(np.pi * freqs * L * dt) ** 2
        den = np.sin(np.pi * freqs * dt) ** 2
        out.append(np.sum(S * df * dt ** 2 * num / den))
    return np.array(out)


def measured_increment_var(phi, fs, lags_s):
    out = []
    for lag in lags_s:
        L = int(round(lag * fs))
        d = phi[L:] - phi[:-L]
        out.append(np.mean(d * d))
    return np.array(out)


# ---------------------------------------------------------------------------
# Spectral-shape measurement
# ---------------------------------------------------------------------------
def measure_half_widths(off, S, smooth_bins, search_hw, levels=(0.5, 0.1)):
    """Half-widths (Hz) at power levels relative to the peak (both sides averaged)."""
    Ss = uniform_filter1d(S, max(int(smooth_bins), 1))
    idx = np.where(np.abs(off) <= search_hw)[0]
    i_pk = idx[np.argmax(Ss[idx])]
    peak = Ss[i_pk]
    widths = {}
    for lev in levels:
        thr = peak * lev
        j = i_pk
        while j < len(Ss) - 1 and Ss[j] > thr:
            j += 1
        w_pos = np.interp(thr, [Ss[j], Ss[j - 1]], [off[j], off[j - 1]]) - off[i_pk]
        k = i_pk
        while k > 0 and Ss[k] > thr:
            k -= 1
        w_neg = off[i_pk] - np.interp(thr, [Ss[k], Ss[k + 1]], [off[k], off[k + 1]])
        widths[lev] = 0.5 * (w_pos + w_neg)
    return widths, peak, i_pk, Ss


def lorentz_db(x, a_db, w):
    return a_db - 10 * np.log10(1.0 + (x / w) ** 2)


def theory_half_width_ratio(dfreqs, Lvals):
    """-10dB/-3dB half-width ratio of a (smooth) theory line sampled on dfreqs>=0."""
    pk = Lvals[0]
    hw = {}
    for lev in (0.5, 0.1):
        j = np.argmax(Lvals < pk * lev)
        hw[lev] = np.interp(pk * lev, [Lvals[j], Lvals[j - 1]], [dfreqs[j], dfreqs[j - 1]])
    return hw[0.1] / hw[0.5], hw


def main():
    print("[lab_29] flicker-FM lineshape vs white-FM Lorentzian ...")

    # ------------------------------------------------------------------ setup
    fs = 262144.0            # sample rate [Hz]  (2^18)
    n = 2 ** 23              # samples -> T = 32 s record
    T = n / fs
    f0 = 80.0e3              # carrier [Hz]
    f_match = 10.0e3         # offset where both oscillators share the same L
    D = 50.0 * np.pi         # white-FM phase diffusion [rad^2/s] -> FWHM = D/pi = 50 Hz
    W0 = 4.0 * D             # one-sided S_phidot of the white case [rad^2/s]
    K = W0 * f_match         # flicker-FM: S_phidot = K/f  [rad^2 s^-2]
    B3 = K / (4 * np.pi ** 2)  # S_phi = B3/f^3 (one-sided) [rad^2 Hz^2]
    df1 = fs / n             # lowest synthesized frequency = 1/T = 1/32 Hz
    fl_eff = np.exp(-EULER_GAMMA) * df1  # discrete-bin -> continuous-cutoff calibration

    L_th_lin = 2 * D / (2 * np.pi * f_match) ** 2  # = S_phi/2 at f_match (both cases)
    print(f"    D = {D:.2f} rad^2/s -> white FWHM theory = D/pi = {D/np.pi:.1f} Hz")
    print(f"    K = {K:.4g} rad^2/s^2 ; b3 = {B3:.4g} rad^2 Hz^2 ; f_l(record) = {df1:.4g} Hz")
    print(f"    design L({f_match/1e3:.0f} kHz) = {10*np.log10(L_th_lin):.2f} dBc/Hz  (time-domain /2 convention)")

    # ------------------------------------------------------- (i) white FM
    dphi = RNG.standard_normal(n) * np.sqrt(2 * D / fs)   # Var[dphi] = 2 D dt
    phi_w = np.cumsum(dphi)
    del dphi

    t = np.arange(n) / fs
    x = np.cos(2 * np.pi * f0 * t + phi_w)
    fW, Pw = welch(x, fs=fs, nperseg=2 ** 18, scaling="density")
    del x

    # ------------------------------------------------------- (ii) flicker FM
    # Flicker's slowest components (~1/T) do NOT self-average inside one
    # record (Part-B teaching point), so we ensemble-average N_REAL records
    # and also report the single-record spread of the measured linewidth.
    N_REAL = 6
    lags = np.array([5e-5, 1e-4, 2e-4, 5e-4, 1e-3, 2e-3, 5e-3, 1e-2, 2e-2, 5e-2, 1e-1])
    i10ms = np.argmin(np.abs(lags - 1e-2))
    Pf_acc = None
    var_f_acc = np.zeros_like(lags)
    var_f2_acc = 0.0
    fwhm_single = []
    cal_first = None
    phi_f = None
    for r in range(N_REAL):
        y_f = synth_from_one_sided_psd(n, fs, lambda f: K / f, RNG)
        if r == 0:  # synthesis calibration check: welch of y vs K/f near 1 kHz
            fy, Sy = estimate_psd(y_f, fs, nperseg=2 ** 16)
            band = (fy > 800) & (fy < 1250)
            cal_first = np.median(Sy[band] * fy[band]) / K
            del fy, Sy
        phi = np.cumsum(y_f) / fs
        del y_f
        x = np.cos(2 * np.pi * f0 * t + phi)
        _, Pf_r = welch(x, fs=fs, nperseg=2 ** 18, scaling="density")
        del x
        Pf_acc = Pf_r if Pf_acc is None else Pf_acc + Pf_r
        var_f_acc += measured_increment_var(phi, fs, lags)
        if r == 0:
            phi_f = phi  # keep one record for the S_phi panel
        del phi
        # per-record linewidth (single-record scatter demo)
        i0_ = int(round(f0 / (fW[1] - fW[0])))
        span_ = int(round(30e3 / (fW[1] - fW[0])))
        off_ = fW[i0_ - span_: i0_ + span_ + 1] - f0
        L_r = Pf_r[i0_ - span_: i0_ + span_ + 1] / np.trapezoid(Pf_r, fW)
        wid_r, _, _, _ = measure_half_widths(off_, L_r, 51, 8000.0, levels=(0.5,))
        fwhm_single.append(2 * wid_r[0.5])
        # cutoff experiment: same PSD but zero below 1 Hz
        y2 = synth_from_one_sided_psd(n, fs, lambda f: np.where(f >= 1.0, K / f, 0.0), RNG)
        phi2 = np.cumsum(y2) / fs
        del y2
        var_f2_acc += measured_increment_var(phi2, fs, np.array([1e-2]))[0]
        del phi2
    del t
    print(f"{cal_first:.3f}")  # -> synthesized S_phidot*f / K near 1 kHz (calibration ~ 1.0)
    Pf = Pf_acc / N_REAL
    var_f = var_f_acc / N_REAL
    var_f2 = var_f2_acc / N_REAL
    fwhm_single = np.array(fwhm_single)

    dfW = fW[1] - fW[0]                    # 1 Hz bins
    Ptot_w = np.trapezoid(Pw, fW)          # carrier power ~ 1/2
    Ptot_f = np.trapezoid(Pf, fW)
    i0 = int(round(f0 / dfW))
    span = int(round(30e3 / dfW))
    sl = slice(i0 - span, i0 + span + 1)
    off = fW[sl] - f0
    Lw = Pw[sl] / Ptot_w                   # measured L(df), linear [1/Hz]
    Lf = Pf[sl] / Ptot_f

    # ------------------------------------------------------- L(10 kHz) match
    mb = np.abs(np.abs(off) - f_match) < 150.0
    L10_w = 10 * np.log10(np.median(Lw[mb]))
    L10_f = 10 * np.log10(np.median(Lf[mb]))
    print(f"{L10_w:.1f}")   # -> white  L(10 kHz) dBc/Hz
    print(f"{L10_f:.1f}")   # -> flicker L(10 kHz) dBc/Hz (same by design)
    print(f"{L10_w - 10*np.log10(L_th_lin):+.2f}")  # -> white meas - theory (dB): /2 convention check

    # ------------------------------------------------------- S_phi one-sided check
    fP, Sphi_w = estimate_psd(phi_w, fs, nperseg=2 ** 16)
    _, Sphi_f = estimate_psd(phi_f, fs, nperseg=2 ** 16)
    bandP = (fP > 9.5e3) & (fP < 10.5e3)
    Sphi_th_10k = 4 * D / (2 * np.pi * f_match) ** 2      # ONE-SIDED 4D/dw^2
    r_onesided = np.median(Sphi_w[bandP]) / Sphi_th_10k
    print(f"{r_onesided:.3f}")  # -> measured one-sided S_phi(10kHz) / (4D/dw^2): pins the 4 (not 2)

    # ------------------------------------------------------- widths + shapes
    wid_w, pk_w, ipk_w, Lw_sm = measure_half_widths(off, Lw, 7, 500.0)
    wid_f, pk_f, ipk_f, Lf_sm = measure_half_widths(off, Lf, 51, 8000.0)
    fwhm_w = 2 * wid_w[0.5]
    fwhm_f = 2 * wid_f[0.5]
    ratio_w = wid_w[0.1] / wid_w[0.5]
    ratio_f = wid_f[0.1] / wid_f[0.5]
    print(f"{fwhm_w:.1f}")        # -> white FWHM [Hz] (theory 50.0 = D/pi)
    print(f"{fwhm_f:.0f}")        # -> flicker FWHM [Hz], 6-record ensemble (same L(10kHz)!)
    print(f"{np.mean(fwhm_single):.0f} +/- {np.std(fwhm_single):.0f}")  # -> single-record flicker FWHM spread [Hz]
    print(f"{fwhm_f/fwhm_w:.1f}") # -> linewidth ratio flicker/white
    print(f"{ratio_w:.2f}")       # -> white  -10dB/-3dB half-width ratio (Lorentzian: 3.00)
    print(f"{ratio_f:.2f}")       # -> flicker -10dB/-3dB half-width ratio (Gaussian: 1.82)

    # ------------------------------------------------------- Lorentzian fits (dB)
    def fit_lorentz(offv, Ssm, hw):
        m = (np.abs(offv) <= 4 * hw) & (Ssm > 0)
        xdat = offv[m]
        ydat = 10 * np.log10(Ssm[m])
        popt, _ = curve_fit(lorentz_db, xdat, ydat, p0=(ydat.max(), hw))
        resid = ydat - lorentz_db(xdat, *popt)
        return popt, np.sqrt(np.mean(resid ** 2))

    popt_w, rms_w = fit_lorentz(off, Lw_sm, wid_w[0.5])
    popt_f, rms_f = fit_lorentz(off, Lf_sm, wid_f[0.5])
    print(f"{rms_w:.2f}")  # -> white  Lorentzian-fit rms error [dB] over +-4 HWHM (small)
    print(f"{rms_f:.2f}")  # -> flicker Lorentzian-fit rms error [dB] over +-4 HWHM (large)
    print(f"{popt_w[1]:.1f}")  # -> white fitted HWHM [Hz] (theory D/(2 pi) = 25.0 Hz)

    # ------------------------------------------------------- theory lines
    tau_g = np.arange(0.0, 1.5e-3, 1.0e-6)
    E_f = flicker_envelope(tau_g, B3, fl_eff)
    dfr = np.logspace(np.log10(20.0), np.log10(3.0e4), 240)
    L_th_f = line_from_envelope(dfr, tau_g, E_f)
    L_th_w = 2 * D / (D ** 2 + (2 * np.pi * dfr) ** 2)
    # Gaussian-core approximation (freeze the log at tau* where E = 1/e)
    i_star = np.argmax(E_f < np.exp(-1.0))
    tau_star = tau_g[i_star]
    lg_star = np.log(1.0 / (2 * np.pi * fl_eff * tau_star)) + 1.5 - EULER_GAMMA
    sig_tau = 1.0 / np.sqrt(4 * np.pi ** 2 * B3 * lg_star)
    E_gauss = np.exp(-0.5 * (tau_g / sig_tau) ** 2)
    L_th_gauss = line_from_envelope(dfr, tau_g, E_gauss)
    fwhm_gauss_pred = 2 * np.sqrt(2 * np.log(2)) * np.sqrt(B3 * lg_star)
    # fine linear grid for theory shape metrics
    dfr_lin = np.arange(0.0, 12000.0, 5.0)
    L_th_f_lin = line_from_envelope(dfr_lin, tau_g, E_f)
    r_th_f, hw_th_f = theory_half_width_ratio(dfr_lin, L_th_f_lin)
    print(f"{r_th_f:.2f}")             # -> theory (char.-function) width ratio for flicker line
    print(f"{2*hw_th_f[0.5]:.0f}")     # -> theory flicker FWHM [Hz]
    L_th_f_10k = np.interp(f_match, dfr_lin, L_th_f_lin)
    print(f"{10*np.log10(L_th_f_10k):.1f}")  # -> exact-line theory L(10 kHz): slightly above pure 1/f^3 skirt
    print(f"    Gaussian-core approx FWHM = {fwhm_gauss_pred:.0f} Hz (freeze log at tau*={tau_star:.2e} s)")

    # ------------------------------------------------------- increment variance
    var_w = measured_increment_var(phi_w, fs, lags)
    var_w_th = 2 * D * lags
    var_f_cf = flicker_var_closed_form(lags, B3, fl_eff)
    var_f_ex = var_exact_discrete(lags, fs, n, lambda f: K / f)
    slope_w = np.mean(var_w / lags)
    print(f"{slope_w/(2*D):.3f}")      # -> white Var[dphi]/t / (2D): linear-growth check
    i1ms = np.argmin(np.abs(lags - 1e-3))
    print(f"{var_f[i1ms]/var_f_cf[i1ms]:.3f}")   # -> flicker Var(1 ms) measured / closed form
    print(f"{var_f[i10ms]/var_f_cf[i10ms]:.3f}") # -> flicker Var(10 ms) measured / closed form
    print(f"{var_f_cf[i10ms]/var_f_ex[i10ms]:.3f}")  # -> closed form / exact discrete sum (10 ms)

    # ------------------------------------------------------- cutoff experiment
    var_f2_ex = var_exact_discrete([1e-2], fs, n, lambda f: np.where(f >= 1.0, K / f, 0.0))[0]
    r_cut = var_f[i10ms] / var_f2
    r_cut_th = var_f_ex[i10ms] / var_f2_ex
    print(f"{r_cut:.2f}")     # -> Var(10 ms) ratio: cutoff 1/32 Hz vs 1 Hz (measured, 6 records)
    print(f"{r_cut_th:.2f}")  # -> same ratio, exact theory: cutoff enters as ln(f_l)

    # ============================================================== figure
    fig, axes = plt.subplots(2, 2, figsize=(13.5, 9.6))

    # (a) PN-plot view: L(df) both oscillators + theory
    ax = axes[0, 0]
    pos = off > 0
    ax.semilogx(off[pos], 10 * np.log10(Lw[pos]), color="tab:blue", lw=0.7, alpha=0.55,
                label="white FM 模擬")
    ax.semilogx(off[pos], 10 * np.log10(Lf[pos]), color="tab:red", lw=0.7, alpha=0.55,
                label="flicker FM 模擬")
    ax.semilogx(dfr, 10 * np.log10(L_th_w), "k--", lw=1.4, label="Lorentzian 理論（white）")
    ax.semilogx(dfr, 10 * np.log10(L_th_f), color="darkred", ls="--", lw=1.4,
                label="特徵函數理論（flicker）")
    ax.axvline(f_match, color="gray", lw=1, ls="-.")
    ax.plot([f_match], [10 * np.log10(L_th_lin)], "o", color="black", ms=6, zorder=5,
            label=f"設計匹配點：L(10 kHz) = {10*np.log10(L_th_lin):.1f} dBc/Hz")
    ax.set_xlim(20, 3e4)
    ax.set_ylim(-90, -5)
    ax.set_xlabel("offset $\\Delta f$ [Hz]")
    ax.set_ylabel("$\\mathcal{L}(\\Delta f)$ [dBc/Hz]")
    ax.set_title("同一個 L(10 kHz)，兩種線形：Lorentzian vs 近高斯")
    ax.legend(fontsize=8, loc="lower left")

    # (b) normalized line cores in units of each line's own HWHM
    ax = axes[0, 1]
    xg = np.linspace(0, 5, 400)
    ax.plot(xg, -10 * np.log10(1 + xg ** 2), "k--", lw=1.5, label="Lorentzian（比值 3.00）")
    ax.plot(xg, -10 * np.log10(2.0) * xg ** 2, color="darkred", ls=":", lw=1.6,
            label="Gaussian（比值 1.82）")
    for (Ldat, wid, ipk, color, lab) in (
            (Lw_sm, wid_w, ipk_w, "tab:blue", "white FM 模擬"),
            (Lf_sm, wid_f, ipk_f, "tab:red", "flicker FM 模擬")):
        hw = wid[0.5]
        pk = Ldat[ipk]
        m = (np.abs(off) < 5 * hw)
        xs = np.abs(off[m]) / hw
        ys = 10 * np.log10(Ldat[m] / pk)
        o = np.argsort(xs)
        ax.plot(xs[o][::7], ys[o][::7], ".", color=color, ms=2.5, alpha=0.5, label=lab)
    ax.axhline(-3.0103, color="gray", lw=0.8, ls="-.")
    ax.axhline(-10.0, color="gray", lw=0.8, ls="-.")
    ax.text(4.55, -2.6, "-3 dB", fontsize=8, color="gray")
    ax.text(4.55, -9.6, "-10 dB", fontsize=8, color="gray")
    ax.set_xlim(0, 5)
    ax.set_ylim(-30, 1)
    ax.set_xlabel("$\\vert\\Delta f\\vert$ / HWHM（各自線寬歸一）")
    ax.set_ylabel("相對峰值 [dB]")
    ax.set_title(f"線核形狀：white 比值 {ratio_w:.2f}（Lorentzian 3.00）"
                 f"；flicker {ratio_f:.2f}（Gaussian 1.82）")
    ax.legend(fontsize=8)

    # (c) increment variance growth
    ax = axes[1, 0]
    ax.loglog(lags, var_w, "o", color="tab:blue", ms=5, label="white：量測 Var[$\\Delta\\phi$]")
    ax.loglog(lags, var_w_th, "k--", lw=1.3, label="white 理論 $2D\\tau$（斜率 1）")
    ax.loglog(lags, var_f, "s", color="tab:red", ms=5, label="flicker：量測 Var[$\\Delta\\phi$]")
    ax.loglog(lags, var_f_cf, color="darkred", ls="--", lw=1.3,
              label="flicker 理論 $4\\pi^2 b_{-3}\\tau^2[\\ln(1/2\\pi f_l\\tau)+3/2-\\gamma_E]$")
    ax.set_xlabel("time lag $\\tau$ [s]")
    ax.set_ylabel("Var[$\\Delta\\phi(\\tau)$] [rad$^2$]")
    ax.set_title("相位增量方差：white 線性成長；flicker $\\tau^2\\times$log 成長")
    ax.legend(fontsize=8, loc="upper left")

    # (d) phase PSDs: 1/f^2 vs 1/f^3 crossing at 10 kHz
    ax = axes[1, 1]
    mP = (fP > 100) & (fP < 4e4)
    ax.loglog(fP[mP], Sphi_w[mP], color="tab:blue", lw=0.8, alpha=0.6, label="white：$S_\\phi$（Welch）")
    ax.loglog(fP[mP], Sphi_f[mP], color="tab:red", lw=0.8, alpha=0.6, label="flicker：$S_\\phi$（Welch）")
    fg = np.logspace(2, np.log10(4e4), 100)
    ax.loglog(fg, 4 * D / (2 * np.pi * fg) ** 2, "k--", lw=1.2,
              label="$4D/(2\\pi f)^2$（單邊，$1/f^2$）")
    ax.loglog(fg, B3 / fg ** 3, color="darkred", ls="--", lw=1.2,
              label="$b_{-3}/f^3$（單邊，$1/f^3$）")
    ax.axvline(f_match, color="gray", lw=1, ls="-.")
    ax.text(f_match * 1.1, 3e-5, "10 kHz 交點\n（同 $S_\\phi$ → 同 $\\mathcal{L}$）", fontsize=8)
    ax.set_xlabel("offset frequency $f$ [Hz]")
    ax.set_ylabel("$S_\\phi(f)$ [rad$^2$/Hz]（單邊）")
    ax.set_title("有限觀察時間的 $S_\\phi$：$1/f^2$ vs $1/f^3$，10 kHz 交會")
    ax.legend(fontsize=8, loc="lower left")

    savefig(fig, "flicker_lineshape.png")


if __name__ == "__main__":
    main()
