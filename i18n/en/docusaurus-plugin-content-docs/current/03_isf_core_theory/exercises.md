---
title: Core-Theory Chapter Exercises (with Full Solutions)
description: Complete exercise set for the ISF core-theory chapter — Γrms from the ISF, c0→1/f³ corner, white noise→L, impulse→phase, Fourier coefficients, effective ISF. Every problem comes with a step-by-step solution, units and dimension check, numerical answer, and a one-line Python verification.
---

> **β**: This English translation is in beta — the Traditional-Chinese original is the authoritative version.

import NumericQuiz from "@site/src/components/NumericQuiz";

# Core-Theory Chapter Exercises (with Full Solutions)

> **Prerequisite reading**: this chapter's theory pages [isf_definition](/03_isf_core_theory/isf_definition), [fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf), [rms_isf](/03_isf_core_theory/rms_isf), [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise), [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion), [effective_isf](/03_isf_core_theory/effective_isf) (finish them before attempting the problems).

This page is the complete exercise set for **Chapter 03, ISF Core Theory**. The problems span **derivations**, **numerical problems**, and **design back-calculations**,
all built around the [P1] Hajimiri–Lee ISF framework, using the site-wide notation.

> **Format**: every solution = **step-by-step substitution (with units) → result → dimension check → one-line Python verification**.
> Python always imports from `simulations/common/` (real functions, nothing fabricated).

Authoritative formulas involved (verbatim from spec Section 3, with citations):

- impulse→phase (operational ISF): $\Delta\phi=\dfrac{\Gamma(\omega_0\tau)}{q_{max}}\,\Delta q$ (spec formula 5)
- ISF Fourier series: $\Gamma(\omega_0\tau)=\dfrac{c_0}{2}+\displaystyle\sum_{n=1}^{\infty}c_n\cos(n\omega_0\tau+\theta_n)$ ([P1] Eq.(12), p.183)
- Parseval / rms ISF: $\displaystyle\sum_{n=0}^{\infty}c_n^2=\frac{1}{\pi}\int_0^{2\pi}\lvert\Gamma(x)\rvert^2dx=2\,\Gamma_{rms}^2$ ([P1] Eq.(20), p.185)
- The signature white-noise 1/f² result: $\mathcal{L}\{\Delta\omega\}=10\log_{10}\!\left(\dfrac{\Gamma_{rms}^2}{q_{max}^2}\cdot\dfrac{\overline{i_n^2}/\Delta f}{4\,\Delta\omega^2}\right)$ ([P1] Eq.(21), p.185)
- 1/f³ corner: $\Delta\omega_{1/f^3}=\omega_{1/f}\cdot\dfrac{c_0^2}{2\,\Gamma_{rms}^2}\approx\omega_{1/f}\left(\dfrac{c_0}{c_1}\right)^2$ ([P1] Eq.(24), p.185)
- effective ISF (cyclostationary): $\Gamma_{eff}=\Gamma\cdot\alpha$ ([P1] Eqs.(25)–(27), p.186)

---

## Problems

### Exercise 1 (numerical) — impulse → phase step

Ideal LC ($\Gamma(\theta)=-\sin\theta$), $q_{max}=1$ pC, $f_0=5$ GHz. A single charge impulse of $\Delta q=1$ fC
is injected. Find:
(a) the phase step $\Delta\phi$ (rad) and the timing error $\Delta t$ (fs) for injection at $\theta=3\pi/2$ (where $\Gamma$ takes its maximum $+1$).
(b) $\Delta\phi$ for injection at the peak, $\theta=0$.

<NumericQuiz
  prompt="Work out (a) yourself first: injection at θ = 3π/2 gives timing error Δt = ? (Δq = 1 fC, q_max = 1 pC, Γ = +1, f₀ = 5 GHz; answer in fs)"
  answer={31.8}
  unit="fs"
  hint="Δφ = Γ·Δq/q_max = 1×10⁻¹⁵/10⁻¹² = 1 mrad, then Δt = Δφ/(2πf₀)."
  solutionNote="Δt = 10⁻³/(2π×5×10⁹) ≈ 3.18×10⁻¹⁴ s = 31.8 fs (the Γ=1 full-scale version of canonical Example A). See the Exercise 1 solution below."
/>

### Exercise 2 (derivation + numerical) — $\Gamma_{rms}$ from the ISF

A toy ISF is the two-harmonic waveform $\Gamma(\theta)=\cos\theta+\tfrac12\cos(2\theta)$.
(a) Write down the Fourier coefficients $c_0,c_1,c_2$ directly.
(b) Use Parseval to find $\sum c_n^2$ and $\Gamma_{rms}$.

### Exercise 3 (numerical) — white noise → $\mathcal{L}$ (applying Eq.(21))

$f_0=5$ GHz, $\Delta f=1$ MHz, $q_{max}=1$ pC, $\Gamma_{rms}=0.5$, $S_i=\overline{i_n^2}/\Delta f=10^{-24}\ \text{A}^2/\text{Hz}$.
Use [P1] Eq.(21) to find $\mathcal{L}(1\,\text{MHz})$ (dBc/Hz).

<NumericQuiz
  prompt="Work it out yourself first: L(1 MHz) = ? (Γ_rms = 0.5, q_max = 1 pC, S_i = 10⁻²⁴ A²/Hz; answer in dBc/Hz, remember the minus sign)"
  answer={-148.0}
  tol={0.01}
  unit="dBc/Hz"
  hint="Eq.(21): L = 10·log₁₀[(Γ_rms²/q_max²)·S_i/(4Δω²)], with Δω = 2π×10⁶ rad/s, Δω² ≈ 3.95×10¹³."
  solutionNote="Bracketed factor = 2.5×10²³ × 6.33×10⁻³⁹ ≈ 1.58×10⁻¹⁵ → L ≈ −148.0 dBc/Hz (canonical Example B). See the Exercise 3 solution below."
/>

### Exercise 4 (design back-calculation) — solving for the required $q_{max}$

Keep the numbers from Exercise 3, but the target spec is now $\mathcal{L}(1\,\text{MHz})=-160$ dBc/Hz (cleaner than Exercise 3).
With all other parameters unchanged ($\Gamma_{rms}=0.5$, $S_i=10^{-24}$, $\Delta f=1$ MHz), by how much must $q_{max}$
be scaled up?

<NumericQuiz
  prompt="Work it out yourself first: q_max needed to reach −160 dBc/Hz = ? (the original q_max = 1 pC gives −148 dBc/Hz; answer in pC)"
  answer={3.98}
  unit="pC"
  hint="L_lin ∝ 1/q_max²; to squeeze out another 12 dB → scale q_max by 10^(12/20)."
  solutionNote="10^0.6 ≈ 3.98 → q_max ≈ 3.98 pC (every 6 dB reduction costs q_max ×2). See the Exercise 4 solution below."
/>

### Exercise 5 (derivation + numerical) — $c_0\to1/f^3$ corner

An oscillator's measured ISF has $c_0=0.2$, $c_1=1.0$ (i.e., an appreciable DC offset — the waveform is up/down asymmetric),
and the device 1/f corner is $f_{1/f}=1$ MHz (i.e., $\omega_{1/f}=2\pi\times10^6$ rad/s).
Use [P1] Eq.(24) to estimate the $1/f^3$ corner frequency $\Delta f_{1/f^3}$ (with the $c_0/c_1$ approximation).
If the circuit is made symmetric ($c_0\to0.02$), what does the corner become?

### Exercise 6 (derivation) — the frequency-translation meaning of the Fourier coefficients

For a single tone injected near $n\omega_0$, $i(\tau)=I_0\cos((n\omega_0+\Delta\omega)\tau)$, use the product-to-sum identity
to prove by hand that after weighting by the $n$-th ISF harmonic $c_n\cos(n\omega_0\tau+\theta_n)$ and integrating, the surviving
slow term gives $\phi_n(t)\approx\dfrac{I_0 c_n}{2q_{max}}\cdot\dfrac{\sin(\Delta\omega t-\theta_n)}{\Delta\omega}$,
and explain why this is exactly "the oscillator acting as a mixer, downconverting noise near $n\omega_0$ to $\Delta\omega$".

### Exercise 7 (numerical) — effective ISF (cyclostationary)

A certain noise source conducts only during one half-cycle of the waveform. Approximate its noise modulating function (NMF) $\alpha(\theta)$
as square-wave gating: $\alpha(\theta)=1$ for $\theta\in[0,\pi)$, $\alpha(\theta)=0$ for $\theta\in[\pi,2\pi)$.
The base ISF is still $\Gamma(\theta)=-\sin\theta$. Find $\Gamma_{eff,rms}$ of the effective ISF $\Gamma_{eff}=\Gamma\cdot\alpha$,
and compare with the always-conducting case $\Gamma_{rms}=1/\sqrt2$.

### Exercise 8 (design back-calculation) — $\Gamma_{rms}/q_{max}$ from $\mathcal{L}$

A 5 GHz LC oscillator measures $\mathcal{L}(1\,\text{MHz})=-130$ dBc/Hz, and its white-noise source is known to be
$S_i=2\times10^{-23}\ \text{A}^2/\text{Hz}$ (multi-source equivalent). Assuming the $1/f^2$ region is white-noise dominated, apply Eq.(21)
to back-solve the effective $\Gamma_{rms}/q_{max}$ (units $1/\text{C}$). If $q_{max}=1.5$ pC, roughly what is $\Gamma_{rms}$?

---

## Solutions

<details>
<summary><strong>Exercise 1 solution</strong> (impulse → phase step)</summary>

**(a) $\theta=3\pi/2$.** $\Gamma=-\sin(3\pi/2)=-(-1)=+1$. Using spec formula 5:

$$
\Delta\phi=\frac{\Gamma}{q_{max}}\Delta q=\frac{1\times(1\times10^{-15}\ \text{C})}{1\times10^{-12}\ \text{C}}=1\times10^{-3}\ \text{rad}=1\ \text{mrad}.
$$

Timing error (spec formula 17):

$$
\Delta t=\frac{\Delta\phi}{2\pi f_0}=\frac{10^{-3}}{2\pi\times5\times10^{9}}\approx3.18\times10^{-14}\ \text{s}=31.8\ \text{fs}.
$$

**(b) $\theta=0$.** $\Gamma=-\sin0=0\Rightarrow\Delta\phi=0$ (injection at the peak only changes the amplitude, which the restoring force pulls back).

**Result**: (a) $\Delta\phi=1$ mrad, $\Delta t\approx31.8$ fs; (b) $\Delta\phi=0$.

**Intuition**: this is the full-scale version of canonical Example A ($\Gamma=0.5$ gives 15.9 fs) — $\Gamma=1$ gives twice that, i.e. 31.8 fs.

**Dimension check**: $\Gamma$ dimensionless $\times$ (C/C) $=$ rad ✓; $\dfrac{\text{rad}}{\text{rad/s}}=\text{s}$ ✓.

```python
import numpy as np
from simulations.common.isf_utils import gamma_lc_ideal, impulse_to_phase_step
from simulations.common.noise_utils import phase_to_time_error
for th in (3*np.pi/2, 0.0):
    dphi = impulse_to_phase_step(1e-15, gamma_lc_ideal(th), qmax=1e-12)
    print(round(dphi*1e3,3), "mrad ;", round(phase_to_time_error(dphi,5e9)*1e15,1), "fs")
# -> 1.0 mrad ; 31.8 fs    and    0.0 mrad ; 0.0 fs
```

</details>

<details>
<summary><strong>Exercise 2 solution</strong> ($\Gamma_{rms}$ from the ISF)</summary>

**(a) Read off the coefficients.** Match $\Gamma(\theta)=\cos\theta+\tfrac12\cos(2\theta)$ against the Fourier series
$\Gamma=\tfrac{c_0}{2}+\sum c_n\cos(n\theta+\theta_n)$: no constant term $\Rightarrow c_0=0$;
first-harmonic amplitude $c_1=1$ ($\theta_1=0$); second-harmonic amplitude $c_2=\tfrac12$ ($\theta_2=0$); $c_{n\ge3}=0$.

**(b) Parseval.** Spec formula 11:

$$
\sum_{n=0}^{\infty}c_n^2=c_0^2+c_1^2+c_2^2=0+1^2+\left(\tfrac12\right)^2=1.25.
$$

$$
\Gamma_{rms}^2=\frac{\sum c_n^2}{2}=\frac{1.25}{2}=0.625\quad\Longrightarrow\quad\Gamma_{rms}=\sqrt{0.625}\approx0.791.
$$

**Result**: $c_0=0,\ c_1=1,\ c_2=0.5$; $\sum c_n^2=1.25$; $\Gamma_{rms}\approx0.791$.

**Cross-check** (direct integration): $\Gamma_{rms}^2=\tfrac{1}{2\pi}\int_0^{2\pi}(\cos\theta+\tfrac12\cos2\theta)^2d\theta$;
the cross term $\int\cos\theta\cos2\theta=0$ (orthogonality), leaving $\tfrac12+\tfrac12\cdot\tfrac14=0.5+0.125=0.625$ ✓.

**Dimension check**: $c_n$ and $\Gamma_{rms}$ are all dimensionless ✓.

```python
import numpy as np
from simulations.common.isf_utils import gamma_rms, compute_fourier_coefficients
theta = np.linspace(0, 2*np.pi, 8192, endpoint=False)
g = np.cos(theta) + 0.5*np.cos(2*theta)
print(gamma_rms(theta, g))                          # -> 0.7906
a0, a, b, c, ph = compute_fourier_coefficients(theta, g, n_harmonics=3)
print(c[:3], np.sum(c**2))                          # -> ~[1, 0.5] ... ; 1.25
```

</details>

<details>
<summary><strong>Exercise 3 solution</strong> (white noise → $\mathcal{L}$, applying Eq.(21))</summary>

**Step-by-step substitution (with units).** This is canonical Example B.

1. $\Delta\omega=2\pi\Delta f=2\pi\times10^6=6.283\times10^6\ \text{rad/s}$, $\Delta\omega^2=3.948\times10^{13}$.
2. $\dfrac{\Gamma_{rms}^2}{q_{max}^2}=\dfrac{0.25}{(10^{-12})^2}=2.5\times10^{23}\ \text{C}^{-2}$.
3. $\dfrac{S_i}{4\Delta\omega^2}=\dfrac{10^{-24}}{4\times3.948\times10^{13}}=6.332\times10^{-39}$.
4. Multiply: $2.5\times10^{23}\times6.332\times10^{-39}=1.583\times10^{-15}$.
5. $\mathcal{L}=10\log_{10}(1.583\times10^{-15})=-148.0\ \text{dBc/Hz}$.

**Result**: $\mathcal{L}(1\,\text{MHz})\approx-148.0$ dBc/Hz (the theoretical floor for a single ideal white-noise source).

**Dimension check**: inside the bracket, $\text{C}^{-2}\cdot\dfrac{\text{A}^2/\text{Hz}}{(\text{rad/s})^2}$; with $\text{C}=\text{A·s}$
this reduces to $\text{s}$ (per-Hz), and taking $10\log_{10}$ reads as dBc/Hz ✓. See
[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise).

```python
import numpy as np
gamma_rms, qmax, Si = 0.5, 1e-12, 1e-24
dw = 2*np.pi*1e6
L = 10*np.log10((gamma_rms**2/qmax**2)*(Si/(4*dw**2)))
print(round(L,1), "dBc/Hz")   # -> -148.0 dBc/Hz
```

</details>

<details>
<summary><strong>Exercise 4 solution</strong> (solving for the required $q_{max}$)</summary>

**Back-calculation strategy.** $\mathcal{L}\propto1/q_{max}^2$ (denominator of Eq.(21)). The target is
$\Delta L=-160-(-148)=-12$ dB below Exercise 3. Writing $\mathcal{L}$ in linear form with everything else fixed,
$\mathcal{L}_{\text{lin}}\propto1/q_{max}^2$:

$$
\frac{q_{max,\text{new}}^2}{q_{max,\text{old}}^2}=\frac{\mathcal{L}_{\text{lin,old}}}{\mathcal{L}_{\text{lin,new}}}=10^{(-148-(-160))/10}=10^{12/10}=10^{1.2}=15.85.
$$

$$
\frac{q_{max,\text{new}}}{q_{max,\text{old}}}=\sqrt{15.85}=3.98\quad\Longrightarrow\quad q_{max,\text{new}}\approx3.98\times1\ \text{pC}=3.98\ \text{pC}.
$$

**Direct check** (solving Eq.(21) for $q_{max}$ outright):
$q_{max}=\sqrt{\dfrac{\Gamma_{rms}^2}{\mathcal{L}_{\text{lin}}}\cdot\dfrac{S_i}{4\Delta\omega^2}}$,
with $\mathcal{L}_{\text{lin}}=10^{-16}$:

$$
q_{max}=\sqrt{\frac{0.25}{10^{-16}}\times6.332\times10^{-39}}=\sqrt{1.583\times10^{-23}}=3.98\times10^{-12}\ \text{C}=3.98\ \text{pC}.
$$

**Result**: $q_{max}$ must be scaled up by about **4×** to $\approx3.98$ pC (i.e., every 6 dB of phase-noise reduction costs $q_{max}$ $\times2$).

**Intuition**: this quantifies "**increasing the signal swing** is the most direct knob for lowering $1/f^2$ phase noise" (claim C3),
but 12 dB demands 4× the charge swing, paid for in power/area — exactly the trade-off in [tank_swing](/06_design_insights/tank_swing).

**Dimension check**: $\sqrt{\text{C}^{-2}\text{·s}^{-1}\cdots}$ inverts back to $q_{max}$ in C ✓.

```python
import numpy as np
gamma_rms, Si, dw = 0.5, 1e-24, 2*np.pi*1e6
L_lin = 10**(-160/10)
qmax = np.sqrt((gamma_rms**2/L_lin)*(Si/(4*dw**2)))
print(qmax*1e12, "pC")        # -> 3.98 pC
```

</details>

<details>
<summary><strong>Exercise 5 solution</strong> ($c_0\to1/f^3$ corner)</summary>

**Step-by-step substitution (with units).** Use the $c_0/c_1$ approximation of [P1] Eq.(24),
$\Delta\omega_{1/f^3}\approx\omega_{1/f}\left(\dfrac{c_0}{c_1}\right)^2$, then convert via $\Delta f_{1/f^3}=\Delta\omega_{1/f^3}/(2\pi)$;
since $\omega_{1/f}=2\pi f_{1/f}$, the $2\pi$ cancels: $\Delta f_{1/f^3}\approx f_{1/f}\left(\dfrac{c_0}{c_1}\right)^2$.

**Asymmetric case** ($c_0=0.2$, $c_1=1.0$):

$$
\Delta f_{1/f^3}\approx10^6\times\left(\frac{0.2}{1.0}\right)^2=10^6\times0.04=4\times10^{4}\ \text{Hz}=40\ \text{kHz}.
$$

**After symmetrization** ($c_0=0.02$, $c_1=1.0$):

$$
\Delta f_{1/f^3}\approx10^6\times\left(\frac{0.02}{1.0}\right)^2=10^6\times4\times10^{-4}=400\ \text{Hz}.
$$

**Result**: asymmetric, the $1/f^3$ corner is $\approx40$ kHz; after symmetrization ($c_0$ down 10×) the corner drops $100$× to $\approx400$ Hz.

**Validity (approximate vs exact form)**: the $(c_0/c_1)^2$ approximation assumes the ISF is **fundamental-dominated** ($\Gamma_{rms}^2\approx c_1^2/2$).
Here $c_0=0.2$ is not negligible; using the exact form $\Delta f_{1/f^3}=f_{1/f}\cdot\dfrac{c_0^2}{2\Gamma_{rms}^2}$,
with $\Gamma_{rms}^2=(c_0^2+c_1^2)/2=(0.04+1)/2=0.52$, gives
$\Delta f_{1/f^3}=10^6\times\dfrac{0.04}{2\times0.52}\approx38.5$ kHz — about 4% off the approximate 40 kHz.
After symmetrization ($c_0=0.02$, $\Gamma_{rms}^2\approx0.5$) the two forms nearly coincide.

**Design message**: $1/f^3$ corner $\propto c_0^2$. **Making the waveform up/down symmetric (suppressing $c_0$)** is the most effective way to
push flicker-upconverted close-in $1/f^3$ noise away from the carrier (see [symmetry](/06_design_insights/symmetry),
[flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)).

**Dimension check**: $(c_0/c_1)^2$ dimensionless $\times\ f_{1/f}$ (Hz) $=$ Hz ✓.

```python
f_1f = 1e6
for c0 in (0.2, 0.02):
    f_corner = f_1f*(c0/1.0)**2
    print(c0, "->", f_corner, "Hz")   # -> 0.2 -> 40000.0 Hz ; 0.02 -> 400.0 Hz
```

</details>

<details>
<summary><strong>Exercise 6 solution</strong> (frequency-translation meaning of the Fourier coefficients — derivation)</summary>

**Target expression.** The phase contribution of the $n$-th harmonic term ([P1] Eq.(13)):

$$
\phi_n(t)=\frac{1}{q_{max}}\int^{t}\!\!c_n\cos(n\omega_0\tau+\theta_n)\,I_0\cos\big((n\omega_0+\Delta\omega)\tau\big)\,d\tau.
$$

**Step (i): product-to-sum.** Let $A=n\omega_0\tau+\theta_n$, $B=(n\omega_0+\Delta\omega)\tau$, and use
$\cos A\cos B=\tfrac12[\cos(A-B)+\cos(A+B)]$:

$$
A-B=\theta_n-\Delta\omega\tau,\qquad A+B=(2n\omega_0+\Delta\omega)\tau+\theta_n.
$$

Integrand $=\dfrac{I_0c_n}{2}\Big[\underbrace{\cos(\Delta\omega\tau-\theta_n)}_{\text{slow term, }\approx\Delta\omega}+\underbrace{\cos((2n\omega_0+\Delta\omega)\tau+\theta_n)}_{\text{fast term, }\approx2n\omega_0}\Big]$.

**Step (ii): the integrator is a low-pass filter — the fast term averages out.**

- Slow term: $\int\cos(\Delta\omega\tau-\theta_n)d\tau=\dfrac{\sin(\Delta\omega\tau-\theta_n)}{\Delta\omega}$ — the denominator is only the tiny $\Delta\omega$, so it gets **amplified and survives**.
- Fast term: $\dfrac{\sin(\cdots)}{2n\omega_0+\Delta\omega}$ — the denominator is the huge $2n\omega_0$; the amplitude is crushed by a factor $\sim\Delta\omega/(2n\omega_0)$, hence **negligible**.

**Step (iii): keep only the slow term.**

$$
\phi_n(t)\approx\frac{1}{q_{max}}\cdot\frac{I_0c_n}{2}\cdot\frac{\sin(\Delta\omega t-\theta_n)}{\Delta\omega}=\frac{I_0 c_n}{2q_{max}}\cdot\frac{\sin(\Delta\omega t-\theta_n)}{\Delta\omega}.\qquad\blacksquare
$$

**Physical meaning (mixer view)**: the $n$-th ISF harmonic $c_n$ acts like one tooth of an LO (local-oscillator) comb, **downconverting**
noise at the injection frequency $n\omega_0+\Delta\omega$ to $\Delta\omega$ in baseband;
the fast term (sum frequency $\approx2n\omega_0$) is filtered out by the integrator's low-pass action. **The oscillator is itself a mixer sampling its own harmonics** —
this is why $c_n$ is "the conversion coefficient from each harmonic to the phase output" (see [fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf)).

**Dimension check**: the units of $\phi_n=\dfrac{I_0 c_n}{2q_{max}}\cdot\dfrac{\sin(\cdots)}{\Delta\omega}$ are
$\dfrac{[\text{A}]\cdot(\text{dimensionless})}{[\text{C}]\cdot[\text{rad/s}]}$; substituting $\text{C}=\text{A·s}$ and treating rad as dimensionless,
$=\dfrac{\text{A}}{(\text{A·s})\cdot(1/\text{s})}=\dfrac{\text{A}}{\text{A}}=1$ (dimensionless), so $\phi$ is dimensionless (phase in rad) ✓.

```python
import numpy as np
# Numerical check: do the integral directly; the slow term survives, the fast term vanishes
n, w0, dw, c_n, I0, qmax, th_n = 1, 1.0, 1e-3, 1.0, 1.0, 1.0, 0.4
tau = np.linspace(0, 2000*np.pi, 4_000_000)         # spans many slow periods
integrand = c_n*np.cos(n*w0*tau+th_n)*I0*np.cos((n*w0+dw)*tau)
phi = np.cumsum(integrand)*(tau[1]-tau[0])/qmax
analytic = I0*c_n/(2*qmax)*np.sin(dw*tau-th_n)/dw
print(np.max(np.abs(phi-analytic-np.mean(phi-analytic)))/np.max(np.abs(analytic)))
# -> slow-term envelope matches (relative error ~5e-4; the residual is the averaged-out fast term)
```

</details>

<details>
<summary><strong>Exercise 7 solution</strong> (effective ISF, cyclostationary)</summary>

**Step-by-step substitution.** effective ISF ([P1] Eqs.(25)–(27)): $\Gamma_{eff}(\theta)=\Gamma(\theta)\,\alpha(\theta)$.
Here $\alpha$ is square-wave gating (conducting for half the cycle), so

$$
\Gamma_{eff}(\theta)=\begin{cases}-\sin\theta,&\theta\in[0,\pi)\\[2pt]0,&\theta\in[\pi,2\pi).\end{cases}
$$

Take the rms:

$$
\Gamma_{eff,rms}^2=\frac{1}{2\pi}\int_0^{2\pi}\Gamma_{eff}^2\,d\theta=\frac{1}{2\pi}\int_0^{\pi}\sin^2\theta\,d\theta=\frac{1}{2\pi}\cdot\frac{\pi}{2}=\frac14.
$$

$$
\Gamma_{eff,rms}=\frac12=0.5.
$$

**Comparison**: always conducting gives $\Gamma_{rms}=1/\sqrt2\approx0.707$; with half-cycle gating, $\Gamma_{eff,rms}=0.5$.
The ratio is $0.5/0.707=1/\sqrt2$ — gating off half the phase drops the rms by $\sqrt2$ (halves the power).

**Result**: $\Gamma_{eff,rms}=0.5$ ($\approx3$ dB lower in power than the always-on $0.707$).

**Design message**: letting the noise conduct only at phases where the ISF is small greatly reduces its effective contribution — this is the
design intuition of **steering noise current away from the high-sensitivity region (the zero crossings)** (see [effective_isf](/03_isf_core_theory/effective_isf)).
The square-wave gating here is an illustrative toy; the real NMF $\alpha(\theta)$ is set by the device's bias-dependent thermal noise.

**Dimension check**: $\Gamma$, $\alpha$, $\Gamma_{eff}$ are all dimensionless ✓.

```python
import numpy as np
from simulations.common.isf_utils import gamma_lc_ideal, gamma_rms, effective_isf
theta = np.linspace(0, 2*np.pi, 8192, endpoint=False)
g = gamma_lc_ideal(theta)
alpha = (theta < np.pi).astype(float)          # half-cycle square-wave gating
g_eff = effective_isf(g, alpha)                # = g*alpha
print(gamma_rms(theta, g_eff))                 # -> 0.5
```

</details>

<details>
<summary><strong>Exercise 8 solution</strong> ($\Gamma_{rms}/q_{max}$ from $\mathcal{L}$)</summary>

**Back-calculation strategy.** Solve Eq.(21) for $\dfrac{\Gamma_{rms}^2}{q_{max}^2}$:

$$
\frac{\Gamma_{rms}^2}{q_{max}^2}=\frac{\mathcal{L}_{\text{lin}}}{S_i/(4\Delta\omega^2)}=\mathcal{L}_{\text{lin}}\cdot\frac{4\Delta\omega^2}{S_i}.
$$

**Step-by-step substitution (with units).**

1. $\mathcal{L}_{\text{lin}}=10^{-130/10}=10^{-13}$.
2. $\Delta\omega=2\pi\times10^6=6.283\times10^6$, $4\Delta\omega^2=4\times3.948\times10^{13}=1.579\times10^{14}$.
3. $\dfrac{4\Delta\omega^2}{S_i}=\dfrac{1.579\times10^{14}}{2\times10^{-23}}=7.896\times10^{36}$.
4. $\dfrac{\Gamma_{rms}^2}{q_{max}^2}=10^{-13}\times7.896\times10^{36}=7.896\times10^{23}\ \text{C}^{-2}$.
5. $\dfrac{\Gamma_{rms}}{q_{max}}=\sqrt{7.896\times10^{23}}=8.886\times10^{11}\ \text{C}^{-1}$.

**If $q_{max}=1.5$ pC**:

$$
\Gamma_{rms}=\frac{\Gamma_{rms}}{q_{max}}\times q_{max}=8.886\times10^{11}\times1.5\times10^{-12}=1.33.
$$

**Result**: $\Gamma_{rms}/q_{max}\approx8.89\times10^{11}\ \text{C}^{-1}$; if $q_{max}=1.5$ pC, then $\Gamma_{rms}\approx1.33$.

**Intuition check**: $\Gamma_{rms}\approx1.33$ is somewhat above the ideal $-\sin$ value $0.707$ — reasonable, because this part's measured phase noise
($-130$ dBc/Hz) sits about 18 dB above the canonical single ideal white-noise source ($-148$), reflecting the reality of multiple sources, cyclostationarity,
and a larger ISF. **The back-calculation serves as a health check: does the measured PN imply an effective $\Gamma_{rms}$ that is too large?**

**Dimension check**: $\mathcal{L}_{\text{lin}}$ (per-Hz $=$ s) $\times\dfrac{(\text{rad/s})^2}{\text{A}^2/\text{Hz}}=\text{s}\cdot\dfrac{\text{s}^{-2}}{\text{A}^2\text{s}}=\text{A}^{-2}\text{s}^{-2}=\text{C}^{-2}$ ✓.

```python
import numpy as np
L_lin, Si, dw = 10**(-130/10), 2e-23, 2*np.pi*1e6
ratio2 = L_lin*(4*dw**2/Si)              # (Gamma_rms/qmax)^2
ratio = np.sqrt(ratio2)
print(ratio, "1/C ;", ratio*1.5e-12, "= Gamma_rms")   # -> 8.89e11 1/C ; 1.33
```

</details>

---

## Key takeaways

- **impulse→phase**: $\Delta\phi=\Gamma\,\Delta q/q_{max}$; $\Gamma=1$ at 5 GHz gives 31.8 fs (Exercise 1).
- **$\Gamma_{rms}$ from the ISF**: Parseval $\sum c_n^2=2\Gamma_{rms}^2$; two-harmonic example $\Gamma_{rms}=0.791$ (Exercise 2).
- **White noise→$\mathcal{L}$**: canonical Example B $\approx-148$ dBc/Hz (Exercise 3); back-solving $q_{max}$: every 6 dB lower costs $\times2$ (Exercise 4).
- **$c_0\to1/f^3$ corner**: corner $\propto c_0^2$; symmetrizing by 10× → corner drops 100× (Exercise 5).
- **Fourier coefficients = mixer conversion**: $c_n$ downconverts noise near $n\omega_0$ to $\Delta\omega$; fast terms are filtered out by the integrator (Exercise 6).
- **effective ISF**: half-cycle gating gives $\Gamma_{eff,rms}=0.5 < 0.707$; steering noise away from high-sensitivity regions lowers noise (Exercise 7).
- **Back-solving $\Gamma_{rms}/q_{max}$**: measured PN can health-check whether the effective ISF is too large (Exercise 8).
- All Python verifications import from `simulations/common/` (`isf_utils`, `noise_utils`).

## Further reading

- impulse→phase: [impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift)
- white noise→$\mathcal{L}$: [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)
- Fourier series: [fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf)
- $\Gamma_{rms}$ and Parseval: [rms_isf](/03_isf_core_theory/rms_isf)
- flicker upconversion and symmetry: [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)
- effective ISF: [effective_isf](/03_isf_core_theory/effective_isf)

## Other exercises

- Foundations chapter exercises (PSD / jitter dialects / random processes): [02 Foundations exercises](/02_foundations/exercises)
- Design chapter exercises (swing / topology / PLL budget / SerDes back-calculation): [06 Design chapter exercises](/06_design_insights/exercises)
- Graded worked examples (basic conversions / ISF→PN / jitter integration / design back-calculation; each with a step-by-step solution + Python verification): [worked_examples](/04_simulation_labs/worked_examples)
