"""
lab_44_adpll_quantization.py

Goal
----
Numerical check of the two quantization-noise formulas of the ADPLL page
(docs/06_design_insights/adpll_tdc_dco.md) and of its noise budget.

(1) TDC  - time-domain simulation of a uniform quantizer of resolution
           dt_res acting on the reference-to-CKV time difference, one sample
           per reference period (rate f_R).  PSD of the quantization phase
           error vs
               L_TDC = (2 pi)^2/12 * (dt_res/T_V)^2 / f_R        [1/Hz]
           Three inputs:
             T1  fractional-N ramp + random input jitter of rms dt_res/2
                 ("busy" input)                      -> white, ratio ~ 1
             T2  noiseless fractional-N ramp          -> the SAME total power,
                 but it sits in discrete lines (fractional spurs), not white
             T3  integer-N, static offset, jitter << dt_res
                                                      -> the TDC code never
                 moves (dead zone): no quantization "noise" at all
(2) DCO  - an m-th-order Delta-Sigma modulator running at f_dth toggles a
           PHYSICAL unit cell whose frequency step is df_u.  The frequency
           error (modulator output minus its input) is integrated to phase.
           PSD vs
               L = (1/12)(df_u/df)^2 (1/f_dth) [2 sin(pi df/f_dth)]^(2m)
                   * sinc^2(df/f_dth)                              [1/Hz]
           Cases:
             D1  m = 1, busy input (white-error model exact) -> ratio ~ 1
             D2  m = 2 (MASH 1-1), static input             -> ratio ~ 1
             D3  m = 1, static input, no dither -> idle TONES (line spectrum)
             D4  m = 1, static input + 1-LSB in-loop dither -> white, but x2
(3) Budget - S_out = (S_ref N^2 + S_TDC)|H_lp|^2 + (S_DCO + S_vco)|H_hp|^2
           with the page's type-II loop and the site-canonical LC-DCO thermal
           skirt (L(1 MHz) = -148.0 dBc/Hz, [P1] Eq.(21) '/4' family),
           integrated 1 kHz - 1 GHz, vs the analog charge-pump PLL
           (S_cp = 5e-13 rad^2/Hz).

Conventions
-----------
L is the SSB number (= two-sided density of phi); the site's ONE-SIDED
S_phi = 2 L.  scipy.signal.welch returns a one-sided density, so the
simulated curves are divided by 2 before being compared with L.

Limitations (honest)
--------------------
Open-loop, phase-domain toy: an ideal uniform quantizer (no DNL/INL, no
metastability), an ideal unit cell (no mismatch, no switching kickback, no
dither-clock jitter), the sampled phase (aliasing above ~ f_s/4 is not
modelled by the continuous formula).  The budget panel is the analytic
formula, not a closed-loop time-domain run, and has no far-out buffer floor.
Runtime ~ 10 s.  Fixed seeds.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch

from plot_utils import savefig
from pll_utils import H_lowpass_mag2, H_highpass_mag2

# ----------------------------------------------------------------- constants
F0 = 5e9                 # DCO output frequency [Hz]
T_V = 1 / F0             # output period [s]
F_R = 50e6               # reference [Hz]
N_DIV = 100
DT_RES = 10e-12          # TDC resolution [s]
F_DTH = F0 / 8           # dither clock [Hz]
C_TANK = 1e-12           # tank capacitance [F]
GOLDEN = (3 - np.sqrt(5)) / 2          # 0.381966..., "most irrational" fraction


def db(x):
    return 10 * np.log10(x)


# ------------------------------------------------------------------- theory
def L_tdc(dt_res, f_r=F_R):
    return (2 * np.pi) ** 2 / 12 * (dt_res / T_V) ** 2 / f_r


def L_dco_dsm(df_u, df, m, f_dth=F_DTH):
    df = np.asarray(df, dtype=float)
    return ((1 / 12) * (df_u / df) ** 2 / f_dth
            * (2 * np.sin(np.pi * df / f_dth)) ** (2 * m) * np.sinc(df / f_dth) ** 2)


def L_lc_thermal(df):
    """Site canonical LC value, [P1] Eq.(21) '/4' family: -148.0 dBc/Hz at 1 MHz."""
    grms2, qmax, s_i = 0.25, 1e-12, 1e-24
    return grms2 / qmax ** 2 * s_i / (4 * (2 * np.pi * np.asarray(df, dtype=float)) ** 2)


def band_mean(f, p, lo, hi):
    k = (f >= lo) & (f <= hi)
    return float(np.mean(p[k]))


# --------------------------------------------------------------- (1) TDC
def tdc_experiment():
    n = 2 ** 20
    k = np.arange(n)
    rng = np.random.default_rng(44)
    theory = L_tdc(DT_RES)
    sig_uniform = DT_RES / np.sqrt(12)
    out = {}

    def quantize(dt):
        """Uniform mid-tread TDC: returns the time error e_t = Q(dt) - dt [s]."""
        return np.round(dt / DT_RES) * DT_RES - dt

    # T1: fractional-N ramp (irrational fraction) + input jitter rms dt_res/2
    dt1 = (k * GOLDEN % 1.0) * T_V + rng.normal(0, 0.5 * DT_RES, n)
    e1 = quantize(dt1)
    phi1 = 2 * np.pi * e1 / T_V
    f1, p1 = welch(phi1, fs=F_R, nperseg=2 ** 13)
    l1 = band_mean(f1, p1, 1e5, 2e7) / 2            # one-sided -> SSB number
    out["T1"] = dict(f=f1, L=p1 / 2, L_band=l1, ratio=l1 / theory,
                     rms_ratio=np.std(e1) / sig_uniform)

    # T2: noiseless fractional-N ramp, fraction 6257/16384 (exactly periodic,
    # so every line falls on an FFT bin)
    alpha2 = 6257 / 16384
    dt2 = (k * alpha2 % 1.0) * T_V
    e2 = quantize(dt2)
    phi2 = 2 * np.pi * e2 / T_V
    f2, p2 = welch(phi2, fs=F_R, nperseg=2 ** 13)
    spec = np.abs(np.fft.rfft(phi2 - phi2.mean())) ** 2
    spec[1:-1] *= 2
    frac_top10 = float(np.sort(spec)[-10:].sum() / spec.sum())
    amp = np.sqrt(2 * spec.max()) / n                    # peak phase of strongest line [rad]
    spur_dbc = 20 * np.log10(amp / 2)
    spur_f = np.fft.rfftfreq(n, 1 / F_R)[int(np.argmax(spec))]
    amp_th = 2 * np.pi * (DT_RES / np.pi) / T_V           # sawtooth fundamental
    out["T2"] = dict(f=f2, L=p2 / 2, rms_ratio=np.std(e2) / sig_uniform,
                     frac_top10=frac_top10, spur_dbc=spur_dbc, spur_f=spur_f,
                     spur_dbc_th=20 * np.log10(amp_th / 2))

    # T3: integer-N, static offset in the middle of a bin, jitter << dt_res
    dt3 = 0.3 * DT_RES + rng.normal(0, 0.02 * DT_RES, n)
    code3 = np.round(dt3 / DT_RES)
    out["T3"] = dict(codes=int(np.unique(code3).size), code_std=float(np.std(code3)))
    out["theory"] = theory
    return out


# --------------------------------------------------------------- (2) DCO
def dsm_errors(n, rng):
    """Return the dimensionless (unit-cell LSB) error sequences v - x of the
    Delta-Sigma modulators.  Accumulator (carry) form: r = residue in [0,1)."""
    seqs = {}
    # D1: m = 1, busy input: x iid uniform over one LSB -> residue iid uniform
    x = rng.random(n)
    r = np.cumsum(x) % 1.0
    seqs["D1"] = -(np.diff(r, prepend=0.0))               # v - x = -(1 - z^-1) r
    # D2: m = 2, MASH 1-1, static irrational input
    r1 = (np.arange(1, n + 1) * GOLDEN) % 1.0
    r2 = np.cumsum(r1) % 1.0
    d1 = np.diff(r2, prepend=0.0)
    seqs["D2"] = -(np.diff(d1, prepend=0.0))              # -(1 - z^-1)^2 r2
    # D3: m = 1, static input 1565/4096 (exactly periodic -> lines on FFT bins)
    r = (np.arange(1, n + 1) * (1565 / 4096)) % 1.0
    seqs["D3"] = -(np.diff(r, prepend=0.0))
    # D4: m = 1, static input, non-subtractive 1-LSB uniform dither at the
    # quantizer (error feedback).  p = frac(u) rotates deterministically; the
    # dithered quantizer rounds up with probability p.
    p = (np.arange(n) * GOLDEN + 0.123) % 1.0
    eps = np.where(rng.random(n) < p, 1.0 - p, -p)        # total error at quantizer
    seqs["D4"] = np.diff(eps, prepend=0.0)                # v - x = (1 - z^-1) eps
    return seqs


def dco_experiment():
    n = 2 ** 22
    rng = np.random.default_rng(4401)
    seqs = dsm_errors(n, rng)
    out = {}
    for df_u, tag in ((2.5e6, "1fF"), (1e5, "40aF")):
        res = {}
        for name, m in (("D1", 1), ("D2", 2), ("D4", 1)):
            # frequency error [Hz] held for T_dth, integrated to phase [rad]
            phi = 2 * np.pi / F_DTH * df_u * np.cumsum(seqs[name])
            f, p = welch(phi, fs=F_DTH, nperseg=2 ** 15)
            band = (f >= 0.5e6) & (f <= 2e6)
            th = L_dco_dsm(df_u, f[band], m)
            ratio = float(np.mean(p[band] / 2 / th))
            l_1m = ratio * float(L_dco_dsm(df_u, 1e6, m))
            res[name] = dict(f=f, L=p / 2, ratio=ratio, L_1M=l_1m, m=m)
        # D3: idle tones
        phi = 2 * np.pi / F_DTH * df_u * np.cumsum(seqs["D3"])
        f3, p3 = welch(phi, fs=F_DTH, nperseg=2 ** 15)
        spec = np.abs(np.fft.rfft(phi - phi.mean())) ** 2
        spec[1:-1] *= 2
        kmax = int(np.argmax(spec))
        amp = np.sqrt(2 * spec[kmax]) / n                    # peak phase of strongest tone [rad]
        res["D3"] = dict(f=f3, L=p3 / 2,
                         frac_top10=float(np.sort(spec)[-10:].sum() / spec.sum()),
                         spur_dbc=20 * np.log10(amp / 2),
                         spur_f=np.fft.rfftfreq(n, 1 / F_DTH)[kmax],
                         spur_dbc_th=20 * np.log10((2 * df_u / F_DTH) / 2),
                         var_ratio=float(np.var(phi) / ((2 * np.pi * df_u / F_DTH) ** 2 / 12)))
        out[tag] = res
    return out


# --------------------------------------------------------------- (3) budget
def budget_experiment():
    f = np.logspace(3, 9, 4000)
    s_ref = 1e-16 + 1e-18 * (1e6 / f)            # same reference as pll_noise_budget
    s_vco = 2 * L_lc_thermal(f)                  # one-sided, LC-DCO thermal skirt
    s_cp = 5e-13
    fns = np.logspace(3, 7.5, 181)

    def sigma_t(s):
        return np.sqrt(np.trapezoid(s, f)) / (2 * np.pi * F0)

    def best(s_inband, s_dco):
        jit = [sigma_t(s_inband * H_lowpass_mag2(f, x) + (s_dco + s_vco) * H_highpass_mag2(f, x))
               for x in fns]
        j = int(np.argmin(jit))
        return fns[j], jit[j]

    zero = np.zeros_like(f)
    dco_cases = [
        ("無量化（理想 DCO）", zero),
        ("40 aF、m=1、f0/8", 2 * L_dco_dsm(1e5, f, 1)),
        ("1 fF、m=1、f0/8", 2 * L_dco_dsm(2.5e6, f, 1)),
        ("1 fF、m=2、f0/8", 2 * L_dco_dsm(2.5e6, f, 2)),
        ("1 fF、m=2、f0/2", 2 * L_dco_dsm(2.5e6, f, 2, F0 / 2)),
        ("1 fF、m=1、f0/2", 2 * L_dco_dsm(2.5e6, f, 1, F0 / 2)),
        ("40 aF、m=2、f0/8", 2 * L_dco_dsm(1e5, f, 2)),
    ]
    rows = []
    fn_a, j_a = best(s_ref * N_DIV ** 2 + s_cp, zero)
    rows.append(("analog", None, "-", fn_a, j_a))
    for dt in (10e-12, 1e-12):
        s_tdc = 2 * L_tdc(dt)
        for name, s_dco in dco_cases:
            fn, j = best(s_ref * N_DIV ** 2 + s_tdc, s_dco)
            rows.append(("adpll", dt, name, fn, j))
    # quantization-only integrated jitter (|H_hp| ~ 1 over almost all the band)
    q_only = [(name, sigma_t(s)) for name, s in dco_cases[1:]]
    return dict(f=f, s_ref=s_ref, s_vco=s_vco, s_cp=s_cp, rows=rows,
                dco_cases=dco_cases, q_only=q_only)


# -------------------------------------------------------------------- plot
def make_figure(tdc, dco, bud):
    fig, ax = plt.subplots(1, 3, figsize=(16.5, 5.0))

    a = ax[0]
    k = tdc["T2"]["f"] > 0
    a.semilogx(tdc["T2"]["f"][k] / 1e6, db(tdc["T2"]["L"][k] + 1e-30), color="0.6", lw=0.8,
               label="T2 無雜訊分數斜坡：功率集中在離散線（spur）")
    k = tdc["T1"]["f"] > 0
    a.semilogx(tdc["T1"]["f"][k] / 1e6, db(tdc["T1"]["L"][k]), color="C0",
               label="T1 分數斜坡＋輸入 jitter（rms = Δt_res/2）")
    a.axhline(db(tdc["theory"]), color="k", ls="--",
              label=f"公式 L_TDC = {db(tdc['theory']):.1f} dBc/Hz")
    a.set_xlabel("offset 頻率 f [MHz]（取樣率 f_R = 50 MHz）")
    a.set_ylabel("TDC 量化相位雜訊 [dBc/Hz]")
    a.set_title("(a) TDC 量化：Δt_res = 10 ps，白噪假設何時成立")
    a.set_ylim(-140, -40)
    a.legend(loc="upper left", fontsize=8)

    a = ax[1]
    fth = np.logspace(5, np.log10(2.5e8), 400)
    for tag, col in (("1fF", "C3"), ("40aF", "C0")):
        df_u = 2.5e6 if tag == "1fF" else 1e5
        lab = "1 fF（2.5 MHz）" if tag == "1fF" else "40 aF（100 kHz）"
        for name, ls in (("D1", "-"), ("D2", "-")):
            d = dco[tag][name]
            kk = (d["f"] > 1e5) & (d["f"] < 2.5e8)
            a.semilogx(d["f"][kk] / 1e6, db(d["L"][kk]), color=col, lw=0.9,
                       alpha=0.55 if name == "D2" else 0.9,
                       label=f"模擬 {lab}、m = {d['m']}")
            a.semilogx(fth / 1e6, db(L_dco_dsm(df_u, fth, d["m"])), "k:", lw=1.2)
    a.semilogx(fth / 1e6, db(L_lc_thermal(fth)), color="C2", lw=2.2,
               label="LC-DCO 熱雜訊 −148 @ 1 MHz（/4 族）")
    a.plot([], [], "k:", label="公式（以 unit cell 步距 Δf_u 代入）")
    a.set_xlabel("offset 頻率 Δf [MHz]（f_dth = f0/8 = 625 MHz）")
    a.set_ylabel("ΔΣ 整形後 DCO 量化相位雜訊 [dBc/Hz]")
    a.set_title("(b) DCO dither：步距是 unit cell，不是平均後的解析度")
    a.set_ylim(-215, -110)
    a.legend(loc="lower right", fontsize=7.5)

    a = ax[2]
    f = bud["f"]
    fn = [r[3] for r in bud["rows"] if r[1] == 1e-12 and r[2].startswith("40 aF")][0]
    lp, hp = H_lowpass_mag2(f, fn), H_highpass_mag2(f, fn)
    s_tdc = 2 * L_tdc(1e-12)
    parts = [
        ("reference × N²", bud["s_ref"] * N_DIV ** 2 * lp, "C1"),
        ("TDC 1 ps", s_tdc * lp, "C4"),
        ("DCO 熱雜訊（ISF）", bud["s_vco"] * hp, "C2"),
        ("DCO 量化：40 aF、m=1", bud["dco_cases"][1][1] * hp, "C0"),
        ("DCO 量化：1 fF、m=1", bud["dco_cases"][2][1] * hp, "C3"),
    ]
    tot = np.zeros_like(f)
    for lab, s, col in parts:
        a.semilogx(f / 1e6, db(s / 2 + 1e-40), color=col, lw=1.3, label=lab)
        if "1 fF" not in lab:
            tot = tot + s
    a.semilogx(f / 1e6, db(tot / 2), "k", lw=2.2, label="合計（40 aF 版）")
    a.axhline(db(0.5 * (1e-12 + bud["s_cp"])), color="0.5", ls="--",
              label="類比 in-band 地板 −121.2")
    a.set_xlabel("offset 頻率 f [MHz]")
    a.set_ylabel("閉迴路輸出相位雜訊 [dBc/Hz]")
    a.set_title(f"(c) LC-DCO ADPLL 預算（最佳 f_n = {fn / 1e3:.0f} kHz、ζ = 0.707）")
    a.set_ylim(-200, -100)
    a.set_xlim(1e-3, 1e3)
    a.legend(loc="upper right", fontsize=7.5)

    savefig(fig, "adpll_quantization.png")


# -------------------------------------------------------------------- main
def main():
    print("=== (1) TDC quantization, dt_res = 10 ps, f_R = 50 MHz ===")
    tdc = tdc_experiment()
    print(f"theory L_TDC = {tdc['theory']:.4e} ({db(tdc['theory']):.2f} dBc/Hz)")
    t1 = tdc["T1"]
    print(f"T1 busy input : measured {db(t1['L_band']):.2f} dBc/Hz, measured/theory = {t1['ratio']:.3f}, "
          f"rms(e_t)/(dt_res/sqrt12) = {t1['rms_ratio']:.3f}")
    t2 = tdc["T2"]
    print(f"T2 noiseless ramp: rms ratio = {t2['rms_ratio']:.3f}, power in the 10 strongest lines = "
          f"{100 * t2['frac_top10']:.1f} %, strongest spur {t2['spur_dbc']:.1f} dBc at "
          f"{t2['spur_f'] / 1e6:.2f} MHz (sawtooth theory {t2['spur_dbc_th']:.1f} dBc)")
    t3 = tdc["T3"]
    print(f"T3 integer-N static offset, jitter 0.02 LSB: distinct TDC codes = {t3['codes']}, "
          f"code std = {t3['code_std']:.3f} LSB (dead zone)")

    print("=== (2) DCO Delta-Sigma dither, f_dth = f0/8 = 625 MHz, at 1 MHz ===")
    dco = dco_experiment()
    for tag, df_u in (("40aF", 1e5), ("1fF", 2.5e6)):
        for name, m in (("D1", 1), ("D2", 2), ("D4", 1)):
            d = dco[tag][name]
            th = float(L_dco_dsm(df_u, 1e6, m))
            print(f"{tag:>5} {name} m={m}: theory {db(th):.2f}, measured {db(d['L_1M']):.2f} dBc/Hz, "
                  f"measured/theory = {d['ratio']:.3f}")
        d = dco[tag]["D3"]
        print(f"{tag:>5} D3 m=1 static input: phase-variance ratio = {d['var_ratio']:.3f}, "
              f"power in 10 strongest lines = {100 * d['frac_top10']:.1f} %, strongest idle tone "
              f"{d['spur_dbc']:.1f} dBc at {d['spur_f'] / 1e6:.2f} MHz (theory {d['spur_dbc_th']:.1f} dBc)")
    lth = float(L_lc_thermal(1e6))
    print(f"LC-DCO thermal ('/4' family) at 1 MHz = {db(lth):.2f} dBc/Hz "
          f"('/2' family {db(2 * lth):.2f})")

    print("=== (3) budget: optimum f_n and integrated jitter (1 kHz - 1 GHz) ===")
    bud = budget_experiment()
    for kind, dt, name, fn, j in bud["rows"]:
        if kind == "analog":
            print(f"analog CP-PLL + LC          : f_n* = {fn / 1e6:.3f} MHz, sigma_t = {j * 1e15:.1f} fs")
        else:
            print(f"ADPLL {dt * 1e12:>4.0f} ps, {name:<16}: f_n* = {fn / 1e6:.3f} MHz, "
                  f"sigma_t = {j * 1e15:.1f} fs")
    for name, j in bud["q_only"]:
        print(f"DCO quantization alone, {name:<16}: {j * 1e15:.1f} fs")

    make_figure(tdc, dco, bud)
    return tdc, dco, bud


if __name__ == "__main__":
    main()
