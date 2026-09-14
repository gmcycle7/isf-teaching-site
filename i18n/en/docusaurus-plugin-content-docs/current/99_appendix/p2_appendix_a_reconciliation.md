---
title: "[P2] Appendix A Verbatim Reconciliation: The Time-Domain Autocorrelation Route and the Khinchin Route"
description: "Verbatim transcription and factor-by-factor reconciliation of [P2] Appendix A, \"Relationship Between Jitter and Phase Noise\" (p.802-803): the white-noise time-domain autocorrelation route Eq.(40)-(44) and the autocorrelation + Khinchin route Eq.(45)-(51), mapped step by step against Steps 3 and 4 of the jitter_kernels page, with an honest account of what each route skips and what it spells out in full, plus a Python replay of both routes landing on the same kappa^2*DeltaT."
---

> **β**: This English translation is in beta — the Traditional-Chinese original is the authoritative version.

# [P2] Appendix A Verbatim Reconciliation: The Time-Domain Autocorrelation Route and the Khinchin Route

> Prerequisites: [jitter_kernels](/02_foundations/jitter_kernels) (Steps 0-4: the single-convention declaration, edge = a sample of the phase, the derivation of the three kernels, the white-FM closed form) | Next: back to [jitter_kernels](/02_foundations/jitter_kernels) Step 5 (the flicker $1/f^3$ closed form) · [allan_variance](/02_foundations/allan_variance)

> This page is the **paper-native source** for Steps 3 and 4 of [jitter_kernels](/02_foundations/jitter_kernels): it transcribes [P2] Appendix A verbatim, then maps it term by term and factor by factor against that page's own derivation. **"That page" below always refers to the [jitter_kernels](/02_foundations/jitter_kernels) main page.** This page only transcribes and reconciles — it does not re-derive anything; every formula, number, and code block shares the same canonical parameters and notation as Steps 0-4 of that page.

Steps 3 and 4 are this site's own derivation; [P2] actually walks the very same
ground **twice, once along each route**, in **Appendix A "Relationship Between
Jitter and Phase Noise"** — it **starts in the right column of p.802 and ends in
the left column of p.803** (the right column of p.803 onward is Appendix B on
nonsymmetric edges; don't confuse the two): Eq.(40)–(44) is the white-noise
time-domain route (= Section 4.2 of that page), Eq.(45)–(49) is the
autocorrelation + Khinchin route (= that page's Route A), followed by two
practical corollaries Eq.(50)/(51) (= Section 4.5 and the one-period version of
4.4). The main text on p.793 states explicitly that Eq.(11)'s source is here
("As shown in Appendix A, for $\Delta T\gg T$ or $\Delta T=nT$…", immediately
followed by
$\sigma_{\Delta\phi}^2=\frac{\Gamma_{rms}^2\cdot\overline{i_n^2}/\Delta f}{2q_{max}^2}\Delta T$).
What follows is transcribed verbatim from the rendered PDF pages of p.802–803
(verified under magnification), exactly as printed — printing slips included.

## A.1 The white-noise time-domain route: Eq.(40)–(44) (p.802, right column)

The definition of phase jitter (in the paper's words: "The phase jitter is"):

$$
\sigma_{\Delta\phi}^2=E\{\Delta\phi^2\}=E\big\{[\phi(t+\Delta T)-\phi(t)]^2\big\}
\qquad(\text{[P2] Eq.(40), p.802})
$$

where (the ISF phase integral of [P1], with its limits cut to the observation window):

$$
\Delta\phi=\int_0^{\Delta T}\frac{\Gamma(\omega_0\tau)}{q_{max}}\,i(\tau)\,d\tau.
\qquad(\text{Eq.(41)})
$$

Squaring and exchanging expectation with integration:

$$
\sigma_{\Delta\phi}^2=\frac{1}{q_{max}^2}\int_0^{\Delta T}\!\!\int_0^{\Delta T}
\Gamma(\omega_0\tau_1)\,\Gamma(\omega_0\tau_2)\cdot E[i(\tau_1)i(\tau_2)]\,d\tau_1\,d\tau_2.
\qquad(\text{Eq.(42)})
$$

The paper writes the white-noise current autocorrelation explicitly as
$R_{ii}(t_1,t_2)=(1/2)\big(\overline{i_n^2}/\Delta f\big)\delta(t_1-t_2)$;
substituting it collapses the double integral into a single one:

$$
\sigma_{\Delta\phi}^2=\frac12\,\frac{\overline{i_n^2}/\Delta f}{q_{max}^2}
\int_0^{\Delta T}\Gamma^2(\omega_0\tau)\,d\tau
\qquad(\text{Eq.(43)})
$$

$$
\sigma_{\Delta\phi}^2=\frac12\,\frac{\overline{i_n^2}/\Delta f}{q_{max}^2}\,
\Gamma_{rms}^2\,\Delta T
\quad\text{for}\quad\Delta T\gg T\ \text{or}\ \Delta T=mT.
\qquad(\text{Eq.(44)})
$$

**Eq.(44) is literally the main text's Eq.(11)** (p.793; only the typesetting
differs), and its coefficient
$\tfrac12\,(\overline{i_n^2}/\Delta f)\,\Gamma_{rms}^2/q_{max}^2$ is exactly the
$\kappa^2$ of Section 4.2 (with $S_i\equiv\overline{i_n^2}/\Delta f$) — the
paper's time-domain route matches 4.2 **symbol for symbol**.

## A.2 The autocorrelation + Khinchin route: Eq.(45)–(51) (p.803, left column)

The paper then switches to the second route — stating up front that timing
jitter is the standard deviation of the timing uncertainty:

$$
\sigma_{\Delta\phi}^2=\frac{1}{\omega_0^2}E\big\{[\phi(t+\Delta T)-\phi(t)]^2\big\}
=\frac{E[\phi^2(t)]}{\omega_0^2}+\frac{[\phi^2(t+\Delta T)]}{\omega_0^2}
-\frac{E[\phi(t)\phi(t+\Delta T)]}{\omega_0^2}
\qquad(\text{Eq.(45), as printed})
$$

$$
R_\phi(\tau)=E[\phi(t)\phi(t+\Delta T)]
\qquad(\text{Eq.(46), as printed})
$$

$$
\sigma_{\Delta\phi}^2=\frac{2}{\omega_0^2}\big[R_\phi(0)-R_\phi(\Delta T)\big].
\qquad(\text{Eq.(47)})
$$

$$
R_\phi(\tau)=\int_{-\infty}^{\infty}S_\phi(f)\,e^{j2\pi f\tau}\,df
\qquad(\text{Eq.(48), the Khinchin theorem})
$$

$$
\sigma_{\Delta\phi}^2=\frac{8}{\omega_0^2}\int_0^{\infty}S_\phi(f)\sin^2(\pi f\tau)\,df.
\qquad(\text{Eq.(49)})
$$

plus the two practical corollaries restricted to white noise (the $1/f^2$
region) — Eq.(50) is obtained by combining the main text's (6)+(12), and
Eq.(51) then follows "based on (8)" (i.e., $\sigma=\kappa\sqrt T$); **neither**
comes from integrating (49):

$$
\kappa=\frac{\Delta f}{f_0}\cdot10^{-\mathcal{L}\{\Delta f\}/20}
\qquad(\text{Eq.(50)})
$$

$$
\sigma_{CTC}=\frac{f}{f_0^{1.5}}\cdot10^{-\mathcal{L}\{\Delta f\}/20}.
\qquad(\text{Eq.(51), as printed})
$$

**As-printed disclosure (verified under magnification; symbol overloading and
printing slips listed honestly)**:

1. **$\sigma_{\Delta\phi}^2$ does double duty**: in Eq.(40)–(44) the LHS is
   **phase** jitter (rad²); from Eq.(45) on, the LHS is still printed
   $\sigma_{\Delta\phi}^2$ yet carries an extra $1/\omega_0^2$, and the text
   explicitly calls it timing jitter — it is really
   $\sigma_{\Delta T}^2=\sigma_{\Delta\phi}^2/\omega_0^2$ (s², i.e., the
   Eq.(10) conversion). That page names $\sigma_{\Delta\phi}$ and
   $\sigma_{\Delta t}$ separately precisely to defuse this mine.
2. **The expansion line of Eq.(45) drops two symbols**: the middle term is
   missing its $E$, and the cross term is missing its factor 2 (the cross term
   of $[a-b]^2$ is $2ab$; under stationarity the first two terms combine into
   $2R_\phi(0)$, so landing on Eq.(47) requires the cross term to be
   $2R_\phi(\Delta T)$). Eq.(47) itself is printed correctly — the slip does
   not propagate.
3. **$\tau$ and $\Delta T$ are mixed**: Eq.(46) writes $R_\phi(\tau)$ on the
   LHS but uses $\Delta T$ on the RHS; the kernel of Eq.(49) is written
   $\sin^2(\pi f\tau)$, where this $\tau$ is the delay $\Delta T$.
4. **The numerator of Eq.(51) is printed as $f$**: multiplying Eq.(50)'s
   (time-version) $\kappa$ by $\sqrt T=f_0^{-0.5}$ gives
   $\sigma_{CTC}=\kappa\sqrt T$, so the numerator should be the offset
   frequency $\Delta f$ — the printing swallowed the $\Delta$ (the
   transcription in "Corresponding papers / equations" is annotated
   accordingly).
5. The integration limits $\int_{-\infty}^{\infty}$ of Eq.(48) declare that
   $S_\phi$ here is a **two-sided** spectrum — the only place in the whole
   paper where the convention leaks out; the 8 of Eq.(49) therefore has one
   bookkeeping 2 built in (see the table below).

## A.3 Step-by-step mapping: the paper's two routes ↔ that page's derivation

| [P2] | what that step does | that page's counterpart | factor reconciliation (against the Step 0 table) |
|---|---|---|---|
| Eq.(40) | defines phase jitter | Step 2's first-order difference $P_k(N)$ (in phase language) | — |
| Eq.(41) | $\Delta\phi$ = ISF-weighted window integral | [P1] Eq.(11) as cited in 4.2 (limits changed to the window) | — |
| Eq.(42) | expands the square into a double integral + $E[i(\tau_1)i(\tau_2)]$ | first line of 4.2 (the general form before substituting the autocorrelation) | holds for any (non-white) autocorrelation |
| Eq.(43) | white noise $R_{ii}=\tfrac12(\overline{i_n^2}/\Delta f)\delta$ collapses it to a single integral | 4.2's $R_i(\tau)=\tfrac{S_i}{2}\delta(\tau)$ | **the same $\tfrac12$**: one-sided PSD ↔ two-sided flat level |
| Eq.(44) | $\int\Gamma^2\to\Gamma_{rms}^2\Delta T$ ($\Delta T\gg T$ or $=mT$) | 4.2's parenthetical "exact for integer periods" + 4.3's $\kappa^2NT$ | Eq.(44) = main text Eq.(11) = $\kappa^2\Delta T$ |
| Eq.(45)–(47) | WSS expansion: variance of a difference $=2[R_\phi(0)-R_\phi(\Delta T)]$ | Route A, step 1 (same equation) | **the 2 of Eq.(47)** = the "variance of a difference" 2 |
| Eq.(48) | Khinchin theorem (two-sided spectrum, $\int_{-\infty}^{\infty}$) | Route A, step 2 (one-sided cosine version) | $S_\phi^{DS}=S_\phi/2$ |
| Eq.(49) | $\dfrac{8}{\omega_0^2}\displaystyle\int_0^\infty S_\phi^{DS}\sin^2(\pi f\tau)\,df$ | kernel (b)'s $\dfrac{1}{\omega_0^2}\displaystyle\int_0^\infty S_\phi\,4\sin^2 df$ | **8 = 2 (two-sided→one-sided) × 4 (difference kernel)**, $1/\omega_0^2$ = phase→time — a literal reprise of the Step 0 table's second column |
| Eq.(50) | reads $\kappa\leftarrow\mathcal{L}$ off the main text's (6)+(12) | 4.5 (the negative exponent = the "dB below carrier" reading, per the v5 note) | takes the $/2$-convention $\mathcal{L}$ |
| Eq.(51) | $\sigma_{CTC}=\kappa\sqrt T$ (one-period version) | end note of 4.4 (adjacent-difference definition multiplies by another $\sqrt2$) | printed numerator $f$ should read $\Delta f$ |

## A.4 Who skips what (honest bookkeeping in both directions)

**Skipped by [P2], filled in by that page**:

- **The stationarity rigor gap**: Eq.(45)–(47) needs $R_\phi(0)$ finite; a
  free-running oscillator's $\phi$ is a random walk, so $R_\phi(0)$ diverges
  (exactly the confession at the start of that page's Route A). The difference
  $R_\phi(0)-R_\phi(\Delta T)$ is finite and the conclusion survives, but
  making it rigorous requires that page's **Route B** (which only demands that
  $\nu=\dot\phi$ be stationary) — the paper does not address this step.
- **No convention declared**: not one sentence in the paper says whether
  $S_\phi$ is one- or two-sided; only the integration limits of Eq.(48) give
  it away. That page's three-column table in Step 0 lays that out in the open
  (v5 used exactly those limits to infer "two-sided" and reconcile the
  literature's "coefficient-8 version" with the one-sided $4\sin^2$ kernel).
- **The two routes are never interlocked in the paper**: Eq.(44) stops in the
  time domain, Eq.(49) stops in the frequency domain; the paper never
  substitutes the white-noise spectrum into (49) to check that it lands back
  on (44). That page's 4.1 integral
  $\int_0^\infty\sin^2(ax)/x^2\,dx=\pi a/2$ plus the substitution in 4.3 is
  that missing closed loop (the code below computes both routes — same
  number).
- Neither the time-domain flicker $1/f^3$ closed form (Step 5's log formula)
  nor the c2c $16\sin^4$ kernel (kernel (c); Eq.(51) is only the one-period
  version) appears in the paper.

**Glossed over by that page, written out in full by [P2]**:

- **The general double integral of Eq.(42)**: Section 4.2 jumps straight to
  "white-noise δ correlation ⇒ single integral"; the paper writes out the
  general form
  $\Gamma(\omega_0\tau_1)\Gamma(\omega_0\tau_2)\,E[i(\tau_1)i(\tau_2)]$ — the
  starting point that accepts any colored-noise autocorrelation, with white
  noise merely a special case.
- **The validity condition printed inside the equation**: Eq.(44)'s "for
  $\Delta T\gg T$ or $\Delta T=mT$" prints right next to the equals sign the
  condition for $\int\Gamma^2\to\Gamma_{rms}^2\Delta T$ to be exact; this
  page's 4.2 only mentions it in a parenthesis. For short or non-integer
  $\Delta T$ there is an $O(T/\Delta T)$-level $\Gamma^2$ ripple residual.

## A.5 Replaying the white-FM variance along both routes (checkable via # ->)

```python
import numpy as np
from simulations.common.isf_utils import gamma_lc_ideal

F0, T = 5e9, 2e-10
W0 = 2 * np.pi * F0
QMAX, SI, GRMS = 1e-12, 1e-24, 0.5      # canonical parameters
N = 100
DT = N * T                              # ΔT = mT (the validity condition of Eq.(44))

# Route 1: [P2] Appendix A time-domain autocorrelation route — substituting R_ii=(S_i/2)δ into Eq.(42) collapses it to Eq.(43)
tau = np.linspace(0.0, DT, 200 * N + 1)
gam = np.sqrt(2.0) * GRMS * gamma_lc_ideal(W0 * tau)     # LC-shaped ISF with Γrms=0.5
var_43 = 0.5 * SI / QMAX**2 * np.trapezoid(gam**2, tau)  # Eq.(43), numerical integral
var_44 = 0.5 * SI / QMAX**2 * GRMS**2 * DT               # Eq.(44) = main text Eq.(11)
print(f"{var_43:.4e}")            # -> 2.5000e-09 rad^2 (Eq.(43), σ²_Δφ @ N=100)
print(f"{var_43/var_44:.4f}")     # -> 1.0000 (at ΔT=mT, ∫Γ² is exactly Γrms²ΔT)

# Route 2: that page's kernel route — one-sided S_φ=2κ²/(2πf)² times the 4sin²(πfΔT) kernel
kappa2 = GRMS**2 / QMAX**2 * SI / 2                      # κ²=Γrms²S_i/(2q_max²)
print(f"{kappa2:.4f}")            # -> 0.1250 rad^2/s (the same prefactor as Eq.(44))
x = np.linspace(1e-8, 1e4, 4_000_001)                    # x = fΔT
core = np.trapezoid(np.sin(np.pi * x)**2 / x**2, x) + 0.5 / x[-1]  # tail: sin²→1/2
var_kernel = 2 * kappa2 * DT / np.pi**2 * core           # = κ²ΔT (the 4.3 analytic value)
print(f"{var_kernel/var_43:.4f}") # -> 1.0000 (frequency kernel = Appendix A route, same number)

# Reconciling [P2] Eq.(49): 8/ω₀² × two-sided S_φ^DS=κ²/(2πf)², LHS is the time-version variance
var_49 = 8 / W0**2 * (kappa2 * DT / 4 / np.pi**2) * core
print(f"{var_49/(kappa2*DT/W0**2):.4f}")   # -> 1.0000 (8 = 2(two-sided→one-sided)×4(kernel))
print(f"{np.sqrt(var_49)*1e15:.2f} fs")    # -> 1.59 fs (σ_ΔT @ N=100 = √100×0.159 fs)
```

The first two prints walk [P2] Eq.(43)→(44) (the time-domain autocorrelation
route); the remaining four walk that page's kernel (b) and the two-sided
bookkeeping of Eq.(49) — **one oscillator, two routes, one number,
$\kappa^2\Delta T=2.5\times10^{-9}\ \text{rad}^2$**. Appendix A and Steps 3/4
of that page are two proofs of the same theorem; the only difference is that
the paper hides its convention inside the integration limits, while that page
prints it in Step 0.

## Applicability and failure conditions

| Condition | When both routes (this page) agree with that page's kernel route | When they disagree / need care |
|---|---|---|
| $\Delta T\gg T$ or $\Delta T=mT$ (an integer number of periods) | Eq.(44)'s $\int\Gamma^2\to\Gamma_{rms}^2\Delta T$ is exact, matching that page's 4.3 $\kappa^2NT$ digit for digit (A.5 code) | For short or non-integer $\Delta T$: $\Gamma^2$ carries an $O(T/\Delta T)$-level ripple residual, so Eq.(44) is only approximate |
| The convention of $S_\phi$ (one-sided vs. two-sided) is known | Eq.(49)'s 8 = 2 (two-sided→one-sided) × 4 (difference kernel), matching that page's one-sided $4\sin^2$ kernel exactly (A.3 table) | If the convention is unstated and Eq.(49)'s "8" is applied directly, it disagrees with that page's one-sided kernel by a factor of 2 (jitter off by $\sqrt2$) |
| Only the phase increments / frequency noise $\nu=\dot\phi$ need be stationary | That page's Route B kernel formula holds rigorously even for a random-walk $\phi$ (where $R_\phi(0)$ diverges) | Insisting on the paper's Eq.(45)-(47) WSS expansion (which needs $R_\phi(0)$ finite) requires the extra convergence argument of A.4 |
| Only the white-FM $1/f^2$ region is being computed | Eq.(50)/(51) read $\kappa$ off $\mathcal{L}$ directly (taking the time-domain $/2$-convention $\mathcal{L}$) | If flicker or other colored noise dominates, or the $\mathcal{L}$ bookkeeping is mixed up ($/2$ vs. $/4$): Eq.(50)/(51) no longer apply — fall back to that page's Step 5 log closed form |

## Key takeaways

- [P2] Appendix A proves the same thing along **two independent routes**: **A.1** the white-noise time-domain autocorrelation route (Eq.(40)-(44), converging on the main text's Eq.(11)), and **A.2** the autocorrelation + Khinchin route (Eq.(45)-(49)), plus two white-noise-special-case corollaries Eq.(50)/(51).
- **A.3**'s step-by-step table pins every equation in the paper back onto that page's matching derivation and convention (which 2 belongs to which step); **A.4** honestly accounts for what each side skips and spells out in full (the paper never states its $S_\phi$ convention and never interlocks the two routes; that page never writes out the general double integral of Eq.(42)).
- **A.5**'s Python computes the time-domain autocorrelation route (Eq.(43)) and that page's frequency-domain kernel route separately, for the same oscillator, landing on the same number $\kappa^2\Delta T=2.5\times10^{-9}\ \text{rad}^2$ (every `# ->` prints 1.0000).
- The paper itself has a few **printing slips** (the expansion of Eq.(45) drops $E$ and a factor of 2; the numerator of Eq.(51) is printed as $f$ and should read $\Delta f$) — this page transcribes them exactly as printed and annotates them alongside, without correcting the paper.

## Further reading

- The first-principles derivation of the three kernels and the white-noise/flicker closed forms: [jitter_kernels](/02_foundations/jitter_kernels)
- PSD / phase noise / jitter basics: [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter)
- Stochastic-process and stationarity basics: [stochastic_noise_basics](/02_foundations/stochastic_noise_basics)
- Allan variance (another difference kernel): [allan_variance](/02_foundations/allan_variance)
- Full reference list: [references](/99_appendix/references)
