---
title: Waveform Symmetry and Flicker Upconversion
description: Why a waveform with symmetric rise/fall "blocks" 1/f device noise from close-in — how the ISF's c0 sets the 1/f³ corner, and the design knobs for lowering c0.
---

> **β**: This English translation is in beta — the Traditional-Chinese original is the authoritative version.

# Waveform Symmetry and Flicker Upconversion

> **Prerequisites**: [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion) (the full flicker → $1/f^3$ derivation; this page is its design-facing counterpart), [fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf) (the ISF's Fourier coefficients $c_0,c_n$ and Parseval), [device_noise_mapping](/06_design_insights/device_noise_mapping) (the $c_0$ of the effective ISF $\Gamma_{eff}=\Gamma\cdot\alpha$ is the real culprit) | **Next**: [waveform_slope](/06_design_insights/waveform_slope), [serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)

This page answers a question that must be settled at the layout/topology stage: **why does a waveform
with symmetric rise/fall have noticeably lower close-in (near-carrier) 1/f³ phase noise?** The answer is
hidden entirely in one Fourier coefficient of the ISF — the DC term $c_0$.

> **Physical intuition (conclusion first)**: a device's flicker noise (1/f noise, slow-varying noise in
> the gate/channel) is a **near-DC, low-frequency** noise. Low-frequency noise should not normally
> contaminate a high-frequency carrier — but the ISF is a **periodic function**, and its DC component
> $c_0/2$ acts like a "rectifier": it accumulates low-frequency device noise **with a persistent sign**
> into the phase, **upconverting** it to a close-in 1/f³ skirt near the carrier. If the rise/fall is
> perfectly symmetric, the ISF's positive and negative areas cancel over one period, $c_0\to0$, and this
> upconversion channel is shut off.

## Step 1: why only $c_0$ upconverts flicker

Write the ISF as a Fourier series ([P1] Eq.(12), p.183):

$$
\Gamma(\omega_0\tau)=\frac{c_0}{2}+\sum_{n=1}^{\infty}c_n\cos(n\omega_0\tau+\theta_n)
$$

Substitute into the LTV phase response ([P1] Eq.(13), p.183), splitting the phase into contributions
from each harmonic:

$$
\phi(t)=\frac{1}{q_{max}}\!\left[\frac{c_0}{2}\!\int_{-\infty}^{t}\!i_n\,d\tau+\sum_{n=1}^{\infty}c_n\!\int_{-\infty}^{t}\!i_n\cos(n\omega_0\tau+\theta_n)\,d\tau\right]
$$

- **Key observation**: device flicker-noise energy is concentrated **near DC** ($\Delta\omega\ll\omega_0$).
  In the expression above, every $c_n$ term ($n\ge1$) carries a $\cos(n\omega_0\tau+\theta_n)$ factor, which
  multiplies the low-frequency noise by a high-frequency carrier — a **mixing** operation that moves the
  noise to near $\pm n\omega_0$, **away from** DC.
- Only the **$c_0/2$ term has no carrier**: it performs a **pure integration** of the low-frequency noise.
  Low-frequency noise stays nearly the same sign over an extended interval, so the integral
  **accumulates without cancelling**, continuously driving the close-in phase → upconverted into 1/f³.
- **In one line**: $c_n$ acts like a mixer (it moves the noise away), while $c_0$ acts like an integrator
  (it retains and amplifies DC noise).

## Step 2: 1/f³ phase noise and the corner formula

Feed the device flicker model ([P1] Eq.(22), p.185)

$$
\overline{i_{n,1/f}^2}=\overline{i_n^2}\cdot\frac{\omega_{1/f}}{\Delta\omega}
$$

into the phase noise from the $c_0$-only channel to get the 1/f³ region ([P1] Eq.(23), p.185):

$$
\mathcal{L}\{\Delta\omega\}=10\log_{10}\!\left(\frac{c_0^2}{q_{max}^2}\cdot\frac{\overline{i_n^2}/\Delta f}{8\,\Delta\omega^2}\cdot\frac{\omega_{1/f}}{\Delta\omega}\right)
$$

- **Slope dimension check**: $1/\Delta\omega^2$ (from the phase integration) times $1/\Delta\omega$ (from
  flicker's $\omega_{1/f}/\Delta\omega$ factor) = $1/\Delta\omega^3$ → $-30$ dB per decade, exactly 1/f³. ✓
- **Key point**: the numerator is $c_0^2$. **A symmetric waveform drives $c_0\to0$ → the entire 1/f³
  region is suppressed.**

Intersecting the 1/f³ region with the 1/f² region ([P1] Eq.(21)) defines the **1/f³ corner** ([P1] Eq.(24), p.185):

$$
\Delta\omega_{1/f^3}=\omega_{1/f}\cdot\frac{c_0^2}{2\,\Gamma_{rms}^2}\approx\omega_{1/f}\left(\frac{c_0}{c_1}\right)^2
$$

**Step-by-step algebra: how the corner falls out of "the two regions are equal."** The corner is defined
as the offset where the 1/f³ region and the 1/f² region are **exactly equal in height**. Setting the two
(linear, not-yet-log) power spectral densities equal:

$$
\begin{aligned}
\underbrace{\frac{c_0^2}{q_{max}^2}\cdot\frac{\overline{i_n^2}/\Delta f}{8\,\Delta\omega^2}\cdot\frac{\omega_{1/f}}{\Delta\omega}}_{\text{1/f}^3\text{ region (inside the brackets of Eq.23)}}
&=\underbrace{\frac{\Gamma_{rms}^2}{q_{max}^2}\cdot\frac{\overline{i_n^2}/\Delta f}{4\,\Delta\omega^2}}_{\text{1/f}^2\text{ region (inside the brackets of Eq.21)}} \\[4pt]
\frac{c_0^2}{8}\cdot\frac{\omega_{1/f}}{\Delta\omega}&=\frac{\Gamma_{rms}^2}{4}
\qquad(\text{both sides cancel }q_{max}^2,\ \overline{i_n^2}/\Delta f,\ \Delta\omega^2) \\[4pt]
\frac{\omega_{1/f}}{\Delta\omega}&=\frac{\Gamma_{rms}^2}{4}\cdot\frac{8}{c_0^2}=\frac{2\,\Gamma_{rms}^2}{c_0^2} \\[4pt]
\Rightarrow\quad \Delta\omega=\Delta\omega_{1/f^3}&=\omega_{1/f}\cdot\frac{c_0^2}{2\,\Gamma_{rms}^2}.
\end{aligned}
$$

- **What each step uses**: the second line is just "dividing out the factors common to both sides" (pure
  algebra, no new physics); note that $\overline{i_n^2}/\Delta f$, $q_{max}^2$, and $\Delta\omega^2$ are
  **the same value** in both regions, so they cancel.
- **Why $\Delta\omega^2$ also cancels**: the 1/f³ region is $1/\Delta\omega^3$, the 1/f² region is
  $1/\Delta\omega^2$; dividing leaves a single $1/\Delta\omega$ — exactly the $\omega_{1/f}/\Delta\omega$
  factor still on the left in line 2 above. Solving this linear equation gives the corner.
- **Getting to $\approx(c_0/c_1)^2$**: using Parseval ([P1] Eq.(20)) $2\Gamma_{rms}^2=\sum c_n^2$; if the
  ISF is dominated by its fundamental ($c_1\gg c_2,c_3,\dots$), then $2\Gamma_{rms}^2\approx c_1^2$,
  giving $\Delta\omega_{1/f^3}\approx\omega_{1/f}(c_0/c_1)^2$.
- **Dimension check**: on the right, $\omega_{1/f}$ is rad/s, and $c_0^2/(2\Gamma_{rms}^2)$ is
  dimensionless/dimensionless = dimensionless, so $\Delta\omega_{1/f^3}$ is rad/s ✓.

- **The most important design implication (claim C5)**: the 1/f³ corner is **not equal to** the device's
  1/f corner $\omega_{1/f}$! It is scaled by a factor $c_0^2/(2\Gamma_{rms}^2)$. The smaller $c_0$ is, the
  further the corner is **pushed below** $\omega_{1/f}$ — i.e., for the same transistor with the same
  device 1/f corner, simply making the waveform symmetric can push the 1/f³ skirt's knee down several
  decades in frequency.
- **Notation trap** (see [notation](/00_overview/notation)): $c_0$ is the Fourier **coefficient**; the
  ISF's DC **value** is $c_0/2$. Eq.(24) uses the coefficient $c_0$ — don't drop a factor of 2 here.

## Step 3: how symmetry drives $c_0\to0$

$c_0$ is (twice) the ISF's average over one period:

$$
\frac{c_0}{2}=\frac{1}{2\pi}\int_0^{2\pi}\Gamma(x)\,dx\quad\Rightarrow\quad c_0=\frac{1}{\pi}\int_0^{2\pi}\Gamma(x)\,dx
$$

- The ISF's shape is roughly **proportional to the waveform slope** (large slope near a zero crossing →
  large $|\Gamma|$; zero slope at the peak → $\Gamma\approx0$; see [waveform_slope](/06_design_insights/waveform_slope)).
- If the rise and fall segments have **symmetric shapes** (rise slope = mirror image of fall slope), the
  ISF values over the rising and falling half-periods are **equal in magnitude, opposite in sign**, and
  cancel when integrated over one period → $c_0=0$.
- An ideal LC's $\Gamma(\theta)=-\sin\theta$ is exactly this kind of **odd symmetry**:
  $\int_0^{2\pi}(-\sin\theta)\,d\theta=0$, so an ideal LC naturally has $c_0=0$ and very weak 1/f³ upconversion.
- Asymmetry (e.g. fast rise, slow fall, or even-order harmonics that make the waveform top/bottom
  asymmetric) shifts the ISF's average away from 0 → $c_0\neq0$.

The figure below overlays a symmetric and an asymmetric ISF: the symmetric one has its DC average pinned
at 0, while the asymmetric one is lifted by a "DC offset" of $c_0/2$ — that offset is the culprit behind
flicker upconversion.

![symmetric vs. asymmetric ISF and their c0](/figures/symmetric_vs_asymmetric_isf_c0.png)

Feeding actual device flicker into a simulation makes the close-in difference very clear: the asymmetric
waveform shows a steep 1/f³ skirt, while the symmetric waveform shows almost none (only 1/f² and the floor
remain).

![flicker upconversion for symmetric vs. asymmetric waveforms](/figures/flicker_upconversion_symmetric_vs_asymmetric.png)

> Both figures are **pedagogical toy models (not transistor-level)**: the ISF uses an analytic shape
> (symmetric $\cos\theta$, asymmetric $\cos\theta+0.4$, etc.), and flicker is a synthesized 1/f sequence.
> They faithfully illustrate "$c_0$ determines 1/f³" causally, but are not a measurement of any real
> transistor. Full scripts: `simulations/lab_05_fourier_isf.py`, `simulations/lab_07_flicker_noise.py`.

## Numerical example (building intuition)

> Using canonical numbers plus an assumed device 1/f corner.

**Symmetric waveform ($c_0\approx0$)**: theoretically $\Delta\omega_{1/f^3}=\omega_{1/f}\cdot
c_0^2/(2\Gamma_{rms}^2)\to0$, and the 1/f³ corner is pushed to extremely low frequency — in practice it is
dominated by the small residual $c_0$ set by mismatch (see the knobs table below).

**Asymmetric waveform**: take $c_0=0.4$, $\Gamma_{rms}=0.5$ (so $c_0^2/(2\Gamma_{rms}^2)=0.16/(2\times0.25)=0.32$).
If the device $f_{1/f}=1$ MHz, then

$$
f_{1/f^3}=f_{1/f}\cdot\frac{c_0^2}{2\Gamma_{rms}^2}=1\ \text{MHz}\times0.32=320\ \text{kHz}.
$$

- **Intuition**: lowering $c_0$ from 0.4 to 0.04 (10× smaller) drops the corner by 100× ($c_0^2$) — from
  320 kHz down to 3.2 kHz. In other words, **each order-of-magnitude improvement in symmetry shrinks the
  reach of the 1/f³ skirt by two orders of magnitude** — an extremely cost-effective design lever.
- Corresponding experimental evidence: [P2] Fig. 17, p.802 measures ring-oscillator phase noise vs.
  "symmetry control voltage," which shows a **minimum at the symmetry point** — direct support for the
  design rule "symmetric → low 1/f³."
  (Verified: [P2] Fig. 17, p.802, "Phase noise versus symmetry voltage for oscillator number 7" — the
  y-axis is the 1/f³ corner frequency, showing a clear dip to a minimum at the symmetry point.)

## Design knobs for lowering $c_0$ (checklist)

| Knob | How | Why it lowers $c_0$ | Cost/notes |
|---|---|---|---|
| Symmetric rise/fall | NMOS/PMOS drive-strength or pull-up/pull-down symmetry (ring); differential topology | ISF's upper and lower half-periods cancel → average → 0 | needs sizing/bias tuning; process offset leaves residual $c_0$ |
| Differential / even-harmonic suppression | fully differential, symmetric loads, suppress even harmonics | even harmonics make the waveform top/bottom asymmetric → raise $c_0$ | 2× devices, area, power |
| Symmetric load (ring) | use a symmetric load ([P2]'s approach) instead of a single-ended inverter delay cell | matches rise/fall shape | [P2] Fig. 17's "symmetry voltage" tunes exactly this |
| Reduce DC-bias-point drift | control duty cycle near 50% | duty deviating from 50% means a DC-asymmetric waveform → $c_0\neq0$ | needs duty-cycle correction |
| Directly lower device flicker | use large-area, PMOS, buried-channel devices | lowers $\omega_{1/f}$ itself (does not change $c_0$, but lowers the magnitude of 1/f³) | large area → large parasitic capacitance → lowers $f_0$ |

> Note the two categories: the first four knobs change **$c_0$ / the $f_{1/f^3}$ corner location**; the
> last one changes **the device $\omega_{1/f}$ / the overall height of 1/f³**. Both can be used in design,
> but "making it symmetric" is usually free (no extra power) — take that shot first.

## Validity and failure conditions

| Condition | Holds when | Fails when |
|---|---|---|
| Small perturbation, ISF known and fixed | $c_0$ fully determines 1/f³ | under large injection/strong nonlinearity the ISF itself changes |
| Device noise is pure 1/f | the $\omega_{1/f}/\Delta\omega$ model holds | with RTS/burst noise, a separate calculation is needed |
| Cyclostationarity already folded into the effective ISF | compute $c_0$ using $\Gamma_{eff}=\Gamma\cdot\alpha$ | if $\alpha$ is also asymmetric, it can "recreate" a nonzero effective $c_0$ (see [device_noise_mapping](/06_design_insights/device_noise_mapping)) |

> **Important warning**: what actually determines the upconversion is the $c_0$ of the **effective ISF
> $\Gamma_{eff}=\Gamma\cdot\alpha$**, not just the $c_0$ of the bare $\Gamma$. Even if $\Gamma$ is
> symmetric, if the device only "leaks noise" during half the period ($\alpha$ is asymmetric), the
> effective $c_0$ of $\Gamma_{eff}$ can still be nonzero. See [device_noise_mapping](/06_design_insights/device_noise_mapping)
> and [effective_isf](/03_isf_core_theory/effective_isf).

## Worked examples

The following two examples demonstrate the most cost-effective design lever — "improving symmetry lowers
the 1/f³ corner" — reusing this site's canonical $\Gamma_{rms}=0.5$, device $f_{1/f}=1$ MHz.

> **Example 1 (baseline: compute the 1/f³ corner for an asymmetric waveform)**
> Given $c_0=0.4$, $\Gamma_{rms}=0.5$, device 1/f corner $f_{1/f}=1$ MHz, find the 1/f³ corner $f_{1/f^3}$.

**Step-by-step substitution (with units)**, using the just-derived $f_{1/f^3}=f_{1/f}\cdot c_0^2/(2\Gamma_{rms}^2)$:

$$
\begin{aligned}
\frac{c_0^2}{2\Gamma_{rms}^2}&=\frac{(0.4)^2}{2\times(0.5)^2}=\frac{0.16}{0.50}=0.32\quad(\text{dimensionless}) \\[4pt]
f_{1/f^3}&=f_{1/f}\times0.32=1\ \text{MHz}\times0.32=0.32\ \text{MHz}=320\ \text{kHz}.
\end{aligned}
$$

- **Result**: $f_{1/f^3}=320$ kHz — **lower** than the device's own 1 MHz corner, because
  $c_0^2/(2\Gamma_{rms}^2)=0.32 < 1$.
- **Dimension check**: $[\text{Hz}]\times[\text{dimensionless}]=[\text{Hz}]$ ✓ (a ratio of frequencies
  works equally in Hz or rad/s, since $f_{1/f^3}/f_{1/f}=\omega_{1/f^3}/\omega_{1/f}$ and the $2\pi$'s cancel).
- **One-line Python check** (using the canonical conversion; `simulations/common/` has no dedicated
  corner function, so compute it directly):

```python
c0, gamma_rms, f_1f = 0.4, 0.5, 1e6
f_1f3 = f_1f * c0**2 / (2 * gamma_rms**2)
print(f_1f3 / 1e3, "kHz")   # -> 320.0 kHz
```

> **Example 2 (improving symmetry by one order of magnitude → corner drops two orders of magnitude)**
> Make the waveform more symmetric so $c_0$ drops from $0.4$ to $0.04$ (10× smaller), with $\Gamma_{rms}$
> and $f_{1/f}$ unchanged. Find the new corner, and express in dB how much the heights of the two 1/f³
> asymptotes (extrapolated skirts) differ.

**Step-by-step substitution (with units)**:

$$
\begin{aligned}
f_{1/f^3}'&=f_{1/f}\cdot\frac{(c_0')^2}{2\Gamma_{rms}^2}=1\ \text{MHz}\times\frac{(0.04)^2}{2\times(0.5)^2}
=1\ \text{MHz}\times\frac{0.0016}{0.5}=1\ \text{MHz}\times3.2\times10^{-3}=3.2\ \text{kHz}.
\end{aligned}
$$

The corner drops from $320$ kHz → $3.2$ kHz (a 100× reduction $=$ the square of the $c_0$ ratio, $10^2$).
Note that after improvement the corner falls to $3.2$ kHz, so $\Delta f=10$ kHz for the improved waveform
now lies in the **1/f² region** (no longer 1/f³); what follows compares the heights of the two **1/f³
asymptotes (extrapolated skirts)**. 1/f³ phase noise ([P1] Eq.(23)) $\propto c_0^2$, so the change in
height is

$$
\Delta\mathcal{L}=10\log_{10}\!\left(\frac{(c_0')^2}{c_0^2}\right)=10\log_{10}\!\left(\frac{0.04^2}{0.4^2}\right)=10\log_{10}(0.01)=-20\ \text{dB}.
$$

- **Result**: lowering $c_0$ by 10× → the 1/f³ skirt overall drops **20 dB**, and the corner drops **100×**
  (to 3.2 kHz). "Each order-of-magnitude improvement in symmetry shrinks the reach of 1/f³ by two orders
  of magnitude" is exactly this $c_0^2$ law.
- **Dimension check**: dB is a log of a power ratio (dimensionless) ✓; the corner is still in Hz ✓.
- **One-line Python check**:

```python
import numpy as np
c0_old, c0_new = 0.4, 0.04
print("corner ratio:", (c0_new/c0_old)**2,            # -> 0.01  (3.2 kHz / 320 kHz)
      "; dL =", 10*np.log10((c0_new/c0_old)**2), "dB") # -> -20.0 dB
```

> Both examples are **pedagogical toys (not transistor-level)**: $c_0$ uses assumed values representing
> "residual asymmetry." A real circuit's $c_0$ must be extracted from the effective ISF (including
> cyclostationary $\alpha$); see [device_noise_mapping](/06_design_insights/device_noise_mapping).

## Key takeaways

- Only the ISF's DC coefficient $c_0$ upconverts device 1/f noise into close-in 1/f³ ([P1] Eq.(23)).
- 1/f³ corner $=\omega_{1/f}\cdot c_0^2/(2\Gamma_{rms}^2)$, **not equal to** the device's 1/f corner ([P1] Eq.(24)).
- Symmetric rise/fall → the ISF cancels over one period → $c_0\to0$ → the 1/f³ corner is pushed to very low frequency.
- Lowering $c_0$ by 10× lowers the 1/f³ corner by 100× ($c_0^2$): asymmetric $c_0=0.4$, $f_{1/f}=1$ MHz → corner 320 kHz.
- Design levers: differential, symmetric loads, 50% duty; must look at the $c_0$ of the **effective** ISF (including $\alpha$).
- Experiment: [P2] Fig. 17, phase noise vs. symmetry voltage, shows a minimum.

## Further reading

- Full upconversion derivation: [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)
- Why $\Gamma$'s shape tracks the waveform slope: [waveform_slope](/06_design_insights/waveform_slope)
- Effective ISF and $\alpha$: [device_noise_mapping](/06_design_insights/device_noise_mapping), [effective_isf](/03_isf_core_theory/effective_isf)
- Fourier coefficients and Parseval: [fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf)
- Why SerDes cares more about close-in: [serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)
