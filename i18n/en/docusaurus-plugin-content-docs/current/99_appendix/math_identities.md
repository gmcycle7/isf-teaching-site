---
title: Math Toolbox — Math Identities
description: The math tools this site's derivations use repeatedly — Fourier series/Parseval, LTV convolution, Wiener–Khinchin, dB conversion, integrator response, small-angle PM, trigonometric identities, random-walk variance — each with a short proof and the pages that use it.
---

> **β**: This English translation is in beta — the Traditional-Chinese original is the authoritative version.

# Math Toolbox — Math Identities

> **See also**: [notation](/00_overview/notation) (authoritative symbols and units), [glossary](/99_appendix/glossary) (Chinese–English term intuitions), [convolution_derivation](/03_isf_core_theory/convolution_derivation) (LTV convolution uses the tools on this page), [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) (application site for Parseval/integrator response)

ISF theory looks very "circuits," but its skeleton is really a handful of standard math tools combined repeatedly.
This page collects them, gives each a **short proof or citation**, and marks **which page on the site uses it**.
Come back here when a derivation stalls — it beats memorizing formulas by rote.

> **How to use this page**: each section first gives "one line on what it says," then "why it holds" (proof or citation),
> and finally "where on the site it's used." Every quantity carries units — doing a dimension check is always the fastest way to catch mistakes.

---

## 1. Fourier series and Parseval (harmonic decomposition of the ISF)

**One line**: any $2\pi$-periodic real function can be split into DC plus a set of harmonics; its "total energy" equals the sum of each harmonic's energy.
This is the mathematical basis for splitting the ISF $\Gamma(\omega_0\tau)$ into $c_0,c_1,c_2,\dots$.

The ISF is a dimensionless, $2\pi$-periodic function, written as a cosine series ([P1] Eq.(12), p.183):

$$
\Gamma(\omega_0\tau)=\frac{c_0}{2}+\sum_{n=1}^{\infty}c_n\cos(n\omega_0\tau+\theta_n)
$$

Write the argument as $x=\omega_0\tau$. **Parseval's relation** ([P1] Eq.(20), p.185):

$$
\sum_{n=0}^{\infty}c_n^2=\frac{1}{\pi}\int_0^{2\pi}|\Gamma(x)|^2\,dx=2\,\Gamma_{rms}^2
$$

**Why it holds (short proof)**: square the series and integrate from $0$ to $2\pi$. Cosines of different harmonics are mutually orthogonal,

$$
\int_0^{2\pi}\cos(mx+\theta_m)\cos(nx+\theta_n)\,dx=\pi\,\delta_{mn}\quad(m,n\ge1),
$$

so the cross terms all vanish, leaving only the square terms: each $c_n\cos(\cdot)$ term contributes $c_n^2\cdot\pi$, and the DC term
$\left(\frac{c_0}{2}\right)^2$ contributes $\left(\frac{c_0}{2}\right)^2\cdot 2\pi=\frac{c_0^2}{2}\pi$.
Dividing both sides by $\pi$ gives $\sum_{n=1}^{\infty}c_n^2+\frac{c_0^2}{2}$. Hajimiri–Lee write the DC term as
$\frac{c_0^2}{2}$ (note the $n=0$ term is counted as only half in the sum), and rearranging gives exactly the form above.

**rms definition consistency check**: $\Gamma_{rms}^2=\frac{1}{2\pi}\int_0^{2\pi}|\Gamma(x)|^2\,dx$
(rms is just "root mean square": square first, average, then take the root). Substituting into the right-hand side of Parseval:
$\frac{1}{\pi}\int=2\cdot\frac{1}{2\pi}\int=2\Gamma_{rms}^2$ ✓.

**Numerical feel**: for the ideal LC, $\Gamma(\theta)=-\sin\theta$, only $c_1=1$ (all others 0).
$\Gamma_{rms}^2=\frac{1}{2\pi}\int_0^{2\pi}\sin^2\theta\,d\theta=\frac12$, so $\Gamma_{rms}=1/\sqrt2\approx0.707$;
the right-hand side of Parseval, $2\times\frac12=1=c_1^2$ ✓.

**Used on this site**: [fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf) (splitting the ISF into harmonics,
explaining how noise near $n\omega_0$ downconverts), [rms_isf](/03_isf_core_theory/rms_isf),
[lab_05](/04_simulation_labs/lab_05_isf_fourier_coefficients) (numerically verifying $\sum c_n^2=2\Gamma_{rms}^2$).

---

## 2. Convolution and the LTI vs LTV distinction (why the oscillator is "time-variant")

**One line**: an LTI (linear time-invariant) system's impulse response depends only on "how long ago" $t-\tau$; an LTV (linear time-variant) system
also depends on "at what instant it's kicked" $\tau$. The oscillator's response to noise is LTV — this is the core of ISF theory.

LTI superposition is standard convolution:

$$
y(t)=\int_{-\infty}^{\infty}h(t-\tau)\,x(\tau)\,d\tau .
$$

- **Core feature**: $h$ depends only on the difference $t-\tau$ (time-invariant). Delay the input, and the output is delayed unchanged.

The oscillator's excess-phase impulse response, however, is ([P1] Eq.(10), p.182):

$$
h_\phi(t,\tau)=\frac{\Gamma(\omega_0\tau)}{q_{max}}\,u(t-\tau).
$$

It **simultaneously** depends on $\tau$ (via $\Gamma(\omega_0\tau)$ — at what phase of the waveform it's kicked) and on $t-\tau$
(via the step $u(t-\tau)$ — it persists permanently after being kicked). Superposing all past noise ([P1] Eq.(11), p.182):

$$
\phi(t)=\int_{-\infty}^{\infty}h_\phi(t,\tau)\,i_n(\tau)\,d\tau=\frac{1}{q_{max}}\int_{-\infty}^{t}\Gamma(\omega_0\tau)\,i_n(\tau)\,d\tau .
$$

**Why it's LTV, not LTI**: because $\Gamma(\omega_0\tau)$ is a periodic function of the **absolute instant of injection**. The same impulse,
kicked at the peak ($\Gamma\approx0$), barely changes phase; kicked at the zero crossing ($|\Gamma|$ maximal), changes it the most.
This is exactly [P1] Sec. III's claim C1: "the oscillator's response to noise is linear time-variant, not LTI."

**Unit check**: $h_\phi$ has units of $1/\text{C}$ ($\Gamma$ dimensionless, $q_{max}$ in C, $u$ dimensionless),
$\int h_\phi\, i_n\, d\tau$ has units $=(1/\text{C})\cdot\text{A}\cdot\text{s}=(1/\text{C})\cdot\text{C}=$ dimensionless $=$ rad ✓.

**Used on this site**: [impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift),
[convolution_derivation](/03_isf_core_theory/convolution_derivation),
[lab_04](/04_simulation_labs/lab_04_impulse_injection_sweep) (`lti_vs_ltv_impulse_response.png`:
LTI's step height is fixed, LTV's step height varies with injection phase).

---

## 3. The integrator's frequency response $1/(j\omega)$ (why white noise → 1/f² phase noise)

**One line**: phase is the "integral" of noise current (the upper limit of Eq.(11) is $t$); an integrator in the frequency domain is
$1/(j\omega)$, and in power terms $1/\omega^2$. This is the source of the $-20$ dB/dec slope.

For an ideal integrator $y(t)=\int_{-\infty}^{t}x(\tau)\,d\tau$, with a single tone $x(t)=e^{j\omega t}$:

$$
\int^{t}e^{j\omega\tau}\,d\tau=\frac{1}{j\omega}e^{j\omega t}\;\Rightarrow\;H(j\omega)=\frac{1}{j\omega}.
$$

- **Magnitude**: $|H(j\omega)|=1/\omega$. **Power (PSD multiplier)**: $|H|^2=1/\omega^2$.
- **dB slope**: $10\log_{10}(1/\omega^2)=-20\log_{10}\omega$, $-20$ dB per decade — exactly the
  $1/f^2$-region slope of phase noise.

**Connecting to the ISF**: taking $\Gamma$'s rms as an effective gain, the noise-current PSD $S_i$, after "multiplying by $\Gamma_{rms}/q_{max}$
then integrating," gives the phase PSD:

$$
S_\phi(\Delta\omega)=\frac{\Gamma_{rms}^2}{q_{max}^2}\cdot\frac{S_i}{\Delta\omega^2}.
$$

- **Unit check** (using $\text{C}=\text{A}\cdot\text{s}$):

$$
\frac{1}{\text{C}^2}\cdot\frac{\text{A}^2/\text{Hz}}{(\text{rad/s})^2}=\frac{\text{A}^2/\text{Hz}}{\text{C}^2\cdot\text{s}^{-2}}=\frac{\text{A}^2/\text{Hz}}{\text{A}^2}=\frac{1}{\text{Hz}}=\text{rad}^2/\text{Hz}\ \checkmark
$$

**Factor-of-2 note**: using the equation above (a clean time-domain derivation) gives $\mathcal{L}=\frac12 S_\phi$, corresponding to a denominator of $2\Delta\omega^2$;
whereas [P1] Eq.(21), p.185 writes $4\Delta\omega^2$. The factor-of-2 difference is an SSB bookkeeping convention, a well-known minor point of contention in the literature,
and **does not affect** the $\Gamma_{rms}^2/q_{max}^2$ scaling or the $-20$ dB/dec slope. See
[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) for details.

**Used on this site**: [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise),
[lab_06](/04_simulation_labs/lab_06_white_noise_phase_noise).

---

## 4. The PSD of a stochastic process and the Wiener–Khinchin theorem

**One line**: a stationary stochastic process's "power spectral density" (PSD) is the Fourier transform of its "autocorrelation function."
This connects time-domain noise (autocorrelation) with frequency-domain noise (PSD), and is the foundation of every phase-noise calculation.

For a stationary stochastic process $x(t)$, the autocorrelation is $R_x(\tau)=\langle x(t)\,x(t+\tau)\rangle$.
**Wiener–Khinchin theorem**:

$$
S_x(\omega)=\int_{-\infty}^{\infty}R_x(\tau)\,e^{-j\omega\tau}\,d\tau .
$$

- **White-noise special case**: $R_x(\tau)=\frac{N_0}{2}\delta(\tau)$ (completely uncorrelated at different instants) $\Rightarrow S_x(\omega)=\frac{N_0}{2}$
  (frequency-independent — that's what "white" means). This site uses the single-sided PSD $S_i=\overline{i_n^2}/\Delta f$ (A²/Hz).
- **Variance (total power)**:

$$
\sigma_x^2=R_x(0)=\frac{1}{2\pi}\int_{-\infty}^{\infty}S_x(\omega)\,d\omega=\int_0^{\infty}S_x^{(1\text{-side})}(f)\,df .
$$

This is where the phase-variance formula $\sigma_\phi^2=\int_{f_1}^{f_2}S_\phi(f)\,df$ comes from: phase variance
is the integral of the phase PSD over frequency ([P1]'s usage convention; a standard stochastic-process result).

**Unit check**: $S_\phi$ is in rad²/Hz, $\int S_\phi\, df$ has units $=\text{rad}^2/\text{Hz}\cdot\text{Hz}=\text{rad}^2$ ✓.

**External source**: Wiener–Khinchin is a standard stochastic-process theorem (**not among the five downloaded PDFs**, standard textbook material,
e.g. Papoulis; [P1] uses its conclusion directly).

**Used on this site**: [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter),
[stochastic_processes_recap](/02_foundations/stochastic_noise_basics),
[lab_06](/04_simulation_labs/lab_06_white_noise_phase_noise) (estimating PSD via Welch's method),
[lab_08](/04_simulation_labs/lab_08_jitter_integration) (integrating PSD to get jitter).

---

## 5. $10\log_{10}$ / dB and dBc/Hz conversion

**One line**: dB is a "log scale of a power ratio"; dBc/Hz is the phase-noise unit "power relative to the carrier, per Hz of bandwidth."
Remembering "$\times10$ power $=+10$ dB, $\times2$ power $\approx+3$ dB" is enough to get by.

Definition (power ratio):

$$
X_{\text{dB}}=10\log_{10}\!\left(\frac{P}{P_{ref}}\right).
$$

- **Voltage/amplitude ratio**: because power $\propto$ amplitude$^2$, $X_{\text{dB}}=20\log_{10}(V/V_{ref})$
  (an extra factor of 2).
- **Inverse conversion**: $P/P_{ref}=10^{X_{\text{dB}}/10}$.
- **SSB phase noise** $\mathcal{L}(\Delta f)$'s unit is dBc/Hz: "c" = relative to carrier,
  "/Hz" = per unit bandwidth. Its relation to the phase PSD (small-angle approximation, see Section 6):

$$
\mathcal{L}(\Delta f)\approx\frac12 S_\phi(\Delta f)\quad\Longrightarrow\quad
\mathcal{L}_{\text{dBc/Hz}}=10\log_{10}\!\left(\tfrac12 S_\phi\right),\;\;
S_\phi=2\cdot10^{\mathcal{L}_{\text{dBc/Hz}}/10}\ \text{rad}^2/\text{Hz}.
$$

**Numerical feel (canonical example C)**: $\mathcal{L}=-100$ dBc/Hz $\Rightarrow 10^{-100/10}=10^{-10}$,
$S_\phi=2\times10^{-10}$ rad²/Hz. 10× better in power ($-110$ dBc/Hz) = $\sqrt{10}\approx3.16\times$ better in amplitude (rms).

**Common conversion table**:

| Power ratio | dB | Voltage ratio | Intuition |
|---|---|---|---|
| $\times2$ | $+3.01$ dB | $\times\sqrt2$ | double the power |
| $\times10$ | $+10$ dB | $\times\sqrt{10}\approx3.16$ | one order of magnitude |
| $\times100$ | $+20$ dB | $\times10$ | two orders of magnitude |
| $\times\tfrac12$ | $-3.01$ dB | $\times1/\sqrt2$ | halve it |

**Used on this site**: [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter),
[numerical_feeling](/04_simulation_labs/numerical_feeling) (Example 3, the full set of conversions),
[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise).

---

## 6. The small-angle PM approximation (where $\mathcal{L}\approx\frac12 S_\phi$ comes from)

**One line**: when phase jitter is small, the single-sideband power of a phase modulation is about half the phase PSD. This is the bridge
that converts "phase PSD" into the "dBc/Hz" on a datasheet.

Consider a phase-modulated carrier: $v(t)=A\cos\!\big(\omega_0 t+\phi(t)\big)$. When $|\phi(t)|\ll1$ rad
(small-angle), expand trigonometrically and approximate $\cos\phi\approx1$, $\sin\phi\approx\phi$:

$$
v(t)=A\big[\cos\omega_0 t\cos\phi-\sin\omega_0 t\sin\phi\big]\approx A\cos\omega_0 t-A\,\phi(t)\sin\omega_0 t .
$$

- The first term is the pure carrier; the second term $-A\,\phi(t)\sin\omega_0 t$ is the "phase sideband" — it moves the baseband
  $\phi(t)$ to either side of the carrier.
- For a phase component at a single offset frequency $\Delta f$, the sideband power is proportional to the power of $\phi$; converting to the **single-sideband**
  (SSB) density relative to the carrier gives

$$
\mathcal{L}(\Delta f)\approx\frac12 S_\phi(\Delta f).
$$

That $\frac12$ comes from the bookkeeping of "total phase power split evenly between the upper and lower sidebands."

**Applicability condition (important)**: holds only for $\sigma_\phi\ll1$ rad. If the integration bandwidth is wide enough that $\sigma_\phi$ approaches or exceeds 1 rad,
this approximation fails (the carrier gets "smeared out"), and a more complete treatment is needed. Canonical example C's $\sigma_\phi=14.07$ mrad
$\ll1$, so it is safe.

**Used on this site**: [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter),
[numerical_feeling](/04_simulation_labs/numerical_feeling), Eq.(16) of the spec ($\mathcal{L}\approx\frac12 S_\phi$).

---

## 7. Trigonometric identities (the workhorse behind deriving Eq.(15)–(18))

**One line**: when multiplying "some harmonic of the ISF" by "an injected single tone" and integrating over time, you use product-to-sum identities
to split the product into a slow term (survives) and a fast term (vanishes after integration).

For an injected single tone $i(t)=I_0\cos(\Delta\omega\,t)$ near DC, the phase response ([P1] Eq.(13), p.183's $c_0$ term)
requires computing $\int^{t}I_0\cos(\Delta\omega\,\tau)\,d\tau=\dfrac{I_0\sin(\Delta\omega\,t)}{\Delta\omega}$,
directly giving [P1] Eq.(15), p.183:

$$
\phi(t)\approx\frac{I_0\,c_0\sin(\Delta\omega\,t)}{2q_{max}\,\Delta\omega}.
$$

When the tone is near $n\omega_0$, use **product-to-sum**:

$$
\cos(n\omega_0\tau+\theta_n)\cos\big((n\omega_0+\Delta\omega)\tau\big)
=\frac12\cos\big((2n\omega_0+\Delta\omega)\tau+\theta_n\big)+\frac12\cos\big(\Delta\omega\,\tau-\theta_n\big).
$$

- The first term has frequency $\approx2n\omega_0$ (fast); after integration its amplitude $\propto1/(2n\omega_0)$, tiny, negligible.
- The second term has frequency $\Delta\omega$ (slow, near DC); after integration its amplitude $\propto1/\Delta\omega$, survives.

Keeping only the slow term and integrating gives [P1] Eq.(16)/(17), p.183:

$$
\phi(t)\approx\frac{I_0\,c_n\sin(\Delta\omega\,t)}{2q_{max}\,\Delta\omega}.
$$

That $\frac12$ is exactly what falls out of the product-to-sum step. **Physical meaning**: the ISF's $n$-th harmonic acts like a mixer,
"downconverting" noise near $n\omega_0$ into low-frequency phase modulation near the carrier — this is the frequency-translation picture of phase noise.

**Common identity quick reference**:

| Identity | Use |
|---|---|
| $\cos A\cos B=\tfrac12[\cos(A-B)+\cos(A+B)]$ | separating slow/fast terms (Eq.16/17) |
| $\sin^2\theta=\tfrac12(1-\cos2\theta)$ | computing $\Gamma_{rms}$ (rms of $-\sin$ is $1/\sqrt2$) |
| $\int^{t}\cos(\omega\tau)d\tau=\sin(\omega t)/\omega$ | integrator $1/\omega$ (Eq.15) |

**Used on this site**: [fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf),
[convolution_derivation](/03_isf_core_theory/convolution_derivation), the orthogonality used in Section 1's Parseval.

---

## 8. Random walk variance (the $\sqrt{\Delta t}$ law of accumulated jitter)

**One line**: an open-loop oscillator has no absolute time reference, so each period's phase error accumulates independently like a "drunkard's walk";
the **variance** of the error grows linearly, so the **standard deviation** grows as $\sqrt{\Delta t}$.

Suppose each period injects an independent, zero-mean phase error $\delta_k$ with variance $\sigma_1^2$ (the result of white noise integrated over one period).
After $M$ periods the total phase error is $\Phi_M=\sum_{k=1}^{M}\delta_k$. Because each $\delta_k$ is **independent**,
the variances add (cross-correlation terms have zero expectation):

$$
\mathrm{Var}(\Phi_M)=\sum_{k=1}^{M}\mathrm{Var}(\delta_k)=M\,\sigma_1^2 .
$$

- The measurement interval is $\Delta t=M\cdot T$, so $M=\Delta t/T$, $\mathrm{Var}(\Phi_M)=\dfrac{\sigma_1^2}{T}\,\Delta t\propto\Delta t$.
- Converting to time jitter ($\sigma_t=\sigma_\phi/(2\pi f_0)$) and taking the square root:

$$
\sigma_{\Delta t}=\kappa\,\sqrt{\Delta t}\qquad([P2]\ \text{Eq.}(10),\ \text{p.793}).
$$

$\kappa$ is a proportionality constant specific to each device, with units $\sqrt{\text{s}}$; it is determined by the same
$\Gamma_{rms}^2/q_{max}^2$ ratio
([P2] Eq.(12), p.793: $\kappa=\frac{\Gamma_{rms}}{q_{max}}\sqrt{\tfrac12\tfrac{\overline{i_n^2}}{\Delta f}}$, verified verbatim).

**Key intuition**: variance (power) grows linearly, standard deviation (rms) grows as a square root. This is the hallmark of a random walk;
it appears whenever phase errors **accumulate independently with no restoring force** (contrast: with a PLL locked, there is a restoring force and jitter is suppressed,
no longer growing without bound). Corresponds to claim C6.

**Numerical feel**: at a spacing of 1000 periods (at 5 GHz, $\Delta t=200$ ns), $\sigma_{\Delta t}$ is $\sqrt{1000/10}=\sqrt{100}=10\times$ that at a spacing of 10 periods
($\Delta t=2$ ns) — a 100× longer interval gives only 10× more jitter.

**Used on this site**: [lab_03](/04_simulation_labs/lab_03_ring_oscillator_toy_model)
(`ring_oscillator_timing_noise_accumulation.png`: $\sigma_{\Delta t}=\sigma\sqrt{\Delta N}$ random walk),
[psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter),
[serdes_clocking_connection](/06_design_insights/serdes_clocking_connection).

---

## Quick-reference summary table

| Tool | Core formula | Main use on this site |
|---|---|---|
| Fourier/Parseval | $\sum c_n^2=2\Gamma_{rms}^2$ | ISF harmonic decomposition, $\Gamma_{rms}$ |
| LTV convolution | $\phi=\frac{1}{q_{max}}\int^{t}\Gamma\,i_n\,d\tau$ | phase superposition, LTV vs LTI |
| integrator $1/(j\omega)$ | $\vert H\vert ^2=1/\omega^2$ | white noise → $1/f^2$ ($-20$ dB/dec) |
| Wiener–Khinchin | $S_x=\mathcal{F}\{R_x\}$ | PSD ↔ autocorrelation, variance |
| dB / dBc/Hz | $X_{\text{dB}}=10\log_{10}(P/P_{ref})$ | unit conversion |
| small-angle PM | $\mathcal{L}\approx\frac12 S_\phi$ | dBc/Hz ↔ phase PSD |
| product-to-sum | $\cos A\cos B=\tfrac12[\cdots]$ | Eq.(15)–(18) mixing |
| random walk | $\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$ | accumulated jitter |

## Further reading

- Symbol and unit summary table: [notation](/00_overview/notation)
- Stochastic-process recap: [stochastic_processes_recap](/02_foundations/stochastic_noise_basics)
- Numerical-feel exercises: [numerical_feeling](/04_simulation_labs/numerical_feeling)
- Equation index (each equation → derivation page → source): [equation_index](/01_paper_map/equation_index)
- Full literature list: [references](/99_appendix/references)
