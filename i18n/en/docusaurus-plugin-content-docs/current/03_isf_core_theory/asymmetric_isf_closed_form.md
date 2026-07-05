---
title: Closed Forms for the Asymmetric Triangular ISF ([P2] Appendix B)
description: Step-by-step derivation of [P2] Appendix B Eq.(52)–(57) — closed forms for Γrms, Γdc and the 1/f³ corner of a triangular ISF with asymmetric rise/fall; A=1 reduces exactly to Eq.(16), corner ∝ (1−A)²/(1−A+A²) and ∝ 1/N; with worked numbers, convention factor-2 flags and lab_33 verification.
---

import NumericQuiz from "@site/src/components/NumericQuiz";
import AsymmetricIsfExplorer from "@site/src/components/AsymmetricIsfExplorer";

> **β**: This English translation is in beta — the Traditional-Chinese original is the authoritative version.

# Closed Forms for the Asymmetric Triangular ISF ([P2] Appendix B)

> **Prerequisites**: [fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf) ($c_0$ and Parseval), [rms_isf](/03_isf_core_theory/rms_isf) (definition and role of $\Gamma_{rms}$), [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion) (why $c_0$ is the only gate for flicker upconversion) | **Next**: [symmetry](/06_design_insights/symmetry) (turning these closed forms into design knobs), [lab_32](/04_simulation_labs/lab_32_mos_level1_ring) (equation-level ring ISF extraction — where the triangular approximation breaks)

The [symmetry](/06_design_insights/symmetry) page gives the qualitative rule "symmetric rise/fall →
$c_0\to0$ → 1/f³ suppressed," but its numerical example plugs in an **assumed** $c_0$. This page fills
the missing piece: **given a ring oscillator's stage count $N$ and how asymmetric its waveform is, what
exactly are $\Gamma_{rms}$, $c_0$, and the 1/f³ corner?** [P2] Appendix B (p.803) answers with a full
set of closed forms, Eq.(52)–(57), built on an asymmetric triangular ISF model — one of the very few
places on this site where $c_0$ is computed **directly from topology parameters**, so it is worth
walking through step by step.

> **Physical intuition (conclusion first)**: a ring's ISF concentrates at the two transitions: a
> **positive lobe** at the rising edge and a **negative lobe** at the falling edge, with lobe height
> inversely proportional to that edge's slope (steeper edge → less sensitive). If the rise is steeper
> than the fall ($A=f'_{rise}/f'_{fall}>1$), the positive lobe is short and narrow while the negative
> lobe is tall and wide — the two lobe areas no longer cancel, and the leftover net area is exactly
> $\Gamma_{dc}$ (i.e. $c_0/2$), which upconverts device 1/f noise into close-in 1/f³. The closed forms
> turn this geometric picture into three formulas — $\Gamma_{rms}^2$ (Eq.55), $\Gamma_{dc}$ (Eq.56),
> corner (Eq.57) — and the corner depends on only **two dimensionless numbers**, $A$ and $N$.

## Step 0: the model — the asymmetric triangular ISF of [P2] Fig. 18

[P2] Fig. 18, p.803 (verified against the rendered PDF page for this unit): *"Approximate waveform and
the ISF for asymmetric rising and falling edges."* The figure plots $\Gamma(x)$ over one period
($x$ from $0$ to $2\pi$) as two triangular lobes:

| Lobe | Height (peak) | Base width | Corresponds to |
|---|---|---|---|
| positive | $1/f'_{rise}$ | $2/f'_{rise}$ | rising edge |
| negative | $1/f'_{fall}$ (depth) | $2/f'_{fall}$ | falling edge |

Here $f'_{rise}$, $f'_{fall}$ are the **maximum slopes of the normalized waveform** ($f(x)$ normalized
to unit amplitude, $x=\omega_0\tau$) during the rising/falling edges (verbatim: *"where $f'_{rise}$ and
$f'_{fall}$ are the maximum slope during the rising and falling edge, respectively"*, p.803).

- **Unit check**: $x=\omega_0\tau$ is $[\text{rad/s}]\cdot[\text{s}]=[\text{rad}]$, and this site treats
  rad as a dimensionless pure number; $f(x)$ is dimensionless, so $f'=df/dx$ and $1/f'$ are also
  dimensionless — consistent with $\Gamma$ being dimensionless ✓.
- **Why the height is $1/f'$**: the ISF peak is inversely proportional to the waveform slope — the
  steeper the edge, the smaller the phase shift caused by the same charge perturbation (see
  [waveform_slope](/06_design_insights/waveform_slope); this is the starting point of the triangular
  approximation in the main text of [P2]).
- **Key geometric observation (slope = 1)**: each lobe has "height $=1/f'$, base width $=2/f'$", so the
  **half-width equals the height** and the two sides of the triangle have slope $\pm1$ in the $x$
  coordinate. This is no accident: the sensitivity peak is $\propto 1/f'$ and the sensitive window (the
  phase width the transition occupies) is also $\propto 1/f'$; they share the same origin, so their
  ratio is fixed at 1. This "unit slope" makes the integrals below extremely clean.
- The **positions** of the lobes along $x$ (where the positive and negative lobes sit) do not affect
  $\Gamma_{rms}$ or $\Gamma_{dc}$ (they only affect the harmonic phases $\theta_n$), so the derivation
  may place the lobes at any non-overlapping positions.

## Step 1: piecewise integration for $\Gamma_{rms}^2$ — Eq.(52)

Start from the definition of $\Gamma_{rms}$ (the [P1] Eq.(20) form, see
[rms_isf](/03_isf_core_theory/rms_isf)) and integrate the two triangular lobes piecewise. Because the
sides have slope $=\pm1$, on each half-side we can use the "value of the ISF" itself as the integration
variable ($\Gamma$ walks linearly from 0 to the peak $1/f'$, with $d\Gamma = \pm\,dx$); one lobe = two
half-sides = $2\int_0^{1/f'}x^2\,dx$. Verbatim ([P2] Eq.(52), p.803, verified against the render):

$$
\Gamma_{rms}^2=\frac{1}{2\pi}\int_0^{2\pi}\Gamma^2(x)\,dx
=\frac{1}{\pi}\!\left[\int_0^{1/f'_{rise}}x^2\,dx+\int_0^{1/f'_{fall}}x^2\,dx\right]
=\frac{1}{3\pi}\left(\frac{1}{f'_{rise}}\right)^{\!3}(1+A^3)
$$

Expanding the middle step into the last step, one line at a time:

$$
\begin{aligned}
\frac{1}{2\pi}\!\left[2\!\int_0^{1/f'_{rise}}\!x^2dx+2\!\int_0^{1/f'_{fall}}\!x^2dx\right]
&=\frac{1}{\pi}\!\left[\frac{x^3}{3}\Big\vert_0^{1/f'_{rise}}+\frac{x^3}{3}\Big\vert_0^{1/f'_{fall}}\right] \\[4pt]
&=\frac{1}{3\pi}\!\left[\left(\frac{1}{f'_{rise}}\right)^{\!3}+\left(\frac{1}{f'_{fall}}\right)^{\!3}\right] \\[4pt]
&=\frac{1}{3\pi}\left(\frac{1}{f'_{rise}}\right)^{\!3}\left(1+A^3\right).
\end{aligned}
$$

- Line 1: each lobe has two half-sides; the sign disappears after squaring, so the positive and negative
  lobes each contribute $2\int_0^{h}x^2dx$ ($h$ = peak height).
- Line 3: factor out $(1/f'_{rise})^3$ using $\dfrac{1}{f'_{fall}}=\dfrac{A}{f'_{rise}}$,
  where $A$ is the **asymmetry ratio** ([P2] Eq.(53), p.803, verbatim):

$$
A\equiv\frac{f'_{rise}}{f'_{fall}}
$$

- **Dimension check**: $[x^2\,dx]=\text{rad}^3$ (dimensionless), divided by $\pi$ (rad) → dimensionless;
  $\Gamma_{rms}^2$ is dimensionless ✓.
- **Sanity check**: at $A=1$ (symmetric), $1+A^3=2$ and the two lobes contribute equally; for $A>1$
  (steep rise), $1/f'_{fall}$ is large and the negative lobe dominates $\Gamma_{rms}^2$ — **the slower
  edge sets the rms sensitivity**.

## Step 2: swap $f'_{rise}$ for circuit parameters — the period constraint Eq.(54)

Eq.(52) still contains the waveform slope. To express it in "parameters a designer holds" (the stage
count $N$), use the ring's period constraint. [P2] Eq.(14), p.794 defines the **normalized stage delay**
$\hat t_D=\eta/f'_{max}$ ($\eta\approx1$ is a proportionality constant: one stage's delay is roughly the
inverse of the transition slope, times $\eta$). In a single-ended inverting ring, the signal travels
around the loop **twice** per full period (every node rises once and falls once), i.e. $2N$ stage
delays — $N$ of them rising-edge delays $\eta/f'_{rise}$ and $N$ falling-edge delays $\eta/f'_{fall}$.
Writing the period's phase length $2\pi$ as the sum of these delays ([P2] Eq.(54), p.803, verbatim):

$$
2\pi=\eta N\!\left(\frac{1}{f'_{rise}}+\frac{1}{f'_{fall}}\right)=\frac{\eta N}{f'_{rise}}(1+A)
$$

Solving for the positive-lobe peak height:

$$
\frac{1}{f'_{rise}}=\frac{2\pi}{\eta N(1+A)},\qquad
\frac{1}{f'_{fall}}=\frac{2\pi A}{\eta N(1+A)}.
$$

- **Dimension check**: both sides are rad (dimensionless) ✓; $\eta,N,A$ are all dimensionless.
- **Sanity check**: at $A=1$ this reduces to the symmetric case $2\pi=2N\hat t_D$ (exactly the
  phase-domain form of [P2] Eq.(15), $f_0=1/(2N\tau_D)$); larger $N$ or larger $A+1$ shrinks the
  positive lobe — every piece of the geometry is "diluted" by the fixed $2\pi$ budget.

## Step 3: combine into $\Gamma_{rms}^2(N,A)$ — Eq.(55), and verify the $A=1$ reduction

Substituting the $1/f'_{rise}$ from Step 2 into Eq.(52):

$$
\Gamma_{rms}^2=\frac{1}{3\pi}\cdot\frac{(2\pi)^3}{\eta^3N^3(1+A)^3}\,(1+A^3)
=\frac{8\pi^2}{3\eta^3N^3}\cdot\frac{1+A^3}{(1+A)^3}
$$

Rearranged into the paper's form ([P2] Eq.(55), p.803, verbatim):

$$
\Gamma_{rms}^2=\frac{2\pi^2}{3\eta^3}\,\frac{1}{N^3}\left[4\,\frac{1+A^3}{(1+A)^3}\right]
$$

- **The $A=1$ check (mandatory)**: the bracket $=4\cdot\dfrac{2}{8}=1$, so
  $\Gamma_{rms}^2=\dfrac{2\pi^2}{3\eta^3}\dfrac{1}{N^3}$ — reducing **exactly** to the v7 reading of
  [P2] Eq.(16), p.794, $\Gamma_{rms}=\sqrt{2\pi^2/(3\eta^3)}\cdot N^{-1.5}$ (the radical covers only the
  constant). Numerically: at $N=5$, $\eta=1$, both give $\Gamma_{rms}=0.229429$ (printed by lab_33).
  This is also a third independent verification of Eq.(16)'s N-scaling (see the
  [paper_002 deep dive](/05_paper_deep_dives/paper_002_jitter_phase_noise_ring)).
- **The cost of asymmetry is mild here**: the bracket is $=1.12$ at $A=1.5$ and $=1.75$ at $A=3$ —
  $\Gamma_{rms}$ only rises by 6% / 32%. **Asymmetry barely hurts the 1/f² (white-noise) region**; its
  real damage comes through $c_0$ below.
- **Invariant under $A\to1/A$**: $\dfrac{1+A^3}{(1+A)^3}$ is unchanged when $A$ is replaced by $1/A$
  (multiply top and bottom by $A^3$). "Steep rise, slow fall" and "steep fall, slow rise" have the same
  rms sensitivity — the direction does not matter, only the degree of asymmetry.

## Step 4: the DC value $\Gamma_{dc}$ — Eq.(56), connecting to $c_0$

$\Gamma_{dc}$ is the average of the ISF over one period. Triangle area $=\tfrac12\cdot$base$\cdot$height:
positive-lobe area $\tfrac12\cdot\dfrac{2}{f'_{rise}}\cdot\dfrac{1}{f'_{rise}}=\dfrac{1}{f'^2_{rise}}$,
and likewise $\dfrac{1}{f'^2_{fall}}$ for the negative lobe (with a minus sign):

$$
\Gamma_{dc}=\frac{1}{2\pi}\!\left[\frac{1}{f'^2_{rise}}-\frac{1}{f'^2_{fall}}\right]
=\frac{1}{2\pi}\,\frac{1-A^2}{f'^2_{rise}}
=\frac{1}{2\pi}\cdot\frac{4\pi^2}{\eta^2N^2(1+A)^2}\,(1-A^2)
$$

Using $1-A^2=(1-A)(1+A)$ to cancel one $(1+A)$ gives the paper's form ([P2] Eq.(56), p.803, verbatim):

$$
\Gamma_{dc}=\frac{2\pi}{\eta^2}\,\frac{1}{N^2}\left(\frac{1-A}{1+A}\right)
$$

- **Connecting to the Fourier coefficient**: the DC **value** of the ISF series ([P1] Eq.(12)) is
  $c_0/2$, so $c_0=2\,\Gamma_{dc}$ — this is the $c_0$ that feeds the [P1] Eq.(24) corner formula
  (same sign trap as on the [symmetry](/06_design_insights/symmetry) page: $c_0$ is the coefficient,
  $c_0/2$ is the DC value).
- **Sign**: $A>1$ (steep rise) → $\Gamma_{dc}<0$ (larger negative-lobe area); $A<1$ flips the sign.
  Upconversion only sees $c_0^2$; the sign does not enter the corner.
- **Scaling highlight**: $\Gamma_{dc}\propto N^{-2}$ falls **faster** than
  $\Gamma_{rms}\propto N^{-1.5}$ (lobe area $\propto$ peak height squared $\propto N^{-2}$; rms squared
  $\propto$ peak height cubed $\propto N^{-3}$). That "extra half power" is precisely the source of the
  corner's $1/N$ law in the next step.
- **Dimension check**: area $[\Gamma\cdot dx]=$ rad (dimensionless), divided by $2\pi$ → dimensionless ✓.

## Step 5: the 1/f³ corner — Eq.(57) (with the factor-2 convention flag)

The corner relation in the main text of [P2] ([P2] Eq.(7), p.792, verified against the render, verbatim):

$$
f_{1/f^3}=f_{1/f}\cdot\frac{\Gamma_{dc}^2}{\Gamma_{rms}^2}
$$

Substituting Eq.(55) and (56), and factoring $1+A^3=(1+A)(1-A+A^2)$:

$$
\frac{\Gamma_{dc}^2}{\Gamma_{rms}^2}
=\frac{\dfrac{4\pi^2}{\eta^4N^4}\dfrac{(1-A)^2}{(1+A)^2}}
      {\dfrac{2\pi^2}{3\eta^3N^3}\cdot\dfrac{4(1+A^3)}{(1+A)^3}}
=\frac{3}{2\eta N}\cdot\frac{(1-A)^2(1+A)}{1+A^3}
=\frac{3}{2\eta N}\cdot\frac{(1-A)^2}{1-A+A^2}
$$

which gives the paper's result ([P2] Eq.(57), p.803, verbatim):

$$
f_{1/f^3}=f_{1/f}\cdot\frac{3}{2\eta N}\cdot\frac{(1-A)^2}{(1-A+A^2)}
$$

> **Factor-2 convention flag (flagged every time a 2 or 4 appears)**: substituting $c_0=2\Gamma_{dc}$
> into [P1] Eq.(24), $\Delta\omega_{1/f^3}=\omega_{1/f}\cdot c_0^2/(2\Gamma_{rms}^2)$, yields
> $2\,\omega_{1/f}\Gamma_{dc}^2/\Gamma_{rms}^2$ — **exactly 2× [P2] Eq.(7)/(57)**. This belongs to the
> same family of bookkeeping issues as the SSB $/4$ vs time-domain $/2$ discussed on the white_noise
> page (how the DC channel is weighted in the $\sum c_n^2$ sum; [P2] Eq.(6), p.792 itself uses
> $/(8\pi^2f^2)$ = the time-domain $/2$ convention). Each paper is internally self-consistent; **the
> scalings ($\propto(1-A)^2/(1-A+A^2)$, $\propto1/N$) and all ratios are unaffected**. This site reports
> the [P2] Eq.(57) value as primary and quotes the [P1] Eq.(24)-convention value (=2×) alongside.

**Interactive exploration**: the widget below lets you drag $N$, $A$, $\eta$, and $f_{1/f}$
directly and watch $\Gamma_{rms}$, $c_0$, and the corner (from Eq.55–57) update live, alongside
the Fig.18 triangular-lobe shape on the left and the corner-vs-$A$ V-shaped valley on the right
(the analytic version of the [P2] Fig.17 measured bowl) with the current point marked:

<AsymmetricIsfExplorer />

Eq.(57) has three structural properties, each carrying a design message:

1. **The corner vanishes quadratically as $A\to1$**: the numerator $(1-A)^2$ — near the symmetry point
   the corner is **second-order insensitive** to asymmetry, but once you drift away the degradation also
   accelerates quadratically (lab_33: at $A=1.01$ corner$/f_{1/f}$ is only $2.97\times10^{-5}$, while at
   $A=1.10$ it is already $2.70\times10^{-3}$ — nearly 100× apart). This is the analytic version of the
   bowl-shaped minimum of [P2] Fig. 17, p.802 ("phase noise vs symmetry control voltage").
2. **Invariant under $A\to1/A$**: $(1-A)^2/(1-A+A^2)$ is unchanged when $A$ is replaced by $1/A$
   (multiply top and bottom by $A^2$; lab_33 verifies corner$(A{=}2)=$ corner$(A{=}0.5)
   =1.000000\times10^{-1}\,f_{1/f}$). The V-shaped valley is left-right symmetric on a log-$A$ axis —
   "which edge is steeper" does not matter.
3. **Corner $\propto 1/N$**: at fixed $A$, more stages means a lower corner. Verbatim (p.803, end of
   App. B): *"As can be seen for a constant rise-to-fall ratio, the 1/f³ corner decreases inversely
   with the number of stages; therefore, ring oscillators with a smaller number of stages will have a
   larger 1/f³ noise corner. As a special case, if the rise and fall time are symmetric, A = 1, and the
   1/f³ corner approaches zero."*

> **Reconciling with the "N-independence" conclusion**: [P2]'s main-text Eq.(23) says that at fixed
> $f_0$ and power, phase noise in the **white-noise (1/f²) region** is approximately N-independent (see
> the [paper_002 deep dive](/05_paper_deep_dives/paper_002_jitter_phase_noise_ring) and
> [lc_vs_ring](/06_design_insights/lc_vs_ring)). There is no contradiction: $N$ does not move the
> **height** of the 1/f² region, but it pushes the 1/f³ **knee** toward lower frequency ($\propto1/N$).
> Design message: if your pain point is close-in flicker (e.g. the PLL loop bandwidth is too narrow to
> clean up the VCO's 1/f³), **more stages is an effective lever**; if the pain point is white-region
> jitter, adding stages does not help. This is the new design takeaway of this page — called out by
> [P2] itself.

## Numerical examples (canonical: $N=5$, $\eta=1$, $f_{1/f}=1$ MHz)

> **Example 1 ($A=1.5$: moderate asymmetry — rise 1.5× steeper than fall)**

Step-by-step substitution (everything dimensionless; only the corner carries Hz):

$$
\begin{aligned}
\Gamma_{rms}^2&=\frac{2\pi^2}{3}\cdot\frac{1}{125}\cdot\left[4\cdot\frac{1+3.375}{(2.5)^3}\right]
=6.5797\times0.008\times1.12=0.05895
\;\Rightarrow\;\Gamma_{rms}=0.2428 \\[4pt]
\Gamma_{dc}&=\frac{2\pi}{25}\cdot\frac{1-1.5}{1+1.5}=0.25133\times(-0.2)=-0.05027
\;\Rightarrow\;c_0=2\Gamma_{dc}=-0.1005 \\[4pt]
f_{1/f^3}&=1\ \text{MHz}\times\frac{3}{2\times1\times5}\times\frac{(-0.5)^2}{1-1.5+2.25}
=1\ \text{MHz}\times0.3\times\frac{0.25}{1.75}=42.9\ \text{kHz}.
\end{aligned}
$$

- **Result**: $\Gamma_{rms}=0.2428$, $c_0=-0.1005$, corner $=42.86$ kHz ([P2] Eq.(57) convention);
  the [P1] Eq.(24) convention gives $85.71$ kHz ($=2\times$, flag as above).
- **Dimension check**: $[\text{Hz}]\times[\text{dimensionless}]\times[\text{dimensionless}]=[\text{Hz}]$ ✓.
- **Feel for the numbers**: the $N=5$ ring's $\Gamma_{rms}\approx0.24$ is about half of this site's
  representative $\Gamma_{rms}=0.5$. Plugging into canonical Example B ($q_{max}=1$ pC,
  $S_i=10^{-24}$ A²/Hz, $f_0=5$ GHz, $\Delta f=1$ MHz): $\mathcal{L}$ sits
  $20\log_{10}(0.2428/0.5)=-6.3$ dB below $-148.0$ dBc/Hz → about $-154.3$ dBc/Hz
  (SSB $/4$ convention; the time-domain $/2$ convention lifts the whole curve $+3$ dB → about
  $-151.3$ dBc/Hz).
- **One-line Python check** (closed forms directly; full verification in lab_33):

```python
import numpy as np
N, A, eta, f1f = 5, 1.5, 1.0, 1e6
grms2 = (2*np.pi**2/(3*eta**3))/N**3 * 4*(1+A**3)/(1+A)**3
gdc = (2*np.pi/eta**2)/N**2 * (1-A)/(1+A)
print(round(np.sqrt(grms2), 4), round(2*gdc, 4))
# -> 0.2428 -0.1005 (Γrms and c0=2Γdc; same values as lab_33)
print(round(f1f*3/(2*eta*N)*(1-A)**2/(1-A+A**2)/1e3, 2), "kHz")
# -> 42.86 kHz ([P2] Eq.(57); [P1] Eq.(24) convention = 85.71 kHz)
```

> **Example 2 ($A=3$: heavy asymmetry — rise 3× steeper than fall)**

$$
\begin{aligned}
\Gamma_{rms}^2&=6.5797\times0.008\times\left[4\cdot\frac{28}{64}\right]
=6.5797\times0.008\times1.75=0.09212\;\Rightarrow\;\Gamma_{rms}=0.3035 \\[4pt]
c_0&=2\times\frac{2\pi}{25}\times\frac{1-3}{1+3}=-0.2513 \\[4pt]
f_{1/f^3}&=1\ \text{MHz}\times0.3\times\frac{4}{7}=171.4\ \text{kHz}
\qquad(\text{[P1] Eq.(24) convention: }342.9\ \text{kHz}).
\end{aligned}
$$

- **Versus Example 1**: as $A$ worsens from 1.5 to 3, $\Gamma_{rms}$ only rises from 0.2428 to 0.3035
  (+25%, minor damage in the 1/f² region), but $c_0$ goes from $-0.1005$ to $-0.2513$ ($\times2.5$) and
  the corner jumps from 42.86 kHz to 171.43 kHz (**$\times4.0$, printed by lab_33**; the ratio is
  convention-free because the factor 2 multiplies and divides out). The height of the 1/f³ skirt
  $\propto c_0^2$ rises by $10\log_{10}(2.5^2)=+8.0$ dB.
- **Versus the assumed example on [symmetry](/06_design_insights/symmetry)**: that page's illustrative
  $c_0=0.4$, $\Gamma_{rms}=0.5$ give a 320 kHz corner ([P1] Eq.(24) convention); this page computes the
  same quantity directly from $(N,A)$, with no assumed $c_0$ needed.

<NumericQuiz
  prompt="Same ring with N = 5, η = 1, device 1/f corner f₁/f = 1 MHz. The waveform asymmetry ratio worsens from A = 1.5 to A = 3. By what factor does the 1/f³ corner grow? (Hint: this ratio is independent of the [P1]/[P2] factor-2 convention)"
  answer={4}
  tol={0.02}
  unit="×"
  hint="Only (1−A)²/(1−A+A²) in Eq.(57) depends on A: A=1.5 gives 0.25/1.75 = 1/7, A=3 gives 4/7."
  solutionNote="The corner goes from 42.86 kHz → 171.43 kHz, ratio = (4/7)/(1/7) = 4.0 (printed by lab_33). Under the [P1] Eq.(24) convention both numbers double (85.71 → 342.86 kHz) and the ratio is still 4 — the convention factor cancels in the ratio."
/>

## Simulation verification: lab_33 (closed forms vs numeric integration)

`simulations/lab_33_asymmetry_corner.py` (runtime about 1.5 s) builds the piecewise triangular
$\Gamma(x)$ of Fig. 18 numerically on an $(N,A)$ grid ($4\times10^5$ points/period) and triple-checks
Eq.(55)/(56): numeric trapezoid integration, the $a_0$ of `compute_fourier_coefficients`
($=c_0=2\Gamma_{dc}$), and pure algebra (Eq.(52)+(54) combined = Eq.(55)).

| Parameter | Value | Unit |
|---|---|---|
| $N$ grid | 3, 4, 5, 7, 9, 12, 15 | — |
| $A$ grid | 1.0, 1.25, 1.5, 2.0, 3.0, 4.0 | — |
| $\eta$ | 1.0 | — |
| $f_{1/f}$ | 1 | MHz |
| $\theta$ sampling | 400001 points / $2\pi$ | — |

Core verification code (excerpt; `gamma_fig18` assembles $\Gamma$ from two unit-slope triangular lobes):

```python
g = gamma_fig18(theta, n_st, a_r)            # Fig.18 piecewise triangle (unit slopes)
g2_num  = gamma_rms(theta, g)**2             # numeric (1/2π)∫Γ²dx
gdc_num = np.trapezoid(g, theta) / (2*np.pi) # numeric (1/2π)∫Γdx
a0, *_  = compute_fourier_coefficients(theta, g, 2)   # a0 = c0
# all 42 (N,A) cases compared against Eq.(55)/(56):
# -> 1.17e-09 (max relative error, Γrms², far below the 0.5% gate)
# -> 1.60e-09 (max relative error, Γdc and c0=2Γdc, both identical)
```

![Asymmetric triangular ISF: Fig.18 geometry, V-shaped corner-vs-A valley, 1/N corner-vs-N law](/figures/asymmetry_corner.png)

**How to read the figure**:

- **(a)** $\Gamma(x)$ for $N=5$, three curves $A=1/1.5/3$. Larger $A$ makes the positive lobe shorter
  and narrower and the negative lobe taller and wider (the total phase budget $2\pi/(\eta N)$ is fixed
  and split $1:A$); the dotted lines are the respective $\Gamma_{dc}$ (Eq.56) — asymmetry pulls the
  ISF's average away from 0, and that offset is the gate for flicker upconversion.
- **(b)** The Eq.(57) corner vs $A$ (log axis): the symmetry point $A=1$ is the bottom of a V-shaped
  valley (corner → 0), mirror-symmetric under $A\to1/A$; larger $N$ lowers the whole curve. This is the
  analytic version of the measured bowl in [P2] Fig. 17. Annotated points: at $N=5$,
  $A=1.5\to42.9$ kHz, $A=3\to171.4$ kHz.
- **(c)** Corner vs $N$ at fixed $A$ (log-log): slope $-1$ (coincides with the dashed $\propto1/N$
  guide; lab_33 prints, at $A=1.5$, $N=3/5/9/15\to71.43/42.86/23.81/14.29$ kHz, and the $N{=}3$ to
  $N{=}15$ ratio is exactly 5.0 = 15/3). **Rings with fewer stages have a higher flicker corner** —
  put this into the trade-off when choosing $N$.

## Validity and failure conditions

| Assumption | Holds when | Fails when |
|---|---|---|
| Triangular ISF (linear-ramp transitions, peak $=1/f'$, width $=2/f'$, unit slopes) | large $N$, edges occupy a small fraction of the period, near-trapezoidal waveform | small $N$ or near-sinusoidal waveform: the equation-level $N=3$ ring of [lab_32](/04_simulation_labs/lab_32_mos_level1_ring) measures $\Gamma_{rms}=0.9303$ while Eq.(16) gives 0.4937 — nearly 2× off; the closed forms then serve only as scaling guides |
| Lobes do not overlap | total lobe width $4\pi/(\eta N)\le2\pi$, i.e. $N\ge2/\eta$ | $N$ too small (the approximation is already broken there) |
| $\eta\approx1$ (the stage-delay proportionality constant of [P2] Eq.(14)) | typical inverter stages | for $\eta$ away from 1 the formulas still hold, but use the actual $\eta$ ($\Gamma_{rms}^2\propto\eta^{-3}$, corner $\propto\eta^{-1}$) |
| Flicker upconverts only via $\Gamma_{dc}$ ($c_0$) | bare-ISF asymmetry dominates | if the cyclostationary NMF $\alpha(t)$ is itself asymmetric, look at the $c_0$ of the **effective ISF** (see [effective_isf](/03_isf_core_theory/effective_isf), [device_noise_mapping](/06_design_insights/device_noise_mapping)) — upconversion can survive even at $A=1$ |
| Corner bookkeeping convention | [P2] Eq.(7)/(57) self-consistent | differs by 2× from [P1] Eq.(24) (with $c_0=2\Gamma_{dc}$ substituted); always state which convention a quoted number uses |
| $A=1\Rightarrow$ corner $\to0$ | exact within the model | in real circuits the residual $c_0$ is set by duty cycle, even harmonics, $\alpha(t)$ and process offsets; the corner never truly reaches 0 |

## Mapping to the papers

| This page | Paper source | Verification status |
|---|---|---|
| Asymmetric triangular ISF geometry (lobes of height $1/f'$, width $2/f'$) | [P2] Fig. 18, p.803 | ✓ rendered this unit |
| Piecewise integration of $\Gamma_{rms}^2$ | [P2] Eq.(52), p.803 | ✓ rendered this unit |
| Asymmetry ratio $A\equiv f'_{rise}/f'_{fall}$ | [P2] Eq.(53), p.803 | ✓ rendered this unit |
| Period constraint $2\pi=\eta N(1/f'_{rise}+1/f'_{fall})$ | [P2] Eq.(54), p.803 | ✓ rendered this unit |
| Closed-form $\Gamma_{rms}^2(N,A)$ | [P2] Eq.(55), p.803 | ✓ rendered this unit |
| Closed-form $\Gamma_{dc}(N,A)$ | [P2] Eq.(56), p.803 | ✓ rendered this unit |
| Closed-form corner $\propto(1-A)^2/(1-A+A^2)$, $\propto1/N$ | [P2] Eq.(57), p.803 | ✓ rendered this unit |
| Corner relation $f_{1/f^3}=f_{1/f}\Gamma_{dc}^2/\Gamma_{rms}^2$ | [P2] Eq.(7), p.792 | ✓ rendered this unit |
| Symmetric special case (bracket $=1$) | [P2] Eq.(16), p.794 | ✓ existing v7 verification |
| $c_0$-form corner ($=2\times$ Eq.(7), convention flag) | [P1] Eq.(24), p.185 | ✓ authoritative formula table |
| Measured bowl at the symmetry point | [P2] Fig. 17, p.802 | ✓ existing verification |

## What to remember

- [P2] App. B models the ring ISF as **two unit-slope triangular lobes** (height $1/f'$, width $2/f'$);
  piecewise integration gives $\Gamma_{rms}^2=\frac{1}{3\pi}(1/f'_{rise})^3(1+A^3)$ (Eq.52).
- The period constraint $2\pi=\eta N(1+A)/f'_{rise}$ (Eq.54) converts slope into $(N,A)$, giving
  $\Gamma_{rms}^2=\frac{2\pi^2}{3\eta^3N^3}[4(1+A^3)/(1+A)^3]$ (Eq.55); at $A=1$ the bracket $=1$ and
  it reduces exactly to Eq.(16).
- $\Gamma_{dc}=\frac{2\pi}{\eta^2N^2}\frac{1-A}{1+A}$ (Eq.56), $c_0=2\Gamma_{dc}$;
  $\Gamma_{dc}\propto N^{-2}$ falls faster than $\Gamma_{rms}$ → corner $\propto1/N$.
- Corner $=f_{1/f}\cdot\frac{3}{2\eta N}\cdot\frac{(1-A)^2}{1-A+A^2}$ (Eq.57): vanishes quadratically
  at the symmetry point, symmetric under $A\to1/A$, and higher for fewer stages ([P2]'s own sentence).
- **Convention flag**: [P1] Eq.(24) (with $c_0=2\Gamma_{dc}$) $=2\times$ [P2] Eq.(7)/(57);
  ratios and scalings are unaffected.
- Numeric feel ($N=5$, $\eta=1$, $f_{1/f}=1$ MHz): $A=1.5\to c_0=-0.1005$, corner 42.86 kHz;
  $A=3\to c_0=-0.2513$, corner 171.43 kHz (ratio 4.0).
- Model-failure warning: for small $N$ / near-sinusoidal waveforms the triangular approximation is far
  off (lab_32 measures nearly 2× deviation); with asymmetric cyclostationary $\alpha$, look at the
  effective ISF's $c_0$.

## Further reading

- Design-facing application and knobs: [symmetry](/06_design_insights/symmetry) (the "user manual" for these closed forms)
- Why $c_0$ is the only gate for flicker: [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)
- $c_0,c_n$ and Parseval: [fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf)
- Where $\Gamma_{rms}$ enters phase noise: [rms_isf](/03_isf_core_theory/rms_isf), [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) (full story of the $/4$ vs $/2$ convention)
- Where the triangular approximation breaks: [lab_32](/04_simulation_labs/lab_32_mos_level1_ring) (equation-level ring ISF extraction)
- Ring vs LC topology trade-offs: [lc_vs_ring](/06_design_insights/lc_vs_ring), [paper_002 deep dive](/05_paper_deep_dives/paper_002_jitter_phase_noise_ring)
