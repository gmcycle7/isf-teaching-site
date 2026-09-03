"""
fig_subharmonic_injection.py

Goal
----
Numbers + figure for docs/06_design_insights/subharmonic_injection.md:
subharmonic (M:1) injection, i.e. an injection-locked clock multiplier (ILCM)
whose oscillator runs at f0 = N*f_ref and is realigned once per reference
period T_inj = N*T0.

Paper anchors (verified against the PDFs by the page)
-----------------------------------------------------
[P3] B. Hong & A. Hajimiri, JSSC 54(8) 2109-2121, Aug. 2019.
  Sec. IV p.2112: impulse-train locking, Eq.(19) dphi = +-q_inj/q_max,
  Eq.(21) dw = dphi/T_inj, Eq.(23) I_inj = 2 q_inj/T_inj (fundamental of a
  delta train); footnote 7: "This injection can also happen every M periods
  ..., corresponding to subharmonic locking."
[P4] B. Hong & A. Hajimiri, JSSC 54(8) 2122-2139, Aug. 2019.
  Eq.(28)-(29) p.2129: M:N averaging over N*T_inj of Gt((M/N) w_inj t + theta)
  * i_inj(t); text: "locking requires the Mth-multiple harmonics of the
  injection to interact with the Nth-multiple harmonics of the oscillator's
  ISF"; Eq.(30) is spelled out ONLY for the superharmonic (M = 1) sinusoid.
  The subharmonic (N_paper = 1, M_paper = N_site) case is derived on the page.

Model (pedagogical, phase-only, weak injection q_inj << q_max)
-------------------------------------------------------------
  * ISF (ideal LC toy)  Gamma(theta) = -sin(theta), Gt = Gamma/q_max [rad/C]
  * Route 1 (Fourier, [P4] Eq.(29) with M = N_site, N_paper = 1):
        Omega(theta) = I_dc*Gt_dc + sum_m (1/2)|I_{mN}||Gt_m| cos(m theta + ...)
        -> omega_L = (1/2) |I_N| |Gt_1|   (fundamental ISF x N-th INJECTION harmonic)
  * Route 2 (impulse train, [P3] Sec. IV + footnote 7, T_inj = N*T0):
        per-pulse map  theta_{k+1} = theta_k + dw0*T_inj + q_inj*Gt(theta_k)
        -> omega_L = q_inj*|Gt|_max / (N*T0)   (1/N scaling)
    The two routes coincide exactly for a delta train (|I_k| = 2 q_inj/T_inj).
  * Realignment factor  beta = -q_inj * Gt'(theta_ss)   (dimensionless);
    LC at zero detuning: beta = q_inj/q_max.  Stability 0 < beta < 2.
  * Discrete-time noise model (one update per T_inj), sampled just BEFORE
    each injection:
        theta-_{k+1} = (1-beta) theta-_k + beta*N*psi_k + w_{k+1}
        Var[w] = kappa^2 * T_inj  (site kappa^2 = 0.125 rad^2/s, white FM)
        psi_k  = reference phase error [rad at f_ref], white, Var = sigma_psi^2
    -> H_ref = beta/(1-(1-beta)z^-1), H_osc = (1-z^-1)/(1-(1-beta)z^-1) acting
       on the free-running random walk, z = exp(j 2 pi f T_inj).
    Closed forms verified by Monte-Carlo below:
        Var-  = (sigma_w^2 + beta^2 N^2 sigma_psi^2) / (beta (2-beta))
        Var+  = (1-beta)^2 Var-  + beta^2 N^2 sigma_psi^2
        time-averaged (osc only) = sigma_w^2 (1 - beta + beta^2/2)/(beta(2-beta))
  * Detuning-induced reference spur (first order): steady-state sawtooth of
    peak-to-peak dtheta_pp = |dw0| T_inj  ->  spur_1 = 20 log10(dtheta_pp/(2 pi))
    = 20 log10(|df0| / f_ref).

Canonical site values: f0 = 5 GHz, q_max = 1 pC, kappa^2 = 0.125 rad^2/s,
N = 20 -> f_ref = 250 MHz, q_inj = 50 fC, pulse width 10 ps.
Reference floor L_ref = -160 dBc/Hz (ASSUMED value for the worked example).
Ring case: q_max = 10 fC (lab_32) and kappa^2 from L(1 MHz) = -100 dBc/Hz.

Figure
------
  static/figures/subharmonic_injection_ilcm.png

Run
---
  PYTHONPATH=. python3 simulations/fig_subharmonic_injection.py   (~10 s)
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt

from plot_utils import savefig
from isf_utils import gamma_lc_ideal, gamma_asymmetric, compute_fourier_coefficients
from noise_utils import estimate_psd

# ---------------------------------------------------------------------------
# Canonical parameters
# ---------------------------------------------------------------------------
F0 = 5e9                      # oscillator frequency            [Hz]
T0 = 1.0 / F0                 # 200 ps                          [s]
QMAX = 1e-12                  # LC q_max                        [C]
KAPPA2 = 0.125                # phase-variance growth rate      [rad^2/s]  (diffusion_dictionary)
N_MULT = 20                   # multiplication ratio (paper's M; paper's N = 1)
FREF = F0 / N_MULT            # 250 MHz                         [Hz]
TINJ = 1.0 / FREF             # 4 ns = N*T0                     [s]
QINJ = 50e-15                 # injected charge per pulse       [C]
TAU_P = 10e-12                # rectangular pulse width         [s]
L_REF_DBC = -160.0            # ASSUMED white reference floor   [dBc/Hz]

QMAX_RING = 10e-15            # lab_32 ring node q_max = C_L V_DD = 10 fF x 1 V
L_RING_1MHZ = -100.0          # ring L(1 MHz) for the second worked case [dBc/Hz]

rng = np.random.default_rng(20260903)


def sinc(x):
    """sin(pi x)/(pi x) (numpy convention)."""
    return np.sinc(x)


def rect_harmonic(k, q, t_inj, tau):
    """|I_k| of a periodic rectangular pulse train, area q, period t_inj, width tau [A]."""
    return 2.0 * q / t_inj * np.abs(sinc(k * tau / t_inj))


def gamma_ring_p2(x, n_stages, eta=0.75):
    """[P2] App.B triangular ring ISF toy (A = 1), same construction as lab_39:
    height 1/f', half-width 1/f' [rad], f' = eta*N/pi. Rising pulse (+) at pi/2,
    falling pulse (-) at 3pi/2. TOY MODEL."""
    fp = eta * n_stages / np.pi
    h = 1.0 / fp
    w = 1.0 / fp

    def tri(center):
        d = np.angle(np.exp(1j * (x - center)))
        return np.clip(1.0 - np.abs(d) / w, 0.0, None)

    return h * (tri(np.pi / 2) - tri(3 * np.pi / 2))


def h_mag2(f, beta, t_inj):
    """|1/(1-(1-beta) z^-1)|^2, z = exp(j 2 pi f t_inj)."""
    z_inv = np.exp(-1j * 2 * np.pi * f * t_inj)
    return 1.0 / np.abs(1.0 - (1.0 - beta) * z_inv) ** 2


def h_osc_mag2(f, beta, t_inj):
    """|(1-z^-1)/(1-(1-beta) z^-1)|^2."""
    z_inv = np.exp(-1j * 2 * np.pi * f * t_inj)
    return np.abs(1.0 - z_inv) ** 2 / np.abs(1.0 - (1.0 - beta) * z_inv) ** 2


def g_timeavg(beta):
    """time-averaged output variance / sigma_w^2 (oscillator noise only)."""
    return (1.0 - beta + 0.5 * beta ** 2) / (beta * (2.0 - beta))


def map_lock_edge(n_mult, q_ratio, n_iter=4000, grid=601):
    """Largest |df0| [Hz] for which the per-pulse map with Gamma = -sin converges."""
    t_inj = n_mult * T0
    df_theory = q_ratio / (t_inj * 2 * np.pi)
    dfs = np.linspace(0.0, 1.3 * df_theory, grid)
    th = np.full(dfs.size, 0.3)
    for _ in range(n_iter):
        th = th + 2 * np.pi * dfs * t_inj - q_ratio * np.sin(th)
    # one more step to measure residual motion
    th2 = th + 2 * np.pi * dfs * t_inj - q_ratio * np.sin(th)
    locked = np.abs(np.angle(np.exp(1j * (th2 - th)))) < 1e-9
    return dfs[locked].max(), df_theory


def main():
    print("=" * 72)
    print("fig_subharmonic_injection.py  --  ILCM numbers (canonical site values)")
    print("=" * 72)
    print(f"f0 = {F0/1e9:.1f} GHz, N = {N_MULT}, f_ref = {FREF/1e6:.1f} MHz, "
          f"T_inj = {TINJ*1e9:.1f} ns, q_inj = {QINJ*1e15:.0f} fC, q_max = {QMAX*1e12:.0f} pC")

    # ------------------------------------------------------------------ (1)
    print("\n(1) Injection harmonics of a rectangular pulse (area q_inj, width tau_p)")
    i_pk = QINJ / TAU_P
    i_dc = QINJ / TINJ
    i_env = 2 * QINJ / TINJ
    i_n = rect_harmonic(N_MULT, QINJ, TINJ, TAU_P)
    s_n = sinc(N_MULT * TAU_P / TINJ)
    print(f"  pulse height I_p = q_inj/tau_p           = {i_pk*1e3:.2f} mA")
    print(f"  DC  I_0 = q_inj/T_inj                    = {i_dc*1e6:.2f} uA")
    print(f"  delta-train envelope 2 q_inj/T_inj       = {i_env*1e6:.2f} uA")
    print(f"  sinc(N f_ref tau_p) = sinc(f0 tau_p)     = {s_n:.5f}   (f0*tau_p = {F0*TAU_P:.3f})")
    print(f"  |I_N| (N = {N_MULT}, tau_p = {TAU_P*1e12:.0f} ps)      = {i_n*1e6:.2f} uA")
    for tau in (50e-12, 100e-12, 200e-12):
        print(f"  |I_N| for tau_p = {tau*1e12:4.0f} ps             = "
              f"{rect_harmonic(N_MULT, QINJ, TINJ, tau)*1e6:.3f} uA  "
              f"(sinc = {sinc(F0*tau):.4f})")
    # fixed pulse HEIGHT view: |I_N| = (2 I_p/(pi N)) sin(pi f0 tau_p)
    i_n_fixed_height_max = 2 * i_pk / (np.pi * N_MULT)
    print(f"  fixed-height view: |I_N| = (2 I_p/(pi N)) sin(pi f0 tau_p); "
          f"max at tau_p = T0/2 -> {i_n_fixed_height_max*1e6:.1f} uA (I_p = {i_pk*1e3:.0f} mA)")
    print("  pure sinusoid at f_ref: |I_k| = 0 for k >= 2  ->  |I_N| = 0  ->  omega_L = 0 (first order)")

    # ------------------------------------------------------------------ (2)
    print("\n(2) Lock range: route 1 (Fourier) vs route 2 (impulse train)")
    gt1 = 1.0 / QMAX                                # |Gt_1| of -sin/q_max [rad/C]
    wl_route1 = 0.5 * i_n * gt1
    wl_impulse = QINJ / (QMAX * TINJ)
    print(f"  |Gt_1| = 1/q_max                          = {gt1:.3e} rad/C")
    print(f"  route 1: omega_L = 1/2 |I_N| |Gt_1|       = {wl_route1:.4e} rad/s -> f_L = {wl_route1/2/np.pi/1e6:.4f} MHz")
    print(f"  route 2: omega_L = q_inj/(q_max N T0)     = {wl_impulse:.4e} rad/s -> f_L = {wl_impulse/2/np.pi/1e6:.4f} MHz")
    print(f"  ratio route1/route2                      = {wl_route1/wl_impulse:.5f}  (= sinc(f0 tau_p))")
    print(f"  fractional lock range f_L/f0 (impulse)   = {wl_impulse/(2*np.pi*F0)*1e6:.1f} ppm")
    # numerical map sweep vs 1/N
    print("  per-pulse map sweep (Gamma = -sin), measured lock edge / theory:")
    n_list = (5, 10, 20, 40)
    meas = []
    for n in n_list:
        m, th = map_lock_edge(n, QINJ / QMAX)
        meas.append(m)
        print(f"    N = {n:2d}: f_L,meas = {m/1e6:.4f} MHz, theory q_inj/(2 pi q_max N T0) = {th/1e6:.4f} MHz, "
              f"ratio = {m/th:.4f}")
    slope = np.polyfit(np.log(n_list), np.log(meas), 1)[0]
    print(f"    log-log slope of f_L vs N = {slope:.3f}  (theory -1)")
    # DC term of a unipolar train x ISF dc (asymmetric toy)
    XE = np.linspace(0, 2 * np.pi, 4097)
    a0, a, b, c, ph = compute_fourier_coefficients(XE, gamma_asymmetric(XE, 0.3), 4)
    gt_dc = (a0 / 2) / QMAX
    dw_dc = i_dc * gt_dc
    print(f"  DC term (unipolar train, asym. toy c0/2 = {a0/2:.3f}): I_0*Gt_dc = {dw_dc:.3e} rad/s "
          f"-> {dw_dc/2/np.pi/1e3:.0f} kHz static shift")

    # ------------------------------------------------------------------ (3)
    print("\n(3) Realignment factor beta = -q_inj Gt'(theta_ss)")
    beta_lc = QINJ / QMAX
    beta_lc_pulse = beta_lc * s_n
    print(f"  LC toy, zero detuning: beta = q_inj/q_max   = {beta_lc:.4f}  (10 ps pulse: x sinc -> {beta_lc_pulse:.4f})")
    print(f"  beta at detuning: beta = (q_inj/q_max) sqrt(1-(dw0/wL)^2); at 0.5 wL -> {beta_lc*np.sqrt(0.75):.4f}, "
          f"at 0.95 wL -> {beta_lc*np.sqrt(1-0.95**2):.4f}")
    k_e = -1.0 / np.log(1.0 - beta_lc)
    print(f"  1/e settling: k_e = -1/ln(1-beta)          = {k_e:.2f} injections (1/beta = {1/beta_lc:.1f}) "
          f"-> {k_e*TINJ*1e9:.1f} ns")
    print(f"  identity: beta/T_inj = {beta_lc/TINJ:.4e} rad/s  vs  omega_L(impulse) = {wl_impulse:.4e} rad/s  "
          f"(ratio {beta_lc/TINJ/wl_impulse:.4f})")
    # ring toy slope ([P2] App.B, N = 17, eta = 0.75)
    xg = np.linspace(0, 2 * np.pi, 200001)
    g_ring = gamma_ring_p2(xg, 17)
    dg = np.gradient(g_ring, xg)
    slope_ring = np.abs(dg).max()
    # slope of -sin at its zero crossing
    slope_lc = 1.0
    print(f"  ring toy [P2] App.B (N=17, eta=0.75): peak |Gamma| = {np.abs(g_ring).max():.4f}, "
          f"max |dGamma/dtheta| = {slope_ring:.4f} per rad  (LC -sin: peak 1, slope {slope_lc:.1f})")
    print(f"  -> same q_inj, same q_max: beta_ring/beta_LC = {slope_ring/slope_lc:.3f} (slope TIES in this toy)")
    q_small = 1e-15
    print(f"  -> same q_inj = 1 fC, site q_max: LC beta = {q_small/QMAX*slope_lc:.4f}, "
          f"ring (q_max = 10 fC) beta = {q_small/QMAX_RING*slope_ring:.4f}  (x{QMAX/QMAX_RING:.0f} from q_max)")
    # a 50 fC pulse into a 10 fC ring node is NOT weak injection:
    print(f"  (50 fC into q_max = 10 fC: q_inj/q_max = {QINJ/QMAX_RING:.0f} -> outside the linear model)")

    # ------------------------------------------------------------------ (4)
    print("\n(4) Noise: discrete-time first-order loop, Monte-Carlo vs closed forms")
    sig_w2 = KAPPA2 * TINJ
    s_psi = 2.0 * 10 ** (L_REF_DBC / 10)            # single-sided S_phi = 2 L (site convention)
    sig_psi2 = s_psi * FREF / 2                     # white over Nyquist [rad^2]
    print(f"  sigma_w^2 = kappa^2 T_inj = {sig_w2:.3e} rad^2 -> sigma_w = {np.sqrt(sig_w2)*1e6:.2f} urad "
          f"= {np.sqrt(sig_w2)/(2*np.pi*F0)*1e15:.2f} fs")
    print(f"  reference (ASSUMED L_ref = {L_REF_DBC:.0f} dBc/Hz white): S_psi = {s_psi:.1e} rad^2/Hz, "
          f"sigma_psi^2 = S_psi f_ref/2 = {sig_psi2:.3e} rad^2 -> {np.sqrt(sig_psi2)*1e6:.1f} urad "
          f"= {np.sqrt(sig_psi2)/(2*np.pi*FREF)*1e15:.1f} fs")
    beta = beta_lc
    K = 2 ** 20
    w = rng.normal(0.0, np.sqrt(sig_w2), K)
    psi = rng.normal(0.0, np.sqrt(sig_psi2), K)

    def run(w_seq, psi_seq):
        th = np.zeros(K)
        x = 0.0
        for k in range(1, K):
            x = (1 - beta) * x + beta * N_MULT * psi_seq[k - 1] + w_seq[k]
            th[k] = x
        return th

    th_osc = run(w, np.zeros(K))
    th_ref = run(np.zeros(K), psi)
    th_all = run(w, psi)
    var_minus_th = (sig_w2 + beta ** 2 * N_MULT ** 2 * sig_psi2) / (beta * (2 - beta))
    var_minus_osc_th = sig_w2 / (beta * (2 - beta))
    var_plus_osc_th = (1 - beta) ** 2 * var_minus_osc_th
    var_ref_th = beta * N_MULT ** 2 * sig_psi2 / (2 - beta)
    burn = 10000
    v_osc = th_osc[burn:].var()
    v_plus_osc = ((1 - beta) * th_osc[burn:]).var()
    v_ref_plus = ((1 - beta) * th_ref[burn:-1] + beta * N_MULT * psi[burn:-1]).var()
    v_all = th_all[burn:].var()
    print(f"  osc only : Var- MC = {v_osc:.4e}, theory sigma_w^2/(beta(2-beta)) = {var_minus_osc_th:.4e}, "
          f"ratio {v_osc/var_minus_osc_th:.4f}")
    print(f"             Var+ MC = {v_plus_osc:.4e}, theory (1-beta)^2 x = {var_plus_osc_th:.4e}, "
          f"ratio {v_plus_osc/var_plus_osc_th:.4f}")
    # time-averaged variance with 8 sub-steps of random walk per interval
    sub = 4
    thp = (1 - beta) * th_osc[burn:]
    steps = rng.normal(0.0, np.sqrt(sig_w2 / sub), (thp.size, sub))
    half = rng.normal(0.0, np.sqrt(sig_w2 / sub / 2), (thp.size, sub))
    walk = np.cumsum(steps, axis=1) - steps + half     # random walk sampled at the MID-point of each sub-interval
    var_tavg_mc = (thp[:, None] + walk).var()
    var_tavg_th = sig_w2 * g_timeavg(beta)
    print(f"             time-averaged Var MC = {var_tavg_mc:.4e}, theory sigma_w^2(1-b+b^2/2)/(b(2-b)) = "
          f"{var_tavg_th:.4e}, ratio {var_tavg_mc/var_tavg_th:.4f}")
    print(f"             -> sigma_out (time-avg) = {np.sqrt(var_tavg_th)*1e6:.2f} urad = "
          f"{np.sqrt(var_tavg_th)/(2*np.pi*F0)*1e15:.2f} fs ; sigma_out(before) = "
          f"{np.sqrt(var_minus_osc_th)/(2*np.pi*F0)*1e15:.2f} fs ; sigma_out(after) = "
          f"{np.sqrt(var_plus_osc_th)/(2*np.pi*F0)*1e15:.2f} fs")
    print(f"             continuous-time check S_n/(4 omega_c), S_n = 2 kappa^2, omega_c = beta/T_inj: "
          f"{2*KAPPA2/(4*beta/TINJ):.4e} rad^2")
    print(f"  ref only : Var+ MC = {v_ref_plus:.4e}, theory beta N^2 sigma_psi^2/(2-beta) = {var_ref_th:.4e}, "
          f"ratio {v_ref_plus/var_ref_th:.4f} -> {np.sqrt(var_ref_th)*1e6:.1f} urad = "
          f"{np.sqrt(var_ref_th)/(2*np.pi*F0)*1e15:.2f} fs at the {F0/1e9:.0f} GHz output")
    print(f"  both     : Var- MC = {v_all:.4e}, theory = {var_minus_th:.4e}, ratio {v_all/var_minus_th:.4f}")

    # PSD checks (oscillator-only run)
    f, S_osc = estimate_psd(th_osc[burn:], FREF, nperseg=2 ** 14)
    f = f[1:]
    S_osc = S_osc[1:]
    S_free = 2 * KAPPA2 / (2 * np.pi * f) ** 2                 # single-sided free-running 1/f^2
    S_th_disc = 2 * sig_w2 * TINJ * h_mag2(f, beta, TINJ)      # discrete-time form
    S_th_cont = h_osc_mag2(f, beta, TINJ) * S_free              # |H_osc|^2 S_free (page form)
    f_c = beta * FREF / (2 * np.pi * (1 - beta))
    band_lo = f < f_c / 10
    band_hi = (f > 10 * f_c) & (f < FREF / 8)
    plateau_th = 2 * sig_w2 * TINJ / beta ** 2
    print(f"  PSD osc-only: plateau MC/theory (f < f_c/10) = {np.mean(S_osc[band_lo])/plateau_th:.3f}  "
          f"(theory 2 kappa^2 T_inj^2/beta^2 = {plateau_th:.3e} rad^2/Hz -> L = {10*np.log10(plateau_th/2):.1f} dBc/Hz)")
    print(f"                MC / |H_osc|^2 S_free (10 f_c .. f_ref/8) = {np.mean(S_osc[band_hi]/S_th_cont[band_hi]):.3f}; "
          f"|H_osc|^2 S_free / discrete form at f_ref/8 = {S_th_cont[band_hi][-1]/S_th_disc[band_hi][-1]:.3f}")
    ratio = S_osc / S_free
    target = 0.5 / (1 - beta) ** 2
    idx = np.where((ratio[1:] >= target) & (ratio[:-1] < target))[0]
    f_c_meas = f[idx[0]] if idx.size else np.nan
    print(f"  corner: theory f_c = beta f_ref/(2 pi (1-beta)) = {f_c/1e6:.3f} MHz (small-beta: "
          f"{beta*FREF/2/np.pi/1e6:.3f} MHz); MC first crossing of |H_osc|^2 = 0.5/(1-beta)^2 at {f_c_meas/1e6:.3f} MHz")
    print(f"  in-band reference: N^2 = {N_MULT**2} -> +{20*np.log10(N_MULT):.2f} dB; "
          f"N^2 S_psi = {N_MULT**2*s_psi:.2e} rad^2/Hz -> L = {10*np.log10(N_MULT**2*s_psi/2):.1f} dBc/Hz in-band floor")
    print(f"  out-of-band excess of VCO noise 1/(1-beta)^2 = {1/(1-beta)**2:.4f} ({20*np.log10(1/(1-beta)):.2f} dB)")

    # ------------------------------------------------------------------ (5)
    print("\n(5) beta optimum (osc random walk vs N^2 reference) and N sweep")
    betas = np.linspace(0.001, 1.999, 40000)

    def total_var(sw2, spsi2, n):
        return sw2 * g_timeavg(betas) + n ** 2 * spsi2 * betas / (2 - betas)

    tot = total_var(sig_w2, sig_psi2, N_MULT)
    b_opt = betas[np.argmin(tot)]
    b_opt_sm = np.sqrt(sig_w2 / (N_MULT ** 2 * sig_psi2))
    print(f"  LC (kappa^2 = {KAPPA2}): beta_opt numeric = {b_opt:.4f}, small-beta sqrt(sigma_w^2/(N^2 sigma_psi^2)) = {b_opt_sm:.4f}")
    print(f"      sigma_out,min = {np.sqrt(tot.min())*1e6:.1f} urad = {np.sqrt(tot.min())/(2*np.pi*F0)*1e15:.2f} fs; "
          f"at beta = {beta_lc}: {np.sqrt(total_var(sig_w2, sig_psi2, N_MULT)[np.argmin(np.abs(betas-beta_lc))])/(2*np.pi*F0)*1e15:.2f} fs")
    print(f"      q_inj,opt = beta_opt q_max = {b_opt*QMAX*1e15:.2f} fC -> f_L = {b_opt*FREF/2/np.pi/1e3:.0f} kHz")
    # ring case
    s_phi_ring = 2 * 10 ** (L_RING_1MHZ / 10)
    kappa2_ring = s_phi_ring * (2 * np.pi * 1e6) ** 2 / 2
    sw2_ring = kappa2_ring * TINJ
    tot_r = total_var(sw2_ring, sig_psi2, N_MULT)
    b_opt_r = betas[np.argmin(tot_r)]
    print(f"  ring (L(1 MHz) = {L_RING_1MHZ:.0f} dBc/Hz -> kappa^2 = {kappa2_ring:.0f} rad^2/s): sigma_w = "
          f"{np.sqrt(sw2_ring)*1e3:.3f} mrad = {np.sqrt(sw2_ring)/(2*np.pi*F0)*1e15:.0f} fs per T_inj")
    print(f"      beta_opt numeric = {b_opt_r:.3f}; sigma_out,min = {np.sqrt(tot_r.min())*1e3:.2f} mrad = "
          f"{np.sqrt(tot_r.min())/(2*np.pi*F0)*1e15:.0f} fs; at beta = 0.05: "
          f"{np.sqrt(tot_r[np.argmin(np.abs(betas-0.05))])/(2*np.pi*F0)*1e15:.0f} fs; at beta = 1: "
          f"{np.sqrt(tot_r[np.argmin(np.abs(betas-1.0))])/(2*np.pi*F0)*1e15:.0f} fs")
    # N sweep at fixed f0, beta re-optimized, reference TIME jitter fixed
    print("  N sweep (fixed f0, fixed reference time jitter, beta re-optimized), LC case:")
    sig_t_ref = np.sqrt(sig_psi2) / (2 * np.pi * FREF)
    ns = np.array([5, 10, 20, 40, 80])
    st_min = []
    for n in ns:
        fr = F0 / n
        tinj = 1 / fr
        sw2 = KAPPA2 * tinj
        spsi2 = (2 * np.pi * fr * sig_t_ref) ** 2
        tv = total_var(sw2, spsi2, n)
        st_min.append(np.sqrt(tv.min()) / (2 * np.pi * F0))
        print(f"    N = {n:2d}: f_ref = {fr/1e6:6.1f} MHz, beta_opt = {betas[np.argmin(tv)]:.4f}, "
              f"sigma_t,min = {st_min[-1]*1e15:.2f} fs")
    st_min = np.array(st_min)
    exp_n = np.polyfit(np.log(ns), np.log(st_min), 1)[0]
    print(f"    log-log slope sigma_t,min vs N = {exp_n:.3f}  (small-beta prediction +1/4)")

    # ------------------------------------------------------------------ (6)
    print("\n(6) Detuning-induced reference spur (first-order sawtooth)")
    df0 = 100e3
    dth_pp = 2 * np.pi * df0 * TINJ
    spur_th = 20 * np.log10(dth_pp / (2 * np.pi))
    print(f"  df0 = {df0/1e3:.0f} kHz -> dtheta_pp = 2 pi df0 T_inj = {dth_pp*1e3:.3f} mrad; "
          f"spur_1 = 20 log10(dtheta_pp/2pi) = 20 log10(df0/f_ref) = {spur_th:.2f} dBc")
    # numeric: build the steady-state sawtooth PM, FFT
    per = 2048
    spp = 64
    t = np.arange(per * spp) * (TINJ / spp)
    phi_saw = dth_pp * ((t / TINJ) % 1.0 - 0.5)
    X = np.abs(np.fft.fft(np.exp(1j * phi_saw)))
    spur_num = 20 * np.log10(X[per] / X[0])
    spur_num2 = 20 * np.log10(X[2 * per] / X[0])
    print(f"  FFT of exp(j phi_saw): spur at f_ref = {spur_num:.2f} dBc, at 2 f_ref = {spur_num2:.2f} dBc "
          f"(theory k=2: {20*np.log10(dth_pp/(4*np.pi)):.2f})")
    for d in (10e3, 1e6):
        print(f"  df0 = {d/1e3:6.0f} kHz -> spur_1 = {20*np.log10(d/FREF):.1f} dBc")
    print(f"  in beta form: dtheta_pp = beta |dtheta_offset|; at df0 = 100 kHz the lock point sits "
          f"{dth_pp/beta_lc*1e3:.1f} mrad from the zero-kick phase (beta = {beta_lc})")

    # ------------------------------------------------------------------ figure
    fig, axs = plt.subplots(2, 2, figsize=(12, 8.6))

    ax = axs[0, 0]
    ks = np.arange(1, 61)
    for tau, col in ((10e-12, "C0"), (50e-12, "C1"), (100e-12, "C2")):
        env = np.abs(sinc(ks * tau / TINJ))
        ax.plot(ks, env, "o-", ms=3, color=col, label=rf"$\tau_p$ = {tau*1e12:.0f} ps（$f_0\tau_p$ = {F0*tau:.2f}）")
    ax.axvline(N_MULT, color="k", ls="--", lw=1)
    ax.plot([1], [1.0], "r*", ms=13, label="純正弦：只有 k = 1")
    ax.text(N_MULT + 0.8, 0.92, rf"k = N = {N_MULT}：鎖定用的諧波", fontsize=9)
    ax.set_xlabel("注入諧波序號 k（頻率 k·f_ref）")
    ax.set_ylabel(r"$\vert I_k\vert\,/\,(2q_{inj}/T_{inj})$（sinc 包絡）")
    ax.set_title("(a) 矩形脈衝的注入諧波：鎖定要的是第 N 個")
    ax.set_ylim(-0.02, 1.08)
    ax.legend(fontsize=8, loc="lower left")

    ax = axs[0, 1]
    nn = np.linspace(2, 64, 200)
    ax.loglog(nn, QINJ / (QMAX * nn * T0) / (2 * np.pi) / 1e6, "k-", label=r"理論 $f_L=\frac{q_{inj}}{2\pi q_{max}NT_0}\propto 1/N$")
    ax.loglog(n_list, np.array(meas) / 1e6, "ro", ms=7, label="per-pulse map 掃頻量測")
    ax.set_xlabel("倍頻比 N（$f_{ref}=f_0/N$）")
    ax.set_ylabel("半 lock range $f_L$ [MHz]")
    ax.set_title(rf"(b) lock range ∝ 1/N（$q_{{inj}}$ = {QINJ*1e15:.0f} fC, $q_{{max}}$ = 1 pC）")
    ax.legend(fontsize=8)

    ax = axs[1, 0]
    ax.loglog(f / 1e6, S_free, color="0.6", label=r"自由跑 $S_{free}=2\kappa^2/\omega^2$")
    ax.loglog(f / 1e6, S_osc, color="C0", lw=1.0, alpha=0.8, label=r"MC：鎖定後 $S_\theta$（自身雜訊）")
    ax.loglog(f / 1e6, S_th_cont, "k--", lw=1.2, label=r"$\vert H_{osc}\vert^2 S_{free}$")
    S_ref_out = N_MULT ** 2 * s_psi * beta ** 2 * h_mag2(f, beta, TINJ)
    ax.loglog(f / 1e6, S_ref_out, color="C3", ls=":", lw=1.6, label=r"$N^2\vert H_{ref}\vert^2 S_{ref}$（假設 −160 dBc/Hz）")
    ax.axvline(f_c / 1e6, color="C2", ls="--", lw=1)
    ax.text(f_c / 1e6 * 1.1, S_free[0] * 0.3, rf"$f_c\approx\beta f_{{ref}}/2\pi$ = {f_c/1e6:.2f} MHz", fontsize=8, color="C2")
    ax.set_xlabel("offset 頻率 f [MHz]")
    ax.set_ylabel(r"$S_\theta(f)$ [rad$^2$/Hz]（單邊）")
    ax.set_title(rf"(c) 一階離散迴路的雜訊整形（β = {beta:.2f}, N = {N_MULT}）")
    ax.set_xlim(f[0] / 1e6, FREF / 2 / 1e6)
    ax.legend(fontsize=7.5, loc="lower left")

    ax = axs[1, 1]
    kk = np.arange(0, 80)
    for b, lab, col in ((beta_lc, rf"LC：β = {beta_lc:.2f}（$q_{{inj}}/q_{{max}}$ = 50 fC / 1 pC）", "C0"),
                        (0.5, "β = 0.5（例：ring 節點 $q_{max}$ 小、$q_{inj}/q_{max}$ 大）", "C1"),
                        (1.0, "β = 1（一步對齊，MDLL 式硬重置）", "C2")):
        ax.semilogy(kk, np.maximum((1 - b) ** kk, 1e-6), "o-", ms=3, color=col, label=lab)
    ax.axhline(np.exp(-1), color="k", ls=":", lw=1)
    ax.axvline(1 / beta_lc, color="C0", ls=":", lw=1)
    ax.text(1 / beta_lc + 1, 0.5, rf"1/β = {1/beta_lc:.0f} 次注入 ≈ 1/e", fontsize=8, color="C0")
    ax.set_xlabel("注入次數 k（每次相隔 $T_{inj}=NT_0$）")
    ax.set_ylabel(r"殘餘相位誤差 $\vert\delta\theta_k/\delta\theta_0\vert=(1-\beta)^k$")
    ax.set_title("(d) 線性化 per-pulse map 的收斂：$\\delta\\theta_{k+1}=(1-\\beta)\\delta\\theta_k$")
    ax.set_ylim(1e-6, 2)
    ax.legend(fontsize=8, loc="lower left")

    fig.suptitle(rf"Subharmonic injection ×{N_MULT}：$f_0$ = 5 GHz, $f_{{ref}}$ = 250 MHz, "
                 r"$\Gamma=-\sin\theta$, $q_{max}$ = 1 pC（toy model）", fontsize=12)
    savefig(fig, "subharmonic_injection_ilcm.png")


if __name__ == "__main__":
    main()
