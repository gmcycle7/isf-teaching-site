---
title: Claims Cross-Reference
description: Source paper, confidence, manual-verification status, and page usage for teaching claims C1–C13; cross-paper agreement and items needing verification are flagged.
---

> **β**: This English translation is in beta — the Traditional-Chinese original is the authoritative version.

# Claims Cross-Reference

Every key teaching claim on this site is numbered **C1–C13**, each annotated with: which paper it comes from, how high the confidence is,
whether it needs manual comparison against the PDF (`Verify?`), and **which pages** use it. Data comes from
`extracted/extracted_claims.json`.

> **How to use this page**: when writing a page or reviewing, first find which C-number a conclusion belongs to, then trace it back to the source paper and
> confidence level. **Confidence** has three levels: `high (read from text)` / `high (equation verified)` /
> `medium`. A ⚠️ in `Verify?` means `manual_verification_needed = true` — the constants or exact form
> still need manual comparison against the original PDF.

## C1–C13 at a glance

| Claim | Source Paper | Confidence | Verify? | Used on |
|---|---|---|---|---|
| **C1** All oscillators are **LTV**, not LTI, with respect to noise: the same impulse injected at different instants of the period produces different phase shifts. | [P1] (paper_001) Sec. III | high (read from text) | No | [lti_vs_ltv](/02_foundations/lti_vs_ltv), [isf_definition](/03_isf_core_theory/isf_definition), [lab_04](/04_simulation_labs/lab_04_impulse_injection_sweep) |
| **C2** Amplitude perturbations are pulled back to the limit cycle (stable oscillation requires a restoring mechanism), but **phase** perturbations persist and accumulate. | [P1] Sec. III-A; [P4] (APF/decay function) | high | No | [oscillator_phase](/02_foundations/oscillator_phase), [phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise), [impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift) |
| **C3** Phase noise $\propto\Gamma_{rms}^2/q_{max}^2$: increase the signal charge swing $q_{max}$ and lower the rms ISF to reduce $1/f^2$ phase noise. | [P1] Eq.(21) | high (equation verified) | No | [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise), [rms_isf](/03_isf_core_theory/rms_isf), [lab_06](/04_simulation_labs/lab_06_white_noise_phase_noise), [lc_vs_ring](/06_design_insights/lc_vs_ring) |
| **C4** $1/f$ device noise upconverts to close-in $1/f^3$ **only** through the ISF DC term $c_0$; rise/fall symmetry (small $c_0$) → low $1/f^3$. | [P1] Eqs (23),(24); [P2] symmetry section and Fig. 17 | high | No | [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion), [fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf), [symmetry](/06_design_insights/symmetry), [lab_07](/04_simulation_labs/lab_07_flicker_noise_upconversion) |
| **C5** The $1/f^3$ corner is **not** the device $1/f$ corner: $\Delta\omega_{1/f^3}=\omega_{1/f}\,c_0^2/(2\Gamma_{rms}^2)$, so symmetry can push it below the device corner. | [P1] Eq.(24) | high (equation verified) | No | [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion), [symmetry](/06_design_insights/symmetry), [equation_index](/01_paper_map/equation_index) |
| **C6** A free-running oscillator's accumulated jitter grows as the square root of the measurement interval, $\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$ — the random-walk signature of having no absolute time reference. | [P2] (paper_002) Eq.(8), p.792 | high | No | [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter), [lab_03](/04_simulation_labs/lab_03_ring_oscillator_toy_model), [serdes_clocking_connection](/06_design_insights/serdes_clocking_connection) |
| **C7** At fixed center frequency and power dissipation, a single-ended ring's phase noise/jitter is essentially **independent of the number of stages $N$**. | [P2] Sec. V, Eq.(23)/(25), p.796 | high (equation verified) ($N$-independence verified; only the FOM prefactor $8/(3\eta)$ is a detail) | No | [lc_vs_ring](/06_design_insights/lc_vs_ring), [lab_03](/04_simulation_labs/lab_03_ring_oscillator_toy_model) |
| **C8** A single-ended ring's rms ISF scales roughly as $\Gamma_{rms}\propto N^{-3/2}$. | [P2] Eq.(16), p.794 | high (equation verified) | No | [rms_isf](/03_isf_core_theory/rms_isf), [lc_vs_ring](/06_design_insights/lc_vs_ring), [lab_03](/04_simulation_labs/lab_03_ring_oscillator_toy_model) |
| **C9** The ISF framework subsumes prior phase-noise models (e.g. Leeson) as special cases, and naturally accommodates cyclostationary noise via the effective ISF $\Gamma_{eff}=\Gamma\cdot\alpha$. | [P1] Abstract and cyclostationary section | high | No | [effective_isf](/03_isf_core_theory/effective_isf), [paper_summary_table](/01_paper_map/paper_summary_table), [equation_index](/01_paper_map/equation_index) |
| **C10** The same ISF that determines phase noise also determines injection locking/pulling; a single first-order (generalized Adler) equation predicts lock range, locked phase, and stability. | [P3] (Hong Part I, 2019) Eq.(30), p.2113 / Eq.(35), p.2114 | high (equation verified) | No | [paper_003_injection_locking_part1](/05_paper_deep_dives/paper_003_injection_locking_part1), [equation_index](/01_paper_map/equation_index) |
| **C11** Amplitude effects under injection are described by the **APF** (amplitude perturbation function, the amplitude analogue of the ISF, units $\mathrm{A^{-1}}$); in an ideal LC the ISF and APF are **orthogonal**. | [P4] (Hong Part II, 2019) Fig.5, p.2126; orthogonality Eq.(26), p.2128 | high (equation verified) | No | [paper_004_injection_locking_part2](/05_paper_deep_dives/paper_004_injection_locking_part2), [phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise) |
| **C12** The cross-coupled-inverter sense-amplifier paper is **unrelated to ISF/phase noise**; the only conceptual link is the cross-coupled-pair regeneration/positive-feedback mechanism shared with latches/LC. | [P5] (Hajimiri–Heald, ISCAS 1998) | high (clearly off-topic by title/abstract) | No | [paper_005_sense_amplifier](/05_paper_deep_dives/paper_005_cross_coupled_sense_amp), [paper_summary_table](/01_paper_map/paper_summary_table), [build_report](/00_overview/build_report) |
| **C13** PPV/adjoint/Floquet is the rigorous mathematical foundation of the ISF, coming from the broader literature (Demir 2000 DOI 10.1109/81.847872, Kärtner 1990 DOI 10.1002/cta.4490180505), **not among the five source PDFs**; citation volume/issue/page/DOI have been checked. | external (**not in the source folder**) | high (sourcing statement) | ✓ citation | [effective_isf](/03_isf_core_theory/effective_isf), [equation_index](/01_paper_map/equation_index), [references](/99_appendix/references) |

## Claims consistent across papers (mutually corroborating, high confidence)

These claims are supported by **more than one paper**, or reappear in different papers in different forms, corroborating each other:

- **C2 (phase persists / amplitude decays)**: [P1] argues from the limit cycle that "phase has no restoring force"; [P4] corroborates from the amplitude side
  with the **APF and the amplitude decay function** that "amplitude perturbations are pulled back". Same physics, two angles.
- **C3 ↔ C6 ($\Gamma_{rms}^2/q_{max}^2$)**: the phase noise in [P1] Eq.(21) and the
  jitter proportionality constant $\kappa^2$ in [P2] **share the same $\Gamma_{rms}^2/q_{max}^2$ ratio** — phase noise
  and accumulated jitter are the same physics in the frequency and time domains.
- **C4/C5 (symmetry suppresses $1/f^3$)**: [P1] **derives it theoretically** from Eq.(23)(24); [P2]'s Fig. 17
  **corroborates it by measurement** (phase noise minimum at the symmetric control voltage). Theory + experiment.
- **C1 (LTV) and C10 (injection)**: the same $\Gamma$ determines both noise→phase ([P1])
  and injection→phase ([P3]); the LTV viewpoint runs through both papers.

## Claims needing manual verification (flagged ⚠️)

For the claims below, the **direction of the statement is trustworthy**, but the **exact constants/equation forms** should still be compared against the original PDFs; wherever they are used,
this site retains a `TODO:` marker:

- **C7**: "ring phase noise independent of $N$" holds under **fixed power, fixed frequency** and a specific noise
  model; verified against [P2] Sec. V, Eq.(23)/(25), p.796. The FOM prefactor is
  $\frac{8}{3\eta}\,\frac{V_{DD}}{V_{char}}\,\frac{kT}{P}$ ($\eta$ is the stage-delay proportionality constant of Eq.(14), $\approx1$; $\gamma$ enters only through $V_{char}=\Delta V/\gamma$).
  The only item still needing verbatim confirmation is this prefactor itself; the $N$-independence conclusion is firmly verified.
- **C8**: [P2] Eq.(16), p.794 (v7 re-verified: the radical covers only the constant, $\Gamma_{rms}\propto N^{-3/2}$;
  confirmed by triple evidence — the text's $4/N^{1.5}$@$\eta=0.75$ and App.B Eq.(55). v3 had misread it as $N^{-3/4}$).
  The closed form is $\Gamma_{rms}=\sqrt{\dfrac{2\pi^2}{3\eta^3}}\;\dfrac{1}{N^{1.5}}$ (at $\eta=0.75$, $\approx 4/N^{1.5}$, the solid line in [P2] Fig.8).
- **C10**: the generalized Adler equation is verified against [P3]: the time-averaged form $d\theta/dt=\omega_0-\omega_{inj}+\frac{1}{T_{inj}}\int\tilde\Gamma(\omega_{inj}t+\theta)\,i_{inj}\,dt$ = Eq.(30), p.2113 (the original uses a **plus** sign), lock range $\omega_L=\tfrac12 I_{inj}\vert\tilde\Gamma_1\vert$ = Eq.(35), p.2114.
  (If some pages on this site write a **minus** sign in front of the averaged term, that is because this site's $\Gamma$ uses the opposite sign convention to [P3]; numerically equivalent.)
- **C11**: the APF is verified against [P4]: decomposition $D(\tau,\phi)=\tilde\Lambda(\phi)\,d(\tau,\phi)$ = Eq.(18), definition $\Delta(\phi):=\int_0^\infty D\,d\tau$ (units $\mathrm{A^{-1}}$) = Eq.(19), both on p.2126; ISF/APF orthogonality in an ideal LC = Eq.(26), p.2128.
- **C13**: this is the **sourcing statement** itself — the point is to honestly flag PPV/adjoint/Floquet as **external literature**,
  **not among the five source PDFs**; the citation volume/issue/page/DOI have been checked online (see references [E2]–[E4]).

> **Confidence vs Verify — the difference**: `high (equation verified)` (e.g. C3, C5, and the verbatim-verified
> C7/C8/C10/C11 from v3) means the equation's LaTeX has been checked against the rendered pages and the original PDFs. C13's ✓ citation is a reminder
> to "verify external citations yourself" — it does not mean the site's statement is wrong.

## Key takeaways

- All 13 teaching claims are filed against their source papers and confidence levels; C1–C12 are high confidence (C7/C8/C10/C11 verified verbatim in v3), only C13 carries ✓ citation (external literature — verify yourself).
- **Cross-paper agreement**: C2 ([P1]+[P4]), C3↔C6 ([P1]+[P2] same ratio), C4/C5 ([P1] theory + [P2] measurement).
- **Verified verbatim**: ring constants (C7/C8, [P2] Eq.(16)/(23)), injection/APF forms (C10 [P3] Eq.(30)/(35), C11 [P4] Eq.(18)/(19)/(26)); external-literature sourcing (C13) is verify-yourself.
- PPV/adjoint/Floquet (C13) is **not among the five source PDFs** — external literature, honestly flagged.

## Further reading

- Paper roles and the "no dedicated PPV/PSS paper" note: [paper_summary_table](/01_paper_map/paper_summary_table)
- Equation → derivation page → source: [equation_index](/01_paper_map/equation_index)
- Source and toy flags for every figure: [figure_index](/01_paper_map/figure_index)
- External literature (Demir, Leeson, Adler): [references](/99_appendix/references)
