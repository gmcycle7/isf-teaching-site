"""
lab_38_supply_pushing_ring.py

Goal
----
Measure supply pushing  K_push = df0/dVDD  of the MOS Level-1
(Shichman-Hodges) 3-stage ring FROM FIRST PRINCIPLES -- nothing fitted,
nothing assumed beyond the device equations already used in lab_32:

  (a) static : sweep VDD = 0.9 .. 1.1 V, measure f0(VDD) by threshold
      crossings  ->  K_push = df0/dVDD at VDD = 1.0 V  [Hz/V]
      (central difference + quadratic-fit cross-check + hand model
       f0 ~ (VDD-VT)^2/VDD  =>  dlnf0/dVDD = 2/(VDD-VT) - 1/VDD).

  (b) dynamic: superimpose a small sinusoidal ripple
          VDD(t) = 1.0 V + V_r sin(2*pi*f_m*t),  V_r = 10 mV, f_m = 100 MHz,
      extract the induced phase modulation phi(t) from threshold-crossing
      times and check the narrowband-FM prediction
          beta = K_push * V_r / f_m          [rad]
      plus the spectral sidebands at f0 +/- f_m with relative level
      20*log10(J1(beta)/J0(beta)) ~ 20*log10(beta/2).  NOTE: this "/2" is
      FM sideband math (Bessel), NOT the SSB-vs-S_phi bookkeeping factor.

Circuit core credited to lab_32_mos_level1_ring.py: identical device law
(_sq_v is imported, not copied) and identical ring topology; the ONLY
generalization is that VDD becomes an explicit argument of the node
equation.  Cross-checked bit-exactly against lab_32's ring_dvdt_v at
VDD = 1.0 V.  MOS Level-1 equation level, NOT SPICE/BSIM/PDK.

Figure
------
  static/figures/supply_pushing_ring.png
    (a) f0 vs VDD with the tangent at 1.0 V (K_push),
    (b) extracted phi(t) at the ripple tone vs the fitted sinusoid,
    (c) spectrum around f0 with the FM sidebands at +/- f_m.

Run
---
    PYTHONPATH=. python simulations/lab_38_supply_pushing_ring.py   (~55 s)
"""
import os
import sys
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.join(_HERE, "common"))

import numpy as np

import lab_32_mos_level1_ring as l32          # device law + ring constants

# ---------------------------------------------------------------------------
# Parameters (device/circuit inherited from lab_32; only VDD is swept here)
# ---------------------------------------------------------------------------
VDD0 = l32.VDD           # nominal supply 1.0 V (operating point for K_push)
CL = l32.CL              # 10 fF per node
N_STAGES = l32.N_STAGES  # 3
DT = 25e-15              # fine step for the static sweep [s] (= lab_32 DT)
DTD = 100e-15            # coarser step for the long dynamic run [s]
VDD_SWEEP = np.linspace(0.9, 1.1, 9)   # static sweep [V], 25 mV grid
V_R = 10e-3              # ripple amplitude [V]
F_M = 100e6              # ripple frequency [Hz]
T_DYN = 150e-9           # dynamic record length [s]
T_DROP = 10e-9           # discarded head of the dynamic record [s]

_IDX = np.array([2, 0, 1])   # == np.roll(..., 1, axis=-1) for 3 stages


def ring_dvdt(v, vdd):
    """lab_32's ring_dvdt_v with VDD promoted to an argument.

    v: node voltages, shape (..., 3);  vdd: scalar or shape (..., 1).
    Device law _sq_v is IMPORTED from lab_32 (credit: lab_32_mos_level1_ring),
    so at vdd = 1.0 this is bit-exact identical to lab_32 (checked in main).
    """
    vin = v[..., _IDX]
    i_n = (l32._sq_v(vin, np.maximum(v, 0.0), l32.BETA_N, l32.VTN)
           - l32._sq_v(vin - v, np.maximum(-v, 0.0), l32.BETA_N, l32.VTN))
    i_p = (l32._sq_v(vdd - vin, np.maximum(vdd - v, 0.0),
                     l32.BETA_P, l32.VTP_ABS)
           - l32._sq_v(v - vin, np.maximum(v - vdd, 0.0),
                       l32.BETA_P, l32.VTP_ABS))
    return (i_p - i_n) / CL


def settle_batch(V, vddcol, t_total, dt):
    """Forward-Euler settle of a batch of rings (no recording)."""
    for _ in range(int(round(t_total / dt))):
        V += dt * ring_dvdt(V, vddcol)
    return V


def record_node1_batch(V, vddcol, t_total, dt):
    """Integrate a batch, recording node-1 voltage of every run."""
    n = int(round(t_total / dt))
    rec = np.empty((n + 1, V.shape[0]), np.float32)
    rec[0] = V[:, 0]
    for k in range(n):
        V += dt * ring_dvdt(V, vddcol)
        rec[k + 1] = V[:, 0]
    return rec, V


def freq_from_record(x, dt, vdd):
    """f0 from the mean of the last 6 rising-crossing periods."""
    tc = l32.rising_crossings(np.asarray(x, np.float64), dt, th=0.5 * vdd)
    T = float(np.mean(np.diff(tc)[-6:]))
    return 1.0 / T


# ---------------------------------------------------------------------------
def main():
    import matplotlib.pyplot as plt
    from plot_utils import savefig

    t_start = time.time()
    print("[lab_38] supply pushing of the MOS Level-1 3-stage ring "
          "(device-equation level, NOT SPICE/BSIM/PDK) ...")

    # ---- consistency: at VDD=1.0 this file's node equation == lab_32's ----
    rng = np.random.default_rng(7)
    vtest = rng.uniform(-0.05, 1.05, (50, 3))
    dmax = float(np.max(np.abs(ring_dvdt(vtest, VDD0)
                               - l32.ring_dvdt_v(vtest))))
    print("cross-check vs lab_32 ring_dvdt_v @ VDD=1.0: max|ddV/dt| =",
          "{:.1e}".format(dmax), "V/s")
    # -> 0.0e+00 V/s（本檔的 VDD 參數化 node equation 與 lab_32 逐位元一致）

    # ================= (a) static sweep: f0(VDD) -> K_push =================
    V = VDD_SWEEP[:, None] * np.array([0.9, 0.1, 0.5])   # staggered start
    vddcol = VDD_SWEEP[:, None].copy()
    V = settle_batch(V, vddcol, 10e-9, 100e-15)          # coarse settle
    V = settle_batch(V, vddcol, 1e-9, DT)                # fine settle
    rec, V = record_node1_batch(V, vddcol, 6e-9, DT)

    f0s = np.array([freq_from_record(rec[:, r], DT, VDD_SWEEP[r])
                    for r in range(len(VDD_SWEEP))])
    print("f0(VDD) table (VDD [V] : f0 [GHz]):")
    for vdd, f in zip(VDD_SWEEP, f0s):
        print(f"  {vdd:5.3f} : {f/1e9:.4f}")
    # -> 0.900:0.9394, 0.950:1.0803, 1.000:1.2252, 1.050:1.3738, 1.100:1.5255
    #    （f0 隨 VDD 單調上升：驅動電流 ~(VDD-VT)^2 長得比 swing ~VDD 快）
    i_op = 4                                             # VDD = 1.000 V
    f0_op = float(f0s[i_op])
    print("f0(1.000 V) =", round(f0_op / 1e9, 4),
          "GHz  (lab_32 reference: 1.2252 GHz)")
    # -> 1.2252 GHz（與 lab_32 同一顆 ring、同 dt：完全再現）

    # K_push three ways: central difference / quadratic fit / hand model
    k_push = float((f0s[i_op + 1] - f0s[i_op - 1])
                   / (VDD_SWEEP[i_op + 1] - VDD_SWEEP[i_op - 1]))
    pq = np.polyfit(VDD_SWEEP, f0s, 2)
    k_quad = float(2.0 * pq[0] * VDD0 + pq[1])
    k_hand = f0_op * (2.0 / (VDD0 - l32.VTN) - 1.0 / VDD0)
    print("K_push (central diff @1.0V) =", round(k_push / 1e9, 4), "GHz/V")
    # -> 2.936 GHz/V（本 lab 的主角數字；+-25 mV 中央差分）
    print("K_push (quadratic fit)      =", round(k_quad / 1e9, 4), "GHz/V")
    # -> 2.9319 GHz/V（9 點二次擬合在 1.0 V 的導數，與中央差分差 0.1%）
    print("hand model f0~(VDD-VT)^2/VDD -> f0*(2/(VDD-VT)-1/VDD) =",
          round(k_hand / 1e9, 4), "GHz/V")
    # -> 2.8588 GHz/V（純手算 RC-delay 模型，差 2.6%：量級與物理都對）
    print("normalized pushing K_push/f0 =", round(k_push / f0_op, 3),
          "1/V =", "{:.2e}".format(k_push / f0_op * 1e6), "ppm/V")
    # -> 2.396 1/V = 2.40e+06 ppm/V（ring 的 f0 由 device 電流直接決定，
    #    比典型 LC VCO 的 pushing 大好幾個數量級）

    # ============ (b) dynamic: 10 mV ripple @ 100 MHz -> FM ================
    # runs: 0 = clean VDD reference, 1 = VDD(t) = 1.0 + V_r*sin(2*pi*f_m*t)
    v2 = np.tile(V[i_op], (2, 1))                        # settled @ 1.0 V
    vdd2 = np.full((2, 1), VDD0)
    v2 = settle_batch(v2, vdd2, 2e-9, DTD)               # re-settle at DTD
    n = int(round(T_DYN / DTD))
    ripple = VDD0 + V_R * np.sin(2.0 * np.pi * F_M * np.arange(n) * DTD)
    rec2 = np.empty((n + 1, 2), np.float32)
    rec2[0] = v2[:, 0]
    for k in range(n):
        vdd2[1, 0] = ripple[k]
        v2 += DTD * ring_dvdt(v2, vdd2)
        rec2[k + 1] = v2[:, 0]

    # reference frequency at DTD (same integrator -> dt bias cancels)
    tc_ref = l32.rising_crossings(rec2[:, 0].astype(np.float64), DTD, th=0.5)
    T0 = float((tc_ref[-1] - tc_ref[0]) / (len(tc_ref) - 1))
    w0 = 2.0 * np.pi / T0
    print("dynamic-run reference: f0 =", round(1.0 / T0 / 1e9, 4),
          "GHz at dt =", DTD * 1e15, "fs")
    # -> 1.2251 GHz（dt=100 fs 的 O(dt) 偏差 ~1e-4；漣波/參考共用同一積分器）

    # excess phase from crossing times: phi_k = 2*pi*k - w0*tc_k  (+ const)
    tc = l32.rising_crossings(rec2[:, 1].astype(np.float64), DTD, th=0.5)
    phi = 2.0 * np.pi * np.arange(len(tc)) - w0 * tc
    m = tc > T_DROP
    tt, ph = tc[m], phi[m]
    wm = 2.0 * np.pi * F_M
    M = np.column_stack([np.ones_like(tt), tt,
                         np.sin(wm * tt), np.cos(wm * tt)])
    coef, *_ = np.linalg.lstsq(M, ph, rcond=None)
    beta_meas = float(np.hypot(coef[2], coef[3]))
    psi_meas = float(np.degrees(np.arctan2(coef[3], coef[2])))
    resid = ph - M @ coef
    beta_pred = k_push * V_R / F_M
    print("beta_pred = K_push*V_r/f_m =", round(beta_pred, 4), "rad ;",
          "beta_meas =", round(beta_meas, 4), "rad")
    # -> 0.2936 rad 預測 vs 0.2942 rad 量測（單位檢查：Hz/V * V / Hz = 無因次 rad）
    print("beta_meas / beta_pred =", round(beta_meas / beta_pred, 3))
    # -> 1.002（窄帶 FM 預測與直接量測吻合到 0.2%：K_push 的動態驗證）
    print("modulation phase =", round(psi_meas, 1),
          "deg (ideal quasi-static FM: -90 deg, i.e. phi ~ -beta*cos)")
    # -> -88.2 deg（phi = 積分(sin) = -cos：相位落在預期象限，偏差 ~2 deg）
    print("fit residual rms =", "{:.2e}".format(float(np.std(resid))), "rad")
    # -> 1.21e-04 rad（殘差比 beta 小三個數量級：單音正弦模型已足夠）

    # spectrum of the rippled run: carrier at f0, sidebands at f0 +/- f_m
    i0 = int(round(T_DROP / DTD))
    x = rec2[i0:, 1].astype(np.float64)
    x -= x.mean()
    win = np.hanning(len(x))
    A = np.abs(np.fft.rfft(x * win))
    fr = np.fft.rfftfreq(len(x), DTD)

    def peak(f_center, half=25e6):
        sel = (fr > f_center - half) & (fr < f_center + half)
        j = np.argmax(A[sel])
        return float(fr[sel][j]), float(A[sel][j])

    f_c, a_c = peak(1.0 / T0)
    f_u, a_u = peak(f_c + F_M)
    f_l, a_l = peak(f_c - F_M)
    usb = 20.0 * np.log10(a_u / a_c)
    lsb = 20.0 * np.log10(a_l / a_c)
    # J1/J0 by series (beta << 1): J0=1-b^2/4+b^4/64, J1=(b/2)(1-b^2/8+...)
    b = beta_meas
    j_ratio = (b / 2.0) * (1 - b * b / 8 + b ** 4 / 192) \
        / (1 - b * b / 4 + b ** 4 / 64)
    sb_pred_nb = 20.0 * np.log10(beta_pred / 2.0)
    sb_pred_j = 20.0 * np.log10(j_ratio)
    print("sideband level: USB =", round(usb, 2), "dBc ; LSB =",
          round(lsb, 2), "dBc")
    # -> -16.31 / -16.83 dBc（頻譜直接量到的 f0+-f_m sideband）
    print("prediction: 20log10(beta_pred/2) =", round(sb_pred_nb, 2),
          "dBc ; 20log10(J1/J0)(beta_meas) =", round(sb_pred_j, 2), "dBc")
    # -> -16.67 dBc 窄帶近似 vs -16.55 dBc Bessel 精確；量測夾在中間。
    #    此 /2 是 FM 數學（J1/J0 ~ beta/2），不是 SSB 記帳的 2 或 4
    print("USB-LSB asymmetry =", round(usb - lsb, 2),
          "dB (concurrent AM: the swing itself tracks VDD, m ~ V_r/VDD)")
    # -> 0.52 dB（VDD 同時調 swing：伴生 AM 使上/下 sideband 不對稱）
    # 2nd-order FM sidebands at f0 +/- 2*f_m: expect 20log10(J2/J0)
    _, a_u2 = peak(f_c + 2.0 * F_M)
    _, a_l2 = peak(f_c - 2.0 * F_M)
    j2_ratio = (b * b / 8.0) * (1 - b * b / 12) \
        / (1 - b * b / 4 + b ** 4 / 64)
    print("2nd-order sidebands: USB2 =",
          round(20.0 * np.log10(a_u2 / a_c), 2), "dBc ; LSB2 =",
          round(20.0 * np.log10(a_l2 / a_c), 2), "dBc ; 20log10(J2/J0) =",
          round(20.0 * np.log10(j2_ratio), 2), "dBc")
    # -> -38.64 / -39.84 dBc vs 理論 -39.19 dBc（f0+-2f_m 的二階 FM sideband
    #    也對上 Bessel J2：beta=0.29 已在窄帶邊緣，高階項開始可見）

    # ---- end-to-end: plug K_push into S_phi = K_push^2 * S_v / df^2 -------
    s_v = 1e-12            # V^2/Hz  (1 uV/rtHz supply noise, as Example H)
    df = 1e6               # Hz offset
    s_phi = k_push ** 2 * s_v / df ** 2
    l_dbc = 10.0 * np.log10(0.5 * s_phi)     # L ~ (1/2) S_phi (SSB smallangle)
    print("end-to-end: S_v = 1e-12 V^2/Hz @ 1 MHz -> S_phi =",
          "{:.3e}".format(s_phi), "rad^2/Hz ; L =", round(l_dbc, 1), "dBc/Hz")
    # -> 8.620e-06 rad^2/Hz ; -53.7 dBc/Hz（L ~ (1/2)S_phi 的 2 是 SSB 小角
    #    慣例[規範第3節公式16]；1 uV/rtHz 髒電源直灌就是這麼災難）
    print("vs Example H (K_push = 2 MHz/V -> -117.0 dBc/Hz): this ring is",
          round(20.0 * np.log10(k_push / 2e6), 1), "dB worse")
    # -> 63.3 dB worse（= 20log10(2.936 GHz / 2 MHz)：全部來自 K_push 平方）

    # ------------------------------------------------------------------ fig
    fig, axes = plt.subplots(1, 3, figsize=(14.5, 4.4))

    # (a) f0 vs VDD + tangent at 1.0 V
    ax = axes[0]
    vv = np.linspace(VDD_SWEEP[0], VDD_SWEEP[-1], 200)
    ax.plot(vv, np.polyval(pq, vv) / 1e9, "-", color="tab:blue", lw=1.2,
            label="二次擬合")
    ax.plot(VDD_SWEEP, f0s / 1e9, "o", color="tab:blue", ms=6,
            label=r"量測 $f_0(V_{DD})$")
    vt = np.linspace(VDD0 - 0.06, VDD0 + 0.06, 2)
    ax.plot(vt, (f0_op + k_push * (vt - VDD0)) / 1e9, "--", color="tab:red",
            lw=1.8, label=fr"切線 $K_{{push}}$={k_push/1e9:.2f} GHz/V")
    ax.plot([VDD0], [f0_op / 1e9], "*", ms=14, color="tab:red")
    ax.set_xlabel(r"$V_{DD}$ [V]")
    ax.set_ylabel(r"$f_0$ [GHz]")
    ax.set_title("(a) 靜態掃描：$f_0(V_{DD})$（Level-1 方程級）\n"
                 fr"$K_{{push}}=\partial f_0/\partial V_{{DD}}"
                 fr"$={k_push/1e9:.2f} GHz/V @ 1.0 V")
    ax.legend(fontsize=8, loc="upper left")

    # (b) extracted phi(t) at the ripple tone vs fit
    ax = axes[1]
    ph_ac = ph - (coef[0] + coef[1] * tt)     # remove offset + drift
    td = np.linspace(tt[0], tt[0] + 3.0 / F_M, 400)   # show 3 ripple cycles
    sel = tt <= td[-1]
    ax.plot(tt[sel] * 1e9, ph_ac[sel], "o", ms=4, color="tab:purple",
            label=r"門檻交越萃取的 $\phi(t_k)$")
    ax.plot(td * 1e9, coef[2] * np.sin(wm * td) + coef[3] * np.cos(wm * td),
            "-", color="tab:purple", lw=1.2, label="正弦擬合")
    for s in (+1.0, -1.0):
        ax.axhline(s * beta_pred, color="tab:red", ls="--", lw=1.0)
    ax.set_ylim(-1.32 * beta_pred, 1.45 * beta_pred)
    ax.text(td[0] * 1e9, beta_pred * 1.08,
            r"$\pm\beta_{pred}=K_{push}V_r/f_m$", color="tab:red",
            fontsize=8.5, va="bottom")
    ax.set_xlabel("t [ns]")
    ax.set_ylabel(r"$\phi(t)$ [rad]（去除直流與漂移）")
    ax.set_title(f"(b) 動態：$V_r$={V_R*1e3:.0f} mV @ "
                 f"$f_m$={F_M/1e6:.0f} MHz 漣波 → 相位調變\n"
                 fr"$\beta$: 量測 {beta_meas:.3f} / 預測 {beta_pred:.3f} rad"
                 fr"（比 {beta_meas/beta_pred:.3f}）")
    ax.legend(fontsize=8, loc="lower right")

    # (c) spectrum around the carrier
    ax = axes[2]
    selw = (fr > f_c - 3.6 * F_M) & (fr < f_c + 3.6 * F_M)
    ax.plot((fr[selw] - f_c) / 1e6, 20.0 * np.log10(A[selw] / a_c),
            "-", color="tab:blue", lw=1.2)
    ax.axhline(sb_pred_nb, color="tab:red", ls="--", lw=1.0,
               label=fr"預測 $20\log_{{10}}(\beta/2)$={sb_pred_nb:.1f} dBc")
    for fx, ax_lvl in ((f_u, usb), (f_l, lsb)):
        ax.annotate(f"{ax_lvl:.1f} dBc",
                    xy=((fx - f_c) / 1e6, ax_lvl),
                    xytext=((fx - f_c) / 1e6 * 2.2, ax_lvl + 9),
                    ha="center", fontsize=9, color="tab:red",
                    arrowprops=dict(arrowstyle="->", color="tab:red"))
    ax.set_ylim(-80, 8)
    ax.set_xlabel(r"$f-f_0$ [MHz]")
    ax.set_ylabel("相對載波 [dBc]")
    ax.set_title("(c) 頻譜：$f_0\\pm f_m$ 的 FM sidebands\n"
                 "（此處的 /2 是 FM 數學 $J_1/J_0\\approx\\beta/2$，"
                 "非 SSB 記帳因子）")
    ax.legend(fontsize=8, loc="lower left")

    savefig(fig, "supply_pushing_ring.png")
    print("runtime =", round(time.time() - t_start, 1), "s")


if __name__ == "__main__":
    main()
