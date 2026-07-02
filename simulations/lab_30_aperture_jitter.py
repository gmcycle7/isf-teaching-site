"""
lab_30_aperture_jitter.py

Goal
----
Verify the ADC aperture-jitter SNR formula from first principles by direct
Monte-Carlo sampling:

    sample a full-scale sine V(t) = sin(2*pi*f_in*t) at jittered instants
    t_n = n/fs + dt_n,  dt_n ~ N(0, sigma_t^2)  (white / i.i.d. RJ),
    FFT (coherent bin, rectangular window), and measure

        SNR_meas = P(signal bin) / sum(all other bins)

    against the standard data-converter formula (external textbook result):

        SNR_jitter [dB] = -20*log10(2*pi*f_in*sigma_t)
        ENOB           = (SNR - 1.76) / 6.02

sigma_t = 447.9 fs is the site's canonical example C (5 GHz clock,
L(1 MHz) = -100 dBc/Hz, 1/f^2 skirt, integrated 1 MHz -> 100 MHz; see
simulations/lab_08_jitter_integration.py). The aperture-jitter SNR formula
itself is standard ADC theory (e.g. Kester MT-007; Walden JSAC 1999), not
from the site's five PDFs.

Also prints the design table (f_in = 1 / 2.5 / 5 / 10 GHz -> SNR, ENOB) and
the inverse design point: sigma_t needed for 10 ENOB at f_in = 5 GHz.

Figure
------
  static/figures/aperture_jitter_snr.png
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt
from plot_utils import savefig

RNG = np.random.default_rng(30)

SIGMA_T = 447.9e-15   # s   canonical example C rms jitter
FS = 25.6e9           # Hz  sample rate (Nyquist 12.8 GHz covers f_in <= 10 GHz)
NFFT = 2 ** 14        # samples per record (coherent FFT)


def snr_formula_db(f_in, sigma_t):
    """SNR_jitter = -20*log10(2*pi*f_in*sigma_t)  [dB] (white RJ, sine input)."""
    return -20.0 * np.log10(2.0 * np.pi * f_in * sigma_t)


def enob(snr_db):
    """ENOB = (SNR - 1.76)/6.02  [bits]."""
    return (snr_db - 1.76) / 6.02


def measure_snr_db(f_in_target, sigma_t, fs=FS, n=NFFT, n_avg=10, rng=RNG):
    """
    Sample a unit sine at jittered instants and measure SNR from the FFT.

    Coherent sampling: force the signal onto an exact odd bin m (odd m is
    coprime with the power-of-two record length, so every sample phase is
    distinct). Rectangular window; signal power = bin m, noise power = all
    remaining bins except DC. Returns (actual f_in, mean SNR in dB).
    """
    m = int(round(f_in_target * n / fs))
    if m % 2 == 0:
        m += 1                      # odd bin -> coherent & coprime with n
    f_in = m * fs / n
    t_ideal = np.arange(n) / fs
    ratios = []
    for _ in range(n_avg):
        dt = rng.standard_normal(n) * sigma_t
        x = np.sin(2 * np.pi * f_in * (t_ideal + dt))
        spec = np.fft.rfft(x) / n
        p = np.abs(spec) ** 2
        p_sig = p[m]
        p_noise = p[1:].sum() - p_sig   # exclude DC bin, keep everything else
        ratios.append(p_sig / p_noise)
    return f_in, 10.0 * np.log10(np.mean(ratios))


def main():
    print("[lab_30] ADC aperture jitter: Monte-Carlo sampling vs formula ...")
    print(f"    sigma_t = {SIGMA_T*1e15:.1f} fs (canonical example C), "
          f"fs = {FS/1e9:.1f} GS/s, NFFT = {NFFT}, unit sine, no quantizer")

    # ------------------------------------------------------------------
    # 1) design table: formula at f_in = 1 / 2.5 / 5 / 10 GHz
    # ------------------------------------------------------------------
    print("\n    design table (sigma_t = 447.9 fs):")
    print("      f_in [GHz]   2*pi*f_in*sigma_t [rad]   SNR [dB]   ENOB [bit]")
    for f_in in [1e9, 2.5e9, 5e9, 10e9]:
        s = snr_formula_db(f_in, SIGMA_T)
        print(f"      {f_in/1e9:8.1f}   {2*np.pi*f_in*SIGMA_T:.4e}"
              f"              {s:6.2f}     {enob(s):5.2f}")

    # ------------------------------------------------------------------
    # 2) inverse design: sigma_t for 10 ENOB at 5 GHz
    # ------------------------------------------------------------------
    snr_req = 6.02 * 10 + 1.76
    sigma_req = 10 ** (-snr_req / 20.0) / (2 * np.pi * 5e9)
    print(f"\n    inverse design @ f_in = 5 GHz, 10 ENOB:")
    print(f"      SNR required        = {snr_req:.2f} dB")
    print(f"      sigma_t required    = {sigma_req*1e15:.2f} fs "
          f"(x{SIGMA_T/sigma_req:.1f} cleaner than 447.9 fs, "
          f"= {20*np.log10(SIGMA_T/sigma_req):.1f} dB lower L(f) skirt)")

    # ------------------------------------------------------------------
    # 3) Monte-Carlo check at two spot frequencies (~1 GHz, ~5 GHz)
    # ------------------------------------------------------------------
    print("\n    Monte-Carlo vs formula (same actual coherent f_in):")
    for f_target in [1e9, 5e9]:
        f_act, snr_meas = measure_snr_db(f_target, SIGMA_T, n_avg=20)
        snr_theo = snr_formula_db(f_act, SIGMA_T)
        print(f"      f_in = {f_act/1e9:7.4f} GHz : measured {snr_meas:6.2f} dB,"
              f" formula {snr_theo:6.2f} dB, diff {snr_meas-snr_theo:+.2f} dB")

    # ------------------------------------------------------------------
    # 4) sweep f_in for the figure (two sigma_t values)
    # ------------------------------------------------------------------
    f_sweep = np.logspace(np.log10(0.5e9), np.log10(10e9), 10)
    meas = {}
    for st in [SIGMA_T, sigma_req]:
        pts = [measure_snr_db(f, st, n_avg=10) for f in f_sweep]
        meas[st] = (np.array([p[0] for p in pts]), np.array([p[1] for p in pts]))

    fig, axes = plt.subplots(1, 2, figsize=(13.0, 4.9))

    # (a) SNR vs f_in: formula lines + measured points
    ax = axes[0]
    f_line = np.logspace(np.log10(0.4e9), np.log10(12e9), 200)
    ax.semilogx(f_line / 1e9, snr_formula_db(f_line, SIGMA_T), color="tab:blue",
                label=r"$-20\log_{10}(2\pi f_{in}\sigma_t)$, $\sigma_t$=447.9 fs")
    ax.semilogx(f_line / 1e9, snr_formula_db(f_line, sigma_req), color="tab:green",
                ls="--", label=fr"$\sigma_t$={sigma_req*1e15:.1f} fs (10 ENOB @ 5 GHz)")
    fm, sm = meas[SIGMA_T]
    ax.plot(fm / 1e9, sm, "o", color="tab:blue", mfc="white", ms=6,
            label="模擬量測 (FFT), 447.9 fs")
    fm, sm = meas[sigma_req]
    ax.plot(fm / 1e9, sm, "s", color="tab:green", mfc="white", ms=6,
            label=fr"模擬量測 (FFT), {sigma_req*1e15:.1f} fs")
    ax.plot(5, snr_req, "*", color="tab:red", ms=15, zorder=5)
    ax.annotate("10 ENOB 目標\n(5 GHz, 61.96 dB)", xy=(5, snr_req),
                xytext=(1.4, 66), fontsize=9, color="tab:red",
                arrowprops=dict(arrowstyle="->", color="tab:red"))
    sec = ax.secondary_yaxis(
        "right", functions=(lambda s: (s - 1.76) / 6.02,
                            lambda e: 6.02 * e + 1.76))
    sec.set_ylabel("ENOB [bit]")
    ax.set_xlabel(r"輸入頻率 $f_{in}$ [GHz]")
    ax.set_ylabel("SNR [dB]")
    ax.set_title(r"(a) aperture-jitter SNR：$-6$ dB/octave（每倍頻掉 1 bit）")
    ax.legend(fontsize=8, loc="lower left")

    # (b) one spectrum: f_in ~ 5 GHz, sigma_t = 447.9 fs
    ax = axes[1]
    m = int(round(5e9 * NFFT / FS)) + 1   # odd coherent bin (3201)
    f_in = m * FS / NFFT
    dt = RNG.standard_normal(NFFT) * SIGMA_T
    x = np.sin(2 * np.pi * f_in * (np.arange(NFFT) / FS + dt))
    spec = np.abs(np.fft.rfft(x) / NFFT) ** 2
    dbc = 10 * np.log10(spec / spec[m] + 1e-30)
    freq = np.fft.rfftfreq(NFFT, 1 / FS)
    ax.plot(freq / 1e9, dbc, color="tab:blue", lw=0.7)
    snr_theo = snr_formula_db(f_in, SIGMA_T)
    floor_db = -(snr_theo + 10 * np.log10(NFFT / 2))
    ax.axhline(floor_db, color="tab:red", ls="--", lw=1.2,
               label=fr"理論 noise floor $\approx$ {floor_db:.0f} dBc/bin")
    ax.set_xlabel(r"頻率 [GHz]")
    ax.set_ylabel(r"相對載波功率 [dBc]")
    ax.set_title(fr"(b) FFT 頻譜：$f_{{in}}$={f_in/1e9:.2f} GHz, "
                 fr"$\sigma_t$=447.9 fs $\Rightarrow$ SNR={snr_theo:.1f} dB")
    ax.set_ylim(-120, 5)
    ax.legend(fontsize=9, loc="upper right")

    savefig(fig, "aperture_jitter_snr.png")


if __name__ == "__main__":
    main()
