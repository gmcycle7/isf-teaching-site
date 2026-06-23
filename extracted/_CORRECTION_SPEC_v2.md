# ISF Site — v3 Correction Spec ADDENDUM (round-2 findings, PDF-verified)

Fix-agents: apply every item below that appears in YOUR file (Grep to locate). This ADDENDUM has priority
over any conflicting wording in extracted/_ROUND2_FINDINGS.md. Also read your file's section in
_ROUND2_FINDINGS.md and apply those page-specific fixes. Math fences: every $$ on its own line; no
&gt;/&lt; in math; table-cell math uses \vert. NEVER fabricate.

## D0 — κ (Eq.12) is CORRECT as printed — DO NOT add ω₀  [OVERRIDES the round-2 "κ missing ω₀" finding]
Verified at high zoom against [P2] p.793: **Eq.(11) is σ²_Δφ = (Γ²rms·ī²ₙ/Δf)/(2 q²max)·ΔT** (PHASE jitter,
dimensionless), and **Eq.(12) is κ = (Γrms/q_max)·√( ½·ī²ₙ/Δf )** — there is NO ω₀ in Eq.(12).
- So κ√Δt gives the PHASE jitter σ_Δφ (dimensionless). The TIMING jitter is σ_Δt = σ_Δφ/ω₀ ([P2] Eq.(10):
  σ_ΔT = ω₀·σ_Δτ). The ω₀ lives in the phase→time conversion (Eq.10), NOT inside κ.
- DO NOT add ω₀ to Eq.(12) anywhere. The round-2 finding claiming "κ missing ω₀" is REJECTED (it conflated
  phase vs timing jitter).
- ONLY fix needed: if a page writes "σ_Δt = κ√Δt" and calls the result the *timing* jitter while using the
  Eq.(12) κ, clarify that κ√Δt is the PHASE jitter σ_Δφ (Eq.11/12) and the timing jitter is σ_Δφ/ω₀ (Eq.10).
  Keep κ = (Γrms/q_max)√(½ ī²ₙ/Δf) verbatim.

## D1 — [P4] ISF/APF figure: remaining "Fig. 3" → "Fig. 5, p.2126"
Round-1 C3 missed these pages. Replace "[P4] Fig. 3" (where it denotes the ISF / APF / amplitude-decay /
quadrature characterization figure) with "[P4] Fig. 5, p.2126". Affected: phase_vs_amplitude_noise.md
(≈lines 102,124,181,184), derivation_floquet_ppv.md (≈line 131). DO NOT touch build_report.md's sentence that
*describes the correction itself* ("Fig.3→Fig.5 已更正") — that is correct meta-text.

## D2 — [P4] amplitude-decay form is PROSE, not Eq.(25)
d(t,φ)=e^{−t/τ₀}, τ₀=2Q/ω_osc is unnumbered prose in [P4] Sec. III-F, p.2128. Eq.(25) is Λ(φ)=τ₀·Λ̃(φ)
(APF = τ₀ × amplitude ISF). Where a page cites the decay closed form as "Eq.(25)" (phase_vs_amplitude_noise
≈lines 74,85), recite as "[P4] Sec. III-F, p.2128（緊接 Eq.(25) 之前的正文）" and drop any "已逐字確認 Eq.(25)".

## D3 — [P2] Fig.17 page: remaining "p.800" → "p.802"
Round-1 C5 missed these. flicker_noise_upconversion.md (≈lines 199,203,273) and fourier_series_of_isf.md
(≈line 122): change Fig.17 "p.800" → "p.802".

## D4 — [P2] f0 period relation: remaining "Eq.(14)" → "Eq.(15)"  [CONTEXT-SENSITIVE]
Only where a page cites **f₀ = 1/(2N τ_D)** (the period relation) as Eq.(14): change to **Eq.(15)** ([P2] p.794;
Eq.(14) is the normalized stage delay t̂_D=η/f'_max, Eq.(15) is 2π=2N t̂_D ⇒ f₀=1/(2Nτ_D)). DO NOT change
Eq.(14) where it correctly denotes the stage-delay t̂_D or supplies the η used in the FOM. Likely affected:
paper_002, worked_examples (≈630), exercises (06, ≈line 20), and check cheat_sheet, rms_isf, lc_vs_ring,
equation_index, claims_cross_reference, lab_03, lab_09, lab_17, references.

## D5 — close stale "⚠️ 常數待查" on Γrms ∝ N^(−3/4)
[P2] Eq.(16), p.794 is verified (√(2π²/(3η³))·N^(−3/4), η≈1). Remove "⚠️ 常數待查" and cite
"[P2] Eq.(16), p.794（已核實）". Remaining on: lab_03, lab_11, worked_examples (≈636,654).

## D6 — QVCO I/Q phase-error Q-dependence is INVERTED (quadrature_and_coupled_oscillators.md)
The Adler-consistent result is Δφ_IQ ∝ (Q/m)·(Δω₀/ω₀), i.e. higher Q → LARGER residual I/Q error (narrower
lock range ω_L=(ω₀/2Q)·m → harder to pull into quadrature); stronger coupling m → smaller error. The page
currently has 1/(mQ) (inverted) and the wrong prose "Q 越大誤差越小".
- Replace the formula with Δφ_IQ ≈ (Q/m)·(Δω₀/ω₀) (order; external/Andreani — mark 外部文獻).
- Fix the prose to "Q 越大（lock range 越窄）I/Q 誤差越大；耦合 m 越強誤差越小".
- Recompute the numeric example with a realistic mismatch, e.g. m=0.3, Q=10, Δω₀/ω₀=0.1% ⇒
  Δφ_IQ≈(10/0.3)(0.001)≈0.033 rad≈1.9°. Keep the dimension check.

## D7 — garbled-math / homoglyph REGRESSIONS (visible breakage — top priority)
- psd_phase_noise_jitter.md ≈line 357: delete the dangling "=T^4\,\omega_0^{?}\ \cdots" scratch term (no ω₀
  belongs; the next line is correct). ≈line 480: fix the "\text{Hz}^{?}" units placeholder.
- lorentzian_linewidth.md ≈line 233: delete the broken duplicate block ending "\cdot\frac{1}{?}$$"; the
  correct standard integral (=π) follows immediately.
- real_oscillator_topologies.md ≈line 121: fix "\sqrt{\tfrac12(c_0/ \text{...})}" placeholder to the actual
  Γrms_eff value used consistently on the page.
- symmetry.md ≈line 151: fix the Cyrillic homoglyph "топology" → "topology".
- quadrature_and_coupled_oscillators.md ≈line 218: complete the dangling "（功率 ×N² 除以 …）" parenthetical.

## D8 — page-local correctness (see _ROUND2_FINDINGS.md for the exact quote+fix per file)
white_noise_to_phase_noise (2nω₀→nω₀ in the down-conversion summary), dsp_view_of_phase_noise (the code uses
apply_isf_weighting which does NOT integrate — add the cumsum·dt step; fix the wrong script filename
lab_06_white_noise_to_phase_noise.py → lab_06_white_noise_phase_noise.py), device_noise_mapping
(effective_isf(gamma, 0.5) positional, not alpha=), ltv_htm (Parseval middle term + index/sign slip),
paper_001 (c0/c1 vs c0/Γrms algebra), tank_swing (dimension-check equality), measurement_and_spurs (SA 2.5 dB
correction sign; delay-line H step), pll_noise_budget (H_lp/H_hp values at f=f_n), derivation_leeson (origin
of the leading "2"), real_oscillator_topologies (tail-ISF Γrms consistency), effective_isf (body-toy window
self-contradiction + 7 dB baseline + half-applied "已補上" sentence), capstone (station-⑤ still says −148 vs
its own derived value; Parseval cell), paper_002 (Fig.5 table row page+content), paper_003 (Adler "Sec. II"
attribution; Fig.6 page), lti_vs_ltv (slope heuristic direction), convolution_derivation (note the −636619 rad
is the half-period transient, not steady state), exercises pages (Ex1 consistency; garbled dimension checks).
