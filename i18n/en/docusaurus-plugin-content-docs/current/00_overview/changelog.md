---
title: Changelog
description: Full version-history record from v1 to v8, including what was added, correction incidents, and audit details in each version.
---

> **β**: This English translation is in beta — the Traditional-Chinese original is the authoritative version.

# Changelog

This page preserves, in full, the version-by-version history that used to live in
[build_report](/00_overview/build_report) (v1→v8, including audit processes, correction
incidents, and deployment notes). If you only want the **current** site state and honesty
principles, see [build_report](/00_overview/build_report); this page is for readers who want to
trace how a particular number or equation evolved over time.

Newest version first.

---

## v10: Subharmonic injection, the injection/frequency-conversion mini-chapter, growth-debt payoff

**Rollback points**: `v9-stable` (`ab33656`) / branch `backup/v9-stable` / v9 live gh-pages `0bd6af7b4`; intermediate `v10-w1-partial` (`dd35ce7`).

- **Subharmonic injection (headline)**: [subharmonic_injection](/06_design_insights/subharmonic_injection) — from [P3] p.2112 (impulse train every M periods = subharmonic locking, transcribed verbatim) and [P4] Eq.(28)–(30): only the N-th harmonic of the injection waveform couples to the ISF fundamental ($\omega_L=\tfrac12\lvert I_N\rvert\lvert\tilde\Gamma_1\rvert$) ⇒ **a pure sub-harmonic sinusoid does not lock to first order**; impulse-train route $\Delta\omega_L\propto1/N$; realignment factor $\beta=-q_{inj}\tilde\Gamma'(\theta_{ss})$; discrete-time noise loop, corner, closed-form output jitter (MC ratio 0.999); ILCM vs PLL vs sub-sampling table. Two brief assumptions corrected honestly: the ring's edge comes from $q_{max}$ (×100), not ISF slope; no interior optimum in N at fixed $f_0$ (the real optimum is in β). lab_40 (six experiments: 1/N slope −1.000, pulse train 15/15 locks vs pure sine 0/15, measured β 0.0486 vs 0.0498, spur error ≤0.01 dB) + SubharmonicInjectionExplorer widget.
- **Standalone ILFD page**: [injection_locked_division](/06_design_insights/injection_locked_division) (divider↔multiplier duality; M:N noise corner $\omega_c=N\sqrt{\omega_L^2-\Delta\omega^2}$ = [P4] Eq.(32)).
- **[P4] large-injection model & transients**: [paper_004_large_injection_transient](/05_paper_deep_dives/paper_004_large_injection_transient) + lab_41.
- **Theory map**: [theory_map](/00_overview/theory_map) (236 breadcrumb edges, 56-node mermaid).
- **Growth debt**: chapter 06 regrouped into 3 sub-categories and 3 orphaned sidebar entries restored; print CSS; GitHub Discussions + issue templates; deprecation warning fixed; EN full parity pass over 91 pages (8 fixes).
- **Pagefind evaluation: NO-GO** (Chinese recall ~1% on core terms; report in `scripts/pagefind_integration_patch.md`); current search kept.
- Process note: fable 5 hit 529 overload three times; the S2 page was finished by sonnet from the already-verified simulation; an unquoted `: ` in the EN lab_40 front matter broke the en build again — fixed and now part of the gate.
- Scale: **97 pages × 2 locales, 56 figures, 49 simulations, 21 interactive components, 160 checkable examples (147 auto-pass / 0 errors)**.

## v9: growth-debt payoff + learning path v2 + EN audit + paper finishers (G1–G4)

- equation_index 28→62 rows; figure_index 52→53 figures, zero orphans; cheat_sheet v2; `scripts/update_stats.py` keeps facade stats in sync; build_report slimmed + this changelog split out.
- learning_path 9→12 steps (12-item progress checklist); quizzes 10→33; [final_exam](/04_simulation_labs/final_exam) (10 cross-chapter questions); capstone toolbox pointers.
- EN: 92-file terminology audit (0 real drift; 4 files fixed), 16-page parity spot-check all pass; widget a11y (12 components).
- [P2] Appendix A as a teaching asset (actual location p.802–803); [P1] Fig.29/30 conceptual replica.
- Scale: 92 pages × 2, 53 figures, 46 sims, 20 widgets, 156 examples (145/0/0).

## v8: three enhancement waves (A/B/C/D, all delivered)

**All 23 units delivered** (hard units → fable, mechanical/interactive units → sonnet; every unit
also got its English sibling written in the same pass):

- **Paper-verbatim math (7)**: App.B asymmetric-ISF closed forms Eq.(52)–(57) (lab_33; closed form vs. numeric agree to 1.6e-9; a new corner∝1/N design rule; also caught a 2× DC-bookkeeping convention gap between [P1] Eq.24 and [P2] Eq.7, honestly dual-listed on both pages); [P1] appendix's three ISF-extraction methods Eq.(31)–(38) (a three-way comparison; honestly discloses the closed-form method's O(μ) isochron-shear error); differential-ring degradation with N (Eq.31–35, p.796); [P3] optimal injection waveform Eq.(43)–(45) (Cauchy–Schwarz, lab_39); correlated-supply N·f₀ selection rule Eq.(37)–(38) (lab_34); [P4] M:N subharmonic locking Eq.(28)–(30) (lab_37; c₂=0 means you cannot divide by 2); [P3] impulse-train locking Eq.(19)–(23).
- **Derivations/examples (5)**: flicker ADEV floor = √(2ln2·h₋₁) (rigorous proof that ∫sin⁴u/u³=ln2, plus lab_19 verifying the absolute value); [P2] Fig.16 two-regime jitter (lab_24 Part 5; **found a printing erratum in the paper: ζ=2.5e5 should read 2.5e-5**, confirmed via 6× zoom and honestly flagged); PLL peaking closed form (ζ=0.707→2.09 dB @0.786fₙ) plus the fractional-N ΔΣ third-order term; [P1] Sec.V real-silicon ring fully re-derived numerically (**found the paper's p.191 "58.8 fF" should read fC**); large-angle Bessel sideband ladder plus a multi-source superposition example.
- **Interactivity (8 new bilingual widgets)**: AsymmetricIsfExplorer (2646-combination sweep, 0 NaN), AdlerWashboard (washboard potential plus cycle-slip counting), PullingSpectrumExplorer (built-in radix-2 FFT, ω_b error 0.59% @ r=1.5), HtmFoldingExplorer, DualDiracFitter, EffectiveIsfExplorer, LineshapeExplorer (RBW smearing), AdevLiveExplorer (error bars for finite data).
- **New simulations (6)**: lab_33 asymmetric corner, lab_34 correlated-supply selection rule, lab_35 cross-correlation measurement (floor∝1/√M), lab_36 lock acquisition plus Kramers escape, lab_38 first-principles K_push (2.936 GHz/V, FM sideband ratio 1.002), lab_39 optimal injection.

Site size: **90 pages × 2 locales, 52 figures, 45 simulations, 20 interactive components, 144 checkable examples (133 auto-pass, 0 errors)**.

---

## v7: re-audit of [P2] Eq.(16) ring $\Gamma_{rms}$'s N-scaling (radical-scope misreading fixed)

**Ruling** (triple-locked evidence, verified against high-resolution renders of p.794/p.803): the
correct reading of [P2] Eq.(16) is that the radical **covers only the constant**, i.e.
$\Gamma_{rms}=\sqrt{2\pi^2/(3\eta^3)}\cdot(1/N^{1.5})$, so $\Gamma_{rms}\propto N^{-3/2}$ (not the
$N^{-3/4}$ that v3 mistakenly changed it to). Triple evidence: (1) the paper's body text states
outright "$1/N^{1.5}$ dependence of $\Gamma_{rms}$"; (2) the $\eta=0.75$ numerical anchor — the text
gives the solid line as $\approx4/N^{1.5}$, and plugging in $\sqrt{2\pi^2/(3\cdot0.75^3)}=3.95\approx4$
checks out (if $N^{1.5}$ were inside the radical this would instead give $4/N^{0.75}$, contradicting
the text); (3) App.B Eq.(52)+(54) independently derives $\Gamma_{rms}^2\propto N^{-3}$, consistent
with $N^{-3/2}$. **History**: v1 originally wrote $N^{-3/2}$ (correct); the v3 audit misread the
radical's scope and "corrected" it to $N^{-3/4}$, mislabeling it "verified" — the same type of
misreading as the FOM $8/(3\gamma)$ incident. v7 checked it against the original
text, restored it, and recorded the incident here. All affected
pages site-wide (real_oscillator_topologies, waveform_slope, references, etc.) have had the
exponent and related numbers corrected in step (e.g. the $N{=}5\to15$ ratio changed from $0.4387$ /
$-7.16$ dB to $0.1925$ / $-14.31$ dB). The N-independence of the Eq.(23) FOM, $8/(3\eta)$, $\kappa$,
Eq.(15) $f_0$, and Eq.(17)/(18)/(21) are all unaffected.

---

## v6: interactivity, content, English version, and polish (waves C+D)

- **Interactivity**: 9 instant-graded exercises across three chapters (NumericQuiz); the **impulse→phase animation** on isf_definition (tangential/radial decomposition, ghost reference, Δφ accumulation); the **ISF sandbox** (drag the waveform → live c_n/Γrms/L/corner, slope approximation, sinusoidal anchor verified at −145 dBc/Hz); learning_path progress checkmarks (localStorage); 7 downloadable Jupyter notebooks (all executed and verified with nbclient).
- **Content**: lab_32 **MOS Level-1 equation-level ring** (Shichman–Hodges; impulse-method extraction of the true ISF; Parseval 1.7308 vs 1.7309; energy concentrated in transitions, consistent with [P2]); sampling/sub-sampling PLLs, crystal/MEMS reference sources, a **gallery of common mistakes** (12 entries, all drawn from errors this site actually caught).
- **English β**: en locale + language switcher + UI translation + 7 core pages translated (the rest fall back to Chinese).
- **Polish/bugs**: favicon + logo + og social card; **mobile horizontal-scroll fix** (slider rows flexWrap, measured to zero at 375px); LICENSE (content CC BY-NC-SA 4.0 / code MIT); README, repo topics, editUrl.
- **[P2] p.803 verified verbatim**: Eq.(45)–(51) transcribed; the coefficient 8 in (49) = double-sided spectrum (exactly equivalent to the single-sided 4sin² kernel in jitter_kernels); (50) κ value cross-locks at 2.0×10⁻⁹√s; (51) as printed has no √2 (definition difference noted).
- **Lighthouse baseline** (live site): Performance 89 / Accessibility 93 / SEO 100.
- Honestly rejected (reverted after measurement): zh-only search index (only −2%), lossless PNG re-encoding (+10%).
- Deployment note: the bilingual build is ~200MB; Pages once hung at "building" for 35 minutes, and a rebuild via `POST /pages/builds` finished in 30 seconds — use this trick when a large deployment gets stuck.

---

## v5: theory-deepening wave (12 items) plus one caught factor-2

**v5 added 12 theory units** (8 new pages + 2 expanded pages + 9 new labs + 2 fig scripts); each one
is "a derivation page + a simulation actually run to obtain the numbers before writing the page":

1. **[diffusion_dictionary](/03_isf_core_theory/diffusion_dictionary)**: κ↔D↔linewidth↔ADEV↔S_φ — five representations of the same quantity reconciled in one pass (lab_23: one simulation, four extraction routes, all yielding the same 0.125).
2. **[jitter_kernels](/02_foundations/jitter_kernels)**: TIE / period / cycle-to-cycle kernels (4sin², 16sin⁴) derived from first principles + MC (theory/measured ratio 0.999–1.001); the white-noise closed form exactly reproduces [P2] Eq.(8). **Closes the site's last theory TODO.**
3. **Floquet/PPV made numerical** ([derivation_floquet_ppv](/99_appendix/derivation_floquet_ppv) expanded + lab_25): computed the monodromy (μ₁=1.000000), adjoint-extracted v₁, overlaid with the impulse-method ISF at rms 0.0016 — "PPV=ISF" goes from prose to a computed fact.
4. **[injection_locking_noise](/06_design_insights/injection_locking_noise)** (lab_26/27): locking = first-order PLL (own noise high-passed, reference low-passed, corner=ω_L cosθ_ss) plus the asymmetric beat spectrum under pulling.
5. **Full AM-noise spectrum** ([phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise) expanded + lab_28): OU process → flat-topped Lorentzian (corner=ω₀/2Q).
6. **[beyond_lorentzian](/03_isf_core_theory/beyond_lorentzian)** (lab_29): under flicker the lineshape departs from Lorentzian (near-Gaussian core), plus the non-stationarity point that "a free-running oscillator strictly has no S_φ".
7. **[adc_aperture_jitter](/06_design_insights/adc_aperture_jitter)** (lab_30): SNR=−20log₁₀(2πf·σ_t) derivation plus the ENOB table for 447.9 fs.
8. **[dj_dual_dirac](/06_design_insights/dj_dual_dirac)** (lab_31): dual-Dirac, TJ@BER, and the honest distinction DJ_δδ≤DJ_pp.
9. **[clock_chain_budget](/06_design_insights/clock_chain_budget)**: the four bookkeeping rules for ×N/÷N/PLL/buffer plus a full-chain worked example.
10. **[fom_limit](/06_design_insights/fom_limit)**: FOM ceiling = 173.8−10log₁₀F_eff dB@300K (self-computed and verified, not a memorized value).

> **v5's factor-2 catch**: the jitter_kernels MC cross-check caught **a 2× error in the D mapping of spec item 11.2** — v3 had taken the variance growth rate κ² ([P2] Eq.11) as the diffusion constant D and plugged it into Δf=D/π. Adjudicated by lab_23 and an independent MC + Lorentzian fit (fitted FWHM/κ²·2π=0.992), then **corrected site-wide**: D=Γ²rms·S_i/(4q²max)=κ²/2; representative linewidth 40→**19.9 mHz**, true LC 80→**39.8 mHz**, −100 dBc/Hz anchor 1257→**628 Hz** (lorentzian / capstone / lab_22 / spec 11.2 updated together). Scalings and the −145/−148 dBc/Hz values are unaffected.

---

## v4: deep audit and improvement pass (research-style multi-agent harness)

Round four ran a deep audit and fix pass over the whole site with a "research-style multi-agent
harness", staged with a gate after each stage (`run_all_sims` + `verify_examples` +
`check_site_quality` + `npm run build` + math scan):

1. **WF-1 multi-lens audit**: 7 lenses (correctness / pedagogy / citation / consistency / completeness /
   figure / code) plus page-by-page deep reading, yielding ~45 structured findings.
2. **WF-2 PDF citation verification**: for every citation finding, **the original PDF pages were actually rendered and checked verbatim** (adversarial).
3. **WF-3 fixes**: one owner agent per page applying a unified correction spec; added **3 pages** (varactor tuning / supply pushing,
   quadrature / coupled oscillators, tank Q and energy restoration), **lab_22 end-to-end simulation**, **4 conceptual figures**,
   **3 interactive widgets** (injection-locking Adler, Allan deviation, PLL loop-BW), and site-wide navigation
   (breadcrumbs / further reading / goal-based landing).
4. **WF-4 + round-2/3 re-review**: page-by-page deep reading caught round-1 leftovers and new bugs, then fixed them.

Key outcomes (all verified against the original PDFs):

- **Ring FOM prefactor re-corrected `8/(3γ)→8/(3η)`** (v2 had mis-edited it and mislabeled it "verified verbatim"; γ enters only through
  `V_char=ΔV/γ`); the worked example moved `−89.2→−91.0 dBc/Hz`, 57 dB from ideal LC.
- **`[P4]` ISF/APF figure `Fig.3→Fig.5, p.2126`**; APF definition Eq.(18)–(22), ideal-LC quadrature
  Eq.(26) p.2128 (not the old "Eq.25/26/27" labels).
- Citation page/equation corrections: `Fig.17 p.800→p.802`, `Sec.VIII p.1163→p.2135`, `Fig.4 p.182→p.181`,
  `f₀=1/(2Nτ_D)` citation `Eq.(14)→Eq.(15)` (Eq.14 is actually the normalized stage delay `t̂_D`).
- Closed the closable TODOs: cyclostationary `[P1] Eq.(25)–(27) p.186`, generalized Adler `[P3] Eq.(30)/(35)`,
  Γrms `Eq.(16) p.794`; unified the Chinese term for "cyclostationary" site-wide.
- Code bugs: lab_05 Parseval DC double-counted (`c₀²→c₀²/2`, giving `2Γ²rms` after the fix), `accumulated_jitter_curve`
  broken call signature; lab_06/07/15 gained numerical-consistency metrics; lab_10/20 figure fixes; `verify_examples` regex tightened.
- **Honestly blocked one false fix**: the audit claimed "κ Eq.(12) is missing ω₀"; zooming into the original PDF p.793 confirmed Eq.(12) never
  had ω₀ — κ√Δt is the **phase** jitter `σ_Δφ` (Eq.11), and only the **time** jitter is `÷ω₀` (Eq.10). No blind edit was made.
- External literature now carries CrossRef-verified DOIs: Leeson 1966 (10.1109/PROC.1966.4682), Demir PPV 2000
  (10.1109/81.847872), Kärtner 1990 (10.1002/cta.4490180505), Adler 1946 (10.1109/JRPROC.1946.229930).

**Convergence (loop is dry)**: all substantive findings from 3 audit rounds are handled;
`verify_examples` shows, of 88 verifiable blocks, **73 pass with 0 errors**; the remaining 13 are
verifier false positives on "formula constants / contextual numbers / deliberately blank exercises"
(manually confirmed correct). Final site size: **74 pages, 30 figures, 25 simulation scripts, 6
interactive widgets**; final gate: build green, 0 broken links, 0 KaTeX errors, 0 content issues, 0
soft warnings.

> **Process limitation (honest disclosure)**: WF-4's parallel fix agents repeatedly hit
> **Anthropic-side server throttling** ("not your usage limit", i.e. not an account usage cap), so
> citation-type and mechanical fixes were completed inline instead and verified item by item.

---

## v3: worked-example numerical QA plus ring-constant audit corrections

Added `scripts/verify_examples.py`: it actually runs every Python worked example in docs that has a
"reference answer" (`# ->`) and checks the numbers. **Of 80 verifiable blocks, 65 pass automatically
with 0 errors**; the remaining 14 were manually confirmed correct (the verifier misjudges formula
constants in comments, such as the "2" in $2\Gamma_{rms}^2$, or comparison numbers like "much smaller
than 447.9 fs"). The process fixed real bugs: `np.trapz`→`np.trapezoid` (NumPy 2.0) ×3, a broken
`import` (added `simulations/__init__.py` to make the package importable), and 2 wrong example
numbers (the $c_2$ in effective_isf, and $S_{ref}$ in the PLL optimal-BW example). Also fixed
**dark-mode figures**: matplotlib PNGs get a white card background in dark mode (`.markdown img`
CSS).

**[P2] ring constants were verified verbatim against the original PDF (high-resolution rendering) and corrected**:

- Eq.(23) FOM: the prefactor was mis-edited to $8/(3\gamma)$ (v2 had mislabeled it "verified
  verbatim"); corrected against the original PDF p.796 to $8/(3\eta)$ ($\eta$ is the stage-delay
  proportionality constant of Eq.(14), $\approx 1$; $\gamma$ enters only through
  $V_{char}=\Delta V/\gamma$); the $V_T=0$ lower bound Eq.(25) is $\frac{16\gamma}{3\eta}$.
- Eq.(16) $\Gamma_{rms}$'s N-scaling: at the time, the v3 audit misread the radical's scope and
  "corrected" v1's originally-correct $N^{-3/2}$ to $N^{-3/4}$, mislabeling it "verified" — this
  misreading was not fixed until **v7**, which cross-checked the paper's body text, the numerical
  anchor, and App.B (see the v7 entry above).

**v3 audit corrections (other corrections against the original PDFs)**: the **[P4]** ISF/APF figure
was corrected from Fig. 3 to Fig. 5 (p.2126); citation page numbers corrected: **[P2]** Fig.17
(symmetric-voltage plot) p.802, **[P4]** Sec. VIII p.2135, **[P1]** Fig.4 p.181, $f_0=1/(2N\tau_D)$
now cites Eq.(15); TODOs closed: **[P1]** cyclostationary $i_n(t)=i_{n0}(t)\alpha(\omega_0 t)$,
$\Gamma_{eff}=\Gamma\cdot\alpha$ (Sec. II-D, Eq.(25)–(27), p.186) and the generalized Adler equation
(**[P3]** Eq.(30)/(35)) are both verified; also fixed 2 code bugs: lab_05's Parseval DC term must be
counted as $(c_0/2)^2$, and the `accumulated_jitter_curve` call was missing `f0` / misusing
`max_lag` — both fixed.

**[P3]/[P4] injection & APF equations were likewise verified verbatim against the original PDFs in v3**:

- **[P3]** Eq.(26) $\tilde\Gamma=\Gamma/q_{max}$; generalized Adler Eq.(30),(33)
  $\frac{d\theta}{dt}=(\omega_0-\omega_{inj})+\Omega(\theta)$,
  $\Omega(\theta)=\frac{1}{T_{osc}}\int\tilde\Gamma(\omega_0 t+\theta)i_{inj}dt$; sinusoidal
  degenerate case Eq.(34), lock range Eq.(35) $\omega_L=\frac12 I_{inj}|\tilde\Gamma_1|$.
- **[P4]** amplitude decay $d(t,\phi)=e^{-t/\tau_0}$, $\tau_0=2Q/\omega_{osc}$ (Sec. III-F p.2128 body
  text; Eq.(25) itself is $\Lambda=\tau_0\tilde\Lambda$); Eq.(26) ideal-LC fundamental
  $\tilde\Gamma_1=\frac{1}{q_{max}}\angle90°$, $\tilde\Lambda_1=\frac{\tau_0}{q_{max}}\angle0°$
  (quadrature); Eq.(27) amplitude-corrected Adler.

> **v3 deepening (graduate level)**: added **Lorentzian linewidth** (resolving the 1/f² divergence
> paradox as Δf→0), **Allan variance / ADEV** (time-domain frequency stability), a **rigorous
> spectrum derivation** (cyclostationary autocorrelation → Wiener-Khinchin), a **full PLL noise
> budget + optimal loop BW**, **real-topology ISF** (cross-coupled VCO tail upconversion, Colpitts,
> ring stage), **measurement & spurs**, an **LTV/HTM** appendix, a **Capstone** (ideal LC from state
> equations all the way to BER), plus **problem sets with full solutions for chapters 02/03/06**.
> Accompanied by 4 new simulations (lab_18–21).

---

## v4 addendum: items the audit still flagged TODO

**The v4 deep audit (see the v4 entry above) closed most of them**: [P2] ring constants (FOM
`8/(3η)`, Γrms `Eq.16`), [P3]/[P4] citations and page numbers (generalized Adler `Eq.(30)/(35)`, APF
`Fig.5`/`Eq.(18)–(22)`), cyclostationary `[P1] Eq.(25)–(27)`, external-literature DOIs — all verified
verbatim against the original PDFs. The remaining `TODO`s are mostly **deliberately retained
"external-literature scope" flags** (e.g. period-jitter kernel conventions, standard LC-VCO design
lore) and transistor-level exclusion statements, which do not affect the correctness of the core
theory.

The following remained flagged ⚠️ / `TODO` (external literature or secondary details, not core
ISF/injection physics):

- **External literature (not among the 5 source PDFs)**: formal volume/issue/page numbers for
  Leeson 1966, Demir et al. 2000 (PPV), Kärtner 1990 — volume/issue/page numbers and equation
  notation were checked in v4; the period/cycle-to-cycle jitter kernels were, in **v5**, **derived
  in-house from first principles and Monte-Carlo verified** at
  [jitter_kernels](/02_foundations/jitter_kernels) (no longer relying on external conventions).
- **[P2]** exact axes of the Fig.17 symmetric-voltage plot; **[P4]** stage-allocation details of the dual-modulus prescaler (Sec. VIII).
- **[P5]** (sense amplifier, unrelated to ISF, deliberately not transcribed).
- **[P4]** exact defining equation and Fourier expansion of the APF (Sec. III-D, p.2127); Fig. 3 subplot captions.

---

## v2: step-by-step derivation expansions plus waves A/B/C/D

After the core equations of [P1] (general.pdf) — Eq.(1),(9),(10),(11),(12),(13),(15)–(24) — were all
converted to LaTeX via high-resolution page rendering and manual line-by-line comparison, v2 added
step-by-step algebraic expansions (downconversion integral, factor-8 summation, $\mathcal{L}\approx\frac12 S_\phi$
small-angle PM, jitter high-pass kernel, flicker 1/f³ corner, the three classes of
Parseval terms), plus two derivation appendices (Floquet/PPV, Leeson↔ISF).

Added 8 new simulation figures (`lab_10`–`lab_17`: RF spectrum sidebands, Monte Carlo jitter
histogram, SerDes eye/BER bathtub, PLL/CDR jitter transfer, cyclostationary effective ISF, nonlinear
oscillator ISF, Leeson vs. ISF overlay, design tradeoff sweeps) plus 2 corresponding new util
modules (`pll_utils.py`, `serdes_utils.py`).

**Error introduced in v2** (later corrected in v3/v4, see above): the ring FOM prefactor was at one
point mistakenly changed to $8/(3\gamma)$ and mislabeled "verified verbatim" — the correct value is
$8/(3\eta)$.

`npm run build` succeeded (Docusaurus 3.10.1); historical fixes: two classes of rendering bugs were
fixed — (a) multi-line display-math fences not on their own lines caused micromark to
cascade-swallow subsequent formulas (fixed site-wide with a normalizer, now part of the standard
pipeline); (b) HTML entities (gt/lt entities) misused inside math → replaced with the proper
greater-than/less-than symbols for math.

`python scripts/run_all_sims.py`: **36/36 pass** (29 labs + 7 `fig_*` scripts), producing 41 figures
in `static/figures/` (v4 added 4 more conceptual figures).

---

## v1: initial build

- Scanned the source folder's **5 PDFs** (`scripts/extract_papers.py` scans all of them and dumps
  plain text): paper_001 `general.pdf` ([P1], core foundation), paper_002 `jitter_ring.pdf` ([P2],
  ring extension), paper_003 `BHongGenTheor-I_JSSC2019_Postprint.pdf` ([P3], injection, advanced),
  paper_004 `BHongGenTheor-II_JSSC2019_Postprint.pdf` ([P4], APF, advanced), paper_005
  `Hajimiri_ISCS_98.pdf` ([P5], **unrelated** to ISF, honestly flagged as a cross-coupled
  sense-amplifier paper).
- [P1]'s core equations Eq.(1),(9),(10),(11),(12),(13),(15)–(24) were all converted to LaTeX via
  high-resolution page rendering and manual line-by-line comparison, and used verbatim in the
  teaching pages and `extracted/*.json`.
- All figures are conceptual simulations regenerated in Python (not bitmaps extracted from the
  PDFs), reproducing the mechanisms of [P1]/[P2].
- The vast majority of figures are toy / conceptual models (explicitly flagged as not
  transistor-level). A few purely mathematical figures (jitter integration, Leeson↔ISF overlay,
  design sweeps, PLL transfer, BER bathtub) are computed from formulas and agree with the analytic
  expressions.
- Completed chapters: 00 Overview / 01 Paper Map / 02 Foundations / 03 ISF Core Theory (equations
  verified), 04 Simulation Labs (numerical_feeling, interactive tools, lab_01–08), 05 Paper Deep
  Dives (all 5) / 06 Design Insights / 99 Appendix.
- Eq.(16) $\Gamma_{rms}$'s N-scaling: **v1 originally wrote $N^{-3/2}$ (correct)** — this conclusion
  was later mistakenly changed to $N^{-3/4}$ in v3, and not restored until v7 (see the v3/v7 entries
  above for the full incident record).

---

## After v8: deployment

Publicly deployed as a **GitHub Pages (project page)**:

- Site: `https://gmcycle7.github.io/isf-teaching-site/`
- Source (public): `https://github.com/gmcycle7/isf-teaching-site`
- `baseUrl` set to `/isf-teaching-site/`; KaTeX CSS/fonts bundled via webpack (baseUrl-safe, fully offline).
- Deployment mechanism: local `npm run build`, then push `build/` to the `gh-pages` branch (with `.nojekyll`); Pages serves from that branch.
  Each update is just re-build + force-push `gh-pages` — packaged as the one-click script **`./scripts/deploy.sh`** (needs only `repo`
  scope, no `workflow` scope).
- **Copyright handling**: the full text and PDFs of the 5 papers are **not committed** (`.gitignore` excludes `extracted/raw_text/` and `*.pdf`);
  the footer and each page state that copyright belongs to the original authors and the content is for teaching purposes.
- CI (optional): `.github/workflows/deploy.yml` is ready; pushing the workflow file requires a token with `workflow` scope
  (`gh auth refresh -s workflow`) to enable push-to-deploy.
- The bilingual build is ~200MB; Pages once hung at "building" for 35 minutes, and a rebuild via
  `POST /pages/builds` finished in 30 seconds — use this trick when a large deployment gets stuck
  (recorded in v6).
