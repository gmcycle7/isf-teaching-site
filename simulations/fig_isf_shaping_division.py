"""
fig_isf_shaping_division.py -- ISF shaping for even-ratio injection-locked
frequency division ([P4] Sec. VII-A, Fig. 15-16, Table IV, p.2132-2134).

Companion script for docs/06_design_insights/injection_locked_division.md.

PEDAGOGICAL TOY, NOT TRANSISTOR-LEVEL.  A single-ended inverter-chain ring
stage is caricatured by an ISF with two Gaussian pulses per period: a negative
one at the falling edge (phase pi/2) and a positive one at the rising edge
(phase 3*pi/2), following the shape of [P4] Fig. 16.  Each pulse's height and
width are taken proportional to the edge time (ISF peak ~ 1/slope, pulse
width ~ transition time, [P2] Sec. IV), with the rise/fall times of
[P4] Table IV:

    (a) exactly symmetric   t_F = t_R = 44.4 ps  (mean of Table IV's 37.93/50.92;
                            makes footnote 14's Gamma(x+pi) = -Gamma(x) EXACT)
    (b) PFET-dominant       t_F/t_R = 60.83/31.73 ps
    (c) NFET-dominant       t_F/t_R = 26.35/87.44 ps
    (console only) Table IV's "fairly symmetric" 37.93/50.92 ps

What is shown / checked
-----------------------
  top row    : [P4] Fig. 15 logic.  Gamma_tilde((w_inj/2) t + theta_u) times a
               second-harmonic sinusoidal injection i_inj(t) = I_inj cos(w_inj t)
               over three oscillation periods, and its NT_inj-average, at the
               phase theta_u that maximizes the average ([P4] footnote 15):
                 w_L^+ := max_theta < Gamma_tilde((w_inj/N)t+theta) i_inj(t) >_{N T_inj}
               For a half-wave-symmetric ISF (Gamma(x+pi) = -Gamma(x), footnote
               14) the kicks of consecutive injection cycles cancel -> average 0
               for every theta.  With asymmetry a net kick survives.
  bottom row : [P4] Fig. 16 logic.  Normalized magnitudes |c_n|/Gamma_rms of the
               first five Fourier coefficients (n = 0..4).  Half-wave symmetry
               kills n = 0, 2, 4.

Printed markers
---------------
  * |c_2|/Gamma_rms of the toy for the three cases (compare [P4] Table IV
    0.0927 / 0.301 / 0.371 -- the toy is only meant to reproduce the trend)
  * brute-force w_L^+ (footnote 15) / closed form (1/2) I_inj |Gamma_tilde_2|
    ([P4] Eq.(30)) -> 1.000 for the asymmetric cases; ~0 for the symmetric one
  * ratio of the toy's asymmetric-to-"fairly symmetric" |Gamma_tilde_2| (paper: x15.3 / x23.3)

Figure produced: static/figures/isf_shaping_division.png
"""
import numpy as np
import matplotlib.pyplot as plt

from simulations.common.plot_utils import savefig

T_OSC = 1e-9            # 1-GHz ring, as in [P4] Fig. 16 / Table IV
QMAX = 1e-12            # 1 pC (site canonical; only sets the rad/C scale)
I_INJ = 1.5e-3          # 1.5 mA, as in [P4] Table IV
N_DIV = 2
CASES = [
    ("(a) exactly symmetric  t_F = t_R", 44.425e-12, 44.425e-12, "tab:blue"),
    ("(b) PFET-dominant  t_F/t_R = 1.92", 60.83e-12, 31.73e-12, "tab:red"),
    ("(c) NFET-dominant  t_F/t_R = 0.30", 26.35e-12, 87.44e-12, "tab:green"),
]
T_REF = 50e-12          # reference edge time: pulse height 1/qmax at t_edge = T_REF


def toy_isf(x, t_f, t_r):
    """Two-pulse ring-stage ISF caricature, x in rad (2*pi periodic), rad/C."""
    x = np.mod(x, 2 * np.pi)
    sig_f = 2 * np.pi * t_f / T_OSC
    sig_r = 2 * np.pi * t_r / T_OSC
    a_f = (t_f / T_REF) / QMAX
    a_r = (t_r / T_REF) / QMAX
    g = np.zeros_like(x)
    for k in (-1, 0, 1):  # wrap neighbours so the pulses are periodic
        g += -a_f * np.exp(-(x - np.pi / 2 - 2 * np.pi * k) ** 2 / (2 * sig_f ** 2))
        g += a_r * np.exp(-(x - 3 * np.pi / 2 - 2 * np.pi * k) ** 2 / (2 * sig_r ** 2))
    return g


def fourier_mags(t_f, t_r, nmax=4, npts=8192):
    x = np.linspace(0, 2 * np.pi, npts, endpoint=False)
    g = toy_isf(x, t_f, t_r)
    grms = np.sqrt(np.mean(g ** 2))
    X = np.fft.rfft(g) / npts
    mags = np.abs(X[: nmax + 1]) * 2.0          # |c_n| = 2|X_n| for n>=1 ...
    mags[0] = np.abs(X[0])                       # ... and the DC value for n = 0
    return mags, grms


def lock_edge_bruteforce(t_f, t_r, nth=721, npts=20000):
    """[P4] footnote 15: w_L^+ = max_theta <Gamma((w_inj/N)t+theta) i_inj(t)>_{N T_inj}."""
    w_inj = N_DIV * 2 * np.pi / T_OSC
    t = np.linspace(0, N_DIV * (2 * np.pi / w_inj), npts, endpoint=False)
    i_inj = I_INJ * np.cos(w_inj * t)
    thetas = np.linspace(0, 2 * np.pi, nth, endpoint=False)
    avg = np.array([np.mean(toy_isf(w_inj / N_DIV * t + th, t_f, t_r) * i_inj) for th in thetas])
    k = int(np.argmax(avg))
    return avg[k], thetas[k], t, i_inj


def main():
    fig, axes = plt.subplots(2, 3, figsize=(13.5, 7.2))
    print("=" * 72)
    print("[P4] Sec. VII-A toy: two-pulse ring-stage ISF, N = 2 sinusoidal injection")
    g2_list = []
    for j, (label, t_f, t_r, color) in enumerate(CASES):
        mags, grms = fourier_mags(t_f, t_r)
        g2 = mags[2]
        g2_list.append(g2)
        wl_bf, th_u, t, i_inj = lock_edge_bruteforce(t_f, t_r)
        wl_closed = 0.5 * I_INJ * g2
        ratio = wl_bf / wl_closed if wl_closed > 1e-3 else float("nan")  # nan: exact symmetry, c2 = 0
        print(f"  {label:36s} Grms = {grms/1e12:.3f} rad/pC  |c2|/Grms = {mags[2]/grms:.4f}  "
              f"|c0|/Grms = {mags[0]/grms:.4f}  |c4|/Grms = {mags[4]/grms:.4f}")
        print(f"      w_L+ brute force = {wl_bf:.4e} rad/s ; (1/2) I_inj |G2| = {wl_closed:.4e} rad/s ; "
              f"ratio = {ratio:.4f} ; theta_u = {np.degrees(th_u):.1f} deg ; 2 f_L = {2*wl_bf/(2*np.pi)/1e6:.2f} MHz")

        # ---- top row: Fig. 15 logic ------------------------------------
        w_inj = N_DIV * 2 * np.pi / T_OSC
        tt = np.linspace(0, 3 * T_OSC, 3000)
        ii = I_INJ * np.cos(w_inj * tt)
        gg = toy_isf(w_inj / N_DIV * tt + th_u, t_f, t_r)
        prod = gg * ii
        ax = axes[0, j]
        ax.plot(tt / T_OSC, prod / 1e9, color=color, lw=1.4,
                label=r"$i_{inj}(t)\,\tilde\Gamma[(\omega_{inj}/N)t+\theta_u]$")
        ax.fill_between(tt / T_OSC, prod / 1e9, 0, where=prod > 0, color="tab:red", alpha=0.25)
        ax.fill_between(tt / T_OSC, prod / 1e9, 0, where=prod < 0, color="tab:blue", alpha=0.25)
        ax.axhline(wl_bf / 1e9, color="green", ls="--", lw=1.6,
                   label=r"average $=\omega_L^+$ = %.3g Grad/s" % (wl_bf / 1e9)
                   if wl_closed > 1e-3 else r"average $=\omega_L^+\approx 0$ (kicks cancel)")
        ax.plot(tt / T_OSC, ii / I_INJ * np.max(np.abs(prod)) / 1e9 * 0.5, color="0.6", lw=0.8, alpha=0.8,
                label=r"$i_{inj}(t)$ (scaled, N=2)")
        ax.set_title(label, fontsize=10)
        ax.set_xlabel(r"$t/T_{osc}$")
        if j == 0:
            ax.set_ylabel("product [Grad/s]")
        ax.legend(loc="upper right", fontsize=7)

        # ---- bottom row: Fig. 16 logic ---------------------------------
        ax = axes[1, j]
        n = np.arange(5)
        ax.stem(n, mags / grms, linefmt=color, markerfmt="o", basefmt="k-")
        ax.set_ylim(0, 1.1)
        ax.set_xticks(n)
        ax.set_xlabel("harmonic n")
        if j == 0:
            ax.set_ylabel(r"$|c_n|/\Gamma_{rms}$")
        ax.set_title(r"$|c_2|/\Gamma_{rms}$ = %.3f   (%s)"
                     % (mags[2] / grms, ["half-wave symmetric: exactly 0",
                                         "[P4] Table IV: 0.301", "[P4] Table IV: 0.371"][j]), fontsize=9)

    m_fs, g_fs = fourier_mags(37.93e-12, 50.92e-12)
    print(f"  (console) Table IV 'fairly symmetric' t_F/t_R = 0.74 toy: |c2|/Grms = {m_fs[2]/g_fs:.4f} "
          f"(paper 0.0927), Grms = {g_fs/1e12:.3f} rad/pC")
    print(f"  toy |G2| enhancement vs the 'fairly symmetric' case: PFET x{g2_list[1]/m_fs[2]:.2f}, "
          f"NFET x{g2_list[2]/m_fs[2]:.2f}  (paper Table IV: x15.3, x23.3; exactly symmetric |c2| = {g2_list[0]:.1e} rad/C)")
    fig.suptitle("ISF shaping for /2 ILFD (toy two-pulse ring-stage ISF; [P4] Fig. 15-16 logic, Table IV edge times)",
                 fontsize=11)
    savefig(fig, "isf_shaping_division.png")


if __name__ == "__main__":
    main()
