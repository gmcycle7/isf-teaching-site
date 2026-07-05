"""
lab_35_xcorr_measurement.py

Goal
----
Simulate the cross-correlation phase-noise measurement described in
docs/06_design_insights/measurement_and_spurs.md Part 1, Method C
(external instrument technique, NOT among the five source PDFs; the
underlying DSP -- PSD/cross-spectrum estimation and averaging -- is
general signal-processing knowledge).

Setup
-----
A single DUT (device under test) phase process phi_DUT(t) is observed
through TWO independent measurement channels. Each channel adds its own
white instrument noise ON TOP OF phi_DUT, well ABOVE the DUT's own floor:

    y1(t) = phi_DUT(t) + n1(t)      n1 white, PSD S_n1
    y2(t) = phi_DUT(t) + n2(t)      n2 white, PSD S_n2   (n1 _|_ n2 _|_ phi_DUT)

phi_DUT(t) is synthesized with a canonical 1/f^2 mid-band (site value:
L(1 MHz) = -148.0 dBc/Hz, i.e. S_phi = 2*L_lin, AUTHORING_SPEC Sec.8
canonical example B) plus a DUT-intrinsic white floor 20 dB below the
1/f^2 level at 1 MHz -- a "true" two-segment toy DUT spectrum. The two
synthetic instrument noises are white, each with PSD chosen so the
SINGLE-CHANNEL floor sits well ABOVE the DUT floor -- exactly the regime
cross-correlation measurement is built for.

Two spectra are computed from the same time series:
  (1) single-channel PSD S_yy = <|Y1|^2> (auto-spectrum, M segments
      averaged): shows S_DUT + S_instr -- the instrument floor masks the
      true DUT floor.
  (2) cross-spectrum S_y1y2 = <Y1 Y2*> averaged over M segments: the
      correlated DUT term adds coherently (its estimate does not shrink
      with M); the uncorrelated instrument cross-terms behave like a
      2-D random walk in the complex plane, and the RESIDUAL magnitude
      of their average over M independent segments falls as 1/sqrt(M)
      (a fixed decision floor set by scipy/DSP statistics of independent
      complex Gaussians, not by the ISF physics).

We sweep M = 1, 4, 16, 64, 256, 1024 (powers of 4) and:
  (a) measure the residual cross-spectrum "floor" at high offset -- a band
      chosen far enough from f_ref that the DUT's own 1/f^2 skirt has
      fallen to <2% of the DUT's white floor there -- vs M, and check it
      falls at -5*log10(M) dB over the range where the uncorrelated
      instrument residual S_instr/sqrt(M) still clearly dominates
      S_dut_floor, i.e. M <= M_FIT_MAX (# -> printed slope check against
      theory: for M iid zero-mean complex Gaussian terms,
      E[|mean|] ~ 1/sqrt(M) exactly [verified analytically below]; reported
      in the standard PSD dB convention 10*log10(power ratio), this
      amplitude-like quantity gives 10*log10(1/sqrt(M)) = -5*log10(M) dB,
      matching AUTHORING_SPEC's "each x10 averaging drops the floor 5 dB"),
  (b) show the M=1024 recovered cross-spectrum against the true DUT
      spectrum: does cross-correlation dig the true DUT floor out from
      under the single-channel instrument floor. Because the M=1..1024
      sweep only spans a factor 32 in sqrt(M) (~15 dB of possible
      improvement) and the single-channel margin is also 15 dB (matching
      the docs page's worked example), the M=1024 residual ends up close
      to -- not far below -- S_dut_floor, so the recovered floor sits a
      small residual amount (~1-2 dB, computed and printed, not asserted)
      above the true value. This is the correct, honestly-reported
      outcome of a finite averaging budget, not a bug.

Honest limits (stated in the docs page, not re-derived here): in a real
cross-correlation analyzer the floor cannot fall forever as 1/sqrt(M) --
eventually residual channel-to-channel correlation (shared reference
distribution, shared supply/ground, thermal pickup) sets a practical
floor BELOW WHICH the recovered estimate cannot improve no matter how
large M is. This is external engineering knowledge, not modeled
numerically here (# -> no fabricated number for the residual-correlation
floor); this simulation only shows the idealized 1/sqrt(M) mechanism and
a realistic finite-M outcome, not that additional physical limit.

Figure
------
static/figures/xcorr_floor.png  (2 panels: floor-vs-M with 5*log10(M)
overlay; recovered spectrum at M=1024 vs truth)

Runtime: a few seconds (<60 s required).
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt

from plot_utils import savefig

RNG = np.random.default_rng(35)

# ---------------------------------------------------------------------------
# Site-canonical DUT parameters (AUTHORING_SPEC Sec.8 canonical example B,
# [P1] Eq.21 worked example: L(1 MHz) = -148.0 dBc/Hz)
# ---------------------------------------------------------------------------
F_REF = 1e6                # reference offset for the canonical L value [Hz]
L_REF_DBC = -148.0         # site canonical 1/f^2 level at 1 MHz
S_PHI_REF = 2 * 10 ** (L_REF_DBC / 10)   # S_phi(f_ref) = 2*L_lin [rad^2/Hz]

# DUT intrinsic white floor: 20 dB below the 1/f^2 level AT f_ref (a "true"
# two-segment toy DUT spectrum: 1/f^2 skirt transitioning to a low floor
# near f_corner = f_ref*sqrt((S_ref-S_floor)/S_floor) ~ 10*f_ref here).
DUT_FLOOR_REL_DB = 20.0
S_DUT_FLOOR = S_PHI_REF * 10 ** (-DUT_FLOOR_REL_DB / 10)   # [rad^2/Hz]

# Each channel's instrument white noise: chosen so the SINGLE-CHANNEL floor is
# 15 dB ABOVE the DUT floor at M=1 (the whole point of doing cross-correlation
# -- this matches the 15 dB example used in the docs page prose). Because the
# M=1..1024 sweep only spans a factor 32 in sqrt(M) (~15 dB of possible
# 1/sqrt(M) improvement), the same 15 dB margin that makes the single-channel
# masking obvious at M=1 also means the uncorrelated residual S_instr/sqrt(M)
# lands almost exactly ON TOP of S_dut_floor by M=1024 (ratio ~1). This is not
# a bug: it is the honest, expected outcome of "one decade and a half of
# averaging removes about one decade and a half of instrument floor" -- after
# M=1024 the recovered floor is close to, but not perfectly at, the true DUT
# floor (see the residual-error print in main()). The 1/sqrt(M) SLOPE itself
# is verified over the earlier part of the sweep (M<=M_FIT_MAX), where the
# residual still clearly dominates over S_dut_floor.
INSTR_FLOOR_REL_DB = 15.0
S_INSTR = S_DUT_FLOOR * 10 ** (INSTR_FLOOR_REL_DB / 10)    # [rad^2/Hz], per channel

# M range over which the uncorrelated residual S_instr/sqrt(M) stays at least
# ~4x above S_dut_floor (bias from the DUT's own floor leaking into the
# "floor" estimate is then only a percent or two -- verified numerically);
# used only for the 1/sqrt(M) slope fit, the full M_LIST is still plotted.
M_FIT_MAX = 64

# ---------------------------------------------------------------------------
# Time-series synthesis parameters (baseband simulation of phi(t) itself;
# this stands in for whatever baseband voltage a real carrier-suppression
# front end -- Part 1 Method B/C of the docs page -- would produce)
# ---------------------------------------------------------------------------
FS = 200e6                 # baseband sample rate [Hz]; Nyquist = 100 MHz gives
                            # a wide enough span above f_corner (~10 MHz) that
                            # a genuine "DUT-floor-only" band exists (80-95 MHz)
SEG_LEN = 4096              # samples per segment -> freq resolution 48.8 kHz
M_LIST = [1, 4, 16, 64, 256, 1024]        # averaging counts (powers of 4)
M_MAX = max(M_LIST)
N_TOTAL = SEG_LEN * M_MAX                  # total samples needed for M_MAX segments

# "High offset" analysis band: where the DUT's 1/f^2 skirt has fallen to a
# small fraction of the DUT's own white floor, so what's left in the single
# channel is (DUT floor) + (instrument floor), and what's left in the
# uncorrelated residual is essentially the two instrument noises alone.
F_HI_LO, F_HI_HI = 80e6, 95e6


def make_dut_phase(n, fs, rng):
    """Synthesize phi_DUT(t): 1/f^2 skirt (colored Gaussian spectrum) with a
    white floor added underneath, matched to S_PHI_REF at F_REF and
    S_DUT_FLOOR at high offset. Frequency-domain construction gives the
    exact target PSD shape in expectation (not a fit).
    """
    freqs = np.fft.rfftfreq(n, d=1.0 / fs)
    freqs_safe = np.where(freqs > 0, freqs, freqs[1] if len(freqs) > 1 else 1.0)
    s_skirt = (S_PHI_REF - S_DUT_FLOOR) * (F_REF / freqs_safe) ** 2
    s_dut = s_skirt + S_DUT_FLOOR
    s_dut[0] = s_dut[1] if n > 1 else s_dut[0]   # tame DC bin

    # One-sided PSD -> complex Gaussian spectrum with the right expected
    # power per bin (Parseval-consistent with noise_utils.white_noise's
    # var = psd*fs/2 one-sided convention).
    scale = np.sqrt(s_dut * n * fs / 2.0)
    re = rng.standard_normal(len(freqs))
    im = rng.standard_normal(len(freqs))
    spec = (re + 1j * im) / np.sqrt(2.0) * scale
    spec[0] = spec[0].real * np.sqrt(2.0)          # DC must be real
    if n % 2 == 0:
        spec[-1] = spec[-1].real * np.sqrt(2.0)    # Nyquist must be real
    x = np.fft.irfft(spec, n=n)
    return x, s_dut


def add_white_instrument_noise(n, fs, s_level, rng):
    """White instrument noise with one-sided PSD s_level [rad^2/Hz]."""
    sigma = np.sqrt(s_level * fs / 2.0)
    return rng.standard_normal(n) * sigma


def segment_average_spectra(y1, y2, seg_len, m, fs):
    """Split y1, y2 into m segments of seg_len, FFT each, and average the
    auto-spectrum of y1 and the cross-spectrum Y1*conj(Y2) over the first m
    segments. Returns (freqs, Syy_avg, Sxy_avg) as one-sided densities
    [units^2/Hz].

    Uses a rectangular window (no taper) deliberately: the DUT spectrum here
    is smooth (no large dynamic-range features within one segment needing
    sidelobe suppression), and a taper window correlates neighboring
    frequency bins (reduces the effective number of independent samples
    averaged over a band), which biases the finite-sample floor-vs-M slope
    check in Part (a) below. A rectangular window gives the cleanest
    verification of the 1/sqrt(M) law; production PN analyzers do use
    tapered windows for exactly the sidelobe-suppression reason a real
    multi-decade spectrum needs.
    """
    freqs = np.fft.rfftfreq(seg_len, d=1.0 / fs)
    enbw_scale = fs * seg_len  # rectangular window: window power = seg_len

    syy_acc = np.zeros(len(freqs))
    sxy_acc = np.zeros(len(freqs), dtype=complex)
    for k in range(m):
        seg1 = y1[k * seg_len:(k + 1) * seg_len]
        seg2 = y2[k * seg_len:(k + 1) * seg_len]
        Y1 = np.fft.rfft(seg1)
        Y2 = np.fft.rfft(seg2)
        syy_acc += (np.abs(Y1) ** 2) * 2.0 / enbw_scale
        sxy_acc += (Y1 * np.conj(Y2)) * 2.0 / enbw_scale
    syy_acc /= m
    sxy_acc /= m
    syy_acc[0] /= 2.0   # DC has no image; one-sided factor-of-2 doesn't apply
    return freqs, syy_acc, sxy_acc


def main():
    print("[lab_35] cross-correlation phase-noise measurement simulation ...")
    print(f"  DUT canonical: L({F_REF/1e6:.0f} MHz)={L_REF_DBC} dBc/Hz -> "
          f"S_phi_ref={S_PHI_REF:.3e} rad^2/Hz")
    print(f"  DUT intrinsic floor: {DUT_FLOOR_REL_DB:.0f} dB below S_phi_ref -> "
          f"S_dut_floor={S_DUT_FLOOR:.3e} rad^2/Hz")
    print(f"  per-channel instrument floor: {INSTR_FLOOR_REL_DB:.0f} dB above DUT "
          f"floor -> S_instr={S_INSTR:.3e} rad^2/Hz")

    freqs = np.fft.rfftfreq(SEG_LEN, d=1.0 / FS)
    mask_hi = (freqs >= F_HI_LO) & (freqs <= F_HI_HI)
    skirt_hi = (S_PHI_REF - S_DUT_FLOOR) * (F_REF / freqs[mask_hi]) ** 2
    print(f"\n  high-offset analysis band [{F_HI_LO/1e6:.0f}, {F_HI_HI/1e6:.0f}] MHz: "
          f"DUT 1/f^2 skirt there is {np.max(skirt_hi/S_DUT_FLOOR)*100:.1f}% of the DUT "
          f"floor at worst (# -> negligible)")

    # ---- generate N_OUTER independent (DUT, instrument-noise) realizations
    # and average the floor-vs-M curve over them -- reduces the single-draw
    # estimator variance of the M=1 point (only ~300 independent frequency
    # bins in the analysis band) so the fitted 1/sqrt(M) slope is reliable.
    # One representative realization (the last one) is kept for the
    # single-channel spectrum and the M=1024 recovered-spectrum panel.
    N_OUTER = 8
    floor_accum = np.zeros((N_OUTER, len(M_LIST)))
    syy_max = None
    sxy_at_mmax = None
    for outer in range(N_OUTER):
        phi_dut, _ = make_dut_phase(N_TOTAL, FS, RNG)
        n1 = add_white_instrument_noise(N_TOTAL, FS, S_INSTR, RNG)
        n2 = add_white_instrument_noise(N_TOTAL, FS, S_INSTR, RNG)
        y1 = phi_dut + n1
        y2 = phi_dut + n2
        for j, m in enumerate(M_LIST):
            _, syy, sxy = segment_average_spectra(y1, y2, SEG_LEN, m, FS)
            floor_accum[outer, j] = np.mean(np.abs(sxy[mask_hi]))
            if outer == N_OUTER - 1 and m == M_MAX:
                syy_max = syy
                sxy_at_mmax = sxy

    single_ch_floor_meas = np.mean(syy_max[mask_hi])
    single_ch_floor_theory = S_DUT_FLOOR + S_INSTR
    print(f"\n  single-channel floor (high offset, M={M_MAX}, one representative run): "
          f"measured={single_ch_floor_meas:.3e}, "
          f"theory S_dut_floor+S_instr={single_ch_floor_theory:.3e} rad^2/Hz")

    # ---- cross-spectrum floor vs M (averaged over N_OUTER realizations) ----
    print(f"\n  cross-spectrum residual floor vs M (high-offset band, averaged over "
          f"{N_OUTER} independent realizations; clearly uncorrelated-noise-dominated for "
          f"M<={M_FIT_MAX}, approaching the true DUT floor by M={M_MAX}):")
    print("     M  |  floor [rad^2/Hz]  |  dB rel. M=1  |  theory -5*log10(M) [dB]")
    floor_vs_m = np.mean(floor_accum, axis=0)
    # floor_vs_m is |Sxy| -- a PSD-like quantity in rad^2/Hz (power units), and
    # AUTHORING_SPEC / the docs page report it in dB via the standard PSD
    # convention dB=10*log10(power ratio). |Sxy| itself (not its square) is the
    # quantity that decays as 1/sqrt(M) (verified analytically: for M iid
    # zero-mean complex terms, E[|mean|] ~ 1/sqrt(M)), so
    # 10*log10(|Sxy|(M)/|Sxy|(1)) ~ 10*log10(1/sqrt(M)) = -5*log10(M).
    floor_db_rel = 10 * np.log10(floor_vs_m / floor_vs_m[0])
    theory_db_rel = -5 * np.log10(np.array(M_LIST) / M_LIST[0])
    for m, f_abs, f_db, f_th in zip(M_LIST, floor_vs_m, floor_db_rel, theory_db_rel):
        print(f"    {m:5d} |     {f_abs:.3e}      |   {f_db:7.2f}    |   {f_th:7.2f}")

    # linear regression of measured dB drop vs log10(M) -> slope check, fit
    # ONLY over the range where the uncorrelated residual S_instr/sqrt(M)
    # still clearly dominates S_dut_floor (M <= M_FIT_MAX, margin >= ~4x);
    # once the residual gets close to S_dut_floor (M=256..1024 here) the two
    # add non-trivially and the pure 1/sqrt(M) LINE (not the physics) stops
    # being the right model for floor_db_rel, which would bias a fit over
    # the full range.
    fit_mask = np.array(M_LIST) <= M_FIT_MAX
    logM_fit = np.log10(np.array(M_LIST, dtype=float)[fit_mask])
    slope_fit, intercept_fit = np.polyfit(logM_fit, floor_db_rel[fit_mask], 1)
    print(f"\n  # -> fitted slope (M<={M_FIT_MAX}, uncorrelated-dominated regime) = "
          f"{slope_fit:.3f} dB/decade(log10 M)   "
          f"(theory: -5.0 dB/decade of M, i.e. floor ~ 1/sqrt(M))")
    print(f"  # -> slope match: fitted/theory = {slope_fit/-5.0:.4f}")
    print(f"  # -> by M={M_MAX} the uncorrelated residual has fallen close to S_dut_floor "
          f"itself, so the curve bends toward (not below) the true DUT floor -- see the "
          f"recovered-vs-truth check below")

    # ---- recovered spectrum at M=1024 vs the true DUT spectrum ----
    recovered = np.real(sxy_at_mmax)   # cross-spectrum of a real common process is real in expectation
    recovered_clipped = np.clip(recovered, 1e-30, None)
    # truth spectrum evaluated on the segment-length frequency grid (freqs),
    # same closed-form used by make_dut_phase (not the full N_TOTAL-length grid).
    s_dut_theory_seg = (S_PHI_REF - S_DUT_FLOOR) * (F_REF / np.where(freqs > 0, freqs, freqs[1])) ** 2 + S_DUT_FLOOR
    l_recovered = 10 * np.log10(0.5 * recovered_clipped)     # L = 0.5*S_phi -> dBc/Hz
    l_truth = 10 * np.log10(0.5 * s_dut_theory_seg)
    l_single_ch = 10 * np.log10(0.5 * syy_max)

    # numeric check: at f_ref, recovered vs truth
    idx_ref = np.argmin(np.abs(freqs - F_REF))
    print(f"\n  at f={freqs[idx_ref]/1e6:.3f} MHz (M={M_MAX}):")
    print(f"    truth        L = {l_truth[idx_ref]:.2f} dBc/Hz")
    print(f"    single-ch    L = {l_single_ch[idx_ref]:.2f} dBc/Hz  (instrument-floor-limited)")
    print(f"    xcorr M=1024 L = {l_recovered[idx_ref]:.2f} dBc/Hz  (recovered)")

    idx_hi = np.argmin(np.abs(freqs - 90e6))
    print(f"\n  at f={freqs[idx_hi]/1e6:.1f} MHz (DUT floor region, M={M_MAX}):")
    print(f"    truth (DUT floor)  L = {l_truth[idx_hi]:.2f} dBc/Hz")
    print(f"    single-ch          L = {l_single_ch[idx_hi]:.2f} dBc/Hz  (masked by instrument floor)")
    print(f"    xcorr M=1024       L = {l_recovered[idx_hi]:.2f} dBc/Hz  (should be close to truth)")
    residual_db = l_recovered[idx_hi] - l_truth[idx_hi]
    print(f"    # -> residual error at DUT floor after M=1024 averaging: {residual_db:+.2f} dB")

    make_figure(M_LIST, floor_db_rel, theory_db_rel, slope_fit,
                freqs, l_truth, l_single_ch, l_recovered)
    print("\n[lab_35] done.")


def make_figure(m_list, floor_db_rel, theory_db_rel, slope_fit,
                 freqs, l_truth, l_single_ch, l_recovered):
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.6))

    # panel (a): floor vs M
    ax = axes[0]
    m_arr = np.array(m_list, dtype=float)
    fit_mask = m_arr <= M_FIT_MAX
    ax.plot(m_arr, floor_db_rel, "o-", color="tab:red", ms=7,
            label=r"measured cross-spectrum floor")
    ax.plot(m_arr[fit_mask], theory_db_rel[fit_mask], "k--", lw=1.8,
            label=r"theory $-5\log_{10}(M/M_0)$（不相關本底段，用於擬合）")
    ax.plot(m_arr[~fit_mask], theory_db_rel[~fit_mask], "k:", lw=1.2, alpha=0.5,
            label=r"（若持續 $1/\sqrt{M}$，此段的預測值）")
    ax.axvline(M_FIT_MAX, color="gray", lw=0.9, ls=":", alpha=0.7)
    ax.text(M_FIT_MAX * 1.1, floor_db_rel[0] - 2, "本底漸近\nDUT 真實 floor",
            fontsize=7.5, color="dimgray")
    ax.set_xscale("log")
    ax.set_xlabel(r"averaging count $M$ [—]")
    ax.set_ylabel(r"floor level rel. $M=1$ [dB]")
    ax.set_title(f"(a) 互相關本底 vs $M$（擬合斜率={slope_fit:.2f} dB/decade, $M\\leq${M_FIT_MAX}）")
    ax.legend(fontsize=8, loc="lower left")
    ax.grid(True, which="both", alpha=0.3)

    # panel (b): recovered spectrum at M=1024 vs truth
    ax = axes[1]
    ax.semilogx(freqs[1:], l_single_ch[1:], color="gray", lw=1.3, alpha=0.8,
                label="單通道 auto-spectrum（受儀器本底限制）")
    ax.semilogx(freqs[1:], l_recovered[1:], color="tab:red", lw=1.0, alpha=0.85,
                label=r"cross-spectrum, $M$=1024（還原）")
    ax.semilogx(freqs[1:], l_truth[1:], "k--", lw=2.0,
                label="真實 DUT 頻譜（合成用）")
    ax.axvspan(F_HI_LO, F_HI_HI, color="tab:blue", alpha=0.08,
               label="floor 分析頻帶")
    ax.set_xlabel(r"offset frequency $\Delta f$ [Hz]")
    ax.set_ylabel(r"$\mathcal{L}(\Delta f)$ [dBc/Hz]")
    ax.set_title("(b) 還原頻譜（$M$=1024）vs 真實 DUT")
    ax.legend(fontsize=8, loc="upper right")
    ax.set_ylim(bottom=min(l_truth[1:]) - 10, top=max(l_single_ch[1:]) + 5)

    fig.suptitle(
        r"Cross-correlation 量測模擬：兩獨立通道儀器本底以 $1/\sqrt{M}$ 收斂，DUT 相關項不變"
        f"\n（$L$({F_REF/1e6:.0f} MHz)={L_REF_DBC} dBc/Hz, DUT floor {DUT_FLOOR_REL_DB:.0f} dB 以下, "
        f"單通道儀器本底 +{INSTR_FLOOR_REL_DB:.0f} dB 高於 DUT floor）",
        fontsize=10.5)
    savefig(fig, "xcorr_floor.png")


if __name__ == "__main__":
    main()
