---
title: "[P2] Jitter and Phase Noise in Ring Oscillators"
description: "Hajimiri–Limotyrakis–Lee 1999 deep dive: accumulated jitter, Γrms∝N^(-3/2), N-independence (verified), symmetry, and Fig.17."
---

> **β**: This English translation is in beta — the Traditional-Chinese original is the authoritative version.

# Jitter and Phase Noise in Ring Oscillators

> **Prerequisites (recommended reading order)**: first digest [paper_001](/05_paper_deep_dives/paper_001_general_theory_phase_noise) (ISF, $\Gamma_{rms}^2/q_{max}^2$, the symmetry rule) — every conclusion on this page is [P1]'s ISF applied to the ring. For the time-/frequency-domain language of jitter see [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter).

[P2] applies the ISF framework of [P1] **to the ring oscillator**. It answers three very practical
questions: (1) how does the long-term jitter of a free-running ring grow with time? (2) what effect
does the number of stages $N$ have on phase noise? (3) why does waveform symmetry suppress close-in
noise? The answers are, respectively, $\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$,
$\Gamma_{rms}\propto N^{-3/2}$ (with "nearly $N$-independent at fixed power and frequency"), and the symmetry experiment of Fig. 17.

## Citation

> **[P2]** A. Hajimiri, S. Limotyrakis, and T. H. Lee, *"Jitter and Phase Noise in Ring
> Oscillators,"* IEEE J. Solid-State Circuits, vol. 34, no. 6, pp. 790–804, Jun. 1999.
> (file `jitter_ring.pdf`, paper_002)

## One-sentence contribution

Applying [P1]'s ISF to the ring oscillator yields closed forms for jitter and phase noise, the
$\Gamma_{rms}\propto N^{-3/2}$ scaling, and the counter-intuitive conclusion that "at fixed $f_0$
and power, the phase noise/jitter of a single-ended ring is nearly independent of the number of
stages $N$" (claim C7, C8).

## Why this paper matters

An LC oscillator needs an inductor — large area, hard to integrate; **a ring oscillator is all
inverters: small area, easy to integrate, wide tuning range** — the most common VCO in PLLs/CDRs.
But a ring's phase noise is usually much worse than an LC's — [P2] uses the ISF to explain
**why**, and gives actionable design rules:

- It ties the ring's jitter to **the same $\Gamma_{rms}^2/q_{max}^2$ ratio as phase noise** (claim C6),
  unifying "time-domain jitter" and "frequency-domain phase noise" under the ISF framework.
- It settles a commonly misunderstood question: "does adding more stages $N$ to a ring make it
  better?" Under the constraint of fixed power and frequency the answer is "**almost no
  difference**" (claim C7) — more stages shrink $\Gamma_{rms}$, but each stage's swing shrinks and
  there are more devices; the effects cancel.
- It confirms [P1]'s symmetry rule with measurements (Fig. 17): tuning the control voltage to the
  point of symmetric rise/fall produces a **minimum** in phase noise (claim C4).

## Main assumptions

Per paper_metadata (paper_002.assumptions):

1. The same LTV/ISF small-perturbation assumptions as [P1].
2. Per-stage device noise is white (plus a 1/f component handled via symmetry).
3. Identical stages; delay and noise add independently at every transition.

> **Physical intuition**: nearly all of a ring's energy is injected in the instant of a transition
> (edge flip), so its ISF is not the smooth $-\sin$ of an LC but a set of **sharp peaks concentrated
> at the transitions** ([P2] Fig. 5). The sensitive spots — where a kick hurts phase the most — sit
> on those peaks. The more stages, the smaller the fraction of the full period a single transition
> occupies, and the smaller the rms ISF.

## Key equations

### Eq.(8): accumulated jitter (the random-walk fingerprint)

**Original formula** ([P2] Eq.(8), p.792; κ from Eq.(12), p.793):

$$
\sigma_{\Delta t}=\kappa\sqrt{\Delta t}
$$

**Meaning**: for two edges of a free-running oscillator separated by $\Delta t$, the standard
deviation of the timing error is **proportional to $\sqrt{\Delta t}$** — the **random-walk
fingerprint** of an oscillator with "no absolute time reference" (claim C6). $\kappa$ is a
device-dependent proportionality constant with units of $\sqrt{\text{s}}$.

**Step-by-step derivation**: each transition injects an independent, zero-mean timing perturbation
with variance $\sigma_{step}^2$. Over $\Delta t$ there are about $M=\Delta t/T$ transitions;
independent quantities add in variance:

$$
\begin{aligned}
\sigma_{\Delta t}^2 &= M\,\sigma_{step}^2 = \frac{\Delta t}{T}\,\sigma_{step}^2 \\
\Rightarrow\quad \sigma_{\Delta t} &= \underbrace{\frac{\sigma_{step}}{\sqrt{T}}}_{\equiv\,\kappa}\sqrt{\Delta t}=\kappa\sqrt{\Delta t}.
\end{aligned}
$$

**Dimension check**: $\kappa$ is $\sqrt{\text{s}}$ and $\sqrt{\Delta t}$ is $\sqrt{\text{s}}$;
their product is $\text{s}$ ✓. Cross-check against [P1] in the frequency domain:
$\sigma_{\Delta t}\propto\sqrt{\Delta t}$ corresponds to 1/f² phase noise (the two are the
time-/frequency-domain faces of the same thing).

**Numerical example**: the toy ring sets per-edge $\sigma_{step}=50$ fs (see the parameters of
`ring_oscillator_timing_noise_accumulation.png`). Accumulated jitter over $\Delta t=1$ µs (about
5000 periods at $f_0=5$ GHz): first find $\kappa$. With $T=200$ ps,
$\kappa=50\text{fs}/\sqrt{200\text{ps}}=50\times10^{-15}/\sqrt{2\times10^{-10}}=3.54\times10^{-9}\ \sqrt{\text{s}}$,
so $\sigma_{\Delta t}=3.54\times10^{-9}\times\sqrt{10^{-6}}=3.54\ \text{ps}$. Intuition: the longer the separation, the larger the drift — but it grows only slowly, as $\sqrt{\Delta t}$.

**Python verification**:

```python
import numpy as np
from simulations.common.oscillator_models import accumulated_jitter_curve

# toy random walk: each edge adds an independent 50 fs timing perturbation
lags, sigma = accumulated_jitter_curve(f0=5e9, sigma_edge=50e-15, max_lag_periods=500, n_trials=2000)
# expect sigma(lag) ~ sigma_edge * sqrt(lag) -> log-log slope 0.5
slope = np.polyfit(np.log(lags[1:]), np.log(sigma[1:]), 1)[0]
print(round(slope, 2))  # -> 0.50
```

The full toy derivation is in [lab_03_ring_oscillator_toy_model](/04_simulation_labs/lab_03_ring_oscillator_toy_model)
(**pedagogical toy model, not transistor-level**).

### Eq.(11)–(12): the jitter constant κ and its relation to the ISF (verified ✓)

**Original formula** ([P2] Eq.(11)–(12), p.793, proportionality):

$$
\kappa^2\;\propto\;\frac{\Gamma_{rms}^2}{q_{max}^2}\cdot\frac{\overline{i_n^2}}{\Delta f}
$$

**Meaning**: the jitter proportionality constant $\kappa$ is set by **exactly the same
$\Gamma_{rms}^2/q_{max}^2$ ratio as phase noise** (claim C6). This ties time-domain jitter and
frequency-domain phase noise to the same ISF quantity: the knobs that lower phase noise lower
jitter as well.

> **Verified**: [P2] Eq.(12), p.793 gives $\kappa=\frac{\Gamma_{rms}}{q_{max}}\sqrt{\tfrac12\tfrac{\overline{i_n^2}}{\Delta f}}$ (verified verbatim against the original PDF rendering);
> it shares the same $\Gamma_{rms}^2/q_{max}^2$ ratio with phase noise (claim C6).

### Eq.(14): ring frequency vs number of stages

**Original formula** ([P2] Eq.(14), p.794):

$$
f_0=\frac{1}{2N\tau_D}
$$

**Meaning**: an $N$-stage ring with per-stage delay $\tau_D$ oscillates at this frequency. **The
factor of 2** comes from the signal having to travel around the ring **twice** per period (one lap
inverts; a second lap returns it in phase) to complete one full cycle.

**Dimension check**: $1/(N\cdot\text{s})=\text{Hz}$ ✓ ($N$ dimensionless).

**Numerical example**: for a 5-stage ring at $f_0=5$ GHz, the per-stage delay is
$\tau_D=1/(2\times5\times5\times10^9)=2\times10^{-11}\ \text{s}=20$ ps. Doubling to $N=10$
while keeping 5 GHz halves the per-stage delay to 10 ps — this is exactly where "at fixed
frequency, larger $N$ forces faster, smaller-swing stages" comes from, leading into the
N-independence below.

### Eq.(16): rms-ISF scaling with the number of stages (re-verified in v7 ✓)

**Original formula** ([P2] Eq.(16), p.794; the radical covers only the constant term):

$$
\Gamma_{rms}=\sqrt{\dfrac{2\pi^2}{3\eta^3}}\;\dfrac{1}{N^{1.5}}
$$

where $\eta$ is the frequency proportionality constant (Eq.(14)–(15): $\hat t_D=\eta/f_{max}$, $2\pi=2N\eta/f_{max}$);
at $\eta=0.75$, $\sqrt{2\pi^2/(3\times0.75^3)}\approx3.95\approx4$, i.e. $\Gamma_{rms}\approx4/N^{1.5}$,
which is the solid line in [P2] Fig. 8 — the radical covers only the constant, and $1/N^{1.5}$ sits outside it.

**Meaning**: **$\Gamma_{rms}\propto N^{-3/2}$** (i.e. $\Gamma_{rms}^2\propto N^{-3}$).
Intuition: with more stages, each transition occupies a narrower "sensitive window" of the $2\pi$ period and the peaks get shorter, so the rms naturally shrinks.

> **[P2] Eq.(16), p.794 (re-verified in v7: the radical covers only the constant, $\Gamma_{rms}\propto N^{-3/2}$;
> triple-confirmed by the prose's $4/N^{1.5}$@$\eta=0.75$ and App.B Eq.(55). v3 had misread this as $N^{-3/4}$)**:
> three independent lines of evidence — (1) the paper's own text (p.794, the paragraph after Eq.16) states
> "the $1/N^{1.5}$ dependence of $\Gamma_{rms}$"; (2) the $\eta=0.75$ numerical anchor: the text says
> "solid line = $\Gamma_{rms}\approx4/N^{1.5}$, obtained from (16) for $\eta=0.75$", and
> $\sqrt{2\pi^2/(3\times0.75^3)}=3.95\approx4$ ✓ (if $N^{1.5}$ were inside the radical this would give
> $4/N^{0.75}$, contradicting the text); (3) independent algebra in App.B Eq.(52)+(54) (p.803):
> $\Gamma_{rms}^2=(1/3\pi)(1/f'_{rise})^3(1+A^3)$, $2\pi=\eta N(1+A)/f'_{rise}$, which combine to give
> $\Gamma_{rms}^2=(2\pi^2/3\eta^3)\cdot[4(1+A^3)/(1+A)^3]\cdot N^{-3}$; at $A=1$ the bracket equals 1, so
> $\Gamma_{rms}^2\propto N^{-3}\Rightarrow\Gamma_{rms}\propto N^{-3/2}$ ✓. All three point to $N^{-3/2}$;
> there is no real "formula-vs-text" inconsistency — it was a prior misreading of the radical's scope.

### Eq.(23): ring white-noise phase-noise FOM and N-independence (prefactor corrected to 8/(3η) and verified)

**Original formula** ([P2] Eq.(23), p.796; the $V_T=0$ lower bound is Eq.(25)):

$$
\mathcal{L}\{\Delta f\}=\frac{8}{3\eta}\cdot\frac{kT}{P}\cdot\frac{V_{DD}}{V_{char}}\cdot\left(\frac{f_0}{\Delta f}\right)^2
\qquad\Big(\min_{V_T=0}:\ \frac{16\gamma}{3\eta}\cdot\frac{kT}{P}\cdot\frac{f_0^2}{\Delta f^2}\Big)
$$

where $\gamma$ is the MOSFET channel thermal-noise coefficient ($2/3$ long-channel, larger for
short-channel), $V_{char}$ is the device's **characteristic voltage** (long-channel
$\approx\Delta V/\gamma$), $P$ is the power dissipation (Eq.(21): $P=2\eta N V_{DD}q_{max}f_0$),
and the per-stage noise is given by Eq.(17),(18) $\overline{i_n^2}/\Delta f=4kT\gamma\mu C_{ox}(W/L)\Delta V$.

**Meaning**: ring white-noise phase noise collapses into a figure of merit — only $kT/P$, the
voltage ratio $V_{DD}/V_{char}$, and $(f_0/\Delta f)^2$ appear. **Key conclusion (claim C7): $N$
is entirely absent from Eq.(23) — at fixed $f_0$ and power $P$, the phase noise of a single-ended
ring is independent of the number of stages $N$.**

**Why N-independent**: microscopically, raising $N$ lowers $\Gamma_{rms}$ (Eq.16) but
simultaneously lowers each stage's swing $q_{max}$ and adds more noisy stages; [P2] shows these
effects cancel exactly at fixed $P$, $f_0$, so Eq.(23) contains no $N$. Hence "how many stages
should my ring have" is not decided by phase noise, but by phase margin, tuning range, area,
quadrature needs, and other considerations.

> **Correction note (v3)**: the prefactor of [P2] Eq.(23) is $8/(3\eta)$ ($\eta$ being the
> stage-delay proportionality constant of Eq.14, $\approx1$); $\gamma$ enters only through
> $V_{char}=\Delta V/\gamma$. (v2 mistakenly changed it to $8/(3\gamma)$ and mislabeled it
> "verified verbatim"; v3 corrected it against the original PDF p.796.) The $V_T=0$ lower bound is
> accordingly corrected to $16\gamma/(3\eta)$. $\gamma$ (noise coefficient) and $\eta$ (frequency
> proportionality constant, Eq.14) are different quantities — do not confuse them.

## Key figures

| Paper figure | Page | Content | Site counterpart | Note |
|---|---|---|---|---|
| Fig. 5 | 793 | Overlaid ISFs at the same frequency for different stage counts $N$ (3/5/15) | scaling intuition ($\Gamma_{rms}\propto N^{-3/2}$) | ✓ |
| Fig. 6 | 793 | Approximate waveform and ISF of one single-ended ring stage (energy concentrated at the transition) | toy triangular ISF (lab_03) | ✓ |
| Fig. 8 | 794 | rms ISF vs $N$ for rings of different stage counts; the solid line is Eq.(16) at $\eta=0.75$, $\Gamma_{rms}\approx4/N^{1.5}$ | scaling argument for `lc_vs_ring_isf_comparison.png` | ✓ |
| **Fig. 17** | 802 | phase noise vs the symmetry (control) voltage, with a **minimum** at the symmetric point | direct experimental support for the symmetry design rule | ✓ |

**Fig. 17 is the smoking gun for the symmetry rule**: sweep the control voltage; at the point where
the PMOS pull-up current = NMOS pull-down current and the waveform is symmetric, $c_0$ is squeezed
to its minimum, 1/f³ upconversion is suppressed, and the phase noise shows a **bowl bottom**. This
directly verifies [P1] Eq.(24) (claim C4).

This site compares LC ($-\sin$) and ring (triangular ISF, peaks shrinking with $N$) with a toy
model — **not transistor-level**:

![ISF comparison of LC vs ring (toy)](/figures/lc_vs_ring_isf_comparison.png)
![Ring accumulated jitter growing as √Δt over time (toy)](/figures/ring_oscillator_timing_noise_accumulation.png)

## Design insights

- **Jitter and phase noise share one origin**: lowering $\Gamma_{rms}^2/q_{max}^2$ lowers both; do
  not treat long-term jitter and close-in phase noise as two separate problems.
- **Adding stages is not a phase-noise cure**: at fixed $f_0$, $P$ the phase noise is nearly
  independent of $N$ (conclusion verified); the real reasons to add stages are quadrature/multi-phase
  outputs, tuning range, and phase margin.
- **Symmetry is the master knob for close-in noise**: tune the rise/fall to be symmetric (e.g. the
  control voltage of Fig. 17) to suppress $c_0$ and push the 1/f³ corner far out. Differential
  rings are usually more symmetric than single-ended ones.
- **The steeper the transition, the better**: the energy is concentrated at the transitions; the
  higher the slope, the larger $q_{max}$ and the relatively smaller $\Gamma_{rms}$.

Design-side summaries in [lc_vs_ring](/06_design_insights/lc_vs_ring) and [symmetry](/06_design_insights/symmetry);
the SerDes view is in [serdes_clocking_connection](/06_design_insights/serdes_clocking_connection).

## Limitations

Per paper_metadata (paper_002.limitations):

- Toy/first-order: short-channel effects and detailed device noise are approximate.
- **The N-independence conclusion** holds only at fixed power, fixed frequency, and for the specific noise model ([P2] Sec.V, Eq.(23)/(25), p.796, verified, claim C7).
- Substrate/supply noise is treated separately and qualitatively.

## Relationship to other papers

- **[P1]** is the foundation: this page's jitter $\kappa$, $\Gamma_{rms}$, and symmetry all use
  [P1]'s ISF and Eq.(21)/(24).
- **[P3]/[P4]** also use the ring as a vehicle ([P4]'s ILFD/prescaler is an inverter-chain ring),
  extending the ISF from phase noise to injection.
- **[P5]** is unrelated to this page; but latch-based/differential ring start-up also relies on
  cross-coupled positive feedback (the corner-case bridge of claim C12).

## Further reading / companion teaching pages

| Which block of this page | Companion teaching page | What that page adds |
|---|---|---|
| The LC ($-\sin$) vs ring (transition-concentrated) ISF comparison and the N-scaling argument | [lc_vs_ring](/06_design_insights/lc_vs_ring) | The $\Gamma_{rms}$, $q_{max}$, and phase-noise trade-offs of the two topologies organized into a design table |
| The random walk behind Eq.(8) accumulated jitter $\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$ | [lab_03_ring_oscillator_toy_model](/04_simulation_labs/lab_03_ring_oscillator_toy_model) | A runnable toy model: add an independent perturbation per edge; the log-log slope verifies $\sqrt{\Delta t}$ (**pedagogical toy, not transistor-level**) |
| The Fig. 17 phase-noise bowl at the symmetric point, $c_0$, and the 1/f³ corner | [symmetry](/06_design_insights/symmetry) | how rise/fall symmetry suppresses $c_0$, differential vs single-ended, design knobs |

> **How to read**: this page is the story of "how the paper applies [P1] to the ring"; to watch jitter grow as $\sqrt{\Delta t}$ hands-on, go back to lab_03; to turn the conclusions into topology selection, go back to lc_vs_ring and symmetry. For the SerDes view see also [serdes_clocking_connection](/06_design_insights/serdes_clocking_connection).

## What to remember

- **Accumulated jitter $\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$**: the random-walk fingerprint of a free-running oscillator ([P2] Eq.(8), p.792).
- $\kappa$ is set by **the same $\Gamma_{rms}^2/q_{max}^2$ as phase noise** ([P2] Eq.16/23, verified).
- **$\Gamma_{rms}\propto N^{-3/2}$** ([P2] Eq.(16), p.794, re-verified in v7: the radical covers only the
  constant, triple-confirmed by the prose's $4/N^{1.5}$@$\eta=0.75$ and App.B Eq.(55)); yet at fixed $f_0$, $P$ the phase noise is
  **nearly independent of $N$** (no $N$ in [P2] Eq.(23), claim C7, verified).
- **Fig. 17**: the phase-noise bowl bottom at the symmetric point — the smoking gun for the symmetry rule (claim C4).
- Rings integrate better than LC but usually have worse phase noise; this page shows where the knobs are.
