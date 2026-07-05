---
title: "[P3] Injection Locking & Pulling — Part I (Time-Synchronous Modeling)"
description: Hong–Hajimiri 2019 Part I deep dive — ISF-based time-synchronous model, generalized Adler equation, lock range, injection waveform design (advanced; core equations verified against the [P3] original).
---

> **β**: This English translation is in beta — the Traditional-Chinese original is the authoritative version.

# A General Theory of Injection Locking and Pulling in Electrical Oscillators—Part I

> **Prerequisites**: [paper_001](/05_paper_deep_dives/paper_001_general_theory_phase_noise) (the ISF definition and the Eq.(11) phase kick from [P1]), [fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf) (the Fourier harmonics $c_n$ of the ISF) | **Next**: [paper_004](/05_paper_deep_dives/paper_004_injection_locking_part2) (Part II: APF amplitude, transient, frequency division).

This is an **advanced** deep dive. It extends the ISF of [P1] from "phase noise of a free-running
oscillator" to "injection locking / pulling of an oscillator driven by an external signal."
Core result: a **single first-order differential equation** written in terms of the ISF
(the generalized Adler equation) predicts the lock range, the locked phase, and stability,
for **any** oscillator topology and **any** injection waveform — and from it follows a recipe
for designing the injection waveform that maximizes the lock range.

> **Scope of this page**: advanced deep-dive, **not a core teaching chapter**. The core equations (generalized Adler Eq.(26), (28)–(30),
> (33), (35)) have been verified against the original [P3] PDF. Make sure you have digested the ISF from [P1] ([paper_001](/05_paper_deep_dives/paper_001_general_theory_phase_noise)) before reading this.

## Citation

> **[P3]** B. Hong and A. Hajimiri, *"A General Theory of Injection Locking and Pulling in
> Electrical Oscillators—Part I: Time-Synchronous Modeling and Injection Waveform Design,"*
> IEEE J. Solid-State Circuits, vol. 54, no. 8, pp. 2109–2121, Aug. 2019.
> (file `BHongGenTheor-I_JSSC2019_Postprint.pdf`, paper_003)

## One-sentence contribution

The same ISF $\Gamma$ that computes phase noise also yields a topology-independent generalized Adler equation
that predicts the lock range, locked phase, and stability for any oscillator and any injection waveform,
and shows how to design the injection waveform to enlarge the lock range (claim C10).

## Why this paper matters

**Injection locking** means: when an oscillator is injected with an external signal whose frequency is
close to its own, it "synchronizes to the external signal" — its phase and frequency get captured.
When the frequency offset is too large to follow, the phase slips periodically and produces unwanted spurs;
this is **injection pulling**. The phenomenon is everywhere — PLLs, clock distribution, quadrature
generation, frequency division — both exploited and feared.

In 1946 **Adler** described the behavior of an LC oscillator under **weak, sinusoidal, near-free-running**
injection with a single first-order phase equation. [P3] identifies five major limitations of the Adler
equation (weak injection only, LC only, sinusoidal injection assumed, requires hard-to-measure
$Q$ and $I_{osc}$, and predicts a symmetric lock range), then **fully generalizes** it using the ISF:

- Replace the LC-only parameters $Q$ / $I_{osc}$ with $\Gamma$ — any oscillator whose ISF can be extracted qualifies.
- Allow **arbitrary injection waveforms** (not just sinusoids), so the injection waveform can be **designed** to maximize the lock range.
- Naturally produces an **asymmetric lock range** (common in real circuits, missed by Adler).
- Covers subharmonic / superharmonic locking (injection frequency near $\omega_0/m$ or $m\omega_0$).

## Main assumptions

Per paper_metadata (paper_003.assumptions):

1. **Oscillator autonomy and periodic time variance** (same foundation as the ISF).
2. Injection (perturbation) maps to phase through the ISF; amplitude is deferred to Part II (APF).
3. **Time-synchronous averaging**: time-synchronous averaging over one period.

> **Physical intuition**: phase noise feeds the perturbation machine random noise; injection feeds it
> a **deterministic, periodic injection current $i_{inj}$**. Same "ISF-weight-then-integrate" machine —
> when the input changes from random to deterministic, the output changes from statistics
> ($\Gamma_{rms}$, PSD) to deterministic phase dynamics (locking / slipping).

## Key equations

### Classical Adler equation (baseline)

**Original formula** ([P3] Sec. III (SURVEY OF EXISTING MODELS), around p.2111, cross-checked against Eq.(15) of the original):

$$
\frac{d\theta}{dt}=\omega_0-\omega_{inj}-\frac{\omega_0}{2Q}\frac{I_{inj}}{I_{osc}}\sin\theta
$$

In the simplified form of Section 3 of the site conventions ($\omega_L\equiv\dfrac{\omega_0}{2Q}\dfrac{I_{inj}}{I_{osc}}$,
$\Delta\omega_{inj}\equiv\omega_0-\omega_{inj}$):

$$
\frac{d\phi}{dt}=-\omega_L\sin\phi+\Delta\omega_{inj}
$$

**Meaning**: the injection-locking phase difference $\theta$ (or $\phi$) satisfies a first-order nonlinear ODE.
$\omega_L$ is the (half) lock range. **Locking** = existence of a steady-state solution $d\theta/dt=0$,
which requires $|\Delta\omega_{inj}|\le\omega_L$.

**Step-by-step (summary of the simplified LC derivation in [P3])**: write the injection current as the phasor
$i_{inj}=I_{inj}e^{j\omega_{inj}t}$, write KCL for the LC tank (the injection current must supply the
reactive current when the tank is detuned from resonance), take the real part under the weak-injection
($I_{inj}\ll I_{osc}$) and slow-phase ($|d\theta/dt|\ll\omega_{inj}$) approximations, and the equation above
follows. The steady-state solution gives the lock characteristic and the **symmetric** lock range
$\omega_L=\dfrac{\omega_0}{2Q}\dfrac{I_{inj}}{I_{osc}}$.

**Numerical example**: $f_0=5$ GHz, $Q=10$, $I_{inj}/I_{osc}=0.1$. Half lock range

$$
\omega_L=\frac{\omega_0}{2Q}\frac{I_{inj}}{I_{osc}}=\frac{2\pi\times5\times10^{9}}{2\times10}\times0.1=1.57\times10^{8}\ \text{rad/s},
$$

or in frequency, $f_L=\omega_L/2\pi\approx25$ MHz. Intuition: the lock range grows linearly with injection
strength and shrinks inversely with $Q$ (a high-$Q$ LC is more "stubborn" — harder to pull away).

> **Note**: the classical Adler result is standard ([P3] Sec. III, p.2111 reviews Adler [20]); this page uses generic simplified notation.
> The **generalized Adler** in the next section has been verified verbatim against the original PDF.

### Generalized Adler equation / lock characteristic (core of this paper, verified against the original PDF ✓)

[P3] first converts Hajimiri's **dimensionless** ISF $\Gamma$ into a **unit-bearing** version ([P3] Eq.(26), p.2113):

$$
\tilde\Gamma(x)\equiv\frac{\Gamma(x)}{q_{max}}\qquad[\text{單位 rad/C}]
$$

Then the instantaneous phase kick of the injection current, and the change of coordinates to the relative phase $\theta=\phi-\omega_{inj}t$ ([P3] Eq.(28)–(29), p.2113):

$$
\frac{d\phi}{dt}=\tilde\Gamma(\phi)\,i_{inj}(t)
\;\xrightarrow{\ \theta=\phi-\omega_{inj}t\ }\;
\frac{d\theta}{dt}=(\omega_0-\omega_{inj})+\tilde\Gamma(\omega_{inj}t+\theta)\,i_{inj}(t)
$$

Time-synchronous averaging over "one fast injection period" (treating the slowly varying $\theta$ as constant) gives the **time-averaged generalized Adler equation** ([P3] Eq.(30), p.2113):

$$
\frac{d\theta}{dt}=(\omega_0-\omega_{inj})+\frac{1}{T_{inj}}\int_{T_{inj}}\tilde\Gamma(\omega_{inj}t+\theta)\,i_{inj}(t)\,dt
$$

Rearranged into lock-characteristic form ([P3] Eq.(33), p.2114):

$$
\frac{d\theta}{dt}=(\omega_0-\omega_{inj})+\Omega(\theta),\qquad
\boxed{\ \Omega(\theta)=\frac{1}{T_{inj}}\int_{T_{inj}}\tilde\Gamma(\omega_{inj}t+\theta)\,i_{inj}(t)\,dt\ }
$$

where $\Omega(\theta)$ is called the **lock characteristic** ([P3] Eq.(33), p.2114): the injection-induced average frequency shift as a function of the phase difference $\theta$. Note the **plus sign** in front of the averaged term (same sign convention as [P3] Eq.(30)).

**Meaning**: a single first-order ODE built from the **unit-bearing ISF $\tilde\Gamma=\Gamma/q_{max}$** and the **injection waveform $i_{inj}$**,
predicting the behavior of any oscillator under any injection waveform (claim C10). **Locking** = existence of a $\theta^\*$ with
$\omega_{inj}-\omega_0=\Omega(\theta^\*)$; lock range = the width of the range of $\Omega(\theta)$; **stability** is set by the sign of $d\Omega/d\theta$.

**Sinusoidal injection reduces to classical Adler ([P3] Eq.(34)–(35))**: for a single tone $i_{inj}=I_{inj}\cos\omega_{inj}t$,
only the ISF fundamental $\tilde\Gamma_1$ survives:

$$
\Omega(\theta)=\tfrac12 I_{inj}\,\lvert\tilde\Gamma_1\rvert\cos(\theta+\angle\tilde\Gamma_1),
\qquad
\omega_L=\tfrac12 I_{inj}\,\lvert\tilde\Gamma_1\rvert
$$

Half lock range $\omega_L=\frac12 I_{inj}\lvert\tilde\Gamma_1\rvert$ ([P3] Eq.(35)) — $\Omega\propto\cos\theta$ is symmetric about 0, exactly classical Adler.

**Why it is asymmetric in general**: for an arbitrary injection, $\Omega(\theta)$ contains **multiple harmonics**, its range is no longer symmetric about 0, so
$\omega_L^+\ne-\omega_L^-$ — the asymmetry common in real circuits that Adler cannot capture.

**Injection waveform design**: lock range = the width of the range of $\Omega(\theta)$. Aligning the harmonics of the injection waveform $i_{inj}$
**with the harmonics of the ISF $\tilde\Gamma$** (making the inner product larger) enlarges the lock range — one more degree of freedom
(waveform shape) beyond "just increase the injection current."

> **Verified**: $\tilde\Gamma=\Gamma/q_{max}$ (Eq.26), the pulling equations Eq.(28)–(30), the lock characteristic
> Eq.(33), the sinusoidal reduction Eq.(34), and the lock range Eq.(35) have all been confirmed verbatim against the rendered original [P3] PDF, p.2113–2114.

### Lock range = the range of $\Omega(\theta)$ (toy illustration)

Plotting the lock characteristic $\Omega(\theta)$ directly from the time-synchronous averaging integral of [P3] Eq.(33) makes the statement
"lock range = the width of the range of $\Omega(\theta)$; the edges = the max/min of $\Omega(\theta)$" visible at a glance:

![Lock characteristic Ω(θ): left, sinusoidal injection (Γ̃=−sinθ/q_max) gives a clean cosine, symmetric about 0 (ω_L⁺=−ω_L⁻, classical Adler); right, a harmonic-rich injection gives an asymmetric Ω with ω_L⁺≠−ω_L⁻; triangles/inverted triangles mark the upper and lower lock-range edges. Toy model, [P3] Eq.(33).](/figures/lock_characteristic_omega.png)

- **Left (a) sinusoidal injection**: single tone $i_{inj}=I_{inj}\cos\omega_{inj}t$ injected into the ideal-LC ISF $\tilde\Gamma=-\sin\theta/q_{max}$.
  Only the ISF fundamental survives (Eq.(34)); $\Omega(\theta)$ is a clean cosine, symmetric about 0, with edges
  $\pm\omega_L=\pm\tfrac12 I_{inj}\lvert\tilde\Gamma_1\rvert$ (toy value $=\pm0.50$ rad/s, exactly Eq.(35)) — this is classical Adler.
- **Right (b) harmonic-rich injection**: the injection carries the fundamental plus a deliberately phased second harmonic, and the ISF also contains a second harmonic. Multiple harmonics contribute simultaneously,
  so $\Omega(\theta)$ is **asymmetric about 0**: upper edge $\omega_L^+=+0.56$, lower edge $\omega_L^-=-0.63$ rad/s
  ($\omega_L^+\ne-\omega_L^-$) — the asymmetric lock range common in real circuits that Adler cannot capture.

**How to read it**: to lock, $\omega_{inj}-\omega_0=\Omega(\theta^\*)$ must have a solution; the reachable range of $\omega_{inj}-\omega_0$ is exactly
the range of the $\Omega$ curve (between the two horizontal dashed lines). Aligning the injection-waveform harmonics with the ISF harmonics
(making the inner product in Eq.(33) larger) pushes this curve taller and enlarges the lock range — one more degree of freedom
(waveform shape) beyond "just increase $I_{inj}$."

> **Toy-model disclosure**: this is a pedagogical toy model, **not transistor-level**. The ideal-LC $\Gamma=-\sin\theta$ is an exact result;
> the harmonic-rich ISF and the designed injection waveform are **illustrative only**, used solely to expose the asymmetry mechanism. $\Omega(\theta)$ is computed numerically from the time-averaging integral of Eq.(33).
> Full script: `simulations/fig_lock_characteristic.py` (generates `static/figures/lock_characteristic_omega.png`).

## Key figures

| Paper figure | Page | Content | Teaching purpose |
|---|---|---|---|
| Fig. 6 | 2113 | Block diagram: the harmonics of the injection current are **filtered** by the harmonics of the ISF to form the lock characteristic | Explains why $\Omega(\theta)$ keeps only the aligned harmonics |
| Fig. 7 | 2114 | **Time-domain** view of the lock characteristic: the ISF×injection area for the upper/lower edges and the free-running case | Intuition: lock range = extrema of the net area per cycle |

> This site **deliberately does not redraw** Fig. 6 / Fig. 7 of [P3] (no matching transistor-level toy simulation);
> the page numbers/content above have been checked against the [P3] original. The $\Omega(\theta)$ figure in Key equations above is an **independent toy illustration**
> (it only demonstrates the concept "lock range = range of $\Omega(\theta)$"), **not** a redraw of Fig. 6 / Fig. 7.

## Design insights

- **The lock range is designable**: lock range = the width of the range of $\langle\Gamma\,i_{inj}\rangle$ over $\phi$.
  Aligning the harmonics of the injection waveform $i_{inj}$ with the harmonics of the ISF $\Gamma$ (making the inner product larger)
  enlarges the lock range — one more degree of freedom (waveform shape) beyond "just increase the injection current."
- **Topology-independent**: as long as the ISF can be extracted, the same equation applies to ring, LC, and relaxation oscillators;
  no need to measure the hard-to-measure $Q$ and $I_{osc}$.
- **Subharmonic / superharmonic locking**: when the injection frequency is near $\omega_0/m$ or $m\omega_0$, it is the
  corresponding harmonic of $\Gamma$ that does the averaging — this connects directly to frequency division (ILFD) in [P4].
- **Pulling is the other face of the same equation**: when $|\Delta\omega| > $ lock range, $d\phi/dt$ is nonzero and the phase
  slips periodically, producing pulling spurs. In design, make sure the operating frequency falls inside the lock range.

## Limitations

Per paper_metadata (paper_003.limitations):

- **Part I covers phase only**; amplitude modulation is deferred to Part II (APF, [P4]).
- Relies on an **accurately extracted ISF** — if the ISF is off, the predictions are off.
- This site treats it as an **advanced deep-dive, not a core teaching chapter**; the core generalized-Adler equations have been verified against the [P3] original.

## Relationship to other papers

- **[P1]** provides the ISF $\Gamma$ and the Eq.(11) phase kick — the mathematical starting point of this paper.
- **[P2]** provides the ring ISF, connecting to ring injection here (and the ILFD of [P4]).
- **[P4]** is the direct sequel: it adds amplitude (APF), transient pulling, and frequency division; see
  [paper_004](/05_paper_deep_dives/paper_004_injection_locking_part2).
- The generalized Adler equation is entry 20 in [equation_index](/01_paper_map/equation_index) ([P3] Eq.(30)/(33)/(35)).

## What to remember

- **The same ISF computes both phase noise and injection locking** — the input changes from random noise to a deterministic
  $i_{inj}$ (claim C10).
- **Generalized Adler equation**: $\dfrac{d\theta}{dt}=(\omega_0-\omega_{inj})+\dfrac{1}{T_{inj}}\displaystyle\int_{T_{inj}}\tilde\Gamma(\omega_{inj}t+\theta)\,i_{inj}(t)\,dt$ ([P3] Eq.(30), p.2113, with a **plus sign** in front of the averaged term).
- **Noise shaping (new in v5)**: once locked, the oscillator = a first-order PLL — its own noise is high-pass suppressed while reference noise enters low-pass, with corner=ω_L cosθ_ss; full derivation and simulation in [injection_locking_noise](/06_design_insights/injection_locking_noise).
- **Locking** = existence of a steady-state solution / $|\omega_0-\omega_{inj}|\le\omega_L$; **lock range** = the width of the range of the lock characteristic $\Omega(\theta)$; for sinusoidal injection $\omega_L=\tfrac12 I_{inj}\lvert\tilde\Gamma_1\rvert$ ([P3] Eq.(35), p.2114).
- Stronger than Adler in: topology independence, arbitrary waveforms, asymmetric lock range, and designable waveforms that enlarge the lock range.
- This page is **advanced**; the core equations (Eq.26, 28–30, 33, 35) have been verified against the original [P3] PDF, p.2113–2114.

## Further reading

- The mathematical starting point, the ISF $\Gamma$: [paper_001](/05_paper_deep_dives/paper_001_general_theory_phase_noise) ([P1]).
- The Fourier harmonics $c_n$ of the ISF (why only aligned harmonics survive in $\Omega(\theta)$): [fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf).
- The direct sequel, Part II (APF amplitude, transient pulling, frequency division): [paper_004](/05_paper_deep_dives/paper_004_injection_locking_part2) ([P4]).
- Where the generalized Adler equation sits in the equation index: [equation_index](/01_paper_map/equation_index) (entry 20, [P3] Eq.(30)/(33)/(35)).
- Where this advanced page sits in the overall path (optional): [learning_path](/00_overview/learning_path).
- Quick overview of the five papers' division of labor: [paper_summary_table](/01_paper_map/paper_summary_table).
