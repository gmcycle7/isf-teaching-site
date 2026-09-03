---
title: Paper Summary Table
description: The five source papers on one page — contributions, key equations, key figures, what we teach with each, plus their division of labor from a teaching viewpoint.
---

> **β**: This English translation is in beta — the Traditional-Chinese original is the authoritative version.

# Paper Summary Table

The source folder contains **5 PDFs**. This page lays them out in a single table, then organizes their division of labor from a **teaching viewpoint**:
which paper is the ISF core, which extends to rings, which covers injection, which is actually **off-topic**, and which equations
are the same thing written differently, plus which notation differs and needs to be unified.

> **Honesty note (up front)**: of these 5, 4 are Hajimiri-series oscillator phase-noise/
> injection papers, and **1 (`Hajimiri_ISCS_98.pdf` = [P5]) is actually a cross-coupled
> sense-amplifier paper, unrelated to ISF** — this site treats it only as a footnote. Also, the frequently co-mentioned
> **PPV / adjoint / PSS / PNoise / Floquet** topics have **no** dedicated paper among these 5 PDFs
> — they belong to external literature and are honestly flagged below.

## One-page summary table

Data comes from `extracted/paper_metadata.json`. Citation strings follow the site convention verbatim (see [references](/99_appendix/references)).

| Paper | Year | Main Contribution | Key Equations | Key Figures | What We Use It For |
|---|---|---|---|---|---|
| **[P1]** Hajimiri & Lee, *A General Theory of Phase Noise in Electrical Oscillators*, IEEE JSSC 33(2):179–194 (`general.pdf`, paper_001) | 1998 | Establishes the **LTV / ISF** theory of oscillator noise: introduces $\Gamma(\omega_0\tau)$ and the $q_{max}$ normalization, derives closed forms for $1/f^2$ and $1/f^3$ plus design rules (large $q_{max}$, small $\Gamma_{rms}$, waveform symmetry to suppress $c_0$). | Eq.(1) output decomposition; (9) $\Delta V=\Delta q/C$; (10)(11) ISF impulse response and convolution; (12) Fourier series; (19)(20) summation and Parseval; **(21)** the signature $1/f^2$ formula; (22)(23)(24) flicker $1/f^3$ and corner | Fig. 4 (peak vs ZC injection), Fig. 6 ($\Delta\phi$–$\Delta q$ linearity), Fig. 7 (LC/ring ISF shapes), Fig. 8 ($n\omega_0$→carrier downconversion), Fig. 11/12 ($1/f^3,1/f^2$,floor panorama and corner) | **The ISF core foundation** — the theory source of chapters 02/03 and most labs. |
| **[P2]** Hajimiri, Limotyrakis & Lee, *Jitter and Phase Noise in Ring Oscillators*, IEEE JSSC 34(6):790–804 (`jitter_ring.pdf`, paper_002) | 1999 | Applies the ISF to ring oscillators: closed forms for jitter/phase noise, the $\Gamma_{rms}\propto N^{-3/2}$ scaling, "ring phase noise nearly independent of stage count $N$ at fixed power and frequency", and how rise/fall symmetry suppresses $1/f$ upconversion. | (8) accumulated jitter $\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$; (11)(12) $\kappa^2\propto\Gamma_{rms}^2/q_{max}^2\cdot\overline{i_n^2}/\Delta f$; (15) $f_0=1/(2N\tau_D)$; (16) $\Gamma_{rms}=\sqrt{2\pi^2/(3\eta^3)}\cdot1/N^{1.5}\propto N^{-3/2}$; text result $\mathcal{L}\vert _{1/f^2}\approx\frac{8}{3\eta}\,\frac{V_{DD}}{V_{char}}\,\frac{kT}{P}(\omega_0/\Delta\omega)^2$ ($\eta$ is the stage-delay proportionality constant of Eq.14, $\approx 1$; $\gamma$ enters only through $V_{char}=\Delta V/\gamma$) | Fig. 5 (ring single-stage ISF), Fig. 8 ($\Gamma_{rms}$ vs $N$; solid line is $4/N^{1.5}$@$\eta=0.75$), Fig. 17 (phase noise vs symmetry control voltage, minimum at the symmetric point) | **The ring-oscillator extension** — chapter 06 lc_vs_ring, symmetry, and lab_03. |
| **[P3]** B. Hong & A. Hajimiri, *Injection Locking and Pulling…Part I: Time-Synchronous Modeling and Injection Waveform Design*, IEEE JSSC 54(8):2109–2121 (`BHongGenTheor-I_JSSC2019_Postprint.pdf`, paper_003) | 2019 | Builds a **time-synchronous** injection locking/pulling model on the ISF, generalizing Adler 1946 to **arbitrary oscillators and arbitrary injection waveforms**: a single first-order (generalized Adler) equation predicts lock range, locked phase, and mode stability. | classic Adler $\dot\phi=-\omega_L\sin\phi+\Delta\omega_{inj}$; generalized Adler (time-averaged) $\dot\theta=\omega_0-\omega_{inj}-\frac{1}{q_{max}}\langle\Gamma(\omega_{inj}t+\theta)\,i_{inj}\rangle$ = Eq.(30) (this site's $\Gamma$ uses the sign convention opposite to [P3], hence the $-$ before the averaged term; numerically equivalent, the original PDF Eq.(30) has $+$); sinusoidal lock range $\omega_L=\tfrac{1}{2}I_{inj}\vert\tilde\Gamma_1\vert$ = Eq.(35), p.2114 (verified) | Fig. 1–3 (time-synchronous injection model and ISF formulation) | **Advanced injection-locking deep dive** (chapter 05, elective); demonstrates the same $\Gamma$ extending beyond phase noise. |
| **[P4]** B. Hong & A. Hajimiri, *…Part II: Amplitude Modulation in LC Oscillators, Transient Behavior, and Frequency Division*, IEEE JSSC 54(8):2122–2139 (`BHongGenTheor-II_JSSC2019_Postprint.pdf`, paper_004) | 2019 | Introduces the **APF (amplitude perturbation function)** — the amplitude analogue of the ISF (units $\mathrm{A^{-1}}$): handles amplitude modulation under injection, transient locking, and injection-locked frequency division. In an ideal LC the ISF and APF are orthogonal. | APF definition $\Delta(\phi):=\int_0^\infty D(\tau,\phi)\,d\tau$ (units $\mathrm{A^{-1}}$) = Eq.(19), p.2126 (decomposition $D=\tilde\Lambda(\phi)\,d(\tau,\phi)$ = Eq.(18); ideal-LC orthogonality = Eq.(26), p.2128, verified) | Fig. 5, p.2126 (effect of instantaneous charge injection on the oscillator: ISF / excess phase / amplitude decay / APF; ISF and APF orthogonal in an ideal LC) | **APF / advanced deep dive** (chapter 05, elective); chapter 02's phase_vs_amplitude_noise borrows it to explain "why amplitude noise decays". |
| **[P5]** A. Hajimiri & R. Heald, *Design Issues in Cross-Coupled Inverter Sense Amplifier*, Proc. IEEE ISCAS 1998 (`Hajimiri_ISCS_98.pdf`, paper_005) | 1998 | Analytic design of the cross-coupled-inverter sense amplifier (regeneration speed, mismatch offset, FOM). **Completely unrelated to ISF/phase noise**; included only because it was in the source folder with the same author. | None (off-topic, equations not transcribed) `TODO: equations not transcribed because off-topic` | None | **Footnote** — honestly explains the mislabeling; the only conceptual link is the cross-coupled-pair regeneration/positive-feedback mechanism shared with latches/LC oscillation. |

⚠️ = `manual_verification_needed = true`, exact constants/forms still need comparison against the original PDFs. See
[claims_cross_reference](/01_paper_map/claims_cross_reference) and
[equation_index](/01_paper_map/equation_index) for details.

---

## Teaching viewpoint: who teaches what

### Which paper is the ISF core foundation

**[P1]** is the foundation of the whole site. Every LTV/ISF concept — $\Gamma(\omega_0\tau)$, the $q_{max}$
normalization, the convolutional phase response, Fourier downconversion, the $1/f^2$/$1/f^3$ closed forms — all comes from here.
Chapters 02 (foundations) and 03 (isf core theory) map almost section-by-section to [P1] Secs. III–IV,
and lab_01/02/04/05/06/07 all reproduce figures and equations from [P1].

### Which paper extends to rings

**[P2]** grounds [P1]'s general theory in the **ring oscillator**: the same $\Gamma_{rms}^2/q_{max}^2$
logic yields accumulated jitter (claim **C6**), $\Gamma_{rms}\propto N^{-3/2}$ (claim **C8**),
and "ring phase noise nearly independent of $N$ at fixed power/frequency" (claim **C7**). Chapter 06's
[lc_vs_ring](/06_design_insights/lc_vs_ring), [symmetry](/06_design_insights/symmetry)
and [lab_03](/04_simulation_labs/lab_03_ring_oscillator_toy_model) use it.

### Which paper covers adjoint / PPV / PSS / PNoise / simulation

**Honestly: none of these 5 papers is dedicated to PPV/adjoint/PSS/PNoise.**

- **PPV (perturbation projection vector) / adjoint method / Floquet
  theory** is the rigorous mathematical foundation behind the ISF, but it comes from the **broader literature** (e.g.
  Demir–Mehrotra–Roychowdhury 2000, Kaertner), **not among the 5 downloaded PDFs**. This site treats them
  as **standard external literature**, explicitly flagged in [effective_isf](/03_isf_core_theory/effective_isf)
  (claim **C13**).
- **PSS (periodic steady-state) / PNoise** are numerical methods in commercial simulators (e.g. SpectreRF) for extracting ISF/
  phase noise, and likewise are **not the subject of any of these 5 papers**; this site cites them only conceptually
  and does not claim they come from the downloaded PDFs.
- The closest thing to "simulation" is actually [P1]'s own **limitation** that "real circuits require transient impulse
  response or adjoint/PSS methods to extract the ISF" — i.e., simulation extraction is **mentioned**,
  but has no dedicated paper. All labs on this site are **teaching toy models (not transistor-level)**,
  reproducing the concepts in Python, not a real PSS/PNoise flow.

### Which paper corrects / critiques / extends prior work

**[P1] supersedes Leeson's empirical formula.** Leeson 1966's $\mathcal{L}$ expression (with $2FkT/P_s$,
$(\omega_0/2Q\Delta\omega)^2$, $1+\omega_{1/f^3}/|\Delta\omega|$) is an **empirical fit**: it can draw the
$1/f^3$, $1/f^2$, floor regions, but $F$ (noise factor) and the $1/f^3$ corner are **after-the-fact
fitting parameters**, not computed from first principles. [P1]'s contribution is precisely to **compute** these three regions from first principles with the ISF,
and to point out that **the $1/f^3$ corner is not the device's $1/f$ corner**, but $\omega_{1/f}(c_0/c_1)^2$
([P1] Eq.(24), claim **C5**) — a key correction to the Leeson empirical model. The Leeson formula itself
is **not** one of the 5 downloaded PDFs; this site uses it only for comparison (see
[equation_index](/01_paper_map/equation_index) row 19, flagged reference ⚠️).

In addition, **[P3]** extends/generalizes **Adler 1946**'s injection-locking equation, and **[P4]** supplies the
**amplitude dimension** (APF) missing from [P1]/[P3]. Neither Adler's nor Leeson's original paper is among these 5 PDFs.

### Which equations are the same thing written differently across papers

| Concept | [P1] form | Other papers' form | Unifying note |
|---|---|---|---|
| phase sensitivity | $\Gamma(\omega_0\tau)$ (ISF) | [P2] keeps $\Gamma$; [P3] writes $\Gamma(\theta+\phi)$ inside the injection inner product | the same $\Gamma$; [P3] just uses it as the injection weighting kernel |
| phase evolution | $\phi(t)=\frac{1}{q_{max}}\int\Gamma i_n\,d\tau$ (Eq.11, noise view) | [P3] $\dot\phi=\Delta\omega-\frac{1}{q_{max}}\langle\Gamma i_{inj}\rangle$ (injection view) | the same LTV phase equation, one driven by random noise, one by deterministic injection |
| $1/f^2$ phase noise | Eq.(21) $\propto\Gamma_{rms}^2/q_{max}^2$ | [P2] $\kappa^2\propto\Gamma_{rms}^2/q_{max}^2$ (jitter version) | the same $\Gamma_{rms}^2/q_{max}^2$ ratio; phase noise and accumulated jitter are the same physics (claims **C3**=**C6** share the source) |
| the two directions of sensitivity | phase version $\Gamma$ only | [P4] adds the amplitude version, APF $\Lambda$ | $\Gamma$ (tangential/phase) and $\Lambda$ (radial/amplitude) are two orthogonal projections on the limit cycle |

### Which notation differs and needs unifying

Different papers use different symbols for the same quantity; this site always follows [notation](/00_overview/notation):

- **Offset frequency**: [P1] mostly uses $\Delta\omega$ (rad/s), datasheets/SerDes use $\Delta f$ (Hz);
  this site uses both, $\Delta\omega=2\pi\Delta f$.
- **The ISF's DC**: note that $c_0$ is a Fourier **coefficient**, while the ISF's DC **value** is $c_0/2$ (Eq.(12)) —
  very easy to get wrong when computing the $1/f^3$ corner (Eq.(24)); this site repeats the reminder.
- **Amplitude sensitivity**: [P4]'s APF is written $\Lambda(\phi)$ with units $\mathrm{A^{-1}}$; it has **different dimensions**
  from the dimensionless ISF $\Gamma$ and must not be mixed up.
- **PPV/adjoint/Floquet**: this site does not use their dedicated notation (e.g. Demir's $v_1^T(t)$) in the main track,
  mentioning them only as external literature in [effective_isf](/03_isf_core_theory/effective_isf).

For the full symbol comparison (including a "per-paper notation / remarks" column) see
[the "per-paper notation comparison" section of notation](/00_overview/notation).

## Key takeaways

- **[P1]** = ISF core; **[P2]** = ring extension; **[P3]/[P4]** = injection locking / APF advanced;
  **[P5]** = sense amplifier, **unrelated to ISF** (honestly flagged).
- **None** of the papers is a dedicated PPV/adjoint/PSS/PNoise paper; those belong to **external literature** (e.g. Demir 2000).
- [P1] **supersedes the Leeson empirical formula** from first principles, and corrects "$1/f^3$ corner ≠ device $1/f$ corner".
- Across papers, $\Gamma$, the phase equation, and $\Gamma_{rms}^2/q_{max}^2$ are often the same thing seen from different angles;
  notation is always unified per [notation](/00_overview/notation).

## Further reading

- Every equation → derivation page → source: [equation_index](/01_paper_map/equation_index)
- Every figure's script/formula/source: [figure_index](/01_paper_map/figure_index)
- Teaching-claims cross-reference (C1–C13): [claims_cross_reference](/01_paper_map/claims_cross_reference)
- Paper-by-paper deep dives: [paper deep dives](/05_paper_deep_dives/)
- Why the sources include one off-topic PDF: [build_report](/00_overview/build_report)
