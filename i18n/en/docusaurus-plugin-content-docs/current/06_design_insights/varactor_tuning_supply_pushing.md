---
title: Tuning-line and supply-pushing phase noise
description: Define K_VCO=∂f0/∂V_tune and supply pushing K_push=∂f0/∂V_DD; derive how low-frequency noise voltage on the tune/supply node FM-modulates the carrier to give S_φ=K_VCO²·S_v/Δf² (white→1/f², 1/f→1/f³, paralleling the device flicker c0 mechanism); AM-PM from varactor C(V) nonlinearity; design knobs — split tuning, flat bias point, LDO/common-mode rejection; worked example K_VCO=50 MHz/V, 100 nV/√Hz @ 1 MHz, f0=5 GHz → L=-109 dBc/Hz; lab_38 measures K_push=2.936 GHz/V from first principles on the Level-1 ring and verifies it via FM sidebands (β ratio 1.002).
---

> **β**: This English translation is in beta — the Traditional-Chinese original is the authoritative version.

# Tuning-line and supply-pushing phase noise

**Prerequisites (read these first)**: [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) (white noise → $1/f^2$ via the $1/\Delta\omega^2$ integrator), [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion) ($1/f$ → $1/f^3$; this page draws the parallel), [phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise) (the AM-PM back door). This page assumes you already accept the main thread: "phase has no restoring force → noise integrates through $1/\Delta\omega^2$ into the skirt."

Everything in the ISF framework so far has been about the **device's own noise current** $i_n(t)$ injected directly into the tank node. But a real VCO (voltage-controlled oscillator — output frequency set by a control voltage) has two more phase-noise gates that **don't rely on the device's internal $i_n$ at all, but on jitter of an external voltage node**:

1. **tuning line**: you use a voltage $V_{tune}$ to tune the varactor (a varactor diode — bias changes its capacitance) and set $f_0$ to the desired channel. Any noise voltage $v_n$ on this line **directly FM-modulates** (frequency-modulates) the carrier.
2. **supply ($V_{DD}$)**: supply voltage variation changes the effective $f_0$ via the device operating point, parasitic capacitance, and similar paths — this is called **supply pushing** (supply voltage pushes the oscillation frequency around).

This page answers: **how do these two external voltage gates turn low-frequency noise voltage into close-in phase noise? Why does the mechanism look identical to device flicker's $1/f^3$? And how do design choices close these two gates down?**

> **Physical intuition (the punchline first)**: think of the VCO as a "voltage → frequency" converter with sensitivity $K_{VCO}=\partial f_0/\partial V_{tune}$ (Hz/V). A noise voltage $v_n(t)$ on the control node jitters the instantaneous frequency by $\Delta f(t)=K_{VCO}\,v_n(t)$. **Frequency is the derivative of phase, so phase is the integral of frequency** — this integrator is the exact same machine that turns $S_v$ (voltage noise) into the $1/\Delta\omega^2$ skirt in the ISF white-noise result: **literally the same integrator**. Hence: **white** noise on the tune line → $1/f^2$; **$1/f$** noise on the tune line → $1/f^3$. The larger $K_{VCO}$, the wider this gate opens; shrinking it (coarse tuning via switched-cap, fine tuning via varactor) and cleaning up $V_{tune}/V_{DD}$ (LDO, common-mode rejection) is the core of every design knob on this page.

The concrete circuit/topology/instrumentation details on this page — the varactor $C$–$V$ model, LDO/cross-coupled VCO topology specifics, measurement methods — belong to **standard RF IC design literature** (Razavi, Leeson, vendor datasheets); **not among the five source PDFs on this site**, and this page explicitly flags them "(external literature, not among the five source PDFs)." But the main thread — "voltage noise → FM → $1/\Delta\omega^2$ phase skirt" — follows **strictly from [P1]'s existing phase-integration concept** alone, which is what we do below.

## Step 1: define $K_{VCO}$ and supply pushing $K_{push}$

A VCO is by definition "output frequency varies with control voltage." Treat oscillation frequency $f_0$ as a function of control voltage $V_{tune}$ and supply $V_{DD}$, and do a first-order Taylor expansion about the operating point:

$$
f_0(V_{tune},V_{DD})\approx f_{0,op}+\underbrace{\frac{\partial f_0}{\partial V_{tune}}}_{K_{VCO}}\,(V_{tune}-V_{op})+\underbrace{\frac{\partial f_0}{\partial V_{DD}}}_{K_{push}}\,(V_{DD}-V_{DD,op}).
$$

The two slopes are this page's two protagonists:

$$
K_{VCO}\equiv\frac{\partial f_0}{\partial V_{tune}}\qquad(\text{units Hz/V})
$$

$$
K_{push}\equiv\frac{\partial f_0}{\partial V_{DD}}\qquad(\text{units Hz/V})
$$

- **$K_{VCO}$ (VCO gain, also called tuning sensitivity)**: how far frequency moves per 1 V of control voltage. It sets the **tuning range** (the frequency span it can sweep) and also the **gain applied to tune-line noise** — the core tension on this page: $K_{VCO}$ must be large enough to cover the band, yet small enough not to amplify noise.
- **$K_{push}$ (supply pushing coefficient)**: how far frequency moves per 1 V of supply variation. Ideally the VCO is supply-immune ($K_{push}=0$); in practice the supply alters $f_0$ via device bias point, parasitic capacitance, and effective swing, so $K_{push}\ne0$. (Vendors often quote a pushing figure in $\text{Hz/V}$ or $\text{ppm/V}$ — external literature, not among the five source PDFs.)
- **Dimension check**: $[\partial f_0/\partial V]=\text{Hz}/\text{V}$ ✓. Both have the same dimension and are **exactly parallel** mathematically — every derivation below applies verbatim to tune line and supply; just swap $K_{VCO},v_{n,tune}$ for $K_{push},v_{n,DD}$.
- **Physical meaning**: these two coefficients connect the "external voltage world" to the "frequency world." They are **designer-controllable** — unlike the device's $i_n$ (fixed by process/physics), $K_{VCO}$ and $K_{push}$ are outcomes of topology and bias choices.

> **Division of labor with ISF $\Gamma$**: ISF $\Gamma(\omega_0\tau)$ handles "a current impulse $\Delta q$ injected at what phase of the tank node → how much phase shift"; $K_{VCO}/K_{push}$ handles "a quasi-static (slow relative to the carrier) control/supply voltage → how much frequency shift." Tune/supply noise is slow (offset $\ll f_0$), so it **need not go through ISF's per-impulse phase projection** — it takes the more direct FM route: "voltage → frequency → integrate into phase." Both routes ultimately converge on the same $1/\Delta\omega^2$ integrator (see end of Step 2) — exactly the parallel this page draws.

## Step 2: how voltage noise FM-modulates the carrier → $S_\phi=K_{VCO}^2 S_v/\Delta\omega^2$

Let the tune node carry a **low-frequency** noise voltage $v_n(t)$ (offset frequency $\Delta\omega\ll\omega_0$, so it's nearly constant over one carrier cycle — the quasi-static assumption holds). Derive step by step.

**Step 2.1: voltage noise → instantaneous frequency deviation.** By the definition of $K_{VCO}$, the instantaneous oscillation frequency jitters with $v_n$:

$$
\Delta f(t)=K_{VCO}\,v_n(t)\qquad\Longleftrightarrow\qquad \Delta\omega_{inst}(t)=2\pi K_{VCO}\,v_n(t).
$$

- **Dimension check**: $\text{Hz/V}\times\text{V}=\text{Hz}$ ✓ (the angular-frequency version, multiplied by $2\pi$, gives rad/s ✓).
- This is **FM (frequency modulation)**: the control voltage directly modulates the carrier's instantaneous frequency.

**Step 2.2: frequency is the derivative of phase → phase is the integral of frequency.** The excess phase $\phi(t)$ is by definition "the time integral of the instantaneous frequency's deviation from nominal":

$$
\phi(t)=\int^{t}\Delta\omega_{inst}(t')\,dt'=2\pi K_{VCO}\int^{t}v_n(t')\,dt'.
$$

- **This integrator is the key point**: it is the **same integrator** [P1] Eq.(11)/(13) uses to integrate $i_n$ into $\phi$ — only here the integrand is not "$\Gamma\cdot i_n$" but "$K_{VCO}\cdot v_n$." **Integration = multiply by $1/(j\Delta\omega)$ in the frequency domain** (basic signals-and-systems), so power multiplies by $1/\Delta\omega^2$ — the next step relies on exactly this.
- **Physical meaning**: phase has no restoring force ([phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise), Step 1), so a "slowly drifting frequency" gets **accumulated indefinitely** into an ever-growing phase offset — the closer the offset $\Delta\omega$ is to the carrier, the larger the integrator gain $1/\Delta\omega$, and the higher the skirt.

**Step 2.3: take the PSD (the integrator is $1/\Delta\omega^2$ in the power domain).** For an LTI system $\phi=\mathcal{H}\,v$, the effect on input PSD is $S_\phi=|\mathcal{H}(j\Delta\omega)|^2 S_v$. Here $\mathcal{H}=2\pi K_{VCO}/(j\Delta\omega)$, so $|\mathcal{H}|^2=(2\pi K_{VCO})^2/\Delta\omega^2$:

$$
\boxed{\ S_\phi(\Delta\omega)=\frac{(2\pi K_{VCO})^2\,S_v(\Delta\omega)}{\Delta\omega^2}=\frac{K_{VCO}^2\,S_v(\Delta\omega)}{\Delta f^2}\ }
$$

The right-hand form uses $\Delta\omega=2\pi\Delta f$ to cancel the $2\pi$'s (numerator $(2\pi)^2$, denominator $(2\pi)^2$), so **computing in Hz is cleaner**: $S_\phi=K_{VCO}^2 S_v/\Delta f^2$.

- **Dimension check**: $\dfrac{(\text{Hz/V})^2\cdot(\text{V}^2/\text{Hz})}{\text{Hz}^2}=\dfrac{\text{Hz}^2/\text{Hz}}{\text{Hz}^2}=\dfrac{1}{\text{Hz}}$, and phase is dimensionless (rad), so $S_\phi$ is $\text{rad}^2/\text{Hz}$ ✓. (Strictly, the "dimensionless phase" carried by $K_{VCO}^2$ is implicit; FM phase is inherently dimensionless.)
- **Side by side with the ISF white-noise result** — [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)'s signature formula $S_\phi=\dfrac{\Gamma_{rms}^2}{q_{max}^2}\dfrac{\overline{i_n^2}/\Delta f}{\Delta\omega^2}$ and this page's $S_\phi=\dfrac{(2\pi K_{VCO})^2 S_v}{\Delta\omega^2}$ **both have $\Delta\omega^2$ in the denominator**. The device-noise version's "conversion gain" is $\Gamma_{rms}/q_{max}$ (A → rad); the tune-line version's is $2\pi K_{VCO}$ (V → rad/s, then integrated). **Same $1/\Delta\omega^2$ integrator, different entry point** — this is the structural isomorphism this page wants you to remember.

**Step 2.4: apply SSB phase noise (small-angle approximation).** Using the site-wide convention $\mathcal{L}(\Delta f)\approx\tfrac12 S_\phi(\Delta f)$ (spec Section 3, Eq. 16):

$$
\mathcal{L}(\Delta f)=10\log_{10}\!\left[\frac{1}{2}\cdot\frac{K_{VCO}^2\,S_v(\Delta f)}{\Delta f^2}\right]\qquad(\text{dBc/Hz}).
$$

The supply version is completely parallel: substitute $K_{VCO}\to K_{push}$, $S_v\to S_{v,DD}$ (supply-voltage noise PSD). **The two gates' contributions are independent sources, so powers add**: $S_\phi^{tot}=\dfrac{K_{VCO}^2 S_{v,tune}+K_{push}^2 S_{v,DD}}{\Delta f^2}+(\text{the device-ISF contribution})$.

## Step 3: white tune-line noise → $1/f^2$; $1/f$ tune-line noise → $1/f^3$ (paralleling device $c_0$)

Step 2's $S_\phi\propto S_v/\Delta\omega^2$ carries the tune line's **spectral shape** through unchanged, then multiplies by $1/\Delta\omega^2$. Two cases:

**Case A — tune line is white noise ($S_v=$ constant):** e.g. series-resistor thermal noise, wideband buffer noise. Then

$$
S_\phi=\frac{K_{VCO}^2\,S_{v,0}}{\Delta f^2}\ \propto\ \frac{1}{\Delta f^2}\quad\Rightarrow\quad -20\ \text{dB/decade}\ (1/f^2).
$$

This has **exactly the same slope, exactly the same mechanism** as device white noise's $1/f^2$ via ISF (both: white entry → $1/\Delta\omega^2$ integrator).

**Case B — tune line is $1/f$ noise ($S_v=k_v/\Delta f$):** e.g. low-frequency flicker from a charge pump / bandgap / LDO reference, or $1/f$ in the varactor bias circuit. Then

$$
S_\phi=\frac{K_{VCO}^2}{\Delta f^2}\cdot\frac{k_v}{\Delta f}=\frac{K_{VCO}^2\,k_v}{\Delta f^3}\ \propto\ \frac{1}{\Delta f^3}\quad\Rightarrow\quad -30\ \text{dB/decade}\ (1/f^3).
$$

**This is precisely the "external-voltage version" of the device flicker mechanism.** Put the two $1/f^3$ paths side by side:

| Mechanism | Entry (low-frequency source) | Upconversion "gate" | $1/f^3$ formula skeleton |
|---|---|---|---|
| **device flicker** ([P1] Eq.(23)) | device $1/f$ current $\overline{i_n^2}\,\omega_{1/f}/\Delta\omega$ | ISF's DC term $c_0$ | $\mathcal{L}\propto\dfrac{c_0^2}{q_{max}^2}\dfrac{\overline{i_n^2}/\Delta f}{\Delta\omega^2}\dfrac{\omega_{1/f}}{\Delta\omega}$ |
| **tune/supply $1/f$** (this page) | control-voltage $1/f$ noise $S_v=k_v/\Delta f$ | VCO gain $K_{VCO}$ (or $K_{push}$) | $\mathcal{L}\propto K_{VCO}^2\,\dfrac{k_v}{\Delta f^3}$ |

- **Where the parallel lies**: the device version's "gate" is ISF's DC Fourier coefficient $c_0$ ([flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion), Step 2: "$c_0$ is flicker's only gate to the carrier"); the tune-line version's "gate" is $K_{VCO}$. **The role $K_{VCO}$ plays in the external-voltage world is exactly the role $c_0$ plays in the device-current world** — both are conversion gains that "connect a low-frequency source to the $1/\Delta\omega^2$ integrator," and both enter $\mathcal{L}$ **squared** ($c_0^2$ vs $K_{VCO}^2$).
- **The difference (stated honestly)**: the device version's $c_0$ can be pushed close to 0 via **waveform symmetry** (this rescues flicker); the tune-line version's $K_{VCO}$ **cannot be zeroed** (zero means the frequency can't be tuned at all) — it can only be **shrunk** (split tuning) or have its **entry $S_v$ cleaned up** (LDO). So this gate is "permanently half-open," which makes it a design problem that demands direct attention.
- **Slope mnemonic**: each extra $1/\Delta\omega$ factor in the denominator adds $-10$ dB/dec. White entry + integrator = $1/\Delta\omega^2$ ($-20$); $1/f$ entry (one extra $1/\Delta\omega$) + integrator = $1/\Delta\omega^3$ ($-30$). Identical bookkeeping to the device side.

## Step 4: varactor $C(V)$ nonlinearity → AM-PM

So far $K_{VCO}$ has been treated as constant. But the varactor is inherently a **nonlinear capacitor** $C(V)$ — this opens a second, more subtle gate: **AM-PM conversion** (amplitude modulation converted to phase modulation), the back door discussed in [phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise), Step 4.

Mechanism chain (each link uses an existing concept):

1. **Frequency is set by the tank's total capacitance**: LC oscillation $f_0=\dfrac{1}{2\pi\sqrt{L\,C_{tot}}}$, where $C_{tot}$ includes the varactor's $C(V)$.
2. **The varactor sees "bias + oscillation swing"**: the node voltage is $V_{tune}+v_{osc}(t)$; a sinusoidal swing of amplitude $A$ sweeps across the $C(V)$ curve every cycle.
3. **Nonlinearity → effective capacitance varies with swing**: because $C(V)$ is curved, the **average effective capacitance** $\bar C(A)$ over one cycle changes with amplitude $A$ (Taylor-expand $C(V)$ about the bias point; the second-order term $\tfrac12 C''(V_{tune})\langle v_{osc}^2\rangle$ is proportional to $A^2$ and nonzero). Hence $f_0$ becomes a function of amplitude, $f_0(A)$.
4. **This is exactly $\partial\omega/\partial A\ne0$**: amplitude noise $\Delta A$ (which would normally be squashed by the limit cycle's restoring force) leaks into frequency/phase noise via $\partial f_0/\partial A$, then gets **permanently accumulated** by Step 2's integrator into a close-in skirt.

$$
\Delta\omega_{AM\text{-}PM}=\frac{\partial\omega_0}{\partial A}\,\Delta A,\qquad \frac{\partial\omega_0}{\partial A}\propto C''(V_{tune})\ \ (\text{varactor curvature}).
$$

- **Physical meaning**: amplitude noise that was originally "suppressed" ([phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise) argues amplitude has a restoring force) escapes through this varactor-curvature back door, **coming back to life as long-lived phase noise** — in particular, it upconverts the device's $1/f$ amplitude fluctuations into the close-in region, worsening $1/f^3$.
- **Key design corollary**: AM-PM is proportional to $C''(V_{tune})$ (curve **curvature**), not $C'$ (slope, which is $K_{VCO}$). So biasing at the **inflection/flat point of $C(V)$** can drive $C''\approx0$, greatly reducing AM-PM — a **different knob** from "shrink $K_{VCO}$" (one controls curvature, the other controls slope).
- **Units/dimension**: $\partial\omega_0/\partial A$ is $(\text{rad/s})/\text{V}$; multiplied by amplitude noise $\Delta A$ (V) gives rad/s, then integrates into phase ✓.
- **Detailed amplitude-modulation and large-signal analysis is the main subject of [P4] (advanced)**; the exact closed form of varactor $C(V)$ belongs to device literature (external literature, not among the five source PDFs). This page only connects the chain to the existing AM-PM concept.

## Step 5: design knobs (closing both gates)

Translate the physics above directly into actionable knobs. Each knob states **which quantity it acts on**.

- **Split tuning — shrinks $K_{VCO}$.** The single most important technique (external literature, not among the five source PDFs). Split tuning into two layers:
  - **coarse: switched-capacitor bank** (an array of switched capacitors, switched in/out by a digital code). It selects the band with a **digital code**, providing most of the tuning range, but is **immune to continuous voltage noise** (the code doesn't jitter, so the capacitance doesn't jitter).
  - **fine: varactor**, responsible only for continuous fine-tuning within a small sub-band.
  - Effect: total tuning range = coarse (digital, noise-free) ⊕ fine (small range), and the **fine varactor's $K_{VCO}$ drops sharply because it only spans a small sub-band**. By Step 2's $S_\phi\propto K_{VCO}^2$, halving $K_{VCO}$ **cuts the tune-line phase-noise contribution by 6 dB**. This is the standard way to untangle the "range vs. noise" tension.
- **Bias at the flat point of $C(V)$ — suppresses AM-PM (controls $C''$).** Choose the varactor operating point so $C''(V_{tune})\approx0$ (small curvature), driving $\partial\omega/\partial A\to0$ and closing the AM-PM back door. Note this is a different knob from shrinking $K_{VCO}$: the flat point suppresses **second-order curvature**, not first-order slope.
- **Supply regulation / LDO — suppresses the $S_{v,DD}$ entry (external literature, not among the five source PDFs).** To combat supply pushing: place an **LDO (low-dropout regulator)** ahead of the VCO to filter a dirty supply into a clean local supply, reducing $S_{v,DD}$ (the supply-noise PSD reaching the VCO) by tens of dB. By the supply-side formula $S_\phi\propto K_{push}^2 S_{v,DD}$, reducing $S_{v,DD}$ reduces phase noise proportionally. You can also reduce $K_{push}$ itself (topology-level: symmetric bias, less supply-to-swing modulation).
- **Common-mode rejection — makes a differential VCO immune to common-mode supply/substrate noise.** On a differential tank, supply/substrate noise mostly appears as a **common-mode** disturbance; good differential symmetry keeps common-mode disturbances from converting to differential-mode frequency shifts (ideally $K_{push,CM}\to0$). This shares its origin with [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion) Step 6's differential concept, but here it combats **external common-mode voltage** rather than device $c_0$.
- **Clean $V_{tune}$ routing — suppresses the $S_{v,tune}$ entry.** Loop-filter resistor thermal noise, charge-pump $1/f$, and bandgap reference noise all feed into $V_{tune}$; these are the physical origin of the "in-band" terms in [pll_noise_budget](/06_design_insights/pll_noise_budget). Within a PLL, the loop bandwidth also determines how much this tune-line noise gets high-pass/low-pass filtered.

> **Design rule of thumb (in one line)**: the phase noise from these two gates = (conversion gain $K^2$) × (entry voltage noise $S_v$) × ($1/\Delta f^2$ integrator). Each of the three factors has its own knob: suppress $K$ with **split tuning / symmetric topology**, suppress $S_v$ with **LDO / clean reference / low-noise loop filter**, and suppress the curvature-driven AM-PM with a **flat bias point**.

## Worked example (with units + dimension check)

> **Example G (tune-line white noise → $\mathcal{L}$)**: $K_{VCO}=50$ MHz/V, tune-line voltage noise $100$ nV$/\sqrt{\text{Hz}}$ (i.e. $\sqrt{S_v}=100$ nV$/\sqrt{\text{Hz}}$) at $\Delta f=1$ MHz offset, $f_0=5$ GHz. Find $\mathcal{L}(1\,\text{MHz})$.

**Step 1 (square $\sqrt{S_v}$ into a PSD)**:

$$
S_v=(100\ \text{nV}/\sqrt{\text{Hz}})^2=(10^{-7}\ \text{V}/\sqrt{\text{Hz}})^2=10^{-14}\ \text{V}^2/\text{Hz}.
$$

**Step 2 (voltage noise → frequency-deviation density, for intuition)**: the rms density of frequency deviation $=K_{VCO}\sqrt{S_v}=5\times10^7\ \text{Hz/V}\times10^{-7}\ \text{V}/\sqrt{\text{Hz}}=5\ \text{Hz}/\sqrt{\text{Hz}}$. In other words, at 1 MHz offset this tune line jitters the frequency by "5 Hz per $\sqrt{\text{Hz}}$."

**Step 3 (apply Step 2's $S_\phi$, in Hz form)**:

$$
S_\phi=\frac{K_{VCO}^2\,S_v}{\Delta f^2}=\frac{(5\times10^{7})^2\times10^{-14}}{(10^{6})^2}=\frac{(2.5\times10^{15})\times10^{-14}}{10^{12}}=\frac{25}{10^{12}}=2.5\times10^{-11}\ \text{rad}^2/\text{Hz}.
$$

**Step 4 (SSB)**: $\mathcal{L}=\tfrac12 S_\phi=1.25\times10^{-11}$, take $10\log_{10}$:

$$
\mathcal{L}(1\,\text{MHz})=10\log_{10}(1.25\times10^{-11})=-109.0\ \text{dBc/Hz}.
$$

- **Result**: $\mathcal{L}(1\,\text{MHz})\approx-109$ dBc/Hz — **this single tune-line white-noise source alone** contributes $-109$ dBc/Hz. Compared with the canonical "single device white-noise source" Example B ($-148$ dBc/Hz, [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)), the tune line is **nearly 40 dB higher** at the same offset — showing that **one poorly handled tune line can easily dominate a whole VCO's $1/f^2$ region**, which is exactly why split tuning / a clean $V_{tune}$ matter so much.
- **Dimension check**: $\dfrac{(\text{Hz/V})^2\cdot(\text{V}^2/\text{Hz})}{\text{Hz}^2}=\dfrac{\text{Hz}^2\cdot\text{V}^{-2}\cdot\text{V}^2\cdot\text{Hz}^{-1}}{\text{Hz}^2}=\text{Hz}^{-1}$ → $S_\phi$ is $\text{rad}^2/\text{Hz}$ ✓.
- **Where did $f_0=5$ GHz go? (honesty note)**: this formula's $\mathcal{L}$ **does not explicitly contain $f_0$** — $f_0$ only tells you which carrier this skirt sits on; the skirt's $1/f^2$ height is set by $K_{VCO}^2 S_v/\Delta f^2$, independent of $f_0$. $f_0$ genuinely enters when converting to timing jitter ($\Delta t=\Delta\phi/2\pi f_0$, see [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter)), or when expressing $K_{VCO}/f_0$'s relative sensitivity in $\text{ppm/V}$. $f_0=5$ GHz is given so you know this is a 5 GHz VCO, but don't force it into the $\mathcal{L}$ formula.

```python
import math
K_vco = 50e6          # Hz/V
S_v   = (100e-9)**2   # V^2/Hz  (100 nV/sqrt(Hz))
df    = 1e6           # Hz offset
S_phi = K_vco**2 * S_v / df**2          # rad^2/Hz
L     = 10*math.log10(0.5*S_phi)        # SSB, L = (1/2) S_phi
print(S_phi, L)        # -> 2.5e-11 rad^2/Hz, -109.03 dBc/Hz
```

> **Example H (supply pushing → $\mathcal{L}$, parallel verification)**: $K_{push}=2$ MHz/V, supply noise $1\ \mu\text{V}/\sqrt{\text{Hz}}$ ($S_{v,DD}=10^{-12}\ \text{V}^2/\text{Hz}$) at $\Delta f=1$ MHz. Find the supply contribution to $\mathcal{L}$.

$$
S_\phi=\frac{K_{push}^2 S_{v,DD}}{\Delta f^2}=\frac{(2\times10^{6})^2\times10^{-12}}{(10^{6})^2}=\frac{4\times10^{12}\times10^{-12}}{10^{12}}=4\times10^{-12}\ \text{rad}^2/\text{Hz},
$$

$$
\mathcal{L}=10\log_{10}(\tfrac12\times4\times10^{-12})=10\log_{10}(2\times10^{-12})=-117.0\ \text{dBc/Hz}.
$$

- **Intuition**: even though $K_{push}$ is 25x smaller than $K_{VCO}$, a "mere" $1\ \mu\text{V}/\sqrt{\text{Hz}}$ dirty supply still contributes $-117$ dBc/Hz. Add an LDO that cuts $S_{v,DD}$ by 20 dB (a 10x reduction in voltage noise), and this contribution drops 20 dB to $-137$ dBc/Hz — the direct payoff of an LDO against supply pushing.
- **Dimension check**: same as Example G, $\text{Hz}^{-1}$ → $\text{rad}^2/\text{Hz}$ ✓.

```python
# supply pushing parallel version: same formula, K_vco->K_push, S_v->S_vdd
K_push, S_vdd, df = 2e6, (1e-6)**2, 1e6
S_phi = K_push**2 * S_vdd / df**2
print(10*math.log10(0.5*S_phi))   # -> -117.0 dBc/Hz
```

## K_push from first principles (Level-1 ring measurement, lab_38)

Example H's $K_{push}=2$ MHz/V was a **given** representative value (a well-cared-for LC-VCO grade number). This section gives nothing: take the **MOS Level-1 (Shichman-Hodges square-law) 3-stage ring** from [lab_32](/04_simulation_labs/lab_32_mos_level1_ring) and measure $K_{push}$ directly **by its definition** — first a static $V_{DD}$ sweep for the slope of $f_0(V_{DD})$, then a small superimposed ripple to verify Step 2's FM-integrator prediction. Honesty statement: this is **device-equation level (Level-1 square law, $\lambda=0$), NOT SPICE/BSIM/PDK**; the numbers belong to this toy ring, but the physics and the order-of-magnitude lesson are general. Full script: `simulations/lab_38_supply_pushing_ring.py` (the node equation reuses lab_32 bit-exactly, only promoting $V_{DD}$ to an argument; cross-check difference $0.0$ V/s).

### Static measurement: $f_0(V_{DD})$ sweep → $K_{push}$

Sweep $V_{DD}$ from 0.9 V to 1.1 V (25 mV grid); at each point let the ring reach steady oscillation and measure the period by threshold crossings:

| $V_{DD}$ [V] | 0.900 | 0.950 | 1.000 | 1.050 | 1.100 |
|---|---|---|---|---|---|
| $f_0$ [GHz] | 0.9394 | 1.0803 | 1.2252 | 1.3738 | 1.5255 |

$f_0(1.000\,\text{V})=1.2252$ GHz exactly reproduces lab_32 (same ring, same integrator). Central difference at 1.0 V:

$$
K_{push}=\left.\frac{\partial f_0}{\partial V_{DD}}\right|_{1.0\,\text{V}}=\frac{f_0(1.025)-f_0(0.975)}{0.05\ \text{V}}=2.936\ \text{GHz/V}
$$

(The 9-point quadratic-fit derivative gives 2.932 GHz/V, 0.1% apart — the slope extraction is self-consistent.) **Dimension check**: Hz ÷ V = Hz/V ✓.

**Why so large? A hand sanity check (step by step)**: the ring's frequency is $f_0=\dfrac{1}{2N\tau_D}$ (the concept of [P2] Eq.(15); this 2 is the circuit fact "two edges per period," not a bookkeeping convention), and each stage delay is $\tau_D\approx C_L\,\Delta V/I_D$, where the swing $\Delta V\propto V_{DD}$ and the drive current follows the square law $I_D\approx\tfrac{k'}{2}\tfrac{W}{L}(V_{DD}-V_T)^2$. Hence

$$
f_0\ \propto\ \frac{(V_{DD}-V_T)^2}{V_{DD}}\quad\Rightarrow\quad \frac{1}{f_0}\frac{\partial f_0}{\partial V_{DD}}=\frac{2}{V_{DD}-V_T}-\frac{1}{V_{DD}}
$$

(The 2 in the numerator is the square-law exponent — a physical origin, not a convention.) Plug in $V_{DD}=1.0$ V, $V_T=0.4$ V: $2/0.6-1/1.0=2.33\ \text{V}^{-1}$, times $f_0=1.2252$ GHz gives **2.859 GHz/V** — 2.6% from the measured 2.936 GHz/V; both magnitude and physics agree. **Dimension check**: $\text{V}^{-1}\times\text{Hz}=\text{Hz/V}$ ✓.

The normalized pushing is $K_{push}/f_0=2.40$ /V $=2.4\times10^6$ ppm/V. For contrast: an LC VCO's $f_0$ is set by the tank's $L\,C$ and the supply only **perturbs** it through parasitics and bias (typical pushing figures sit in the ppm/V to thousands-of-ppm/V range — external literature, not among the five source PDFs); a ring's $f_0$ **is** device current divided by capacitance — the supply sits directly inside the formula. **"A ring's supply pushing is inherently orders of magnitude larger than an LC's" is not folklore; it is a direct consequence of $f_0=1/(2N\tau_D)$.**

### Dynamic verification: 10 mV ripple → narrowband FM sidebands

Superimpose a sinusoidal ripple $V_r=10$ mV at $f_m=100$ MHz on $V_{DD}$. By Step 2's integrator, step by step:

$$
\Delta f(t)=K_{push}V_r\sin(2\pi f_m t)\quad\Rightarrow\quad\phi(t)=\int 2\pi\,\Delta f\,dt'=-\underbrace{\frac{K_{push}V_r}{f_m}}_{\beta}\cos(2\pi f_m t)
$$

The peak phase deviation (FM modulation index) is $\beta=K_{push}V_r/f_m$. **Dimension check**: $\dfrac{(\text{Hz/V})\cdot\text{V}}{\text{Hz}}=$ dimensionless (rad) ✓ — exactly the FM fundamental "frequency deviation ÷ modulation frequency = phase." Plug in the measured value:

$$
\beta_{pred}=\frac{2.936\times10^{9}\ \text{Hz/V}\times 0.01\ \text{V}}{10^{8}\ \text{Hz}}=0.2936\ \text{rad}.
$$

The simulation puts the ripple physically into the node equation, extracts $\phi(t)$ from threshold-crossing times, and fits a sinusoid: $\beta_{meas}=0.2942$ rad, **ratio 1.002** (modulation phase $-88.2°$, theory $-90°$: $\phi=\int\sin=-\cos$ ✓). The spectrum shows sidebands at $f_0\pm f_m$: measured $-16.31/-16.83$ dBc, against the narrowband-FM prediction $20\log_{10}(\beta/2)=-16.67$ dBc (exact Bessel value $20\log_{10}(J_1/J_0)=-16.55$ dBc). **Convention flag**: this $/2$ is **FM math** ($J_1/J_0\approx\beta/2$) — it is **not the same 2** as the SSB bookkeeping in $\mathcal{L}\approx\tfrac12 S_\phi$, nor the 4 in the denominator of [P1] Eq.(21). The 0.52 dB upper/lower sideband asymmetry is concurrent AM (the swing itself tracks $V_{DD}$, $m\approx V_r/V_{DD}=1\%$) — a supply-side miniature of Step 4's AM-PM issue; even the second-order sidebands at $f_0\pm2f_m$ ($-38.6/-39.8$ dBc) match $J_2/J_0$'s $-39.2$ dBc.

This deterministic single-tone experiment verifies **precisely** Step 2's integrator: a random $v_n(t)$ is nothing but a superposition of countless such tones (in PSD language), so "$\beta$ checks out" is equivalent to "$S_\phi=K_{push}^2S_v/\Delta f^2$ checks out."

```python
# lab_38 key numbers (reproduce with: PYTHONPATH=. python simulations/lab_38_supply_pushing_ring.py)
K_push = (1.2991e9 - 1.1523e9) / 0.05
print(f"{K_push:.3e}")   # -> 2.936e9 Hz/V (central difference @ 1.0 V)
beta   = K_push * 10e-3 / 100e6
print(round(beta, 4))         # -> 0.2936 rad (measured 0.2942, ratio 1.002)
```

![Supply pushing of the Level-1 ring: f0(VDD) sweep, ripple phase modulation, FM sidebands](/figures/supply_pushing_ring.png)

**How to read the figure**: (a) $f_0(V_{DD})$ is nearly a straight line (slightly curved); the red tangent's slope is $K_{push}$; (b) $\phi(t)$ extracted from threshold crossings (purple dots) with the sinusoidal fit; the red dashed lines $\pm\beta_{pred}$ are pure theory, not fitted; (c) the spectrum normalized to the carrier at 0 dB — the $\pm100$ MHz sidebands land on the predicted level, and the small peaks at $\pm200$ MHz are second-order FM sidebands. Parameters: $C_L=10$ fF/node, $N=3$, static sweep $dt=25$ fs, dynamic $dt=100$ fs, 150 ns record; runtime about 28 s.

> **Example I (end-to-end: measured $K_{push}$ × this page's formula)**: take Example H's same supply noise, $1\ \mu\text{V}/\sqrt{\text{Hz}}$ ($S_{v,DD}=10^{-12}\ \text{V}^2/\text{Hz}$) at $\Delta f=1$ MHz, but substitute this ring's measured $K_{push}=2.936$ GHz/V:
>
> $$
> S_\phi=\frac{K_{push}^2\,S_{v,DD}}{\Delta f^2}=\frac{(2.936\times10^{9})^2\times10^{-12}}{(10^{6})^2}=8.62\times10^{-6}\ \text{rad}^2/\text{Hz},
> $$
>
> $$
> \mathcal{L}(1\,\text{MHz})=10\log_{10}\!\big(\tfrac12\times8.62\times10^{-6}\big)=-53.7\ \text{dBc/Hz}.
> $$
>
> (The $\tfrac12$ here is the SSB small-angle convention $\mathcal{L}\approx\tfrac12S_\phi$, spec Section 3, Eq. 16.) **Dimension check**: $(\text{Hz/V})^2\cdot\text{V}^2/\text{Hz}\div\text{Hz}^2=\text{Hz}^{-1}$ → rad²/Hz ✓. This is **63.3 dB worse** than Example H's $-117.0$ dBc/Hz — exactly $20\log_{10}(2936/2)$, entirely from the square of $K_{push}$. That is the quantitative version of "an unregulated ring on a dirty supply is a disaster"; conversely, the $K^2$ is also good news: every 20 dB an LDO shaves off the voltage noise removes 20 dB of this phase-noise contribution.

### Interface with the ISF: the supply sees the "coherent sum of per-stage sensitivities"

In ISF language there is one key difference between device noise and supply noise:

- **device noise (each stage's own $i_n$)**: the $N$ stages' noise sources are **mutually independent**, so per-stage contributions add in **power** — this is [P2]'s bookkeeping for the ring analysis (one $\Gamma_{rms}^2$ share per stage).
- **supply (the $V_{DD}$ rail)**: the supply is a port **shared by all $N$ stages**. One low-frequency (quasi-static) supply disturbance changes **every stage's delay simultaneously and in the same direction** — whichever stage is switching gets sped up or slowed down by the same $v_n$, and within one period the delay changes of all $2N$ edges **accumulate with the same sign** into $\Delta T$. So the supply's effective sensitivity is the **coherent (amplitude) sum of the per-stage sensitivities**, and the **average (DC) component** of that sum is exactly $2\pi K_{push}$: for a slow disturbance, "some stage is being pushed at every instant," and the summed sensitivity never changes sign.
- Corollary 1: stacking $N$ independent sources scales as $\sqrt N$ (power addition); a coherent source scales as $N$ (amplitude addition) — supply noise is not merely "one more noise source": it **bypasses the statistical discount of independent sources**.
- Corollary 2: the DC term of the supply's effective sensitivity is inherently large (its role is that of $c_0$ in device-flicker upconversion), so the supply's $1/f$ noise upconverts to $1/f^3$ as in Step 3; but while the device version can push $c_0$ near 0 via **waveform symmetry** (lab_32's symmetric ring measured $c_0=0.0014$), the supply version **has no such card to play** — "every stage's delay tracks $V_{DD}$" is not something symmetry can cancel. The remaining cards are suppressing the entry (LDO) and suppressing $K_{push}$ itself (differential/regulated topologies, stage designs whose delay is first-order insensitive to $V_{DD}$ — external literature, not among the five source PDFs).

**Limitations (honestly)**: Level-1 square law, $\lambda=0$, a single lumped $C_L$, single point $N=3$ (no $N$-scaling verified); a real PDK ring's $K_{push}$ number will differ due to velocity saturation and short-channel effects (though it remains far larger than an LC's — external-literature experience), while this section's **method** (definition-based measurement + FM verification) and **structural conclusions** (coherent summing, the $K^2$ lever) stand.

## Validity and failure conditions

| Condition | When it holds | What breaks when it doesn't |
|---|---|---|
| Control/supply noise is slow ($\Delta\omega\ll\omega_0$, quasi-static) | $K_{VCO}/K_{push}$ constant, FM model holds | At high frequency (near $f_0$) must fall back to ISF/HTM's per-harmonic treatment |
| $K_{VCO}$ is approximately linear at the operating point | A single slope $\partial f_0/\partial V$ suffices | Strong varactor nonlinearity → $K_{VCO}$ varies with $V_{tune}$ and generates AM-PM (Step 4) |
| Small perturbation, linear phase | $S_\phi=K^2 S_v/\Delta f^2$ holds | Large voltage swing → higher-order FM sidebands, spectral distortion |
| AM-PM negligible ($C''\approx0$) | "FM only" approximation is good | Strong curvature → amplitude noise revives as phase noise; needs the [P4] APF framework |
| Sources independent | Powers add directly, $S_\phi^{tot}=\sum$ | Correlated sources (shared reference) need cross terms; common-mode rejection can help |

## Corresponding papers/formulas

- **The $1/\Delta\omega^2$ phase integrator** and its structural link to device white noise's $1/f^2$ and flicker's $1/f^3$: [P1] Eq.(11)/(13), p.182–183 (phase is the integral of noise), Eq.(21) p.185 ($1/f^2$), Eq.(23) p.185 ($1/f^3$, $c_0$ gate). This page draws the analogy "$c_0$ gate" ↔ "$K_{VCO}$ gate."
- **AM-PM / amplitude modulation**'s full framework: [P4] (APF, amplitude decay, advanced; see [phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise)).
- **$K_{VCO}/K_{push}$ definitions, split tuning, switched-cap bank, LDO, varactor $C(V)$, common-mode rejection, pushing figure** and other circuit/topology/instrumentation specifics: **standard RF IC design literature (external literature, not among the five source PDFs)** — Razavi's *RF Microelectronics*, the Leeson model, vendor datasheets.
- $\mathcal{L}\approx\tfrac12 S_\phi$: spec Section 3, Eq. 16 (small-angle PM).
- **$K_{push}$ first-principles measurement (lab_38)**: the ring frequency concept $f_0=1/(2N\tau_D)$ comes from [P2] Eq.(15), p.794; the device equations and the ring itself reuse lab_32 (Level-1 equation level, NOT SPICE/BSIM/PDK); narrowband FM's $J_1/J_0\approx\beta/2$ is standard communications-textbook material (external literature, not among the five source PDFs).

## Key takeaways

- **$K_{VCO}=\partial f_0/\partial V_{tune}$, $K_{push}=\partial f_0/\partial V_{DD}$** (both Hz/V): the conversion gains connecting the external-voltage world to the frequency world.
- Noise voltage $v_n$ on the tune/supply node **FM-modulates the carrier**: $\Delta f=K\,v_n$ → phase is the integral of frequency → **$S_\phi=K^2 S_v/\Delta f^2$** (using the **same $1/\Delta\omega^2$ integrator** as ISF white noise).
- **White tune-line noise → $1/f^2$**; **$1/f$ tune-line noise → $1/f^3$**. $K_{VCO}$'s role in the external-voltage world $=$ ISF's $c_0$'s role in the device-current world (both enter $\mathcal{L}$ squared), but $K_{VCO}$ cannot be zeroed, only shrunk.
- **Varactor $C(V)$ nonlinearity → AM-PM**: $\partial\omega/\partial A\propto C''(V_{tune})$, reviving suppressed amplitude noise as phase noise; a **flat bias point (small $C''$)** suppresses it (a different knob from shrinking $K_{VCO}$).
- Design knobs: **split tuning (coarse switched-cap + fine varactor, shrinks $K_{VCO}$)**, flat bias point (suppresses AM-PM), **LDO / clean reference (suppresses the $S_v$ entry)**, **common-mode rejection (combats supply/substrate common mode)**.
- Numbers: $K_{VCO}=50$ MHz/V, $100$ nV$/\sqrt{\text{Hz}}$ @ 1 MHz → $\mathcal{L}(1\,\text{MHz})=-109$ dBc/Hz (a single tune line alone can dominate the $1/f^2$ region); $\mathcal{L}$ does not explicitly contain $f_0$.
- **lab_38 first-principles measurement**: the Level-1 3-stage ring measures $K_{push}=2.936$ GHz/V ($2.4\times10^6$ ppm/V; the hand square-law model is 2.6% away); the 10 mV @ 100 MHz ripple FM verification gives $\beta_{meas}/\beta_{pred}=1.002$; with the same $1\ \mu\text{V}/\sqrt{\text{Hz}}$ supply, $\mathcal{L}=-53.7$ dBc/Hz — 63.3 dB worse than Example H. A ring's supply sees the "coherent sum of per-stage sensitivities," has no symmetry-zeroing card to play, and must rely on LDO/regulated topologies.

## Further reading

- The common origin of the $1/\Delta\omega^2$ integrator and white-noise $1/f^2$: [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)
- The $c_0$ → $1/f^3$ mechanism this page parallels: [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)
- The AM-PM back door and why amplitude noise is normally suppressed: [phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise)
- How tune-line noise is high-pass/low-pass filtered in the loop, and optimal loop BW: [pll_noise_budget](/06_design_insights/pll_noise_budget)
- The swing/$q_{max}$ lever (another independent knob): [tank_swing](/06_design_insights/tank_swing)
- Which knobs change $\Gamma_{rms}$ and which change $q_{max}$: [device_noise_mapping](/06_design_insights/device_noise_mapping)
- The Level-1 ring used by lab_38, and its ISF extraction: [lab_32_mos_level1_ring](/04_simulation_labs/lab_32_mos_level1_ring)
- The **high-frequency** entrance for supply/substrate noise — correlated noise only enters from near DC and $k\cdot N\cdot f_0$ ([P2] Eqs.(37)–(38) selection rule; this page's $K_{push}$ is precisely the DC tooth of that comb): [lab_34_correlated_supply](/04_simulation_labs/lab_34_correlated_supply)
