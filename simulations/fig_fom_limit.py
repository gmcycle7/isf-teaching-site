"""
fig_fom_limit.py — FOM 的理論天花板（thermodynamic-ish ceiling of the oscillator FOM）

Goal
----
Support docs/06_design_insights/fom_limit.md with *checkable* numbers:

  (1) The reference constant  C_ref(T) = -10*log10(kT * 1Hz / 1mW).
      At T = 300 K this is 173.83 dB (this is the "1*kT" pairing; the
      often-misquoted "2kT" pairing gives 170.82 dB — computed below so the
      page never has to trust memory).  At T0 = 290 K, kT in dBm/Hz is the
      famous -174 dBm/Hz thermal floor.

  (2) Universal reduction: any topology whose white-noise (1/f^2) phase noise
      can be written  L_lin = F_eff * (kT/P) * (f0/df)^2   [1/Hz, SSB]
      has          FOM = C_ref(T) - 10*log10(F_eff)        [dB]
      with FOM = -L + 20log10(f0/df) - 10log10(P/1mW)  (positive convention).

  (3) Ring ([P2] Eq.(23), p.796):  F_eff = (8/(3*eta)) * (VDD/Vchar).
      Site worked example (docs/06_design_insights/lc_vs_ring.md):
      eta=1, VDD/Vchar=3 -> F_eff = 8 -> FOM = 164.8 dB;  cross-check against
      the page's L = -91.0 dBc/Hz @ 1 MHz, f0=5 GHz, P=1 mW -> FOM = 165.0 dB
      (0.2 dB gap traced to that page's rounded kT = 4.0e-21 J, which is
      actually the 290 K value).
      VT=0 bound ([P2] Eq.(25)): F_eff >= 16*gamma/(3*eta) -> ring ceiling.

  (4) LC from [P1] Eq.(21), p.185 (single white source, SSB "/4" convention):
      with Si = F*4kT/Rp, qmax = C*Vmax, Ptank = Vmax^2/(2*Rp), Q = w0*Rp*C:
          L_lin = (F*Grms^2/(2*Q^2)) * (kT/Ptank) * (f0/df)^2
      i.e.  F_eff,LC = F*Grms^2 / (2*Q^2*eta_P),  eta_P = Ptank/Pdc <= 1.
      Numeric identity check: reverse-engineering canonical example B
      (Grms=0.5, qmax=1 pC, Si=1e-24 A^2/Hz, f0=5 GHz; assume Vmax=1 V)
      must reproduce L = -148.0 dBc/Hz through BOTH routes.

  (5) Convention discipline: the time-domain "/2" bookkeeping doubles F_eff
      and lowers FOM by exactly 10*log10(2) = 3.01 dB. Leeson's "2FkT" form
      lands on F_eff = F/(2Q^2) (the /2 flavour). C_ref itself is
      convention-free — the 2's live inside F_eff.

Figure produced
---------------
  static/figures/fom_limit.png   (2 panels)
    (a) FOM ceiling family vs temperature T for several fixed F_eff.
    (b) LC ceiling vs tank Q at 300 K (both SSB conventions), with the
        F_eff = 1 reference line, the ring VT=0 ceiling, the site's ring
        worked example, and this page's reverse-engineered LC example.
  NO published-design scatter points are drawn (we do not have verified
  per-design numbers in the 5 site PDFs; the ceiling lines are exact).

Pedagogical model only — no transistor netlist. All formulas from
[P1] Eq.(21) p.185, [P2] Eq.(23)/(25) p.796, plus standard circuit
identities (Q = w0*Rp*C, P = Vmax^2/(2*Rp)) stated in the page.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "common"))

import numpy as np
import matplotlib.pyplot as plt

from plot_utils import savefig

KB = 1.380649e-23      # Boltzmann constant [J/K] (exact SI value)
P_REF = 1e-3           # FOM power reference: 1 mW [W]
B_REF = 1.0            # bandwidth hidden in "per Hz": 1 Hz [Hz]


# ---------------------------------------------------------------------------
# Core relations
# ---------------------------------------------------------------------------
def c_ref_db(T=300.0):
    """Reference constant C_ref(T) = -10*log10(kT*B_ref/P_ref)  [dB]."""
    return -10.0 * np.log10(KB * T * B_REF / P_REF)


def fom_from_L(L_dbc, f0, df, P):
    """FOM (positive convention) from SSB phase noise L [dBc/Hz]."""
    return -L_dbc + 20.0 * np.log10(f0 / df) - 10.0 * np.log10(P / P_REF)


def L_from_feff(F_eff, P, f0, df, T=300.0):
    """L [dBc/Hz] of the universal 1/f^2 form  F_eff*(kT/P)*(f0/df)^2."""
    return 10.0 * np.log10(F_eff * (KB * T / P) * (f0 / df) ** 2)


def fom_from_feff(F_eff, T=300.0):
    """FOM = C_ref(T) - 10*log10(F_eff)  [dB]."""
    return c_ref_db(T) - 10.0 * np.log10(F_eff)


def feff_lc(F, grms2, Q, eta_p=1.0):
    """LC topology noise factor F_eff = F*Grms^2/(2*Q^2*eta_P) ([P1] /4 conv)."""
    return F * grms2 / (2.0 * Q ** 2 * eta_p)


def L_eq21(grms, qmax, Si, df):
    """[P1] Eq.(21), p.185 (SSB, /4 convention)  [dBc/Hz]."""
    dw = 2.0 * np.pi * df
    return 10.0 * np.log10(grms ** 2 / qmax ** 2 * Si / (4.0 * dw ** 2))


def L_ring_eq23(kT, P, f0, df, eta=1.0, vdd_vchar=3.0):
    """[P2] Eq.(23), p.796 (prefactor 8/(3*eta))  [dBc/Hz]."""
    return 10.0 * np.log10(8.0 / (3.0 * eta) * (kT / P) * vdd_vchar * (f0 / df) ** 2)


# ---------------------------------------------------------------------------
def main():
    f0, df = 5e9, 1e6
    gamma = 2.0 / 3.0          # long-channel thermal-noise coefficient
    grms2_lc = 0.5             # true-LC Gamma_rms^2 = (1/sqrt(2))^2

    print("=== [1] 參考常數（reference constant） ===")
    kT300 = KB * 300.0
    print(f"kT(300K) [J]              : {kT300:.4e}")
    print(f"C_ref(300K) = -10log10(kT*1Hz/1mW) [dB] : {c_ref_db(300.0):.2f}")
    print(f"-10log10(2kT/1mW) (300K)  [dB]          : "
          f"{-10*np.log10(2*kT300/P_REF):.2f}   <- 2kT pairing, NOT 173.8")
    print(f"kT(290K) in dBm/Hz (thermal floor)      : "
          f"{10*np.log10(KB*290.0/P_REF):.2f}")
    print(f"C_ref slope near 300K [dB per +10K]     : "
          f"{c_ref_db(310.0)-c_ref_db(300.0):+.3f}")

    print()
    print("=== [2] ring：[P2] Eq.(23)/(25) ===")
    feff_ring = 8.0 / 3.0 * 3.0          # eta=1, VDD/Vchar=3
    print(f"F_eff(ring, VDD/Vchar=3)                : {feff_ring:.3f}")
    print(f"10log10(F_eff)  [dB]                    : {10*np.log10(feff_ring):.2f}")
    print(f"FOM(ring example) = C_ref - 10log10(F_eff) [dB] : "
          f"{fom_from_feff(feff_ring):.2f}")
    # site chain (lc_vs_ring.md uses kT = 4.0e-21 J)
    L_site = L_ring_eq23(4.0e-21, 1e-3, f0, df)
    print(f"L site-chain (kT=4.0e-21) [dBc/Hz]      : {L_site:.2f}   (page quotes -91.0)")
    print(f"FOM from quoted -91.0 dBc/Hz, P=1mW     : {fom_from_L(-91.0, f0, df, 1e-3):.2f}")
    L_300 = L_ring_eq23(kT300, 1e-3, f0, df)
    print(f"L with kT(300K)=4.142e-21 [dBc/Hz]      : {L_300:.2f}")
    print(f"FOM from that L (consistent kT)         : {fom_from_L(L_300, f0, df, 1e-3):.2f}")
    ident = fom_from_L(L_300, f0, df, 1e-3) + 10*np.log10(feff_ring) - c_ref_db(300.0)
    print(f"identity check FOM+10log10(Feff)-C_ref  : {ident:.2e}   (should be ~0)")
    feff_ring_min = 16.0 * gamma / 3.0   # [P2] Eq.(25), VT=0, eta=1
    print(f"F_eff min (VT=0, Eq.25) = 16*gamma/3    : {feff_ring_min:.3f}")
    print(f"ring ceiling FOM_max [dB]               : {fom_from_feff(feff_ring_min):.2f}")
    print(f"ring example distance to ring ceiling   : "
          f"{fom_from_feff(feff_ring_min)-fom_from_feff(feff_ring):.2f} dB")

    print()
    print("=== [3] LC：[P1] Eq.(21) → F_eff = F*Grms^2/(2*Q^2*eta_P) ===")
    # Reverse-engineer canonical example B as a single tank source, Vmax = 1 V.
    Si, qmax, grms = 1e-24, 1e-12, 0.5
    Rp = 4.0 * kT300 / Si                # Si = 4kT/Rp  ->  Rp
    Vmax = 1.0
    C = qmax / Vmax
    w0 = 2.0 * np.pi * f0
    Q = w0 * Rp * C
    Ptank = Vmax ** 2 / (2.0 * Rp)
    print(f"Rp = 4kT/Si [ohm]                       : {Rp:.0f}")
    print(f"C = qmax/Vmax [F]                       : {C:.1e}")
    print(f"Q = w0*Rp*C (dimensionless)             : {Q:.1f}")
    print(f"Ptank = Vmax^2/(2Rp) [W]                : {Ptank:.3e}")
    feffB = feff_lc(F=1.0, grms2=grms ** 2, Q=Q)
    L_direct = L_eq21(grms, qmax, Si, df)
    L_via_feff = L_from_feff(feffB, Ptank, f0, df)
    print(f"F_eff(example B, F=1)                   : {feffB:.3e}")
    print(f"L direct  [P1] Eq.(21) [dBc/Hz]         : {L_direct:.2f}")
    print(f"L via F_eff*(kT/P)*(f0/df)^2 [dBc/Hz]   : {L_via_feff:.2f}")
    print(f"algebra identity |diff| [dB]            : {abs(L_direct-L_via_feff):.2e}")
    fomB1 = fom_from_L(L_direct, f0, df, Ptank)
    fomB2 = fom_from_feff(feffB)
    print(f"FOM(example B) via L,P route [dB]       : {fomB1:.2f}")
    print(f"FOM(example B) via F_eff route [dB]     : {fomB2:.2f}   (Q=520 -> unphysical on-chip)")

    F_ideal = 1.0 + gamma                # tank + ideal class-B pair (external: Hegazi 2001)
    for Qv in (10.0, 15.0, 20.0):
        fom4 = fom_from_feff(feff_lc(F_ideal, grms2_lc, Qv))
        fom2 = fom4 - 10*np.log10(2.0)
        print(f"LC ceiling Q={Qv:4.0f}: FOM_max = {fom4:.2f} dB ([P1]/4 conv) | "
              f"{fom2:.2f} dB (/2 conv, Leeson 2FkT)")

    print()
    print("=== [4] ring 落後 LC 天花板的分解（Q=10 ideal） ===")
    d_pref = 10*np.log10(8.0/3.0)
    d_vchar = 10*np.log10(3.0)
    d_store = 10*np.log10(2.0*10.0**2)
    d_wave = -10*np.log10(F_ideal*grms2_lc)
    total = d_pref + d_vchar + d_store + d_wave
    gap = fom_from_feff(feff_lc(F_ideal, grms2_lc, 10.0)) - fom_from_feff(feff_ring)
    print(f"prefactor 8/3      [dB] : {d_pref:.2f}")
    print(f"VDD/Vchar = 3      [dB] : {d_vchar:.2f}")
    print(f"storage 2Q^2 (Q=10)[dB] : {d_store:.2f}")
    print(f"waveform (1+g)G^2  [dB] : {d_wave:.2f}")
    print(f"sum of terms       [dB] : {total:.2f}")
    print(f"direct FOM gap     [dB] : {gap:.2f}   (must equal the sum)")

    print()
    print("=== [5] 反推 worked example（L=-125 dBc/Hz @1MHz, f0=5GHz, P=10mW） ===")
    fom_ex2 = fom_from_L(-125.0, f0, df, 10e-3)
    feff_ex2 = 10 ** ((c_ref_db(300.0) - fom_ex2) / 10.0)
    Q_implied = np.sqrt(2.0 * grms2_lc / (2.0 * feff_ex2 * 0.5))  # F=2, eta_P=0.5
    print(f"FOM  [dB]                               : {fom_ex2:.2f}")
    print(f"implied F_eff                           : {feff_ex2:.4f}")
    print(f"implied Q (F=2, Grms^2=0.5, eta_P=0.5)  : {Q_implied:.2f}")
    print(f"convention shift /4 -> /2 [dB]          : {-10*np.log10(2.0):.2f}")

    # -----------------------------------------------------------------------
    # Figure
    # -----------------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.6))

    # (a) ceiling family vs temperature
    T = np.linspace(250, 400, 301)
    families = [
        (1.0, r"$F_{eff}=1$（$kT$ 參考線）", "tab:blue", "-"),
        (feff_ring_min, r"ring 天花板 $F_{eff}=16\gamma/3\approx3.56$", "tab:red", "-"),
        (feff_ring, r"ring 例 $F_{eff}=8$（$V_{DD}/V_{char}=3$）", "tab:orange", "--"),
        (feff_lc(F_ideal, grms2_lc, 10.0),
         r"LC 理想天花板 $Q=10$（$F=1+\gamma$）", "tab:green", "-"),
        (feff_lc(F_ideal, grms2_lc, 30.0),
         r"LC 理想天花板 $Q=30$", "tab:green", "--"),
    ]
    for fe, lab, col, ls in families:
        ax1.plot(T, [fom_from_feff(fe, t) for t in T], color=col, ls=ls, label=lab)
    ax1.axvline(300.0, color="gray", lw=1, ls=":")
    ax1.annotate("T = 300 K", xy=(302, 202.5), fontsize=9, color="gray", ha="left")
    ax1.set_xlabel("溫度 T (K)")
    ax1.set_ylabel("FOM 上限 (dB)")
    ax1.set_title("(a) FOM 天花板家族 vs 溫度（各 $F_{eff}$ 一條線）")
    ax1.legend(fontsize=8, loc="center right")

    # (b) LC ceiling vs Q at 300 K
    Qs = np.logspace(np.log10(2), np.log10(100), 200)
    fom4 = np.array([fom_from_feff(feff_lc(F_ideal, grms2_lc, q)) for q in Qs])
    ax2.plot(Qs, fom4, color="tab:green",
             label=r"LC 理想天花板（[P1] Eq.(21) SSB /4 慣例）")
    ax2.plot(Qs, fom4 - 10*np.log10(2.0), color="tab:green", ls="--",
             label=r"同上、時域 /2 慣例（Leeson $2FkT$）：低 3.0 dB")
    ax2.axhline(c_ref_db(300.0), color="tab:blue", lw=1.2,
                label=r"$F_{eff}=1$：173.8 dB")
    ax2.axhline(fom_from_feff(feff_ring_min), color="tab:red", lw=1.2,
                label=r"ring 天花板（[P2] Eq.(25)）：168.3 dB")
    ax2.axhline(fom_from_feff(feff_ring), color="tab:orange", lw=1.0, ls="--",
                label=r"本站 ring 例：164.8 dB（與 $Q$ 無關）")
    ax2.plot([Q_implied], [fom_ex2], "o", color="tab:purple", ms=7,
             label=f"本頁例 2 反推：FOM=189.0 dB, Q≈{Q_implied:.1f}")
    ax2.plot([10.0], [fom_from_feff(feff_lc(F_ideal, grms2_lc, 10.0))], "s",
             color="tab:green", ms=6)
    ax2.annotate("Q=10 → 197.6 dB",
                 xy=(10.0, fom_from_feff(feff_lc(F_ideal, grms2_lc, 10.0))),
                 xytext=(13, 193.5), fontsize=9,
                 arrowprops=dict(arrowstyle="->", lw=0.8))
    ax2.set_xscale("log")
    ax2.set_xlabel("tank 品質因數 Q（無因次）")
    ax2.set_ylabel("FOM (dB)")
    ax2.set_title("(b) 300 K：LC 天花板 vs Q、ring 天花板、參考線")
    ax2.legend(fontsize=8, loc="lower right")

    savefig(fig, "fom_limit")


if __name__ == "__main__":
    main()
