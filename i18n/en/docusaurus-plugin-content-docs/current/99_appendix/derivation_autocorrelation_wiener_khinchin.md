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
- **The white-noise autocorrelation is a delta**: white noise at different instants is uncorrelated, $\langle i_n(t)i_n(t+\tau)\rangle=S_i\,\delta(\tau)$
  (where $S_i=\overline{i_n^2}/\Delta f$ is its (two-sided) PSD, a constant). Substituting:

$$
R_{\dot\phi}(t,\,t+\tau)=g(t)\,g(t+\tau)\,S_i\,\delta(\tau).
$$

- **Key observation (cyclostationary)**: this autocorrelation **explicitly contains the absolute time $t$** (through $g(t)g(t+\tau)$),
  and it repeats with period $T$ ($g$ is $T$-periodic) — exactly the defining feature of a **cyclostationary** process, **not** a stationary one.
  You cannot apply Wiener-Khinchin directly; you must first period-average over $t$.
- **Unit check**: $[g]=1/\text{C}$ ($\Gamma$ dimensionless $/q_{max}$), $[g^2 S_i\delta(\tau)]=
  \text{C}^{-2}\cdot(\text{A}^2/\text{Hz})\cdot(1/\text{s})$. With $\delta(\tau)$ carrying $1/\text{s}$ and $\text{Hz}^{-1}=\text{s}$,
  this reduces to $\text{C}^{-2}\text{A}^2=\text{s}^{-2}$, i.e. $[\dot\phi^2]=(\text{rad/s})^2$ ✓.

## Step B: period-average over absolute time → stationarize the cyclostationary process

The **time-averaged autocorrelation** of a cyclostationary process is defined by averaging over the absolute time $t$ over one period:

$$
\bar R_{\dot\phi}(\tau)=\frac{1}{T}\int_{0}^{T}R_{\dot\phi}(t,\,t+\tau)\,dt=\Big[\frac{1}{T}\int_{0}^{T}g(t)\,g(t+\tau)\,dt\Big]\,S_i\,\delta(\tau).
$$

The bracketed quantity is the **(deterministic, periodic) autocorrelation** of the weighting kernel $g$; denote it

$$
\bar g(\tau)\equiv\frac{1}{T}\int_{0}^{T}g(t)\,g(t+\tau)\,dt=\frac{1}{q_{max}^2}\cdot\frac{1}{T}\int_{0}^{T}\Gamma(\omega_0 t)\,\Gamma(\omega_0(t+\tau))\,dt.
$$

Because $\delta(\tau)$ is nonzero only at $\tau=0$, we **only need $\bar g(0)$**:

$$
\bar R_{\dot\phi}(\tau)=\bar g(0)\,S_i\,\delta(\tau),\qquad\bar g(0)=\frac{1}{q_{max}^2}\cdot\frac{1}{T}\int_{0}^{T}\Gamma^2(\omega_0 t)\,dt.
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

Writing the DC part as the $n=0$ term and arranging it into "half of $\sum_{n\ge0}c_n^2$" form (the same bookkeeping as [P1] Eq.(20):
the $c_0$ term carries coefficient $\tfrac14$, which equals $\tfrac12\cdot\tfrac12$ — i.e. $c_0^2$ is also folded into the $\tfrac12\sum$ with the
DC half-weight restored), we get:

$$
\frac{1}{2\pi}\int_{0}^{2\pi}\Gamma^2(x)\,dx=\Gamma_{rms}^2,\qquad\text{where}\quad\Gamma_{rms}^2\equiv\frac{1}{2\pi}\int_0^{2\pi}\Gamma^2(x)\,dx.
$$

This is precisely the **definition** of $\Gamma_{rms}$. Now compare with the Parseval relation of [P1] Eq.(20) (note it uses $\tfrac1\pi$ rather than $\tfrac1{2\pi}$):

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

Now $\bar R_{\dot\phi}(\tau)=\dfrac{\Gamma_{rms}^2}{q_{max}^2}S_i\,\delta(\tau)$ is a stationary autocorrelation **depending only on $\tau$**,
so we may safely apply **Wiener-Khinchin** (Fourier transform of the autocorrelation $=$ PSD):

$$
S_{\dot\phi}(\Delta\omega)=\int_{-\infty}^{\infty}\bar R_{\dot\phi}(\tau)\,e^{-j\Delta\omega\tau}\,d\tau=\frac{\Gamma_{rms}^2}{q_{max}^2}\,S_i\int_{-\infty}^{\infty}\delta(\tau)e^{-j\Delta\omega\tau}d\tau=\frac{\Gamma_{rms}^2}{q_{max}^2}\,S_i.
$$

The Fourier transform of $\delta$ is the constant $1$ — so **the spectrum of $\dot\phi$ (the instantaneous frequency perturbation) is white**, with strength
$\Gamma_{rms}^2 S_i/q_{max}^2$. Final step: phase is the integral of frequency, and **integration in the frequency domain is division by $j\Delta\omega$**,
so the power spectrum divides by $\Delta\omega^2$:

$$
S_\phi(\Delta\omega)=\frac{S_{\dot\phi}(\Delta\omega)}{\Delta\omega^2}=\frac{\Gamma_{rms}^2}{q_{max}^2}\cdot\frac{S_i}{\Delta\omega^2}\qquad[\text{rad}^2/\text{Hz}].
$$

This is **verbatim identical** to [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)'s "clean time-domain version" (the one in the factor-of-2 note), $S_\phi=\Gamma_{rms}^2S_i/(q_{max}^2(2\pi f)^2)$
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
| factor-of-2 | SSB bookkeeping ($/4$) | clean time-domain ($/2$); same factor-2 gap as noted |

> **Summary**: the rigorous version wields three tools — "cyclostationary autocorrelation → period average → Wiener-Khinchin" — turning both $\Gamma_{rms}$
> and $1/f^2$ into **mechanical inevitabilities**. $\sum c_n^2=2\Gamma_{rms}^2$ is no coincidence, but the Parseval incarnation of the
> ISF's mean square. This autocorrelation machinery is also precisely the entry point of the next page, [lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth):
> there, "$\dot\phi$ white ⇒ $\phi$ is a random walk" is pushed to its conclusion, yielding the **carrier autocorrelation
> $R_x(\tau)=\tfrac12\cos(\omega_0\tau)e^{-D|\tau|}$**, and Wiener-Khinchin then produces the **Lorentzian** —
> resolving the spurious divergence of $1/f^2$ as $\Delta\omega\to0$. The $S_\phi=\Gamma_{rms}^2S_i/(q_{max}^2\Delta\omega^2)$ computed on this page
> is exactly the source of $D=\Gamma_{rms}^2S_i/(4q_{max}^2)$ there (this site's single-sided bookkeeping is $S_\phi=4D/\Delta\omega^2$, two-sided
> $2D/\Delta\omega^2$; corrected in v5, reconciliation in [diffusion_dictionary](/03_isf_core_theory/diffusion_dictionary)).

## Applicability and failure conditions

| Condition | When it holds | What happens when it fails |
|---|---|---|
| $i_n(t)$ is (approximately) white, $\langle i_n(t)i_n(t+\tau)\rangle=S_i\delta(\tau)$ | Step A's delta autocorrelation holds, so later steps can take only $\bar g(0)$ | If the noise is colored (e.g. flicker), the autocorrelation is not a delta; Step B cannot look only at $\tau=0$ and needs separate treatment (see [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)) |
| $g(t)=\Gamma(\omega_0t)/q_{max}$ is a deterministic function with period $T$ (cyclostationary) | Step B's period average "stationarizes" the process so Wiener-Khinchin applies | A non-periodic or randomly modulated weight (e.g. an oscillator with frequency dithering) needs a more general time-varying spectral analysis; this page's result does not directly apply |
| Small perturbation, phase linear in the noise ([P1] Eq.(11) holds) | The linear relation $\dot\phi=g(t)i_n(t)$ holds | Large injection perturbs the ISF itself, breaking linear superposition |
| Only the stationarized autocorrelation of $\dot\phi$ matters (not the $\tau\neq0$ details) | Step D only needs $\bar g(0)$; $S_{\dot\phi}$ is white | For the precise near-carrier ($\Delta\omega\to0$) lineshape, the random-walk statistics of the phase itself must be kept — see [lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth) |

## Corresponding papers and equations

- Starting point: the LTV phase integral [P1] Eq.(11), p.182; the ISF Fourier series [P1] Eq.(12), p.183.
- Parseval bookkeeping compared against: [P1] Eq.(20), p.185 (Step C on this page re-derives the same $2\Gamma_{rms}^2$, but via the autocorrelation route rather than the single-tone summation).
- The final result is equivalent to the heuristic version's [P1] Eq.(19)→(21) (p.185); see [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise).
- The Wiener-Khinchin theorem itself is a standard signals-and-systems result, not from the 5 PDFs; this page only uses it as a tool and does not change [P1]'s physical conclusions.

## Key takeaways

- The heuristic version ([P1]'s original route) hand-computes sideband power by treating white noise as countless independent tones and summing; the rigorous version
  instead follows "LTV autocorrelation → cyclostationary period average → Wiener-Khinchin", deriving the same result **mechanically**.
- An oscillator's output is **cyclostationary** (its statistics repeat with period $T$ as a function of absolute time $t$), not strictly stationary;
  you must period-average over $t$ to "stationarize" it before applying Wiener-Khinchin.
- $\sum c_n^2=2\Gamma_{rms}^2$ is **not** a Parseval relation plugged in externally — it is the natural result of the period-average integral
  $\tfrac1{2\pi}\int_0^{2\pi}\Gamma^2(x)dx$.
- The result is word-for-word identical to the heuristic version: $S_\phi(\Delta\omega)=\dfrac{\Gamma_{rms}^2}{q_{max}^2}\cdot\dfrac{S_i}{\Delta\omega^2}$,
  with $1/\Delta\omega^2$ coming entirely from the one integration $\dot\phi\to\phi$.
- This page is the entry point of [lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth): there the same autocorrelation machinery is applied
  to the phase itself (rather than $\dot\phi$), resolving the spurious divergence of $1/f^2$ at the carrier.

## Further reading

- The full heuristic version (including canonical Example B and the factor-of-2 note): [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)
- Full discussion of $\Gamma_{rms}$ and Parseval: [rms_isf](/03_isf_core_theory/rms_isf)
- Near-carrier Lorentzian, linewidth $D/\pi$: [lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth)
- Reconciling the diffusion constant $D$ across pages' bookkeeping conventions: [diffusion_dictionary](/03_isf_core_theory/diffusion_dictionary)
- Close-in $1/f^3$ upconversion: [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)
