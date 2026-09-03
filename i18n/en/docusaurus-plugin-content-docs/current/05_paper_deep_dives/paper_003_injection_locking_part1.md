---
title: "[P3] Injection Locking & Pulling — Part I (Time-Synchronous Modeling)"
description: Hong–Hajimiri 2019 Part I deep dive — ISF-based time-synchronous model, generalized Adler equation, lock range, injection waveform design (advanced; core equations verified against the [P3] original).
---

> **β**: This English translation is in beta — the Traditional-Chinese original is the authoritative version.

# A General Theory of Injection Locking and Pulling in Electrical Oscillators—Part I

> **Prerequisites**: [paper_001](/05_paper_deep_dives/paper_001_general_theory_phase_noise) (the ISF definition and the Eq.(11) phase kick from [P1]), [fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf) (the Fourier harmonics $c_n$ of the ISF) | **Next**: [paper_004](/05_paper_deep_dives/paper_004_injection_locking_part2) (Part II: APF amplitude, transient, frequency division).

This is an **advanced** deep dive. It extends the ISF of [P1] from "phase noise of a free-running
oscillator" to "injection locking / pulling of an oscillator driven by an external signal."
Core result: a **single first-order differential equation** written in terms of the ISF
(the generalized Adler equation) predicts the lock range, the locked phase, and stability,
for **any** oscillator topology and **any** injection waveform — and from it follows a recipe
for designing the injection waveform that maximizes the lock range.

> **Scope of this page**: advanced deep-dive, **not a core teaching chapter**. The core equations (impulse-train Eq.(19)–(23), generalized Adler Eq.(26), (28)–(30),
> (33), (35)) have been verified against the original [P3] PDF. Make sure you have digested the ISF from [P1] ([paper_001](/05_paper_deep_dives/paper_001_general_theory_phase_noise)) before reading this.

## Citation

> **[P3]** B. Hong and A. Hajimiri, *"A General Theory of Injection Locking and Pulling in
> Electrical Oscillators—Part I: Time-Synchronous Modeling and Injection Waveform Design,"*
> IEEE J. Solid-State Circuits, vol. 54, no. 8, pp. 2109–2121, Aug. 2019.
> (file `BHongGenTheor-I_JSSC2019_Postprint.pdf`, paper_003)

## One-sentence contribution

The same ISF $\Gamma$ that computes phase noise also yields a topology-independent generalized Adler equation
that predicts the lock range, locked phase, and stability for any oscillator and any injection waveform,
and shows how to design the injection waveform to enlarge the lock range (claim C10).

## Why this paper matters

**Injection locking** means: when an oscillator is injected with an external signal whose frequency is
close to its own, it "synchronizes to the external signal" — its phase and frequency get captured.
When the frequency offset is too large to follow, the phase slips periodically and produces unwanted spurs;
this is **injection pulling**. The phenomenon is everywhere — PLLs, clock distribution, quadrature
generation, frequency division — both exploited and feared.

In 1946 **Adler** described the behavior of an LC oscillator under **weak, sinusoidal, near-free-running**
injection with a single first-order phase equation. [P3] identifies five major limitations of the Adler
equation (weak injection only, LC only, sinusoidal injection assumed, requires hard-to-measure
$Q$ and $I_{osc}$, and predicts a symmetric lock range), then **fully generalizes** it using the ISF:

- Replace the LC-only parameters $Q$ / $I_{osc}$ with $\Gamma$ — any oscillator whose ISF can be extracted qualifies.
- Allow **arbitrary injection waveforms** (not just sinusoids), so the injection waveform can be **designed** to maximize the lock range.
- Naturally produces an **asymmetric lock range** (common in real circuits, missed by Adler).
- Covers subharmonic / superharmonic locking (injection frequency near $\omega_0/m$ or $m\omega_0$).

## Main assumptions

Per paper_metadata (paper_003.assumptions):

1. **Oscillator autonomy and periodic time variance** (same foundation as the ISF).
2. Injection (perturbation) maps to phase through the ISF; amplitude is deferred to Part II (APF).
3. **Time-synchronous averaging**: time-synchronous averaging over one period.

> **Physical intuition**: phase noise feeds the perturbation machine random noise; injection feeds it
> a **deterministic, periodic injection current $i_{inj}$**. Same "ISF-weight-then-integrate" machine —
> when the input changes from random to deterministic, the output changes from statistics
> ($\Gamma_{rms}$, PSD) to deterministic phase dynamics (locking / slipping).

## Key equations

### Classical Adler equation (baseline)

**Original formula** ([P3] Sec. III (SURVEY OF EXISTING MODELS), around p.2111, cross-checked against Eq.(15) of the original):

$$
\frac{d\theta}{dt}=\omega_0-\omega_{inj}-\frac{\omega_0}{2Q}\frac{I_{inj}}{I_{osc}}\sin\theta
$$

In the simplified form of Section 3 of the site conventions ($\omega_L\equiv\dfrac{\omega_0}{2Q}\dfrac{I_{inj}}{I_{osc}}$,
$\Delta\omega_{inj}\equiv\omega_0-\omega_{inj}$):

$$
\frac{d\phi}{dt}=-\omega_L\sin\phi+\Delta\omega_{inj}
$$

**Meaning**: the injection-locking phase difference $\theta$ (or $\phi$) satisfies a first-order nonlinear ODE.
$\omega_L$ is the (half) lock range. **Locking** = existence of a steady-state solution $d\theta/dt=0$,
which requires $|\Delta\omega_{inj}|\le\omega_L$.

**Step-by-step (summary of the simplified LC derivation in [P3])**: write the injection current as the phasor
$i_{inj}=I_{inj}e^{j\omega_{inj}t}$, write KCL for the LC tank (the injection current must supply the
reactive current when the tank is detuned from resonance), take the real part under the weak-injection
($I_{inj}\ll I_{osc}$) and slow-phase ($|d\theta/dt|\ll\omega_{inj}$) approximations, and the equation above
follows. The steady-state solution gives the lock characteristic and the **symmetric** lock range
$\omega_L=\dfrac{\omega_0}{2Q}\dfrac{I_{inj}}{I_{osc}}$.

**Numerical example**: $f_0=5$ GHz, $Q=10$, $I_{inj}/I_{osc}=0.1$. Half lock range

$$
\omega_L=\frac{\omega_0}{2Q}\frac{I_{inj}}{I_{osc}}=\frac{2\pi\times5\times10^{9}}{2\times10}\times0.1=1.57\times10^{8}\ \text{rad/s},
$$

or in frequency, $f_L=\omega_L/2\pi\approx25$ MHz. Intuition: the lock range grows linearly with injection
strength and shrinks inversely with $Q$ (a high-$Q$ LC is more "stubborn" — harder to pull away).

> **Note**: the classical Adler result is standard ([P3] Sec. III, p.2111 reviews Adler [20]); this page uses generic simplified notation.
> The **impulse-train thought experiment** in the next section and the **generalized Adler** after it have both been verified verbatim against the original PDF.

### Locking to an impulse train — Adler with zero calculus ([P3] Sec. IV, p.2112, verified ✓)

Between classical Adler (Sec. III) and the time-synchronous model (Sec. V), [P3] inserts a purely
arithmetic thought experiment (Sec. IV *Locking to an Impulse Train*, p.2112): feed an ideal LC
oscillator a train of current impulses. Its value: **not a drop of calculus is needed** — using only
the discrete bookkeeping "one impulse = one phase kick," it reproduces the lock range of classical
Adler's Eq.(18) to the letter. And "one impulse = one kick" is exactly the interactive animation
**ImpulseAnimation** you played with on [isf_definition](/03_isf_core_theory/isf_definition): one press of "Inject!" = one

$$
\Delta\phi=\Gamma(\theta)\,\frac{\Delta q}{q_{max}}
$$

This section merely replaces "press once by hand" with "press automatically every $T_{inj}$ seconds" —
the same physics, made periodic. (The animation kicks along the voltage axis with $\Delta V=\Delta q/C$;
[P3] Fig. 3 kicks along the charge axis with $q_{inj}$ — the same thing, since $V=q/C$.)

**Setup ([P3] Fig. 3(a), p.2112)**: an ideal parallel LC ($C$, $L$, $R_P$, $-G_m$) with a periodic impulse-train injection current

$$
i_{inj}(t)=\pm\,q_{inj}\sum_{n=-\infty}^{\infty}\delta(t-nT_{inj}),\qquad T_{inj}\equiv\frac{2\pi}{\omega_{inj}}
$$

([P3] adopts the convention $q_{inj}\ge0$; the sign selects Fig. 3(b), speeding up, or Fig. 3(c),
slowing down). Each impulse dumps a fixed charge $q_{inj}$ [C] onto the capacitor in one shot. The key
arrangement: the impulse lands at the zero crossing of the capacitor charge $q(t)$ — it moves the
capacitor voltage "to the opposite side of the zero-crossing" ([P3]'s words: "moving the capacitor
voltage to the opposite side of the zero-crossing"), shifting the state-space point horizontally from
$q=-q_{inj}/2$ to $q=+q_{inj}/2$. Both endpoints lie on **the same circle**, so the amplitude never
moves and only the phase jumps ("the amplitude remains perpetually unaffected", p.2112) — exactly the
"ZC injection = pure phase jump" of [P1] / lab_02.

**Step 1 | The kick per impulse ([P3] Eq.(19), p.2112)**: for small injections ($q_{inj}\ll q_{max}$)

$$
\Delta\phi=\pm\frac{q_{inj}}{q_{max}}\qquad[\text{rad}]
$$

This is the operational definition of [P1], $\Delta\phi=\Gamma(\theta)\,\Delta q/q_{max}$, specialized
to $\Gamma=-\sin\theta$ with the impulse landing at $\theta=\mp\pi/2$ (the zero crossing of $q$, the
most sensitive point where $\lvert\Gamma\rvert=1$).
Dimension check: $\tilde\Gamma=\Gamma/q_{max}$ has units of rad/C ([P3] writes 1/Coulomb; rad is
dimensionless), times $q_{inj}$ [C] gives rad ✓.

Exact geometry ([P3] footnote 9, p.2112): two points on the circle joined by a horizontal chord of length $q_{inj}$, with $q_{inj}=2q_{max}\sin(\Delta\phi/2)$, hence

$$
\Delta\phi=\pm2\sin^{-1}\!\left[\frac{q_{inj}}{2q_{max}}\right]
$$

For small injections $2\sin^{-1}\!\big(\tfrac{q_{inj}}{2q_{max}}\big)\approx q_{inj}/q_{max}$, recovering Eq.(19);
in the extreme $q_{inj}=2q_{max}$ (chord = diameter), $\Delta T=\mp T_0/2$, i.e., $\Delta\omega=+\omega_0$
(period halved) or $-\omega_0/3$ (period stretched to 1.5×) — footnote 9 points this out explicitly:
**even for an ideal LC, the strong-injection "lock range" of this thought experiment is asymmetric**.
This foreshadows that the asymmetric lock range of the generalized Adler equation is not pathological — it is the norm.

**Step 2 | Kick → frequency shift ([P3] Eq.(20)–(21), p.2112)**: eating the same kick every period is equivalent to rewriting the period:

$$
\frac{\Delta\phi}{2\pi}=-\frac{\Delta T}{T_0}=\frac{\Delta\omega}{\omega_{inj}}
$$

(a forward phase jump $\Delta\phi>0$ ⇒ shorter period $\Delta T<0$ ⇒ higher frequency). The average frequency shift is

$$
\Delta\omega=\frac{\Delta\phi}{T_{inj}}=\pm\frac{1}{T_{inj}}\frac{q_{inj}}{q_{max}}\qquad[\text{rad/s}]
$$

Dimension check: rad ÷ s = rad/s ✓. This is already the embryo of the lock range: **an impulse train
can move the oscillator by at most $q_{inj}/(q_{max}T_{inj})$ of angular frequency per period**.

**Step 3 | Discrete map, fixed point, lock range** (this site writes [P3] Sec. IV's verbal narrative as an explicit map):

The impulse need not land at the most sensitive point — under lock it finds its own position. Let
$\theta_n$ = the oscillator's relative phase at the instant the $n$-th impulse arrives (i.e., the
next section's coordinate $\theta=\phi-\omega_{inj}t$ sampled at $t=nT_{inj}$). Between impulses the
oscillator free-runs and the phase difference drifts with the detuning; at each impulse it eats one ISF kick:

$$
\theta_{n+1}=\theta_n+\underbrace{(\omega_0-\omega_{inj})\,T_{inj}}_{\text{drift per period [rad]}}+\underbrace{\Gamma(\theta_n)\,\frac{q_{inj}}{q_{max}}}_{\text{kick per impulse [rad]}}
$$

where the drift per period is $(\omega_0-\omega_{inj})T_{inj}=2\pi\dfrac{\omega_0-\omega_{inj}}{\omega_{inj}}\approx2\pi\dfrac{\omega_0-\omega_{inj}}{\omega_0}$ [rad] (small detuning).
**Locking = a fixed point of the map**, $\theta_{n+1}=\theta_n=\theta^\*$:

$$
(\omega_{inj}-\omega_0)\,T_{inj}=\Gamma(\theta^\*)\,\frac{q_{inj}}{q_{max}}
$$

The left side is "the phase owed per period," the right side is "the phase repaid per impulse" —
**the per-period kick exactly cancels the detuning drift**. This is [P3] Sec. IV's own words: there
exists a $T_{inj}$ such that "the next impulse always occurs at the same place on the waveform" (p.2112).
The condition for a fixed point to exist = the right side can supply the left:

$$
\lvert\omega_{inj}-\omega_0\rvert\le\frac{q_{inj}}{q_{max}\,T_{inj}}\,\max_\theta\lvert\Gamma(\theta)\rvert
$$

For the ideal LC, $\max\lvert\Gamma\rvert=1$ — exactly the extremum of Step 2. **Lock range = maximum kick per period ÷ $T_{inj}$**.

Stability (this site's addition; the paper does not write the discrete version): linearize the map at
$\theta^\*$, $\delta\theta_{n+1}=\big[1+\tfrac{q_{inj}}{q_{max}}\Gamma'(\theta^\*)\big]\delta\theta_n$;
stability requires the multiplier's absolute value to be less than 1, i.e.,
$-2<\tfrac{q_{inj}}{q_{max}}\Gamma'(\theta^\*)<0$. Under weak injection this reduces to
$\Gamma'(\theta^\*)<0$ — the same statement as the continuous version's "stable only if $d\Omega/d\theta<0$"
in the next section; but the discrete version also reveals something the continuous average cannot see:
a kick strong enough that $\tfrac{q_{inj}}{q_{max}}\lvert\Gamma'(\theta^\*)\rvert\ge2$ overcorrects and
$\theta_n$ oscillates back and forth (map instability) — though strong injection lies outside the scope
of this section and of time-averaging anyway (see [P4]).

**Step 4 | Substitute back into Adler — to the letter ([P3] Eq.(22)–(23), p.2112)**: the "curiously"
moment that closes Sec. IV. The balance between the tank loss and the energy-restoration mechanism gives

$$
\omega_0\,q_{max}=Q\,I_{osc}
$$

([P3] Eq.(22), with $Q$ per Eq.(16), p.2111; check: (rad/s)·C = A ✓). The **fundamental amplitude** of the impulse train ([P3] Eq.(23)):

$$
I_{inj}=\frac{2q_{inj}}{T_{inj}}
$$

> **Whose 2 is this?** A δ train of area $q_{inj}$ and period $T_{inj}$ has the Fourier series
> $\frac{q_{inj}}{T_{inj}}\big[1+2\sum_{n\ge1}\cos(n\omega_{inj}t)\big]$: every harmonic (including the
> fundamental) has twice the DC amplitude. This is the 2 of a "real Fourier series," and has **nothing**
> to do with the SSB bookkeeping $/4$ (Example B's $-148$ dBc/Hz) vs the time-domain bookkeeping $/2$
> ($-145$) flagged throughout the phase-noise pages of this site.

Substituting Eq.(23) ($q_{inj}=I_{inj}T_{inj}/2$) and Eq.(22) ($q_{max}=QI_{osc}/\omega_0$) into the extremum of Step 2:

$$
\lvert\Delta\omega\rvert_{max}=\frac{1}{T_{inj}}\frac{q_{inj}}{q_{max}}=\frac{I_{inj}}{2\,q_{max}}=\frac{\omega_0}{2Q}\frac{I_{inj}}{I_{osc}}
$$

= classical Adler's half lock range (Eq.(18), p.2111). [P3] describes this coincidence as "curiously
yields an (absolute) frequency shift exactly equal to Adler's lock range." Now balance a third ledger:
the ideal LC's $\Gamma=-\sin$ has fundamental amplitude 1, so $\lvert\tilde\Gamma_1\rvert=1/q_{max}$,
and the next section's generalized Adler Eq.(35) gives
$\omega_L=\tfrac12 I_{inj}\lvert\tilde\Gamma_1\rvert=I_{inj}/(2q_{max})$ — **discrete arithmetic,
classical Adler, and generalized Adler compute the same number by three routes**. (The $\tfrac12$ in
Eq.(35) is the averaging factor "single tone × ISF fundamental, average of $\cos^2$ = $\tfrac12$";
the 2 in Adler's $\omega_0/2Q$ comes from the tank phase slope $d\varphi/d\omega\approx2Q/\omega_0$;
neither has anything to do with the SSB 2/4 bookkeeping.)

**Step 5 | The continuum limit = generalized Adler Eq.(30) (the other end of the zero-calculus bridge)**:
feed the impulse train into the next section's time-averaged equation ([P3] Eq.(30), p.2113). One
averaging window $T_{inj}$ contains exactly one δ (at $t=nT_{inj}$, where the argument of $\tilde\Gamma$
is $\omega_{inj}t+\theta=2\pi n+\theta\equiv\theta$):

$$
\frac{1}{T_{inj}}\int_{T_{inj}}\tilde\Gamma(\omega_{inj}t+\theta)\,i_{inj}(t)\,dt
=\frac{q_{inj}}{T_{inj}}\,\tilde\Gamma(\theta)
\;\Longrightarrow\;
\frac{d\theta}{dt}=(\omega_0-\omega_{inj})+\frac{q_{inj}}{T_{inj}}\,\tilde\Gamma(\theta)
$$

Meanwhile, divide both sides of Step 3's map by $T_{inj}$:

$$
\frac{\theta_{n+1}-\theta_n}{T_{inj}}=(\omega_0-\omega_{inj})+\frac{q_{inj}}{T_{inj}}\,\tilde\Gamma(\theta_n)
$$

When the net change per period is $\ll2\pi$, the left side becomes $d\theta/dt$ — **the discrete
bookkeeping and Eq.(30) are the same equation**. For an impulse train, the intimidating averaging
integral of Eq.(30) does exactly one thing: it picks out that one kick. Reading it the other way is
even more valuable: Eq.(30) for an arbitrary injection waveform = "slice the continuous $i_{inj}$ into
infinitely many small impulses, log each one ImpulseAnimation-style as $d\phi=\tilde\Gamma\,i_{inj}\,dt$,
then average over each period" — this is the zero-calculus bridge from the animation to Adler.
Incidentally, the impulse train's lock characteristic $\Omega(\theta)=\frac{q_{inj}}{T_{inj}}\tilde\Gamma(\theta)$
**is a scaled copy of the ISF itself** — because all harmonics of a δ train have equal weight
($\lvert I_{inj,n}\rvert=2q_{inj}/T_{inj}$ for all $n\ge1$), every ISF harmonic is excited with equal
weight (compare the picture of [P3] Fig. 6, "injection harmonics filtered by ISF harmonics").

**Worked example (canonical $\Gamma=-\sin\theta$)**: $q_{max}=1$ pC, $f_0=5$ GHz (the oscillator of
Example A), $q_{inj}=10$ fC (1% of $q_{max}$), $f_{inj}=5.005$ GHz (detuning $+5$ MHz), $T_{inj}=1/f_{inj}=199.8$ ps.

1. **Kick budget per impulse**: $\lvert\Delta\phi\rvert_{max}=q_{inj}/q_{max}=10^{-14}/10^{-12}=0.01$ rad.
   The exact formula gives $2\sin^{-1}(0.005)=0.0100000417$ rad, a difference of $4\times10^{-6}$ — the linearization is excellent.
2. **Drift per period**: $(\omega_0-\omega_{inj})T_{inj}=2\pi\times(-5\times10^{6}\ \text{Hz})\times199.8\ \text{ps}=-6.277\times10^{-3}$ rad
   (check: Hz × s is dimensionless, times $2\pi$ gives rad ✓).
3. **Does it lock?** $6.277\ \text{mrad}<10\ \text{mrad}$ ✓. Fixed point: $-\sin\theta^\*\times0.01=+6.277\times10^{-3}$
   ⇒ $\sin\theta^\*=-0.6277$ ⇒ $\theta^\*=-0.679$ rad $=-38.9^\circ$
   (the other solution $\theta=-\pi+0.679=-2.463$ rad is unstable because $\Gamma'(\theta)>0$).
4. **Half lock range**: $f_L=\dfrac{q_{inj}}{q_{max}T_{inj}}\cdot\dfrac{1}{2\pi}=\dfrac{0.01\times5.005\times10^{9}}{2\pi}=7.97$ MHz;
   the 5 MHz detuning is inside the range ✓.
5. **Adler cross-check**: $I_{inj}=2q_{inj}/T_{inj}=100.1\ \mu\text{A}$,
   $\omega_L=I_{inj}/(2q_{max})=5.005\times10^{7}$ rad/s $=2\pi\times7.97$ MHz — the same number.
6. **Feel for the convergence**: multiplier $1-0.01\cos\theta^\*=0.9922$, so $1/e$ convergence takes
   about 128 periods ($\approx25.7$ ns) — weak-injection locking is a "hundreds of periods" slow
   dynamic, which is precisely what justifies treating $\theta$ as a slow variable in the time-averaging.

```python
import numpy as np

q_max, q_inj = 1e-12, 10e-15      # C
f0, f_inj = 5e9, 5.005e9          # Hz
T_inj = 1/f_inj                   # s
drift = 2*np.pi*(f0 - f_inj)*T_inj            # rad per period
print(q_inj/q_max)                            # -> 0.01
print(drift)                                  # -> -0.0062769083987808056
theta = 0.0
for n in range(3000):             # discrete map
    theta += drift + (-np.sin(theta))*q_inj/q_max
print(theta, np.degrees(theta))               # -> -0.6785833433413406 -38.879961621335696
print((q_inj/(q_max*T_inj))/(2*np.pi)/1e6)    # -> 7.965704901749362
I_inj = 2*q_inj/T_inj
print(I_inj, I_inj/(2*q_max))                 # -> 0.0001001 50050000.0
print(1 - (q_inj/q_max)*np.cos(theta))        # -> 0.9922153727798411
print(1/((q_inj/q_max)*np.cos(theta)))        # -> 128.45830271877517
```

(The 3000 steps are just conservative convergence; the fixed point $\theta^\*$, the lock range, and the Adler cross-check all agree with the hand calculation.)

**Applicability and failure conditions**:

- **Small injection**: linearizing the kick requires $q_{inj}\ll q_{max}$; for large injections use the exact formula of footnote 9 (which is itself asymmetric).
- **Slow phase**: the net phase change per period must be $\ll2\pi$ rad for the map→ODE continuum limit (also the premise of Eq.(30)'s time-averaging) to hold.
- **Amplitude assumption**: "the amplitude never moves" holds only for an ideal LC with a charge kick across the zero crossing; a general oscillator relies on its amplitude-restoration mechanism to pull back to the
  limit cycle — that is the subject of Part II's APF ([P4]).
- **Subharmonic**: the impulse may also land once every $M$ periods ([P3] footnote 7, p.2112) — the same arithmetic
  with the drift accumulated over $M$ periods; this is the discrete picture of subharmonic locking.
  > **[P3] footnote 7, verbatim** (p.2112): "...injection could also occur every $M$ periods
  > ($M$ a positive integer), corresponding to subharmonic locking."
  > In other words: **when $T_{inj}=N\cdot T_0$ (injecting once every $N$ oscillation periods)
  > that is exactly subharmonic locking** — swap the paper's $M$ for the site's usual
  > multiplication ratio $N$ and expand term by term; the closed-form lock range lives on the
  > [subharmonic_injection](/06_design_insights/subharmonic_injection) page.
- **Very strong kicks**: when the multiplier leaves the unit interval ($\tfrac{q_{inj}}{q_{max}}\lvert\Gamma'\rvert\ge2$) the discrete map goes unstable — the averaged ODE cannot see this.

> **Verified**: Sec. IV's Eq.(19), (20), (21), (22), (23) plus footnote 7 (subharmonic) and footnote 9
> (exact kick; the strong-injection asymmetry $\Delta\omega=+\omega_0$ vs $-\omega_0/3$) have all been
> confirmed verbatim against the rendered original [P3] PDF, p.2112; classical Adler's Eq.(15)/(18) and
> the $Q$ of Eq.(16) are on p.2111.

### Generalized Adler equation / lock characteristic (core of this paper, verified against the original PDF ✓)

[P3] first converts Hajimiri's **dimensionless** ISF $\Gamma$ into a **unit-bearing** version ([P3] Eq.(26), p.2113):

$$
\tilde\Gamma(x)\equiv\frac{\Gamma(x)}{q_{max}}\qquad[\text{units: rad/C}]
$$

Then the instantaneous phase kick of the injection current, and the change of coordinates to the relative phase $\theta=\phi-\omega_{inj}t$ ([P3] Eq.(28)–(29), p.2113):

$$
\frac{d\phi}{dt}=\tilde\Gamma(\phi)\,i_{inj}(t)
\;\xrightarrow{\ \theta=\phi-\omega_{inj}t\ }\;
\frac{d\theta}{dt}=(\omega_0-\omega_{inj})+\tilde\Gamma(\omega_{inj}t+\theta)\,i_{inj}(t)
$$

Time-synchronous averaging over "one fast injection period" (treating the slowly varying $\theta$ as constant) gives the **time-averaged generalized Adler equation** ([P3] Eq.(30), p.2113):

$$
\frac{d\theta}{dt}=(\omega_0-\omega_{inj})+\frac{1}{T_{inj}}\int_{T_{inj}}\tilde\Gamma(\omega_{inj}t+\theta)\,i_{inj}(t)\,dt
$$

Rearranged into lock-characteristic form ([P3] Eq.(33), p.2114):

$$
\frac{d\theta}{dt}=(\omega_0-\omega_{inj})+\Omega(\theta),\qquad
\boxed{\ \Omega(\theta)=\frac{1}{T_{inj}}\int_{T_{inj}}\tilde\Gamma(\omega_{inj}t+\theta)\,i_{inj}(t)\,dt\ }
$$

where $\Omega(\theta)$ is called the **lock characteristic** ([P3] Eq.(33), p.2114): the injection-induced average frequency shift as a function of the phase difference $\theta$. Note the **plus sign** in front of the averaged term (same sign convention as [P3] Eq.(30)).

**Meaning**: a single first-order ODE built from the **unit-bearing ISF $\tilde\Gamma=\Gamma/q_{max}$** and the **injection waveform $i_{inj}$**,
predicting the behavior of any oscillator under any injection waveform (claim C10). **Locking** = existence of a $\theta^\*$ with
$\omega_{inj}-\omega_0=\Omega(\theta^\*)$; lock range = the width of the range of $\Omega(\theta)$; **stability** is set by the sign of $d\Omega/d\theta$.

**Sinusoidal injection reduces to classical Adler ([P3] Eq.(34)–(35))**: for a single tone $i_{inj}=I_{inj}\cos\omega_{inj}t$,
only the ISF fundamental $\tilde\Gamma_1$ survives:

$$
\Omega(\theta)=\tfrac12 I_{inj}\,\lvert\tilde\Gamma_1\rvert\cos(\theta+\angle\tilde\Gamma_1),
\qquad
\omega_L=\tfrac12 I_{inj}\,\lvert\tilde\Gamma_1\rvert
$$

Half lock range $\omega_L=\frac12 I_{inj}\lvert\tilde\Gamma_1\rvert$ ([P3] Eq.(35)) — $\Omega\propto\cos\theta$ is symmetric about 0, exactly classical Adler.

**Why it is asymmetric in general**: for an arbitrary injection, $\Omega(\theta)$ contains **multiple harmonics**, its range is no longer symmetric about 0, so
$\omega_L^+\ne-\omega_L^-$ — the asymmetry common in real circuits that Adler cannot capture.

**Injection waveform design**: lock range = the width of the range of $\Omega(\theta)$. Aligning the harmonics of the injection waveform $i_{inj}$
**with the harmonics of the ISF $\tilde\Gamma$** (making the inner product larger) enlarges the lock range — one more degree of freedom
(waveform shape) beyond "just increase the injection current."

> **Verified**: $\tilde\Gamma=\Gamma/q_{max}$ (Eq.26), the pulling equations Eq.(28)–(30), the lock characteristic
> Eq.(33), the sinusoidal reduction Eq.(34), and the lock range Eq.(35) have all been confirmed verbatim against the rendered original [P3] PDF, p.2113–2114.

### Lock range = the range of $\Omega(\theta)$ (toy illustration)

Plotting the lock characteristic $\Omega(\theta)$ directly from the time-synchronous averaging integral of [P3] Eq.(33) makes the statement
"lock range = the width of the range of $\Omega(\theta)$; the edges = the max/min of $\Omega(\theta)$" visible at a glance:

![Lock characteristic Ω(θ): left, sinusoidal injection (Γ̃=−sinθ/q_max) gives a clean cosine, symmetric about 0 (ω_L⁺=−ω_L⁻, classical Adler); right, a harmonic-rich injection gives an asymmetric Ω with ω_L⁺≠−ω_L⁻; triangles/inverted triangles mark the upper and lower lock-range edges. Toy model, [P3] Eq.(33).](/figures/lock_characteristic_omega.png)

- **Left (a) sinusoidal injection**: single tone $i_{inj}=I_{inj}\cos\omega_{inj}t$ injected into the ideal-LC ISF $\tilde\Gamma=-\sin\theta/q_{max}$.
  Only the ISF fundamental survives (Eq.(34)); $\Omega(\theta)$ is a clean cosine, symmetric about 0, with edges
  $\pm\omega_L=\pm\tfrac12 I_{inj}\lvert\tilde\Gamma_1\rvert$ (toy value $=\pm0.50$ rad/s, exactly Eq.(35)) — this is classical Adler.
- **Right (b) harmonic-rich injection**: the injection carries the fundamental plus a deliberately phased second harmonic, and the ISF also contains a second harmonic. Multiple harmonics contribute simultaneously,
  so $\Omega(\theta)$ is **asymmetric about 0**: upper edge $\omega_L^+=+0.56$, lower edge $\omega_L^-=-0.63$ rad/s
  ($\omega_L^+\ne-\omega_L^-$) — the asymmetric lock range common in real circuits that Adler cannot capture.

**How to read it**: to lock, $\omega_{inj}-\omega_0=\Omega(\theta^\*)$ must have a solution; the reachable range of $\omega_{inj}-\omega_0$ is exactly
the range of the $\Omega$ curve (between the two horizontal dashed lines). Aligning the injection-waveform harmonics with the ISF harmonics
(making the inner product in Eq.(33) larger) pushes this curve taller and enlarges the lock range — one more degree of freedom
(waveform shape) beyond "just increase $I_{inj}$."

> **Toy-model disclosure**: this is a pedagogical toy model, **not transistor-level**. The ideal-LC $\Gamma=-\sin\theta$ is an exact result;
> the harmonic-rich ISF and the designed injection waveform are **illustrative only**, used solely to expose the asymmetry mechanism. $\Omega(\theta)$ is computed numerically from the time-averaging integral of Eq.(33).
> Full script: `simulations/fig_lock_characteristic.py` (generates `static/figures/lock_characteristic_omega.png`).

## Key figures

| Paper figure | Page | Content | Teaching purpose |
|---|---|---|---|
| Fig. 6 | 2113 | Block diagram: the harmonics of the injection current are **filtered** by the harmonics of the ISF to form the lock characteristic | Explains why $\Omega(\theta)$ keeps only the aligned harmonics |
| Fig. 7 | 2114 | **Time-domain** view of the lock characteristic: the ISF×injection area for the upper/lower edges and the free-running case | Intuition: lock range = extrema of the net area per cycle |

> This site **deliberately does not redraw** Fig. 6 / Fig. 7 of [P3] (no matching transistor-level toy simulation);
> the page numbers/content above have been checked against the [P3] original. The $\Omega(\theta)$ figure in Key equations above is an **independent toy illustration**
> (it only demonstrates the concept "lock range = range of $\Omega(\theta)$"), **not** a redraw of Fig. 6 / Fig. 7.

## Design insights

- **The lock range is designable**: lock range = the width of the range of $\langle\Gamma\,i_{inj}\rangle$ over $\phi$.
  Aligning the harmonics of the injection waveform $i_{inj}$ with the harmonics of the ISF $\Gamma$ (making the inner product larger)
  enlarges the lock range — one more degree of freedom (waveform shape) beyond "just increase the injection current."
- **Topology-independent**: as long as the ISF can be extracted, the same equation applies to ring, LC, and relaxation oscillators;
  no need to measure the hard-to-measure $Q$ and $I_{osc}$.
- **Subharmonic / superharmonic locking**: when the injection frequency is near $\omega_0/m$ or $m\omega_0$, it is the
  corresponding harmonic of $\Gamma$ that does the averaging — this connects directly to frequency division (ILFD) in [P4].
- **Pulling is the other face of the same equation**: when $|\Delta\omega| > $ lock range, $d\phi/dt$ is nonzero and the phase
  slips periodically, producing pulling spurs. In design, make sure the operating frequency falls inside the lock range.

## Limitations

Per paper_metadata (paper_003.limitations):

- **Part I covers phase only**; amplitude modulation is deferred to Part II (APF, [P4]).
- Relies on an **accurately extracted ISF** — if the ISF is off, the predictions are off.
- This site treats it as an **advanced deep-dive, not a core teaching chapter**; the core generalized-Adler equations have been verified against the [P3] original.

## Relationship to other papers

- **[P1]** provides the ISF $\Gamma$ and the Eq.(11) phase kick — the mathematical starting point of this paper.
- **[P2]** provides the ring ISF, connecting to ring injection here (and the ILFD of [P4]).
- **[P4]** is the direct sequel: it adds amplitude (APF), transient pulling, and frequency division; see
  [paper_004](/05_paper_deep_dives/paper_004_injection_locking_part2).
- The generalized Adler equation is entry 20 in [equation_index](/01_paper_map/equation_index) ([P3] Eq.(30)/(33)/(35)).

## What to remember

- **The same ISF computes both phase noise and injection locking** — the input changes from random noise to a deterministic
  $i_{inj}$ (claim C10).
- **Generalized Adler equation**: $\dfrac{d\theta}{dt}=(\omega_0-\omega_{inj})+\dfrac{1}{T_{inj}}\displaystyle\int_{T_{inj}}\tilde\Gamma(\omega_{inj}t+\theta)\,i_{inj}(t)\,dt$ ([P3] Eq.(30), p.2113, with a **plus sign** in front of the averaged term).
- **Impulse-train thought experiment ([P3] Sec. IV, p.2112)**: kick per impulse $\Delta\phi=\pm q_{inj}/q_{max}$ (Eq.(19));
  locking = the per-period kick cancels the detuning drift; the maximum frequency shift $\pm q_{inj}/(q_{max}T_{inj})$ (Eq.(21)),
  rewritten via $\omega_0q_{max}=QI_{osc}$ (Eq.(22)) and $I_{inj}=2q_{inj}/T_{inj}$ (Eq.(23)), matches Adler's lock
  range Eq.(18) to the letter — one ImpulseAnimation kick, made periodic, is injection locking.
- **Noise shaping (new in v5)**: once locked, the oscillator = a first-order PLL — its own noise is high-pass suppressed while reference noise enters low-pass, with corner=ω_L cosθ_ss; full derivation and simulation in [injection_locking_noise](/06_design_insights/injection_locking_noise).
- **Locking** = existence of a steady-state solution / $|\omega_0-\omega_{inj}|\le\omega_L$; **lock range** = the width of the range of the lock characteristic $\Omega(\theta)$; for sinusoidal injection $\omega_L=\tfrac12 I_{inj}\lvert\tilde\Gamma_1\rvert$ ([P3] Eq.(35), p.2114).
- Stronger than Adler in: topology independence, arbitrary waveforms, asymmetric lock range, and designable waveforms that enlarge the lock range.
- This page is **advanced**; the core equations (Eq.19–23, 26, 28–30, 33, 35) have been verified against the original [P3] PDF, p.2112–2114.

## Further reading

- The mathematical starting point, the ISF $\Gamma$: [paper_001](/05_paper_deep_dives/paper_001_general_theory_phase_noise) ([P1]).
- The Fourier harmonics $c_n$ of the ISF (why only aligned harmonics survive in $\Omega(\theta)$): [fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf).
- The direct sequel, Part II (APF amplitude, transient pulling, frequency division): [paper_004](/05_paper_deep_dives/paper_004_injection_locking_part2) ([P4]).
- Where the generalized Adler equation sits in the equation index: [equation_index](/01_paper_map/equation_index) (entry 20, [P3] Eq.(30)/(33)/(35)).
- Where this advanced page sits in the overall path (optional): [learning_path](/00_overview/learning_path).
- Quick overview of the five papers' division of labor: [paper_summary_table](/01_paper_map/paper_summary_table).
