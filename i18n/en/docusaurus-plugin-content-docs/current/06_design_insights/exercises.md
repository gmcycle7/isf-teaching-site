---
title: Design Chapter Exercises (with Full Solutions)
description: Complete exercise set for the design chapter — q_max/Γrms design back-calculation, symmetry design back-calculation, ring vs LC comparison, PLL optimal loop BW, σt→BER, tail-noise countermeasures. Every problem comes with a step-by-step solution, units and a dimension check, a numerical answer, and a one-line Python verification.
---

> **β**: This English translation is in beta — the Traditional-Chinese original is the authoritative version.

import NumericQuiz from "@site/src/components/NumericQuiz";

# Design Chapter Exercises (with Full Solutions)

> **Prerequisites**: [tank_swing](/06_design_insights/tank_swing), [symmetry](/06_design_insights/symmetry), [lc_vs_ring](/06_design_insights/lc_vs_ring), [pll_noise_budget](/06_design_insights/pll_noise_budget), [serdes_clocking_connection](/06_design_insights/serdes_clocking_connection) (every problem on this page uses the ISF formulas from these pages) | **Other exercise sets**: [02 Foundations chapter exercises](/02_foundations/exercises), [03 ISF core-theory chapter exercises](/03_isf_core_theory/exercises)

This page is the complete exercise set for **Chapter 06, Design Insights**. The focus is on **design back-calculation problems** (given a target spec, solve for the knob)
and **comparison/trade-off problems** (ring vs LC, loop-BW trade-off, tail-noise countermeasures), all answered with the ISF formulas.

> **Format**: every solution = **step-by-step substitution (with units) → result → dimension check → one-line Python verification**.
> Python imports from `simulations/common/` (including `pll_utils`, `serdes_utils`, `isf_utils`, `noise_utils`).

Authoritative formulas involved (verified verbatim from the spec, with citations):

- The signature white-noise 1/f² result: $\mathcal{L}\{\Delta\omega\}=10\log_{10}\!\left(\dfrac{\Gamma_{rms}^2}{q_{max}^2}\cdot\dfrac{\overline{i_n^2}/\Delta f}{4\,\Delta\omega^2}\right)$ ([P1] Eq.(21), p.185)
- 1/f³ corner: $\Delta\omega_{1/f^3}=\omega_{1/f}\cdot\dfrac{c_0^2}{2\,\Gamma_{rms}^2}$ ([P1] Eq.(24), p.185)
- ring $\Gamma_{rms}\propto N^{-3/2}$ ([P2] Eq.(16), p.794; re-verified in v7: the square root covers only the constant, $\Gamma_{rms}\propto N^{-3/2}$; triple-checked against the body text's 4/N^{1.5}@η=0.75 and App. B Eq.(55). v3 had misread this as $N^{-3/4}$); ring frequency $f_0=\dfrac{1}{2N\tau_D}$ ([P2] Eq.(15), p.794)
- PLL output: $S_{out}=S_{ref}\lvert H_{lp}\rvert^2+S_{vco}\lvert H_{hp}\rvert^2$, see spec Section 10.2 for $\lvert H_{lp}\rvert^2,\lvert H_{hp}\rvert^2$
- SerDes BER (RJ): $\text{BER}(t)=\tfrac12\big[Q(\tfrac{UI/2-t}{\sigma_t})+Q(\tfrac{UI/2+t}{\sigma_t})\big]$, $Q(x)=\tfrac12\,\mathrm{erfc}(x/\sqrt2)$ (spec Section 10.2)
- rms jitter: $\sigma_t=\dfrac{1}{2\pi f_0}\sqrt{\int S_\phi df}$ (spec formula 19)

---

## Problems

### Exercise 1 (design back-calculation) — $q_{max}$, $\Gamma_{rms}$ target combinations

A 5 GHz LC oscillator currently has $\mathcal{L}(1\,\text{MHz})=-140$ dBc/Hz (using Eq.(21), with $\Gamma_{rms}=0.7$,
$q_{max}=1$ pC, $S_i=3.2\times10^{-24}\ \text{A}^2/\text{Hz}$, which self-consistently gives $-140$ when substituted into Eq.(21)). The target is to push it down another 9 dB, to $-149$ dBc/Hz.
List two ways to hit the target: (a) change only $q_{max}$; (b) change only $\Gamma_{rms}$. How much change is needed in each case?

<NumericQuiz
  prompt="Work out (a) yourself first: changing only q_max to drop 9 dB, what q_max is needed? (original q_max = 1 pC; answer in pC)"
  answer={2.82}
  unit="pC"
  hint="L_lin ∝ 1/q_max² → a 9 dB drop needs q_max scaled up by 10^(9/20)."
  solutionNote="10^0.45 ≈ 2.818 → q_max ≈ 2.82 pC ((b) instead pushes Γ_rms down to ≈0.248). See the Exercise 1 solution below."
/>

### Exercise 2 (design back-calculation) — using symmetry to suppress the $1/f^3$ corner

A ring oscillator has $\Gamma_{rms}=0.9$, $c_0=0.3$, device $f_{1/f}=2$ MHz.
(a) Use [P1] Eq.(24) (the exact form $\Delta\omega_{1/f^3}=\omega_{1/f}c_0^2/(2\Gamma_{rms}^2)$) to find the $1/f^3$ corner $\Delta f_{1/f^3}$.
(b) If rise/fall symmetrization pushes $c_0$ down to $0.05$, what does the corner become? To achieve corner < 1 kHz, what is the maximum allowed $c_0$?

<NumericQuiz
  prompt="Try (a) yourself first: Δf_1/f³ = ? (Γ_rms=0.9, c₀=0.3, f_1/f=2 MHz; answer in kHz)"
  answer={111.1}
  tol={0.02}
  unit="kHz"
  hint="Exact form: Δf_1/f³ = f_1/f · c0²/(2·Γ_rms²)."
  solutionNote="Δf_1/f³ = 2×10⁶×0.09/1.62 ≈ 1.111×10⁵ Hz = 111.1 kHz. Details in the Exercise 2 solution below."
/>

### Exercise 3 (comparison) — $\Gamma_{rms}$ scaling for ring vs LC

(a) Using the [P2] Eq.(16) scaling $\Gamma_{rms}\propto N^{-3/2}$, if the ring stage count is increased from $N=5$ to $N=15$,
by what factor does $\Gamma_{rms}$ drop? How much does phase noise ($\propto\Gamma_{rms}^2$) improve, in dB?
(b) In one sentence, explain why LC is usually still cleaner than ring (in terms of the two knobs $\Gamma_{rms}$ and $q_{max}$).

<NumericQuiz
  prompt="Try (a) yourself first: going from N=5 to N=15, how much does phase noise improve, in dB? (Γ_rms ∝ N⁻¹·⁵; answer in dB, include the sign)"
  answer={-14.31}
  tol={0.01}
  unit="dB"
  hint="Γ_rms ratio = (15/5)^(-1.5); phase noise ∝ Γ_rms², improvement = 10·log₁₀(ratio²)."
  solutionNote="ratio = 3^(-1.5) ≈ 0.1925 → 10·log₁₀(0.1925²) ≈ −14.31 dB. Details in the Exercise 3 solution below."
/>

### Exercise 4 (design) — PLL optimal loop BW (intuition + numerical)

A ring VCO has poor intrinsic $1/f^2$ phase noise ($S_{vco}=K_v/f^2$, $K_v=10^{2}\ \text{rad}^2\text{Hz}$),
while the reference is very clean and white ($S_{ref}=K_r=10^{-14}\ \text{rad}^2/\text{Hz}$, divide ratio $N=1$).
Using the type-II 2nd-order transfer functions from spec Section 10.2, sweep the loop natural frequency $f_n$ to find the $f_n$
that minimizes the integrated output jitter ($\int S_{out}df$, integrated from 1 kHz to 100 MHz). Where would you intuitively expect $f_n$ to land?

### Exercise 5 (numerical) — $\sigma_t\to$ BER bathtub

A 25 Gb/s SerDes has UI $=1/25\text{G}=40$ ps, and the sampling clock has RJ $\sigma_t=1.2$ ps (Gaussian).
Find (a) the BER when sampling at the eye center ($t=0$); (b) the timing margin (how far the sampling point may deviate from center) to achieve $\text{BER}=10^{-12}$.

### Exercise 6 (design back-calculation) — back-calculating the allowed $\sigma_t$ from a BER budget

Same SerDes as above (UI $=40$ ps); the spec requires $\text{BER}\le10^{-15}$ when sampling at center. Find the maximum allowed RJ $\sigma_t$ (ps).
(Hint: $\text{BER}\approx Q(\tfrac{UI/2}{\sigma_t})$, and $Q^{-1}(10^{-15})\approx7.94$.)

<NumericQuiz
  prompt="Work it out yourself first: the maximum σ_t allowed for BER ≤ 10⁻¹⁵ = ? (UI = 40 ps, Q⁻¹(10⁻¹⁵) ≈ 7.94; answer in ps)"
  answer={2.52}
  unit="ps"
  hint="σ_t,max = (UI/2)/Q⁻¹(10⁻¹⁵) = 20 ps ÷ 7.94."
  solutionNote="σ_t,max ≈ 2.519 ps, i.e. UI ≥ 15.9 σ_t. See the Exercise 6 solution below."
/>

### Exercise 7 (countermeasures) — tail-noise countermeasures (cross-coupled LC VCO)

In a cross-coupled LC VCO, tail current-source noise is upconverted by $2\times$ (landing near $2\omega_0$), then
folded back close-in via the ISF's $c_2$ component and its DC component $c_0$. Using the viewpoint that "the effective ISF's $c_0,c_2$
are what make tail noise a problem," list three design measures for reducing the tail-noise contribution, and for each, explain why it works using one ISF quantity ($c_0$, $c_2$,
$\Gamma_{eff,rms}$, $q_{max}$). This problem is explicitly marked as illustrative.

### Exercise 8 (design back-calculation) — allocating a jitter budget across PLL bands

A clock has a total rms jitter budget of $\sigma_{t,\text{tot}}=300$ fs ($f_0=10$ GHz). The near-carrier (ref/in-band)
contribution is known to be $\sigma_{t,\text{ref}}=180$ fs. RJ sources are uncorrelated (variances add). What is the maximum
jitter budget $\sigma_{t,\text{vco}}$ (fs) left for the VCO (out-of-band)? What is the corresponding phase variance $\sigma_{\phi,\text{vco}}^2$ (rad²)?

<NumericQuiz
  prompt="Work it out yourself first: σ_t,vco = ? (total budget 300 fs, ref accounts for 180 fs, sources uncorrelated; answer in fs)"
  answer={240}
  unit="fs"
  hint="RJ uncorrelated → variances add: σ_vco = √(300² − 180²) fs (not 300 − 180)."
  solutionNote="√(90000 − 32400) = √57600 = 240 fs (a 3-4-5 right triangle). Corresponding σ_φ² ≈ 2.27×10⁻⁴ rad². See the Exercise 8 solution below."
/>

---

## Solutions in full

<details>
<summary><strong>Exercise 1 solution</strong> ($q_{max}$, $\Gamma_{rms}$ target combinations)</summary>

**Design back-calculation strategy.** Inside Eq.(21), $\mathcal{L}_{\text{lin}}\propto\Gamma_{rms}^2/q_{max}^2$. To drop 9 dB, the
linear value must drop by $10^{0.9}=7.94\times$.

**(a) Change only $q_{max}$** ($\mathcal{L}_{\text{lin}}\propto1/q_{max}^2$):

$$
\frac{q_{max,\text{new}}}{q_{max,\text{old}}}=10^{9/20}=10^{0.45}=2.818\quad\Longrightarrow\quad q_{max,\text{new}}\approx2.82\ \text{pC}.
$$

**(b) Change only $\Gamma_{rms}$** ($\mathcal{L}_{\text{lin}}\propto\Gamma_{rms}^2$):

$$
\frac{\Gamma_{rms,\text{new}}}{\Gamma_{rms,\text{old}}}=10^{-9/20}=10^{-0.45}=0.3548\quad\Longrightarrow\quad\Gamma_{rms,\text{new}}\approx0.7\times0.3548=0.248.
$$

**Result**: (a) $q_{max}$ scaled up $\approx2.82\times$ to $\approx2.82$ pC; (b) $\Gamma_{rms}$ pushed down to $\approx0.248$
(about 1/2.82 of the original). Both give the same effect (each $-9$ dB), but the cost differs: increasing $q_{max}$ requires larger swing/power,
while pushing down $\Gamma_{rms}$ requires improving waveform symmetry and noise-injection timing (see [waveform_slope](/06_design_insights/waveform_slope)).

**Consistency check**: $\mathcal{L}\propto\Gamma_{rms}^2/q_{max}^2$, 9 dB $=10\log_{10}(7.94)$, $\sqrt{7.94}=2.818$ ✓.

**Dimension check**: both ratios are dimensionless (same physical quantity divided by itself); $q_{max}$ remains in C, $\Gamma_{rms}$ remains dimensionless ✓.

```python
import numpy as np
g = 10**(9/10)                     # linear factor for 9 dB
print("qmax x", round(np.sqrt(g),3), "; Gamma_rms x", round(1/np.sqrt(g),3))
# -> qmax x 2.818 ; Gamma_rms x 0.355
print("new qmax", round(1.0*np.sqrt(g),2), "pC ; new Grms", round(0.7/np.sqrt(g),3))
# -> 2.82 pC ; 0.248
```

</details>

<details>
<summary><strong>Exercise 2 solution</strong> (using symmetry to suppress the $1/f^3$ corner)</summary>

**(a) Exact formula.** [P1] Eq.(24): $\Delta\omega_{1/f^3}=\omega_{1/f}\dfrac{c_0^2}{2\Gamma_{rms}^2}$.
Converting to $\Delta f$ (the $2\pi$ cancels since $\omega_{1/f}=2\pi f_{1/f}$): $\Delta f_{1/f^3}=f_{1/f}\dfrac{c_0^2}{2\Gamma_{rms}^2}$.

$$
\Delta f_{1/f^3}=2\times10^6\times\frac{0.3^2}{2\times0.9^2}=2\times10^6\times\frac{0.09}{1.62}=2\times10^6\times0.05556=1.111\times10^{5}\ \text{Hz}\approx111\ \text{kHz}.
$$

**(b) Symmetrizing to $c_0\to0.05$.**

$$
\Delta f_{1/f^3}=2\times10^6\times\frac{0.05^2}{1.62}=2\times10^6\times1.543\times10^{-3}=3086\ \text{Hz}\approx3.09\ \text{kHz}.
$$

**Upper bound on $c_0$ to reach corner < 1 kHz**: require $f_{1/f}\dfrac{c_0^2}{2\Gamma_{rms}^2}<10^3$:

$$
c_0^2<\frac{10^3\times2\times0.81}{2\times10^6}=\frac{1620}{2\times10^6}=8.1\times10^{-4}\quad\Longrightarrow\quad c_0<0.0285.
$$

**Result**: (a) $\approx111$ kHz; (b) after pushing $c_0$ to 0.05, $\approx3.09$ kHz; to achieve corner < 1 kHz requires $c_0<0.0285$.

**Design takeaway**: the $1/f^3$ corner $\propto c_0^2$, so **waveform symmetry (suppressing $c_0$) is the most effective knob for suppressing close-in flicker
upconversion** (see [symmetry](/06_design_insights/symmetry)). $c_0$ arises from rise/fall asymmetry and
duty-cycle deviation.

**Dimension check**: $(c_0/\Gamma_{rms})^2$ is dimensionless, $\times\ f_{1/f}$ (Hz) $=$ Hz ✓.

```python
import numpy as np
def corner(c0, Grms=0.9, f1f=2e6): return f1f*c0**2/(2*Grms**2)
print(corner(0.3), "Hz ;", corner(0.05), "Hz")           # -> 111111 ; 3086
c0_max = np.sqrt(1e3*2*0.9**2/2e6)
print("c0 <", round(c0_max,4))                            # -> 0.0285
```

</details>

<details>
<summary><strong>Exercise 3 solution</strong> ($\Gamma_{rms}$ scaling for ring vs LC)</summary>

**(a) Scaling.** [P2] Eq.(16) (re-verified in v7: the square root covers only the constant, $\Gamma_{rms}\propto N^{-3/2}$; triple-checked against the body text's
4/N^{1.5}@η=0.75 and App. B Eq.(55). v3 had misread this as $N^{-3/4}$): $N:5\to15$ ($\times3$):

$$
\frac{\Gamma_{rms}(15)}{\Gamma_{rms}(5)}=\left(\frac{15}{5}\right)^{-3/2}=3^{-1.5}=0.1925.
$$

Phase noise $\propto\Gamma_{rms}^2$, so the improvement is:

$$
\Delta\mathcal{L}=10\log_{10}\big(0.1925^2\big)=10\log_{10}(0.03704)=-14.31\ \text{dB}.
$$

**(b) Why LC stays cleaner.** Both knobs favor LC:
- **$\Gamma_{rms}$**: the LC waveform is a smooth sinusoid ($\Gamma=-\sin$, $\Gamma_{rms}=0.707$, low sensitivity spread out evenly);
  the ring's ISF is concentrated at the transition (steep edge), giving higher rms and concentrating energy at the most sensitive point.
- **$q_{max}$**: the LC tank's high $Q$ permits a large voltage swing → large $q_{max}=C V_{max}$; each ring stage has swing limited by
  $V_{DD}$ and small capacitance, so $q_{max}$ is usually much smaller. Since $\mathcal{L}\propto\Gamma_{rms}^2/q_{max}^2$,
  LC wins on both ends — smaller numerator, larger denominator.

**Result**: (a) $N:5\to15$ drops $\Gamma_{rms}$ by $\approx0.19\times$ and improves phase noise by $\approx14.3$ dB;
(b) LC beats ring on both knobs — $\Gamma_{rms}$ (small and spread out) and $q_{max}$ (high Q, large swing).

**Note**: increasing $N$ simultaneously lowers frequency ($f_0=1/(2N\tau_D)$) and raises power; ring's real appeal is area/tunability/no inductor,
not low phase noise. See [lc_vs_ring](/06_design_insights/lc_vs_ring).

**Dimension check**: $N$ is dimensionless, $\Gamma_{rms}$ is dimensionless; the ratio and the dB value are both dimensionless ✓.

```python
import numpy as np
ratio = (15/5)**(-1.5)
print("Grms ratio", round(ratio,4), "; dPN", round(10*np.log10(ratio**2),2), "dB")
# -> Grms ratio 0.1925 ; dPN -14.31 dB
```

</details>

<details>
<summary><strong>Exercise 4 solution</strong> (PLL optimal loop BW)</summary>

**Intuition.** The PLL **low-pass filters the ref and high-pass filters the VCO** (spec Section 10.2).
- If loop BW $f_n$ is **too small** → the VCO's close-in $1/f^2$ noise isn't suppressed by the loop, so in-band noise is dominated by the VCO → large jitter.
- If loop BW $f_n$ is **too large** → a large amount of ref noise (and CP noise) is let through, and the VCO high-pass corner is pushed too high,
  so out-of-band VCO noise is also large → large jitter.
- The **optimal $f_n^\*$** sits near the **crossover point** of the "rising ref+CP curve" and the "falling VCO curve" — where the two shaped
  curves intersect near $f_n$, minimizing the total integrated area.

**Numerical (sweeping $f_n$).** Using `shape_output_phase_noise` and trapezoidal integration, sweep $f_n=10^4\to10^7$ Hz,
and find the one minimizing $\int S_{out}df$ (1 kHz→100 MHz):

**Result**: the optimal $f_n^\*\approx$ a few hundred kHz to ~1 MHz (near the crossover of the ref white-floor curve and the VCO $1/f^2$ curve).
For this problem's parameters, the grid sweep gives $f_n^\*\approx3\times10^5$ Hz order of magnitude (shifts with $S_{ref},K_v$).
**This is the core trade-off in PLL noise budgeting: loop BW is neither best maximized nor minimized — an optimum exists.**

**Dimension check**: $S_{out}$ is in rad²/Hz, $\int S_{out}df$ is in rad² (phase variance);
$\sigma_t=\sqrt{\cdot}/(2\pi f_0)$ is in s ✓.

```python
import numpy as np
from simulations.common.pll_utils import shape_output_phase_noise
f = np.logspace(3, 8, 4000)
S_ref = np.full_like(f, 1e-9)           # white-floor reference (tuned so the optimal BW falls within the sweep range)
S_vco = 1e2 / f**2                       # VCO 1/f^2
fn_grid = np.logspace(4, 7, 60)
var = []
for fn in fn_grid:
    S_out, _, _ = shape_output_phase_noise(f, S_ref, S_vco, fn_hz=fn)
    var.append(np.trapezoid(S_out, f))       # rad^2
fn_opt = fn_grid[int(np.argmin(var))]
print("optimal f_n ~", f"{fn_opt:.2e}", "Hz")   # -> ~1.9e5 Hz (order 10^5; slightly below 10/√S_ref≈3e5 due to non-ideal brick-wall rolloff)
```

(See [pll_noise_budget](/06_design_insights/pll_noise_budget) for the full plot.)

</details>

<details>
<summary><strong>Exercise 5 solution</strong> ($\sigma_t\to$ BER bathtub)</summary>

**(a) Center-sampled BER ($t=0$).** In the spec Section 10.2 RJ bathtub, at $t=0$ the two $Q$ terms are equal:

$$
\text{BER}(0)=\tfrac12\big[Q(\tfrac{UI/2}{\sigma_t})+Q(\tfrac{UI/2}{\sigma_t})\big]=Q\!\left(\frac{UI/2}{\sigma_t}\right)=Q\!\left(\frac{20\ \text{ps}}{1.2\ \text{ps}}\right)=Q(16.67).
$$

$Q(16.67)$ is astronomically small ($\sim10^{-62}$) — a center-sampled error is essentially impossible.

**(b) Margin for $\text{BER}=10^{-12}$.** Solve $Q\!\left(\dfrac{UI/2-t}{\sigma_t}\right)=10^{-12}$ (single-sided term dominates).
$Q^{-1}(10^{-12})\approx7.03$, so

$$
\frac{UI/2-t}{\sigma_t}=7.03\quad\Longrightarrow\quad t=\frac{UI}{2}-7.03\,\sigma_t=20-7.03\times1.2=20-8.44=11.56\ \text{ps}.
$$

I.e. the sampling point can deviate $\pm11.56$ ps from center while still meeting $\text{BER}\le10^{-12}$; the **eye opening (@$10^{-12}$) $\approx2\times11.56=23.1$ ps**
(58% of UI).

**Result**: (a) $\text{BER}(0)\approx Q(16.67)\sim10^{-62}$ (center is extremely safe); (b) $10^{-12}$ margin $\pm11.56$ ps,
eye opening $\approx23$ ps.

**Dimension check**: the argument of $Q$, $\dfrac{\text{ps}}{\text{ps}}$, is dimensionless ✓; margin units are ps ✓.

```python
import numpy as np
from scipy.special import erfcinv
from simulations.common.serdes_utils import Q, ber_bathtub
ui, sigma_t = 40e-12, 1.2e-12
print("BER(0) =", ber_bathtub(np.array([0.0]), sigma_t, ui)[0])      # ~1e-62
qinv = np.sqrt(2)*erfcinv(2*1e-12)                                    # Q^-1(1e-12) ~ 7.03
margin = ui/2 - qinv*sigma_t
print("margin", round(margin*1e12,2), "ps ; eye", round(2*margin*1e12,1), "ps")
# -> margin 11.56 ps ; eye 23.1 ps
```

</details>

<details>
<summary><strong>Exercise 6 solution</strong> (back-calculating the allowed $\sigma_t$ from a BER budget)</summary>

**Design back-calculation strategy.** Center-sampled $\text{BER}(0)=Q\!\left(\dfrac{UI/2}{\sigma_t}\right)$. Requiring $\le10^{-15}$
means $\dfrac{UI/2}{\sigma_t}\ge Q^{-1}(10^{-15})\approx7.94$. Solving for the upper bound on $\sigma_t$:

$$
\sigma_{t,\max}=\frac{UI/2}{Q^{-1}(10^{-15})}=\frac{20\ \text{ps}}{7.94}=2.519\ \text{ps}.
$$

**Result**: the maximum allowed RJ $\sigma_t\approx2.52$ ps (i.e. $UI/2$ must be $\ge7.94\sigma_t$, half of the common "$\approx16\,\sigma$ full opening"
rule: $UI\ge15.9\,\sigma_t$).

**Design takeaway**: the tighter the BER spec ($10^{-15}$ vs $10^{-12}$), the larger $Q^{-1}$ (7.94 vs 7.03), so the smaller the allowed jitter.
At 25 Gb/s, requiring $\sigma_t<2.5$ ps directly throws the spec back onto the clock source: use Eq.(19) to back-calculate the allowed
$\int S_\phi df$, then back to $\Gamma_{rms}/q_{max}$ (connect to [serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)).

**Dimension check**: $\dfrac{\text{ps}}{\text{dimensionless}}=\text{ps}$ ✓.

```python
import numpy as np
from scipy.special import erfcinv
ui = 40e-12
qinv = np.sqrt(2)*erfcinv(2*1e-15)        # Q^-1(1e-15) ~ 7.94
sigma_max = (ui/2)/qinv
print(round(sigma_max*1e12,3), "ps ; UI/sigma =", round(ui/sigma_max,1))
# -> 2.519 ps ; UI/sigma = 15.9
```

</details>

<details>
<summary><strong>Exercise 7 solution</strong> (tail-noise countermeasures, illustrative)</summary>

> **Marked illustrative**: the following cross-coupled LC VCO tail mechanism is a qualitative teaching model; the constants/specific $c_n$
> depend on topology, and rigorous values require transient/adjoint extraction (see [real_oscillator_topologies](/06_design_insights/real_oscillator_topologies)).

**Mechanism review.** The tail current source's low-frequency (including flicker) noise is upconverted by $2\times$ via the
differential-pair switching, landing near $2\omega_0$; it then folds back close-in via the effective ISF's $c_2$ (second harmonic) and its DC component $c_0$,
forming a $1/f^3$/$1/f^2$ skirt. So "tail-noise trouble" is primarily written into the ISF's $c_0$ and $c_2$.

**Three countermeasures (each paired with one ISF quantity):**

| Countermeasure | Why it works (ISF quantity) |
|---|---|
| **Tail filter (add a $2\omega_0$ notch/large capacitor at the tail)** | Directly blocks tail noise near $2\omega_0$ in the frequency domain → equivalently reduces the energy folded back by $c_2$, suppressing close-in $1/f^2$. |
| **Waveform symmetrization (balance upper/lower half-cycles, reduce rise/fall asymmetry)** | Suppresses the effective ISF's $c_0$; the $1/f^3$ corner $\propto c_0^2$ (Eq.(24)), so $c_0\downarrow$ directly pushes the flicker-upconversion corner away from the carrier. |
| **Increase tank swing / raise $q_{max}$** | $\mathcal{L}\propto\Gamma_{rms}^2/q_{max}^2$; $q_{max}\uparrow$ suppresses the contribution of every source (including the tail) together (claim C3). |

(A fourth measure as a supplement: use a device with lower noise and a lower $1/f$ corner for the tail, or use resistive degeneration to reduce tail $g_m$ noise —
equivalently reducing the $\overline{i_n^2}$ injected into $c_0,c_2$.)

**Result**: tail noise is best addressed with three combined measures — "**tail filter to block $2\omega_0$**," "**symmetrization to suppress $c_0$**," and "**increase $q_{max}$**";
the corresponding quantitative knobs are $c_2$ (folded-back energy), $c_0$ (the $1/f^3$ corner $\propto c_0^2$), and $q_{max}$ ($\mathcal{L}\propto1/q_{max}^2$).

**Python verification (quantifying the effect of "symmetrization to suppress $c_0$" on the corner):**

```python
import numpy as np
# Use Eq.(24) to quantify the benefit of symmetrizing to suppress c0 (f1f=2 MHz, Grms=0.9 toy values)
def f3_corner(c0, Grms=0.9, f1f=2e6): return f1f*c0**2/(2*Grms**2)
print("c0=0.3 ->", round(f3_corner(0.3)/1e3,1), "kHz ; c0=0.05 ->",
      round(f3_corner(0.05)/1e3,2), "kHz")
# -> c0=0.3 -> 111.1 kHz ; c0=0.05 -> 3.09 kHz  (symmetrization suppresses the corner by ~36x)
```

</details>

<details>
<summary><strong>Exercise 8 solution</strong> (allocating a jitter budget across PLL bands)</summary>

**Design back-calculation strategy.** RJ sources are uncorrelated → **variances (not rms values) add**:

$$
\sigma_{t,\text{tot}}^2=\sigma_{t,\text{ref}}^2+\sigma_{t,\text{vco}}^2\quad\Longrightarrow\quad\sigma_{t,\text{vco}}=\sqrt{\sigma_{t,\text{tot}}^2-\sigma_{t,\text{ref}}^2}.
$$

**Step-by-step substitution (with units).**

$$
\sigma_{t,\text{vco}}=\sqrt{(300\ \text{fs})^2-(180\ \text{fs})^2}=\sqrt{90000-32400}\ \text{fs}=\sqrt{57600}\ \text{fs}=240\ \text{fs}.
$$

**Corresponding phase variance** (using $\sigma_\phi=2\pi f_0\,\sigma_t$, spec formula 19 reversed):

$$
\sigma_{\phi,\text{vco}}=2\pi f_0\,\sigma_{t,\text{vco}}=2\pi\times10^{10}\times240\times10^{-15}=1.508\times10^{-2}\ \text{rad},
$$

$$
\sigma_{\phi,\text{vco}}^2=(1.508\times10^{-2})^2=2.274\times10^{-4}\ \text{rad}^2.
$$

**Result**: VCO budget $\sigma_{t,\text{vco}}=240$ fs; corresponding $\sigma_{\phi,\text{vco}}^2\approx2.27\times10^{-4}$ rad².

**Intuition**: because **variances add**, 180 fs + 240 fs (rms) combine to 300 fs (not 420 fs) — RJ budgets
must be allocated by sum of squares. This 240 fs is exactly the integrated jitter allowed for the PLL's out-of-band VCO segment, which feeds back
into loop BW and VCO spec (connects to Exercise 4's optimal BW, [pll_noise_budget](/06_design_insights/pll_noise_budget)).

**Dimension check**: $\sqrt{\text{fs}^2-\text{fs}^2}=\text{fs}$ ✓; $2\pi f_0\,\sigma_t$ is $\text{rad/s}\cdot\text{s}=\text{rad}$ ✓.

```python
import numpy as np
sigma_tot, sigma_ref, f0 = 300e-15, 180e-15, 10e9
sigma_vco = np.sqrt(sigma_tot**2 - sigma_ref**2)
sigma_phi = 2*np.pi*f0*sigma_vco
print(sigma_vco*1e15, "fs ;", sigma_phi**2, "rad^2")   # -> 240.0 fs ; 2.27e-4 rad^2
```

</details>

---

## Key takeaways

- **$q_{max}$/$\Gamma_{rms}$ back-calculation**: $\mathcal{L}\propto\Gamma_{rms}^2/q_{max}^2$; every 6 dB reduction needs $q_{max}\times2$ or $\Gamma_{rms}\div2$ (Exercise 1).
- **Symmetry**: the $1/f^3$ corner $\propto c_0^2$; suppressing $c_0$ is the most effective lever (Exercises 2, 7).
- **Ring vs LC**: $\Gamma_{rms}\propto N^{-3/2}$; LC wins on both $\Gamma_{rms}$ (small/spread out) and $q_{max}$ (high Q, large swing) (Exercise 3).
- **PLL optimal BW**: low-pass the ref, high-pass the VCO; $f_n^\*$ sits at the curve crossover, and a minimum integrated jitter exists (Exercise 4).
- **$\sigma_t\to$BER**: bathtub $Q$ function; $10^{-12}$ requires $UI/2\ge7.03\sigma_t$, $10^{-15}$ requires $\ge7.94\sigma_t$ (Exercises 5, 6).
- **Tail noise**: tail filter (block $2\omega_0$) / symmetrization (suppress $c_0$) / increase $q_{max}$, all three together (Exercise 7).
- **Jitter budget**: RJ sources' **variances add**, $\sigma_{t,\text{vco}}=\sqrt{\sigma_{tot}^2-\sigma_{ref}^2}$ (Exercise 8).
- All Python verifications import from `simulations/common/` (`pll_utils`, `serdes_utils`, `isf_utils`).

## Further reading

- Increasing swing to reduce noise: [tank_swing](/06_design_insights/tank_swing)
- Waveform slope and the ISF: [waveform_slope](/06_design_insights/waveform_slope)
- Symmetry suppressing $1/f^3$: [symmetry](/06_design_insights/symmetry)
- ring vs LC: [lc_vs_ring](/06_design_insights/lc_vs_ring)
- PLL noise budget and optimal BW: [pll_noise_budget](/06_design_insights/pll_noise_budget)
- Real topologies and tail noise: [real_oscillator_topologies](/06_design_insights/real_oscillator_topologies)
- SerDes connection: [serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)
- Phase noise from tuning/supply pushing: [varactor_tuning_supply_pushing](/06_design_insights/varactor_tuning_supply_pushing)
- Tank $Q$ and energy restoration: [tank_Q_and_energy_restoration](/02_foundations/tank_Q_and_energy_restoration)

## Other exercise sets

The same ISF machinery applied at different levels — foundational conversions, core ISF→PN derivations, complementing this page's design back-calculations:

- Foundations chapter exercises (unit conversions, PSD/jitter, random processes): [02 Foundations chapter exercises](/02_foundations/exercises)
- Core-theory chapter exercises (ISF definition, convolution, white noise→$1/f^2$, flicker→$1/f^3$, Fourier/Parseval): [03 ISF core-theory chapter exercises](/03_isf_core_theory/exercises)
