"""
lab_19_allan.py

Goal
----
The time-domain companion of phase noise: the Allan deviation sigma_y(tau).
Oscillator/clock engineers quote sigma_y(tau) because plain variance of frequency
does not converge for flicker/random-walk noise. Each power-law noise type maps
to a characteristic sigma_y(tau) slope:

    white FM        S_y ~ f^0   ->  sigma_y ~ tau^{-1/2}
    flicker FM      S_y ~ f^-1  ->  sigma_y ~ tau^{0}   (flat floor)
    random-walk FM  S_y ~ f^-2  ->  sigma_y ~ tau^{+1/2}

We generate each fractional-frequency process, integrate to time error x(t), and
compute the OVERLAPPING Allan deviation, then check the slopes.

Extension (ABSOLUTE flicker-FM floor, not just the slope)
---------------------------------------------------------
For S_y(f) = h_{-1}/f the Allan variance is tau-independent with the exact
constant

    sigma_y^2 = 2 * ln(2) * h_{-1}          (flicker-FM floor)

because  2*int_0^inf (h_{-1}/f) sin^4(pi f tau)/(pi f tau)^2 df
       = 2*h_{-1} * int_0^inf sin^4(u)/u^3 du  =  2*h_{-1}*ln 2.

We (1) verify int_0^inf sin^4 u/u^k du numerically for k=2,3,4
(pi/4, ln 2, pi/3 -- the white-FM, flicker-FM, RW-FM prefactors), and
(2) synthesize flicker FM with an EXACTLY known h_{-1} (canonical value from
the worked example: Gamma_rms=0.5, S_i=1e-24 A^2/Hz, q_max=1 pC, f0=5 GHz,
1/f^3 corner f_c=3.2 kHz  =>  h_{-1}=8.11e-19), measure the ADEV floor and
compare with sqrt(2*ln2*h_{-1}) = 1.06e-9. A combined white+flicker FM run
reproduces the knee at tau_knee = 1/(4*ln2*f_c) = 113 us.

Figures
-------
  static/figures/allan_deviation.png       (original slope figure, unchanged)
  static/figures/allan_flicker_floor.png   (absolute floor verification)
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt
from plot_utils import savefig

RNG = np.random.default_rng(19)

LN2 = float(np.log(2.0))


def power_law_y(n, fs, alpha, rng):
    """Fractional-frequency y(t) with one-sided PSD S_y(f) ~ f^alpha."""
    w = rng.standard_normal(n)
    F = np.fft.rfft(w)
    f = np.fft.rfftfreq(n, d=1.0 / fs)
    shape = np.ones_like(f)
    nz = f > 0
    shape[nz] = f[nz] ** (alpha / 2.0)
    shape[0] = shape[nz][0] if np.any(nz) else 1.0
    y = np.fft.irfft(F * shape, n=n)
    return y / np.std(y)


def overlapping_adev(x, tau0, ms):
    """Overlapping Allan deviation from time-error samples x at spacing tau0."""
    x = np.asarray(x)
    N = len(x)
    out = []
    for m in ms:
        if N - 2 * m < 1:
            out.append(np.nan); continue
        d = x[2 * m:] - 2 * x[m:-m] + x[:-2 * m]
        avar = np.sum(d ** 2) / (2 * (N - 2 * m) * (m * tau0) ** 2)
        out.append(np.sqrt(avar))
    return np.array(out)


def synth_y_from_psd(n, fs, s_y_one_sided, rng):
    """
    Synthesize fractional-frequency samples y(t) whose ONE-SIDED PSD equals
    s_y_one_sided(f) EXACTLY (not just in slope).

    Method: unit-variance white noise has one-sided PSD 2/fs, so shape its
    rFFT by |H(f)|^2 = S_target(f) / (2/fs). The DC bin is zeroed.
    """
    w = rng.standard_normal(n)
    W = np.fft.rfft(w)
    f = np.fft.rfftfreq(n, d=1.0 / fs)
    H = np.zeros_like(f)
    nz = f > 0
    H[nz] = np.sqrt(s_y_one_sided(f[nz]) * fs / 2.0)
    return np.fft.irfft(W * H, n=n)


def verify_sin4_integrals():
    """
    Numerically verify the sin^4 integral family behind the ADEV prefactor
    table (quad on [0, 200*pi] + analytic <sin^4>=3/8 tail estimate):

        I_2 = int_0^inf sin^4 u / u^2 du = pi/4   -> white FM   h0/(2 tau)
        I_3 = int_0^inf sin^4 u / u^3 du = ln 2   -> flicker FM 2 ln2 h_{-1}
        I_4 = int_0^inf sin^4 u / u^4 du = pi/3   -> RW FM (2 pi^2/3) h_{-2} tau
    """
    from scipy.integrate import quad

    U = 200 * np.pi
    exact = {2: np.pi / 4, 3: LN2, 4: np.pi / 3}
    tail = {2: (3 / 8) / U, 3: (3 / 8) / (2 * U ** 2), 4: (3 / 8) / (3 * U ** 3)}
    print("[lab_19] sin^4 integral family (scipy.integrate.quad):")
    for k in (2, 3, 4):
        v, _ = quad(lambda u: np.sin(u) ** 4 / u ** k, 0, U, limit=4000)
        v += tail[k]
        print(f"  I_{k} = int sin^4(u)/u^{k} du = {v:.4f}   (exact {exact[k]:.4f})")


def verify_flicker_floor():
    """
    Verify the ABSOLUTE flicker-FM ADEV floor sigma_y = sqrt(2*ln2*h_{-1}).

    Canonical numbers (site worked example): the white-FM segment of the
    canonical 5 GHz oscillator has (time-domain-clean, single-sided)
        S_phi(f) = Gamma_rms^2 * S_i / (q_max^2 * (2 pi f)^2),
    i.e. S_phi = h_phi_m2 / f^2 with h_phi_m2 = Gamma_rms^2*S_i/(4 pi^2 q_max^2).
    Below the 1/f^3 corner f_c the phase PSD steepens to h_phi_m2*f_c/f^3
    (continuity at f_c), so S_y = (f^2/f0^2) S_phi = h_m1/f with
        h_m1 = h_phi_m2 * f_c / f0^2.
    """
    gamma_rms, s_i, qmax, f0 = 0.5, 1e-24, 1e-12, 5e9   # -, A^2/Hz, C, Hz
    f_c = 3.2e3                                          # Hz (symmetric c0=0.04)
    h_phi_m2 = gamma_rms ** 2 * s_i / (qmax ** 2 * 4 * np.pi ** 2)  # rad^2*Hz
    h_m1 = h_phi_m2 * f_c / f0 ** 2                      # dimensionless
    h0 = h_phi_m2 / f0 ** 2                              # 1/Hz (white FM level)
    floor_theory = np.sqrt(2 * LN2 * h_m1)               # dimensionless
    tau_knee = 1 / (4 * LN2 * f_c)                       # s
    print("[lab_19] canonical flicker-FM floor numbers:")
    print(f"  h_phi_m2 = {h_phi_m2:.2e} rad^2*Hz   h_m1 = {h_m1:.2e}   "
          f"h0 = {h0:.2e} /Hz")
    print(f"  theory floor sigma_y = sqrt(2*ln2*h_m1) = {floor_theory:.2e}")
    print(f"  tau_knee = 1/(4*ln2*f_c) = {tau_knee*1e6:.0f} us")

    # --- (a) pure flicker FM at exactly known h_m1: measured floor / theory ---
    fs, n = 1.0, 2 ** 20
    tau0 = 1.0 / fs
    ms = np.unique(np.round(np.logspace(1, 3.3, 12)).astype(int))
    ratios = []
    for seed in range(8):
        rng = np.random.default_rng(190 + seed)
        y = synth_y_from_psd(n, fs, lambda f: h_m1 / f, rng)
        x = np.cumsum(y) * tau0
        ratios.append(overlapping_adev(x, tau0, ms) / floor_theory)
    ratio_mean = float(np.mean(ratios))
    print(f"  pure flicker FM: measured floor / theory = {ratio_mean:.3f} "
          f"(8 seeds, tau = {ms[0]}..{ms[-1]} s)")

    # --- (b) white FM + flicker FM: absolute curve incl. the knee ---
    fs2, n2 = 1e6, 2 ** 22
    tau0_2 = 1.0 / fs2
    ms2 = np.unique(np.round(np.logspace(0, np.log10(n2 / 256), 20)).astype(int))
    taus2 = ms2 * tau0_2
    theory2 = np.sqrt(h0 / (2 * taus2) + 2 * LN2 * h_m1)
    adevs = []
    for seed in range(6):
        rng = np.random.default_rng(1900 + seed)
        y = synth_y_from_psd(n2, fs2, lambda f: h0 + h_m1 / f, rng)
        x = np.cumsum(y) * tau0_2
        adevs.append(overlapping_adev(x, tau0_2, ms2))
    adev2 = np.mean(adevs, axis=0)
    dev_max = float(np.max(np.abs(adev2 / theory2 - 1)))
    print(f"  white+flicker FM: max |measured/theory - 1| = {dev_max*100:.1f}% "
          f"over tau = 1 us .. {taus2[-1]*1e3:.1f} ms")

    fig, ax = plt.subplots(figsize=(8.4, 5.4))
    ax.loglog(taus2, adev2, "o", ms=4, color="tab:blue",
              label="模擬（white FM + flicker FM，6 seeds 平均）")
    ax.loglog(taus2, theory2, "-", color="black", lw=1.4,
              label=r"理論 $\sqrt{h_0/2\tau+2\ln 2\,h_{-1}}$")
    ax.loglog(taus2, np.sqrt(h0 / (2 * taus2)), "--", color="tab:gray", lw=1.0,
              label=r"white FM 漸近 $\sqrt{h_0/2\tau}$")
    ax.axhline(floor_theory, ls="--", color="tab:green", lw=1.2,
               label=r"flicker floor $\sqrt{2\ln 2\,h_{-1}}=1.06\times10^{-9}$")
    ax.axvline(tau_knee, ls=":", color="tab:red", lw=1.2)
    ax.annotate(r"$\tau_{knee}=\frac{1}{4\ln 2\,f_c}=113\,\mu$s",
                xy=(tau_knee, floor_theory), xytext=(tau_knee * 2.2, floor_theory * 2.4),
                fontsize=9, color="tab:red",
                arrowprops=dict(arrowstyle="->", color="tab:red", lw=0.9))
    ax.set_xlabel(r"averaging time $\tau$ (s)")
    ax.set_ylabel(r"$\sigma_y(\tau)$（分數頻率，無因次）")
    ax.set_title("flicker-FM floor 絕對高度驗證（canonical 5 GHz、$f_c$=3.2 kHz）")
    ax.legend(fontsize=8.5, loc="upper right")
    ax.grid(True, which="both", alpha=0.3)
    savefig(fig, "allan_flicker_floor.png")


def main():
    print("[lab_19] Allan deviation vs noise type ...")
    fs = 1.0
    n = 2 ** 18
    tau0 = 1.0 / fs
    ms = np.unique(np.round(np.logspace(0, np.log10(n // 8), 30)).astype(int))
    taus = ms * tau0

    cases = [
        (0.0, "white FM ($S_y\\sim f^0$)", "tab:blue", -0.5),
        (-1.0, "flicker FM ($S_y\\sim f^{-1}$)", "tab:green", 0.0),
        (-2.0, "random-walk FM ($S_y\\sim f^{-2}$)", "tab:red", 0.5),
    ]

    fig, ax = plt.subplots(figsize=(8.4, 5.4))
    for alpha, label, c, slope in cases:
        y = power_law_y(n, fs, alpha, RNG)
        x = np.cumsum(y) * tau0           # time error = integral of fractional freq
        adev = overlapping_adev(x, tau0, ms)
        ax.loglog(taus, adev / adev[0], "o-", ms=3, color=c, label=label)
        # reference slope line through first point
        ref = (adev[0] / adev[0]) * (taus / taus[0]) ** slope
        ax.loglog(taus, ref, color=c, ls="--", lw=0.9, alpha=0.7)

    ax.set_xlabel(r"averaging time $\tau$ (s)")
    ax.set_ylabel(r"$\sigma_y(\tau)$ (normalized)")
    ax.set_title("Allan deviation：每種 FM 雜訊有特徵斜率（虛線 = 理論斜率）")
    ax.legend(fontsize=9)
    ax.grid(True, which="both", alpha=0.3)
    ax.text(0.02, 0.04,
            "slopes: white FM $-1/2$, flicker FM $0$, random-walk FM $+1/2$",
            transform=ax.transAxes, fontsize=8)
    savefig(fig, "allan_deviation.png")

    # --- extension: absolute flicker-FM floor (constant, not just slope) ---
    verify_sin4_integrals()
    verify_flicker_floor()


if __name__ == "__main__":
    main()
