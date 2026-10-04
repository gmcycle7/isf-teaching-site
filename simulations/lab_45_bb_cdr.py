"""
lab_45_bb_cdr.py

Goal
----
Monte-Carlo / time-domain check of the bang-bang CDR page
(docs/06_design_insights/cdr_bang_bang_jtol.md):

  (a) the Alexander 3-sample decision (D_{k-1}, E_k, D_k) drawn as a timing
      diagram for an EARLY and a LATE clock;
  (b) the phase-detector characteristic E[e] versus a static offset Dt under
      Gaussian edge jitter sigma_j = 447.9 fs, obtained by running the literal
      Alexander truth table on random NRZ data: slope on transitions vs
      K_bb = sqrt(2/pi)/sigma_j, slope over all bits vs rho_T*K_bb;
  (c) the first-order bang-bang loop phi[k+1] = phi[k] + K_p*e[k]:
      noise-free limit cycle (2D+1)*K_p for latency D, and the rms "hunting"
      jitter with input jitter present vs the linearised sqrt(K_p/(2 K_bb));
  (d) sinusoidal-jitter tolerance (largest peak-to-peak amplitude for which the
      tracking error stays inside the eye margin) versus jitter frequency for
      the proportional-only loop and for the proportional+integral loop,
      compared with the slew line, the acceleration line and the linear
      type-II template of the page;
  (e) a PCIe-style SSC profile (-0.5 %, 30 kHz triangle): proportional-only
      loses lock, proportional+integral tracks.

Model (behavioural, phase domain; NOT transistor level)
-------------------------------------------------------
  * 25 Gb/s NRZ, UI = 40 ps, 6-bit phase interpolator: K_p = UI/64 = 0.625 ps.
  * The loop is updated every N_dec = 16 UI (f_u = 1.5625 GHz).  As on the page
    ("one sign per update, no voting") ONE Alexander decision is used per
    update: e = sign(Dt + n) if that bit pair has a transition (probability
    rho_T = 0.5), else 0;  n ~ N(0, sigma_j^2) is white from update to update.
    A majority-vote variant (vote over the N_dec decisions) is run at one
    frequency to show the slew ceiling without the rho_T factor.
  * Sign convention of the page: Dt = t_data_edge - t_clock_edge, positive when
    the clock is EARLY; the loop moves the clock later by K_p when e = +1:
        phi[k+1]   = phi[k] + K_p*e[k] + omega[k]
        omega[k+1] = omega[k] + K_i*e[k]          (K_i = 0: proportional only)
  * The decision uses the error wrapped into (-UI/2, UI/2] (a real PD cannot
    tell a whole-UI slip); the pass/fail criterion uses the unwrapped error:
        max |Dt_deterministic| <= (UI - TJ_eye)/2,   TJ_eye = 2*7.03*sigma_j.
  * No loop latency in (d)/(e) (D = 0), ideal PI (no INL), no ISI, the random
    jitter is only white Gaussian.

Run:  PYTHONPATH=<site root> python3 simulations/lab_45_bb_cdr.py
"""
import time

import numpy as np
from scipy.special import erf, erfinv, ndtr

from simulations.common.plot_utils import plt, savefig
from simulations.common.pll_utils import H_highpass_mag2

# ----------------------------------------------------------------------------
# Site / page numbers
# ----------------------------------------------------------------------------
FB = 25e9                 # bit rate [b/s]
UI = 40e-12               # [s]
SIGMA_J = 447.9e-15       # rms jitter between data edge and clock [s]
B_PI = 6
KP = UI / 2**B_PI         # 0.625 ps
N_DEC = 16
FU = FB / N_DEC           # 1.5625 GHz update rate
RHO_T = 0.5
K_BB = np.sqrt(2/np.pi) / SIGMA_J
QINV = 7.03
MARGIN_UI = 1 - 2*QINV*SIGMA_J/UI          # 0.843 UI (peak-to-peak eye margin)
KI = KP / 1024            # integral-path step per update [s per update^2]
SIG_UI = SIGMA_J / UI
KP_UI = KP / UI
KI_UI = KI / UI


# ----------------------------------------------------------------------------
# (b) literal Alexander truth table on random NRZ data
# ----------------------------------------------------------------------------
def alexander_mc(dt, n_bits, rng):
    """Mean PD output for a static offset dt [s] (clock early positive).

    Bit k-1 ends / bit k starts at the edge k*UI + j_k (j_k = Gaussian jitter).
    The edge sampler fires at k*UI - dt.  It still sees the OLD bit b[k-1] when
    it fires before the edge (dt + j_k > 0), otherwise the NEW bit b[k].
    Truth table: no transition -> 0;  E == D_{k-1} -> +1 (early);
                 E == D_k     -> -1 (late).
    Returns (mean over all bits, mean over transitions only, transition density).
    """
    bits = rng.integers(0, 2, n_bits + 1, dtype=np.int8)
    d_prev, d_now = bits[:-1], bits[1:]
    j = rng.standard_normal(n_bits) * SIGMA_J
    edge = np.where(dt + j > 0, d_prev, d_now)
    trans = d_prev != d_now
    e = np.where(trans, np.where(edge == d_prev, 1, -1), 0)
    return e.mean(), e[trans].mean(), trans.mean()


# ----------------------------------------------------------------------------
# (c) first-order loop: noise-free limit cycle and noisy hunting
# ----------------------------------------------------------------------------
def limit_cycle(D, n=400):
    """Noise-free first-order BB loop with latency D updates; phase in K_p."""
    phi, q, hist = 0.3, [0.0]*D, []
    for _ in range(n):
        q.append(-np.sign(phi) if phi != 0 else 1.0)
        phi += q.pop(0)
        hist.append(phi)
    return np.array(hist)


def hunting_noisy(n, rng):
    """First-order loop locked to a jittery (sigma_j) but otherwise static edge.

    Returns the clock-phase sequence [s] (deviation from the mean data edge).
    """
    noise = (rng.standard_normal(n) * SIGMA_J).tolist()
    trans = (rng.random(n) < RHO_T).tolist()
    phi, out = 0.0, [0.0]*n
    for k in range(n):
        if trans[k]:
            phi += KP if (noise[k] - phi) > 0 else -KP
        out[k] = phi
    return np.array(out)


# ----------------------------------------------------------------------------
# (d)/(e) vectorised bang-bang loop (all phases in UI, one column per config)
# ----------------------------------------------------------------------------
def bb_loop(x_fn, n_steps, n_cfg, ki_ui, rng, eval_from, vote=1, trace=False):
    """Run the BB loop for n_cfg parallel configurations.

    x_fn(k) -> input (data-edge) phase [UI] at update indices k (1-D int array),
               shape (len(k), n_cfg).
    ki_ui   -> scalar or (n_cfg,) integral step [UI per update^2].
    vote    -> 1: one Alexander decision per update (page model);
               N>1: majority vote over N decisions (transitions ~ Binomial(N, rho_T)).
    Returns max |x - phi| [UI] over k >= eval_from (and the error trace if asked).
    """
    phi = np.zeros(n_cfg)
    om = np.zeros(n_cfg)
    worst = np.zeros(n_cfg)
    tr = np.empty((n_steps, n_cfg)) if trace else None
    chunk = 8192
    for k0 in range(0, n_steps, chunk):
        k1 = min(k0 + chunk, n_steps)
        x = x_fn(np.arange(k0, k1))
        m = k1 - k0
        if vote == 1:
            noise = rng.standard_normal((m, 1)) * SIG_UI
            tmask = (rng.random((m, 1)) < RHO_T).astype(float)
        else:
            n_tr = rng.binomial(vote, RHO_T, size=(m, 1))
        for i in range(m):
            err = x[i] - phi
            if trace:
                tr[k0 + i] = err
            if k0 + i >= eval_from:
                np.maximum(worst, np.abs(err), out=worst)
            errw = err - np.rint(err)                 # PD only sees the error mod UI
            if vote == 1:
                e = np.sign(errw + noise[i]) * tmask[i]
            else:
                n_plus = rng.binomial(n_tr[i], ndtr(errw / SIG_UI))
                e = np.sign(2*n_plus - n_tr[i])
            phi += KP_UI*e + om
            om += ki_ui*e
    return (worst, tr) if trace else worst


def sj_tolerance(f, ki_ui, pred_pp, rng, vote=1, n_amp=96, span=0.6):
    """Largest sinusoidal-jitter amplitude [UI pp] with max|error| <= margin/2."""
    amps = pred_pp * np.logspace(-span, span, n_amp)
    per = FU / f                                     # updates per jitter period
    n_ramp = int(max(per, 6000))
    n_steps = int(max(3*per, 30000))
    w = 2*np.pi*f/FU

    def x_fn(k):
        env = np.where(k < n_ramp, 0.5*(1 - np.cos(np.pi*k/n_ramp)), 1.0)
        return (env*np.sin(w*k))[:, None] * (amps/2)[None, :]

    worst = bb_loop(x_fn, n_steps, n_amp, ki_ui, rng, eval_from=n_ramp, vote=vote)
    ok = worst <= MARGIN_UI/2
    if not ok[0]:
        return np.nan
    first_fail = np.argmin(ok) if not ok.all() else n_amp
    return amps[first_fail - 1]


def ssc_phase(k, delta=0.005, fm=30e3):
    """Data-edge phase [UI] for a down-spread triangular SSC (0 -> -delta -> 0)."""
    t = k / FU
    tm = 1/fm
    tau = np.mod(t, tm)
    n_per = np.floor(t/tm)
    a = delta*FB/(tm/2)                              # UI/s^2
    # frequency offset (data slower -> edges later -> phase grows): triangle 0..delta*FB
    up = tau < tm/2
    ph_up = 0.5*a*tau**2
    tau2 = tau - tm/2
    ph_dn = 0.5*a*(tm/2)**2 + delta*FB*tau2 - 0.5*a*tau2**2
    per_tot = delta*FB*tm/2                          # phase gained per modulation period
    return n_per*per_tot + np.where(up, ph_up, ph_dn)


# ----------------------------------------------------------------------------
def main():
    t0 = time.time()
    rng = np.random.default_rng(45)

    print("=== lab_45: bang-bang CDR ===")
    print(f"K_p = {KP*1e12:.3f} ps, f_u = {FU/1e9:.4f} GHz, sigma_j = {SIGMA_J*1e15:.1f} fs, "
          f"K_bb = {K_BB:.3e} 1/s, margin = {MARGIN_UI:.3f} UI")

    # ---------------- (b) PD characteristic -------------------------------
    dts = np.linspace(-3, 3, 25) * SIGMA_J
    pd_all = np.array([alexander_mc(d, 400_000, rng)[0] for d in dts])
    d0 = 0.1*SIGMA_J
    n_sl = 8_000_000
    ap, tp, rho_p = alexander_mc(+d0, n_sl, rng)
    am, tm_, rho_m = alexander_mc(-d0, n_sl, rng)
    slope_trans = (tp - tm_)/(2*d0)
    slope_all = (ap - am)/(2*d0)
    rho_meas = 0.5*(rho_p + rho_m)
    print(f"(b) PD slope on transitions = {slope_trans:.3e} 1/s, / K_bb = {slope_trans/K_BB:.3f}")
    print(f"    PD slope over all bits  = {slope_all:.3e} 1/s, / (rho_T K_bb) = "
          f"{slope_all/(RHO_T*K_BB):.3f}, transition density = {rho_meas:.3f}")
    e1 = alexander_mc(SIGMA_J, 2_000_000, rng)[1]
    print(f"    <e>(+sigma_j) on transitions = {e1:.3f} (erf(1/sqrt2) = {erf(1/np.sqrt(2)):.3f})")

    # ---------------- (c) hunting ------------------------------------------
    pp = [float(np.ptp(limit_cycle(D)[200:])) for D in (0, 1, 2)]
    print(f"(c) noise-free limit cycle pp / K_p for D = 0, 1, 2: {pp}  (theory 2D+1)")
    phi_h = hunting_noisy(1_500_000, rng)[5000:]
    s_h = phi_h.std()
    s_lin = np.sqrt(KP/(2*K_BB))
    g_lin = KP*K_BB*RHO_T
    g_eff = KP**2*RHO_T/(2*s_h**2)
    print(f"    noisy hunting rms = {s_h*1e15:.1f} fs; linearised sqrt(K_p/2K_bb) = {s_lin*1e15:.1f} fs; "
          f"ratio = {s_h/s_lin:.3f}")
    print(f"    effective gain/update = {g_eff:.3f} (linear {g_lin:.3f}); "
          f"effective f_BW = {g_eff*FU/(2*np.pi)/1e6:.1f} MHz (linear {g_lin*FU/(2*np.pi)/1e6:.1f} MHz)")
    print(f"    hunting pp (99.9 % span) = {(np.quantile(phi_h, 0.9995)-np.quantile(phi_h, 0.0005))*1e12:.2f} ps")

    # ---------------- (d) sinusoidal-jitter tolerance ----------------------
    slew = RHO_T*KP_UI*FU                 # UI/s, one decision per update
    slew_vote = KP_UI*FU                  # UI/s, every update carries a decision
    acc = RHO_T*KI_UI*FU**2               # UI/s^2
    freqs = 1e4 * 10**(np.arange(0, 13)/3.0)
    line_slew = slew/(np.pi*freqs)
    line_slew_vote = slew_vote/(np.pi*freqs)
    line_acc = acc/(2*np.pi**2*freqs**2)
    jt_p, jt_pi = [], []
    for f, ls, la in zip(freqs, line_slew, line_acc):
        jt_p.append(sj_tolerance(f, 0.0, ls + MARGIN_UI, rng))
        jt_pi.append(sj_tolerance(f, KI_UI, max(ls, la) + MARGIN_UI, rng))
    jt_p, jt_pi = np.array(jt_p), np.array(jt_pi)
    print("(d) f [Hz]   JTOL_P [UI pp]  /slew line   JTOL_PI [UI pp]  /acc line")
    for f, a, b, ls, la in zip(freqs, jt_p, jt_pi, line_slew, line_acc):
        print(f"    {f:9.3e}  {a:10.3f}   {a/ls:7.3f}     {b:10.3f}    {b/la:7.3f}")
    f30 = 30e3
    s30 = slew/(np.pi*f30)
    s30v = slew_vote/(np.pi*f30)
    a30 = acc/(2*np.pi**2*f30**2)
    j30_p = sj_tolerance(f30, 0.0, s30 + MARGIN_UI, rng, n_amp=128, span=0.25)
    j30_v = sj_tolerance(f30, 0.0, s30v + MARGIN_UI, rng, vote=N_DEC, n_amp=64, span=0.2)
    j30_pi = sj_tolerance(f30, KI_UI, a30 + MARGIN_UI, rng, n_amp=128, span=0.5)
    lin30 = MARGIN_UI/np.sqrt(H_highpass_mag2(np.array([f30]), 1e6, 0.707)[0])
    print(f"    30 kHz, P only, one decision/update: {j30_p:.1f} UI pp; rho_T slew line {s30:.1f}; ratio {j30_p/s30:.3f}")
    print(f"    30 kHz, P only, majority vote of 16: {j30_v:.1f} UI pp; slew line {s30v:.1f}; ratio {j30_v/s30v:.3f}")
    print(f"    30 kHz, P+I (K_i = K_p/1024):        {j30_pi:.1f} UI pp; acceleration line {a30:.1f}; ratio {j30_pi/a30:.3f}; "
          f"linear type-II template (1 MHz, 0.707) {lin30:.1f}")
    print(f"    high-frequency plateau (100 MHz): P {jt_p[-1]:.3f}, P+I {jt_pi[-1]:.3f} UI pp; margin {MARGIN_UI:.3f}")

    # ---------------- (e) SSC ----------------------------------------------
    fm, delta = 30e3, 0.005
    n_ssc = int(3*FU/fm)
    worst, tr = bb_loop(lambda k: np.repeat(ssc_phase(k, delta, fm)[:, None], 2, axis=1),
                        n_ssc, 2, np.array([0.0, KI_UI]), rng, eval_from=0, trace=True)
    a_ssc = delta*FB/(1/fm/2)
    per = int(FU/fm)
    k = np.arange(n_ssc)
    tau = np.mod(k, per)/per
    mid_up = (tau > 0.15) & (tau < 0.45) & (k > per)          # settled part of the up-ramp
    mid_dn = (tau > 0.65) & (tau < 0.95) & (k > per)
    mean_up = tr[mid_up, 1].mean()*UI
    mean_dn = tr[mid_dn, 1].mean()*UI
    pred = np.sqrt(2)*SIGMA_J*erfinv(a_ssc/acc)
    s_ramp = 0.5*(tr[mid_up, 1].std() + tr[mid_dn, 1].std())*UI   # clock hunting on the ramps
    sig_eff = np.hypot(SIGMA_J, s_ramp)                            # jitter the PD really sees
    pred_eff = np.sqrt(2)*sig_eff*erfinv(a_ssc/acc)
    print(f"(e) SSC phase pp = {delta*FB/fm/8:.1f} UI, ramp acceleration = {a_ssc:.2e} UI/s^2, "
          f"integral-path limit = {acc:.2e} UI/s^2 (ratio {a_ssc/acc:.3f})")
    print(f"    P only : max |error| = {worst[0]:.1f} UI  (cycle slips, lock lost)")
    print(f"    P + I  : max |error| = {worst[1]:.4f} UI = {worst[1]*UI*1e12:.2f} ps; "
          f"rms = {tr[per:, 1].std()*UI*1e12:.3f} ps")
    print(f"    P + I  : mean error on the ramps = {mean_up*1e15:+.0f} / {mean_dn*1e15:+.0f} fs; "
          f"sqrt2*sigma*erfinv(a/a_max) = {pred*1e15:.0f} fs with sigma_j alone, "
          f"{pred_eff*1e15:.0f} fs with sigma_eff = {sig_eff*1e15:.0f} fs (hunting {s_ramp*1e15:.0f} fs rms included)")

    # ---------------- figure ------------------------------------------------
    fig, axs = plt.subplots(2, 3, figsize=(17.5, 9.6))

    # (a) timing diagram
    ax = axs[0, 0]
    tt = np.linspace(-1.0, 1.0, 801)
    for row, (off, name, col) in enumerate([(+0.16, "時脈早（Δt > 0）", "tab:blue"),
                                             (-0.16, "時脈晚（Δt < 0）", "tab:red")]):
        y0 = 1.6 - 2.6*row
        wave = y0 + 0.5*np.tanh(tt/0.035)                    # old bit = 0, new bit = 1, edge at t = 0
        ax.plot(tt, wave, color="k", lw=2)
        ax.text(-0.98, y0 + 0.72, name, color=col, fontsize=11, fontweight="bold")
        ax.text(-0.98, y0 - 0.38, "舊位元 = 0", fontsize=9)
        ax.text(0.62, y0 + 0.62, "新位元 = 1", fontsize=9)
        ts = np.array([-0.5, 0.0, 0.5]) - off
        labs = ["$D_{k-1}$", "$E_k$", "$D_k$"]
        for tsi, lab in zip(ts, labs):
            val = 1 if tsi > 0 else 0
            ax.plot([tsi, tsi], [y0 - 0.75, y0 + 0.75], color=col, ls="--", lw=1.2)
            ax.plot(tsi, y0 - 0.5 + val, "o", color=col, ms=9, zorder=5)
            ax.text(tsi, y0 - 1.02, f"{lab}={val}", ha="center", color=col, fontsize=10)
        ax.plot([0, 0], [y0 - 0.75, y0 + 0.75], color="gray", lw=0.8)
        verdict = ("$E_k=D_{k-1}\\neq D_k$ → 早，e = +1" if off > 0
                   else "$E_k=D_k\\neq D_{k-1}$ → 晚，e = −1")
        ax.text(0.0, y0 + 0.92, verdict, ha="center", color=col, fontsize=10)
    ax.set_xlim(-1.05, 1.05)
    ax.set_ylim(-2.3, 2.85)
    ax.set_yticks([])
    ax.set_xlabel("時間 [UI]（0 = 資料轉態的名義位置）")
    ax.set_title("(a) Alexander 三取樣：邊緣取樣看到舊位元還是新位元")
    ax.grid(False)

    # (b) PD characteristic
    ax = axs[0, 1]
    xs = np.linspace(-3, 3, 301)
    ax.plot(xs, erf(xs/np.sqrt(2)), "k-", label="理論（只算轉態）erf(Δt/√2σ_j)")
    ax.plot(xs, RHO_T*erf(xs/np.sqrt(2)), "-", color="gray", label="理論（全部位元）ρ_T·erf")
    ax.plot(dts/SIGMA_J, pd_all, "o", color="tab:orange", ms=5, label="Monte-Carlo（全部位元）")
    ax.plot(xs, np.clip(K_BB*SIGMA_J*xs, -1, 1), "--", color="tab:green", label="切線 K_bb·Δt（±1 截止）")
    ax.set_xlabel("靜態偏移 Δt / σ_j（時脈早為正）")
    ax.set_ylabel("PD 平均輸出 ⟨e⟩")
    ax.set_title(f"(b) PD 特性：轉態斜率／K_bb = {slope_trans/K_BB:.3f}")
    ax.legend(loc="upper left", fontsize=8)

    # (c) hunting
    ax = axs[0, 2]
    for D, col in zip((0, 2), ("tab:blue", "tab:red")):
        h = limit_cycle(D)[200:240]
        ax.step(np.arange(h.size), h, where="post", color=col,
                label=f"無雜訊，延遲 D={D}：峰峰 {np.ptp(h):.0f} K_p")
    ax.step(np.arange(40), phi_h[1000:1040]/KP, where="post", color="tab:green", alpha=0.9,
            label=f"有 jitter：rms {s_h/KP:.2f} K_p = {s_h*1e15:.0f} fs")
    ax.set_xlabel("更新次數 k")
    ax.set_ylabel("時脈相位誤差 [K_p]")
    ax.set_title("(c) 一階 bang-bang 迴路的 hunting")
    ax.set_ylim(-3.2, 4.6)
    ax.legend(loc="upper right", fontsize=8)

    # (d) JTOL
    ax = axs[1, 0]
    ff = np.logspace(4, 8, 300)
    lin = MARGIN_UI/np.sqrt(H_highpass_mag2(ff, 1e6, 0.707))
    ax.loglog(ff, lin, "k-", lw=1.4, label="線性 type-II 樣板（f_n=1 MHz, ζ=0.707）")
    ax.loglog(ff, slew/(np.pi*ff), "--", color="tab:blue", lw=1.2, label="slew 線 ρ_T(K_p/UI)f_u/(πf)")
    ax.loglog(ff, acc/(2*np.pi**2*ff**2), "--", color="tab:red", lw=1.2,
              label="加速度線 ρ_T(K_i/UI)f_u²/(2π²f²)")
    ax.axhline(MARGIN_UI, color="gray", ls=":", label=f"平台 UI−TJ_eye = {MARGIN_UI:.3f} UI")
    ax.loglog(freqs, jt_p, "s", color="tab:blue", ms=6, label="模擬：只有比例路徑")
    ax.loglog(freqs, jt_pi, "o", color="tab:red", ms=6, label="模擬：比例＋積分路徑")
    ax.plot(30e3, 520.8, "*", color="tab:purple", ms=14, label="SSC 需求 521 UI @ 30 kHz")
    ax.set_xlabel("正弦 jitter 頻率 f [Hz]")
    ax.set_ylabel("可容忍輸入 jitter [UI 峰峰]")
    ax.set_ylim(0.3, 3e4)
    ax.set_title("(d) 正弦 jitter 容忍度：模擬 vs 三條線")
    ax.legend(loc="upper right", fontsize=7.5)

    # (e) SSC tracking error
    ax = axs[1, 1]
    tms = np.arange(n_ssc)/FU*1e6
    dec = slice(0, n_ssc, 16)
    ax.plot(tms[dec], tr[dec, 0], color="tab:blue", label="只有比例路徑（失鎖）")
    ax.plot(tms[dec], tr[dec, 1], color="tab:red", label="比例＋積分路徑")
    ax.set_yscale("symlog", linthresh=0.5)
    ax.axhline(MARGIN_UI/2, color="gray", ls=":")
    ax.axhline(-MARGIN_UI/2, color="gray", ls=":", label="±(UI−TJ_eye)/2")
    ax.set_xlabel("時間 [µs]")
    ax.set_ylabel("追蹤誤差 Δt [UI]（symlog）")
    ax.set_title("(e) SSC（−0.5 %、30 kHz 三角）追蹤誤差")
    ax.legend(loc="lower left", fontsize=8)

    # (f) zoom of the P+I error + SSC frequency profile
    ax = axs[1, 2]
    ax.plot(tms[dec], tr[dec, 1]*UI*1e12, color="tab:red", lw=0.6, label="比例＋積分：誤差 [ps]")
    blk = 2048
    nb = n_ssc//blk
    avg = tr[:nb*blk, 1].reshape(nb, blk).mean(axis=1)*UI*1e12
    ax.plot(tms[:nb*blk].reshape(nb, blk).mean(axis=1), avg, color="k", lw=1.6, label="區塊平均")
    ax.axhline(pred_eff*1e12, color="tab:green", ls="--",
               label=f"±√2σ_eff·erfinv(a/a_max) = ±{pred_eff*1e15:.0f} fs")
    ax.axhline(-pred_eff*1e12, color="tab:green", ls="--")
    ax.set_xlabel("時間 [µs]")
    ax.set_ylabel("追蹤誤差 Δt [ps]")
    ax2 = ax.twinx()
    tau_s = np.mod(tms*1e-6, 1/fm)*fm
    prof = -delta*1e6*np.where(tau_s < 0.5, 2*tau_s, 2 - 2*tau_s)
    ax2.plot(tms[dec], prof[dec], color="tab:purple", lw=1.0, alpha=0.6)
    ax2.set_ylabel("SSC 頻偏 [ppm]", color="tab:purple")
    ax2.grid(False)
    ax.set_title("(f) 積分路徑追 SSC：誤差只有 ps 等級")
    ax.legend(loc="upper right", fontsize=8)

    savefig(fig, "bb_cdr.png")
    print(f"runtime {time.time()-t0:.1f} s")


if __name__ == "__main__":
    main()
