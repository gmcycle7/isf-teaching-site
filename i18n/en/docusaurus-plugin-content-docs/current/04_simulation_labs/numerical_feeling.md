---
title: Numerical Feeling
description: "Three must-do mental-math drills that turn conversions among rad, fs, dBc/Hz, and jitter into muscle memory."
---

> **β**: This English translation is in beta — the Traditional-Chinese original is the authoritative version.

# Numerical Feeling

However beautiful the theory, without numbers there is no feel. This page uses three small
examples to turn the conversions among phase, time, dBc/Hz, and jitter
into reflexes. Each example comes with a Python check; the full library lives in
`simulations/common/`.

> **Formula sources**: the phase/time/jitter conversions and the 1/f² integral are all
> standard results, consistent with
> [P1] A. Hajimiri and T. H. Lee, *"A General Theory of Phase Noise in Electrical
> Oscillators,"* IEEE JSSC, 33(2), 1998 (especially Eq.(21)); step-by-step derivations in
> [impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift) and
> [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter).

> **Why drill the numbers first**: an analog designer's ability to estimate orders of
> magnitude at the whiteboard matters more than memorizing formulas. Given
> "$-100$ dBc/Hz @ 1 MHz, 5 GHz," you should be able to estimate "a few hundred fs of jitter"
> within 30 seconds.

## Example 1: phase → time

> Given $f_0=5$ GHz and $\Delta\phi=1$ mrad, find the timing error.

$$
\Delta t=\frac{\Delta\phi}{2\pi f_0}=\frac{1\times10^{-3}\ \text{rad}}{2\pi\times5\times10^{9}\ \text{Hz}}=\frac{10^{-3}}{3.1416\times10^{10}}\ \text{s}\approx3.18\times10^{-14}\ \text{s}=31.8\ \text{fs}.
$$

- **Dimension check**: $[\text{rad}]/[\text{rad/s}]=[\text{s}]$ ✓ ($2\pi f_0$ is in rad/s).
- **Feel**: at 5 GHz, "1 mrad ≈ 32 fs." The period is 200 ps, so 1 mrad is about $1.6\times10^{-4}$ of a period.

```python
from simulations.common.noise_utils import phase_to_time_error
print(phase_to_time_error(1e-3, 5e9) * 1e15, "fs")   # -> 31.83 fs
```

## Example 2: injected charge → phase step → time

> Given $q_{max}=1$ pC, $\Delta q=1$ fC, $\Gamma=0.5$, find the phase step and the timing error (at 5 GHz).

**Phase step**:

$$
\Delta\phi=\frac{\Gamma\,\Delta q}{q_{max}}=\frac{0.5\times10^{-15}}{10^{-12}}=5\times10^{-4}\ \text{rad}\;(\approx0.0286^\circ).
$$

**Timing error** ($f_0=5$ GHz):

$$
\Delta t=\frac{5\times10^{-4}}{2\pi\times5\times10^{9}}\approx15.9\ \text{fs}.
$$

- **Feel**: 1 fC ≈ 6240 electrons; even at the most sensitive phase it only kicks out ~16 fs.
  Each kick is tiny, but noise keeps kicking and
  the phase integrator accumulates it (see [convolution_derivation](/03_isf_core_theory/convolution_derivation)).
- Full derivation in [impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift) (Example A).

```python
from simulations.common.isf_utils import impulse_to_phase_step
from simulations.common.noise_utils import phase_to_time_error
dphi = impulse_to_phase_step(1e-15, 0.5, 1e-12)
print(dphi, "rad ->", phase_to_time_error(dphi, 5e9)*1e15, "fs")  # 0.0005 rad -> 15.92 fs
```

## Example 3: phase noise plot → rms jitter (you must be able to integrate)

> Given $\mathcal{L}(1\,\text{MHz})=-100$ dBc/Hz, assuming a 1/f² slope, integrating from 1 MHz to 100 MHz,
> $f_0=5$ GHz, estimate the rms jitter.

**Step 1: convert dBc/Hz to linear and recover the phase PSD.**
Under the single-tone small-angle approximation $\mathcal{L}(f)\approx\frac12 S_\phi(f)$, so $S_\phi(f)=2\cdot10^{\mathcal{L}(f)/10}$.
At 1 MHz: $\mathcal{L}=-100$ dBc/Hz $\Rightarrow 10^{-10}$, $S_\phi(1\text{MHz})=2\times10^{-10}$ rad²/Hz.

**Step 2: write down the 1/f² shape.** Anchored at $f_{ref}=1$ MHz:

$$
S_\phi(f)=S_\phi(f_{ref})\left(\frac{f_{ref}}{f}\right)^2=2\times10^{-10}\left(\frac{10^6}{f}\right)^2.
$$

**Step 3: integrate to get the phase variance.**

$$
\sigma_\phi^2=\int_{f_1}^{f_2}S_\phi(f)\,df=2\times10^{-10}\,(10^6)^2\!\int_{10^6}^{10^8}\frac{df}{f^2}=2\times10^{2}\left(\frac{1}{10^6}-\frac{1}{10^8}\right).
$$

$$
\sigma_\phi^2=200\times(10^{-6}-10^{-8})=200\times9.9\times10^{-7}=1.98\times10^{-4}\ \text{rad}^2\Rightarrow\sigma_\phi=1.407\times10^{-2}\ \text{rad}=14.07\ \text{mrad}.
$$

**Step 4: convert to rms jitter.**

$$
\sigma_t=\frac{\sigma_\phi}{2\pi f_0}=\frac{1.407\times10^{-2}}{2\pi\times5\times10^{9}}\approx4.48\times10^{-13}\ \text{s}=447.9\ \text{fs}.
$$

- **Feel**: the integral is **dominated by the lower limit $f_1$** (the $1/f_1$ term is
  largest) — so "where you start integrating" is critical for 1/f².
- **Reference point**: if this part were $-120$ dBc/Hz @ 1 MHz (10× better in power,
  $\sqrt{10^2}=10$× in voltage), the jitter shrinks to roughly ~45 fs.
- This is exactly the figure of [lab_08](/04_simulation_labs/lab_08_jitter_integration); the numerical integration matches the analytic expression exactly.

![rms jitter obtained by integrating L(f)](/figures/phase_noise_to_jitter_integration.png)

```python
import numpy as np
from simulations.common.noise_utils import leeson_one_over_f2, integrate_rms_jitter

f  = np.logspace(6, 8, 4000)                 # 1 MHz -> 100 MHz
L  = leeson_one_over_f2(f, L_ref_dbc=-100, f_ref=1e6)   # 1/f^2 skirt
sigma_t, sigma_phi = integrate_rms_jitter(f, L, f0=5e9, fmin=1e6, fmax=100e6)
print(sigma_phi*1e3, "mrad ;", sigma_t*1e15, "fs")   # -> 14.07 mrad ; 447.9 fs
```

Full script: `simulations/lab_08_jitter_integration.py`.

## Parameter and unit quick reference

| Quantity | Symbol | Unit | Conversion |
|---|---|---|---|
| Phase error | $\Delta\phi,\sigma_\phi$ | rad | $1$ rad $=180/\pi\approx57.3^\circ$ |
| Timing error | $\Delta t,\sigma_t$ | s | $\Delta t=\Delta\phi/(2\pi f_0)$ |
| phase PSD | $S_\phi$ | rad²/Hz | $S_\phi=2\cdot10^{\mathcal{L}/10}$ |
| SSB phase noise | $\mathcal{L}$ | dBc/Hz | $\mathcal{L}\approx\frac12 S_\phi$ (→ dB) |
| Charge | $\Delta q,q_{max}$ | C | 1 fC $=10^{-15}$ C |

## Key takeaways

- **5 GHz conversion anchors**: 1 mrad ≈ 32 fs; 1 rad ≈ 31.8 ps.
- dBc/Hz → linear → $S_\phi=2\times$linear → integrate → square root → $\div(2\pi f_0)$ = rms jitter.
- 1/f² jitter is dominated by the **lower** integration limit.
- All the numbers in these three examples can be checked in one line with the built-in functions in `simulations/common/`.
