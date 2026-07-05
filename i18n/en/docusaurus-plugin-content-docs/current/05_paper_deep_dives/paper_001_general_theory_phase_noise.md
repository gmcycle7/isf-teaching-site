---
title: "[P1] A General Theory of Phase Noise in Electrical Oscillators"
description: "Hajimiri–Lee 1998 deep dive: ISF, q_max normalization, 1/f² and 1/f³ phase noise, and the three design rules."
---

> **β**: This English translation is in beta — the Traditional-Chinese original is the authoritative version.

# A General Theory of Phase Noise in Electrical Oscillators

> **Prerequisites (recommended reading order)**: [oscillator_phase](/02_foundations/oscillator_phase) (the geometry of the limit cycle and excess phase) → [lti_vs_ltv](/02_foundations/lti_vs_ltv) (why an oscillator is LTV, not LTI) → [stochastic_noise_basics](/02_foundations/stochastic_noise_basics) (white/flicker noise PSD). This page is the **foundation** of the entire site — the other four deep dives all build on it.

This is the **foundation** of the whole course. It is the first work to model an oscillator's
response to noise correctly as an **LTV (linear time-variant)** system, introducing the
**ISF (Impulse Sensitivity Function)** $\Gamma(\omega_0\tau)$ and using it to derive, in one
stroke, closed-form expressions for 1/f² and 1/f³ phase noise together with three design rules
still in use today. The remaining four papers ([P2][P3][P4]) all build on the concepts on this
page.

## Citation

> **[P1]** A. Hajimiri and T. H. Lee, *"A General Theory of Phase Noise in Electrical
> Oscillators,"* IEEE J. Solid-State Circuits, vol. 33, no. 2, pp. 179–194, Feb. 1998.
> (file `general.pdf`, paper_001)

## One-sentence contribution

An oscillator's response to noise is not LTI but **LTV**: the same noise impulse injected at
different phases of the waveform produces different phase shifts; this "phase sensitivity" is
the ISF $\Gamma(\omega_0\tau)$. With it, arbitrary noise can be propagated into phase noise,
yielding the design rule $\mathcal{L}\propto\Gamma_{rms}^2/q_{max}^2$ (claim C1, C3).

## Why this paper matters

Before [P1], engineering practice relied mainly on the **Leeson model** (1966, semi-empirical) —
it draws the 1/f³, 1/f², and flat slope regions, but cannot explain why the 1/f³ corner does not
equal the device's 1/f corner, or why some waveforms upconvert less flicker noise into close-in
phase noise. [P1] supplies the physical answers:

- **LTV, not LTI** (claim C1): an oscillator is an autonomous system with no absolute time
  reference. A noise impulse landing on the waveform peak changes almost only the amplitude;
  one landing at a zero crossing converts almost entirely into phase. So "same impulse,
  different injection instant, different effect" — that is time variance. The LTI convolution
  $h(t-\tau)$ cannot capture it.
- **Phase accumulates permanently, amplitude is pulled back** (claim C2): an oscillator has an
  amplitude-restoring mechanism that pulls amplitude perturbations back onto the limit cycle,
  but phase has **no restoring force** — every kick is kept forever. Phase noise lives in this
  accumulating phase.
- **Quantify both points in a single function $\Gamma$**: phase noise is no longer fitted — it
  can be **computed** from the waveform and the noise PSD, and the computation points at the
  design knobs.

It also subsumes Leeson and cyclostationary noise as its own special cases (claim C9).

## Main assumptions

Per paper_metadata (paper_001.assumptions):

1. **Noise is a small perturbation** — the phase response can be linearized (requires $\Delta q\ll q_{max}$).
2. **Amplitude perturbations decay** (stable limit cycle); only phase persists, so "tracking phase alone" suffices.
3. **The ISF is known, periodic, and frequency-independent** — $\Gamma$ is a $2\pi$-periodic function determined solely by the steady-state waveform.
4. **Hard-switching / large-signal cyclostationary operation** defines the ISF — $\Gamma$ is the sensitivity measured on that steady-state trajectory.

> **Physical intuition**: draw the oscillator state in a 2-D plane; the steady state circulates
> along the limit cycle. A current impulse nudges the state point; the **tangential component
> along the cycle** becomes phase (kept forever), the **radial component off the cycle** becomes
> amplitude (pulled back). The same impulse kicked at different phases splits differently between
> tangential and radial — collect that ratio into a periodic function of the injection phase alone,
> and you have the ISF. Full geometry in [oscillator_phase](/02_foundations/oscillator_phase).

## Key equations

Below are the most critical equations of [P1] (Eq.(1) and Eq.(9)–(24)). The LaTeX of each is
taken **verbatim** from Section 3 of the specification, with `[P1] Eq.(n) page` citations;
constants are never altered.

### Eq.(1): output decomposition (where phase noise lives)

**Original formula** ([P1] Eq.(1), p.181):

$$
V_{out}(t)=A(t)\,f\!\big(\omega_0 t+\phi(t)\big)
$$

**Meaning**: any oscillator output can be decomposed into an "instantaneous amplitude $A(t)$"
times "the periodic waveform $f$ evaluated at $\omega_0 t+\phi(t)$". $f$ is the steady-state
waveform (not necessarily a sinusoid). **Phase noise lives in the excess phase $\phi(t)$**;
amplitude noise lives in $A(t)$.

**Step-by-step**: the ideal oscillation is $f(\omega_0 t)$; once noise enters, the amplitude is
perturbed into $A(t)$ and the phase gains $\phi(t)$. Because amplitude has a restoring force
(assumption 2), $A(t)\to A_0$, so for phase-noise analysis $A(t)$ can be treated as a constant
and only $\phi(t)$ tracked. This step collapses the problem from a "2-D state" to a "1-D phase".

### Eq.(9): charge → voltage step (the physical entry point of noise)

**Original formula** ([P1] Eq.(9), p.182):

$$
\Delta V=\frac{\Delta q}{C_{node}}
$$

**Meaning**: a current impulse deposits charge $\Delta q=\int i\,dt$ on the node capacitance,
instantly stepping the node voltage by $\Delta V$. This is the **physical entry point** through
which noise enters the oscillator state.

**Dimension check**: $[\text{C}]/[\text{F}]=[\text{C}]/[\text{C/V}]=[\text{V}]$ ✓.

### Eq.(10)–(11): the ISF and the LTV phase response (the core)

**Original formula** ([P1] Eq.(10), p.182, excess-phase impulse response):

$$
h_\phi(t,\tau)=\frac{\Gamma(\omega_0\tau)}{q_{max}}\,u(t-\tau)
$$

**Original formula** ([P1] Eq.(11), p.182, convolution form):

$$
\phi(t)=\frac{1}{q_{max}}\int_{-\infty}^{t}\Gamma(\omega_0\tau)\,i_n(\tau)\,d\tau
$$

**Meaning**: $\Gamma(\omega_0\tau)$ is the dimensionless, $2\pi$-periodic ISF; $q_{max}=C_{node}V_{max}$
is the maximum charge swing on the node. **The $u(t-\tau)$ (unit step) is crucial**: once a phase
step is created it persists forever (phase has no restoring force), so the impulse response carries
a step rather than a decaying term. Eq.(11) is the superposition integral over all past noise.

**Step-by-step derivation** (no skipped steps):

$$
\begin{aligned}
&\text{(i) current impulse deposits charge:}\quad \Delta q=\int i_n(\tau)\,d\tau \\
&\text{(ii) charge raises the node voltage (Eq.9):}\quad \Delta V=\frac{\Delta q}{C_{node}} \\
&\text{(iii) project onto the limit-cycle tangent to get the phase step:}\quad \Delta\phi=\frac{\Gamma(\omega_0\tau)}{q_{max}}\,\Delta q \\
&\text{(iv) the step persists forever; write the impulse response:}\quad h_\phi(t,\tau)=\frac{\Gamma(\omega_0\tau)}{q_{max}}\,u(t-\tau) \\
&\text{(v) linear superposition (convolution) over arbitrary }i_n\text{:}\quad \phi(t)=\int_{-\infty}^{\infty} h_\phi(t,\tau)\,i_n(\tau)\,d\tau=\frac{1}{q_{max}}\int_{-\infty}^{t}\Gamma(\omega_0\tau)\,i_n(\tau)\,d\tau
\end{aligned}
$$

**Why $\Gamma$ is dimensionless**: $\Delta\phi$ is in rad (dimensionless) and $\Delta q/q_{max}$
is also dimensionless, so $\Gamma$ must be dimensionless ✓. Note that $h_\phi$ depends on the
**absolute injection instant $\tau$** (through $\Gamma(\omega_0\tau)$), not merely on $t-\tau$ —
exactly the fingerprint of an **LTV** system (claim C1). The full step-by-step derivations are in
[impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift) and
[convolution_derivation](/03_isf_core_theory/convolution_derivation).

**Numerical example (Example A)**: $q_{max}=1$ pC, $\Delta q=1$ fC, $\Gamma=0.5$, $f_0=5$ GHz.

$$
\Delta\phi=\frac{0.5\times(1\times10^{-15})}{1\times10^{-12}}=5\times10^{-4}\ \text{rad}\;(\approx0.0286^\circ),\quad \Delta t=\frac{\Delta\phi}{2\pi f_0}=15.9\ \text{fs}.
$$

**Python verification**:

```python
from simulations.common.isf_utils import impulse_to_phase_step
from simulations.common.noise_utils import phase_to_time_error

dphi = impulse_to_phase_step(delta_q=1e-15, gamma_value=0.5, qmax=1e-12)
dt   = phase_to_time_error(dphi, f0=5e9)
print(dphi, "rad", dt*1e15, "fs")   # -> 0.0005 rad  15.92 fs
```

### Eq.(12)–(13): Fourier series of the ISF and its harmonics

**Original formula** ([P1] Eq.(12), p.183):

$$
\Gamma(\omega_0\tau)=\frac{c_0}{2}+\sum_{n=1}^{\infty}c_n\cos(n\omega_0\tau+\theta_n)
$$

**Original formula** ([P1] Eq.(13), p.183):

$$
\phi(t)=\frac{1}{q_{max}}\!\left[\frac{c_0}{2}\!\int_{-\infty}^{t}\!i_n\,d\tau+\sum_{n=1}^{\infty}c_n\!\int_{-\infty}^{t}\!i_n\cos(n\omega_0\tau+\theta_n)\,d\tau\right]
$$

**Meaning**: expand the ISF in a Fourier series; each harmonic coefficient $c_n$ tells you "how
strongly the oscillator moves noise near $n\omega_0$ onto the carrier". $c_0$ (the DC term — the
DC **value** of the ISF is $c_0/2$) is especially important — it is the **only** channel that
upconverts the device's low-frequency 1/f noise into close-in 1/f³ phase noise (see Eq.(23)–(24)).

**Step-by-step**: substitute Eq.(12) into Eq.(11) and expand term by term to get Eq.(13).
Physically this is a **frequency-translation map** ([P1] Fig. 8): noise near $n\omega_0$ is
down-converted by the $n$-th harmonic into slow phase modulation at baseband. The full derivation
and the notation trap ($c_0$ vs $c_0/2$) are in
[fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf).

### Eq.(20): Parseval / rms ISF

**Original formula** ([P1] Eq.(20), p.185):

$$
\sum_{n=0}^{\infty}c_n^2=\frac{1}{\pi}\int_0^{2\pi}|\Gamma(x)|^2dx=2\,\Gamma_{rms}^2
$$

**Meaning**: summing the energy of all harmonics (Parseval) gives $2\Gamma_{rms}^2$. This is what
lets the "sum over all harmonics" of Eq.(19) collapse into a single clean $\Gamma_{rms}^2$.

**Step-by-step**: square both sides of Eq.(12), integrate over one period $[0,2\pi]$, and use
trigonometric orthogonality (cross terms between different harmonics integrate to 0). Details in
[rms_isf](/03_isf_core_theory/rms_isf).

### Eq.(21): 1/f² phase noise (the signature result)

**Original formula** ([P1] Eq.(21), p.185):

$$
\mathcal{L}\{\Delta\omega\}=10\log_{10}\!\left(\frac{\Gamma_{rms}^2}{q_{max}^2}\cdot\frac{\overline{i_n^2}/\Delta f}{4\,\Delta\omega^2}\right)
$$

**Meaning**: the SSB phase noise produced by a white-noise current source, in the 1/f² region
($-20$ dB/dec). **Phase noise is proportional to $\Gamma_{rms}^2/q_{max}^2$** (claim C3) — the
most important of the three design rules: enlarge $q_{max}$, shrink $\Gamma_{rms}$.

**Step-by-step**: from Eq.(16)/(17) obtain the phase modulation for a single injected tone
($\propto c_n/\Delta\omega$), from Eq.(18) the single-sideband power, then sum over all harmonics
for white noise (Eq.(19)) and use Eq.(20) to collapse the sum into $\Gamma_{rms}^2$.

**Numerical example (Example B)**: $f_0=5$ GHz, $\Delta f=1$ MHz, $q_{max}=1$ pC,
$\Gamma_{rms}=0.5$, $S_i=10^{-24}$ A²/Hz. $\Delta\omega=2\pi\times10^6=6.283\times10^6$
rad/s, $\Delta\omega^2=3.948\times10^{13}$.

$$
\mathcal{L}=10\log_{10}\!\left(\frac{0.25}{10^{-24}}\cdot\frac{10^{-24}}{4\times3.948\times10^{13}}\right)=10\log_{10}(1.583\times10^{-15})=-148.0\ \text{dBc/Hz}.
$$

This is the **ideal value for a single white-noise source**; a real circuit has multiple sources,
cyclostationarity, and flicker, so it sits higher. The full step-by-step account, including the
famous factor-of-2 (SSB bookkeeping convention) discussion, is in
[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise).

### Eq.(22)–(24): flicker upconversion and the 1/f³ corner

**Original formula** ([P1] Eq.(22), p.185, device flicker):

$$
\overline{i_{n,1/f}^2}=\overline{i_n^2}\cdot\frac{\omega_{1/f}}{\Delta\omega}
$$

**Original formula** ([P1] Eq.(23), p.185, 1/f³ phase noise):

$$
\mathcal{L}\{\Delta\omega\}=10\log_{10}\!\left(\frac{c_0^2}{q_{max}^2}\cdot\frac{\overline{i_n^2}/\Delta f}{8\,\Delta\omega^2}\cdot\frac{\omega_{1/f}}{\Delta\omega}\right)
$$

**Original formula** ([P1] Eq.(24), p.185, 1/f³ corner):

$$
\Delta\omega_{1/f^3}=\omega_{1/f}\cdot\frac{c_0^2}{2\,\Gamma_{rms}^2}\approx\omega_{1/f}\left(\frac{c_0}{c_1}\right)^2
$$

**Meaning**: the device's 1/f noise can be upconverted into close-in 1/f³ phase noise only through
the **DC term $c_0$** of the ISF (claim C4). The most counter-intuitive and most important point
(claim C5): **the 1/f³ corner $\ne$ the device 1/f corner** — it is scaled by
$(c_0/\Gamma_{rms})^2/2$. If the waveform is symmetric and $c_0$ is small, the 1/f³ corner can be
pushed far below $\omega_{1/f}$. This is the mathematical basis of the "symmetry design rule".

**Step-by-step**: substitute the 1/f noise of Eq.(22) into Eq.(19); because only the DC coefficient
$c_0$ has a DC response at baseband, only the $c_0^2$ term survives the sum, giving Eq.(23) (note
the denominator is $8$, not $4$). Setting the 1/f² of Eq.(21) equal to the 1/f³ of Eq.(23) and
solving for the crossover frequency gives Eq.(24). The approximation $c_0/c_1\approx \dfrac{c_0/\Gamma_{rms}}{\sqrt2}$
comes from "a symmetric waveform is dominated by $c_1$, so $\Gamma_{rms}^2\approx c_1^2/2$" (i.e. $c_1\approx\sqrt2\,\Gamma_{rms}$, hence $c_0/c_1=(c_0/\Gamma_{rms})/\sqrt2$, consistent with $c_0^2/(2\Gamma_{rms}^2)=(c_0/c_1)^2$).

**Numerical example**: if $\omega_{1/f}=2\pi\times1$ MHz and the waveform is symmetric enough that
$c_0/\Gamma_{rms}=0.1$, then $\Delta\omega_{1/f^3}=\omega_{1/f}\times(0.1)^2/2=\omega_{1/f}\times5\times10^{-3}$,
i.e. a 1/f³ corner of $\approx5$ kHz — far below the device's 1 MHz
corner. Symmetry has pushed the close-in noise away by a factor of 200 in frequency. Full
derivation in [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion).

## Key figures

| Paper figure | Page | Content | Site counterpart |
|---|---|---|---|
| Fig. 4 | 181 | State-space effect of an impulse at the peak vs at a zero crossing | toy reproduction in lab_01/lab_02; see `limit_cycle_phase_amplitude.png` |
| Fig. 6 | 182 | Colpitts and 5-stage ring: excess phase vs injected charge (linear for small charge) | supports the $\Delta\phi\propto\Delta q$ linearity assumption |
| Fig. 7 | 183 | Waveforms and ISFs of (a) LC and (b) ring | toy counterpart `lc_vs_ring_isf_comparison.png` |
| Fig. 8 | 183 | Frequency-translation map: noise near $n\omega_0$ moved onto the carrier | [fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf) |
| Fig. 12 | 185 | $\overline{i^2}/f$ and $\mathcal{L}(\Delta f)$: 1/f³, 1/f², floor | flicker upconversion lab |
| Fig. 20–22 | 189–190 | Injection experiments: sideband $\propto I^2$, $-20$ dB/dec, symmetric vs asymmetric node | see the Sec. V section below |
| Fig. 23–24 | 190–191 | Measured $\mathcal{L}(\Delta f)$ of the 232/115 MHz rings (distinct 1/f³ and 1/f² regions) | see the Sec. V section below |

This site redraws the conceptual comparison with a Python toy model (**not transistor-level**):

![Ideal LC: the -sin ISF vs the numerically extracted one](/figures/isf_impulse_sweep_sinusoidal.png)

## Design insights

[P1] distills phase-noise design into three knobs (all read directly off Eq.(21) and Eq.(24)):

1. **Enlarge $q_{max}$** (node charge swing): $\mathcal{L}\propto1/q_{max}^2$; every doubling of
   $q_{max}$ buys 6 dB. Larger capacitance, larger voltage swing, and higher power all push this way.
2. **Shrink $\Gamma_{rms}$**: make the noise injection instants land where the ISF is small. The
   LC's $\Gamma=-\sin$ is zero at the waveform peak, so "replenishing energy near the peak" hurts
   phase noise the least.
3. **Use symmetry to suppress $c_0$**: a waveform with symmetric rise/fall has $c_0\approx0$,
   pushing the 1/f³ corner (Eq.(24)) very low and cutting close-in phase noise sharply. This rule
   is directly verified in the ring experiment of [P2] (Fig. 17).

Design-side summaries in [symmetry](/06_design_insights/symmetry) and
[lc_vs_ring](/06_design_insights/lc_vs_ring).

## The paper's own end-to-end silicon validation (Sec. V)

> **What this section answers**: this site's numeric chain (Example B's $-148.0$ dBc/Hz) uses
> clean pedagogical numbers; the very same "process data → $C_{node}$ → $q_{max}$ →
> $\overline{i_n^2}/\Delta f$ → $\Gamma_{rms}^2$ → Eq.(21) → $\mathcal{L}$" pipeline was
> validated by [P1] Sec. V (pp.189–191) on **real silicon** with eight experiments, with
> prediction–measurement gaps of 0.2–0.7 dB — and every input is available **a priori**
> (process parameters, geometry, swing, extracted ISF); nothing is fitted after the fact.
> Below we first survey the eight experiments, then replay the chain with the most complete
> numbers step by step.

The eight experiments at a glance (numbers transcribed verbatim from [P1] pp.189–191):

| # | Experiment | What it verifies | Paper's result |
|---|---|---|---|
| 1 | 5-stage 5.4 MHz CMOS ring, sinusoidal current injection, sweeping amplitude ($f_m=100$ kHz, $f_0+f_m=5.5$ MHz, $2f_0+f_m=10.9$ MHz, $3f_0+f_m=16.3$ MHz) | Linearity of current→sideband in Eq.(18) | Upper/lower sidebands equal (within the 0.2 dB accuracy of the setup); best-fit slope 19.8 dB/decade vs predicted 20 (Fig. 20) |
| 2 | Same ring, 20 µA (rms), sweeping $f_m$ | The $1/\Delta\omega$ dependence of Eq.(18) | All four injection frequencies give $-20$ dB/decade (Fig. 21) |
| 3 | 5-stage ring, one stage made asymmetric with an extra pulldown NMOS, 20 µA (rms) injected | Low-frequency upconversion is set by $c_0$ (waveform symmetry) | Sidebands 7 dB larger at the asymmetric node; symmetric nodes essentially unchanged (Fig. 22) |
| 4 | **5-stage 232 MHz single-ended ring (2-µm, 5-V CMOS)** | The full Eq.(21) + Eq.(24) chain | Predicted $-114.7$ vs measured $-114.5$ dBc/Hz @ 500 kHz; corner predicted 75 vs measured 80 kHz (Fig. 23) |
| 5 | 11-stage 115 MHz ring (same die) | Same chain with different $N$ and device sizes | Predicted $-122.1$ vs measured $-122.5$ dBc/Hz @ 500 kHz; corner predicted 43 vs measured 45 kHz (Fig. 24) |
| 6 | 7-stage current-starved ring ($f_0$ held at 60/50 MHz), control voltages tune rise/fall independently | Symmetry should move only 1/f³, not 1/f² (Eq.(24), Eq.(30)) | Tuning symmetry strongly suppresses the 1/f³ region while barely touching 1/f²; an optimum symmetry point exists (Fig. 25/26) |
| 7 | 4-stage differential 200 MHz ring (0.5-µm) | Eq.(21); "only half-circuit symmetry counts" | Predicted $-103.2$ vs measured $-103.9$ dBc/Hz @ 1 MHz; a distinct 1/f³ region despite differential symmetry (Fig. 27) |
| 8 | Bipolar Colpitts 100 MHz, sweeping $n=C_1/(C_1+C_2)$ ($C_{eq}$ fixed) | Conduction-angle effect of cyclostationary noise / $\Gamma_{eff}$ | A definite optimum conduction angle exists; phase noise minimized near $n\approx0.2$ — the theoretical basis for the classic Colpitts rule of thumb (Fig. 28) |

### Full-chain replay: the fourth experiment (5-stage, 232 MHz, 2-µm 5-V CMOS)

This is the chain with the most complete numbers in the whole paper — every input is printed
on p.190, and we substitute them back step by step.

**Step 0 — the paper's process/geometry inputs** ([P1] p.190, transcribed verbatim):

| Quantity | Value | Unit |
|---|---|---|
| gate oxide thickness $t_{ox}$ | 25 | nm |
| $V_{TN}$ | 0.6 | V |
| $V_{TP}$ | 0.53 | V |
| $(W/L)_N$ | 3 µm / 2 µm | — |
| $(W/L)_P$ | 5 µm / 2 µm | — |
| lateral diffusion $L_d$ | 0.1 | µm (so $L_{\text{eff}}=2-2\times0.1=1.8$ µm) |
| total node capacitance $C_{total}$ (incl. parasitics, computed from process + geometry) | 35.7 | fF |
| measurement method | delay-based | — (Fig. 23 shows distinct 1/f³ and 1/f² regions) |

**Step 1 — $q_{max}$**: 5-V process, node swing $V_{swing}=5$ V:

$$
q_{max}=C_{total}\,V_{swing}=35.7\ \text{fF}\times5\ \text{V}=178.5\ \text{fC}
$$

The paper rounds this to **179 fC**. Dimension check: F × V = C ✓ (fF × V = fC).

**Step 2 — noise PSD at the transition point**: a ring's (effective) ISF is concentrated at the
transitions (this site's [lc_vs_ring](/06_design_insights/lc_vs_ring) and [P2]), so the paper
evaluates the noise only at "the instant the output crosses $V_{DD}/2$"; at that point the NMOS
and PMOS are **simultaneously on**, and their current-noise powers add (p.190):

$$
\left(\overline{i_n^2}/\Delta f\right)_{NMOS}=4kT\gamma\mu_nC_{ox}(W/L_{\text{eff}})_N(V_{DD}/2-V_{TN})=4.44\times10^{-24}\ \text{A}^2/\text{Hz}
$$

$$
\left(\overline{i_n^2}/\Delta f\right)_{PMOS}=2.19\times10^{-24}\ \text{A}^2/\text{Hz}
$$

(This is channel thermal noise in the $4kT\gamma g_{d0}$ form with the bias point taken at
$V_{DD}/2$; the paper does not list the individual values of $\mu_n$ and $\gamma$ — the two
PSDs above are given directly by the paper.) Per stage, the total is:

$$
\overline{i_n^2}/\Delta f=(4.44+2.19)\times10^{-24}=6.63\times10^{-24}\ \text{A}^2/\text{Hz}
$$

(Numeric feel: this site's canonical $S_i=10^{-24}$ A²/Hz is the same order of magnitude as
this 2-µm real-silicon $6.63\times10^{-24}$.)

**Step 3 — $\Gamma_{rms}^2$**: using the methods of the Appendix, the paper obtains, for rings,

$$
\Gamma_{rms}^2\approx\frac{16}{N^3}=\frac{16}{125}=0.128
$$

(Dimensionless ✓.) This is the direct ancestor of [P2] Eq.(16):
$\Gamma_{rms}^2=\dfrac{2\pi^2}{3\eta^3}\dfrac{1}{N^3}$, which with $\eta\approx0.75$ gives
$\approx15.6/N^3\approx16/N^3$ — the 1998 and 1999 papers mesh with each other. Incidentally
$\Gamma_{rms}=\sqrt{0.128}=0.358$, the same order as this site's representative 0.5 and smaller
than the true-LC $1/\sqrt2\approx0.707$.

**Step 4 — substitute into Eq.(21) ($N$ identical, uncorrelated sources)**: the powers of $N$
uncorrelated sources add, $\overline{i_n^2}/\Delta f\to N\times6.63\times10^{-24}=3.315\times10^{-23}$ A²/Hz:

$$
\mathcal{L}\{\Delta f\}=10\log_{10}\!\left(\frac{\Gamma_{rms}^2}{q_{max}^2}\cdot\frac{N\,\overline{i_n^2}/\Delta f}{4\,(2\pi\Delta f)^2}\right)=10\log_{10}\!\left(\frac{0.128\times3.315\times10^{-23}}{(179\times10^{-15})^2\times4\times(2\pi)^2\times\Delta f^2}\right)
$$

The numerator is $=4.243\times10^{-24}$ and the denominator is $=3.204\times10^{-26}\times157.9\times\Delta f^2=5.060\times10^{-24}\,\Delta f^2$, so

$$
\mathcal{L}\{\Delta f\}=10\log_{10}\!\left(\frac{0.84}{\Delta f^2}\right)
$$

which matches the $10\log(0.84/\Delta f^2)$ printed on p.190 of the paper (our recomputation
gives 0.839). **Dimension check**: the unit of $\dfrac{S_i}{q_{max}^2}$ is $\dfrac{\text{A}^2/\text{Hz}}{\text{C}^2}=\dfrac{\text{A}^2\cdot\text{s}}{\text{A}^2\text{s}^2}=\text{Hz}$,
and dividing by the Hz² of $(2\pi\Delta f)^2$ gives **1/Hz** — exactly the dimension of
"sideband power per Hz relative to the carrier" ✓. (In other words the prefactor 0.84 carries
the unit Hz.)

**Step 5 — prediction vs measurement**: substituting $\Delta f=500$ kHz:

$$
\mathcal{L}=10\log_{10}\!\left(\frac{0.839\ \text{Hz}}{(5\times10^5\ \text{Hz})^2}\right)=10\log_{10}\!\left(3.35\times10^{-12}\ \text{Hz}^{-1}\right)=-114.7\ \text{dBc/Hz}
$$

The paper measures **$-114.5$ dBc/Hz** — a 0.2 dB gap.

> **factor-of-2/4 flag (called out every time it appears)**: the **4** in the denominator is
> [P1] Eq.(21)'s **SSB bookkeeping**, the same convention as this site's Example B
> ($-148.0$ dBc/Hz). With the clean time-domain **/2** bookkeeping instead, the same inputs
> would predict $-111.7$ dBc/Hz (3 dB higher), i.e. 3.0 dB away from the measurement. This
> experiment is therefore often cited as empirical support for the /4 version; note, however,
> that the 0.2 dB agreement also absorbs estimation errors in $\Gamma_{rms}$ and $C_{total}$,
> so reading it as "the magnitude and scaling are right" is more robust than reading it as a
> definitive verdict on the factor of 2. See
> [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise).

**Step 6 — the 1/f³ corner (Eq.(24) divided through by $2\pi$)**: an isolated inverter on the
same die (input and output shorted) measures a device 1/f corner of $f_{1/f}=250$ kHz; from the
extracted ISF, $c_0^2/2\Gamma_{rms}^2=0.3$:

$$
f_{1/f^3}=f_{1/f}\cdot\frac{c_0^2}{2\,\Gamma_{rms}^2}=250\ \text{kHz}\times0.3=75\ \text{kHz}
$$

Measured: **80 kHz**. This is the most direct silicon evidence for claim C5, "the 1/f³ corner
$\ne$ the device 1/f corner": the corner is pushed from 250 kHz down to 80 kHz by the (partial)
symmetry of the waveform.

**Python verification** (pure-algebra recomputation; all inputs from [P1] p.190–191):

```python
import math

# [P1] Sec. V, fourth experiment: 5-stage 232 MHz single-ended ring (2-µm 5-V CMOS, p.190)
N       = 5              # number of stages
qmax    = 179e-15        # C (= C_total 35.7 fF × V_swing 5 V)
Si_nmos = 4.44e-24       # A²/Hz (given by the paper, p.190, at the transition point)
Si_pmos = 2.19e-24       # A²/Hz (given by the paper, p.190)
G2rms   = 16 / N**3      # Γ²_rms ≈ 16/N³ (paper, p.190)

print(round(G2rms, 3))                            # -> 0.128
Si_total = N * (Si_nmos + Si_pmos)                # powers of N uncorrelated sources add
prefac = G2rms * Si_total / (4 * qmax**2 * (2*math.pi)**2)
print(round(prefac, 3))                           # -> 0.839 (paper prints 0.84)

df = 500e3   # Hz
print(round(10*math.log10(prefac/df**2), 2))      # -> -114.74 (paper predicts -114.7; measured -114.5)
print(round(10*math.log10(2*prefac/df**2), 2))    # -> -111.73 (with the time-domain /2 bookkeeping: 3 dB off the measurement)
print(round(250e3*0.3/1e3, 1))                    # -> 75.0 (kHz, Eq.(24); measured 80 kHz)

# Fifth experiment: 11-stage 115 MHz (same die; noise scales with W: NMOS×4/3, PMOS×6/5, same L)
N2, qmax2 = 11, 217e-15
Si_stage2 = Si_nmos*(4/3) + Si_pmos*(6/5)
prefac2 = (16/N2**3) * N2 * Si_stage2 / (4 * qmax2**2 * (2*math.pi)**2)
print(round(prefac2, 3))                          # -> 0.152 (paper prints 0.152, digit-for-digit)
print(round(10*math.log10(prefac2/df**2), 2))     # -> -122.16 (paper predicts -122.1; measured -122.5)
print(round(250e3*0.17/1e3, 1))                   # -> 42.5 (kHz, paper rounds to 43; measured 45 kHz)

# Seventh experiment: 4-stage differential 200 MHz (0.5-µm; q_max = 49 fF × 1.2 V = 58.8 fC)
prefac3 = (16/4**3) * 4 * 2.63e-23 / (4 * (58.8e-15)**2 * (2*math.pi)**2)
print(round(prefac3, 1))                          # -> 48.2 (paper prints 48.1, trailing-digit rounding)
print(round(10*math.log10(prefac3/(1e6)**2), 2))  # -> -103.17 (paper predicts -103.2; measured -103.9)
```

### Second validation on the same die: the 11-stage 115 MHz ring

The fifth experiment reruns the same chain with different $N$ and device sizes
([P1] p.190, numbers verbatim): $(W/L)_N=4$ µm / 2 µm, $(W/L)_P=6$ µm / 2 µm, total node
capacitance 43.5 fF, $q_{max}=217$ fC ($=43.5\ \text{fF}\times5\ \text{V}$). The paper states
the phase noise is "calculated in exactly the same manner as the previous experiment", giving
$\mathcal{L}\{\Delta f\}=10\log(0.152/\Delta f^2)$, i.e. $-122.1$ dBc/Hz at 500 kHz; measured
**$-122.5$ dBc/Hz** (0.4 dB gap). $c_0^2/2\Gamma_{rms}^2=0.17$ predicts a 1/f³ corner of
43 kHz; measured **45 kHz**. The paper does not list the device PSDs of the 11-stage inverters;
the Python above recomputes them by scaling the noise linearly with $W$ (same $L$) and lands on
a prefactor of **0.152**, digit-for-digit identical to the paper — reverse-confirming that this
is exactly the paper's internal calculation.

As a bonus, we can itemize the 7.4 dB improvement from 5 stages to 11 stages **entirely inside
Eq.(21)** (using the two recomputed prefactors, $10\log_{10}(0.839/0.152)=7.42$ dB):

| Term | Ratio | dB |
|---|---|---|
| $\Gamma_{rms}^2\times N=16/N^2$ ($25\to121$) | $\times4.84$ smaller | $-6.85$ |
| $q_{max}^2$ ($179\to217$ fC) | $\times1.47$ larger | $-1.67$ |
| per-stage noise PSD ($6.63\to8.55\times10^{-24}$ A²/Hz) | $\times1.29$ larger | $+1.10$ |
| **Total** | | $-7.42$ ✓ |

Note this is **not** a free lunch: the stage count grows and $f_0$ also drops from 232 to
115 MHz; [P2] Eq.(23), p.796 later proves that at **fixed total power and fixed $f_0$** the
white-noise phase noise of a single-ended ring is independent of $N$. See
[paper_002](/05_paper_deep_dives/paper_002_jitter_phase_noise_ring).

### Third validation across process and architecture: 4-stage differential 200 MHz (0.5-µm)

The seventh experiment ([P1] p.191): tail current 108 µA, total capacitance on each
differential node $C_{total}=49$ fF, $V_{swing}=1.2$ V, hence $q_{max}=58.8$ fC (the paper's
text prints "58.8 fF" — dimensionally $49\ \text{fF}\times1.2\ \text{V}$ can only be fC; this
is a typo in the paper, which we transcribe faithfully and flag). Total channel noise per node
$(\overline{i_n^2}/\Delta f)_{total}=2.63\times10^{-23}$ A²/Hz; with $N=4$ the same chain gives
$\mathcal{L}\{\Delta f\}=10\log(48.1/\Delta f^2)$ (our recomputation gives 48.2,
a trailing-digit rounding difference), predicting $-103.2$ at 1 MHz; measured
**$-103.9$ dBc/Hz** (0.7 dB gap).

The same experiment carries a symmetry lesson: although the **differential signal** is
perfectly symmetric, the single-ended waveform of each **half-circuit** is not, so Fig. 27
still shows a distinct 1/f³ region — "differential signaling does not rescue $c_0$; what counts
is half-circuit symmetry" (echoing p.188 and [symmetry](/06_design_insights/symmetry)).

### What this set of experiments establishes (applicability and failure conditions)

- **The predictions are a priori**: the three full chains (232 MHz / 115 MHz / 200 MHz
  differential) miss by 0.2 / 0.4 / 0.7 dB, with inputs limited to process parameters,
  geometry, $V_{swing}$, and the extracted ISF. This site's Example B toy chain
  ($q_{max}=1$ pC, $\Gamma_{rms}=0.5$, $S_i=10^{-24}$ A²/Hz → $-148.0$ dBc/Hz @ 1 MHz,
  SSB /4 bookkeeping) runs the very same pipeline, just with clean numbers.
- **Applicable when**: noise is concentrated at the transitions (true for single-ended CMOS
  rings); $\Gamma_{rms}^2\approx16/N^3$ is a ring-specific approximation for "identical
  inverters with standard rise/fall" (corresponding to [P2]'s $\eta\approx0.75$); the noise of
  different stages is uncorrelated (only then may powers be added).
- **Fails when**: the waveform is asymmetric (experiments 3/6/7) so that close-in noise is
  dominated by the $c_0$-driven 1/f³ — Eq.(21) covers only the 1/f² region; very close to the
  carrier the linearization breaks down (see
  [lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth)); strong spurs or injection
  pulling require separate treatment ([P3]/[P4]).
- **Dimensions**: the argument of every $10\log_{10}$ is 1/Hz — the hallmark of dBc/Hz.

## Limitations

Per paper_metadata (paper_001.limitations):

- The 1/f³ region was historically linked empirically; this theory clarifies that it is set by $c_0$, but **the exact $c_0$ still has to be extracted**.
- In real circuits $\Gamma$ must be extracted via transient impulse simulation or adjoint/PSS methods; the closed forms are first-order approximations.
- **AM–PM conversion and strong nonlinearity** are not fully covered by the first-order phase-only model (exactly the hole [P4] patches with the APF).
- The rigorous mathematical foundation (PPV / adjoint / Floquet) is **not among the five source PDFs**; it belongs to external literature (claim C13) —
  see [effective_isf](/03_isf_core_theory/effective_isf).

## Relationship to other papers

- **[P2]** applies this page's ISF to the ring oscillator: it derives the jitter $\kappa$ from the
  same $\Gamma_{rms}^2/q_{max}^2$ ratio and studies the $\Gamma_{rms}\propto N^{-3/2}$ scaling (claim C8).
- **[P3]/[P4]** extend the same ISF from "random noise" to "deterministic injection": [P3] uses
  $\Gamma$ to write the generalized Adler equation (claim C10); [P4] adds the amplitude counterpart, the APF (claim C11).
- **[P5]** is **unrelated** to this page (sense amplifier, claim C12); the only conceptual bridge is regeneration / positive feedback.
- The **Leeson model** is a special case of this theory (claim C9); the Leeson formula is entry 19 in
  [equation_index](/01_paper_map/equation_index), marked as reference (not in the 5 PDFs).

## Further reading / companion teaching pages

This page is the bird's-eye view "at the altitude of the paper"; the five pages below take each
block of [P1] **all the way through, step by step**. Recommended order:

| Which block of this page | Companion teaching page | What that page adds |
|---|---|---|
| Eq.(10)–(13) ISF and LTV phase response | [isf_definition](/03_isf_core_theory/isf_definition) | The full definition of the ISF; its $2\pi$ periodicity and dimensionlessness built up term by term |
| Eq.(11) convolution form $\phi(t)=\frac{1}{q_{max}}\int\Gamma\,i_n\,d\tau$ | [convolution_derivation](/03_isf_core_theory/convolution_derivation) | From the impulse response $h_\phi(t,\tau)$ to the superposition integral with no skipped steps, incl. the LTV fingerprint |
| Eq.(19)–(21) white noise $\to$ 1/f² phase noise | [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) | down-conversion, the factor-8 summation, the famous factor-of-2 SSB bookkeeping controversy |
| Eq.(22)–(24) flicker upconversion and the 1/f³ corner | [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion) | why only $c_0$ can upconvert; the complete algebra behind 1/f³ corner $\ne$ device corner |
| "Use symmetry to suppress $c_0$" among the three design rules | [symmetry](/06_design_insights/symmetry) | how symmetry sets $c_0$, the design knobs, and the experimental cross-check with [P2] Fig. 17 |

> **How to read**: the theory details and numerical feel all live in [03_isf_core_theory](/03_isf_core_theory/isf_definition); to compute hands-on, go back to [numerical_feeling](/04_simulation_labs/numerical_feeling). This page's only job is to **string those blocks into the story of one paper**.

## What to remember

- **LTV, not LTI**: same impulse, different injection phase, different effect — that is the ISF $\Gamma(\omega_0\tau)$.
- **Phase accumulates, amplitude is pulled back**: phase noise lives in the accumulating phase (Eq.(1); the upper limit of the integral in Eq.(11) is $t$).
- **Signature formula**: $\mathcal{L}\propto\dfrac{\Gamma_{rms}^2}{q_{max}^2}\cdot\dfrac{S_i}{\Delta\omega^2}$ (Eq.(21)).
- **Three design rules**: enlarge $q_{max}$, shrink $\Gamma_{rms}$, use symmetry to suppress $c_0$.
- **1/f³ corner $\ne$ device 1/f corner** (Eq.(24)) — symmetry can push it very low.
- All core derivations are in [03_isf_core_theory](/03_isf_core_theory/isf_definition); numerical feel is in
  [numerical_feeling](/04_simulation_labs/numerical_feeling).
