---
title: Tank swing, q_max, and phase noise
description: Why larger signal swing lowers phase sensitivity — phase noise is proportional to 1/q_max² ([P1] Eq.(21)), and the power / voltage-headroom trade-off.
---

> **β**: This English translation is in beta — the Traditional-Chinese original is the authoritative version.

# Tank swing, $q_{max}$, and phase noise

> **Prerequisites**: [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) ([P1] Eq.(21) signature result $\mathcal{L}\propto\Gamma_{rms}^2/q_{max}^2$), [impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift) (why $q_{max}=CV_{max}$ lands in the denominator), [tank_Q_and_energy_restoration](/02_foundations/tank_Q_and_energy_restoration) (why high $Q$ is "nearly-free swing", where $R_p$ comes from) | **Next**: [varactor_tuning_supply_pushing](/06_design_insights/varactor_tuning_supply_pushing), [lc_vs_ring](/06_design_insights/lc_vs_ring)

This page answers the question asked earliest — and most often underestimated — in oscillator design:
**why does making the tank's (LC resonator's) voltage swing larger lower phase noise?**
The answer is the cleanest scaling in ISF theory: phase noise is **inversely proportional to $q_{max}^2$**,
and $q_{max}=C_{node}V_{max}$ is set directly by swing.

> **Physical intuition (conclusion first)**: phase error $=\dfrac{\Gamma}{q_{max}}\Delta q$ — the denominator is $q_{max}$.
> The larger the swing, the more charge $q_{max}$ the signal carries, and the same lump of noise charge $\Delta q$
> becomes proportionally more "negligible" against it, so the phase it can push is smaller. Make the signal big,
> outweigh the noise — this is the first principle of every low-phase-noise design. The cost: swing is bounded by
> supply / headroom, and pushing swing up usually burns more power.

## Step 1: what $q_{max}$ is, and why it lands in the denominator

$q_{max}$ is "the maximum charge corresponding to the signal swing" at a node:

$$
q_{max}=C_{node}\,V_{max}
$$

- **Unit check**: $[\text{F}]\cdot[\text{V}]=[\text{C}]$ ✓.
- It appears in the denominator of the impulse→phase relation ([P1] Eq.(10)–(11), p.182): $\Delta\phi=\dfrac{\Gamma}{q_{max}}\Delta q$.
- **Meaning**: $\Delta q/q_{max}$ is "the injected charge as a fraction of the signal charge." Larger $q_{max}$ →
  the same $\Delta q$ produces a smaller relative disturbance → phase is more stable. $\Gamma$ (a dimensionless
  shape) itself **does not change with swing**; swing only moves $q_{max}$.

## Step 2: the phase-noise $\propto 1/q_{max}^2$ scaling

The signature result for white-noise-induced $1/f^2$ phase noise ([P1] Eq.(21), p.185):

$$
\mathcal{L}\{\Delta\omega\}=10\log_{10}\!\left(\frac{\Gamma_{rms}^2}{q_{max}^2}\cdot\frac{\overline{i_n^2}/\Delta f}{4\,\Delta\omega^2}\right)
$$

- The denominator has **$q_{max}^2$**. So $\mathcal{L}\propto1/q_{max}^2$.
- **Scaling (claim C3)**: doubling $q_{max}$ → $\mathcal{L}$ drops by $10\log_{10}(2^2)=6.02$ dB.
  Every doubling of swing (with $C$ fixed) **improves phase noise by 6 dB**.

**Step-by-step algebra: how "$q_{max}$ doubled → −6 dB" falls out of Eq.(21).**
Let $q_{max}\to q_{max}'=2q_{max}$, with everything else ($\Gamma_{rms}$, $\overline{i_n^2}/\Delta f$, $\Delta\omega$) unchanged.
Phase noise is "dB = $10\log_{10}$(power ratio inside the brackets)", so we only need the **new/old ratio** inside the brackets:

$$
\begin{aligned}
\frac{P_{new}}{P_{old}}
&=\frac{\dfrac{\Gamma_{rms}^2}{(2q_{max})^2}\cdot\dfrac{\overline{i_n^2}/\Delta f}{4\Delta\omega^2}}
       {\dfrac{\Gamma_{rms}^2}{q_{max}^2}\cdot\dfrac{\overline{i_n^2}/\Delta f}{4\Delta\omega^2}}
\;=\;\frac{1/(2q_{max})^2}{1/q_{max}^2}
\;=\;\frac{q_{max}^2}{(2q_{max})^2}
\;=\;\frac{1}{4}, \\[6pt]
\Delta\mathcal{L}&=\mathcal{L}_{new}-\mathcal{L}_{old}
=10\log_{10}\!\left(\frac{P_{new}}{P_{old}}\right)
=10\log_{10}\!\left(\frac14\right)
=-10\log_{10}4 \\[4pt]
&=-20\log_{10}2=-20\times0.30103=-6.02\ \text{dB}.
\end{aligned}
$$

- **What each step uses**: line 1 cancels all common factors ($\Gamma_{rms}^2$, $\overline{i_n^2}/\Delta f$, $4\Delta\omega^2$),
  leaving only the ratio of $q_{max}$; lines 2→3 use the log identity $\log_{10}4=\log_{10}2^2=2\log_{10}2$.
- **Why "6 dB/octave" and not 3 dB**: because $\mathcal{L}\propto q_{max}^{-2}$ is an **inverse-square** law — a power
  ratio of $\tfrac14$ corresponds to $-6$ dB (not $-3$ dB; $-3$ dB is $\tfrac12$). Doubling voltage/charge → power ratio
  $4\times$ → $20\log_{10}2$.
- **Dimension check**: the ratio $P_{new}/P_{old}$ is dimensionless (same units cancel) → $10\log_{10}$ gives dB
  (dimensionless) ✓.
- **Dimension check (the whole bracket must be dimensionless to give dBc/Hz)**:
  $\dfrac{(\text{dimensionless})^2}{[\text{C}]^2}\cdot\dfrac{[\text{A}^2/\text{Hz}]}{[\text{rad/s}]^2}
  =\dfrac{[\text{A}^2/\text{Hz}]}{[\text{C}^2][\text{s}^{-2}]}$. Using $[\text{A}]=[\text{C/s}]$:
  $=\dfrac{[\text{C}^2\text{s}^{-2}/\text{Hz}]}{[\text{C}^2\text{s}^{-2}]}=\dfrac{1}{[\text{Hz}]}$.
  $\overline{i_n^2}/\Delta f$ is itself already per-Hz, and it is exactly this per-Hz factor that makes the absolute
  $\mathcal{L}$ per-Hz (dBc/Hz); and (as above) the ratio $P_{new}/P_{old}$ itself is dimensionless, so $10\log_{10}$
  gives dB ✓.

The same $1/q_{max}^2$ also appears in the ring oscillator's accumulated-jitter proportionality constant
([P2] Eq.(11)–(12), p.793):

$$
\kappa^2\propto\frac{\Gamma_{rms}^2}{q_{max}^2}\cdot\frac{\overline{i_n^2}}{\Delta f}
$$

- So "larger swing lowers phase noise" and "larger swing lowers jitter" are **the same statement** — they share
  the core ratio $\Gamma_{rms}^2/q_{max}^2$. ([P2] Eq.(12), p.793 verified verbatim:
  $\kappa=\dfrac{\Gamma_{rms}}{q_{max}}\sqrt{\tfrac12\,\overline{i_n^2}/\Delta f}$.)

## Step 3: two routes to raise $q_{max}$ — increase $V_{max}$ vs. increase $C$

$q_{max}=C\cdot V_{max}$, so in principle either raising $C$ or raising $V_{max}$ raises $q_{max}$. But the two routes
have completely different costs:

| Route | Change in $q_{max}$ | Effect on phase noise | Side effect |
|---|---|---|---|
| Increase $V_{max}$ (swing) | $q_{max}\propto V_{max}$ | $\mathcal{L}\propto1/V_{max}^2$ (most effective) | Limited by supply / breakdown / headroom; needs more bias current to sustain swing |
| Increase $C$ (tank capacitance) | $q_{max}\propto C$ | Looks like $\propto1/C^2$, but there is a trap ↓ | To hold $f_0$, $L$ must drop proportionally; sustaining the same swing needs a larger tank current ($Q$, $g_m$ limited); $f_0=1/\sqrt{LC}$ is tied down |

- **Increasing swing is usually the first choice**: direct, 6 dB/octave, and does not move $f_0$.
- **Increasing $C$ has a trap**: in an LC tank $f_0=1/(2\pi\sqrt{LC})$, so raising $C$ requires lowering $L$
  proportionally; sustaining the same swing voltage then needs more tank current ($Q$, $g_m$ limited), and the
  real-world improvement is often eaten by "the extra power/noise spent driving the larger $C$."
  The genuinely clean lever is **pushing swing to the headroom limit within the power budget**.

## Step 4: power / voltage headroom trade-off

Swing cannot grow without bound — it hits two walls, supply and device:

1. **Voltage headroom**: the single-ended swing limit of a differential LC tank ranges from about the supply
   $V_{DD}$ (current-limited regime) up to $\sim\dfrac{4}{\pi}\,I_{bias}R_p$ (where $R_p$ is the tank's equivalent
   parallel resistance). Once pushed into the voltage-limited regime, adding more current no longer adds swing —
   the phase-noise improvement saturates.
2. **Power**: in the current-limited regime, swing $\approx\dfrac{4}{\pi}I_{bias}R_p$ is proportional to bias current.
   Doubling swing → doubling current → doubling power.

Putting the two together gives the **FOM (figure of merit) trade-off**:

- phase noise $\mathcal{L}\propto1/q_{max}^2\propto1/V_{max}^2$ (bigger swing is always better),
- but $V_{max}\propto I_{bias}$ (current-limited) → $\mathcal{L}\propto1/I_{bias}^2$, while $P\propto I_{bias}$,
- so does $\mathcal{L}\propto1/P^2$? — **No.** Because the noise current $\overline{i_n^2}$ also rises with bias
  current (more current → more device noise), typically $\overline{i_n^2}\propto I_{bias}$, and the net effect
  reverts to **$\mathcal{L}\cdot P\approx$ constant** (roughly 1 dB of phase noise bought per extra 1 dB of power burned).
- This is why the industry uses **FOM $=\mathcal{L}-20\log_{10}(f_0/\Delta f)+10\log_{10}(P/1\text{mW})$**
  to fairly compare oscillators at different power levels: it normalizes away this "phase noise × power ≈ constant"
  trade-off.

> ⚠️ The "current-limited / voltage-limited" boundary above and $\dfrac{4}{\pi}I_{bias}R_p$ are
> **standard LC-oscillator design knowledge (not among the five downloaded source PDFs; supplemented from
> standard literature, e.g. the Hajimiri-Lee textbook, Razavi's RF Microelectronics)**. [P1] itself gives the
> $1/q_{max}^2$ scaling but does not expand the circuit-level detail of swing-vs-power. The exact swing-limit
> coefficients and phase-noise-factor floor can be found in E. Hegazi, H. Sjöland, A. A. Abidi,
> *A Filtering Technique to Lower LC Oscillator Phase Noise*, IEEE JSSC **36**(12):1921–1930, 2001
> (verified verbatim), and Razavi's *RF Microelectronics* (external literature, not among the five source PDFs).

## Numerical example (building intuition)

> Using canonical example B as the baseline, we look at the effect of doubling swing.

**Baseline** (example B): $f_0=5$ GHz, $\Delta f=1$ MHz, $q_{max}=1$ pC, $\Gamma_{rms}=0.5$, $S_i=10^{-24}$ A²/Hz:

$$
\mathcal{L}=10\log_{10}\!\left(\frac{0.25}{(10^{-12})^2}\cdot\frac{10^{-24}}{4(2\pi\cdot10^6)^2}\right).
$$

First $\Delta\omega=2\pi\cdot10^6=6.283\times10^6$ rad/s, $\Delta\omega^2=3.948\times10^{13}$.
Bracket $=\dfrac{0.25}{10^{-24}}\cdot\dfrac{10^{-24}}{4\cdot3.948\times10^{13}}=\dfrac{0.25}{1.579\times10^{14}}=1.583\times10^{-15}$,
$\mathcal{L}=10\log_{10}(1.583\times10^{-15})=-148.0$ dBc/Hz.

**Swing doubled** ($q_{max}=2$ pC, everything else unchanged): $q_{max}^2$ becomes 4× → bracket becomes 1/4 →

$$
\mathcal{L}_{new}=-148.0-10\log_{10}(4)=-148.0-6.02=-154.0\ \text{dBc/Hz}.
$$

- **Intuition**: doubling swing → phase noise **improves by 6.0 dB**, exactly $20\log_{10}2$.
- **Trade-off reminder**: but if this 6 dB comes from doubling bias current (current-limited, with
  $\overline{i_n^2}\propto I$), $S_i$ also rises by ~3 dB, so the net improvement is only about 3 dB — this is
  "phase noise × power ≈ constant" at work. The genuine free lunch is "raise $V_{max}$ without adding current"
  (e.g., a higher-$Q$ tank, higher $R_p$).

## Design knobs to lower phase noise / raise $q_{max}$ (checklist)

| Knob | Affects | Mechanism | Cost / notes |
|---|---|---|---|
| Increase voltage swing $V_{max}$ | $q_{max}\uparrow$ | $\mathcal{L}\propto1/V_{max}^2$, 6 dB/octave | Limited by headroom / breakdown |
| Raise tank $Q$ (lower loss, $R_p\uparrow$) | $V_{max}\uparrow$ (more swing at same current) | Higher $R_p$ → same $I_{bias}$ gives more swing, free noise reduction | Limited by process inductor $Q$, parasitics |
| Differential topology | Effective swing ×2 | Differential swing is twice single-ended → $q_{max}\uparrow$ | Double the devices/area/power |
| Push bias to the current/voltage boundary | Maximize $V_{max}$ | Take all available headroom | Past the voltage-limited point it saturates — only wastes current |
| Lower $\Gamma_{rms}$ (the other lever) | $\mathcal{L}\propto\Gamma_{rms}^2$ | Equally important as $q_{max}$ | See [device_noise_mapping](/06_design_insights/device_noise_mapping) |

> Note: $\mathcal{L}\propto\Gamma_{rms}^2/q_{max}^2$ — **$q_{max}$ and $\Gamma_{rms}$ are two independent levers**.
> This page covers $q_{max}$ (swing); $\Gamma_{rms}$ (waveform shape, cyclostationary) is covered in
> [device_noise_mapping](/06_design_insights/device_noise_mapping).

## Validity and failure conditions

| Condition | When it holds | When it fails |
|---|---|---|
| Small perturbation, ISF unchanged by swing | $\mathcal{L}\propto1/q_{max}^2$ holds cleanly | Once swing is large enough to change waveform shape/$\Gamma$, the scaling deviates |
| Current-limited regime | Swing $\propto I_{bias}$, buys phase noise | After voltage-limited, more current is useless |
| $\overline{i_n^2}$ unchanged by swing | Full 6 dB/octave is realized | If noise rises with bias, the net improvement is discounted |

## Worked examples

The following two problems use [P1] Eq.(21) step by step to compute "swing/$q_{max}$ change → $\mathcal{L}$ change,"
continuing with canonical example B:
$f_0=5$ GHz, $\Delta f=1$ MHz, $\Gamma_{rms}=0.5$, $S_i=\overline{i_n^2}/\Delta f=10^{-24}$ A²/Hz.

> **Example 1 ($q_{max}$ doubled → $\mathcal{L}$ drops 6 dB, step-by-step with Eq.(21))**
> Baseline $q_{max}=1$ pC gives $\mathcal{L}=-148.0$ dBc/Hz (example B). Double the swing so $q_{max}=2$ pC
> ($C$ fixed, $V_{max}$ doubled), everything else unchanged. Find the new $\mathcal{L}$.

**Step-by-step substitution (with units)**, plugging directly into Eq.(21) for the absolute value
(no approximation), then checking against −6 dB:

$$
\begin{aligned}
\Delta\omega&=2\pi\Delta f=2\pi\times10^{6}=6.283\times10^{6}\ \text{rad/s},\quad \Delta\omega^2=3.948\times10^{13}\ \text{(rad/s)}^2, \\[4pt]
\text{bracket}_{new}&=\frac{\Gamma_{rms}^2}{(q_{max}')^2}\cdot\frac{S_i}{4\Delta\omega^2}
=\frac{(0.5)^2}{(2\times10^{-12}\,\text{C})^2}\cdot\frac{10^{-24}\,\text{A}^2/\text{Hz}}{4\times3.948\times10^{13}} \\[4pt]
&=\frac{0.25}{4\times10^{-24}}\cdot\frac{10^{-24}}{1.579\times10^{14}}
=\frac{0.25}{4\times1.579\times10^{14}}=3.958\times10^{-16}, \\[4pt]
\mathcal{L}_{new}&=10\log_{10}(3.958\times10^{-16})=-154.0\ \text{dBc/Hz}.
\end{aligned}
$$

- **Result**: $\mathcal{L}_{new}=-154.0$ dBc/Hz, exactly **6.0 dB** lower than the baseline $-148.0$ — matching the
  $-20\log_{10}2$ algebraic conclusion above.
- **Dimension check**: inside the bracket, $\dfrac{\text{dimensionless}}{[\text{C}]^2}\cdot\dfrac{[\text{A}^2/\text{Hz}]}{[\text{rad/s}]^2}$,
  using $[\text{A}]=[\text{C/s}]$ → $[\text{A}^2]=[\text{C}^2\text{s}^{-2}]$, numerator $[\text{C}^2\text{s}^{-2}/\text{Hz}]$,
  denominator $[\text{C}^2\text{s}^{-2}]$ → leaves $1/[\text{Hz}]$, absorbed into per-Hz → dimensionless power ratio,
  $10\log_{10}$ gives dBc/Hz ✓.
- **One-line Python check**:

```python
import numpy as np
def L_eq21(grms, qmax, Si, dw):
    return 10*np.log10(grms**2/qmax**2 * Si/(4*dw**2))
dw = 2*np.pi*1e6
L0 = L_eq21(0.5, 1e-12, 1e-24, dw)   # baseline
L1 = L_eq21(0.5, 2e-12, 1e-24, dw)   # qmax doubled
print(round(L0,1), round(L1,1), round(L1-L0,2))  # -> -148.0 -154.0 -6.02
```

> **Example 2 (moving two levers at once: swing doubled + $\Gamma_{rms}$ halved)**
> Starting from the baseline ($q_{max}=1$ pC, $\Gamma_{rms}=0.5$), double the swing ($q_{max}=2$ pC) **and**
> improve the waveform so $\Gamma_{rms}=0.25$ (halved). Find the total improvement $\Delta\mathcal{L}$.

**Step-by-step substitution.** Since $\mathcal{L}\propto\Gamma_{rms}^2/q_{max}^2$, the two levers **add** in the log domain:

$$
\begin{aligned}
\Delta\mathcal{L}&=10\log_{10}\!\left(\frac{(\Gamma_{rms}')^2/(q_{max}')^2}{\Gamma_{rms}^2/q_{max}^2}\right)
=\underbrace{10\log_{10}\!\left(\frac{(0.25)^2}{(0.5)^2}\right)}_{\Gamma_{rms}\,\text{halved}}
+\underbrace{10\log_{10}\!\left(\frac{(10^{-12})^2}{(2\times10^{-12})^2}\right)}_{q_{max}\,\text{doubled}} \\[4pt]
&=10\log_{10}(0.25)+10\log_{10}(0.25)=(-6.02)+(-6.02)=-12.04\ \text{dB}.
\end{aligned}
$$

- **Result**: total improvement **−12 dB** (each lever contributes −6 dB). Relative to example B, $-148.0$ →
  $-160.0$ dBc/Hz. This shows $\Gamma_{rms}$ and $q_{max}$ are **two independent, additive** levers (the
  numerator and denominator of [P1] Eq.(21)).
- **Dimension check**: both ratios are dimensionless → dB values still add as dB ✓.
- **One-line Python check**:

```python
import numpy as np
print(round(L_eq21(0.25, 2e-12, 1e-24, 2*np.pi*1e6) - L_eq21(0.5, 1e-12, 1e-24, 2*np.pi*1e6), 2))
# -> -12.04 dB   (reuse L_eq21 from Example 1)
```

> Reminder (see Step 4): if these improvements come from bias current (current-limited, $\overline{i_n^2}\propto I_{bias}$),
> $S_i$ rises along with it and the net improvement is discounted — this is "phase noise × power ≈ constant" again.
> The two problems above assume $S_i$ fixed (the ideal upper bound).

## Key takeaways

- $q_{max}=C\cdot V_{max}$; phase noise $\mathcal{L}\propto1/q_{max}^2$ ([P1] Eq.(21)).
- Doubling $q_{max}$ → $\mathcal{L}$ improves by **6.02 dB** (e.g., $-148\to-154$ dBc/Hz).
- Increasing swing is cleaner than increasing $C$ (increasing $C$ ties down $f_0$ and needs more current);
  raising tank $Q$ is nearly-free swing.
- Trade-off: in the current-limited regime, swing $\propto$ current, and device noise $\propto$ current too →
  **phase noise × power ≈ constant**; use FOM for a fair comparison.
- $q_{max}$ and $\Gamma_{rms}$ are two independent levers (the numerator and denominator of [P1] Eq.(21)).

## Further reading

- Signature-formula derivation: [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)
- The role of $q_{max}$ in impulse→phase: [impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift)
- Where tank $Q$ comes from, why high $Q$ equals free swing, $R_p$ and $4kT/R_p$ thermal noise: [tank_Q_and_energy_restoration](/02_foundations/tank_Q_and_energy_restoration)
- How tuning-line/supply jitter FMs the carrier (another phase-noise gateway): [varactor_tuning_supply_pushing](/06_design_insights/varactor_tuning_supply_pushing)
- The other lever, $\Gamma_{rms}$: [device_noise_mapping](/06_design_insights/device_noise_mapping)
- Connection to slope/swing: [waveform_slope](/06_design_insights/waveform_slope)
- LC vs. ring swing differences: [lc_vs_ring](/06_design_insights/lc_vs_ring)
