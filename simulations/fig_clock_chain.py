"""
fig_clock_chain.py — clock-chain noise bookkeeping (x N / / N / PLL / buffer).

Companion script for docs/06_design_insights/clock_chain_budget.md.

Worked chain (all levels are illustrative "representative" numbers, consistent
with the site canonicals; NOT a specific silicon design):

    100 MHz reference, flat floor  L_ref = -160 dBc/Hz
      -> PLL x50 (fn = 1 MHz, zeta = 0.707)  -> 5 GHz
             in-band  : L = L_ref + 20*log10(50)  (= ref + 33.98 dB)
             out-band : VCO free-running, site canonical L(1 MHz) = -148 dBc/Hz
                        ([P1] Eq.(21) /4 SSB convention, canonical example B)
      -> ideal /2 -> 2.5 GHz  (-20*log10(2) = -6.02 dB at every offset)
      -> output buffer, additive floor L_buf = -155 dBc/Hz

Printed results (used as checkable markers on the page):
  * the four bookkeeping-rule constants (20log50, 20log2, dB-addition table)
  * stage-by-stage L at 100 kHz (in-band) and 10 MHz (out-of-band)
  * total integrated jitter of the final 2.5 GHz clock, 10 kHz - 100 MHz
    (brick-wall model), plus per-source breakdown
  * sigma_t invariance check across ideal x N / / N (seconds are conserved)
  * honesty check: full type-II 2nd-order shaping (pll_utils) vs brick-wall;
    the +25 dB parallel reference tail; effect of an extra 3rd pole; and the
    jitter-optimal fn for THIS budget.

Figure produced:  static/figures/clock_chain_budget.png

Conventions: L = 0.5*S_phi (SSB small-angle, site standard, noise_utils);
the VCO anchor -148 dBc/Hz is the [P1] Eq.(21) "/4" SSB value (the clean
time-domain "/2" derivation would give -145; see white_noise_to_phase_noise).
"""
import numpy as np

from simulations.common.pll_utils import H_lowpass_mag2, H_highpass_mag2
from simulations.common.noise_utils import integrate_rms_jitter
from simulations.common.plot_utils import savefig
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# chain parameters (site canonicals + representative levels)
# ---------------------------------------------------------------------------
F_REF   = 100e6          # reference frequency [Hz]
L_REF   = -160.0         # reference flat floor [dBc/Hz] (illustrative)
N_MULT  = 50             # PLL multiplication 100 MHz -> 5 GHz
F0_PLL  = 5e9            # PLL output carrier [Hz]
FN      = 1e6            # PLL loop natural frequency [Hz]
ZETA    = 0.707          # damping
L_VCO_1M = -148.0        # site canonical VCO SSB @1MHz ([P1] Eq.21, /4 SSB)
N_DIV   = 2              # divide-by-2 -> 2.5 GHz
F0_OUT  = 2.5e9          # final carrier [Hz]
L_BUF   = -155.0         # output-buffer additive floor [dBc/Hz]
F1, F2  = 1e4, 1e8       # jitter integration band [Hz]


def padd_db(*Ls):
    """Add SSB phase-noise levels as linear powers (rule 4)."""
    return 10 * np.log10(sum(10 ** (np.asarray(L) / 10.0) for L in Ls))


def main():
    print("=" * 72)
    print("[0] canonical VCO anchor check (example B, [P1] Eq.(21), /4 SSB)")
    gamma_rms, qmax, Si, dw = 0.5, 1e-12, 1e-24, 2 * np.pi * 1e6
    L_eq21 = 10 * np.log10((gamma_rms**2 / qmax**2) * Si / (4 * dw**2))
    print(f"  L(1MHz) [P1] Eq.21 = {L_eq21:.1f} dBc/Hz   (/2 time-domain: "
          f"{10*np.log10((gamma_rms**2/qmax**2)*Si/(2*dw**2)):.1f})")

    # -------------------------------------------------------------- rule 1&2
    print("=" * 72)
    print("[1] rule constants")
    mult_db = 20 * np.log10(N_MULT)
    div_db = -20 * np.log10(N_DIV)
    print(f"  xN  : +20*log10(50) = {mult_db:.2f} dB")
    print(f"  /N  : -20*log10(2)  = {div_db:.2f} dB")
    print("  dB-addition table (floor Delta dB below signal -> penalty):")
    for d in (20, 10, 6, 3, 0):
        pen = 10 * np.log10(1 + 10 ** (-d / 10))
        print(f"    Delta = {d:2d} dB  ->  +{pen:.2f} dB")

    # -------------------------------------------------------------- chain
    print("=" * 72)
    print("[2] worked chain, brick-wall bookkeeping, L at 100 kHz / 10 MHz")
    f_ib, f_ob = 1e5, 1e7
    # stage 0: reference (flat floor model)
    L0_ib, L0_ob = L_REF, L_REF
    # stage 1: PLL out @5 GHz: in-band ref+20logN ; out-of-band VCO 1/f^2
    L1_ib = L_REF + mult_db
    L1_ob = L_VCO_1M - 20 * np.log10(f_ob / 1e6)
    # stage 2: ideal /2 @2.5 GHz
    L2_ib, L2_ob = L1_ib + div_db, L1_ob + div_db
    # stage 3: + buffer floor (additive)
    L3_ib, L3_ob = padd_db(L2_ib, L_BUF), padd_db(L2_ob, L_BUF)
    rows = [("ref @100 MHz", L0_ib, L0_ob),
            ("PLL x50 @5 GHz", L1_ib, L1_ob),
            ("/2 @2.5 GHz", L2_ib, L2_ob),
            ("buffer @2.5 GHz", L3_ib, L3_ob)]
    for name, a, b in rows:
        print(f"  {name:18s}  L(100kHz) = {a:8.2f}   L(10MHz) = {b:8.2f}  dBc/Hz")
    # crossover: L1_ib = L_VCO_1M - 20*log10(f/1e6)  ->  solve for f
    f_x = 1e6 * 10 ** ((L_VCO_1M - L1_ib) / 20.0)
    print(f"  crossover ref-floor(xN) vs VCO skirt @5GHz: {f_x/1e3:.1f} kHz")

    # -------------------------------------------------------------- jitter
    print("=" * 72)
    print("[3] final 2.5 GHz clock: integrated jitter 10 kHz - 100 MHz (brick-wall)")
    f = np.logspace(np.log10(F1), np.log10(F2), 20001)
    # in-band: divided ref floor; out-of-band: divided VCO skirt (1 MHz anchor)
    L_core = np.where(f <= FN, L2_ib,
                      (L_VCO_1M + div_db) - 20 * np.log10(f / 1e6))
    L_tot = padd_db(L_core, L_BUF)
    st, sp = integrate_rms_jitter(f, L_tot, f0=F0_OUT, fmin=F1, fmax=F2)
    print(f"  sigma_t(total)  = {st*1e15:.1f} fs   sigma_phi = {sp*1e6:.1f} urad")

    # per-source breakdown (integrate each piece alone)
    st_ib, _ = integrate_rms_jitter(f, np.where(f <= FN, L2_ib, -400.0),
                                    f0=F0_OUT, fmin=F1, fmax=F2)
    st_vco, _ = integrate_rms_jitter(
        f, np.where(f > FN, (L_VCO_1M + div_db) - 20 * np.log10(f / 1e6), -400.0),
        f0=F0_OUT, fmin=F1, fmax=F2)
    st_buf, _ = integrate_rms_jitter(f, np.full_like(f, L_BUF),
                                     f0=F0_OUT, fmin=F1, fmax=F2)
    tot2 = st_ib**2 + st_vco**2 + st_buf**2
    print(f"  breakdown: in-band(refxN) {st_ib*1e15:.1f} fs ({st_ib**2/tot2*100:.1f}%)"
          f" | VCO {st_vco*1e15:.2f} fs ({st_vco**2/tot2*100:.2f}%)"
          f" | buffer {st_buf*1e15:.1f} fs ({st_buf**2/tot2*100:.1f}%)")
    print(f"  RSS check: {np.sqrt(tot2)*1e15:.1f} fs (= total above)")

    # -------------------------------------------------------------- invariance
    print("=" * 72)
    print("[4] sigma_t (seconds) invariance under ideal xN / /N")
    L_5g = np.where(f <= FN, L1_ib, L_VCO_1M - 20 * np.log10(f / 1e6))
    st5, _ = integrate_rms_jitter(f, L_5g, f0=F0_PLL, fmin=F1, fmax=F2)
    st25, _ = integrate_rms_jitter(f, L_5g + div_db, f0=F0_OUT, fmin=F1, fmax=F2)
    print(f"  sigma_t @5 GHz (no buffer)      = {st5*1e15:.1f} fs")
    print(f"  sigma_t @2.5 GHz after ideal /2 = {st25*1e15:.1f} fs  (identical)")

    # -------------------------------------------------------------- honesty
    print("=" * 72)
    print("[5] honesty check: type-II 2nd-order shaping (pll_utils) vs brick-wall")
    S_refN2 = 2 * 10 ** (L1_ib / 10)          # N^2*S_ref, flat [rad^2/Hz]
    S_buf = 2 * 10 ** (L_BUF / 10)

    def sphi_final_shaped(fv, fn, third_pole=None):
        lp = H_lowpass_mag2(fv, fn, ZETA)
        hp = H_highpass_mag2(fv, fn, ZETA)
        ref_path = S_refN2 * lp
        if third_pole is not None:
            ref_path = ref_path / (1 + (fv / third_pole) ** 2)
        S_vco = 2 * 10 ** (L_VCO_1M / 10) * (1e6 / fv) ** 2
        return (ref_path + S_vco * hp) / N_DIV**2 + S_buf

    # spot levels
    for fv in (1e5, 1e7):
        S = sphi_final_shaped(np.array([fv]), FN)[0]
        print(f"  shaped final L({fv/1e6:.1f} MHz) = {10*np.log10(0.5*S):.1f} dBc/Hz"
              f"   (brick-wall: {padd_db(np.interp(fv, f, L_core), L_BUF):.1f})")
    # the parallel-tail constant: ref path vs VCO, both -20 dB/dec beyond fn
    fv = 1e7
    L_refpath_5g = 10 * np.log10(0.5 * S_refN2 * H_lowpass_mag2(fv, FN, ZETA))
    L_vco_5g = L_VCO_1M - 20 * np.log10(fv / 1e6)
    print(f"  @10 MHz, 5 GHz carrier: ref-path {L_refpath_5g:.1f} vs VCO "
          f"{L_vco_5g:.1f} dBc/Hz -> ref tail sits +{L_refpath_5g - L_vco_5g:.1f} dB"
          f" ABOVE the VCO at ALL out-of-band offsets (both -20 dB/dec)")

    for tag, tp in (("2nd-order only          ", None),
                    ("+ 3rd pole @ 3 MHz      ", 3e6)):
        S = sphi_final_shaped(f, FN, tp)
        sphi2 = np.trapezoid(S, f)
        stx = np.sqrt(sphi2) / (2 * np.pi * F0_OUT)
        print(f"  shaped sigma_t ({tag}) = {stx*1e15:.1f} fs   "
              f"(brick-wall said {st*1e15:.1f} fs)")

    # jitter-optimal fn for THIS budget (shaped, 3rd pole at 3*fn)
    fns = np.logspace(4, 7, 121)
    jt = []
    for fn in fns:
        S = sphi_final_shaped(f, fn, 3 * fn)
        jt.append(np.sqrt(np.trapezoid(S, f)) / (2 * np.pi * F0_OUT))
    jt = np.array(jt)
    k = int(np.argmin(jt))
    print(f"  jitter-optimal loop BW for this budget: fn* = {fns[k]/1e3:.0f} kHz"
          f" -> sigma_t = {jt[k]*1e15:.1f} fs  (chain used fn = 1 MHz)")

    # -------------------------------------------------------------- figure
    print("=" * 72)
    print("[6] figure")
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(11.6, 4.6))
    fig.patch.set_facecolor("white")

    # left: stage-by-stage L(f)
    axL.semilogx(f, np.full_like(f, L_REF), color="0.55", ls="--", lw=1.3,
                 label="reference @100 MHz（-160 平坦床）")
    L_5g_brick = np.where(f <= FN, L1_ib, L_VCO_1M - 20 * np.log10(f / 1e6))
    axL.semilogx(f, L_5g_brick, color="tab:blue", lw=1.6,
                 label="PLL x50 輸出 @5 GHz（brick-wall）")
    axL.semilogx(f, L_5g_brick + div_db, color="tab:green", lw=1.6,
                 label="÷2 之後 @2.5 GHz（-6.02 dB）")
    axL.semilogx(f, np.full_like(f, L_BUF), color="tab:orange", ls=":", lw=1.6,
                 label="buffer 加成床 -155 dBc/Hz")
    axL.semilogx(f, L_tot, color="black", lw=2.4,
                 label="最終 2.5 GHz 時脈（總和）")
    S_shaped = sphi_final_shaped(f, FN)
    axL.semilogx(f, 10 * np.log10(0.5 * S_shaped), color="tab:red", ls="--",
                 lw=1.4, label="最終（type-II 2 階完整整形）")
    for fv, lv in ((1e5, padd_db(L2_ib, L_BUF)), (1e7, padd_db(L2_ob, L_BUF))):
        axL.plot([fv], [lv], "o", color="black", ms=6, zorder=6)
        axL.annotate(f"{lv:.1f}", (fv, lv), textcoords="offset points",
                     xytext=(6, 7), fontsize=9)
    axL.set_xlabel("offset 頻率 $f$ [Hz]")
    axL.set_ylabel(r"$\mathcal{L}(f)$ [dBc/Hz]")
    axL.set_title("時脈鏈各級的 SSB phase noise（記帳）")
    axL.set_ylim(-185, -110)
    axL.legend(loc="lower left", fontsize=7.6, framealpha=0.95)
    axL.grid(True, which="both", alpha=0.3)

    # right: cumulative rms jitter of the final clock
    Sphi_brick = 2 * 10 ** (L_tot / 10)
    cum_brick = np.sqrt(np.concatenate(
        ([0.0], np.cumsum(0.5 * (Sphi_brick[1:] + Sphi_brick[:-1]) * np.diff(f))))) \
        / (2 * np.pi * F0_OUT)
    cum_shaped = np.sqrt(np.concatenate(
        ([0.0], np.cumsum(0.5 * (S_shaped[1:] + S_shaped[:-1]) * np.diff(f))))) \
        / (2 * np.pi * F0_OUT)
    axR.semilogx(f, cum_brick * 1e15, color="black", lw=2.2,
                 label=f"brick-wall 記帳：{cum_brick[-1]*1e15:.1f} fs")
    axR.semilogx(f, cum_shaped * 1e15, color="tab:red", ls="--", lw=1.6,
                 label=f"type-II 2 階整形：{cum_shaped[-1]*1e15:.1f} fs")
    axR.axvline(FN, color="0.6", ls=":", lw=1.2)
    axR.text(FN * 1.15, 3, "loop BW $f_n$=1 MHz", fontsize=8, color="0.4",
             rotation=90, va="bottom")
    axR.set_xlabel("積分上限 $f$ [Hz]（從 10 kHz 積起）")
    axR.set_ylabel(r"累積 rms jitter $\sigma_t$ [fs]")
    axR.set_title("最終 2.5 GHz 時脈：jitter 從哪裡累積")
    axR.legend(loc="upper left", fontsize=8.5, framealpha=0.95)
    axR.grid(True, which="both", alpha=0.3)

    savefig(fig, "clock_chain_budget.png")


if __name__ == "__main__":
    main()
