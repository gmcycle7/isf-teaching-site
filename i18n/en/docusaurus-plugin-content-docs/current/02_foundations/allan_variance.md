---
title: "Allan Variance: The Time-Domain Counterpart of Phase Noise"
description: "Starting from the two-sample (Allan) variance σy²(τ)=⟨½(ȳ_{k+1}−ȳ_k)²⟩, we derive step by step the frequency-domain integral σy²=2∫S_y sin⁴(πfτ)/(πfτ)² df with S_y=(f²/f0²)S_φ, and build the ADEV slope table for the five power-law noise types (white/flicker PM τ⁻¹, white FM τ⁻¹ᐟ², flicker FM τ⁰ floor, RW FM τ^{+1/2}), explaining why the clock community uses ADEV rather than the ordinary frequency variance. Embeds the allan_deviation figure, with 2 worked examples (estimating ADEV from L(f))."
---

> **β**: This English translation is in beta — the Traditional-Chinese original is the authoritative version.

# Allan Variance: The Time-Domain Counterpart of Phase Noise

> Prerequisites: [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter) · [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) ｜ Next: [serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)

The previous pages all viewed oscillator imperfection from the **frequency domain**: jitter was written as SSB phase noise $\mathcal{L}(\Delta f)$ (in dBc/Hz) or as the phase PSD $S_\phi(f)$ (in $\text{rad}^2/\text{Hz}$), then integrated into an rms jitter $\sigma_t$ (see [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter)). That language is the natural one for RF/communication circuits. But the people who work on **clocks, frequency standards, GPS, and atomic clocks** speak another language: the **Allan variance** and its square root, the **Allan deviation / ADEV** $\sigma_y(\tau)$. This page answers:

- What does $\sigma_y(\tau)$ actually measure? Why is it defined as the mean square of the "**difference between two adjacent gated frequency averages**"?
- How does it convert to the familiar $S_\phi(f)$ and $\mathcal{L}(\Delta f)$?
- Why does each of the **five power-law noise types** trace a characteristic slope on the ADEV log–log plot, so that the slopes "read out the noise type at a glance"?
- Why does the clock community **prefer ADEV over the ordinary sample variance of frequency**?

> **Physical intuition (conclusion first)**: take a stopwatch (the oscillator under test) and compare it against a perfect clock; every $\tau$ seconds record "over this $\tau$-second gate, how much faster/slower was my average frequency than nominal", producing a string of **fractional frequency deviations** $\bar y_k$. The ordinary variance asks "how far are these $\bar y_k$ from their grand mean" — but for flicker ($1/f$) and random-walk noise, **the grand mean simply does not exist** (it keeps drifting the longer you collect data), so the ordinary variance grows and grows without converging. Allan's trick: **do not compare against the grand mean — compare only against the neighboring gate** — $\tfrac12\langle(\bar y_{k+1}-\bar y_k)^2\rangle$. The adjacent subtraction cancels out the "slow drift", so even for flicker/RW noise the result converges and can be measured repeatably as a stable number. The price: it becomes a **function of $\tau$** — the gate length $\tau$ you choose sets the time scale at which you probe stability.

ADEV is "phase noise in the time domain": the same physics (the same $S_\phi(f)$), just viewed in a different coordinate. Below we connect the two sides step by step.

## Step 1: the fractional frequency deviation $y(t)$ and its PSD $S_y(f)$

First, define the protagonist. Let the instantaneous phase of the signal under test be $\omega_0 t+\phi(t)$, where $\phi(t)$ is the excess phase (the random offset relative to the ideal linear phase, in rad). The **instantaneous fractional frequency deviation** (dimensionless) is defined as the time derivative of the phase deviation divided by the nominal angular frequency:

$$
y(t)=\frac{1}{\omega_0}\frac{d\phi(t)}{dt}=\frac{1}{2\pi f_0}\,\dot\phi(t).
$$

- **Physical meaning**: $y$ is "by what fraction the frequency right now exceeds the nominal frequency". $y=10^{-9}$ means the frequency is off by 1 ppb (one part per billion).
- **Unit check**: $\dot\phi$ is $\text{rad/s}$, $\omega_0$ is $\text{rad/s}$; the ratio is dimensionless ✓. $y$ being dimensionless is exactly what "fractional" means.

**Relation between the PSD of $y$ and the PSD of $\phi$.** Differentiation multiplies by $j2\pi f$ in the frequency domain, so the power spectrum is multiplied by the squared magnitude $(2\pi f)^2$. Hence (spec §11.2):

$$
S_y(f)=\frac{(2\pi f)^2}{(2\pi f_0)^2}\,S_\phi(f)=\frac{f^2}{f_0^2}\,S_\phi(f).
$$

- **Math used**: for a stationary process $a(t)\to\dot a(t)$, the PSD is multiplied by $|j2\pi f|^2=(2\pi f)^2$ (the LTI filter $H(f)=j2\pi f$).
- **Unit check**: $S_\phi$ is $\text{rad}^2/\text{Hz}$; multiplied by the dimensionless $f^2/f_0^2$, $S_y$ has units $1/\text{Hz}$ (the PSD of a dimensionless quantity) ✓.
- **Key marker**: this $S_y=(f^2/f_0^2)S_\phi$ is the adapter between "phase noise ↔ frequency noise" — the entire slope table below hinges on it. Differentiation **adds 2** to the power of $f$: $S_\phi\sim f^{-2}$ (our signature $1/f^2$) corresponds to $S_y\sim f^{0}$ (white FM).

## Step 2: definition of the two-sample (Allan) variance

Slice the continuous $y(t)$ into gates of length $\tau$; the **average fractional frequency** of the $k$-th gate is

$$
\bar y_k=\frac{1}{\tau}\int_{t_k}^{t_k+\tau}y(t)\,dt=\frac{x(t_k+\tau)-x(t_k)}{\tau},
\qquad x(t)\equiv\int^{t}y(t')\,dt'=\frac{\phi(t)}{2\pi f_0}.
$$

Here $x(t)$ is the **time error** (the accumulated time offset of the clock under test relative to an ideal clock, in s) — note that it is exactly the phase divided by $2\pi f_0$, i.e. the $\Delta t=\Delta\phi/(2\pi f_0)$ of [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter). So $\bar y_k$ is nothing but "the difference of the time error at two adjacent instants, divided by the gate length".

The **two-sample (Allan) variance** is defined as the mean square of the difference between adjacent gated frequency averages, times $\tfrac12$ (spec §11.2):

$$
\sigma_y^2(\tau)=\Big\langle\tfrac12\big(\bar y_{k+1}-\bar y_k\big)^2\Big\rangle.
$$

ADEV is its square root, $\sigma_y(\tau)=\sqrt{\sigma_y^2(\tau)}$.

- **What the $\tfrac12$ is for**: if $\bar y_{k+1}$ and $\bar y_k$ are mutually independent, each with variance $\sigma^2$, then $\langle(\bar y_{k+1}-\bar y_k)^2\rangle=2\sigma^2$, and the factor $\tfrac12$ restores exactly $\sigma^2$. In other words, **for white FM (independent adjacent gates) this normalization makes ADEV equal to the classical standard deviation** — Allan chose it deliberately so that in the most common case the two languages agree numerically.
- **Why "adjacent differences"**: differencing is a **high-pass** operation that blocks DC and very low frequencies (slow drift, aging, the unknown grand mean). This is the secret of its convergence even for flicker/RW noise (detailed in Step 5).
- **Unit check**: $\bar y$ dimensionless → $\sigma_y^2$ dimensionless, $\sigma_y$ dimensionless ✓.

**Written as a "second difference" of the time error $x$.** Substituting $\bar y_k=[x(t_{k}+\tau)-x(t_k)]/\tau$, for adjacent gates ($t_{k+1}=t_k+\tau$):

$$
\bar y_{k+1}-\bar y_k=\frac{x_{k+2}-2x_{k+1}+x_k}{\tau},
$$

where $x_k\equiv x(t_k)$ and the sampling interval is $\tau$. The numerator $x_{k+2}-2x_{k+1}+x_k$ is exactly the **second difference** of the time error (a discrete second derivative). This is precisely what the line `d = x[2m:] - 2*x[m:-m] + x[:-2m]` does in the simulation script `lab_19_allan.py`.

## Step 3: moving the definition to the frequency domain — the transfer-function kernel $\sin^4(\pi f\tau)/(\pi f\tau)^2$

The target we want to prove is (spec §11.2):

$$
\sigma_y^2(\tau)=2\int_0^{\infty}S_y(f)\,\frac{\sin^4(\pi f\tau)}{(\pi f\tau)^2}\,df.
$$

Derivation strategy: $\sigma_y^2(\tau)$ is the **power of a linearly filtered signal**, and the power after linear filtering $=\int S_{\text{in}}(f)\,|H(f)|^2\,df$. We only need to find the transfer function $H(f)$ of the operation "from $y(t)$ to $\tfrac{1}{\sqrt2}(\bar y_{k+1}-\bar y_k)$" and compute its $|H(f)|^2$.

**Step (i): gate averaging = convolution with a rectangular window.** $\bar y_k=\frac1\tau\int_{t_k}^{t_k+\tau}y\,dt$ is $y$ convolved with a rectangular window of width $\tau$ and height $1/\tau$, sampled at $t_k$. The frequency response of the rectangular window is a sinc:

$$
H_{\text{avg}}(f)=\frac{1}{\tau}\int_0^{\tau}e^{-j2\pi f t}\,dt=e^{-j\pi f\tau}\,\frac{\sin(\pi f\tau)}{\pi f\tau}.
$$

- **Math used**: rectangular window $\leftrightarrow$ sinc (a basic Fourier-transform pair).
- $\dfrac{\sin(\pi f\tau)}{\pi f\tau}$ is the normalized sinc; the prefactor $e^{-j\pi f\tau}$ is the linear phase due to the window center.

**Step (ii): adjacent subtraction = multiplication by a first-difference kernel.** $\bar y_{k+1}-\bar y_k$ shifts the same gate average by $\tau$ and subtracts, which in the frequency domain multiplies by $\big(e^{-j2\pi f\tau}-1\big)$, whose squared magnitude is

$$
\big|e^{-j2\pi f\tau}-1\big|^2=2-2\cos(2\pi f\tau)=4\sin^2(\pi f\tau).
$$

(Using the half-angle identity $1-\cos2\theta=2\sin^2\theta$ with $\theta=\pi f\tau$.)

**Step (iii): multiply the three pieces together.** The overall operation $g(t)=\tfrac{1}{\sqrt2}(\bar y_{k+1}-\bar y_k)$ (the $\tfrac{1}{\sqrt2}$ is the square root of the $\tfrac12$ in the definition) has the transfer-function magnitude squared:

$$
|H(f)|^2=\underbrace{\tfrac12}_{\text{def.}\,\frac12}\cdot\underbrace{\Big(\frac{\sin(\pi f\tau)}{\pi f\tau}\Big)^2}_{\text{gate average}}\cdot\underbrace{4\sin^2(\pi f\tau)}_{\text{adjacent difference}}=\frac{2\sin^4(\pi f\tau)}{(\pi f\tau)^2}.
$$

**Step (iv): apply Wiener–Khinchin (power = ∫ PSD × |H|²).** Using the single-sided PSD ($\int_0^\infty$):

$$
\sigma_y^2(\tau)=\int_0^{\infty}S_y(f)\,|H(f)|^2\,df=2\int_0^{\infty}S_y(f)\,\frac{\sin^4(\pi f\tau)}{(\pi f\tau)^2}\,df.\qquad\checkmark
$$

This is the frequency-domain integral of spec §11.2.

- **Physical meaning**: $\sin^4/(\cdot)^2$ is a **band-pass kernel**: near $f\to0$ it behaves like $f^2$ (high-pass, blocking slow drift), at high frequency like $1/f^2$ (low-pass, suppressing ultra-fast noise), with its peak near $f\tau\sim 0.5$. **Choosing $\tau$ means choosing which frequency band this band-pass looks at** — large $\tau$ probes low frequencies, small $\tau$ high frequencies.
- **Unit check**: $S_y$ is $1/\text{Hz}$, the kernel is dimensionless, $df$ is Hz; the integral is dimensionless → $\sigma_y^2$ dimensionless ✓.

> **This is the bridge showing "time domain ↔ frequency domain are the same thing"**: given any $S_\phi(f)$, first convert it to $S_y$ via Step 1, then substitute into this integral to get ADEV; conversely, a measured ADEV can be inverted back to $S_y$ and $S_\phi$. The entire slope table below is nothing but this integral evaluated for power laws $S_y\sim f^\alpha$.

## Step 4: the ADEV slope table for the five power-law noise types

The frequency-standards community writes noise as a **superposition of power laws** (the power-law model). Each type is described by $S_y(f)=h_\alpha f^\alpha$, with $\alpha$ running from $-2$ to $+2$. Substituting each into the Step-3 integral gives the characteristic slope $\sigma_y(\tau)\propto\tau^\mu$. The table below is the **core reference table** of frequency metrology (PM = phase modulation, FM = frequency modulation):

| Noise type | $S_\phi(f)$ slope | $S_y(f)=\frac{f^2}{f_0^2}S_\phi$ slope | $\sigma_y^2(\tau)\propto$ | **ADEV $\sigma_y(\tau)\propto$** |
|---|---|---|---|---|
| white PM | $f^{0}$ | $f^{+2}$ | $\tau^{-2}$ | $\tau^{-1}$ |
| flicker PM | $f^{-1}$ | $f^{+1}$ | $\tau^{-2}$ (with $\ln$ correction) | $\tau^{-1}$ |
| white FM | $f^{-2}$ | $f^{0}$ | $\tau^{-1}$ | $\tau^{-1/2}$ |
| flicker FM | $f^{-3}$ | $f^{-1}$ | $\tau^{0}$ | $\tau^{0}$ (floor) |
| random-walk FM | $f^{-4}$ | $f^{-2}$ | $\tau^{+1}$ | $\tau^{+1/2}$ |

> Note the single most important row: our signature **white FM ($S_\phi\sim1/f^2$, produced from white noise by phase integration; see [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)) corresponds to an ADEV slope of $\tau^{-1/2}$**. In other words, the $-20$ dB/decade phase-noise skirt appears on the time-domain ADEV plot as a line of slope $-1/2$.

### Why each slope is what it is

**(a) white FM → $\tau^{-1/2}$ (the one to remember).** $S_y\sim f^0$ is white; $y(t)$ is white noise. $\bar y_k$ averages white noise over a gate $\tau$ — averaging $N$ independent samples of white noise reduces the variance by $1/N\propto1/\tau$, hence $\sigma_y^2\propto1/\tau$ and $\sigma_y\propto\tau^{-1/2}$. **Intuition**: the longer you measure, the steadier the average — the standard error falls like $1/\sqrt{\tau}$; this is the familiar $\sqrt N$ law of "under white frequency noise, longer averaging is more accurate". Equivalently, $y$ white ⇒ the time error $x=\int y$ is a random walk; the variance of adjacent-gate differences $\propto\tau$, and dividing by $\tau^2$ gives $\propto1/\tau$.

**(b) flicker FM → $\tau^{0}$ (the floor).** $S_y\sim1/f$ ($1/f$ frequency noise). The remarkable property of a $1/f$ process is **scale invariance**: it looks statistically the same at every time scale. Feed it into the band-pass kernel and the integral comes out **independent of $\tau$** — ADEV becomes a horizontal line. **Intuition**: the device's $1/f$ (flicker) noise upconverts into $1/f^3$ phase noise (see [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)); in the time domain it becomes the **floor** where "no amount of extra averaging time makes you any more stable". This floor is the **fundamental limit** of long-term stability in quartz/atomic oscillators, known in engineering as the flicker floor.

**(c) random-walk FM → $\tau^{+1/2}$ (heading upward).** $S_y\sim1/f^2$; $y(t)$ itself is a random walk (integrated white noise). The longer the averaging time, the further $y$ itself has already wandered, so the adjacent-gate differences actually **grow**: $\sigma_y^2\propto\tau$, $\sigma_y\propto\tau^{+1/2}$. **Intuition**: temperature drift, precursors of aging — low-frequency processes that "wander ever farther" — get worse the longer you measure. The right half of an ADEV plot bending upward is usually this.

**(d) white PM and flicker PM → both $\tau^{-1}$ (steepest, left side).** PM-type noise is concentrated at high frequency ($S_y\sim f^{+2}$, $f^{+1}$) and is strongly suppressed by the $\text{sinc}^2$ of the gate average, so it drops off quickly as $\tau$ is stretched: ADEV $\propto\tau^{-1}$ (steeper than white FM's $\tau^{-1/2}$). **Intuition**: pure phase noise (e.g., additive white noise of the measurement system, buffer thermal noise) is prominent at small $\tau$ and gets averaged away at large $\tau$. **Note**: white PM and flicker PM have the **same ADEV slope (both $\tau^{-1}$) and cannot be distinguished** — this is a real weakness of ADEV, which motivated the improved **MDEV (modified Allan deviation)**: under MDEV, white PM follows $\tau^{-3/2}$ and flicker PM follows $\tau^{-1}$, making them separable (MDEV is an extension topic not developed here).

**Mnemonic**: from left to right, as $\tau$ grows from small to large, the ADEV slope walks $-1\to-1/2\to0\to+1/2$ — a **bathtub curve** that "drops, bottoms out, then climbs". The minimum at the bottom corresponds to the **optimal averaging time** $\tau_{\text{opt}}$ — the $\tau$ to pick for the most stable measurement or timekeeping.

## Step 5: why does the clock community use ADEV instead of the ordinary frequency variance?

This is the "why" at the heart of this page. Suppose you want the most intuitive description of frequency stability: take $M$ frequency samples $\bar y_k$ and compute the **ordinary sample variance** (also called the N-sample / standard variance)

$$
\sigma^2_{\text{std}}(M,\tau)=\frac{1}{M-1}\sum_{k=1}^{M}\big(\bar y_k-\overline{\bar y}\big)^2,\qquad\overline{\bar y}=\frac1M\sum_k\bar y_k.
$$

The problem is that it **subtracts the "grand mean" $\overline{\bar y}$**.

**For white FM, no problem.** White FM is stationary, $\overline{\bar y}$ converges to the true value, and $\sigma^2_{\text{std}}$ converges too, consistent with ADEV.

**For flicker FM and random-walk FM it blows up.** These two have strong (even divergent) low-frequency energy:

- They are **non-ergodic in the mean**: $\overline{\bar y}$ does not converge; the longer you measure and the larger $M$ gets, the more $\overline{\bar y}$ itself keeps drifting.
- Consequently $\sigma^2_{\text{std}}(M,\tau)$ **grows monotonically with the sample count $M$ and never converges** — the "frequency instability" you report depends on "how long you measured", which is a metrological disaster (not repeatable, not comparable).
- Mathematically: the equivalent kernel of the standard variance against $S_y(f)$ behaves only like $f^0$ as $f\to0$ (DC is not blocked); against $S_y\sim1/f$ or $1/f^2$, the integrals $\int_0\frac{df}{f}$ and $\int_0\frac{df}{f^2}$ **diverge at low frequency**.

**ADEV's fix: replace "subtract the grand mean" with "adjacent differences".** Step 3 showed that ADEV's equivalent kernel behaves like $f^2$ as $f\to0$ ($\sin^4(\pi f\tau)\sim(\pi f\tau)^4$, divided by $(\pi f\tau)^2$, gives $\sim f^2$). This $f^2$ high-pass **tames the low-frequency divergence**:

- flicker FM ($S_y\sim1/f$): the integrand $\sim f^2\cdot f^{-1}=f$, convergent as $f\to0$ ✓.
- random-walk FM ($S_y\sim1/f^2$): the integrand $\sim f^2\cdot f^{-2}=f^0$, still convergent as $f\to0$ (a borderline case, but finite) ✓.

So ADEV is a **convergent, repeatable, measurement-duration-independent** well-defined quantity all the way up to random-walk FM. That is the fundamental reason David Allan proposed it in 1966 and the frequency-standards community (NIST, IEEE) adopted it as the standard:

> **In one sentence**: the ordinary frequency variance **does not converge** for flicker/RW noise (it diverges the longer you collect data); ADEV uses the first difference "subtract the adjacent gate" to block the low-frequency drift, buying a stability metric that is **convergent in $\tau$ and repeatably measurable**.

- **Extensions**: if you also need to distinguish white PM from flicker PM, use MDEV; to ask "is a given time error bounded", use TDEV / time variance. This page focuses on the most commonly used overlapping ADEV.

## Corresponding simulation figure

**lab_19** (`simulations/lab_19_allan.py`) generates the fractional frequency $y(t)$ for the three FM noise types by FFT shaping, integrates it into the time error $x(t)=\int y\,dt$, and then estimates the **overlapping Allan deviation**: for each $\tau=m\tau_0$, take the mean square of the second difference $x_{k+2m}-2x_{k+m}+x_k$ and the square root. In the figure, solid lines are the simulated ADEV, dashed lines the theoretical slopes; the three slopes land precisely on $-1/2$, $0$, and $+1/2$:

![Allan deviation of the three FM noise types, with slopes white FM τ⁻¹ᐟ², flicker FM τ⁰, and random-walk FM τ^{+1/2}](/figures/allan_deviation.png)

| Item | Value | Notes |
|---|---|---|
| Model | toy / illustrative (not transistor-level) | synthesizes $S_y\sim f^\alpha$ by FFT power-law shaping |
| white FM | $S_y\sim f^{0}$ | ADEV slope $\tau^{-1/2}$ (blue) |
| flicker FM | $S_y\sim f^{-1}$ | ADEV slope $\tau^{0}$, flicker floor (green) |
| random-walk FM | $S_y\sim f^{-2}$ | ADEV slope $\tau^{+1/2}$ (red) |
| Estimator | overlapping ADEV | second-difference kernel $x_{k+2m}-2x_{k+m}+x_k$ |
| Vertical axis | normalized $\sigma_y/\sigma_y(\tau_0)$ | compares slopes only; absolute scale arbitrary |

Core Python (full script: `simulations/lab_19_allan.py`, function `overlapping_adev`):

```python
import numpy as np

def overlapping_adev(x, tau0, ms):
    """Compute the overlapping Allan deviation from time-error samples x (spacing tau0)."""
    x = np.asarray(x); N = len(x); out = []
    for m in ms:
        if N - 2 * m < 1:
            out.append(np.nan); continue
        d = x[2 * m:] - 2 * x[m:-m] + x[:-2 * m]      # second difference of the time error
        avar = np.sum(d ** 2) / (2 * (N - 2 * m) * (m * tau0) ** 2)
        out.append(np.sqrt(avar))
    return np.array(out)
```

The `d` line is the second difference $x_{k+2m}-2x_{k+m}+x_k$ of Step 2; dividing by $2(N-2m)(m\tau_0)^2$ corresponds to the discrete estimate of $\sigma_y^2=\langle\tfrac12(\bar y_{k+1}-\bar y_k)^2\rangle$ (with $\tau=m\tau_0$).

## Worked examples

The two problems below follow the strict format: **problem → step-by-step substitution (with units) → result → dimension check → one-line Python verification**. The first practices "reading slopes off the plot"; the second demonstrates **estimating ADEV from $\mathcal{L}(f)$** (the most useful engineering conversion).

### Example 1: reading the noise type from two ADEV points and extrapolating

> **Problem**: an OCXO (oven-controlled crystal oscillator) measures $\sigma_y(1\,\text{s})=2\times10^{-12}$ and $\sigma_y(10\,\text{s})=6.3\times10^{-13}$. Which noise type dominates in this range? Extrapolate $\sigma_y(100\,\text{s})$.

**Steps:**

1. Compute the slope $\mu$ ($\sigma_y\propto\tau^\mu$):

$$
\mu=\frac{\log_{10}\!\big(\sigma_y(10)/\sigma_y(1)\big)}{\log_{10}(10/1)}=\frac{\log_{10}(6.3\times10^{-13}/2\times10^{-12})}{\log_{10}10}=\frac{\log_{10}(0.315)}{1}\approx-0.5.
$$

2. Consulting the Step-4 table: $\mu=-1/2$ ⇒ **white FM dominates** ($S_y\sim f^0$, equivalently $S_\phi\sim1/f^2$).
3. Extrapolate to $\tau=100\,\text{s}$ (still white FM, $\tau^{-1/2}$):

$$
\sigma_y(100)=\sigma_y(1)\times(100)^{-1/2}=2\times10^{-12}\times\frac{1}{10}=2\times10^{-13}.
$$

**Result:** white FM dominates; $\sigma_y(100\,\text{s})\approx2\times10^{-13}$.

**Dimension check:** $\sigma_y$ is dimensionless throughout (fractional frequency); the slope $\mu$ is a ratio of logs of two dimensionless quantities, hence dimensionless ✓.

```python
import numpy as np
mu = np.log10(6.3e-13/2e-12)/np.log10(10)          # -> -0.50  => white FM
adev_100 = 2e-12*(100/1)**mu
print(round(mu,2), f"{adev_100:.2e}")              # -> -0.5  2.00e-13
```

### Example 2: estimating ADEV from the white-noise $1/f^2$ region of $\mathcal{L}(f)$

> **Problem**: a 5 GHz oscillator measures $\mathcal{L}(1\,\text{MHz})=-100\,\text{dBc/Hz}$ in the 1/f² region (the white-FM segment). Estimate how $\sigma_y(\tau)$ scales with $\tau$, and give the numerical value of $\sigma_y(1\,\text{ms})$. Uses the setup of canonical Example C ($f_0=5\,\text{GHz}$).

**Steps:**

1. **dBc/Hz → linear $\mathcal{L}$**: $\mathcal{L}(1\,\text{MHz})=10^{-100/10}=10^{-10}\,\text{rad}^2/\text{Hz}$ (single-sided).
2. **$\mathcal{L}\to S_\phi$** (small-angle $\mathcal{L}\approx\tfrac12 S_\phi$, see spec Eq.16): $S_\phi(1\,\text{MHz})=2\mathcal{L}=2\times10^{-10}\,\text{rad}^2/\text{Hz}$.
3. **Write the explicit $1/f^2$ form**: in the white-FM segment $S_\phi(f)=\dfrac{h_{-2}}{f^2}$. Substituting $f=10^6$: $h_{-2}=S_\phi(10^6)\cdot(10^6)^2=2\times10^{-10}\times10^{12}=2\times10^{2}=200\,\text{rad}^2\,\text{Hz}$.
4. **Convert to $S_y$**: $S_y(f)=\dfrac{f^2}{f_0^2}S_\phi=\dfrac{f^2}{f_0^2}\cdot\dfrac{h_{-2}}{f^2}=\dfrac{h_{-2}}{f_0^2}\equiv h_0$ (white indeed — independent of $f$).
   $h_0=\dfrac{200}{(5\times10^9)^2}=\dfrac{200}{2.5\times10^{19}}=8.0\times10^{-18}\,\text{Hz}^{-1}$.
5. **Closed form of ADEV for white FM** (a standard result, obtained by integrating the Step-3 kernel with $S_y=h_0$):

$$
\sigma_y^2(\tau)=\frac{h_0}{2\tau}\quad\Longrightarrow\quad\sigma_y(\tau)=\sqrt{\frac{h_0}{2\tau}}.
$$

6. Substituting $\tau=10^{-3}\,\text{s}$: $\sigma_y^2=\dfrac{8.0\times10^{-18}}{2\times10^{-3}}=4.0\times10^{-15}$, $\sigma_y=6.3\times10^{-8}$.

**Result:** $S_y$ is white with $h_0=8.0\times10^{-18}\,\text{Hz}^{-1}$; $\sigma_y(\tau)=\sqrt{h_0/2\tau}\propto\tau^{-1/2}$ (consistent with white FM); $\sigma_y(1\,\text{ms})\approx6.3\times10^{-8}$.

**Dimension check:** $h_0$ has units $\text{Hz}^{-1}=\text{s}$; $h_0/\tau$ is dimensionless; the square root remains dimensionless → $\sigma_y$ dimensionless ✓. The slope $\sigma_y\propto\tau^{-1/2}$ matches the white-FM row of the table ✓.

> **Feel for the numbers**: $6.3\times10^{-8}$ looks large at 1 ms, but a free-running 5 GHz oscillator does drift away a lot of phase within 1 ms (which is exactly why a PLL/CDR is used to pin the long-term frequency; see [serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)). Stretch $\tau$ to 1 s and $\sigma_y$ drops by another factor $\sqrt{1000}\approx31.6$ to $\sim2\times10^{-9}$.

```python
import numpy as np
f0, L_dbc, foff = 5e9, -100.0, 1e6
S_phi = 2*10**(L_dbc/10)                 # rad^2/Hz at foff (small-angle L≈½S_φ)
h_2   = S_phi*foff**2                     # S_phi = h_2/f^2  => h_2
h0    = h_2/f0**2                         # S_y = h0 (white FM)
adev  = lambda tau: np.sqrt(h0/(2*tau))
print(f"{h0:.1e}", f"{adev(1e-3):.1e}")  # -> 8.0e-18  6.3e-08
```

(The white-FM closed form $\sigma_y^2=h_0/2\tau$ is a standard frequency-metrology result; lab_19 on this site verifies only the slope, not the absolute constant — the numbers are for illustration.)

## Applicability and failure conditions

| Condition | When it holds | What happens when it fails |
|---|---|---|
| Noise expressible as a power-law superposition | slope table reads off the type directly | with spurs (discrete spectral lines), ADEV shows $\tau$-periodic bumps and needs separate interpretation |
| Distinguishing white PM vs flicker PM | ADEV **cannot** (both $\tau^{-1}$) | switch to MDEV (modified Allan) to separate them |
| Data long enough, $\tau\ll$ total record length | estimate is reliable | as $\tau$ approaches the record length, few samples remain and confidence intervals blow up |
| Processes no lower-frequency than RW FM | ADEV converges | for processes below RW ($S_y\sim f^{-3}$ and steeper) ADEV also diverges; use the Hadamard variance |
| Measurement system itself clean enough | you measure the DUT | otherwise the left end (small $\tau$) is buried under the instrument's white PM |

## Which papers / formulas this maps to

- This page's ADEV definition, $\sigma_y^2=2\int S_y\sin^4(\pi f\tau)/(\pi f\tau)^2 df$, $S_y=(f^2/f_0^2)S_\phi$, and the slope table are all adopted verbatim from spec §11.2 "Allan variance / ADEV".
- **External literature (not among the five downloaded source PDFs; supplied from standard references)**:
  - **[E1] D. W. Allan, "Statistics of Atomic Frequency Standards," Proc. IEEE, vol. 54, no. 2, pp. 221–230, Feb. 1966.** (the original ADEV proposal)
  - **IEEE Std 1139** ("IEEE Standard Definitions of Physical Quantities for Fundamental Frequency and Time Metrology—Random Instabilities") and **NIST Special Publication 1065** (W. Riley, "Handbook of Frequency Stability Analysis," 2008) — the standard references for the power-law slope table and the overlapping-ADEV estimator.
  - The above are **IEEE Std 1139-2008** (prior edition 1139-1999) and **NIST SP 1065** (W. J. Riley, *Handbook of Frequency Stability Analysis*, 2008); volume/issue and edition details have been verified.
- Connection to this site's frequency-domain results: $S_\phi\sim1/f^2$ ([P1] Eq.(21) of [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)) ↔ white FM ↔ ADEV $\tau^{-1/2}$; $1/f^3$ ([P1] Eq.(23) of [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)) ↔ flicker FM ↔ ADEV $\tau^0$ floor.

## Key takeaways

- ADEV $\sigma_y(\tau)$ is the **time-domain counterpart** of phase noise: from the same $S_\phi(f)$, first convert $S_y=(f^2/f_0^2)S_\phi$, then substitute into $\sigma_y^2(\tau)=2\int_0^\infty S_y\,\sin^4(\pi f\tau)/(\pi f\tau)^2\,df$.
- The essence of the definition $\sigma_y^2(\tau)=\langle\tfrac12(\bar y_{k+1}-\bar y_k)^2\rangle$ is the **adjacent difference** (a first difference, i.e. a high-pass) blocking slow drift and the unknown grand mean.
- Five power-law slopes: white/flicker PM $\tau^{-1}$, **white FM $\tau^{-1/2}$**, flicker FM $\tau^{0}$ (floor), RW FM $\tau^{+1/2}$; the ADEV plot is a bathtub — drop, bottom out, climb — with the most stable point $\tau_{\text{opt}}$ at the bottom.
- Signature link: $1/f^2$ phase noise ↔ white FM ↔ ADEV slope $-1/2$.
- **Why ADEV**: the ordinary frequency variance **does not converge** for flicker/RW (it diverges with measurement duration); ADEV's differencing kernel goes like $f^2$ as $f\to0$, taming the low-frequency divergence and yielding a repeatable stability metric.
- Example 2 shows how $\mathcal{L}(1\text{MHz})=-100$ dBc/Hz (5 GHz) yields a white $S_y$ and $\sigma_y(1\text{ms})\approx6.3\times10^{-8}$.

## Further reading

- The same thing in the frequency domain: [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter)
- Where $1/f^2$ comes from (the frequency-domain origin of white FM): [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)
- $1/f^3$ ↔ flicker FM floor: [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)
- Why phase locking pins the long-term frequency: [serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)
- Stochastic processes and PSD fundamentals: [stochastic_noise_basics](/02_foundations/stochastic_noise_basics)
