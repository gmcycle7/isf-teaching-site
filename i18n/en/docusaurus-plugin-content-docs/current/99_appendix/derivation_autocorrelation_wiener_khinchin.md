---
title: Autocorrelation to Wiener-Khinchin Rigorous Derivation
description: Using three steps — the two-time autocorrelation of the LTV phase derivative, period-averaging over absolute time, and Wiener-Khinchin — this page rigorously redoes the heuristic Eq.(19)→(20)→(21) derivation route from white_noise_to_phase_noise, letting Σcₙ²=2Γrms² fall out naturally from the period-averaged autocorrelation, and compares it item by item with the heuristic version.
---

# Autocorrelation to Wiener-Khinchin Rigorous Derivation

> **β**: This English translation is in beta — the Traditional-Chinese original is the authoritative version.

> Prerequisites: [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) (the heuristic route Eq.(19)→(20)→(21), canonical Example B) | Next: [lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth) (integrating the white $\dot\phi$ into a phase random walk, then Wiener-Khinchin to obtain the Lorentzian)

The route in [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) — "treat white noise as countless independent small tones, compute each tone's sideband, then sum" — is [P1]'s original path.
Its physical intuition is strong, but algebraically it is **heuristic**: the steps "white noise $=$ superposition of tones" and "factor-8 bookkeeping"
rely on hand-tallied power accounting. This page redoes the same result with the **rigorous machinery of signals and systems** —
write down the **time-averaged autocorrelation** of the LTV output phase directly, expand it with the ISF's Fourier
coefficients so that $\sum c_n^2=2\Gamma_{rms}^2$ **falls out of the autocorrelation by itself**, then take the spectrum with the **Wiener-Khinchin theorem**.
If you are comfortable with "LTI systems: $S_y=|H|^2S_x$", this page upgrades that to the "**LTV / cyclostationary**" version.

> **Why this page exists**: an oscillator is a **periodically time-varying** system; its output is not strictly
> stationary but **cyclostationary** (its statistics repeat with period $T$). For a cyclostationary
> process, the correct spectral analysis first averages over the **absolute time $t$** over one period, "stationarizing" it, and only then applies Wiener-Khinchin.
> This page walks that path honestly; at the end you will see that $\Gamma_{rms}$ is not "conjured up" — it is the **inevitable product**
> of the period average of the autocorrelation.

## Step A: write down the two-time autocorrelation of the phase

Starting from the phase integral of [P1] Eq.(11), define $g(\tau)\equiv\Gamma(\omega_0\tau)/q_{max}$ (folding the ISF and the
normalization into a single weighting kernel), so that $\phi(t)=\int_{-\infty}^{t}g(\tau)\,i_n(\tau)\,d\tau$.
To see the spectrum cleanly, however, we switch to the **time derivative of the phase** $\dot\phi$ (the instantaneous frequency perturbation), whose autocorrelation is more direct
(the phase itself is a non-stationary random walk, see [lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth);
it is $\dot\phi$ that is cyclostationary-stationary). By the fundamental theorem of calculus:

$$
\dot\phi(t)=g(t)\,i_n(t)=\frac{\Gamma(\omega_0 t)}{q_{max}}\,i_n(t).
$$

This is a **multiplicative LTV**: the input white noise $i_n(t)$ is modulated pointwise by a **deterministic periodic weight** $g(t)$. Compute its
**two-time autocorrelation**:

$$
R_{\dot\phi}(t,\,t+\tau)=\big\langle\dot\phi(t)\,\dot\phi(t+\tau)\big\rangle=g(t)\,g(t+\tau)\,\big\langle i_n(t)\,i_n(t+\tau)\big\rangle.
$$

- **Math used**: $g$ is a deterministic function (it can be pulled outside the expectation); only $i_n$ is random.
- **The white-noise autocorrelation is a delta, with coefficient $S_i/2$**: white noise at different instants is uncorrelated, so its autocorrelation is a $\delta$.
  On this site $S_i\equiv\overline{i_n^2}/\Delta f$ is the **single-sided PSD** — defined on $f\gt0$ only, so that
  $\int_0^{B}S_i\,df$ is the $\overline{i_n^2}$ inside a bandwidth $B$. The Wiener-Khinchin Fourier pair is written on
  $-\infty\lt f\lt\infty$, where the **two-sided flat level is $S_i/2$** (the same power spread over positive and negative frequencies),
  and the coefficient of $\delta(\tau)$ equals the two-sided level:

$$
\big\langle i_n(t)\,i_n(t+\tau)\big\rangle=\frac{S_i}{2}\,\delta(\tau).
$$

Check: for band-limited white noise of bandwidth $B$, $R(0)=\int_{-B}^{B}\tfrac{S_i}{2}df=S_iB=\overline{i_n^2}$ ✓.
This is **the same $\tfrac12$** as in the white-noise autocorrelation [P2] Appendix A prints on the line before Eq.(43) (p.802, with a $(1/2)$ factor);
see [p2_appendix_a_reconciliation](/99_appendix/p2_appendix_a_reconciliation) for the verbatim reconciliation.
The "Numerical verification" section near the end of this page measures this $\tfrac12$ directly. Substituting:

$$
R_{\dot\phi}(t,\,t+\tau)=g(t)\,g(t+\tau)\,\frac{S_i}{2}\,\delta(\tau).
$$

- **Key observation (cyclostationary)**: this autocorrelation **explicitly contains the absolute time $t$** (through $g(t)g(t+\tau)$),
  and it repeats with period $T$ ($g$ is $T$-periodic) — exactly the defining feature of a **cyclostationary** process, **not** a stationary one.
  You cannot apply Wiener-Khinchin directly; you must first period-average over $t$.
- **Unit check**: $[g]=1/\text{C}$ ($\Gamma$ dimensionless $/q_{max}$), $[g^2 (S_i/2)\delta(\tau)]=
  \text{C}^{-2}\cdot(\text{A}^2/\text{Hz})\cdot(1/\text{s})$. With $\delta(\tau)$ carrying $1/\text{s}$ and $\text{Hz}^{-1}=\text{s}$,
  this reduces to $\text{C}^{-2}\text{A}^2=\text{s}^{-2}$, i.e. $[\dot\phi^2]=(\text{rad/s})^2$ ✓ (the $\tfrac12$ is dimensionless and does not affect the units).

## Step B: period-average over absolute time → stationarize the cyclostationary process

The **time-averaged autocorrelation** of a cyclostationary process is defined by averaging over the absolute time $t$ over one period:

$$
\bar R_{\dot\phi}(\tau)=\frac{1}{T}\int_{0}^{T}R_{\dot\phi}(t,\,t+\tau)\,dt=\Big[\frac{1}{T}\int_{0}^{T}g(t)\,g(t+\tau)\,dt\Big]\,\frac{S_i}{2}\,\delta(\tau).
$$

The bracketed quantity is the **(deterministic, periodic) autocorrelation** of the weighting kernel $g$; denote it

$$
\bar g(\tau)\equiv\frac{1}{T}\int_{0}^{T}g(t)\,g(t+\tau)\,dt=\frac{1}{q_{max}^2}\cdot\frac{1}{T}\int_{0}^{T}\Gamma(\omega_0 t)\,\Gamma(\omega_0(t+\tau))\,dt.
$$

Because $\delta(\tau)$ is nonzero only at $\tau=0$, we **only need $\bar g(0)$**:

$$
\bar R_{\dot\phi}(\tau)=\bar g(0)\,\frac{S_i}{2}\,\delta(\tau),\qquad\bar g(0)=\frac{1}{q_{max}^2}\cdot\frac{1}{T}\int_{0}^{T}\Gamma^2(\omega_0 t)\,dt.
$$

- **Physics/math used**: averaging away the absolute time is the same as averaging the oscillator's sensitivity "at every phase within one period" —
  exactly the standard "equivalent stationarization" maneuver for cyclostationary systems.
- **$\Gamma_{rms}$ is about to emerge here**: $\dfrac{1}{T}\int_0^T\Gamma^2(\omega_0t)\,dt$ is precisely the **mean square** of the ISF.

## Step C: expand with the ISF Fourier coefficients → $\sum c_n^2=2\Gamma_{rms}^2$ falls out naturally

Substituting the Fourier series of $\Gamma$ ([P1] Eq.(12)) into that mean-square integral in $\bar g(0)$ produces $\sum c_n^2$ **all by itself**.
First convert the mean-square integral into an integral over the phase $x=\omega_0 t$ ($dt=dx/\omega_0$; one period $t:0\to T$ corresponds to $x:0\to2\pi$):

$$
\frac{1}{T}\int_{0}^{T}\Gamma^2(\omega_0 t)\,dt=\frac{1}{2\pi}\int_{0}^{2\pi}\Gamma^2(x)\,dx.
$$

Insert $\Gamma(x)=\dfrac{c_0}{2}+\sum_{n\ge1}c_n\cos(nx+\theta_n)$ and square. Using the **orthogonality** of the trigonometric functions
(cross-harmonic integrals vanish; same-harmonic $\int_0^{2\pi}\cos^2=\pi$; the DC term gives $\int_0^{2\pi}dx=2\pi$):

$$
\frac{1}{2\pi}\int_{0}^{2\pi}\Gamma^2(x)\,dx=\Big(\frac{c_0}{2}\Big)^2+\sum_{n=1}^{\infty}\frac{c_n^2}{2}=\frac{c_0^2}{4}+\frac12\sum_{n=1}^{\infty}c_n^2.
$$

The left-hand side is precisely the **definition** of $\Gamma_{rms}^2$ (the mean square of the ISF). Factoring $\tfrac12$ out of the right-hand side, the DC coefficient
$\tfrac14=\tfrac12\cdot\tfrac12$ becomes an explicit identity:

$$
\Gamma_{rms}^2\equiv\frac{1}{2\pi}\int_{0}^{2\pi}\Gamma^2(x)\,dx=\frac{c_0^2}{4}+\frac12\sum_{n=1}^{\infty}c_n^2=\frac12\Big[\frac{c_0^2}{2}+\sum_{n=1}^{\infty}c_n^2\Big]
\quad\Longrightarrow\quad
2\,\Gamma_{rms}^2=\frac{c_0^2}{2}+\sum_{n=1}^{\infty}c_n^2.
$$

In words: **the DC term enters as $c_0^2/2$ (half weight), while each $n\ge1$ term enters as the full $c_n^2$**. The half weight has a single origin —
the DC term of the series is written $\tfrac{c_0}{2}$ rather than $c_0$, so its mean square is $(c_0/2)^2=c_0^2/4$, whereas each harmonic's mean square is
$c_n^2/2$; after factoring out $\tfrac12$ from both, the DC term leaves $c_0^2/2$ and each harmonic leaves $c_n^2$. [P1] Eq.(20) abbreviates this right-hand sum as
$\sum_{n=0}^{\infty}c_n^2$ (note it uses $\tfrac1\pi$ rather than $\tfrac1{2\pi}$):

$$
\sum_{n=0}^{\infty}c_n^2=\frac{1}{\pi}\int_0^{2\pi}\Gamma^2(x)\,dx=2\cdot\frac{1}{2\pi}\int_0^{2\pi}\Gamma^2(x)\,dx=\boxed{\,2\,\Gamma_{rms}^2\,}.
$$

> **Note (DC half-weight)**: in this $\sum_{n=0}^{\infty}c_n^2$ the DC term enters as $c_0^2/2$ (half weight);
> if you mistakenly use the full weight $c_0^2$, the sum exceeds $2\Gamma_{rms}^2$ by $c_0^2/2$. This is exactly Parseval's bookkeeping for a DC term written as $\tfrac{c_0}{2}$
> (the first term of the $\Gamma$ series is written $\tfrac{c_0}{2}$; squared, it gives $\tfrac{c_0^2}{4}=\tfrac12\cdot\tfrac{c_0^2}{2}$),
> see [rms_isf](/03_isf_core_theory/rms_isf) for details.

**And so $\sum c_n^2=2\Gamma_{rms}^2$ drops naturally out of the period average of the autocorrelation** — no hand-tallied
factor-8 bookkeeping of [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)'s Step 3b required. The only difference is the factor of 2 from the "$\tfrac1\pi$ vs $\tfrac1{2\pi}$" Parseval convention, fully consistent with
[rms_isf](/03_isf_core_theory/rms_isf). Hence

$$
\bar g(0)=\frac{1}{q_{max}^2}\cdot\Gamma_{rms}^2=\frac{\Gamma_{rms}^2}{q_{max}^2}.
$$

- **Physical meaning**: the strength of the time-averaged autocorrelation of $\dot\phi$ (the weight at $\tau=0$) is **proportional to $\Gamma_{rms}^2/q_{max}^2$** —
  the effective gain with which the oscillator "stirs" white noise into phase is the ISF's mean square divided by $q_{max}^2$. All the details of the individual $c_n$ are
  collected by Parseval into a single $\Gamma_{rms}$.

## Step D: Wiener-Khinchin → phase spectrum $S_\phi\propto1/\Delta\omega^2$

Inserting $\bar g(0)=\Gamma_{rms}^2/q_{max}^2$ from Step C, $\bar R_{\dot\phi}(\tau)=\dfrac{\Gamma_{rms}^2}{q_{max}^2}\cdot\dfrac{S_i}{2}\,\delta(\tau)$ is now a stationary autocorrelation **depending only on $\tau$**,
so we may safely apply **Wiener-Khinchin** (Fourier transform of the autocorrelation $=$ PSD).
**Convention flag**: this transform integrates over $\tau\in(-\infty,\infty)$ and yields a
**two-sided PSD** defined on **both positive and negative frequencies**, marked with the superscript $DS$:

$$
S_{\dot\phi}^{DS}(\Delta\omega)=\int_{-\infty}^{\infty}\bar R_{\dot\phi}(\tau)\,e^{-j\Delta\omega\tau}\,d\tau=\frac{\Gamma_{rms}^2}{q_{max}^2}\cdot\frac{S_i}{2}\int_{-\infty}^{\infty}\delta(\tau)e^{-j\Delta\omega\tau}d\tau=\frac{\Gamma_{rms}^2\,S_i}{2\,q_{max}^2},\qquad-\infty\lt\Delta\omega\lt\infty.
$$

The Fourier transform of $\delta$ is the constant $1$ — so **the spectrum of $\dot\phi$ (the instantaneous frequency perturbation) is white**, with two-sided level
$\Gamma_{rms}^2 S_i/(2q_{max}^2)$. This number is the **phase**-variance growth rate of [P2] Eq.(11), p.793
($\sigma_{\Delta\phi}^2=\Gamma_{rms}^2S_i\,\Delta T/(2q_{max}^2)$; this site writes it $\kappa^2$, in $\text{rad}^2/\text{s}$.
Note that [P2]'s own $\kappa$ (Eq.(12)) is the **timing**-jitter constant $\sigma_{\Delta T}=\kappa\sqrt{\Delta T}$; the two differ by a factor $\omega_0$,
see [diffusion_dictionary](/03_isf_core_theory/diffusion_dictionary) for the conversion), and also equals $2D$ ($D=\Gamma_{rms}^2S_i/(4q_{max}^2)$);
the canonical value is $0.25\times10^{-24}/(2\times10^{-24})=0.125\ \text{rad}^2/\text{s}$.
Units: $\text{C}^{-2}\cdot\text{A}^2/\text{Hz}=\text{s}^{-2}\cdot\text{s}=\text{rad}^2/\text{s}$,
i.e. $(\text{rad/s})^2/\text{Hz}$ ✓ (the density is per Hz of $f=\Delta\omega/2\pi$; $\Delta\omega$ merely labels the abscissa).

Next: phase is the integral of frequency, and **integration in the frequency domain is division by $j\Delta\omega$**, so the power spectrum divides by $\Delta\omega^2$:

$$
S_\phi^{DS}(\Delta\omega)=\frac{S_{\dot\phi}^{DS}(\Delta\omega)}{\Delta\omega^2}=\frac{\Gamma_{rms}^2}{q_{max}^2}\cdot\frac{S_i}{2\,\Delta\omega^2}\qquad[\text{rad}^2/\text{Hz}],\quad-\infty\lt\Delta\omega\lt\infty.
$$

**Last step: two-sided → single-sided.** On this site (and on measurement instruments) $S_\phi$ is always the **single-sided** spectrum: only $\Delta\omega\gt0$ is shown,
and the power of the negative-frequency half is folded onto the positive side. $S_\phi^{DS}$ is even, so folding is a multiplication by 2:

$$
S_\phi(\Delta\omega)=2\,S_\phi^{DS}(\Delta\omega)=\frac{\Gamma_{rms}^2}{q_{max}^2}\cdot\frac{S_i}{\Delta\omega^2}\qquad[\text{rad}^2/\text{Hz}],\quad\Delta\omega\gt0.
$$

**Accounting for the two 2s**: the $\tfrac12$ of Step A (single-sided $S_i$ → two-sided level $S_i/2$) and the $2$ here (two-sided $S_\phi^{DS}$ →
single-sided $S_\phi$) go **one in, one out, and cancel exactly** — the "single-sided input PSD → single-sided output PSD" conversion gain carries no 2 at all;
the $\tfrac12$ is visible only in the intermediate autocorrelation and two-sided spectra. If you mislabel $S_i$ as two-sided (writing $R=S_i\delta$) and also forget
the final folding, the two errors cancel and give the same answer, but every intermediate line is off by 2; commit only one of them and
$S_\phi$ is off by a factor of 2 ($3$ dB).

The single-sided result is therefore **verbatim identical** to [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)'s "clean time-domain version" (the one in the factor-of-2 note), $S_\phi=\Gamma_{rms}^2S_i/(q_{max}^2(2\pi f)^2)$
(with $\Delta\omega=2\pi f$).

- **The rigorous origin of $1/f^2$**: this $1/\Delta\omega^2$ comes **entirely from "the one integration $\dot\phi\to\phi$"**
  (the $1/(j\Delta\omega)$ filter) — word for word the physical intuition at the top of [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise), only now it is proven rigorously via Wiener-Khinchin
  rather than assembled from hand-computed sidebands.
- **The role of the white spectrum**: $\dot\phi$ is white; only $\phi$ is $1/f^2$ — which also explains why the phase is a random walk
  (the integral of white frequency perturbations $=$ a Wiener process), exactly the starting point of the Lorentzian on the next page.

## Rigorous vs heuristic: side-by-side table

| Item | Heuristic ([white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) Step 3, [P1]'s original route) | Rigorous (this page, cyclostationary autocorrelation) |
|---|---|---|
| Starting point | white noise $=$ countless independent tones | two-time autocorrelation of $\dot\phi=g(t)i_n(t)$ |
| Stationarization | implicit in the "sum over $n$" | explicit period average over absolute time $t$ |
| Origin of $\Gamma_{rms}$ | Parseval substituted by hand (Eq.20) | generated naturally by the period-average integral $\tfrac1{2\pi}\int\Gamma^2$ |
| $\sum c_n^2=2\Gamma_{rms}^2$ | applied externally | falls out of the autocorrelation $\bar g(0)$ |
| Origin of $1/\Delta\omega^2$ | the $1/\Delta\omega^2$ of single-tone sidebands | the $1/(j\Delta\omega)$ of the $\dot\phi\to\phi$ integration |
| Obtaining the spectrum | accumulating sideband powers | Wiener-Khinchin (FT of the autocorrelation) |
| factor-of-2 | SSB bookkeeping (the $/4$ of $\mathcal{L}$) | single-sided $S_i$ → $\tfrac{S_i}{2}\delta$ → two-sided $S_\phi^{DS}$ → $\times2$ → single-sided $S_\phi$; $\mathcal{L}=S_\phi/2$ gives $/2$, the same factor-2 gap from $/4$ as noted |

> **Summary**: the rigorous version wields three tools — "cyclostationary autocorrelation → period average → Wiener-Khinchin" — turning both $\Gamma_{rms}$
> and $1/f^2$ into **mechanical inevitabilities**. $\sum c_n^2=2\Gamma_{rms}^2$ is no coincidence, but the Parseval incarnation of the
> ISF's mean square. This autocorrelation machinery is also precisely the entry point of the next page, [lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth):
> there, "$\dot\phi$ white ⇒ $\phi$ is a random walk" is pushed to its conclusion, yielding the **carrier autocorrelation
> $R_x(\tau)=\tfrac12\cos(\omega_0\tau)e^{-D|\tau|}$**, and Wiener-Khinchin then produces the **Lorentzian** —
> resolving the spurious divergence of $1/f^2$ as $\Delta\omega\to0$. The **single-sided** $S_\phi=\Gamma_{rms}^2S_i/(q_{max}^2\Delta\omega^2)$ computed on this page
> is exactly the source of $D=\Gamma_{rms}^2S_i/(4q_{max}^2)$ there (this site's single-sided bookkeeping is $S_\phi=4D/\Delta\omega^2$, two-sided
> $2D/\Delta\omega^2$, i.e. the $S_\phi^{DS}$ of Step D on this page; reconciliation in [diffusion_dictionary](/03_isf_core_theory/diffusion_dictionary)).

## Numerical verification: measuring that $\tfrac12$ directly

The block below draws no figure; it does four things. Generate a record of band-limited white noise with **single-sided PSD $=S_i$** (sample rate $f_s$, bandwidth $f_s/2$), then
(1) confirm with Welch that its single-sided PSD really is $S_i$; (2) compute the autocorrelation numerically and take its area over $\tau$,
$\int R(\tau)d\tau\approx\sum_kR[k]\,\Delta t$ — the coefficient of the $\delta$ is this area, and should be $S_i/2$;
(3) multiply by the ISF weight $g(t)$ to get $\dot\phi$, whose autocorrelation area is the two-sided $S_{\dot\phi}^{DS}$;
(4) the Welch **single-sided** PSD of the same $\dot\phi$ record should be twice the two-sided level. Canonical Example B and the Step C identity are checked at the end.

```python
import numpy as np
from simulations.common.isf_utils import gamma_lc_ideal
from simulations.common.noise_utils import white_noise, estimate_psd

F0 = 5e9
W0 = 2 * np.pi * F0
QMAX, SI, GRMS = 1e-12, 1e-24, 0.5        # canonical parameters
FS = 64 * F0                              # sample rate: 64 points per period (noise bandwidth fs/2 = 160 GHz)
DT = 1 / FS
N = 2**20                                 # = 16384 whole periods
rng = np.random.default_rng(12)

i_n = white_noise(N, SI, FS, rng)         # band-limited white noise with single-sided PSD = S_i

# (1) Welch single-sided PSD: confirm the input really is "single-sided S_i"
f, pxx = estimate_psd(i_n, FS, nperseg=4096)
print(f"{np.mean(pxx[1:-1])/SI:.2f}")     # -> 1.00 (single-sided PSD / S_i)

# (2) autocorrelation area ∫R(τ)dτ ≈ Σ_k R[k]·dt: the delta coefficient should be S_i/2
K = 20
def acorr_area(x):
    r = [np.mean(x[:N - k] * x[k:]) for k in range(K + 1)]
    return (r[0] + 2 * sum(r[1:])) * DT

print(f"{acorr_area(i_n)/SI:.2f}")        # -> 0.50 (autocorrelation area / S_i: this is the 1/2)

# (3) ISF-weighted φ̇ = g(t) i_n(t): autocorrelation area = two-sided S_φ̇ level
t = np.arange(N) * DT
g = np.sqrt(2.0) * GRMS * gamma_lc_ideal(W0 * t) / QMAX
phidot = g * i_n
s_ds = acorr_area(phidot)
print(f"{s_ds:.3f}")                      # -> 0.126 rad^2/s (two-sided S_φ̇, theory κ² = 0.125)
print(f"{s_ds/(GRMS**2*SI/QMAX**2):.2f}") # -> 0.50 (two-sided level / [Γrms² S_i/q_max²])

# (4) Welch single-sided PSD of the same φ̇ record (flat low-frequency region)
f, pxx = estimate_psd(phidot, FS, nperseg=4096)
s_ss = np.mean(pxx[(f > 0) & (f < 0.4 * F0)])
print(f"{s_ss:.3f}")                      # -> 0.254 rad^2/s (single-sided S_φ̇, theory 0.25)
print(f"{s_ss/s_ds:.2f}")                 # -> 2.02 (single-sided / two-sided, theory 2)

# (5) canonical Example B: single-sided S_φ(1 MHz) and the two L families
dw = 2 * np.pi * 1e6
s_phi = GRMS**2 * SI / (QMAX**2 * dw**2)
print(f"{s_phi:.3e}")                     # -> 6.333e-15 rad^2/Hz (single-sided S_φ @ 1 MHz)
print(f"{10*np.log10(s_phi/2):.1f}")      # -> -145.0 dBc/Hz (L = S_φ/2, the "/2" family)
print(f"{10*np.log10(s_phi/4):.1f}")      # -> -148.0 dBc/Hz (the "/4" family of [P1] Eq.(21))

# (6) the DC half-weight identity of Step C: Γ = c0/2 + c1 cos x
x = np.linspace(0, 2 * np.pi, 100000, endpoint=False)
c0, c1 = 0.6, 1.0
gam = c0 / 2 + c1 * np.cos(x)
print(f"{np.mean(gam**2):.3f}")           # -> 0.590 (direct numerical mean square Γrms²)
print(f"{0.5*(c0**2/2 + c1**2):.3f}")     # -> 0.590 ((1/2)[c0²/2 + c1²]: DC at half weight, matches)
print(f"{0.5*(c0**2 + c1**2):.3f}")       # -> 0.680 ((1/2)[c0² + c1²]: DC wrongly at full weight, too large by c0²/4 = 0.09)
```

- **How to read it**: (1) prints 1.00 and (2) prints 0.50 — for one and the same record the single-sided PSD is $S_i$ and the $\delta$ coefficient of the autocorrelation is $S_i/2$;
  that is the $\tfrac12$ of Step A. The 0.126 of (3) matches $\kappa^2=0.125\ \text{rad}^2/\text{s}$ (two-sided);
  the 0.254 of (4) matches $0.25$ (single-sided), and the ratio 2.02 matches 2. The $-145.0$ / $-148.0$ dBc/Hz of (5) are this site's canonical
  "$/2$" and "$/4$" families — the bookkeeping on this page changes no final number.
- **Honest limitations**: these are finite-record ($2^{20}$ samples) statistical estimates, so (3) and (4) carry roughly 1–2% sampling error (0.126, 0.254, 2.02 rather than
  0.125, 0.250, 2.00). The discrete-time "$\delta$" is one bin of width $\Delta t$, so the noise is white only up to $f_s/2=160$ GHz (band-limited);
  ideal continuous-time white noise is the $f_s\to\infty$ limit. $\dot\phi$ is cyclostationary, and Welch's averaging over absolute time
  plays exactly the role of Step B's period average; only the flat region $f\lt0.4f_0$ is used here. This check validates the **bookkeeping** (the single-/two-sided 2),
  not a transistor-level oscillator.

## Applicability and failure conditions

| Condition | When it holds | What happens when it fails |
|---|---|---|
| $i_n(t)$ is (approximately) white, $\langle i_n(t)i_n(t+\tau)\rangle=\tfrac{S_i}{2}\delta(\tau)$ | Step A's delta autocorrelation holds, so later steps can take only $\bar g(0)$ | If the noise is colored (e.g. flicker), the autocorrelation is not a delta; Step B cannot look only at $\tau=0$ and needs separate treatment (see [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)) |
| $g(t)=\Gamma(\omega_0t)/q_{max}$ is a deterministic function with period $T$ (cyclostationary) | Step B's period average "stationarizes" the process so Wiener-Khinchin applies | A non-periodic or randomly modulated weight (e.g. an oscillator with frequency dithering) needs a more general time-varying spectral analysis; this page's result does not directly apply |
| Small perturbation, phase linear in the noise ([P1] Eq.(11) holds) | The linear relation $\dot\phi=g(t)i_n(t)$ holds | Large injection perturbs the ISF itself, breaking linear superposition |
| Only the stationarized autocorrelation of $\dot\phi$ matters (not the $\tau\neq0$ details) | Step D only needs $\bar g(0)$; $S_{\dot\phi}$ is white | For the precise near-carrier ($\Delta\omega\to0$) lineshape, the random-walk statistics of the phase itself must be kept — see [lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth) |

## Corresponding papers and equations

- Starting point: the LTV phase integral [P1] Eq.(11), p.182; the ISF Fourier series [P1] Eq.(12), p.183.
- Parseval bookkeeping compared against: [P1] Eq.(20), p.185 (Step C on this page re-derives the same $2\Gamma_{rms}^2$, but via the autocorrelation route rather than the single-tone summation).
- The final result is equivalent to the heuristic version's [P1] Eq.(19)→(21) (p.185); see [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise).
- The $\tfrac12$ of the white-noise autocorrelation in Step A: [P2] Appendix A, the line before Eq.(43) and Eq.(43)–(44), p.802 (checked against the rendered PDF page);
  the two-sided level $\Gamma_{rms}^2S_i/(2q_{max}^2)$ (written $\kappa^2$ on this site) corresponds to the phase-variance growth rate of [P2] Eq.(11), p.793. Verbatim reconciliation in
  [p2_appendix_a_reconciliation](/99_appendix/p2_appendix_a_reconciliation).
- The Wiener-Khinchin theorem itself is a standard signals-and-systems result, not from the 5 PDFs; this page only uses it as a tool and does not change [P1]'s physical conclusions.

## Key takeaways

- The heuristic version ([P1]'s original route) hand-computes sideband power by treating white noise as countless independent tones and summing; the rigorous version
  instead follows "LTV autocorrelation → cyclostationary period average → Wiener-Khinchin", deriving the same result **mechanically**.
- An oscillator's output is **cyclostationary** (its statistics repeat with period $T$ as a function of absolute time $t$), not strictly stationary;
  you must period-average over $t$ to "stationarize" it before applying Wiener-Khinchin.
- $\sum c_n^2=2\Gamma_{rms}^2$ is **not** a Parseval relation plugged in externally — it is the natural result of the period-average integral
  $\tfrac1{2\pi}\int_0^{2\pi}\Gamma^2(x)dx$.
- **Single-/two-sided bookkeeping**: $S_i$ is a single-sided PSD and the white-noise autocorrelation is $\tfrac{S_i}{2}\delta(\tau)$; Wiener-Khinchin delivers the
  **two-sided** $S_\phi^{DS}=\Gamma_{rms}^2S_i/(2q_{max}^2\Delta\omega^2)$, and the single-sided $S_\phi=2S_\phi^{DS}$.
- The single-sided result is word-for-word identical to the heuristic version: $S_\phi(\Delta\omega)=\dfrac{\Gamma_{rms}^2}{q_{max}^2}\cdot\dfrac{S_i}{\Delta\omega^2}$,
  with $1/\Delta\omega^2$ coming entirely from the one integration $\dot\phi\to\phi$.
- This page is the entry point of [lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth): there the same autocorrelation machinery is applied
  to the phase itself (rather than $\dot\phi$), resolving the spurious divergence of $1/f^2$ at the carrier.

## Further reading

- The full heuristic version (including canonical Example B and the factor-of-2 note): [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)
- Full discussion of $\Gamma_{rms}$ and Parseval: [rms_isf](/03_isf_core_theory/rms_isf)
- Where the same $\tfrac12$ appears in [P2] Appendix A, with factor-by-factor reconciliation: [p2_appendix_a_reconciliation](/99_appendix/p2_appendix_a_reconciliation)
- Near-carrier Lorentzian, linewidth $D/\pi$: [lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth)
- Reconciling the diffusion constant $D$ across pages' bookkeeping conventions: [diffusion_dictionary](/03_isf_core_theory/diffusion_dictionary)
- Close-in $1/f^3$ upconversion: [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)
