---
title: "[P4] Injection Locking & Pulling — Part II (APF / Frequency Division)"
description: Hong–Hajimiri 2019 Part II deep dive — APF (amplitude counterpart of the ISF, units 1/A, [P4] Eq.(18)–(22)), ISF/APF quadrature (Eq.(26)), amplitude modulation, ILFD/frequency division (ILFD details are advanced).
---

> **β**: This English translation is in beta — the Traditional-Chinese original is the authoritative version.

# A General Theory of Injection Locking and Pulling in Electrical Oscillators—Part II

> **Prerequisites (recommended reading order)**: [paper_001](/05_paper_deep_dives/paper_001_general_theory_phase_noise) (the ISF $\Gamma$ is the tangential projection) → [phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise) (why amplitude is pulled back while phase accumulates) → [paper_003](/05_paper_deep_dives/paper_003_injection_locking_part1) (phase-only generalized Adler). This page is **advanced**; the APF is the radial dual of the ISF.

[P3] covered phase only; this paper (Part II, **advanced**) adds the **amplitude** dimension. It introduces the
**APF (Amplitude Perturbation Function)** $\Lambda(\phi)$ — the "amplitude version of the ISF," with units $1/\text{A}$
— and uses it to explain amplitude modulation of LC oscillators under injection, transient locking behavior,
and **injection-locked frequency division (ILFD)**. For an ideal LC, the ISF and APF
are **in quadrature** with each other.

> **Scope of this page**: advanced deep-dive, **not a core teaching chapter**. The APF defining equations ([P4] Eq.(18)–(22), p.2126) and the ideal-LC
> quadrature (Eq.(26), p.2128) have been verified against the original; the ILFD details remain advanced. Read [P1] (ISF) and
> [P3](/05_paper_deep_dives/paper_003_injection_locking_part1) (phase-only injection) first.

## Citation

> **[P4]** B. Hong and A. Hajimiri, *"A General Theory of Injection Locking and Pulling in
> Electrical Oscillators—Part II: Amplitude Modulation in LC Oscillators, Transient Behavior,
> and Frequency Division,"* IEEE J. Solid-State Circuits, vol. 54, no. 8, pp. 2122–2139,
> Aug. 2019. (file `BHongGenTheor-II_JSSC2019_Postprint.pdf`, paper_004)

## One-sentence contribution

Defines the amplitude version of the ISF — the APF $\Lambda(\phi)$ (units $1/\text{A}$) — completing the phase framework of [P3]
into a full phase + amplitude model, explaining amplitude modulation under injection, transient locking, and ILFD frequency division;
for an ideal LC, the ISF and APF are in quadrature (claim C11).

## Why this paper matters

Both [P1] and [P3] assume "amplitude perturbations are pulled back and can be ignored." That assumption is fine for
phase noise and weak injection, but not for **strong injection, transients, or frequency division** — there the
amplitude is visibly modulated, and phase and amplitude couple. Part II adds this dimension:

- **The APF is the ISF of amplitude**: the ISF $\Gamma$ projects injected charge onto the **tangential**
  (phase) direction of the limit cycle; the APF $\Lambda$ projects it onto the **radial** (amplitude) direction.
  Only together do they form the complete projection of a perturbation.
- **In an ideal LC, the ISF and APF are in quadrature** (90° apart): at the moment of maximum phase sensitivity
  (the zero-crossing), amplitude sensitivity is minimal; at the moment of maximum amplitude sensitivity (the peak),
  phase sensitivity is minimal. This is the mathematical version of what
  [phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise) says about "why amplitude noise decays."
- **Frequency division (ILFD)**: inject a signal at $N$ times the frequency into an oscillator so it locks at the $1/N$
  subharmonic — a low-power frequency divider. Part II designs such dividers within the ISF/APF framework and builds a
  dual-modulus prescaler with switchable division ratio.

## Main assumptions

Per paper_metadata (paper_004.assumptions):

1. Built on top of the time-synchronous ISF model of Part I.
2. Amplitude dynamics are captured to first order via the **APF and the amplitude decay function**.
3. The amplitude-modulation results focus on **LC oscillators**.

> **Physical intuition (2-D projection)**: an injected charge $\Delta q$ nudges the state point. Decompose the
> nudge along the two orthogonal directions of the limit cycle — tangential (phase, permanent) measured by $\Gamma$,
> radial (amplitude, pulled back) measured by $\Lambda$. Phase noise cares only about the tangential part;
> the full dynamics of injection need both.

## Key equations

### APF definition and amplitude decay function (verified against the original PDF ✓)

The APF $\tilde\Lambda$ is the **amplitude analog** of Part I's unit-bearing ISF $\tilde\Gamma=\Gamma/q_{max}$: the weight
with which an injected current impulse projects onto the **radial (amplitude) direction** of the limit cycle. [P4] factors the
amplitude perturbation into the product of an APF and a decay,
$D(\tau,\phi)=\tilde\Lambda(\phi)\,d(\tau,\phi)$ ([P4] Eq.(18), p.2126), and defines the **APF**
$\Delta(\phi):=\int_0^\infty D(\tau,\phi)\,d\tau$ ([P4] Eq.(19), p.2126, units $1/\text{A}$). Unlike phase, amplitude perturbations decay —
the ideal-LC **amplitude decay function** (in the ideal-LC section, [P4] p.2127–2128) is:

$$
d(t,\phi)=e^{-t/\tau_0},\qquad \int_0^\infty d(t,\phi)\,dt=\tau_0=\frac{2Q}{\omega_{osc}}
$$

**Key physics (gem)**: the "memory time" of the amplitude is $\tau_0=2Q/\omega_{osc}$ — a high-$Q$ LC recovers its amplitude **slowly** ($\tau_0$ is large),
but it **does recover** (exponential decay back to the limit cycle); the phase has no such restoring force (its impulse response is a unit step — infinite memory).
This is the **quantitative version** of "why amplitude noise is suppressed while phase noise accumulates" (claim C2). For an ideal LC, the APF and the decay are related by
$\Delta(\phi)=\tau_0\,\tilde\Lambda(\phi)$.

**Comparison table (ISF vs APF)**:

| Quantity | Projection direction | Symbol | Fate of the perturbation |
|---|---|---|---|
| ISF | tangential (phase) | $\tilde\Gamma=\Gamma/q_{max}$ | accumulates permanently (impulse response = unit step) |
| APF | radial (amplitude) | $\tilde\Lambda$ | decays back to the limit cycle as $e^{-t/\tau_0}$, $\tau_0=2Q/\omega_{osc}$ |

> **Verified**: the APF factorization $D(\tau,\phi)=\tilde\Lambda(\phi)\,d(\tau,\phi)$ ([P4] Eq.(18), p.2126), the APF definition
> $\Delta(\phi)=\int_0^\infty D\,d\tau$ ([P4] Eq.(19), p.2126, units $1/\text{A}$), and the ideal-LC decay function
> $e^{-t/\tau_0}$, $\tau_0=2Q/\omega_{osc}$ ([P4] ideal-LC section, p.2127–2128) have all been confirmed verbatim against the rendered original PDF.

### Quadrature of the ISF and APF (ideal LC, verified ✓)

The ISF and APF **fundamentals** of an ideal LC ([P4] Eq.(26), p.2128):

$$
\tilde\Gamma_1=\frac{1}{q_{max}}\,\angle 90^\circ,\qquad
\tilde\Lambda_1=\frac{\tau_0}{q_{max}}\,\angle 0^\circ
$$

Their phase difference is exactly **$90^\circ$ (quadrature)** (claim C11). Physical meaning: injecting at the zero-crossing changes almost purely phase
($\tilde\Gamma$ large, $\tilde\Lambda$ small); injecting at the peak changes almost purely amplitude ($\tilde\Lambda$ large, $\tilde\Gamma$ small).
Note the APF fundamental carries an extra factor of $\tau_0$ relative to the ISF — **at high $Q$ the amplitude effect ($\propto\tau_0=2Q/\omega_0$) is actually more pronounced**,
which is also why LC injection locking often comes with substantial amplitude modulation.

**Amplitude-corrected Adler (augmented pulling, ideal-LC special case [P4] Eq.(27), p.2128)**: substitute the ISF and APF
together. The general sinusoidal-injection form is [P4] Eq.(22), p.2126 (with a $+$ sign and phase-offset terms $\cos(\theta+\angle\tilde\Gamma_1)/\cos(\theta+\angle\tilde\Lambda_1)$);
substituting the ideal-LC quadrature angles $\angle 90^\circ/\angle 0$ (Eq.(26)) into Eq.(22), the phase equation under sinusoidal injection simplifies to

$$
\frac{d\theta}{dt}=(\omega_0-\omega_{inj})-\frac{\tfrac12\,(I_{inj}/q_{max})\sin\theta}{1+\tfrac12\,(I_{inj}\tau_0/q_{max})\cos\theta}
$$

The denominator term is the **amplitude-modulation correction** contributed by the APF; Part I's phase-only Adler is the special case with denominator $=1$.

> **Verified**: the quadrature of $\tilde\Gamma_1,\tilde\Lambda_1$ ([P4] Eq.(26), p.2128; sin/cos form in Eq.(24))
> and the amplitude-corrected Adler shown above — i.e., **the ideal-LC special case [P4] Eq.(27), p.2128** (obtained by substituting the $\angle 90^\circ/\angle 0$ of Eq.(26) into the general form Eq.(22), p.2126, with the $-$ sign, the $\sin\theta$ numerator, and the $\tau_0$ factor) — have both been confirmed verbatim against the rendered original PDF.

### Amplitude modulation and frequency division (ILFD)

**Meaning**: expanding the APF as a Fourier series, one can compute how the injection waveform is "filtered" into amplitude modulation
([P4] Sec. III-D text). In an **ILFD**, a signal at frequency $\approx N\omega_0$ is injected, and locking to $\omega_0$ occurs via the
$N$-th harmonic of the ISF/APF, achieving ÷$N$. Part II also builds a **dual-modulus prescaler** that switches between two
division ratios (using a single-ended inverter-chain ring, allocating stages via a quadrature injection scheme).

**Numerical example (÷2 intuition)**: inject a signal at $2f_0$; the oscillator locks at $f_0$, so the output frequency is half
the input. If the input is 10 GHz, the output is 5 GHz. The lock range is now set by the inner product between the **second harmonic**
of the ISF/APF and the injection waveform (connecting back to the generalized Adler of [P3], except that it is the subharmonic-relevant
harmonic doing the averaging). For the concrete stage allocation and modulus switching, see
[P4] Sec. VIII (dual-modulus prescaler, from p.2135; schematic Fig.19, Table VIII, and Fig.21 on p.2137).

## Key figures

| Paper figure | Page | Content | Teaching purpose |
|---|---|---|---|
| Fig. 5 | 2126 | Characterizing the effect of an instantaneous charge injection on the oscillator: ISF / excess phase, the amplitude decay function, and the quadrature relation between ISF and APF (verified) | The single best figure connecting phase (ISF) and amplitude (APF) sensitivities |

This figure is the best visual for "why amplitude noise decays while phase noise does not": the perturbation associated with the APF
is pulled back by the amplitude decay function, whereas the phase perturbation associated with the ISF remains permanently. This site uses
the same concept in [phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise) (toy comparison figure
`limit_cycle_phase_amplitude.png`, **not transistor-level**).

> **Verified**: this figure is [P4] Fig. 5, p.2126, captioned "Characterizing the effect that an instantaneous injection of
> charge has on an oscillator," confirmed against the rendered original PDF. (Fig. 3 p.2124 is the impulse-train↔sinusoid equivalence, and Fig. 6
> p.2127 is the bipolar Colpitts example — neither is this figure.)

![Limit cycle: tangential = phase (persists), radial = amplitude (pulled back) (toy)](/figures/limit_cycle_phase_amplitude.png)

## Design insights

- **Strong injection / transients require the amplitude**: ignoring the APF is fine for weak injection; for strong injection,
  transient locking, and frequency division, amplitude modulation cannot be ignored — compute with ISF + APF together.
- **Quadrature is a design tool**: to modulate phase purely, inject at the phase-sensitive point (ISF extremum); for amplitude keying / AM,
  inject at the amplitude-sensitive point (APF extremum).
- **The ILFD is a low-power divider**: compared with latch-based / CML dividers, which burn power at high frequency, the ILFD divides via
  injection locking at low power; use the $N$-th harmonic of the ISF/APF to design the division ratio and lock range.
- **Dual-modulus prescaler**: switch the division ratio on the same inverter-chain ring via a quadrature injection scheme,
  saving power.

## Limitations

Per paper_metadata (paper_004.limitations):

- Strongly nonlinear effects beyond the first-order APF are only partially captured.
- Relative to this site's core ISF phase-noise goal, it is **advanced / peripheral**.
- The exact APF equations ([P4] Eq.(18)–(22), p.2126; quadrature Eq.(26), p.2128) have been verified against the original (claim C11).

## Relationship to other papers

- **[P3]** is the direct prequel: this paper uses Part I's time-synchronous ISF model and adds amplitude (APF).
- **[P1]** provides the ISF $\Gamma$; the APF is its radial dual. The ideal-LC $\Gamma=-\sin$ also appears in this site's
  [isf_definition](/03_isf_core_theory/isf_definition).
- **[P2]** provides the ring ISF; the ILFD/prescaler in this paper is implemented with an inverter-chain ring.
- **[P5]** is unrelated to this page (sense amplifier); but the start-up of LC / latch oscillators likewise relies on cross-coupled positive feedback
  (the corner-case bridge of claim C12).
- The APF is entry 21 in [equation_index](/01_paper_map/equation_index) (verified on this page against [P4] Eq.(18)–(22)); the phase/amplitude geometry is in
  [phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise).

## Further reading / corresponding teaching pages

| Which part of this page | Corresponding teaching page | What that page adds |
|---|---|---|
| Injection phase sets the effective weight of $\Gamma$ / $\Lambda$ (cyclostationary concept) | [effective_isf](/03_isf_core_theory/effective_isf) | $\Gamma_{eff}=\Gamma\cdot\alpha$, bias-dependent thermal-noise NMF, switching-pair worked example |
| How injection phase changes the effective ISF (numerical feel) | [lab_14_cyclostationary_isf](/04_simulation_labs/lab_14_cyclostationary_isf) | Runnable toy: noise injection phase $\to$ $\Gamma_{eff,rms}$ (**pedagogical toy, not transistor-level**) |
| ISF / APF quadrature, coupled oscillators under injection locking | [quadrature_and_coupled_oscillators](/06_design_insights/quadrature_and_coupled_oscillators) | Quadrature injection, phase relations and design of coupled oscillators |

> **How to read**: this page completes the phase framework of [P3] into phase + amplitude. To understand "why the injection phase (or noise injection phase) changes the effective sensitivity," effective_isf and lab_14 are the theory and hands-on versions of the same cyclostationary concept; to see how quadrature becomes a usable design tool, return to quadrature_and_coupled_oscillators. For the phase/amplitude geometry, also see [phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise).

## What to remember

- **APF = the amplitude version of the ISF**, units $1/\text{A}$; the ISF projects onto the tangential direction (phase), the APF onto the radial direction (amplitude).
- **Ideal LC: the ISF and APF are in quadrature ($90°$ apart)** — when phase is most sensitive, amplitude is least sensitive, and vice versa
  (claim C11).
- **Phase accumulates permanently; amplitude is pulled back by the decay function** — this is the justification for "tracking only phase" in phase noise.
- **ILFD**: inject at $N\omega_0$, lock at $\omega_0$, get a ÷$N$ low-power divider; the dual-modulus prescaler can
  switch division ratios.
- This page is **advanced**; the exact APF equations ([P4] Eq.(18)–(22), p.2126; quadrature Eq.(26), p.2128) have been verified against the original, while the ILFD details remain advanced.
