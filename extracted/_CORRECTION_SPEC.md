# ISF Site — v3 Correction Spec (single source of truth)

All values below were verified by reading the actual paper PDFs (high-DPI render) in June 2026.
Fix-agents: apply every item that appears in YOUR assigned file. Use Grep to find occurrences.
Keep Traditional-Chinese + English-term style. Math fences: every `$$` on its own line; no `&gt;`/`&lt;`
inside math (use `>`/`<`); table-cell math uses `\vert`. NEVER fabricate.

## C1 — Ring FOM prefactor: 8/(3γ) → 8/(3η)  [HIGH; corrects a prior WRONG "verified" edit]
[P2] Eq.(23), journal p.796, reads **L{Δf} ≈ (8/3η)·(kT/P)·(V_DD/V_char)·(f₀/Δf)²**, where **η** is the
stage-delay proportionality constant (Eq.(14), η≈1), NOT γ. γ enters only through **V_char = ΔV/γ**.
The V_T=0 minimum [P2] Eq.(25) is **16γ/(3η)** (NOT 16γ/3 — the η was dropped).
- Replace every `\frac{8}{3\gamma}` / `8/(3γ)` ring-FOM prefactor with `\frac{8}{3\eta}` (η≈1).
- Replace the V_T=0 minimum `16γ/3` with `\frac{16\gamma}{3\eta}`.
- DELETE the false notes claiming "先前寫的 8/(3η)…為錯誤，已更正" / "previously 8/(3η) was an error,
  corrected to 8/(3γ), verified verbatim" — they invert reality. Replace with an honest note:
  "[P2] Eq.(23) 的前置係數是 8/(3η)（η 為級延遲比例常數 Eq.14，≈1）；γ 僅透過 V_char=ΔV/γ 進入。
  （v2 曾誤改為 8/(3γ) 並誤標『逐字核實』，v3 已對照原始 PDF p.796 更正。）"
- Worked example recompute (inputs unchanged: f₀=5 GHz, Δf=1 MHz, kT=4.0e-21 J, P=1 mW, V_DD/V_char=3, η=1):
  prefactor 8/(3η)=8/3≈2.667; L = 10·log10(2.667·4.0e-18·3·(5000)²) = 10·log10(8.0e-10) = **−91.0 dBc/Hz**.
  Change every `−89.2` ring-FOM value to **−91.0**; the step `8/(3γ)=8/(3·2/3)=4` → `8/(3η)=8/3≈2.667`
  (η≈1; γ already sits inside V_DD/V_char=3). Update python `8/(3*gamma)` → `8/(3*eta)` with `eta=1.0`,
  and the `# ->` expected dict `{3:-91.0,5:-91.0,15:-91.0}`.
- **Also fix the stale `−95.7` in lc_vs_ring.md (it disagrees with the page's own −89.2): set to −91.0.**

## C2 — Ring accumulated-jitter law citation: Eq.(10) → Eq.(8)  [HIGH]
σ_Δt = κ√Δt is **[P2] Eq.(8), p.792**; the κ formula is [P2] Eq.(12), p.793.
Replace any "[P2] … Eq.(10)" for σ_Δt=κ√Δt with "[P2] Eq.(8), p.792". In lab_11 line ~167 also fix
"Eq.(10), p.793" → "Eq.(8), p.792".

## C3 — [P4] ISF/APF figure: Fig.3 → Fig.5; APF equation numbers  [HIGH]
Verified in [P4] (BHongGenTheor-II): **Fig.5 (p.2126)** = "Characterizing the effect that an instantaneous
injection of charge has on an oscillator" (the ISF / excess-phase / amplitude-decay / APF figure).
Fig.3 (p.2124) is the impulse-train↔sinusoid equivalence; Fig.6 (p.2127) is the bipolar Colpitts example.
APF decomposition D(τ,φ)=Λ̃(φ)·d(τ,φ) = **Eq.(18)**; APF definition Δ(φ):=∫₀^∞ D dτ (units **[1/A]**) = **Eq.(19)**;
amplitude change = **Eq.(20)**; augmented pulling equation = **Eq.(21)** (sinusoidal form **Eq.(22)**) — all p.2126.
Ideal-LC quadrature (ISF fundamental ∠90°, APF fundamental ∠0°) = **Eq.(26), p.2128** (Eq.(24) gives the sin/cos forms);
decay d(t,φ)=e^{−t/τ₀}, τ₀=2Q/ω_osc, is in the same ideal-LC section p.2127–2128.
- Replace "[P4] Fig.3" (for ISF/APF/quadrature) with "[P4] Fig.5, p.2126".
- Replace the wrong "APF … Eq.(25)/(26)/(27)" with the correct numbers above.
- Remove the self-contradiction in paper_004 (one line says "已核實", another "TODO 待對照"): keep ONE
  corrected, consistent citation.

## C4 — [P4] Sec.VIII page: "p.1163" → p.2135  [MED]
"VIII. APPLICATION: DUAL-MODULUS PRESCALER" begins **p.2135**; schematic Fig.19, Table VIII, Fig.21 on **p.2137**.
[P4] full range pp.2122–2139. Replace "約 p.1163" with "p.2135".

## C5 — [P2] Fig.17 page: p.800 → p.802  [MED]; close ⚠️
[P2] Fig.17 "Phase noise versus symmetry voltage for oscillator number 7" is on **p.802** (y-axis = 1/f³ corner
frequency, sharp dip at the symmetry point). Replace "p.800" → "p.802" and CLOSE the related ⚠️/manual-verification
markers (verified).

## C6 — [P1] cyclostationary TODO → CLOSE  [MED]
Verified [P1] **Sec. II-D "Cyclostationary Noise Sources", p.186**: i_n(t)=i_n0(t)·α(ω₀t) = **Eq.(25)**;
substitution into (11) = **Eq.(26)**; effective ISF **Γ_eff(x)=Γ(x)·α(x) = Eq.(27)**. (Fig.14 caption
"Γ(x), Γ_eff(x), and α(x) for the Colpitts oscillator of Fig. 5(a)" is on the facing p.187.)
Replace the lab_14 TODO and any α(x)/Γ_eff citation with "[P1] Sec. II-D, Eq.(25)–(27), p.186".

## C7 — [P3] generalized Adler TODO → CLOSE + sign reconcile  [MED]
Verified [P3] (BHongGenTheor-I), pp.2113–2114: Γ̃=Γ/q_max (units 1/C) = **Eq.(26)**; dφ/dt=Γ̃[φ]·i_inj = **Eq.(28)**;
injection-frame dθ/dt=ω₀−ω_inj+Γ̃(ω_inj t+θ)·i_inj = **Eq.(29)**; time-averaged generalized Adler
dθ/dt = ω₀−ω_inj **+** (1/T_inj)∫Γ̃(ω_inj t+θ)·i_inj dt = **Eq.(30)** (note **PLUS** sign, averaging period T_inj);
lock characteristic Ω(θ) = **Eq.(33)**; sinusoidal lock range **ω_L = ½ I_inj|Γ̃₁| = Eq.(35), p.2114**.
- Close the ⚠️ markers citing [P3] Eq.(30) p.2113 / Eq.(35) p.2114.
- The docs currently write the averaged term with a **MINUS** sign — reconcile to the paper's **PLUS**, OR add an
  explicit one-line note "本站 Γ 取與 [P3] 相反的符號慣例，故平均項前為 −；數值等價". Do not leave it unstated.
- Lock range symbol is ω_L (not Δω_L).

## C8 — [P2] Γrms Eq.(16) ⚠️"常數待查" → CLOSE  [MED]
Verified [P2] **Eq.(16), p.794**: Γrms = √( (2π²/(3η³))·(1/N^1.5) ) = √(2π²/(3η³))·N^(−3/4), η≈1 (η, not γ).
Remove every "⚠️ 常數待查 / constant to be verified" attached to Γrms∝N^(−3/4); replace with
"[P2] Eq.(16), p.794（已核實）". This matches _AUTHORING_SPEC item 22.

## C9 — [P2] f0 period relation: Eq.(14) → Eq.(15)  [LOW]
Eq.(14) defines the normalized stage delay t̂_D=η/f'_max; the period relation 2π=2N t̂_D ⇒ f₀=1/(2N τ_D) is **Eq.(15)**, p.794.
Re-cite f₀=1/(2N τ_D) as [P2] Eq.(15).

## C10 — [P1] Fig.4 page: p.182 → p.181  [LOW]; narrow TODO
[P1] Fig.4 (impulse at peak / at zero-crossing / state-space) is on **p.181**. Caption: "(a) Impulse injected at
the peak, (b) impulse injected at the zero crossing, and (c) effect of nonlinearity on amplitude and phase … in
state-space." Fix p.182→p.181 and narrow the TODO (only fine axis-tick values remain un-transcribed).

## C11 — 1/f³ corner: standardize to the exact form, canonical Γrms=0.5 → 320 kHz  [HIGH consistency]
The corner is [P1] Eq.(24): Δω_{1/f³}/Δω_{1/f} = **c₀²/(2Γrms²)**. With the site-canonical **Γrms=0.5**, c₀=0.4,
device f_{1/f}=1 MHz: corner = 0.16/(2·0.25)=0.32 → **320 kHz**. Use this on ALL three pages
(flicker_noise_upconversion, symmetry, device_noise_mapping). On flicker_noise_upconversion, present the
(c₀/c₁)² form only as the special case "若 ISF 僅含基波則 Γrms²=c₁²/2，化簡為 (c₀/c₁)²"; compute the actual
number with the canonical Γrms=0.5 → 320 kHz. (exercises.md c₀=0.2 → 40 kHz is a different input — leave it.)

## C12 — Lorentzian linewidth 2× split: add cross-notes (do NOT silently differ)  [HIGH consistency]
capstone_lc_end_to_end uses the TRUE ideal-LC Γrms=1/√2 ⇒ D=0.25 rad²/s ⇒ Δf_3dB=D/π≈**80 mHz**.
lorentzian_linewidth example uses the representative canonical Γrms=0.5 ⇒ D=0.125 ⇒ ≈**40 mHz**.
Add an explicit cross-note on BOTH pages (mirroring the existing −145/−148 dBc reconciliation): the 2× is the
Γrms²=0.5-vs-0.25 packaging, not an error. ALSO in capstone fix the internal HWHM/FWHM wording: the flattening
offset ≈ HWHM = D/2π ≈ 40 mHz while the boxed FWHM linewidth = D/π ≈ 80 mHz (state both so they don't look contradictory).

## C13 — "cyclostationary" Chinese gloss: standardize to 週期穩態  [LOW]
Canonical gloss = **週期穩態（cyclostationary）**. Replace "循環平穩" (white_noise_to_phase_noise) and
"循環穩態" (device_noise_mapping) with 週期穩態.

## C14 — Broken python example: accumulated_jitter_curve  [HIGH code]
In paper_002 line ~92 the call `accumulated_jitter_curve(sigma_edge=50e-15, max_lag=500, n_trials=2000)` is broken
(missing required `f0`, wrong kwarg `max_lag`). Correct to
`accumulated_jitter_curve(f0=5e9, sigma_edge=50e-15, max_lag_periods=500, n_trials=2000)` (matches lab_03) and make
the marker checkable, e.g. `print(round(slope,2))  # -> 0.50`. Also fix `max_lag=500`→`max_lag_periods=500` in figure_index.md.

## C15 — lab_05 Parseval DC double-count  [HIGH code]
In simulations/lab_05_fourier_isf.py `fig_coefficients`, change `parseval_lhs = c[0]**2 + np.sum(c[1:]**2)` to
`parseval_lhs = c[0]**2/2 + np.sum(c[1:]**2)` (the DC harmonic enters Parseval as (c₀/2)²). Verified: the fixed LHS
equals 2·Γrms² exactly. Regenerate the PNG (run `python scripts/run_all_sims.py` or this lab) so the title shows
"sum = 2Γrms²" (match), and add a one-line caption noting the DC term enters as (c₀/2)².

## C16 — verification-status drift  [MED]
Several pages mark the SAME [P2] Eq.(16)/Eq.(23) constants both "✓已核實" and "⚠️待查". After C1/C8, resolve to a
single status: Eq.(16) verified (C8); Eq.(23) prefactor corrected to 8/(3η) and verified (C1). Remove stale ⚠️ on
paper_002:~229, paper_summary_table:~25, lc_vs_ring:~140. Scope any residual C7-FOM caveat to the prefactor only,
not to the N-independence conclusion (which is solidly [P2] Sec.V, Eq.(23)/(25), p.796).

## C17 — references.md external citations (verified DOIs)  [MED]
Use these verified citations (CrossRef-confirmed):
- [E1] Leeson 1966: D. B. Leeson, "A simple model of feedback oscillator noise spectrum," Proc. IEEE, vol. 54,
  no. 2, pp. 329–330, Feb. 1966, doi:10.1109/PROC.1966.4682.
- [E2] Demir 2000: A. Demir, A. Mehrotra, J. Roychowdhury, "Phase noise in oscillators: a unifying theory and
  numerical methods for characterization," IEEE TCAS-I, vol. 47, no. 5, pp. 655–674, May 2000, doi:10.1109/81.847872.
- [E3] Kärtner 1990: F. X. Kärtner, "Analysis of white and f^{−α} noise in oscillators," Int. J. Circuit Theory
  Appl., vol. 18, no. 5, pp. 485–519, Sep. 1990, doi:10.1002/cta.4490180505.
- [E4] Adler 1946: R. Adler, "A study of locking phenomena in oscillators," Proc. IRE, vol. 34, no. 6, pp. 351–357,
  Jun. 1946, doi:10.1109/JRPROC.1946.229930.
Also correct references.md's blanket "[P2] Eq.8/12/14/16/17/21/23 皆已逐字核實" to reflect that Eq.(23) was
corrected to 8/(3η) in v3 (C1), and "[P4] Eq.25/26/27 APF" → the correct Eq.(18)–(22) + Fig.5 (C3).

## C18 — _AUTHORING_SPEC.md items 21/22/23 (root source)  [HIGH]
Item 23 (ring FOM) must be corrected to 8/(3η) and min 16γ/(3η) per C1. Item 21 (f0) → Eq.(15) per C9.
Item 22 (Γrms Eq.16) is already correct (η). This is the propagation root — fix it so future authors don't re-spread 8/(3γ).
