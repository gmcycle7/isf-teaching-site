---
title: Learning Path
description: A twelve-step sequential learning path (nine-step backbone plus three advanced steps) — each step lists its goal, pages to read, prerequisites, expected outcomes, and self-check checkpoints; the fast track covers roughly the nine-step backbone, the full track all twelve steps.
---

import ProgressChecklist from "@site/src/components/ProgressChecklist";

> **β**: This English translation is in beta — the Traditional-Chinese original is the authoritative version.

# Learning Path

This page expands the nine steps from the home page into a learning path you can
**actually follow**, and extends the backbone with three advanced steps (Steps 10–12),
for **12 steps** in total. Each step tells you:

- **What to achieve** (the learning goal of this step);
- **Which pages to read** (in order);
- **Prerequisites** (you will get stuck without these);
- **Expected outcome** (what you should be able to do afterwards).

At the end there are two tracks: a **fast track** (roughly the nine-step backbone —
grasp the ISF backbone in one afternoon) and a **full track** (all twelve steps:
re-derive every formula yourself and run every lab yourself).

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
  {id: "step-9", label: "Step 9: Connect to SerDes clocking (jitter, eye, PLL/CDR)", href: "/02_foundations/psd_phase_noise_jitter"},
  {id: "step-10", label: "Step 10: Advanced theory — from κ to lineshape", href: "/03_isf_core_theory/diffusion_dictionary"},
  {id: "step-11", label: "Step 11: Injection locking and frequency conversion", href: "/05_paper_deep_dives/paper_003_injection_locking_part1"},
  {id: "step-12", label: "Step 12: System integration and measurement", href: "/06_design_insights/clock_chain_budget"}
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
  "symmetric waveform → $c_0\approx0$ → suppressed $1/f^3$"
  (for the closed form that computes $c_0$ and the corner directly from topology
  parameters, see Step 10's
  [asymmetric_isf_closed_form](/03_isf_core_theory/asymmetric_isf_closed_form)).

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
- **Expected outcome**: given an oscillator spec, you can say "which knob to turn first"
  (for the quantitative version of "how many dB from the theoretical ceiling", see
  Step 12's [fom_limit](/06_design_insights/fom_limit)).

## Step 9: Connect to SerDes clocking (jitter, eye, PLL/CDR) {#step-9}

- **What to achieve**: integrate phase noise into rms jitter and connect it to eye
  closure and BER in a SerDes link.
- **Pages to read**: [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter) →
  [serdes_clocking_connection](/06_design_insights/serdes_clocking_connection).
- **Prerequisites**: Steps 5 and 7 (especially lab_08).
- **Expected outcome**: you can do canonical example C — $f_0=5$ GHz,
  $\mathcal{L}(1\text{MHz})=-100$ dBc/Hz, $1/f^2$ slope, integrating 1→100 MHz
  $\Rightarrow\sigma_\phi=14.07$ mrad, $\sigma_t=447.9$ fs — and you know the integral is
  dominated by its **lower limit** (for the rigorous period/cycle-to-cycle kernels see
  Step 10's [jitter_kernels](/02_foundations/jitter_kernels); for the RJ/DJ decomposition
  and TJ@BER see Step 12's [dj_dual_dirac](/06_design_insights/dj_dual_dirac)).

---

## Steps 10–12 (advanced): from deep theory to system integration

The backbone (Steps 1–9) builds the ISF machinery for a **single free-running
oscillator**. The next three steps push the same machinery in three directions:
**deeper theory** (Step 10), **the injected oscillator** (Step 11), and **the whole
clock system** (Step 12). The former "Advanced (optional)" section has been expanded
and absorbed:
[paper_003](/05_paper_deep_dives/paper_003_injection_locking_part1) and
[paper_004](/05_paper_deep_dives/paper_004_injection_locking_part2) now live in Step 11;
[effective_isf](/03_isf_core_theory/effective_isf) (the cyclostationary correction
$\Gamma_{eff}=\Gamma\cdot\alpha$, claim **C9**, plus the **external** mathematical
foundations PPV/adjoint/Floquet, claim **C13**, **not in these 5 PDFs**, supplemented
from standard literature) remains optional — read it before starting Step 10 if you can.

## Step 10: Advanced theory — from κ to lineshape {#step-10}

- **What to achieve**: take "white-noise phase diffusion has only one free parameter"
  all the way — the same phase-variance growth rate $\kappa^2$ wearing five outfits
  ($\kappa$, $D$, linewidth, ADEV, the $1/f^2$ coefficient); the rigorous
  frequency-domain kernels of the three jitters (TIE / N-period / cycle-to-cycle);
  when the lineshape stops being Lorentzian under flicker FM; the closed form for
  $c_0$ and the $1/f^3$ corner; and the three ways to compute $\Gamma$ directly from
  the waveform.
- **Pages to read (one line of "why" each)**:
  1. [diffusion_dictionary](/03_isf_core_theory/diffusion_dictionary) — $\kappa$, $D$,
     linewidth, ADEV, and the $1/f^2$ coefficient are **five outfits of the same
     number**; get the conversion dictionary first (canonical
     $\kappa^2=0.125$ rad²/s).
  2. [jitter_kernels](/02_foundations/jitter_kernels) — the three jitters are the
     0th/1st/2nd-order differences of $\phi$; the prefactors and every single 2 are
     derived from first principles.
  3. [beyond_lorentzian](/03_isf_core_theory/beyond_lorentzian) — flicker FM turns the
     lineshape from Lorentzian into near-Gaussian, and rigorously answers "what does
     the instrument actually measure".
  4. [asymmetric_isf_closed_form](/03_isf_core_theory/asymmetric_isf_closed_form) —
     the [P2] App. B closed form: compute $\Gamma_{rms}$, $c_0$ and the $1/f^3$ corner
     directly from the stage count $N$ and the asymmetry $A$.
  5. [isf_from_waveform](/03_isf_core_theory/isf_from_waveform) — the three methods of
     the [P1] appendix (impulse injection / closed form / first derivative), and where
     each extra approximation starts to fail.
- **Prerequisites**: Steps 5, 6 and 9; plus
  [lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth) and
  [allan_variance](/02_foundations/allan_variance) (direct prerequisites of
  diffusion_dictionary — catch up on them first if needed).
- **Expected outcome**: you can convert any jitter spec into any other representation,
  and you know the failure point of every approximation.
- **Self-check checkpoints**:
  - With the canonical numbers ($\Gamma_{rms}=0.5$, $q_{max}=1$ pC,
    $S_i=10^{-24}$ A²/Hz), $\kappa^2=0.125$ rad²/s; switching to the true ideal LC
    ($\Gamma_{rms}=1/\sqrt2$), why is it exactly 2× ($0.25$ rad²/s)?
  - Under the "single-sided $S_\phi$, $\int_0^\infty$" convention, the period-jitter
    kernel's prefactor is $1/\omega_0^2$; stuffing a single-sided spectrum into the
    $2/\omega_0^2$ version common in the literature overcounts the variance by 2×
    (jitter by $\sqrt2$) — which bookkeeping convention does that 2 belong to?
  - Same $\mathcal{L}(10\,\text{kHz})$ spec: white-FM linewidth 50 Hz, flicker-FM about
    3.1 kHz — why does a dBc/Hz number at a single offset not determine the linewidth
    at all?

## Step 11: Injection locking and frequency conversion {#step-11}

- **What to achieve**: extend the same $\Gamma$ from phase noise into the "injected"
  world — the generalized Adler equation, in-lock noise shaping and out-of-lock
  pulling, acquisition transients and cycle slips, M:N subharmonic locking and the
  ILFD, mutual injection (QVCO), and finally the sub-sampling PLL that kicks the
  divider out of the loop.
- **Pages to read (one line of "why" each)**:
  1. [paper_003](/05_paper_deep_dives/paper_003_injection_locking_part1) — the
     generalized Adler equation: a single first-order equation written with the ISF,
     giving the lock range for any topology and any injection waveform (claim **C10**).
  2. [injection_locking_noise](/06_design_insights/injection_locking_noise) — a locked
     oscillator is a first-order PLL: its own noise is high-passed (corner
     $\omega_c$), the reference low-passed; when lock fails, the one-sided pulling
     comb.
  3. [lab_36](/04_simulation_labs/lab_36_lock_acquisition) — the missing transient
     pieces: the exact closed-form acquisition trajectory, critical slowing at the
     lock-range edge, noise-induced cycle slips.
  4. [paper_004](/05_paper_deep_dives/paper_004_injection_locking_part2) — the APF
     (the amplitude counterpart of the ISF, claim **C11**) and M:N subharmonic
     locking / ILFD.
  5. [quadrature_and_coupled_oscillators](/06_design_insights/quadrature_and_coupled_oscillators)
     — mutual injection = two Adler equations: the QVCO's coupling-strength ↔
     phase-error ↔ phase-noise triangular trade-off and that famous $\sim3$ dB.
  6. [sampling_pll](/06_design_insights/sampling_pll) — sampling the zero crossing =
     sampling the ISF's most sensitive point: sub-sampling makes the divider noise
     vanish and the CP noise no longer $\times N^2$.
- **Prerequisites**: Steps 6 and 8; catching up on
  [effective_isf](/03_isf_core_theory/effective_isf) first is recommended
  (cyclostationary correction, see the top of this section).
- **Expected outcome**: from the generalized Adler equation all the way to the noise
  shaping of ILFD / QVCO / sub-sampling — you can explain injection-related locking,
  pulling and frequency conversion along the same single $\Gamma$.
- **Self-check checkpoints**:
  - With sinusoidal injection and the ideal-LC ISF, the generalized Adler equation
    reduces to $\dot\theta=\Delta\omega-\omega_L\sin\theta$ with
    $\omega_L=I_{inj}/(2q_{max})$; in lock, the oscillator's own noise is high-pass
    shaped with corner $\omega_c=\sqrt{\omega_L^2-\Delta\omega^2}$ (the pull-in
    frequency of [P3] Eq.(40)) — why does the noise suppression vanish at the **edge**
    of the lock range?
  - Out of lock, the beat frequency is $\omega_b=\sqrt{\Delta\omega^2-\omega_L^2}$
    ([P4] Eq.(34)) and the sideband comb grows on one side only; with the canonical
    numbers ($f_L=5$ MHz, true-LC noise) at $r=0.8$ the cycle-slip rate is
    $\sim10^{-1.86\times10^7}$ — why do we say thermal slips are a "cliff", not a
    "slope"?
  - M:N subharmonic locking gives
    $\omega_L=I_{inj}\lvert\tilde\Gamma_N\rvert/2$ ([P4] Eq.(28)–(30)): which harmonic
    does the ÷2 ILFD ride on? The sub-sampling PLL's in-band floor drops from
    $-118.9$ to $-126.0$ dBc/Hz (illustrative example) — where did the divider term
    go?

## Step 12: System integration and measurement {#step-12}

- **What to achieve**: finish at the system level — book-keep a single oscillator's
  $\mathcal{L}(f)$ down the clock chain to every node, compare against the FOM
  theoretical ceiling, understand what a reference oscillator actually buys, compute
  an ADC's SNR/ENOB, book-keep RJ/DJ separately into TJ@BER, read measurement plots
  and spurs, dodge the 12 mines, and finally use the capstone to validate the whole
  site end to end.
- **Pages to read (one line of "why" each)**:
  1. [clock_chain_budget](/06_design_insights/clock_chain_budget) — the four
     bookkeeping rules (×N / ÷N / PLL / buffer) plus a complete worked chain
     100 MHz→5 GHz→2.5 GHz.
  2. [fom_limit](/06_design_insights/fom_limit) — the FOM ceiling
     $=173.8-10\log_{10}(F_{eff})$ dB (300 K): know how many dB your design is from
     the physical limit.
  3. [reference_oscillators](/06_design_insights/reference_oscillators) — a crystal is
     just an LC tank with an outrageously high $Q$: why nothing downstream can fix the
     reference's close-in noise.
  4. [adc_aperture_jitter](/06_design_insights/adc_aperture_jitter) — sampling error =
     slope × timing error: clock quality directly sets the data converter's effective
     number of bits.
  5. [dj_dual_dirac](/06_design_insights/dj_dual_dirac) — RJ unbounded, DJ bounded:
     the dual-Dirac model and the industry-standard TJ@BER bookkeeping.
  6. [measurement_and_spurs](/06_design_insights/measurement_and_spurs) — the three
     ways to measure $\mathcal{L}(f)$, telling spurs from random noise, and how to
     read a real PN plot.
  7. [common_mistakes](/06_design_insights/common_mistakes) — 12 real mines: a full
     review of the site's factor-of-2 discipline.
  8. [capstone_lc_end_to_end](/03_isf_core_theory/capstone_lc_end_to_end) — the site's
     main spine end to end: state equations → ISF → spectrum → linewidth → jitter →
     BER. The finale.
- **Prerequisites**: Steps 7–9; Step 10 (the jitter kernels and the diffusion
  dictionary are used repeatedly); Step 11 helps too (sampling_pll already appeared
  in Step 11).
- **Expected outcome**: you can draw up — and defend — a clock noise budget: from the
  reference to the sampler, every stage's $\mathcal{L}(f)$ and the final jitter have a
  traceable source.
- **Self-check checkpoints**:
  - The worked chain (100 MHz → ×50 PLL → 5 GHz → ÷2 → 2.5 GHz → buffer) ends at an
    integrated jitter of 27.6 fs; under ideal ×N / ÷N, why does $\sigma_t$ **in
    seconds** not change by a single fs?
  - Feeding a 5 GHz input with the canonical $\sigma_t=447.9$ fs clock:
    $\text{SNR}_{jitter}=37.0$ dB, ENOB $=5.86$ bit; 10 ENOB @ 5 GHz requires pushing
    $\sigma_t$ down to $\le25.4$ fs — which formula is doing the conversion?
    ($\text{SNR}=-20\log_{10}(2\pi f_{in}\sigma_t)$)
  - $\text{TJ}(\text{BER})=\text{DJ}_{\delta\delta}+2Q\cdot\sigma$ with
    $Q(10^{-12})=7.03$: why is $\text{DJ}_{\delta\delta}\le\text{DJ}_{pp}$ a
    **deliberate** under-report? And why is a spur specified in dBc and **not**
    dBc/Hz?

---

## Two tracks

### Fast track (about one afternoon, backbone only)

This corresponds to the **Steps 1–9 backbone** (Steps 10–12 are not part of the fast
track). The goal is "understand what the ISF is and how it determines phase noise".
You do **not** re-derive anything and do **not** run the simulations yourself:

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

Follow **Steps 1 through 12** above in order, **cover the answer and re-derive every
formula yourself**, run **every lab yourself with `python scripts/run_all_sims.py`**
and check figures against numbers (the advanced labs referenced in Steps 10–12
included). Suggested pace:

| Stage | Steps | Key deliverable (self-check) |
|---|---|---|
| Geometric intuition | 1–2 | Can draw the limit cycle; can state LTV vs. LTI |
| ISF core | 3–6 | Can re-derive Eq.(9)→(11)→(12)→(20)→(21)→(24) |
| Hands-on | 7 | Can reproduce examples A/B/C; orders of magnitude match |
| Design | 8–9 | Can list the design knobs; can integrate $\mathcal{L}$ into $\sigma_t$ |
| Advanced theory | 10 | Can convert freely among $\kappa$, $D$, linewidth, ADEV and the $1/f^2$ coefficient; can name where every 2 comes from |
| Injection & conversion | 11 | Can derive $\omega_c$, $\omega_b$ and the M:N lock condition from the generalized Adler equation; can say where sub-sampling wins |
| System integration | 12 | Can book-keep $\mathcal{L}(f)$ down a full clock chain; can draw up and defend a jitter budget |

## Key takeaways

- Twelve steps = the nine-step backbone (phase geometry → LTV → ISF definition →
  convolution → white/flicker noise → Fourier → labs → design → SerDes) plus three
  advanced steps (Step 10 κ and lineshape → Step 11 injection locking and frequency
  conversion → Step 12 system integration and measurement).
- The four quick-lookup pages (return there first when stuck):
  [cheat_sheet](/00_overview/cheat_sheet), [notation](/00_overview/notation),
  [glossary](/99_appendix/glossary), [equation_index](/01_paper_map/equation_index)
  (see the "Quick lookup" table at the top of this page).
- The fast track covers the nine-step backbone; the full track walks all twelve steps:
  re-derive every formula, run every lab.
- Steps 10–12 are advanced: injection/APF now live in Step 11; PPV/adjoint and much of
  the instrument/architecture knowledge in the system-integration pages come from
  **external literature** (**not in the 5 PDFs**) — every such page carries an honest
  disclaimer.

## Further reading

- Division of labor among the five papers: [paper_summary_table](/01_paper_map/paper_summary_table)
- The source of every figure: [figure_index](/01_paper_map/figure_index)
- Cross-index of the teaching claims: [claims_cross_reference](/01_paper_map/claims_cross_reference)
- Why the sources include one off-topic PDF: [build_report](/00_overview/build_report)
