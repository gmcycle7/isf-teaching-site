---
title: Foundations Chapter Exercises (with Full Solutions)
description: "Exercise set for the foundations chapter: phase↔jitter conversion, PSD/Parseval, LTI vs LTV, Allan slope reading, Lorentzian linewidth estimation. Every problem comes with a step-by-step solution, units and dimension check, numerical answer, and a one-line Python verification."
---

import NumericQuiz from "@site/src/components/NumericQuiz";

# Foundations Chapter Exercises (with Full Solutions)

> **β**: This English translation is in beta — the Traditional-Chinese original is the authoritative version.

> Prerequisites: [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter) · [lti_vs_ltv](/02_foundations/lti_vs_ltv) | Next: [03 core-theory chapter exercises](/03_isf_core_theory/exercises)

This page is the exercise set for **Chapter 02 (Foundations)**. Problem types cover **derivation problems**
(derive the expressions by hand), **numerical problems** (plug in numbers, carry the units, do the dimension check),
and **reverse-design problems** (given a target spec, back-solve the required parameters).

> **How to use this page**: work each problem yourself first, then expand the "Solution" to compare. Every solution
> follows the same format: **step-by-step substitution (with units) → result → dimension check → one-line Python
> verification**. All Python verifications call this site's real library `simulations/common/` (no invented APIs),
> so you can paste them straight into a REPL.

Core formulas involved (all from the spec and this chapter's pages, using the same notation):

- phase→time: $\Delta t=\dfrac{\Delta\phi}{2\pi f_0}$ (spec Eq. 17)
- phase variance: $\sigma_\phi^2=\displaystyle\int_{f_1}^{f_2}S_\phi(f)\,df$ (spec Eq. 18)
- rms jitter: $\sigma_t=\dfrac{1}{2\pi f_0}\sqrt{\displaystyle\int_{f_1}^{f_2}S_\phi(f)\,df}$ (spec Eq. 19)
- SSB↔phase PSD (small-angle): $\mathcal{L}(\Delta f)\approx\tfrac12 S_\phi(\Delta f)$ (spec Eq. 16)
- Parseval: $\displaystyle\sum_{n=0}^{\infty}c_n^2=\frac{1}{\pi}\int_0^{2\pi}\lvert\Gamma(x)\rvert^2dx=2\,\Gamma_{rms}^2$ ([P1] Eq.(20), p.185)
- Lorentzian linewidth (FWHM): $\Delta f_{3\mathrm{dB}}=\dfrac{D}{\pi}$, phase diffusion $\operatorname{Var}[\Delta\phi(t)]=2D\lvert t\rvert$ (spec §11.2; linked to [E2] Demir 2000, not among the five source PDFs)
- Allan slope reference: white FM $\to\tau^{-1/2}$, flicker FM $\to\tau^{0}$, random-walk FM $\to\tau^{+1/2}$ (spec §11.2; Allan is external literature)

---

## Problems

### Exercise 1 (numerical) — phase ↔ time conversion

An oscillator at $f_0=5$ GHz has an instantaneous excess-phase offset $\Delta\phi=5\times10^{-4}$ rad.
Find the corresponding timing error $\Delta t$ (fs), and convert $\Delta\phi$ to degrees.

<NumericQuiz
  prompt="Try it yourself first: Δt = ? (Δφ = 5×10⁻⁴ rad, f₀ = 5 GHz; answer in fs)"
  answer={15.9}
  unit="fs"
  hint="Δt = Δφ/(2πf₀); the denominator 2πf₀ ≈ 3.14×10¹⁰ rad/s, and rad ÷ (rad/s) = s."
  solutionNote="Δt = 5×10⁻⁴/(2π×5×10⁹) ≈ 1.59×10⁻¹⁴ s = 15.9 fs. Full step-by-step solution (including the conversion to degrees) in the Exercise 1 solution below."
/>

### Exercise 2 (numerical) — rms jitter from phase variance

A clock has rms phase $\sigma_\phi=14.07$ mrad (over the 1→100 MHz integration band), with $f_0=5$ GHz.
Find the rms timing jitter $\sigma_t$ (fs).

### Exercise 3 (derivation + numerical) — Parseval: $\Gamma_{rms}$ and $\sum c_n^2$ from the ISF

The ISF of an ideal LC oscillator is $\Gamma(\theta)=-\sin\theta$.

(a) Using the definition $\Gamma_{rms}^2=\dfrac{1}{2\pi}\displaystyle\int_0^{2\pi}\Gamma^2(\theta)\,d\theta$, compute $\Gamma_{rms}$ by hand.
(b) Using Parseval (spec Eq. 11), find $\sum_{n=0}^{\infty}c_n^2$, and state which $c_n$ is the only nonzero one.

### Exercise 4 (numerical) — phase variance from PSD integration

An oscillator's one-sided phase PSD at offset $f$, in the $1/f^2$ region, can be written $S_\phi(f)=\dfrac{K}{f^2}$,
with $K=10^{-4}\ \text{rad}^2\cdot\text{Hz}$ (i.e., $S_\phi(1\,\text{Hz})=10^{-4}$). Find the phase variance
$\sigma_\phi^2$ and $\sigma_\phi$ (mrad) over the integration band $f_1=10^3$ Hz to $f_2=10^6$ Hz.

<NumericQuiz
  prompt="Try it yourself first: σ_φ = ? (K = 10⁻⁴ rad²·Hz, f₁ = 10³ Hz, f₂ = 10⁶ Hz; answer in mrad)"
  answer={0.316}
  tol={0.06}
  unit="mrad"
  hint="σ_φ² = K(1/f₁ − 1/f₂), dominated by the low-frequency end 1/f₁; remember to take the square root and convert to mrad."
  solutionNote="σ_φ² = 10⁻⁴×(10⁻³ − 10⁻⁶) ≈ 9.99×10⁻⁸ rad² → σ_φ ≈ 3.16×10⁻⁴ rad = 0.316 mrad. Details in the Exercise 4 solution below."
/>

### Exercise 5 (concept + derivation) — LTI vs LTV: same impulse, different phase

The ideal-LC ISF is $\Gamma(\theta)=-\sin\theta$. The same charge impulse $\Delta q$ is injected
(a) at the waveform **zero-crossing** ($\theta=\pi/2$, where the $\cos$ waveform has its maximum slope and $-\sin$ is at its extremum)
and (b) at the waveform **peak** ($\theta=0$). Using $\Delta\phi=\Gamma(\theta)\,\Delta q/q_{max}$,
show how much the two phase effects differ, and explain in one sentence why this is "LTV, not LTI".
Take $\Delta q=1$ fC, $q_{max}=1$ pC.

<NumericQuiz
  prompt="Try (a) yourself first: at the zero-crossing θ=π/2, Δφ_a = ? (Δq=1 fC, q_max=1 pC; answer in mrad, include the sign)"
  answer={-1}
  tol={0.02}
  unit="mrad"
  hint="Γ(π/2) = −sin(π/2) = −1; Δφ = Γ×Δq/q_max, and Δq/q_max = 10⁻³."
  solutionNote="Δφ_a = (−1)×10⁻³ rad = −1 mrad. At the peak θ=0, Δφ_b = 0 (Γ=0). Details in the Exercise 5 solution below."
/>

### Exercise 6 (reverse design) — phase diffusion from the Lorentzian linewidth

A free-running oscillator's measured carrier 3-dB linewidth (FWHM) is $\Delta f_{3\mathrm{dB}}=1$ kHz.

(a) Back-solve the phase-diffusion coefficient $D$ (rad²/s).
(b) Estimate how long $t$ it takes for the phase to accumulate a variance $\operatorname{Var}[\Delta\phi]=1\ \text{rad}^2$ (the phase has "wandered by about 1 rad" and coherence has largely collapsed).

<NumericQuiz
  prompt="Try (a) yourself first: back-solve D = ? (Δf₃dB = 1 kHz; answer in rad²/s)"
  answer={3141.6}
  tol={0.02}
  unit="rad²/s"
  hint="Δf₃dB = D/π ⇒ D = π×Δf₃dB."
  solutionNote="D = π×10³ ≈ 3141.6 rad²/s. (b) t = 1/(2D) ≈ 159 µs. Details in the Exercise 6 solution below."
/>

### Exercise 7 (concept + slope reading) — Allan deviation slopes

On a log–log Allan-deviation plot $\sigma_y(\tau)$ you measure three segments with different slopes:
$-1/2$, $0$, $+1/2$. Which FM noise type does each correspond to? Also explain why "flicker FM" forms a
**flat plateau (floor)** in the ADEV.

### Exercise 8 (numerical) — from a single $\mathcal{L}(\Delta f)$ point to $S_\phi$ to jitter

A spur-free oscillator measures $\mathcal{L}(1\,\text{MHz})=-120$ dBc/Hz at $\Delta f=1$ MHz.
(a) Find $S_\phi$ at that offset (rad²/Hz).
(b) If over the 1-decade span 1→10 MHz the PSD follows $1/f^2$ (i.e., $S_\phi=K/f^2$, with $K$ set by (a)),
and $f_0=5$ GHz, find the rms jitter $\sigma_t$ (fs) over this band.

<NumericQuiz
  prompt="Try (b) yourself first: σ_t = ? (L(1 MHz) = −120 dBc/Hz, 1/f² integrated 1→10 MHz, f₀ = 5 GHz; answer in fs)"
  answer={42.7}
  unit="fs"
  hint="First S_φ = 2×10^(L/10) = 2×10⁻¹² rad²/Hz, set K = S_φ×(10⁶)², then σ_φ² = K(1/f₁ − 1/f₂) and σ_t = σ_φ/(2πf₀)."
  solutionNote="σ_φ² = 1.8×10⁻⁶ rad² → σ_φ ≈ 1.34 mrad → σ_t ≈ 42.7 fs. Details in the Exercise 8 solution below."
/>

---

## Solutions

<details>
<summary><strong>Exercise 1 solution</strong> (phase ↔ time conversion)</summary>

**Step-by-step substitution (with units).** Using phase→time (spec Eq. 17):

$$
\Delta t=\frac{\Delta\phi}{2\pi f_0}=\frac{5\times10^{-4}\ \text{rad}}{2\pi\times5\times10^{9}\ \text{Hz}}=\frac{5\times10^{-4}}{3.1416\times10^{10}}\ \text{s}.
$$

$$
\Delta t\approx1.59\times10^{-14}\ \text{s}=15.9\ \text{fs}.
$$

Converting to degrees:

$$
\Delta\phi=5\times10^{-4}\times\frac{180}{\pi}\approx0.0286^\circ.
$$

**Result**: $\Delta t\approx15.9$ fs, $\Delta\phi\approx0.0286^\circ$.

**Dimension check**: $\dfrac{[\text{rad}]}{[\text{rad/s}]}=[\text{s}]$ ✓ (the unit of $2\pi f_0$ is rad/s; rad is
dimensionless, so the ratio gives seconds). This is exactly the timing error of canonical Example A in spec §8.

```python
from simulations.common.noise_utils import phase_to_time_error
dt = phase_to_time_error(5e-4, f0=5e9)
print(dt*1e15, "fs")   # -> 15.92 fs
```

</details>

<details>
<summary><strong>Exercise 2 solution</strong> (rms jitter from phase variance)</summary>

**Step-by-step substitution (with units).** rms jitter (spec Eq. 19). Here $\sigma_\phi$ is given directly, so
$\sqrt{\int S_\phi df}=\sigma_\phi$ and the formula reduces to the rms version of phase→time:

$$
\sigma_t=\frac{\sigma_\phi}{2\pi f_0}=\frac{14.07\times10^{-3}\ \text{rad}}{2\pi\times5\times10^{9}\ \text{Hz}}=\frac{1.407\times10^{-2}}{3.1416\times10^{10}}\ \text{s}.
$$

$$
\sigma_t\approx4.479\times10^{-13}\ \text{s}=447.9\ \text{fs}.
$$

**Result**: $\sigma_t\approx447.9$ fs. This corresponds to canonical Example C in spec §8 (the lab_08 result for $f_0=5$ GHz,
$\mathcal{L}(1\text{MHz})=-100$ dBc/Hz, 1/f² slope, integrated 1→100 MHz).

**Dimension check**: $\dfrac{[\text{rad}]}{[\text{rad/s}]}=[\text{s}]$ ✓.

```python
import numpy as np
sigma_phi = 14.07e-3            # rad
f0 = 5e9
sigma_t = sigma_phi/(2*np.pi*f0)
print(sigma_t*1e15, "fs")      # -> 447.9 fs
```

(For the full integral version see [numerical_feeling](/04_simulation_labs/numerical_feeling) and
`integrate_rms_jitter` in `simulations/common/noise_utils.py`.)

</details>

<details>
<summary><strong>Exercise 3 solution</strong> (Parseval: $\Gamma_{rms}$ and $\sum c_n^2$ from the ISF)</summary>

**(a) Compute $\Gamma_{rms}$ by direct integration.** Using the fact that $\sin^2\theta$ averages to $\tfrac12$ over one period:

$$
\Gamma_{rms}^2=\frac{1}{2\pi}\int_0^{2\pi}(-\sin\theta)^2\,d\theta=\frac{1}{2\pi}\int_0^{2\pi}\sin^2\theta\,d\theta=\frac{1}{2\pi}\cdot\pi=\frac12.
$$

$$
\Gamma_{rms}=\frac{1}{\sqrt2}\approx0.707.
$$

**(b) Find $\sum c_n^2$ with Parseval.** Spec Eq. 11 ([P1] Eq.(20), p.185):

$$
\sum_{n=0}^{\infty}c_n^2=2\,\Gamma_{rms}^2=2\times\frac12=1.
$$

**Which $c_n$ is nonzero**: $\Gamma(\theta)=-\sin\theta=\cos(\theta+\tfrac{\pi}{2})$ is a **pure first harmonic**,
so only $c_1=1$ (with $\theta_1=\pi/2$); all others $c_0=c_2=\dots=0$. Check: $\sum c_n^2=c_1^2=1$ ✓.

**Result**: $\Gamma_{rms}=1/\sqrt2\approx0.707$, $\sum c_n^2=1$, the only nonzero coefficient is $c_1=1$.

**Dimension check**: $\Gamma$ is dimensionless (spec notation table), so $\Gamma_{rms}^2$ and $\sum c_n^2$ are both dimensionless ✓.

```python
import numpy as np
from simulations.common.isf_utils import gamma_lc_ideal, gamma_rms, compute_fourier_coefficients
theta = np.linspace(0, 2*np.pi, 4096, endpoint=False)
g = gamma_lc_ideal(theta)                     # = -sin(theta)
print(gamma_rms(theta, g))                    # -> 0.7071
a0, a, b, c, ph = compute_fourier_coefficients(theta, g, n_harmonics=5)
print(np.sum(c**2))                           # -> ~1.0  (== 2*Gamma_rms^2)
```

</details>

<details>
<summary><strong>Exercise 4 solution</strong> (phase variance from PSD integration)</summary>

**Step-by-step substitution (with units).** Phase variance (spec Eq. 18), substituting $S_\phi(f)=K/f^2$:

$$
\sigma_\phi^2=\int_{f_1}^{f_2}\frac{K}{f^2}\,df=K\left[-\frac1f\right]_{f_1}^{f_2}=K\left(\frac{1}{f_1}-\frac{1}{f_2}\right).
$$

Substituting $K=10^{-4}\ \text{rad}^2\cdot\text{Hz}$, $f_1=10^3$ Hz, $f_2=10^6$ Hz:

$$
\sigma_\phi^2=10^{-4}\left(\frac{1}{10^3}-\frac{1}{10^6}\right)=10^{-4}\times(10^{-3}-10^{-6})=10^{-4}\times9.99\times10^{-4}=9.99\times10^{-8}\ \text{rad}^2.
$$

$$
\sigma_\phi=\sqrt{9.99\times10^{-8}}\approx3.16\times10^{-4}\ \text{rad}=0.316\ \text{mrad}.
$$

**Result**: $\sigma_\phi^2\approx9.99\times10^{-8}\ \text{rad}^2$, $\sigma_\phi\approx0.316$ mrad.

**Intuition**: the $1/f^2$ integral is **dominated by the low-frequency end $f_1$** ($1/f_1\gg1/f_2$) — which is exactly
why close-in phase noise contributes most of the total jitter.

**Dimension check**: $[K]\cdot[1/f]=(\text{rad}^2\cdot\text{Hz})\cdot(1/\text{Hz})=\text{rad}^2$ ✓
($\sigma_\phi^2$ is in rad²).

```python
import numpy as np
K, f1, f2 = 1e-4, 1e3, 1e6
var = K*(1/f1 - 1/f2)
print(var, "rad^2 ->", np.sqrt(var)*1e3, "mrad")   # -> 9.99e-8 rad^2 -> 0.316 mrad
```

</details>

<details>
<summary><strong>Exercise 5 solution</strong> (LTI vs LTV: same impulse, different phase)</summary>

**Step-by-step substitution (with units).** Using the operational ISF (spec Eq. 5) $\Delta\phi=\Gamma(\theta)\,\Delta q/q_{max}$.
$\Delta q/q_{max}=10^{-15}/10^{-12}=10^{-3}$.

**(a) Zero-crossing $\theta=\pi/2$** ($\Gamma=-\sin(\pi/2)=-1$, maximum sensitivity):

$$
\Delta\phi_a=(-1)\times10^{-3}=-1\times10^{-3}\ \text{rad}=-1\ \text{mrad}.
$$

**(b) Peak $\theta=0$** ($\Gamma=-\sin 0=0$, zero sensitivity):

$$
\Delta\phi_b=0\times10^{-3}=0\ \text{rad}.
$$

**Result**: injection at the zero-crossing produces a phase step of $\lvert\Delta\phi\rvert=1$ mrad; injection at the peak produces **zero** phase step
(there the charge only changes the amplitude, which is subsequently pulled back by amplitude restoring).

**Why this is LTV, not LTI**: the impulse response of an **LTI (linear time-invariant)** system depends only on the
**elapsed time** $t-\tau$, not on the **injection instant** $\tau$. Here, however, the same $\Delta q$ at $\theta=\pi/2$ versus $\theta=0$
produces **completely different** $\Delta\phi$ — the response explicitly depends on the **absolute injection phase** $\Gamma(\omega_0\tau)$,
which is precisely the defining signature of an **LTV (linear time-varying)** system (see [lti_vs_ltv](/02_foundations/lti_vs_ltv)).

**Dimension check**: $\Gamma$ dimensionless $\times\ \Delta q/q_{max}$ (C/C, dimensionless) $=$ rad ✓.

```python
from simulations.common.isf_utils import gamma_lc_ideal, impulse_to_phase_step
import numpy as np
dq, qmax = 1e-15, 1e-12
for name, theta in [("zero-crossing", np.pi/2), ("peak", 0.0)]:
    g = gamma_lc_ideal(theta)                       # -sin(theta)
    dphi = impulse_to_phase_step(dq, g, qmax)
    print(name, dphi*1e3, "mrad")                   # -> -1.0 mrad ; 0.0 mrad
```

</details>

<details>
<summary><strong>Exercise 6 solution</strong> (phase diffusion from the Lorentzian linewidth)</summary>

> Note: Lorentzian linewidth and phase diffusion are **external literature** ([E2] Demir 2000), **not among the five source PDFs**;
> the formulas are taken verbatim from spec §11.2.

**(a) Back-solve $D$.** FWHM linewidth (spec §11.2):

$$
\Delta f_{3\mathrm{dB}}=\frac{D}{\pi}\quad\Longrightarrow\quad D=\pi\,\Delta f_{3\mathrm{dB}}=\pi\times10^{3}\ \text{Hz}=3.142\times10^{3}\ \text{rad}^2/\text{s}.
$$

**(b) Estimate the time to accumulate 1 rad².** Phase diffusion (spec §11.2) $\operatorname{Var}[\Delta\phi(t)]=2D\lvert t\rvert$; setting it $=1\ \text{rad}^2$:

$$
t=\frac{1}{2D}=\frac{1}{2\times3.142\times10^{3}}\approx1.59\times10^{-4}\ \text{s}=159\ \mu\text{s}.
$$

**Result**: $D\approx3.14\times10^{3}\ \text{rad}^2/\text{s}$; accumulating $\approx1\ \text{rad}^2$ of phase variance takes about **159 µs**
(i.e., a coherence time of order $\tau_c\sim1/(2D)$). Note that $1/\Delta f_{3\mathrm{dB}}=1$ ms is of the same order —
**the narrower the linewidth, the longer the coherence time**; the two are reciprocals.

**Dimension check**: (a) $[\,\Delta f\,]=\text{Hz}=1/\text{s}$, multiplied by $\pi$ (dimensionless), gives $D$ in rad²/s
(rad² being the square of the dimensionless "rad" of phase variance, per second) ✓. (b) $\dfrac{\text{rad}^2}{\text{rad}^2/\text{s}}=\text{s}$ ✓.

```python
import numpy as np
df_3db = 1e3                       # Hz (FWHM)
D = np.pi*df_3db                   # rad^2/s
t = 1/(2*D)                        # Var = 2 D t = 1 rad^2
print(D, "rad^2/s ;", t*1e6, "us")   # -> 3141.6 rad^2/s ; 159.2 us
```

(Background and full derivation: [lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth).)

</details>

<details>
<summary><strong>Exercise 7 solution</strong> (reading Allan-deviation slopes)</summary>

> Note: The Allan variance is **external literature** (Allan 1966), **not among the five source PDFs**; the slope table is taken verbatim from spec §11.2.

**Slope reference (spec §11.2).** On a log–log $\sigma_y(\tau)$ plot:

| Measured slope $\sigma_y(\tau)\propto\tau^{?}$ | Noise type | Physics |
|---|---|---|
| $\tau^{-1/2}$ | **white FM** (white frequency modulation) | frequency is white noise → phase is a random walk; the longer you average, the more stable |
| $\tau^{0}$ (plateau/floor) | **flicker FM** (1/f frequency) | $\sigma_y$ is independent of the gate time $\tau$ → ADEV forms a flat floor |
| $\tau^{+1/2}$ | **random-walk FM** (random walk of frequency) | the frequency itself drifts → the longer you average, the **worse** it gets; slope turns upward |

**Why flicker FM forms a plateau**: substitute $S_y(f)\propto1/f$ (flicker FM) into the spec §11.2 expression
$\sigma_y^2(\tau)=2\displaystyle\int_0^\infty S_y(f)\dfrac{\sin^4(\pi f\tau)}{(\pi f\tau)^2}\,df$ and change variables to
$u=\pi f\tau$: $\tau$ **cancels completely** out of the integrand — the integral becomes a pure numerical constant independent of $\tau$,
so $\sigma_y^2(\tau)=$ constant $\Rightarrow\sigma_y(\tau)\propto\tau^0$, a **horizontal line (floor)** on the log–log plot.
This floor is the signature long-term-stability feature of quartz/atomic clocks, marking the limit that no amount of extra averaging time can push down.

**Result**: $\tau^{-1/2}\to$ white FM, $\tau^{0}\to$ flicker FM (floor), $\tau^{+1/2}\to$ random-walk FM.

**Dimension check**: $\sigma_y(\tau)$ is the **dimensionless fractional-frequency stability** ($y=\Delta f/f_0$); its power-law
relationship with $\tau$ only compares slopes and carries no dimension ✓.

```python
import numpy as np
# Read off by the slope definition: fit the log-log slope of a sigma_y(tau) segment
tau = np.logspace(-3, 1, 200)
for label, slope in [("white FM", -0.5), ("flicker FM", 0.0), ("random-walk FM", 0.5)]:
    sy = tau**slope
    fit = np.polyfit(np.log10(tau), np.log10(sy), 1)[0]
    print(label, "slope =", round(fit, 2))   # -> -0.5 ; 0.0 ; 0.5
```

(Full derivation and plots: [allan_variance](/02_foundations/allan_variance).)

</details>

<details>
<summary><strong>Exercise 8 solution</strong> (from a single $\mathcal{L}$ point to $S_\phi$ to jitter)</summary>

**(a) $\mathcal{L}\to S_\phi$.** First convert dBc/Hz back to linear:

$$
\mathcal{L}_{\text{lin}}(1\,\text{MHz})=10^{-120/10}=10^{-12}\ \text{(per Hz)}.
$$

The small-angle relation (spec Eq. 16) $\mathcal{L}\approx\tfrac12 S_\phi\Rightarrow S_\phi=2\mathcal{L}_{\text{lin}}$:

$$
S_\phi(1\,\text{MHz})=2\times10^{-12}=2\times10^{-12}\ \text{rad}^2/\text{Hz}.
$$

**(b) Set $K$, then integrate for $\sigma_t$.** With the $1/f^2$ model $S_\phi(f)=K/f^2$, use (a) to set $K$ at $f=10^6$ Hz:

$$
K=S_\phi(10^6)\cdot(10^6)^2=2\times10^{-12}\times10^{12}=2\ \text{rad}^2\cdot\text{Hz}.
$$

Phase variance (spec Eq. 18), integrated $f_1=10^6\to f_2=10^7$ Hz:

$$
\sigma_\phi^2=\int_{f_1}^{f_2}\frac{K}{f^2}df=K\!\left(\frac{1}{f_1}-\frac{1}{f_2}\right)=2\left(\frac{1}{10^6}-\frac{1}{10^7}\right)=2\times9\times10^{-7}=1.8\times10^{-6}\ \text{rad}^2.
$$

$$
\sigma_\phi=\sqrt{1.8\times10^{-6}}\approx1.342\times10^{-3}\ \text{rad}=1.342\ \text{mrad}.
$$

rms jitter (spec Eq. 19), with $f_0=5$ GHz:

$$
\sigma_t=\frac{\sigma_\phi}{2\pi f_0}=\frac{1.342\times10^{-3}}{2\pi\times5\times10^{9}}\approx4.27\times10^{-14}\ \text{s}=42.7\ \text{fs}.
$$

**Result**: $S_\phi(1\text{MHz})=2\times10^{-12}\ \text{rad}^2/\text{Hz}$, $\sigma_\phi\approx1.34$ mrad,
$\sigma_t\approx42.7$ fs (1→10 MHz band).

**Dimension check**: (a) $\mathcal{L}$ and $S_\phi$ are both per-Hz (rad²/Hz) ✓;
(b) $[K]\cdot[1/f]=\text{rad}^2\cdot\text{Hz}\cdot\text{Hz}^{-1}=\text{rad}^2$ ✓; $\dfrac{\text{rad}}{\text{rad/s}}=\text{s}$ ✓.

```python
import numpy as np
from simulations.common.noise_utils import integrate_rms_jitter
# Analytic path (direct substitution)
L_dbc = -120.0
S_phi_1M = 2*10**(L_dbc/10)              # = 2e-12 rad^2/Hz
K = S_phi_1M*(1e6)**2                    # = 2 rad^2*Hz
var = K*(1/1e6 - 1/1e7)
sigma_phi = np.sqrt(var)
sigma_t = sigma_phi/(2*np.pi*5e9)
print(sigma_phi*1e3, "mrad ;", sigma_t*1e15, "fs")   # -> 1.342 mrad ; 42.7 fs

# Numeric path (fold L(f)=K/f^2 back to dBc/Hz, then integrate); matches the analytic result
f = np.logspace(6, 7, 2000)
L_curve = 10*np.log10(0.5*K/f**2)        # L = S_phi/2 = (K/f^2)/2
st, sp = integrate_rms_jitter(f, L_curve, f0=5e9, fmin=1e6, fmax=1e7)
print(st*1e15, "fs (numeric)")           # -> ~42.7 fs
```

</details>

---

## Key takeaways

- **phase↔time**: $\Delta t=\Delta\phi/(2\pi f_0)$; rms version $\sigma_t=\sigma_\phi/(2\pi f_0)$ (Exercises 1, 2).
- **Parseval**: $\sum c_n^2=2\Gamma_{rms}^2$; for $-\sin$, $\Gamma_{rms}=1/\sqrt2$ and $\sum c_n^2=1$ (Exercise 3).
- **PSD integration**: in the $1/f^2$ region $\sigma_\phi^2$ is dominated by the **low-frequency end**; $\sigma_\phi^2=K(1/f_1-1/f_2)$ (Exercises 4, 8).
- **The essence of LTV**: the response depends on the **absolute injection phase**; the same impulse at different phases gives different $\Delta\phi$ (Exercise 5).
- **Lorentzian**: $D=\pi\Delta f_{3\mathrm{dB}}$, coherence time $\sim1/(2D)$ (Exercise 6, external literature).
- **Allan slopes**: $\tau^{-1/2}/\tau^0/\tau^{+1/2}\to$ white/flicker/random-walk FM; flicker FM forms a floor (Exercise 7, external literature).
- All Python verifications call `simulations/common/` (`noise_utils`, `isf_utils`) and can be reproduced directly.

## Further reading

- Phase/amplitude and jitter definitions: [oscillator_phase](/02_foundations/oscillator_phase), [phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise)
- PSD / phase noise / jitter: [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter)
- LTI vs LTV: [lti_vs_ltv](/02_foundations/lti_vs_ltv)
- Allan variance: [allan_variance](/02_foundations/allan_variance)
- Lorentzian linewidth: [lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth)
- More exercises: [03 core-theory chapter exercises](/03_isf_core_theory/exercises) · [06 design chapter exercises](/06_design_insights/exercises) · [04 simulation chapter worked examples](/04_simulation_labs/worked_examples)
