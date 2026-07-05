---
title: "Reference oscillators: crystal and MEMS phase noise"
description: "Why crystal/MEMS references are the low-offset anchor of every clock chain — a crystal is just an extreme LC tank with Q up to 10⁴–10⁶; using the site's tank_Q page Q↔Γrms/qmax bridge, we derive step by step that close-in L and the Lorentzian linewidth both scale as ∝1/Q²; a checkable worked block (Q=50,000@100 MHz vs Q=10@5 GHz, same-offset Leeson term differs by ~105 dB, ~71 dB after normalizing to the same carrier); a typical-magnitude table for XO/TCXO/OCXO/MEMS (industry convention, external); and why aging/temperature (the ppm slow axis) and phase noise (the dBc/Hz fast axis) are two distinct spec axes."
---

> **β**: This English translation is in beta — the Traditional-Chinese original is the authoritative version.

import RefVsLcLeeson from "@site/src/components/RefVsLcLeeson";

# Reference oscillators (crystal / MEMS): the low-offset anchor of the clock chain

> **Prerequisites**: [clock_chain_budget](/06_design_insights/clock_chain_budget) (rule 3: in-band $= N^2 S_{ref}\lvert H_{lp}\rvert^2$), [tank_Q_and_energy_restoration](/02_foundations/tank_Q_and_energy_restoration) (the three forms of $Q$, $4kT/R_p$, the $Q\leftrightarrow\Gamma_{rms}/q_{max}$ bridge — every derivation on this page stands on it), [derivation_leeson](/99_appendix/derivation_leeson) (the $\big(\tfrac{\omega_0}{2Q\Delta\omega}\big)^2$ shaping term) | **Next**: [pll_noise_budget](/06_design_insights/pll_noise_budget), [fom_limit](/06_design_insights/fom_limit)

Every real clock chain — SoC, SerDes, sampling system, RF transceiver — sits on top of a
**reference oscillator**: a crystal oscillator (XO) or a MEMS oscillator. System
designers often spend more on it than on the entire PLL. The question is: **why? What does it
actually buy, and what doesn't it buy?** This page answers using two bridges already built
on this site:
[clock_chain_budget](/06_design_insights/clock_chain_budget) rule 3 explains **why nothing
downstream in the chain can clean up the reference's close-in noise**;
the [tank_Q_and_energy_restoration](/02_foundations/tank_Q_and_energy_restoration)
$Q\leftrightarrow\Gamma_{rms}/q_{max}$ bridge explains **why a crystal's close-in noise is
inherently orders of magnitude lower**.

> **Physical intuition (conclusion first)**: a crystal is not new physics — it is just an
> **LC tank with an absurdly high $Q$**. The quartz's mechanical resonance maps to an equivalent
> $L$, $C$, $R$, with $Q$ typically $10^4$ to $10^6$ (industry-convention magnitude, external),
> versus an on-chip spiral-inductor tank at only $Q\approx5$–$20$. The same Leeson/ISF formula,
> the same $\big(\tfrac{f_0}{2Q\Delta f}\big)^2$ shaping term, applied with $Q$ going from 10 to
> $5\times10^4$: close-in phase noise drops $\propto 1/Q^2$ — tens of dB, not from clever circuitry
> but from **enormous energy stored in the resonator against a vanishingly small per-cycle loss**.
> The clock chain's division of labor follows naturally: **low offset is the reference's job,
> high offset is the VCO's job**, and the PLL is just the tailor stitching the two segments together.

> **Honesty note (read this first)**: none of the 5 downloaded PDFs on this site ([P1]–[P5])
> cover crystal / MEMS content. Every place on this page that connects to ISF does so through
> the already-verified [P1] Eq.(21), p.185, and the site's own
> [tank_Q_and_energy_restoration](/02_foundations/tank_Q_and_energy_restoration) bridge;
> the Leeson shaping term belongs to [E1] Leeson 1966 (external literature, not among the five
> source PDFs, see [references](/99_appendix/references)); the crystal equivalent circuit (BVD
> model) and the typical numbers for XO/TCXO/OCXO/MEMS belong to **standard frequency-control
> industry knowledge (industry convention, external, not among the five source PDFs)** — this
> page gives only order-of-magnitude ranges, does not fabricate specific paper citations, and
> selection should follow vendor datasheets.

## Step 1: why the reference is the low-offset anchor of the whole chain

[clock_chain_budget](/06_design_insights/clock_chain_budget) rule 3 (PLL) states:

$$
S_{out}(f)=N^2\,S_{ref}(f)\,\lvert H_{lp}(f)\rvert^2+S_{vco}(f)\,\lvert H_{hp}(f)\rvert^2
$$

In-band ($f\ll f_n$, inside the loop bandwidth) $\lvert H_{lp}\rvert^2\to1$: **the output's
close-in phase noise is exactly the reference's phase noise plus $20\log_{10}N$** — not a single
dB escapes this. Now look at what else in the chain can do (same page, rules 1, 2, 4): ×N, ÷N only
**scale** (the entire curve shifts; clean in, clean out); a buffer can only **add** its own floor
(power addition, only ever makes things worse). Conclusion:

- **Nothing in the chain can improve the reference's close-in noise.** The quality of the low
  offset (inside loop BW) is locked in the moment you "buy that reference."
- That page's worked chain is living proof: of the final 27.6 fs integrated jitter, **65.9% of
  the power comes from the reference's in-band floor after being lifted by $\times N^2$**, while
  the pretty $-148$ dBc/Hz VCO contributes only 0.42%.
- Conversely, far-out (outside loop BW) the reference is completely irrelevant — there,
  $\lvert H_{hp}\rvert^2\to1$, and it's the VCO's show. **The reference is a low-offset anchor,
  not a full-spectrum savior** (the worked block in Step 4 puts numbers to this).

> **Example 1 (anchoring a reference into a ×50 PLL — canonical numbers)**: a 100 MHz
> low-noise XO has $\mathcal{L}=-150$ dBc/Hz at 1 kHz offset (low-noise-XO-grade,
> industry-convention magnitude, external). Locked into a ×50 PLL to 5 GHz, what is the
> in-band $\mathcal{L}(1\,\text{kHz})$? How much better is it than a free-running on-chip LC?

**Substituting step by step (with units)** — in-band, using rule 3's asymptotic form:

$$
\mathcal{L}_{out}(1\,\text{kHz})=-150+20\log_{10}50=-150+33.98=-116.02\ \text{dBc/Hz}.
$$

Control case: the site's canonical example B 5 GHz on-chip LC ($\mathcal{L}(1\,\text{MHz})=-148$,
$1/f^2$ skirt) extrapolated free-running to 1 kHz: $-148+20\log_{10}(10^6/10^3)=-148+60=-88$ dBc/Hz.
**Locking to the reference wins by 28.0 dB at 1 kHz** — that's what "buying a reference" buys you.
The two lines cross at $25.2$ kHz (solving $-148-20\log_{10}(f/10^6)=-116.02$ for $f$),
which is exactly the first intuition behind
[pll_noise_budget](/06_design_insights/pll_noise_budget)'s "the crossover point sets the optimal
loop BW." **Dimension check**: dB addition = multiplying dimensionless ratios ✓; $N$ in
$20\log_{10}N$ is dimensionless ✓. One-line Python check:

```python
import numpy as np
L_in = -150.0 + 20*np.log10(50)        # rule 3 in-band: ref + 20logN
print(round(L_in, 2))                  # -> -116.02
L_lc = -148.0 - 20*np.log10(1e3/1e6)   # canonical LC 1/f² skirt extrapolated to 1 kHz
print(round(L_lc, 1))                  # -> -88.0
print(round(L_lc - L_in, 1))           # -> 28.0
f_cross = 1e6 * 10**(-(L_in + 148.0)/20)
print(round(f_cross/1e3, 1))           # -> 25.2
```

## Step 2: a crystal is just an LC tank with an extreme $Q$

A quartz crystal is a **mechanical** resonator: the piezoelectric effect (mechanical
strain↔electric field interconversion) maps the quartz plate's mechanical vibration mode into
an equivalent circuit at the electrical port — the standard **BVD model
(Butterworth–Van Dyke equivalent circuit, external textbook content, not among the five source
PDFs)**:

- **motional branch**: series $L_m$–$C_m$–$R_m$, representing the mechanical mass-stiffness-damping.
  Magnitude (industry convention): $L_m\sim$ mH–H, $C_m\sim$ fF, $R_m\sim$ tens to hundreds of $\Omega$.
- **$C_0$ (static capacitance)**: the ordinary capacitance of the electrodes and package, pF-scale,
  in parallel with the motional branch.

Near the series resonance $\omega_s=1/\sqrt{L_mC_m}$, this is just an LC tank, with $Q$ using the
same definition as in
[tank_Q_and_energy_restoration](/02_foundations/tank_Q_and_energy_restoration)
(series form $Q=\omega_s L_m/R_m$, or the energy definition $Q=\omega_0 E_{stored}/P_{diss}$ —
the same $Q$ on both pages):

$$
Q_{crystal}\sim10^4\ \text{to}\ 10^6\qquad\text{vs}\qquad Q_{on\text{-}chip\ LC}\sim5\text{–}20.
$$

(The crystal $Q$ range is industry-convention magnitude, external; the on-chip $Q$ ceiling is
covered in Step 5 of the tank_Q page.)
$L_m\sim$ mH against on-chip nH — **a 6-order-of-magnitude difference in equivalent inductance**
paired with an even smaller equivalent loss — this is the circuit embodiment of "enormous stored
energy against vanishingly small per-cycle loss." The oscillation waveform is close to sinusoidal,
so the pedagogical-toy ISF is still $\Gamma\approx-\sin$, $\Gamma_{rms}=1/\sqrt2$
([rms_isf](/03_isf_core_theory/rms_isf)) — **the crystal's advantage does not come from ISF shape,
it comes entirely from $Q$ (equivalently: stored energy $E$ and $q_{max}$)**. The next step turns
this sentence into a formula.

## Step 3: using the site's $Q\leftrightarrow\Gamma_{rms}/q_{max}$ bridge to derive $1/Q^2$ scaling

The bridge from Step 4(c) of
[tank_Q_and_energy_restoration](/02_foundations/tank_Q_and_energy_restoration): Leeson's
$\dfrac{1}{2Q}$ and ISF's $\dfrac{\Gamma_{rms}}{q_{max}}$ are the same "noise→phase" conversion
efficiency. Now walk this bridge **step by step from [P1] Eq.(21)** (sinusoidal LC toy, tank
thermal noise only; active core handled separately):

**(1) Starting point — [P1] Eq.(21), p.185 (within the 5 PDFs, already verified):**

$$
\mathcal{L}\{\Delta\omega\}=10\log_{10}\!\left(\frac{\Gamma_{rms}^2}{q_{max}^2}\cdot\frac{\overline{i_n^2}/\Delta f}{4\,\Delta\omega^2}\right)
$$

**(2) Substituting three quantities already derived on this site**: $\Gamma_{rms}^2=\tfrac12$
(the rms of $\Gamma=-\sin$, [rms_isf](/03_isf_core_theory/rms_isf)), $q_{max}=C\,V_p$ (canonical
notation table), $\overline{i_n^2}/\Delta f=4kT/R_p$ (tank loss thermal noise, tank_Q page Step 3):

$$
\mathcal{L}_{lin}=\frac{\tfrac12}{C^2V_p^2}\cdot\frac{4kT/R_p}{4\,\Delta\omega^2}
=\frac{kT}{2\,C^2V_p^2\,R_p\,\Delta\omega^2}.
$$

**(3) Replacing $R_p$ using $Q$** (tank_Q page Step 1: $R_p=Q/(\omega_0 C)$):

$$
\mathcal{L}_{lin}=\frac{kT\,\omega_0 C}{2\,C^2V_p^2\,Q\,\Delta\omega^2}
=\frac{kT\,\omega_0}{2\,C V_p^2\,Q\,\Delta\omega^2}.
$$

**(4) Replacing $CV_p^2$ using stored energy** (tank_Q page Step 2: $E_{stored}=\tfrac12 CV_p^2$,
i.e. $CV_p^2=2E_{stored}$):

$$
\boxed{\ \mathcal{L}_{lin}(\Delta\omega)=\frac{kT\,\omega_0}{4\,E_{stored}\,Q\,\Delta\omega^2}\ }
$$

**(5) Converting to power form using the energy definition** (tank_Q page Step 2:
$P_{diss}=\omega_0E_{stored}/Q$, i.e. $E_{stored}=Q\,P_{diss}/\omega_0$):

$$
\mathcal{L}_{lin}(\Delta\omega)=\frac{kT}{P_{diss}}\left(\frac{\omega_0}{2Q\,\Delta\omega}\right)^2.
$$

This is exactly **Leeson's ([E1], external) $1/f^2$ segment at $F=1$, thermal-only** — the ISF
version and the Leeson version meet exactly along this chain (the factor-of-2 SSB accounting
convention still applies as usual, see
[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise); this page uses
[P1] Eq.(21)'s /4 convention throughout).

- **Dimension check (Step-4 form)**: $\dfrac{[\text{J}][\text{rad/s}]}{[\text{J}][\text{rad/s}]^2}=\dfrac{1}{[\text{1/s}]}=[\text{s}]=1/\text{Hz}$ ✓
  ($\mathcal{L}_{lin}$ is a per-Hz power ratio).
- **Dimension check (Step-5 form)**: $kT/P_{diss}=[\text{J}]/[\text{W}]=[\text{s}]=1/\text{Hz}$,
  the bracketed square is dimensionless ✓.

**Three immediate corollaries** (all backed by the numbers in Step 4 and Example 2):

1. **close-in $\mathcal{L}\propto 1/Q^2$** (fixed $P_{diss}$): $Q\times10\Rightarrow-20$ dB.
   A crystal's $Q$ is $10^3$–$10^5\times$ higher than on-chip LC — this term alone is
   $-60$ to $-100$ dB.
2. **The real lever is the $E_{stored}\cdot Q$ product** (Step-4 form) — "how much energy is
   stored" × "how slowly it leaks." The same $4kT$ fluctuation, against a larger energy reservoir
   with slower leakage, converts to smaller phase. This is the energy reading of the
   $Q\leftrightarrow\Gamma_{rms}/q_{max}$ bridge: **a crystal's effective
   $\Gamma_{rms}/q_{max}$ (together with the noise it sees) is orders of magnitude lower than
   any on-chip LC** — not because the ISF shape differs, but because the denominator $q_{max}$
   (stored charge/energy) is enormous while the noise source (loss) is relatively tiny.
3. **The Lorentzian linewidth also $\propto1/Q^2$**: the close-in $1/f^2$ skirt corresponds to
   the phase diffusion constant $D$
   (single-sideband $S_\phi=4D/\Delta\omega^2$,
   [diffusion_dictionary](/03_isf_core_theory/diffusion_dictionary)), read off from Step 5 as
   $S_\phi=2\mathcal{L}_{lin}$:

$$
D=\frac{\Delta\omega^2 S_\phi}{4}=\frac{kT\,\omega_0^2}{8\,P_{diss}\,Q^2},\qquad
\Delta f_{3\mathrm{dB}}=\frac{D}{\pi}=\frac{kT\,\omega_0^2}{8\pi\,P_{diss}\,Q^2}\ \propto\ \frac{1}{Q^2}.
$$

**Plugging in numbers (how much energy does a crystal actually store)** — crystal:
$f_0=100$ MHz, $Q=5\times10^4$, drive (dissipated) power $P_{diss}=100\ \mu$W (typical crystal
drive-level magnitude, industry convention, external); on-chip LC: the tank_Q page's canonical
example ($C=1.013$ pF, $V_p=1$ V, $Q=10$, $f_0=5$ GHz):

```python
import numpy as np
k, T = 1.380649e-23, 300.0
kT = k*T
f0x, Qx, Px = 100e6, 5e4, 100e-6      # crystal: 100 MHz, Q=50k, drive 100 µW
w0x = 2*np.pi*f0x
Ex = Qx*Px/w0x                        # E = Q·P/ω0 (tank_Q Step 2 energy definition solved backward)
print(round(Ex*1e9, 2))               # -> 7.96
C, Vp, Ql = 1.013e-12, 1.0, 10.0      # on-chip LC (tank_Q canonical example)
El = 0.5*C*Vp**2
w0l = 2*np.pi*5e9
Pl = w0l*El/Ql                        # power the LC must dissipate
print(round(El*1e12, 3))              # -> 0.507
print(round(Pl*1e3, 2))               # -> 1.59
print(round(10*np.log10((Ex*Qx)/(El*Ql)), 1))               # -> 79.0
print(round(10*np.log10((w0l/(El*Ql))/(w0x/(Ex*Qx))), 1))   # -> 95.9
print(round(10*np.log10(kT/Px), 1))   # -> -163.8
```

Reading: the crystal stores **7.96 nJ**, about $1.6\times10^4\times$ the LC's 0.507 pJ — while
dissipating 16× less power (0.1 mW vs 1.59 mW). The $E\cdot Q$ product differs by **79.0 dB**;
factoring in one power of $\omega_0$ as well, **the same-offset thermal-only $\mathcal{L}$
differs by 95.9 dB** (amplitude ratio $\sqrt{3.9\times10^9}\approx6\times10^4$ — this is what
"effective $\Gamma_{rms}/q_{max}$ lower by nearly 5 orders of magnitude" means). The last line
also gives the crystal's ideal floor at its own Leeson corner, $kT/P_{diss}=-163.8$ dBc/Hz —
the same order of magnitude as real low-noise XO floors of $-150$ to $-160$ (industry
convention); the remaining gap belongs to the sustaining amplifier's noise factor and flicker
(see the failure conditions).

> **Example 2 (linewidth $\propto1/Q^2$ — same two oscillators)**: plugging the two parameter
> sets above into $\Delta f_{3\mathrm{dB}}=kT\omega_0^2/(8\pi P_{diss}Q^2)$, what is each
> oscillator's thermal-only Lorentzian linewidth?

**Substituting step by step (with units)**:

$$
\text{crystal}:\ \frac{4.14\times10^{-21}\times(6.28\times10^8)^2}{8\pi\times10^{-4}\times(5\times10^4)^2}
=2.6\times10^{-10}\ \text{Hz},\qquad
\text{LC}:\ 1.02\ \text{Hz}.
$$

A ratio of $3.9\times10^9$ (95.9 dB) — **exactly the same number** as the same-offset
$\mathcal{L}$ ratio above (both $\propto\omega_0^2/(PQ^2)$; a self-consistency check ✓). The
crystal's thermal-only linewidth at the $10^{-10}$ Hz level is **unmeasurable within any
achievable measurement time** — this is the quantitative version of "the reference's carrier is
essentially a delta function." Both numbers are thermal-only ideal values (no flicker, no
sustaining amp) and are marked illustrative. **Dimension check**:
$\dfrac{[\text{J}][\text{rad/s}]^2}{[\text{W}]}=[\text{J/s}]\cdot\dfrac{[\text{J}]}{[\text{W}]}\cdot\dfrac{1}{[\text{s}]}=[\text{1/s}]=[\text{Hz}]$ ✓.
One-line Python check:

```python
import numpy as np
kT = 1.380649e-23*300.0
lw = lambda f0, Q, Ps: kT*(2*np.pi*f0)**2/(8*np.pi*Ps*Q**2)
print(f"{lw(100e6, 5e4, 100e-6):.2e}")   # -> 2.60e-10
print(round(lw(5e9, 10.0, 1.591e-3), 2)) # -> 1.02
print(round(10*np.log10(lw(5e9, 10.0, 1.591e-3)/lw(100e6, 5e4, 100e-6)), 1))  # -> 95.9
```

(The LC's $D=\pi\times1.02\approx3.2$ rad²/s belongs to this page's illustrative parameter set,
distinct input from
[diffusion_dictionary](/03_isf_core_theory/diffusion_dictionary)'s toy parameter set
$D=0.125\to39.8$ mHz; the formula is the same.)

## Step 4: worked block — $Q=50{,}000$ @ 100 MHz vs $Q=10$ @ 5 GHz (checkable)

Now for this page's signature, fully checkable comparison: **at the same offset $\Delta f$, how
much does the Leeson shaping term $10\log_{10}\big[1+\big(\tfrac{f_0}{2Q\Delta f}\big)^2\big]$
differ?**
([E1] form; comparing only the shaping term means assuming the same $F$ and same $P_s$ for both
— a deliberately isolated variable, honestly noted below.)

First compute the **Leeson corner** $f_0/2Q$ for both (where the shaping term rolls off from
$1/f^2$ to flat):

$$
\text{crystal}:\ \frac{10^8}{2\times5\times10^4}=1000\ \text{Hz},\qquad
\text{LC}:\ \frac{5\times10^9}{2\times10}=2.5\times10^8\ \text{Hz}=250\ \text{MHz}.
$$

The crystal's shaping term is **gone** (flattened) beyond 1 kHz; the LC's shaping term keeps
falling as $1/f^2$ all the way to 250 MHz — **the LC is being penalized by
$\big(\tfrac{f_0}{2Q\Delta f}\big)^2$ across the entire practical offset range**. Computing
offset by offset:

| offset $\Delta f$ | crystal term [dB] | LC term [dB] | difference (same offset, own carriers) | normalized to same carrier ($-33.98$) |
|---|---|---|---|---|
| 1 kHz | $3.01$ | $107.96$ | $104.95$ dB | $70.97$ dB |
| 100 kHz | $0.00$ | $67.96$ | $67.96$ dB | $33.98$ dB |
| 1 MHz | $0.00$ | $47.96$ | $47.96$ dB | $13.98$ dB |

- **4th column**: the raw difference at the same offset, same $F$, same $P_s$. At 1 kHz,
  $104.95$ dB (asymptotic ratio $\big(\tfrac{2.5\times10^8}{10^3}\big)^2=6.25\times10^{10}=108.0$ dB;
  the crystal is $3$ dB short of that at its own corner, from the $1+1$ term).
- **5th column (the honest comparison)**: the 100 MHz and 5 GHz carriers differ, so a fair
  comparison must normalize the crystal ×50 up to 5 GHz, paying $+20\log_{10}50=33.98$ dB
  ([clock_chain_budget](/06_design_insights/clock_chain_budget) rule 1). **After normalizing,
  the 1 kHz advantage is still 71.0 dB**; but note the advantage shrinks with offset (34 dB left
  at 100 kHz, 14 dB at 1 MHz), and beyond the boundary where both $1/f^2$ curves meet the floor,
  the crystal's **floor**, lifted by ×50, can actually lose to the LC's far skirt — exactly what
  Step 1 called "the reference is a low-offset anchor, not a full-spectrum savior," and also why
  the PLL loop BW exists.
- **Dimension check**: $\dfrac{f_0}{2Q\Delta f}=\dfrac{[\text{Hz}]}{[\text{Hz}]}$ dimensionless ✓;
  dB difference = ratio ✓.

```python
import numpy as np
f0x, Qx = 100e6, 5e4    # crystal: 100 MHz, Q = 50,000
f0l, Ql = 5e9, 10.0     # on-chip LC: 5 GHz, Q = 10
term = lambda f0, Q, df: 10*np.log10(1 + (f0/(2*Q*df))**2)
print(round(f0x/(2*Qx), 0))                               # -> 1000.0
print(round(f0l/(2*Ql)/1e6, 0))                           # -> 250.0
print(round(term(f0x, Qx, 1e3), 2))                       # -> 3.01
print(round(term(f0l, Ql, 1e3), 2))                       # -> 107.96
print(round(term(f0l, Ql, 1e3) - term(f0x, Qx, 1e3), 2))  # -> 104.95
print(round(term(f0l, Ql, 1e5) - term(f0x, Qx, 1e5), 2))  # -> 67.96
print(round(term(f0l, Ql, 1e6) - term(f0x, Qx, 1e6), 2))  # -> 47.96
print(round(20*np.log10(f0l/f0x), 2))                     # -> 33.98
```

**Honesty note**: (1) Comparing only the shaping term assumes the same $F$ and same $P_s$; the
real crystal drive power ($\sim0.1$ mW) is lower than typical LC tank dissipation ($\sim1.6$ mW),
and folding power in as well would turn the 108 dB into Step 3's 95.9 dB
($108.0-10\log_{10}(1.59\,\text{mW}/0.1\,\text{mW})=95.9$, the two calculation methods are
self-consistent ✓).
(2) Thermal-only: a real crystal's measured close-in noise is often dominated by the sustaining
amp's $1/f^3$, and the floor is limited by the buffer — this table is "the lower bound set by
resonator physics." (3) $Q=5\times10^4$ @ 100 MHz is a conservative value (100 MHz commonly uses
overtone cuts, where $Q$ can be even higher; industry-convention magnitude, external).

The interactive component below is the general-purpose version of this worked block — drag $Q$,
$f_0$, offset, and watch the two Leeson curves and the normalized-×N gap:

<RefVsLcLeeson />

## Step 5: typical-magnitude table — XO / TCXO / OCXO / MEMS

> **This entire table is an industry-convention order-of-magnitude range (external literature,
> not among the five source PDFs)**: it varies significantly by vendor, cut, frequency, and
> vintage; within the same grade, high vs low bins can differ by 20 dB. This table only builds
> intuition for "which magnitude lives at which tier" — **selection must always follow the
> vendor's $\mathcal{L}(f)$ curve and stability table in the datasheet**; this site does not
> fabricate specific part numbers or paper citations.

| Grade | Typical output frequency | Frequency vs temperature (slow axis) | $\mathcal{L}(1\,\text{kHz})$ magnitude | far-out floor magnitude | One-line positioning |
|---|---|---|---|---|---|
| **XO** (plain crystal osc.) | 10–100 MHz | $\pm10\ldots\pm100$ ppm | $-135\ldots-155$ dBc/Hz | $-150\ldots-165$ dBc/Hz | Cheapest high $Q$; low-noise 100 MHz grade can reach $-150$ dBc/Hz @ 1 kHz |
| **TCXO** (temperature-compensated XO) | 10–50 MHz | $\pm0.1\ldots\pm2$ ppm | similar to same-grade XO | $-150\ldots-160$ dBc/Hz | The compensation network fixes the **slow axis** (ppm), barely touching $\mathcal{L}(f)$; some designs are actually slightly worse close-in |
| **OCXO** (oven-controlled XO) | 5–100 MHz | $\pm10^{-4}\ldots\pm10^{-2}$ ppm | $-150\ldots-165$ dBc/Hz | $-155\ldots-170$ dBc/Hz | King of close-in (specified even at 1–10 Hz offset); the price is watt-level heater power and size |
| **MEMS oscillator** | 1–700 MHz (PLL-synthesized) | $\pm0.05\ldots\pm20$ ppm depending on grade | $-120\ldots-145$ dBc/Hz | $-140\ldots-155$ dBc/Hz | Silicon resonator + fractional-N PLL; wins on shock resistance/reliability/programmability, phase noise usually concedes to quartz |

Three points for reading the table:

1. **The XO→TCXO→OCXO ladder is mainly a "slow-axis" (ppm) ladder**; the $\mathcal{L}(f)$
   difference is concentrated close-in (OCXO uses a higher-$Q$ cut, a more careful sustaining
   amp, and the oven to suppress the 1 Hz–1 kHz region).
2. The floor region ($\ge10$ kHz) is crowded into $-150$ to $-170$ dBc/Hz across all grades —
   the floor is set by the sustaining amp/output buffer ($kT/P$ level, see Step 3's $-163.8$),
   **not** by $Q$; $Q$ buys the $1/Q^2$ inside the corner.
3. Read MEMS's $\mathcal{L}$ column carefully: its output frequency is PLL-synthesized, and the
   in-band shape is set by the PLL ($N^2$ floor + charge pump), not directly by the resonator's
   Leeson skirt — expanded in the next step.

## Step 6: MEMS — the $f\cdot Q$ product ceiling and the "multiplication tax"

MEMS (microelectromechanical systems) oscillators replace quartz with a silicon mechanical
resonator (vacuum-packaged, $Q\sim10^4$–$10^5$ magnitude), then synthesize the MHz-level
resonance frequency up to whatever output frequency the user wants via a fractional-N PLL.
Two physical facts determine its phase-noise positioning (both industry-convention/materials-physics
magnitude, external):

**(a) The $f\cdot Q$ product ceiling.** For a given material and loss mechanism (phonon
scattering / Akhiezer damping, thermoelastic damping, anchor loss, etc.), the **product** of
resonance frequency and $Q$ has a magnitude ceiling — both quartz and silicon sit around
$f\cdot Q\sim10^{13}$ Hz at room temperature (industry convention; the exact value depends on
cut/mode/temperature, and this site does not give false precision). **This ceiling ties $Q$ and
$f_0$ into a see-saw**: pushing $f_0$ up forces $Q\propto1/f_0$ down.

**(b) Optimal partitioning under the "multiplication tax."** If $f\cdot Q$ is fixed, the Leeson
corner becomes

$$
\frac{f_0}{2Q}=\frac{f_0^2}{2\,(f\cdot Q)}\ \propto\ f_0^2,
$$

and the resonator's own close-in shaping term
$\big(\tfrac{f_0}{2Q\Delta f}\big)^2\propto f_0^4$; normalizing it ×N to a fixed output carrier
$f_{out}$ costs $20\log_{10}(f_{out}/f_0)$, giving a net close-in

$$
\mathcal{L}_{out,\ close\text{-}in}\ \propto\ f_0^4\cdot\Big(\frac{f_{out}}{f_0}\Big)^2=f_0^2\,f_{out}^2
$$

— **every 10× drop in resonator frequency nets a 20 dB gain in output close-in** (same $f\cdot Q$,
same $F$, same $P$). This is why reference sources all live at 10–100 MHz rather than being
built directly as GHz resonators; it is also why MEMS (equally held hostage by $f\cdot Q$)
chooses the MHz-resonator + PLL-synthesis architecture. Numerical check:

```python
import numpy as np
fQ, fout = 1e13, 5e9    # f·Q product fixed (magnitude, industry convention), output 5 GHz
rel = lambda f0: 20*np.log10(f0/(2*(fQ/f0))) + 20*np.log10(fout/f0)
print(round(rel(10e6), 2))               # -> 67.96
print(round(rel(100e6), 2))              # -> 87.96
print(round(rel(100e6) - rel(10e6), 2))  # -> 20.0
```

($rel$ = corner value + multiplication-tax relative dB; 10 MHz/$Q=10^6$ nets 20.0 dB better than
100 MHz/$Q=10^5$ ✓ the $f_0^2$ law. Of course $f_0$ cannot be lowered indefinitely: a larger
$N=f_{out}/f_0$ raises the in-band floor $\propto N^2$, and divider/PLL floor and flicker take
over too — the practical optimum lands at a few tens of MHz, consistent with reference
frequencies in the market.)

**MEMS's accounting consequence**: the output's in-band is set by the fractional-N PLL's $N^2$
floor plus quantization noise, and the out-of-band is set by the built-in VCO — **the
resonator's extremely high $Q$ mainly buys "frequency stability and a close-in anchor," not the
whole curve**. That's why in the Step 5 table, MEMS's $\mathcal{L}(1\,\text{kHz})$ is usually
higher than a same-grade quartz XO (it's the PLL floor, not the resonator skirt), but this is
adequate for many applications (Ethernet, USB, sensing), in exchange for shock/vibration
resistance, lifetime, size, and arbitrary-frequency programmability (industry-convention
positioning, external).

## Step 7: aging/temperature vs phase noise — two distinct spec axes

The datasheet's "stability ±25 ppm" and "$-150$ dBc/Hz @ 1 kHz" **describe two nearly orthogonal
things**, and conflating them is one of the most common selection mistakes in system design:

| | **Fast axis: spectral purity (phase noise)** | **Slow axis: frequency stability (frequency accuracy/stability)** |
|---|---|---|
| What it measures | $\mathcal{L}(\Delta f)$, integrated jitter | $\Delta f/f_0$ drift vs temperature, time, voltage |
| Units | dBc/Hz, fs | ppm, ppb |
| Time scale | offset $\ge1$ Hz (sub-second fluctuation) | seconds—years (temperature cycling, aging) |
| Physical origin | tank thermal noise ($kT\omega_0/4EQ\Delta\omega^2$), amp's $F$ and flicker | cut's temperature coefficient, stress relaxation, electrode/package contamination migration (aging, industry-convention qualitative) |
| What can fix it | higher $Q$/larger $P$/cleaner amp; **cannot be fixed downstream in the chain** (Step 1) | compensation (TCXO), oven (OCXO), calibration/discipline (GPS-disciplined) |
| Damage to the system | eye closure, BER, ADC SNR (fast jitter) | frequency drifting out of the receive window, PLL/CDR pull-in failure, timestamp drift |

- **The oven and compensation network don't move $\mathcal{L}(f)$**: OCXO's heater suppresses
  drift on an "hour—day" scale, with no effect at all on the 1 kHz offset skirt (the physics
  there is Step 3's $kT/(E\cdot Q)$); conversely, an ever-cleaner buffer cannot rescue aging.
  **Each axis is fixed with its own means, at its own cost.**
- Aging magnitude (industry convention): XO/TCXO first-year $\sim\pm(0.5\ldots5)$ ppm/year; OCXO
  can reach ppb/day–ppb/year. It is **deterministic slow drift**, not random phase noise.
- **The bridge between the two axes is Allan deviation**
  ([allan_variance](/02_foundations/allan_variance)): the short-$\tau$ region (white/flicker
  PM/FM) corresponds to the various slope segments of $\mathcal{L}(f)$, while the upturn at long
  $\tau$ (random-walk FM, drift $\propto\tau^{+1}$) is where temperature and aging enter — a
  single ADEV plot shows the handoff point between both axes at once. That's also why a
  reference's datasheet often gives an $\mathcal{L}(f)$ table, an ADEV table, and an aging table
  together: **three tables, three time scales, none dispensable**.

## Design-knob checklist (how to choose/use a reference)

| Knob | Where it acts | Cost/limit |
|---|---|---|
| Reference grade (XO→TCXO→OCXO) | Directly moves the low-offset anchor (Step 1: in-band $=\mathcal{L}_{ref}+20\log_{10}N$, no cure downstream) | Cost, power (OCXO oven is watt-level), size; TCXO/OCXO mainly buy the slow axis |
| Reference frequency $f_{ref}$ (lower $N$) | In-band floor $\propto N^2$ ([clock_chain_budget](/06_design_insights/clock_chain_budget) rule 3) | The $f\cdot Q$ see-saw: resonator close-in $\propto f_0^2 f_{out}^2$ (Step 6), optimum at a few tens of MHz |
| Drive level $P_{diss}$ | $\mathcal{L}\propto1/P$ (Step 3, Step 5 form) | Overdriving the crystal → nonlinearity, stress, accelerated aging (industry convention); datasheet has a max-drive spec |
| Loop bandwidth $f_n$ | Sets "how far to trust the reference, where to hand off to the VCO" (crossover-point method, 25.2 kHz of Example 1) | Full trade-off in [pll_noise_budget](/06_design_insights/pll_noise_budget) (U-shaped curve) |
| Output buffer/fanout | Floor is clamped by it (rule 4, power addition) | Even a great OCXO is ruined by one noisy buffer stage ([clock_chain_budget](/06_design_insights/clock_chain_budget) rule 4) |
| Quartz vs MEMS | Phase noise vs shock/reliability/programmability trade-off (Step 6) | MEMS in-band is the PLL floor; quartz is vulnerable to vibration (vibration sensitivity, industry convention) |

## Connection to SerDes

- A TX PLL's in-band (inside loop BW) is exactly reference $+20\log_{10}N$ — the reference's
  close-in determines the residual jitter of the TX clock at the **edge** of the CDR tracking
  bandwidth; anything fully inside the CDR bandwidth gets tracked out at the receiver
  ([serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)), so SerDes is
  relatively tolerant of the reference's $\mathcal{L}(10\,\text{Hz})$ but sensitive to the
  10 kHz–few-MHz "handoff band" — right around Example 1's crossover point (25.2 kHz).
- Systems without CDR tracking (ADC/DAC sampling, radar) get no such exemption: aperture jitter
  integrates up from low offset, and the reference's close-in goes directly into SNR
  ([adc_aperture_jitter](/06_design_insights/adc_aperture_jitter)).
- The slow axis bites too: the reference's ppm offset eats into the CDR's pull-in/tracking range
  and the SSC (spread-spectrum clocking) budget — this is Step 7's "two axes" made concrete in
  SerDes.

## Applicability and failure conditions

| Condition | When it holds | What happens when it fails |
|---|---|---|
| Thermal-only, $F=1$ idealization (Steps 3, 4) | $1/Q^2$, $E\cdot Q$ scaling holds cleanly | Real close-in is often dominated by the sustaining amp's flicker ($1/f^3$), floor clamped by the buffer — the numbers here are the **resonator-physics lower bound** |
| BVD equivalent near series resonance | crystal ≈ an LC with extreme $Q$; the full tank_Q toolkit applies | Far from resonance, at overtone/spurious modes, or where the $C_0$ parallel path dominates, the single-LC model fails |
| Drive level within datasheet range | $\mathcal{L}\propto1/P$ applies | Overdrive: nonlinearity, activity dip, accelerated aging; underdrive: poor startup margin (industry convention) |
| Small-angle approximation, $\Delta f$ well beyond linewidth | $\mathcal{L}=\tfrac12S_\phi$, Leeson $1/f^2$ skirt | Very close to the carrier it turns Lorentzian (crystal linewidth at the $10^{-10}$ Hz level, practically never measurable there; [lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth)) |
| Measurement noise floor low enough | Datasheet curve is trustworthy | Measuring a low-noise reference requires cross-correlation, otherwise you measure the instrument ([measurement_and_spurs](/06_design_insights/measurement_and_spurs)) |
| MEMS: look at system output | in-band = PLL floor, resonator buys the close-in anchor and stability | Reading MEMS output as a "bare-resonator Leeson skirt" is entirely wrong (Step 6) |

## Key takeaways

- **The reference is the low-offset anchor**: in-band $\mathcal{L}_{out}=\mathcal{L}_{ref}+20\log_{10}N$
  ([clock_chain_budget](/06_design_insights/clock_chain_budget) rule 3), and nothing downstream
  can rescue its close-in; in the worked chain, 65.9% of the jitter power came from the ref
  $\times N^2$ floor.
- **Crystal = LC with extreme $Q$** (BVD: $L_m\sim$ mH, $C_m\sim$ fF, $Q\sim10^4$–$10^6$,
  industry-convention magnitude); ISF shape unchanged ($\Gamma\approx-\sin$,
  $\Gamma_{rms}=1/\sqrt2$), the entire advantage comes from $Q$ (stored energy vs loss).
- **Scaling derived from the site's bridges**: [P1] Eq.(21) + $4kT/R_p$ + the $Q$ definition ⇒
  $\mathcal{L}_{lin}=\dfrac{kT\,\omega_0}{4E_{stored}Q\,\Delta\omega^2}=\dfrac{kT}{P_{diss}}\big(\tfrac{\omega_0}{2Q\Delta\omega}\big)^2$;
  close-in $\mathcal{L}$ and the Lorentzian linewidth both $\propto1/Q^2$; the real lever is the
  $E\cdot Q$ product (crystal example: 7.96 nJ vs 0.507 pJ, $E\cdot Q$ differs by 79.0 dB,
  same-offset $\mathcal{L}$ differs by 95.9 dB).
- **Worked block**: $Q=5\times10^4$@100 MHz vs $Q=10$@5 GHz — corner at 1 kHz vs 250 MHz;
  same-offset Leeson term differs by 104.95 dB (1 kHz), 67.96 dB (100 kHz); after normalizing to
  the same carrier ($-33.98$), still wins by 71.0/34.0 dB, but the advantage shrinks with
  offset — far-out has to be handed back to the VCO.
- Typical magnitudes (industry convention, external): XO floor $-150$ to $-165$, OCXO is king of
  close-in, the TCXO/OCXO ladder is mainly on the **slow axis** (ppm); floor is set by
  amp/buffer ($kT/P$ level), not $Q$.
- **MEMS**: the $f\cdot Q\sim10^{13}$ Hz magnitude see-saw ⇒ output close-in
  $\propto f_0^2f_{out}^2$ (a 10× drop in resonator frequency nets 20 dB) ⇒ the
  MHz-resonator + fractional-N PLL architecture; in-band is the PLL floor, buying stability,
  shock resistance, and programmability.
- **Two spec axes**: dBc/Hz (fast axis, set by $Q$/$P$/amp, cannot be fixed downstream) and ppm
  (slow axis, fixable by compensation/oven/discipline); the bridge is ADEV
  ([allan_variance](/02_foundations/allan_variance)).
- Source discipline: [P1] Eq.(21) (within the 5 PDFs, already verified) + the site's tank_Q
  bridge; Leeson shaping = [E1] (external); crystal/MEMS equivalent circuit and typical numbers
  = industry-convention order-of-magnitude (external, not among the five source PDFs, no
  fabricated citations).

## Further reading

- The three forms of $Q$, $4kT/R_p$, the $Q\leftrightarrow\Gamma_{rms}/q_{max}$ bridge (the
  foundation of this page's derivation): [tank_Q_and_energy_restoration](/02_foundations/tank_Q_and_energy_restoration)
- The four clock-chain accounting rules and the worked chain (the one where 65.9% comes from
  the ref floor): [clock_chain_budget](/06_design_insights/clock_chain_budget)
- The theoretical ceiling of phase noise × power (another "how many dB are left" perspective): [fom_limit](/06_design_insights/fom_limit)
- Full derivation of the Leeson model and the ISF cross-reference table: [derivation_leeson](/99_appendix/derivation_leeson)
- The U-shaped trade-off for optimal loop BW (the full version of Example 1's crossover point): [pll_noise_budget](/06_design_insights/pll_noise_budget)
- The bridge between slow axis/fast axis — the ADEV slope table: [allan_variance](/02_foundations/allan_variance)
- The Lorentzian near the carrier and the diffusion constant $D$: [lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth), [diffusion_dictionary](/03_isf_core_theory/diffusion_dictionary)
- Why measuring a low-noise reference requires cross-correlation: [measurement_and_spurs](/06_design_insights/measurement_and_spurs)

## External literature (not among the 5 downloaded PDFs)

- **Leeson shaping term**: [E1] D. B. Leeson, *"A Simple Model of Feedback Oscillator Noise
  Spectrum,"* Proc. IEEE, vol. 54, no. 2, pp. 329–330, Feb. 1966 (volume/issue/DOI verified in
  [references](/99_appendix/references)).
- **Crystal BVD equivalent circuit, $Q$/drive level/aging/$f\cdot Q$ product, typical numbers
  for XO/TCXO/OCXO/MEMS**: standard frequency-control industry knowledge and textbook content —
  this page consistently labels these as **industry convention, order-of-magnitude**, and does
  not cite specific papers or part numbers to avoid fabrication; for engineering use, follow
  vendor datasheets and the IEEE International Frequency Control Symposium literature (field
  name, not a citation of a specific paper).
- The 5 PDFs on this site provide the key that connects all of this back to ISF: [P1] Eq.(21),
  p.185 ($\Gamma_{rms}/q_{max}$ and $1/f^2$); [P2]–[P4] have no direct relation to this page.
