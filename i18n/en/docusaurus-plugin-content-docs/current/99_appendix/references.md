---
title: References
description: Full citations for the 5 source PDFs [P1]-[P5], plus external supplementary literature (Leeson 1966, Demir PPV 2000, Kaertner — explicitly flagged as not in the download folder), with citation conventions and a TODO list for manual verification.
---

> **β**: This English translation is in beta — the Traditional-Chinese original is the authoritative version.

# References

> **See also**: [glossary](/99_appendix/glossary) (terminology intuition), [equation_index](/01_paper_map/equation_index) (equation ↔ page-number index); external literature is used in [derivation_leeson](/99_appendix/derivation_leeson) ([E1]) and [derivation_floquet_ppv](/99_appendix/derivation_floquet_ppv) ([E2], [E3])

Every formula and conclusion on this site is tagged with its source. This page collects: **(A)** the 5 PDFs in the download folder (site-internal citation codes
`[P1]`–`[P5]`, citation strings copied **verbatim** from Section 1 of the author's spec), **(B)** external supplementary literature that comes up in teaching but is **not in the download folder**,
and **(C)** citation conventions plus a TODO list of items still awaiting manual verification.

> **Honesty principle**: the formulas in [P1]–[P4] have all been **verified verbatim** against the original PDF rendering; for external literature [E1]–[E4] (flagged as **not
> among the 5 downloaded PDFs**), the volume/issue/page/DOI have been verified online, but the internal formulas of those papers are background only. [P5] is unrelated to the ISF.

---

## A. Core literature (the 5 PDFs in the download folder)

### [P1] — the foundational paper of ISF theory

A. Hajimiri and T. H. Lee, *"A General Theory of Phase Noise in Electrical Oscillators,"*
IEEE J. Solid-State Circuits, vol. 33, no. 2, pp. 179–194, Feb. 1998.
(file `general.pdf`, `paper_001`)

- **One-line contribution**: establishes the view that an oscillator's response to noise is **LTV (linear time-variant)** rather than LTI, introduces the ISF
  $\Gamma(\omega_0\tau)$ and $q_{max}$ normalization, and derives closed forms and design rules for $1/f^2$ and $1/f^3$.
- **Used on this site in**: [impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift),
  [isf_definition](/03_isf_core_theory/isf_definition),
  [convolution_derivation](/03_isf_core_theory/convolution_derivation),
  [fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf),
  [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise),
  [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion).
- **Key equations**: Eqs.(1),(9),(10),(11),(12),(13),(15)–(24), pp.181–185 (see [equation_index](/01_paper_map/equation_index)).

### [P2] — extension to the ring oscillator

A. Hajimiri, S. Limotyrakis, and T. H. Lee, *"Jitter and Phase Noise in Ring Oscillators,"*
IEEE J. Solid-State Circuits, vol. 34, no. 6, pp. 790–804, Jun. 1999.
(file `jitter_ring.pdf`, `paper_002`)

- **One-line contribution**: applies the ISF framework to the ring oscillator, giving closed forms for jitter/phase noise,
  the $\Gamma_{rms}\propto N^{-3/2}$ scaling, and the conclusion that "at fixed power and frequency, single-ended ring phase noise
  is nearly independent of stage count $N$."
- **Used on this site in**: [lab_03](/04_simulation_labs/lab_03_ring_oscillator_toy_model),
  [lc_vs_ring](/06_design_insights/lc_vs_ring), [symmetry](/06_design_insights/symmetry).
- **Key equations (verified)**: Eq.(8) $\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$ p.792, Eq.(12) $\kappa=\frac{\Gamma_{rms}}{q_{max}}\sqrt{\tfrac12\tfrac{\overline{i_n^2}}{\Delta f}}$ p.793,
  Eq.(15) $f_0=1/(2N\tau_D)$ (Eq.(14) is the normalized stage delay $\hat t_D$),
  Eq.(16) $\Gamma_{rms}=\sqrt{\dfrac{2\pi^2}{3\eta^3}}\;\dfrac{1}{N^{1.5}}$ p.794
  (re-verified in v7: the square root covers only the constant, $\Gamma_{rms}\propto N^{-3/2}$; triple-checked against the body-text $4/N^{1.5}$@$\eta=0.75$ and App.B Eq.(55),
  at $\eta=0.75$ this is $\approx4/N^{1.5}$, matching the solid line in [P2] Fig.8; v3 had mis-read this as $N^{-3/4}$),
  Eq.(23) FOM $\frac{8}{3\eta}\frac{kT}{P}\frac{V_{DD}}{V_{char}}(f_0/\Delta f)^2$ p.796 ($\eta$ is the stage-delay proportionality constant from Eq.(14), $\approx 1$; $\gamma$ enters only through $V_{char}=\Delta V/\gamma$. v2 had mis-edited the leading coefficient to $8/(3\gamma)$; v3 corrected it against the original PDF p.796).

### [P3] — injection locking (advanced)

B. Hong and A. Hajimiri, *"A General Theory of Injection Locking and Pulling in Electrical
Oscillators—Part I: Time-Synchronous Modeling and Injection Waveform Design,"*
IEEE J. Solid-State Circuits, vol. 54, no. 8, pp. 2109–2121, Aug. 2019.
(file `BHongGenTheor-I_JSSC2019_Postprint.pdf`, `paper_003`)

- **One-line contribution**: builds a time-synchronous theory of injection locking/pulling using the ISF,
  generalizing Adler 1946 to arbitrary oscillators and arbitrary injection waveforms.
- **Used on this site in**: [paper_003_injection_locking_part1](/05_paper_deep_dives/paper_003_injection_locking_part1).
- **Key equations (verified)**: $\tilde\Gamma=\Gamma/q_{max}$ (Eq.26); the generalized Adler equation
  $\frac{d\theta}{dt}=(\omega_0-\omega_{inj})+\Omega(\theta)$, $\Omega(\theta)=\frac{1}{T_{osc}}\int\tilde\Gamma(\omega_0 t+\theta)i_{inj}\,dt$ (Eq.33);
  lock range $\omega_L=\frac12 I_{inj}\lvert\tilde\Gamma_1\rvert$ (Eq.35), pp.2113–2114.

### [P4] — APF / advanced

B. Hong and A. Hajimiri, *"...Part II: Amplitude Modulation in LC Oscillators, Transient
Behavior, and Frequency Division,"* IEEE J. Solid-State Circuits, vol. 54, no. 8,
pp. 2122–2139, Aug. 2019.
(file `BHongGenTheor-II_JSSC2019_Postprint.pdf`, `paper_004`)

- **One-line contribution**: introduces the **APF (Amplitude Perturbation Function)** — the amplitude-domain
  counterpart of the ISF (units 1/A), covering amplitude modulation under injection, transient locking, and injection-locked frequency division in LC oscillators.
- **Used on this site in**: [paper_004_injection_locking_part2](/05_paper_deep_dives/paper_004_injection_locking_part2),
  [phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise) (uses its ISF/APF quadrature diagram to explain why amplitude perturbations decay).
- **Key equations (verified)**: APF decomposition $D(\tau,\phi)=\tilde\Lambda(\phi)\,d(\tau,\phi)$ (Eq.18); APF definition
  $\Delta(\phi):=\int_0^\infty D\,d\tau$ (units 1/A, Eq.19); amplitude change (Eq.20); augmented pulling equation
  (Eq.21, sinusoidal form Eq.22), all in Fig.5, p.2126; ideal-LC quadrature (ISF fundamental $\angle90°$, APF fundamental $\angle0°$)
  $\tilde\Gamma_1=\frac{1}{q_{max}}\angle90°$, $\tilde\Lambda_1=\frac{\tau_0}{q_{max}}\angle0°$ (Eq.26), p.2128;
  amplitude decay $d(t,\phi)=e^{-t/\tau_0}$, $\tau_0=2Q/\omega_{osc}$ in the same ideal-LC section, p.2127–2128.

### [P5] — unrelated to the ISF (honesty note)

A. Hajimiri and R. Heald, *"Design Issues in Cross-Coupled Inverter Sense Amplifier,"*
Proc. IEEE ISCAS, 1998.
(file `Hajimiri_ISCS_98.pdf`, `paper_005`)

- **Honesty note**: this is a paper on **cross-coupled-inverter sense amplifiers**,
  on the topic of regeneration speed and mismatch offset — **unrelated to oscillator phase noise / the ISF**.
  It appears in the download folder only because it shares an author (Hajimiri).
- **The only conceptual link**: the cross-coupled-pair's **regeneration / positive feedback** mechanism, which is also the underlying mechanism for startup in latch-type and LC oscillators —
  this site uses it only as a peripheral note and does not draw any ISF formula from it (corresponds to claim C12).
- **Key equations**: `TODO: equations not transcribed because this PDF is unrelated to ISF/phase noise.`

---

## B. External supplementary literature (**not among the 5 downloaded PDFs**)

The following literature comes up in teaching but is **not in the download folder**. **Volume/issue/pages/DOI have been verified online**; but for these
papers' **internal** formulas this site provides background only, without re-deriving them verbatim.

### [E1] Leeson 1966 — empirical phase-noise model (for comparison)

D. B. Leeson, *"A Simple Model of Feedback Oscillator Noise Spectrum,"*
Proc. IEEE, vol. 54, no. 2, pp. 329–330, Feb. 1966. **DOI: 10.1109/PROC.1966.4682**.

- **Role**: the most widely used **empirical** phase-noise model before ISF theory; [P1]'s introduction treats it as "the special case that ISF theory subsumes
  and surpasses." For the comparison and derivation see [derivation_leeson](/99_appendix/derivation_leeson):

$$
\mathcal{L}(\Delta\omega)=10\log_{10}\!\left[\frac{2FkT}{P_s}\left(1+\left(\frac{\omega_0}{2Q\,\Delta\omega}\right)^2\right)\left(1+\frac{\omega_{1/f^3}}{|\Delta\omega|}\right)\right].
$$

- **Status**: volume/issue/pages/DOI **verified**; $F$ (noise figure) is an empirically fitted parameter (varies slightly by implementation), used here for comparison only.

### [E2] Demir–Mehrotra–Roychowdhury 2000 — PPV (rigorizing the ISF)

A. Demir, A. Mehrotra, and J. Roychowdhury, *"Phase Noise in Oscillators: A Unifying Theory
and Numerical Methods for Characterization,"* IEEE Trans. Circuits Syst. I: Fundam. Theory
Appl., vol. 47, no. 5, pp. 655–674, May 2000. **DOI: 10.1109/81.847872**.

- **Role**: using the **PPV (Perturbation Projection Vector)** and a nonlinear phase equation, gives the ISF
  a rigorous mathematical foundation (the PPV is the first principal Floquet vector, obtainable numerically via the adjoint). Background equation:
  $\dot{\phi}(t)=v_1^T(t)\,B(t)\,\xi(t)$.
- **Status**: volume/issue/pages/DOI **verified**; the PPV framework is detailed in [derivation_floquet_ppv](/99_appendix/derivation_floquet_ppv).

### [E3] Kärtner 1990 — perturbation analysis of oscillator noise (background)

F. X. Kärtner, *"Analysis of White and $f^{-\alpha}$ Noise in Oscillators,"*
Int. J. Circuit Theory Appl., vol. 18, no. 5, pp. 485–519, 1990. **DOI: 10.1002/cta.4490180505**.

- **Role**: one of the perturbation analyses of oscillator noise predating [P1], often listed alongside Demir as a "mathematical precursor of the ISF/PPV."
- **Status**: volume/issue/pages/DOI **verified**; mentioned on this site as background only.

### [E4] Adler 1946 — the original injection-locking paper (the target of [P3]'s generalization)

R. Adler, *"A Study of Locking Phenomena in Oscillators,"* Proc. IRE, vol. 34, no. 6,
pp. 351–357, Jun. 1946. **DOI: 10.1109/JRPROC.1946.229930**. (Reprinted in Proc. IEEE, vol. 61, no. 10, pp. 1380–1385, Oct. 1973.)

- **Role**: the original source of the classical Adler equation; [P3] generalizes it to arbitrary oscillators / arbitrary injection waveforms.
- **Status**: volume/issue/pages **verified**; the classical and generalized Adler equations appear in
  [paper_003](/05_paper_deep_dives/paper_003_injection_locking_part1).

### [E5] Zadeh 1950 — frequency-domain analysis of linear time-variant systems (the source of the HTM)

L. A. Zadeh, *"Frequency Analysis of Variable Networks,"* Proc. IRE, vol. 38, no. 3,
pp. 291–299, Mar. 1950. **DOI: 10.1109/JRPROC.1950.231083**.

- **Role**: defines the time-variant transfer function $H(f,t)$ (system function), the source of the harmonic transfer matrix and of the
  strict LTV view that "the ISF is the vector that maps phase output onto each harmonic."
- **Status**: volume/issue/pages/DOI **verified**; the framework appears in [ltv_htm](/99_appendix/ltv_htm) (**not among the 5 PDFs**).

---

## C. Citation conventions

1. **Site-internal citation format**: inline usage like `[P1] Eq.(21), p.185`; every definition/formula/conclusion/figure
   drawn from a paper is tagged with its source (see Section 1 of the author's spec).
2. **Codes**: the core 5 papers use `[P1]`–`[P5]` (corresponding to `paper_001`–`paper_005`); external supplements use `[E1]`–`[E3]`,
   and always carry the note "**not among the 5 downloaded PDFs**."
3. **LaTeX sources**: the formula LaTeX in [P1] has been confirmed against the PDF rendering pages (`manual_verification_needed=false`);
   some constants/forms in [P2]–[P4] are flagged ⚠️, see the TODO below.
4. **Units and notation**: consistently follows [notation](/00_overview/notation) site-wide.

---

## D. TODO list awaiting manual verification

After the v3/v4 audit, **all of [P1]; the [P2] ring constants (Eqs.8/12/14/16/17/21/23, where the leading coefficient of Eq.(23) was corrected in v3 from the mis-transcribed
$8/(3\gamma)$ to $8/(3\eta)$ and re-verified; Eq.(16) was re-verified in v7, see the table below); the [P3] generalized Adler equations (Eqs.26/30/33/34/35);
and [P4]'s APF (correctly numbered as Eqs.(18)–(22) + Fig.5, p.2126; ideal-LC quadrature Eq.(26), p.2128) have all been verified verbatim** against the original
PDF rendering; for external literature, **[E1]–[E5]'s volume/issue/pages/DOI have been verified online**, and the design-related external citations
(Hegazi-Sjöland-Abidi JSSC 2001, Andreani JSSC 2002/2005, Romanò TCAS-I 2006, Behbahani JSSC 2001)
have likewise had their volume/issue/pages verified. Only the following minor items remain:

| Item | Content | Source | Nature |
|---|---|---|---|
| Re-verified (v7) | [P2] Eq.(16), p.794 (re-verified in v7: the square root covers only the constant, $\Gamma_{rms}\propto N^{-3/2}$; triple-checked against the body-text $4/N^{1.5}$@$\eta=0.75$ and App.B Eq.(55). v3 had mis-read this as $N^{-3/4}$) | p.794 | Corrected (square-root scope had been mis-read) |
| Verified | [P2] Fig.17 (phase noise vs. symmetry voltage, y-axis = $1/f^3$ corner frequency, drops sharply at the symmetry point) | p.802 | Minor (figure detail, verified) |
| `TODO` | Stage-allocation details of [P4]'s dual-modulus prescaler | Sec. VIII, p.2135 | Minor (advanced circuit) |
| Note | The **internal** formulas of [E1]–[E4] are background only, not re-derived verbatim (volume/issue/DOI verified) | External | Background |
| Note | [P5]'s sense-amplifier formulas are deliberately not transcribed (unrelated to the ISF) | — | Honesty note |

> **Factor-of-2 reminder**: [P1] Eq.(21) writes the denominator as $4\Delta\omega^2$, while a clean time-domain derivation gives $2\Delta\omega^2$;
> the factor-of-2 difference is an SSB accounting convention (a well-known minor point of contention in the literature), **not** a citation error; see
> [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) for details.

## Further reading

- Formula → derivation page → source: [equation_index](/01_paper_map/equation_index)
- Claims and cross-references: [claims_cross_reference](/01_paper_map/claims_cross_reference)
- Glossary: [glossary](/99_appendix/glossary)
- Math toolbox: [math_identities](/99_appendix/math_identities)
