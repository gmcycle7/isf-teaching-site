"""
lab_23_diffusion_dictionary.py

Goal
----
The "diffusion-constant dictionary": show that FIVE quantities quoted by five
different communities are ONE number wearing five sets of clothes:

  (1) kappa      : ring-jitter phase constant, sigma_dphi = kappa*sqrt(dt)
                   ([P2] Eq.(8)/(10)/(11)/(12); kappa in rad/sqrt(s))
  (2) D          : phase-diffusion constant of the Wiener phase
                   (convention A "rate":   Var[dphi] =  D|t|,  D = kappa^2;
                    convention B "Demir":  Var[dphi] = 2D|t|,  D = kappa^2/2)
  (3) FWHM       : Lorentzian 3-dB linewidth, df_3dB = kappa^2/(2*pi) Hz
                   (= D_B/pi = D_A/(2*pi); convention-independent physics)
  (4) S_phi 1/f^2: one-sided S_phi(f) = 2*kappa^2/(2*pi*f)^2  [rad^2/Hz]
                   -> L(/2 clean) = kappa^2/dw^2 ; [P1] Eq.(21) (/4 SSB) halves it
  (5) ADEV       : white-FM Allan deviation sigma_y(tau) = kappa/(2*pi*f0*sqrt(tau))

The master number is the PHASE-VARIANCE GROWTH RATE

    kappa^2 = d Var[dphi]/dt = Gamma_rms^2 * S_i / (2*qmax^2)   [rad^2/s]

([P2] Eq.(11), p.793, one-sided S_i). Canonical: Gamma_rms=0.5, qmax=1 pC,
S_i=1e-24 A^2/Hz  ->  kappa^2 = 0.125 rad^2/s (the site's canonical "D").

The simulation builds ONE ISF-weighted white-noise phase (the [P1] Eq.(11)
integral, exactly like lab_06 but run long enough to resolve the Lorentzian)
and extracts kappa^2 four independent ways:
  (a) phase-variance slope  (also falsifies "Var = 2*0.125*t")
  (b) Lorentzian FWHM of the synthesized carrier (fit 1/S vs offset^2)
  (c) overlapping ADEV (estimator replicated from lab_19_allan.py)
  (d) S_phi(f)*(2*pi*f)^2/2 plateau

The oscillation frequency in the sim is a normalized f0=16 Hz (the linewidth
does NOT depend on f0; only ADEV does, and its f0-scaling is checked in-sim,
then mapped analytically to the canonical 5 GHz).

Figure
------
  static/figures/diffusion_dictionary.png
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch
from plot_utils import savefig
from noise_utils import white_noise

RNG = np.random.default_rng(23)

# ----------------------------------------------------------------------------
# canonical physical constants (identical to example B of the authoring spec)
# ----------------------------------------------------------------------------
GAMMA_RMS = 0.5          # representative ISF rms                     [-]
QMAX = 1e-12             # max charge swing                           [C]
SI = 1e-24               # one-sided current-noise PSD                [A^2/Hz]
F0_REAL = 5e9            # canonical carrier                          [Hz]

KAPPA2 = GAMMA_RMS ** 2 * SI / (2 * QMAX ** 2)   # [rad^2/s]  ([P2] Eq.11/12)
KAPPA = np.sqrt(KAPPA2)                          # [rad/sqrt(s)]

# ----------------------------------------------------------------------------
# simulation grid (normalized carrier; SI-valued noise constants)
# ----------------------------------------------------------------------------
FS = 64.0                # sample rate                                [Hz]
N = 2 ** 23              # samples  -> total time 131072 s
F0_SIM = 16.0            # simulated carrier (4 samples/period)       [Hz]


def overlapping_adev(x, tau0, ms):
    """Overlapping Allan deviation from time-error samples x at spacing tau0.
    (replicated verbatim from simulations/lab_19_allan.py)"""
    x = np.asarray(x)
    n = len(x)
    out = []
    for m in ms:
        if n - 2 * m < 1:
            out.append(np.nan)
            continue
        d = x[2 * m:] - 2 * x[m:-m] + x[:-2 * m]
        avar = np.sum(d ** 2) / (2 * (n - 2 * m) * (m * tau0) ** 2)
        out.append(np.sqrt(avar))
    return np.array(out)


def main():
    print("[lab_23] diffusion-constant dictionary ...")
    dt = 1.0 / FS
    t = np.arange(N) * dt

    # ---- ISF-weighted white-noise phase ([P1] Eq.(11) as a cumulative sum) --
    # Gamma(theta) = -sqrt(2)*Gamma_rms*sin(theta): a sinusoidal ISF scaled so
    # that its rms is exactly the representative Gamma_rms = 0.5.
    gamma = -np.sqrt(2.0) * GAMMA_RMS * np.sin(2 * np.pi * F0_SIM * t)
    i_n = white_noise(N, SI, FS, RNG)               # one-sided PSD = SI
    dphi = gamma * i_n * dt / QMAX                  # [rad] per sample
    phi = np.cumsum(dphi)

    print(f"theory kappa^2 = Gamma_rms^2*Si/(2*qmax^2) = {KAPPA2:.4f}")

    # ------------------------------------------------------------------ (a)
    # phase-variance slope: Var[dphi(tau)] should be kappa^2 * tau
    lags = np.unique(np.round(np.logspace(np.log10(0.25 * FS),
                                          np.log10(1000 * FS), 17)).astype(int))
    taus_v = lags * dt
    var_meas = np.array([np.mean((phi[m:] - phi[:-m]) ** 2) for m in lags])
    qhat_var = float(np.median(var_meas / taus_v))
    slope_loglog = float(np.polyfit(np.log(taus_v), np.log(var_meas), 1)[0])
    print(f"(a) var-slope qhat = {qhat_var:.4f}")
    print(f"(a) log-log exponent of Var vs tau = {slope_loglog:.3f}")
    print(f"(a) 'Var=2D|t|' with D=0.125 would need slope {2 * 0.125:.3f} -> falsified")

    # ------------------------------------------------------------------ (b)
    # Lorentzian linewidth of the carrier
    x = np.cos(2 * np.pi * F0_SIM * t + phi)
    f, P = welch(x, fs=FS, nperseg=2 ** 19, scaling="density")
    off = f - F0_SIM
    m_fit = np.abs(off) < 0.12                      # ~ +-6 half-widths
    # Lorentzian => 1/S is LINEAR in off^2:  1/S = c0 + c1*off^2,
    # with kappa^2 = 4*pi*sqrt(c0/c1)  and  FWHM = 2*sqrt(c0/c1).
    # weight by P^2 so the fit is least-squares in the P domain (the raw
    # 1/P fit over-weights the noisy far tail).
    c1, c0 = np.polyfit(off[m_fit] ** 2, 1.0 / P[m_fit], 1, w=P[m_fit] ** 2)
    fwhm_fit = 2.0 * np.sqrt(c0 / c1)
    qhat_lor = 2 * np.pi * fwhm_fit
    # independent half-max reading on a lightly smoothed PSD
    ker = np.ones(15) / 15.0
    Ps = np.convolve(P, ker, mode="same")
    pk = Ps[m_fit].max()
    half = off[m_fit][Ps[m_fit] >= 0.5 * pk]
    fwhm_meas = float(half.max() - half.min())
    print(f"(b) Lorentzian-fit FWHM = {fwhm_fit * 1e3:.2f} mHz")
    print(f"(b) half-max read FWHM = {fwhm_meas * 1e3:.2f} mHz")
    print(f"(b) qhat from FWHM = 2*pi*FWHM = {qhat_lor:.4f}")
    print(f"(b) theory FWHM = kappa^2/(2*pi) = {KAPPA2 / (2 * np.pi) * 1e3:.2f} mHz")

    # ------------------------------------------------------------------ (c)
    # overlapping ADEV of the fractional frequency (white FM)
    x_time = phi / (2 * np.pi * F0_SIM)             # time error [s]
    ms = np.unique(np.round(np.logspace(np.log10(32),
                                        np.log10(N // 16), 22)).astype(int))
    taus_a = ms * dt
    adev = overlapping_adev(x_time, dt, ms)
    band = (taus_a >= 1.0) & (taus_a <= 1024.0)
    qhat_adev = float(np.median((adev[band] ** 2) * 4 * np.pi ** 2
                                * F0_SIM ** 2 * taus_a[band]))
    print(f"(c) qhat from ADEV = {qhat_adev:.4f}")
    print(f"(c) ADEV(1 s)*2*pi*f0_sim = {np.interp(1.0, taus_a, adev) * 2 * np.pi * F0_SIM:.4f}")

    # ------------------------------------------------------------------ (d)
    # S_phi(f): one-sided 2*kappa^2/(2*pi*f)^2
    f_p, P_phi = welch(phi, fs=FS, nperseg=2 ** 16,
                       detrend="linear", scaling="density")
    band_p = (f_p >= 0.1) & (f_p <= 4.0)
    qhat_sphi = float(np.median(P_phi[band_p] * (2 * np.pi * f_p[band_p]) ** 2 / 2))
    print(f"(d) qhat from S_phi plateau = {qhat_sphi:.4f}")

    # ------------------------------------------------------------- analytic
    # canonical 5-GHz numbers derived from the SAME kappa^2
    dw = 2 * np.pi * 1e6
    L2 = 10 * np.log10(KAPPA2 / dw ** 2)            # clean time-domain /2
    L4 = 10 * np.log10(KAPPA2 / (2 * dw ** 2))      # [P1] Eq.(21) SSB /4
    fwhm_rep = KAPPA2 / (2 * np.pi)
    fwhm_lc = (0.5 * SI / (2 * QMAX ** 2)) / (2 * np.pi)   # Gamma_rms=1/sqrt(2)
    b_m2 = KAPPA2 / (2 * np.pi ** 2)                # S_phi = b_m2 / f^2
    h0 = KAPPA2 / (2 * np.pi ** 2 * F0_REAL ** 2)   # white-FM S_y level
    sy_1s = np.sqrt(h0 / 2.0)
    kappa_t = KAPPA / (2 * np.pi * F0_REAL)         # timing version [sqrt(s)]
    sdt_1us = kappa_t * np.sqrt(1e-6)
    print(f"kappa = {KAPPA:.4f}")
    print(f"kappa_t = kappa/(2*pi*f0) = {kappa_t:.4e}")
    print(f"sigma_dt(1 us) = {sdt_1us * 1e15:.2f} fs")
    print(f"L(1 MHz) clean /2 = {L2:.1f} dBc/Hz")
    print(f"L(1 MHz) [P1] /4 = {L4:.1f} dBc/Hz")
    print(f"FWHM (Gamma_rms=0.5) = {fwhm_rep * 1e3:.2f} mHz")
    print(f"FWHM (true LC, Gamma_rms=1/sqrt2) = {fwhm_lc * 1e3:.2f} mHz")
    print(f"b_-2 = kappa^2/(2*pi^2) = {b_m2:.3e}")
    print(f"h0 (5 GHz) = {h0:.3e}")
    print(f"sigma_y(1 s) at 5 GHz = {sy_1s:.3e}")

    # ---------------------------------------------------------------- figure
    fig, axes = plt.subplots(2, 2, figsize=(13.5, 9.6))

    ax = axes[0, 0]
    ax.loglog(taus_v, var_meas, "o", ms=4, color="tab:blue", label="量測 Var[Δφ(τ)]")
    ax.loglog(taus_v, KAPPA2 * taus_v, "k--", lw=1.6,
              label=r"$\kappa^2\tau=0.125\,\tau$（理論）")
    ax.loglog(taus_v, 2 * KAPPA2 * taus_v, color="tab:red", ls=":", lw=1.4,
              label=r"$2\times0.125\,\tau$（若 Var$=2D|t|$、$D=0.125$）")
    ax.set_xlabel(r"lag $\tau$ (s)")
    ax.set_ylabel(r"Var[$\Delta\phi(\tau)$]  [rad$^2$]")
    ax.set_title("(a) 相位方差斜率 → $\\kappa^2$")
    ax.legend(fontsize=8)
    ax.grid(True, which="both", alpha=0.3)

    ax = axes[0, 1]
    pos = off > 0
    ax.loglog(off[pos], P[pos], color="tab:blue", lw=0.7, alpha=0.55,
              label="模擬載波 PSD")
    fit_curve = 1.0 / (c0 + c1 * off ** 2)
    ax.loglog(off[pos], fit_curve[pos], "k--", lw=1.6, label="Lorentzian 擬合")
    ax.loglog(off[pos], 1.0 / (c1 * off[pos] ** 2), color="tab:red", ls=":",
              lw=1.3, label=r"$1/\Delta f^2$ 漸近")
    ax.axvline(fwhm_fit / 2, color="tab:green", ls="-.", lw=1.2,
               label=f"HWHM = {fwhm_fit / 2 * 1e3:.1f} mHz")
    ax.set_xlim(2e-4, 8)
    ax.set_xlabel(r"offset $\Delta f$ (Hz)")
    ax.set_ylabel(r"$S_x(f_0+\Delta f)$  [1/Hz]")
    ax.set_title(f"(b) Lorentzian 線寬：FWHM = {fwhm_fit * 1e3:.1f} mHz "
                 f"($\\kappa^2/2\\pi$ = {KAPPA2 / (2 * np.pi) * 1e3:.1f} mHz)")
    ax.legend(fontsize=8)
    ax.grid(True, which="both", alpha=0.3)

    ax = axes[1, 0]
    ax.loglog(taus_a, adev, "o-", ms=3.5, color="tab:blue", lw=1.0,
              label="overlapping ADEV（模擬）")
    ax.loglog(taus_a, KAPPA / (2 * np.pi * F0_SIM * np.sqrt(taus_a)), "k--",
              lw=1.6, label=r"$\kappa/(2\pi f_0\sqrt{\tau})$（理論，white FM）")
    ax.set_xlabel(r"averaging time $\tau$ (s)")
    ax.set_ylabel(r"$\sigma_y(\tau)$")
    ax.set_title("(c) white-FM ADEV：斜率 $-1/2$、水平截距給 $\\kappa$")
    ax.legend(fontsize=8)
    ax.grid(True, which="both", alpha=0.3)

    ax = axes[1, 1]
    posf = f_p > 0
    ax.loglog(f_p[posf], P_phi[posf], color="tab:blue", lw=0.9, alpha=0.7,
              label=r"模擬 $S_\phi(f)$")
    ax.loglog(f_p[posf], 2 * KAPPA2 / (2 * np.pi * f_p[posf]) ** 2, "k--",
              lw=1.6, label=r"$2\kappa^2/(2\pi f)^2$（理論，單邊）")
    ax.set_xlabel("frequency $f$ (Hz)")
    ax.set_ylabel(r"$S_\phi(f)$  [rad$^2$/Hz]")
    ax.set_title("(d) $1/f^2$ phase PSD：係數 $2\\kappa^2$（單邊）")
    ax.legend(fontsize=8)
    ax.grid(True, which="both", alpha=0.3)

    fig.suptitle("擴散常數字典：同一個 $\\kappa^2=\\Gamma_{rms}^2 S_i/(2q_{max}^2)"
                 "=0.125$ rad$^2$/s 的四件量測衣服", fontsize=13)
    savefig(fig, "diffusion_dictionary.png")


if __name__ == "__main__":
    main()
