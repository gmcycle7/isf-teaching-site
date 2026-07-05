---
title: Learning Path
description: A nine-step sequential learning path — each step lists its goal, pages to read, prerequisites, and expected outcomes, plus a fast track and a full track.
---

import ProgressChecklist from "@site/src/components/ProgressChecklist";

> 🌐 English translation (β). Most other pages are currently in Traditional Chinese — they will show in Chinese until translated.

# Learning Path

This page expands the nine steps from the home page into a learning path you can
**actually follow**. Each step tells you:

- **What to achieve** (the learning goal of this step);
- **Which pages to read** (in order);
- **Prerequisites** (you will get stuck without these);
- **Expected outcome** (what you should be able to do afterwards).

At the end there are two tracks: a **fast track** (grasp the ISF backbone in one
afternoon) and a **full track** (re-derive every formula yourself and run every lab
yourself).

> **How to use this page**: on a first pass, take the "full track" and come back to tick
> the checkbox after each step. For later review, the "fast track" is enough. A `TODO:`
> marker means that spot still needs manual verification against the original PDF; a
> "toy model" label means it is a **pedagogical simplification, not transistor-level**.

<ProgressChecklist items={[
  {id: "step-1", label: "Step 1: What an oscillator's \"phase\" actually is", href: "/02_foundations/oscillator_phase"},
  {id: "step-2", label: "Step 2: Noise is a small perturbation; the oscillator responds as LTV, not LTI", href: "/02_foundations/lti_vs_ltv"},
  {id: "step-3", label: "Step 3: The operational definition of the ISF (impulse → phase)", href: "/03_isf_core_theory/impulse_to_phase_shift"},
  {id: "step-4", label: "Step 4: From a single impulse to arbitrary noise (convolution)", href: "/03_isf_core_theory/convolution_derivation"},
  {id: "step-5", label: "Step 5: White noise → 1/f², flicker → 1/f³", href: "/03_isf_core_theory/white_noise_to_phase_noise"},
  {id: "step-6", label: "Step 6: The Fourier view of the ISF (c₀, cₙ, upconversion)", href: "/03_isf_core_theory/fourier_series_of_isf"},
  {id: "step-7", label: "Step 7: Simulation labs — build numerical feel", href: "/04_simulation_labs/numerical_feeling"},
  {id: "step-8", label: "Step 8: Design takeaways (symmetry, swing, slope)", href: "/06_design_insights/symmetry"},
  {id: "step-9", label: "Step 9: Connect to SerDes clocking (jitter, eye, PLL/CDR)", href: "/02_foundations/psd_phase_noise_jitter"}
]} />

## Keep these three pages at hand as "dictionaries"

Before you start, keep these three pages nearby; whenever you meet an unfamiliar symbol
or paper reference, look it up there:

- [notation](/00_overview/notation) — the unified symbol table (site-wide symbols, units, per-paper cross-reference).
- [paper_summary_table](/01_paper_map/paper_summary_table) — the five papers at a glance (who is responsible for what).
- [equation_index](/01_paper_map/equation_index) — every formula → derivation page → source.

**Quick lookup** (when unsure about a symbol / formula / English term, jump via the table
below; when stuck, return to these four pages first):

| What you want to look up | Where to go |
|---|---|
| All formulas on one page, canonical numerical examples A/B/C | [Cheat Sheet](/00_overview/cheat_sheet) |
| The meaning and units of a symbol (e.g. $\Gamma_{rms}$, $q_{max}$, $c_0$) | [Notation](/00_overview/notation) |
| An intuitive explanation of an English term (e.g. ISF, cyclostationary, limit cycle) | [Glossary](/99_appendix/glossary) |
| Which paper and Eq. a formula comes from, and where it is derived | [Equation Index](/01_paper_map/equation_index) |

---

## Step 1: What an oscillator's "phase" actually is {#step-1}

- **What to achieve**: build the geometric picture of the limit cycle (the closed
  steady-state trajectory of an oscillator), and clearly separate **phase** (tangential
  along the cycle, no restoring force) from **amplitude** (radial away from the cycle,
  with a restoring force).
- **Pages to read**: [oscillator_phase](/02_foundations/oscillator_phase) →
  [phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise).
- **Prerequisites**: 2-D state space, the phase plane, the basic picture of RLC oscillation.
- **Expected outcome**: you can explain "why a tangential perturbation persists forever
  while a radial one is pulled back" — this is exactly claim **C2**
  (see [claims_cross_reference](/01_paper_map/claims_cross_reference)).

## Step 2: Noise is a small perturbation; the oscillator responds as LTV, not LTI {#step-2}

- **What to achieve**: understand that with respect to noise an oscillator is **LTV
  (linear time-variant)** — the same impulse injected at different phases produces a
  **different** phase shift, unlike an LTI system which only depends on $t-\tau$.
- **Pages to read**: [lti_vs_ltv](/02_foundations/lti_vs_ltv).
- **Prerequisites**: Step 1; linear systems, impulse response, convolution.
- **Expected outcome**: you can sketch the difference between the LTI $h(t-\tau)$ and the
  LTV $h_\phi(t,\tau)$, corresponding to the figure `lti_vs_ltv_impulse_response.png`.
  This is claim **C1**.

## Step 3: The operational definition of the ISF (impulse → phase) {#step-3}

- **What to achieve**: derive, starting from the capacitor relation $q=Cv$, the
  operational definition of the ISF
  $\Delta\phi=\Gamma(\omega_0\tau)\,\Delta q/q_{max}$ ([P1] Eq.(9)–(11), p.182),
  and understand why $\Gamma$ is dimensionless and $2\pi$-periodic.
- **Pages to read**: [impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift) →
  [isf_definition](/03_isf_core_theory/isf_definition).
- **Prerequisites**: Steps 1–2; the capacitor relation, unit conversions.
- **Expected outcome**: you can do canonical example A in your head — with
  $q_{max}=1$ pC, $\Delta q=1$ fC, $\Gamma=0.5$, $f_0=5$ GHz you get
  $\Delta\phi=5\times10^{-4}$ rad and $\Delta t=15.9$ fs.

## Step 4: From a single impulse to arbitrary noise (convolution) {#step-4}

- **What to achieve**: use superposition to generalize a single phase step into the LTV
  convolution
  $\phi(t)=\frac{1}{q_{max}}\int_{-\infty}^{t}\Gamma(\omega_0\tau)\,i_n(\tau)\,d\tau$
  ([P1] Eq.(11), p.182), and see why the upper integration limit $t$ (memory) makes the
  phase **accumulate**.
- **Pages to read**: [convolution_derivation](/03_isf_core_theory/convolution_derivation).
- **Prerequisites**: Step 3; convolution, integration.
- **Expected outcome**: you can explain "phase is an integrator of noise", paving the way
  for the $1/f^2$ slope in Step 5.

## Step 5: White noise → $1/f^2$, flicker → $1/f^3$ {#step-5}

- **What to achieve**: derive the signature result $\mathcal{L}\propto\Gamma_{rms}^2/q_{max}^2$
  ([P1] Eq.(21), p.185, claim **C3**), and see that flicker noise upconverts into
  $1/f^3$ only through the DC term $c_0$ of the ISF ([P1] Eq.(23)(24), claims **C4/C5**).
- **Pages to read**: [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) →
  [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion).
- **Prerequisites**: Step 4; PSD, Parseval.
- **Expected outcome**: you can do canonical example B — the same set of numbers plugged
  into Eq.(21) gives $\mathcal{L}=-148.0$ dBc/Hz; and you understand the **famous
  factor-of-2** SSB bookkeeping controversy mentioned in Section 3 of the spec.

## Step 6: The Fourier view of the ISF ($c_0$, $c_n$, upconversion) {#step-6}

- **What to achieve**: expand the ISF into the Fourier series
  $\Gamma=\frac{c_0}{2}+\sum c_n\cos(n\omega_0\tau+\theta_n)$
  ([P1] Eq.(12), p.183), understand that each $c_n$ "downconverts" the noise near
  $n\omega_0$ to the carrier, and that $\sum c_n^2=2\Gamma_{rms}^2$
  (Parseval, [P1] Eq.(20)).
- **Pages to read**: [fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf) →
  [rms_isf](/03_isf_core_theory/rms_isf).
- **Prerequisites**: Step 5; Fourier series.
- **Expected outcome**: you can state the mathematical basis of the design rule
  "symmetric waveform → $c_0\approx0$ → suppressed $1/f^3$".

## Step 7: Simulation labs — build numerical feel {#step-7}

- **What to achieve**: run the preceding formulas **with your own hands**, look at the
  figures, check the numbers, and turn the conversions between rad, fs, dBc/Hz and
  jitter into reflexes.
- **Pages to read**: first [numerical_feeling](/04_simulation_labs/numerical_feeling)
  (three must-do mental calculations), then in order
  [lab_01](/04_simulation_labs/lab_01_sinusoidal_oscillator),
  [lab_02](/04_simulation_labs/lab_02_lc_oscillator_toy_model),
  [lab_04](/04_simulation_labs/lab_04_impulse_injection_sweep),
  [lab_05](/04_simulation_labs/lab_05_isf_fourier_coefficients),
  [lab_06](/04_simulation_labs/lab_06_white_noise_phase_noise),
  [lab_07](/04_simulation_labs/lab_07_flicker_noise_upconversion),
  [lab_08](/04_simulation_labs/lab_08_jitter_integration).
- **Prerequisites**: Steps 3–6; a little Python/NumPy.
- **Expected outcome**: you can verify canonical examples A/B/C in one line with the
  functions in `simulations/common/`; every figure is traceable to its script and
  formula in the [figure_index](/01_paper_map/figure_index).

## Step 8: Design takeaways (symmetry, swing, slope) {#step-8}

- **What to achieve**: translate the formulas into **design knobs** — increase
  $q_{max}$, lower $\Gamma_{rms}$, enforce waveform symmetry to suppress $c_0$; and
  understand the ring result $\Gamma_{rms}\propto N^{-3/2}$ and "at fixed power and
  frequency, ring phase noise is almost independent of the number of stages $N$"
  (claims **C7/C8**).
- **Pages to read**: [symmetry](/06_design_insights/symmetry) →
  [lc_vs_ring](/06_design_insights/lc_vs_ring).
- **Prerequisites**: Steps 5–6.
- **Expected outcome**: given an oscillator spec, you can say "which knob to turn first".

## Step 9: Connect to SerDes clocking (jitter, eye, PLL/CDR) {#step-9}

- **What to achieve**: integrate phase noise into rms jitter and connect it to eye
  closure and BER in a SerDes link.
- **Pages to read**: [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter) →
  [serdes_clocking_connection](/06_design_insights/serdes_clocking_connection).
- **Prerequisites**: Steps 5 and 7 (especially lab_08).
- **Expected outcome**: you can do canonical example C — $f_0=5$ GHz,
  $\mathcal{L}(1\text{MHz})=-100$ dBc/Hz, $1/f^2$ slope, integrating 1→100 MHz
  $\Rightarrow\sigma_\phi=14.07$ mrad, $\sigma_t=447.9$ fs — and you know the integral is
  dominated by its **lower limit**.

---

## Advanced (optional): injection locking and the APF

Once the backbone is done, if you want to see how the ISF extends beyond phase noise:

- [paper_003_injection_locking_part1](/05_paper_deep_dives/paper_003_injection_locking_part1)
  — the same ISF yields the generalized Adler equation (claim **C10**, [P3]).
- [paper_004_injection_locking_part2](/05_paper_deep_dives/paper_004_injection_locking_part2)
  — the amplitude counterpart, the APF (amplitude perturbation function, claim **C11**, [P4]).
- [effective_isf](/03_isf_core_theory/effective_isf) — the cyclostationary correction
  $\Gamma_{eff}=\Gamma\cdot\alpha$ (claim **C9**), plus the **external** mathematical
  foundations PPV/adjoint/Floquet (claim **C13**, **not in these 5 PDFs**, supplemented
  from standard literature).

---

## Two tracks

### Fast track (about one afternoon, backbone only)

The goal is "understand what the ISF is and how it determines phase noise". You do
**not** re-derive anything and do **not** run the simulations yourself:

1. [oscillator_phase](/02_foundations/oscillator_phase) (only the limit cycle and the phase/amplitude picture)
2. [lti_vs_ltv](/02_foundations/lti_vs_ltv) (the core LTV conclusion and figure)
3. [impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift) (memorize the operational definition + example A)
4. [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) (memorize Eq.(21) and example B)
5. [fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf) (the intuition of $c_0$ suppressing $1/f^3$)
6. [numerical_feeling](/04_simulation_labs/numerical_feeling) (the three mental calculations)
7. [serdes_clocking_connection](/06_design_insights/serdes_clocking_connection) (the jitter and eye conclusions)

After this you should be able to answer: what the ISF is, why LTV,
$\mathcal{L}\propto\Gamma_{rms}^2/q_{max}^2$, why symmetry matters, and how phase noise
becomes jitter.

### Full track (re-derive every step + run every lab)

Follow **Steps 1 through 9** above in order, **cover the answer and re-derive every
formula yourself**, run **every lab yourself with `python scripts/run_all_sims.py`**
and check figures against numbers, then read the three advanced pages. Suggested pace:

| Stage | Steps | Key deliverable (self-check) |
|---|---|---|
| Geometric intuition | 1–2 | Can draw the limit cycle; can state LTV vs. LTI |
| ISF core | 3–6 | Can re-derive Eq.(9)→(11)→(12)→(20)→(21)→(24) |
| Hands-on | 7 | Can reproduce examples A/B/C; orders of magnitude match |
| Design | 8–9 | Can list the design knobs; can integrate $\mathcal{L}$ into $\sigma_t$ |
| Advanced | optional | Can explain how injection/APF/PPV reuse the same $\Gamma$ |

## Key takeaways

- The nine-step backbone: phase geometry → LTV → ISF definition → convolution →
  white/flicker noise → Fourier → labs → design → SerDes.
- The four quick-lookup pages (return there first when stuck):
  [cheat_sheet](/00_overview/cheat_sheet), [notation](/00_overview/notation),
  [glossary](/99_appendix/glossary), [equation_index](/01_paper_map/equation_index)
  (see the "Quick lookup" table at the top of this page).
- Fast track for the backbone; full track re-derives every formula and runs every lab.
- The advanced injection/APF/PPV material is optional; PPV/adjoint is **not in the
  5 PDFs** — it comes from external literature.

## Further reading

- Division of labor among the five papers: [paper_summary_table](/01_paper_map/paper_summary_table)
- The source of every figure: [figure_index](/01_paper_map/figure_index)
- Cross-index of the teaching claims: [claims_cross_reference](/01_paper_map/claims_cross_reference)
- Why the sources include one off-topic PDF: [build_report](/00_overview/build_report)
