"""
lab_32_mos_level1_ring.py

Goal
----
The honest step beyond toy models WITHOUT SPICE: a 3-stage single-ended CMOS
inverter ring oscillator where every stage is built from MOS **Level-1
(Shichman-Hodges) square-law device equations** (cutoff / triode / saturation,
lambda = 0), integrated in numpy with a fixed small time step.  Nothing about
the ISF is assumed: it is EXTRACTED by the impulse method of [P1]
(inject Delta q at a known phase, measure the persistent phase shift by
threshold-crossing comparison against an unperturbed run ~20 cycles later).

    MOS Level-1 equation-level (Shichman-Hodges), NOT SPICE/BSIM/PDK.

Device model (per transistor, lambda = 0, vds >= 0 after source/drain swap):
    cutoff     : vgs <= vt              -> id = 0
    triode     : vds <  vgs - vt        -> id = beta*[(vgs-vt)*vds - vds^2/2]
    saturation : vds >= vgs - vt        -> id = beta/2*(vgs-vt)^2
implemented as one clamped expression  id = beta*(vov - vde/2)*vde  with
vov = max(vgs - vt, 0), vde = min(vds, vov)   (exactly the piecewise law).

Circuit: 3 identical inverters in a ring.  Stage i: input = node (i-1) mod 3,
output = node i;  NMOS (source=0) pulls the node down, PMOS (source=VDD)
pulls it up; a lumped CL loads every node:

    CL * dV_i/dt = I_P(V_{i-1}, V_i) - I_N(V_{i-1}, V_i)

ISF extraction of node 1 (array index 0):
    Delta q = 0.5 fC  ->  Delta V = Delta q / CL = 0.05 V   ([P1] Eq.(9))
    inject at 24 phases theta_j = j*2*pi/24 (theta = 0 at node-1 rising
    VDD/2 crossing), wait >= 20 cycles, compare the threshold-crossing time
    with the unperturbed run (same integrator -> bias cancels), wrap to
    [-T/2, T/2), then
        Delta phi   = -omega0 * Delta t
        Gamma(theta) = Delta phi * q_max / Delta q ,  q_max = CL*VDD = 10 fC.

Expected [P2] signature: ISF energy concentrated near the node's own
transitions, dual-lobe shape (positive lobe at the rising edge -- extra
charge advances the phase; negative lobe at the falling edge -- extra charge
delays it), ~0 while the node sits at a rail (the driving inverter's low
output resistance swallows the charge).  Compare with [P2] Fig. 5 / Fig. 6,
p.793 (triangular approximation) and Eq.(16), p.794 (Gamma_rms ~ N^-3/4;
single N here, so scaling itself is NOT tested).

Figure
------
  static/figures/mos_level1_ring_isf.png
    (a) 3 node waveforms over one period, (b) extracted Gamma(theta) with the
    node-1 transition regions shaded, (c) |c_n| stems.

Run
---
    PYTHONPATH=. python simulations/lab_32_mos_level1_ring.py   (~25 s)
"""
import os
import sys
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.join(_HERE, "common"))

import numpy as np

# ---------------------------------------------------------------------------
# Circuit / device parameters (MOS Level-1, Shichman-Hodges; lambda = 0)
# ---------------------------------------------------------------------------
VDD = 1.0            # supply [V]
VTN = 0.4            # NMOS threshold [V]
VTP_ABS = 0.4        # |Vtp| [V]  (Vtp = -0.4 V)
KPN = 200e-6         # kn' = un*Cox [A/V^2]
KPP = 100e-6         # kp' = up*Cox [A/V^2]
WLN = 2.0            # NMOS W/L
WLP = 4.0            # PMOS W/L
BETA_N = KPN * WLN   # 400 uA/V^2  (device transconductance factor)
BETA_P = KPP * WLP   # 400 uA/V^2  (balanced inverter by construction)
CL = 10e-15          # load capacitance per node [F]
N_STAGES = 3

DT = 25e-15          # fixed integration step [s] (<< CL/g ~ 42 ps)
DQ = 0.5e-15         # injected charge [C]
DV = DQ / CL         # = 0.05 V  voltage step ([P1] Eq.(9): dV = dq/C)
QMAX = CL * VDD      # = 10 fC  ([P1] q_max = C*V_swing)
VTH = 0.5 * VDD      # threshold-crossing level for phase measurement
N_PHASES = 24
N_HARM = 8


# ---------------------------------------------------------------------------
# Level-1 drain current: one clamped expression == the piecewise textbook law
# (vector version for the 25-run batch, scalar version for fast single runs;
#  both use the identical formula -- cross-checked in main()).
# ---------------------------------------------------------------------------
def _sq_v(vgs, vds, beta, vt):
    """Square-law id for vds >= 0 (arrays). cutoff/triode/saturation unified:
    vov=max(vgs-vt,0); vde=min(vds,vov); id = beta*(vov - vde/2)*vde."""
    vov = np.maximum(vgs - vt, 0.0)
    vde = np.minimum(vds, vov)
    return beta * (vov - 0.5 * vde) * vde


def ring_dvdt_v(v):
    """dV/dt [V/s] for all nodes; v shape (..., 3); stage i input = node i-1.
    Reverse terms (source/drain swapped) keep the model physical if an
    injection pushes a node above VDD (PMOS then discharges it back)."""
    vin = np.roll(v, 1, axis=-1)
    i_n = (_sq_v(vin, np.maximum(v, 0.0), BETA_N, VTN)
           - _sq_v(vin - v, np.maximum(-v, 0.0), BETA_N, VTN))
    i_p = (_sq_v(VDD - vin, np.maximum(VDD - v, 0.0), BETA_P, VTP_ABS)
           - _sq_v(v - vin, np.maximum(v - VDD, 0.0), BETA_P, VTP_ABS))
    return (i_p - i_n) / CL


def _sq_s(vgs, vds, beta, vt):
    """Scalar twin of _sq_v (same clamped formula, plain floats for speed)."""
    vov = vgs - vt
    if vov < 0.0:
        vov = 0.0
    vde = vds if vds < vov else vov
    return beta * (vov - 0.5 * vde) * vde


def stage_dvdt_s(vg, v):
    """Scalar dV/dt of one node with input (gate) vg and output voltage v."""
    i_n = (_sq_s(vg, v if v > 0.0 else 0.0, BETA_N, VTN)
           - _sq_s(vg - v, -v if v < 0.0 else 0.0, BETA_N, VTN))
    i_p = (_sq_s(VDD - vg, VDD - v if v < VDD else 0.0, BETA_P, VTP_ABS)
           - _sq_s(v - vg, v - VDD if v > VDD else 0.0, BETA_P, VTP_ABS))
    return (i_p - i_n) / CL


# ---------------------------------------------------------------------------
# Integration helpers (fixed-dt forward Euler everywhere)
# ---------------------------------------------------------------------------
def settle_s(v, t_settle, dt):
    """Integrate a single ring (scalar fast path) without recording."""
    v0, v1, v2 = float(v[0]), float(v[1]), float(v[2])
    for _ in range(int(round(t_settle / dt))):
        d0 = stage_dvdt_s(v2, v0)
        d1 = stage_dvdt_s(v0, v1)
        d2 = stage_dvdt_s(v1, v2)
        v0 += dt * d0
        v1 += dt * d1
        v2 += dt * d2
    return np.array([v0, v1, v2])


def run_record_s(v, t_total, dt):
    """Integrate a single ring, recording all 3 node voltages each step."""
    n = int(round(t_total / dt))
    rec = np.empty((n + 1, 3))
    v0, v1, v2 = float(v[0]), float(v[1]), float(v[2])
    rec[0, 0], rec[0, 1], rec[0, 2] = v0, v1, v2
    for k in range(n):
        d0 = stage_dvdt_s(v2, v0)
        d1 = stage_dvdt_s(v0, v1)
        d2 = stage_dvdt_s(v1, v2)
        v0 += dt * d0
        v1 += dt * d1
        v2 += dt * d2
        rec[k + 1, 0], rec[k + 1, 1], rec[k + 1, 2] = v0, v1, v2
    return rec


def rising_crossings(x, dt, th=VTH):
    """Linearly interpolated times where x rises through th."""
    lo = x[:-1] < th
    hi = x[1:] >= th
    idx = np.nonzero(lo & hi)[0]
    frac = (th - x[idx]) / (x[idx + 1] - x[idx])
    return (idx + frac) * dt


def falling_crossings(x, dt, th=VTH):
    hi = x[:-1] >= th
    lo = x[1:] < th
    idx = np.nonzero(hi & lo)[0]
    frac = (x[idx] - th) / (x[idx] - x[idx + 1])
    return (idx + frac) * dt


def first_after(times, t_late):
    return float(times[times > t_late][0])


# ---------------------------------------------------------------------------
# ISF extraction: 24-phase impulse batch + 1 reference + 1 linearity check
# ---------------------------------------------------------------------------
def extract_isf_batch(v_settled, t0, T, dt):
    """Run 26 rings in lockstep from the same settled state:
       run 0            : unperturbed reference
       runs 1..24       : Delta q = DQ injected on node 1 at theta_j
       run 25           : Delta q = DQ/2 at theta_0 (linearity check)
    Returns (thetas, gamma, gamma_half0)."""
    thetas = 2.0 * np.pi * np.arange(N_PHASES) / N_PHASES
    k_inj = np.round((t0 + thetas / (2.0 * np.pi) * T) / dt).astype(int)
    inj = {int(k): r for r, k in enumerate(k_inj)}
    t_late = t0 + 22.0 * T                      # >= 20 cycles after injection
    n = int(round((t0 + 23.5 * T) / dt))
    R = N_PHASES + 2
    V = np.tile(np.asarray(v_settled, float), (R, 1))
    rec = np.empty((n + 1, R), np.float32)      # node-1 voltage, all runs
    rec[0] = V[:, 0]
    k_half = int(k_inj[0])
    for k in range(n):
        r = inj.get(k)
        if r is not None:
            V[r + 1, 0] += DV                   # dV = dq/CL  ([P1] Eq.(9))
        if k == k_half:
            V[N_PHASES + 1, 0] += 0.5 * DV      # linearity-check run
        V += dt * ring_dvdt_v(V)
        rec[k + 1] = V[:, 0]

    w0 = 2.0 * np.pi / T
    x = rec.astype(np.float64)
    tc_ref = first_after(rising_crossings(x[:, 0], dt), t_late)

    def gamma_of_run(col, dq):
        tc = first_after(rising_crossings(x[:, col], dt), t_late)
        dts = (tc - tc_ref + 0.5 * T) % T - 0.5 * T   # wrap to [-T/2, T/2)
        return -w0 * dts * QMAX / dq                   # dphi*qmax/dq

    gamma = np.array([gamma_of_run(r + 1, DQ) for r in range(N_PHASES)])
    gamma_half0 = gamma_of_run(N_PHASES + 1, 0.5 * DQ)
    return thetas, gamma, gamma_half0


def transition_windows(rec, t0, T, dt):
    """(10%..90%)-swing windows of node 1 around its rising edge at t0 and
    its falling edge ~T/2 later, in theta (rad, theta=0 at t0)."""
    x = rec[:, 0]
    i0 = int(round(t0 / dt))
    half = int(round(0.5 * T / dt))
    seg_pre = x[i0 - half:i0]
    i_r10 = i0 - half + int(np.nonzero(seg_pre < 0.1 * VDD)[0][-1])
    seg_post = x[i0:i0 + half]
    i_r90 = i0 + int(np.nonzero(seg_post > 0.9 * VDD)[0][0])
    t_fall = first_after(falling_crossings(x, dt), t0 + 0.2 * T)
    i_f = int(round(t_fall / dt))
    seg_pre = x[i_f - half:i_f]
    i_f90 = i_f - half + int(np.nonzero(seg_pre > 0.9 * VDD)[0][-1])
    seg_post = x[i_f:i_f + half]
    i_f10 = i_f + int(np.nonzero(seg_post < 0.1 * VDD)[0][0])
    w = 2.0 * np.pi / T
    rise = ((i_r10 * dt - t0) * w, (i_r90 * dt - t0) * w)   # straddles 0
    fall = ((i_f90 * dt - t0) * w, (i_f10 * dt - t0) * w)
    th_fall = (t_fall - t0) * w
    return rise, fall, th_fall


def in_window(th, lo, hi):
    """Is phase th inside [lo, hi] modulo 2*pi (lo may be negative)?"""
    return (th - lo) % (2.0 * np.pi) <= (hi - lo)


# ---------------------------------------------------------------------------
def main():
    import matplotlib.pyplot as plt
    from plot_utils import savefig
    from isf_utils import compute_fourier_coefficients, gamma_rms, \
        gamma_triangular

    t_start = time.time()
    print("[lab_32] MOS Level-1 (Shichman-Hodges) 3-stage ring, NOT "
          "SPICE/BSIM/PDK ...")
    print("beta_n = kn'*(W/L)n =", BETA_N, "A/V^2 ; beta_p = kp'*(W/L)p =",
          BETA_P, "A/V^2")  # -> 0.0004 A/V^2 兩者相同（對稱反相器）

    # scalar vs vector device model must be the SAME function (self-check)
    rng = np.random.default_rng(7)
    vtest = rng.uniform(-0.05, 1.05, (50, 3))
    dv_v = ring_dvdt_v(vtest)
    dv_s = np.array([[stage_dvdt_s(vtest[i, (j - 1) % 3], vtest[i, j])
                      for j in range(3)] for i in range(50)])
    print("scalar-vs-vector max |ddV/dt| =",
          "{:.1e}".format(float(np.max(np.abs(dv_v - dv_s)))), "V/s")
    # -> 0.0e+00 V/s（兩實作逐位元一致）

    # ---- steady oscillation: settle 10 ns coarse + 1 ns at DT -------------
    v = settle_s(np.array([0.9, 0.1, 0.5]), 10e-9, 100e-15)
    v = settle_s(v, 1e-9, DT)

    # ---- reference run: period, f0, waveforms, transition windows ---------
    rec = run_record_s(v, 6e-9, DT)
    tc = rising_crossings(rec[:, 0], DT)
    periods = np.diff(tc)[-8:]
    T = float(np.mean(periods))
    f0 = 1.0 / T
    print("T  =", round(T * 1e12, 3), "ps ; period spread (last 8) =",
          "{:.2e}".format(float(np.ptp(periods) * 1e12)), "ps")
    # -> 816.186 ps（spread 1.23e-08 ps：週期已收斂到數值底限）
    print("f0 =", round(f0 / 1e9, 4), "GHz ; tau_D = 1/(2*N*f0) =",
          round(T / (2 * N_STAGES) * 1e12, 2), "ps  ([P2] Eq.(15))")
    # -> 1.2252 GHz（每級延遲 tau_D = 136.03 ps）
    print("node swing: min =", round(float(rec[:, 0].min()), 4),
          "V , max =", round(float(rec[:, 0].max()), 4), "V")
    # -> 0.0038 / 0.9962 V（近 rail-to-rail；q_max = CL*VDD = 10 fC 合理）

    # dt-convergence check: same settled state, half the step
    rec_h = run_record_s(v, 3e-9, 0.5 * DT)
    T_h = float(np.mean(np.diff(rising_crossings(rec_h[:, 0], 0.5 * DT))[-5:]))
    print("f0(dt) vs f0(dt/2) rel. diff =",
          "{:.2e}".format(abs(T - T_h) / T))
    # -> 1.22e-05（dt 已夠小；且參考/擾動共用同一積分器，偏差互相抵銷）

    # ---- ISF extraction (impulse method, 24 phases, >=20 cycles wait) -----
    t0 = float(tc[2])
    thetas, gam, gam_half0 = extract_isf_batch(v, t0, T, DT)
    print("linearity check at theta=0: Gamma(dq) =", round(float(gam[0]), 4),
          "vs Gamma(dq/2) =", round(float(gam_half0), 4))
    # -> 1.1284 vs 1.1295（差 0.1%：Delta q 在線性區，[P1] Fig.6 前提成立）

    print("Gamma(theta) table (theta_deg: value):")
    for row in range(0, N_PHASES, 6):
        print("  " + " ".join(
            f"{np.degrees(thetas[j]):5.0f}:{gam[j]:+7.3f}"
            for j in range(row, row + 6)))
    # -> 0:+1.128, 75:+0.038, 135:-1.155, 180:-1.132, 255:-0.059, 315:+1.173
    #    （雙葉形：正葉繞上升緣、負葉繞下降緣，過零在 75/255 deg）

    # close the period for Fourier / rms helpers
    th_c = np.concatenate([thetas, [2.0 * np.pi]])
    g_c = np.concatenate([gam, [gam[0]]])
    g_rms = float(gamma_rms(th_c, g_c))
    a0, a, b, c, _ = compute_fourier_coefficients(th_c, g_c, N_HARM)
    print("Gamma_rms =", round(g_rms, 4))
    # -> 0.9303（量測值）
    print("[P2] Eq.(16) with eta=1, N=3 -> Gamma_rms =",
          round(float(np.sqrt(2 * np.pi ** 2 / 3.0 / 3 ** 1.5)), 4))
    # -> 1.1253（公式參考值，同數量級；eta 未擬合，單一 N 不驗證 N^-3/4 標度）
    print("c0 =", round(float(a0), 4), "; c1 =", round(float(c[1]), 4),
          "; c2 =", round(float(c[2]), 4), "; c3 =", round(float(c[3]), 4))
    # -> c0=0.0014 接近 0（上升/下降對稱 -> 1/f 上轉弱, [P1] Eq.(23)(24)）;
    #    c1=1.3047, c2=0.0237, c3=0.1633（奇諧波為主 = 奇對稱雙葉）
    print("Parseval: sum c_n^2 =", round(float(np.sum(c ** 2)), 4),
          "vs 2*Gamma_rms^2 =", round(2 * g_rms ** 2, 4))
    # -> 1.7308 vs 1.7309（吻合; [P1] Eq.(20)）

    # lobe peaks relative to the switching edges
    j_pk = int(np.argmax(np.abs(gam)))
    th_pk = float(thetas[j_pk])
    j_mn = int(np.argmin(gam))
    th_mn = float(thetas[j_mn])
    rise_w, fall_w, th_fall = transition_windows(rec, t0, T, DT)
    d_rise = (th_pk + np.pi) % (2 * np.pi) - np.pi          # vs rising edge
    d_fall = (th_mn - th_fall + np.pi) % (2 * np.pi) - np.pi  # vs falling edge
    print("falling edge of node 1 at theta =", round(np.degrees(th_fall), 1),
          "deg")  # -> 180.0 deg（上升/下降各佔半週期：波形對稱）
    print("max|Gamma| =", round(float(np.abs(gam[j_pk])), 4),
          "at theta =", round(np.degrees(th_pk), 1),
          "deg =", round(np.degrees(d_rise), 1), "deg from RISING edge")
    # -> 1.1734 @ theta=315 deg = 上升緣前 45 deg（transition 起步處最敏感）
    print("negative-lobe min =", round(float(gam[j_mn]), 4),
          "at theta =", round(np.degrees(th_mn), 1),
          "deg =", round(np.degrees(d_fall), 1), "deg from FALLING edge")
    # -> -1.1555 @ theta=135 deg = 下降緣前 45 deg（與正葉近鏡像對稱）

    # energy concentration inside the two (10%..90%) transition windows
    mask = (in_window(thetas, *rise_w) | in_window(thetas, *fall_w))
    e_frac = float(np.sum(gam[mask] ** 2) / np.sum(gam ** 2))
    w_frac = float(((rise_w[1] - rise_w[0]) + (fall_w[1] - fall_w[0]))
                   / (2 * np.pi))
    print("ISF energy inside 10-90% transition windows =",
          round(100 * e_frac, 1), "% of total, in",
          round(100 * w_frac, 1), "% of the period")
    # -> 58.7 % 能量集中在 40.7 % 的週期內（N=3 的 transition 本來就寬，
    #    [P2]: N 越大 transition 佔比越小、ISF 越窄）
    print("quietest phases (zero crossings of Gamma): Gamma(75deg) =",
          round(float(gam[5]), 3), "; Gamma(255deg) =",
          round(float(gam[17]), 3))
    # -> +0.038 / -0.059（rail 中段最不敏感；但 N=3 每 T/6 就有一級在切換，
    #    ISF 從不長時間貼 0 -- N 大時 quiet zone 才會變寬、lobe 變窄）
    print("lobe signs: Gamma(rising, theta=0) =", round(float(gam[0]), 3),
          "; Gamma(falling, theta=180deg) =",
          round(float(gam[int(np.argmin(np.abs(thetas - th_fall)))]), 3))
    # -> +1.128 / -1.132（dual-lobe：正電荷在上升緣提前、下降緣延後相位）

    # ------------------------------------------------------------------ fig
    fig, axes = plt.subplots(1, 3, figsize=(14.5, 4.4))

    # (a) three node waveforms over one period
    ax = axes[0]
    i0 = int(round(t0 / DT))
    npts = int(round(T / DT)) + 1
    tt = (np.arange(npts) * DT) * 1e12          # ps from t0
    for j, (color, lab) in enumerate(zip(
            ["tab:blue", "tab:orange", "tab:green"],
            ["節點 1（ISF 萃取節點）", "節點 2", "節點 3"])):
        ax.plot(tt, rec[i0:i0 + npts, j], color=color, label=lab,
                lw=2.0 if j == 0 else 1.3)
    ax.axhline(VTH, color="gray", lw=0.8, ls=":", label=r"$V_{DD}/2$ 門檻")
    ax.set_xlabel(r"$t-t_0$ [ps]（$t_0$ = 節點1上升緣過 $V_{DD}/2$）")
    ax.set_ylabel("節點電壓 [V]")
    ax.set_title(f"(a) Level-1 方程級 3 級 ring 波形（一週期）\n"
                 f"$f_0$={f0/1e9:.3f} GHz, $T$={T*1e12:.1f} ps"
                 "（非 SPICE/BSIM）")
    ax.legend(fontsize=8, loc="center right")

    # (b) extracted ISF with transition windows shaded
    ax = axes[1]
    frac = thetas / (2 * np.pi)
    fr_c = np.concatenate([frac, [1.0]])
    for (lo, hi), col in [(rise_w, "tab:blue"), (fall_w, "tab:red")]:
        lo_f, hi_f = lo / (2 * np.pi), hi / (2 * np.pi)
        if lo_f < 0:
            ax.axvspan(lo_f + 1.0, 1.0, color=col, alpha=0.12)
            ax.axvspan(0.0, hi_f, color=col, alpha=0.12)
        else:
            ax.axvspan(lo_f, hi_f, color=col, alpha=0.12)
    th_d = np.linspace(0, 2 * np.pi, 600)
    ax.plot(th_d / (2 * np.pi), gamma_triangular(th_d, n_stages=N_STAGES),
            "k--", lw=1.0, label="lab_03 toy 三角（手放的，對照用）")
    ax.plot(fr_c, np.concatenate([gam, [gam[0]]]), "-", color="tab:purple",
            lw=1.4)
    ax.plot(frac, gam, "o", ms=5, color="tab:purple",
            label=r"萃取的 $\Gamma(\theta)$（打脈衝法，24 相位）")
    ax.plot(frac[j_pk], gam[j_pk], "*", ms=14, color="tab:red",
            label=fr"max$\vert\Gamma\vert$={np.abs(gam[j_pk]):.2f} @ "
                  fr"$\theta$={np.degrees(th_pk):.0f}°")
    ax.axhline(0, color="gray", lw=0.6)
    ax.set_xlabel(r"注入相位 $\theta/2\pi$（$\theta=0$: 節點1上升緣）")
    ax.set_ylabel(r"$\Gamma(\theta)$ [無因次]")
    ax.set_title(f"(b) 萃取 ISF：能量集中在自身 transition\n"
                 fr"$\Gamma_{{rms}}$={g_rms:.3f}, $c_0$={a0:+.3f}"
                 f"（藍=上升窗, 紅=下降窗, {100*e_frac:.0f}% 能量）")
    ax.legend(fontsize=7.5, loc="upper center")

    # (c) |c_n| stems
    ax = axes[2]
    nn = np.arange(N_HARM + 1)
    ml, sl, bl = ax.stem(nn, c)
    plt.setp(ml, color="tab:purple", ms=6)
    plt.setp(sl, color="tab:purple", lw=1.6)
    plt.setp(bl, color="gray", lw=0.8)
    ax.set_xlabel(r"諧波序 $n$")
    ax.set_ylabel(r"$\vert c_n\vert$")
    ax.set_title("(c) ISF 傅立葉係數（[P1] Eq.(12)）\n"
                 fr"$c_0$={a0:+.3f} 小 → $1/f^3$ 上轉弱（[P1] Eq.(23)(24)）")
    ax.set_xticks(nn)

    savefig(fig, "mos_level1_ring_isf.png")
    print("runtime =", round(time.time() - t_start, 1), "s")


if __name__ == "__main__":
    main()
