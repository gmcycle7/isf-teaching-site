---
title: Tank Q and Energy Restoration
description: "Derive the quality factor Q cleanly from the parallel RLC tank — three equivalent forms (R_p√(C/L), ω0 R_p C, R_p/(ω0 L)) and the energy definition Q = ω0 · stored energy / dissipated power; show that the active core must supply −R to cancel the tank loss R_p, and that this same R_p is the physical origin of the 4kT/R_p thermal-noise current; connect to phase noise (high Q → narrow band → steep phase slope) and to the Q↔Γrms/qmax correspondence, plus the practical ceiling on on-chip inductor Q. RLC/Q are standard textbook material (external, not among the five source PDFs)."
---

> **β**: This English translation is in beta — the Traditional-Chinese original is the authoritative version.

# Tank Q and Energy Restoration

The "quality factor $Q$ (the measure of how 'sharp' a resonance is and how much energy is lost per cycle)" appears on almost every page of this site: the Leeson model writes it as $\dfrac{1}{2Q}$ ([derivation_leeson](/99_appendix/derivation_leeson)), the LC-vs-ring comparison hinges on it ([lc_vs_ring](/06_design_insights/lc_vs_ring)), and the tank-swing trade-off needs it too ([tank_swing](/06_design_insights/tank_swing)). Yet on all of those pages it is **used as a given — it has never been cleanly derived from the circuit**. This page fills that hole: starting from the most basic parallel RLC tank, we derive the three equivalent forms of $Q$ and its energy definition step by step, then show how it connects to the active core's $-R$, to the tank thermal noise $4kT/R_p$, and finally to how it determines phase noise.

> **Physical intuition (conclusion first)**: the tank (resonant tank — the energy-storage element in which $L$ and $C$ exchange energy back and forth) is like a pendulum. $Q$ measures "how reluctant this pendulum is to stop" — per radian of oscillation it leaks only a tiny fraction of its stored energy into the loss resistance $R_p$. The higher the $Q$, the sharper the resonance peak, the narrower the bandwidth, and the steeper the phase-vs-frequency slope. Think of noise as a force trying to push the oscillation frequency off: the higher the $Q$, the harder the tank "bites down" on $\omega_0$ and refuses to be pushed, so the same lump of noise buys less phase noise. That is why the first slogan of low-phase-noise design is always "make $Q$ high."

This page answers three questions:

1. What exactly is $Q$? Why are the three forms $Q=R_p\sqrt{C/L}=\omega_0 R_p C=R_p/(\omega_0 L)$ equivalent, and why does it equal $\omega_0\times$ (stored energy / dissipated power)?
2. A real tank always has loss $R_p$, so the oscillation decays — how does the active core restore it with $-R$? And why is that cancelled $R_p$ precisely the source of the tank thermal noise $4kT/R_p$?
3. How does $Q$ connect to phase noise? Why "high $Q$ → narrow band → steep phase slope → less noise per unit offset," and why is this the same thing as the ISF's $\Gamma_{rms}/q_{max}$?

> **Honesty note (read first)**: this page's **RLC tank, definition of $Q$ with its three equivalent forms, and $4kTR$ thermal noise** are all **standard circuit-theory / microwave-engineering textbook material (external literature, not among the five source PDFs)** — e.g., Razavi, *RF Microelectronics*; Pozar, *Microwave Engineering*; Lee, *The Design of CMOS RFICs*. This site does not reinvent these constants; it only derives them cleanly and connects them to the verified ISF results within the five PDFs ([P1] Eq.(21), etc.). Every connection to [P1]/[P2] is tagged with paper id + equation.

## Step 1: the parallel RLC tank and the three equivalent forms of $Q$

The most basic LC-oscillator tank is a **parallel RLC**: an inductor $L$, a capacitor $C$, and one parallel loss resistor $R_p$ (all tank losses — inductor series resistance, capacitor dielectric loss, radiation — lumped into this single equivalent parallel resistance).

First define the resonant angular frequency. At one particular frequency, the parallel LC's inductive and capacitive susceptances cancel, the impedance is purely resistive, and the energy swaps entirely back and forth between $L$ and $C$:

$$
\omega_0=\frac{1}{\sqrt{LC}}.
$$

- **Physics used**: inductor impedance $j\omega L$, capacitor impedance $1/(j\omega C)$. In parallel, susceptances add: $\dfrac{1}{j\omega L}+j\omega C=j\big(\omega C-\dfrac{1}{\omega L}\big)$; setting the bracket to zero gives $\omega_0^2=1/(LC)$.
- **Unit check**: $[\sqrt{LC}]=\sqrt{\text{H}\cdot\text{F}}=\sqrt{(\text{V·s/A})(\text{A·s/V})}=\sqrt{\text{s}^2}=\text{s}$, so $1/\sqrt{LC}$ is in rad/s ✓.

**Unloaded vs loaded $Q$ — settle the distinction up front**:

- **Unloaded $Q$ ($Q_0$, unloaded quality factor)**: the $Q$ counting only the tank's own losses ($R_p$ purely from the tank elements). It is the intrinsic "quality" of the tank components themselves.
- **Loaded $Q$ ($Q_L$, loaded quality factor)**: the $Q$ after external loading (downstream circuitry, measurement instruments, buffer input impedance) is folded in. The external load is effectively another parallel resistor $R_{ext}$; the total parallel resistance $R_p\parallel R_{ext}$ is smaller than $R_p$, so $Q_L<Q_0$.
- Relation between the two: $\dfrac{1}{Q_L}=\dfrac{1}{Q_0}+\dfrac{1}{Q_{ext}}$ (conductances add → reciprocal $Q$'s add, since $Q\propto R_p\propto 1/G$). What this page derives, and what determines phase noise, is **primarily the loaded $Q$ (what the oscillator actually sees)**; inductor design, however, cares about the unloaded $Q$. Below, unless stated otherwise, $Q$ means the oscillation loop's actual effective (loaded) $Q$.

Now derive $Q$. The **circuit definition** of the parallel-RLC $Q$ is "at resonance, the energy flow stored in a reactive element ($L$ or $C$) relative to the dissipation rate in the resistor $R_p$." The most convenient equivalent algebraic definition is the ratio of the capacitor's (or inductor's) susceptance magnitude to the conductance at resonance:

$$
Q=\frac{|B_C(\omega_0)|}{G}=\frac{\omega_0 C}{1/R_p}=\omega_0 R_p C.
$$

- **Physics used**: in a parallel RLC, the conductance $G=1/R_p$ is the only dissipative element; the capacitive susceptance $B_C=\omega_0 C$ measures how large the "reactive current" is. $Q$ is the ratio of reactive current to real (dissipative) current.
- **Unit check**: $[\omega_0 R_p C]=(\text{rad/s})(\Omega)(\text{F})=(\text{1/s})(\text{V/A})(\text{A·s/V})=$ dimensionless ✓.

Substituting $\omega_0=1/\sqrt{LC}$ gives the second form:

$$
Q=\omega_0 R_p C=\frac{R_p C}{\sqrt{LC}}=R_p\sqrt{\frac{C^2}{LC}}=R_p\sqrt{\frac{C}{L}}.
$$

- **Every algebra step**: $\omega_0 C=C/\sqrt{LC}=\sqrt{C^2/(LC)}=\sqrt{C/L}$; multiply by $R_p$ and you are done.
- **Unit check**: $\sqrt{C/L}=\sqrt{\text{F/H}}=\sqrt{(\text{A·s/V})/(\text{V·s/A})}=\sqrt{\text{A}^2/\text{V}^2}=\text{A/V}=1/\Omega$, times $R_p$ ($\Omega$) → dimensionless ✓. The quantity $\sqrt{L/C}$ has units of resistance and is called the tank's **characteristic impedance** $R_0=\sqrt{L/C}$, so we may also write $Q=R_p/R_0$ — "how large the parallel loss resistance is relative to the characteristic impedance."

The third form uses $\omega_0=1/\sqrt{LC}$ to swap $C$ for $L$. Because at resonance the inductive susceptance magnitude equals the capacitive susceptance magnitude ($\omega_0 L$ and $1/(\omega_0 C)$ are reciprocals of each other), the same ratio can also be written as the reciprocal of conductance $\times$ inductive reactance:

$$
Q=\omega_0 R_p C=\frac{R_p}{\omega_0 L}.
$$

- **Algebraic verification**: $\omega_0 R_p C\cdot\omega_0 L=\omega_0^2 LC\,R_p=R_p$ (since $\omega_0^2 LC=1$); divide both sides by $\omega_0 L$ to get $\omega_0 R_p C=R_p/(\omega_0 L)$ ✓.
- **Unit check**: $R_p/(\omega_0 L)=\Omega/[(\text{rad/s})(\text{H})]=\Omega/\Omega=$ dimensionless ✓.

**The three forms are equivalent — collected here (cited directly across the site)**:

$$
Q=\omega_0 R_p C=R_p\sqrt{\frac{C}{L}}=\frac{R_p}{\omega_0 L}=\frac{R_p}{R_0},\qquad R_0\equiv\sqrt{\frac{L}{C}}.
$$

- **Physical reading (extremely important)**: note that $R_p$ is in the numerator. **In a parallel tank, larger $R_p$ means higher $Q$** (in parallel, a large resistance = a small loss conductance = less leakage). This is the opposite of the series-RLC intuition (series $Q=\omega_0 L/R_s$ with $R_s$ in the denominator) — the classic beginner mix-up. This site models oscillators exclusively with the **parallel** form; remember "parallel: large $R_p$ → high $Q$."

| Form | When to use it | One-line reading |
|---|---|---|
| $Q=\omega_0 R_p C$ | $C$, $R_p$, $\omega_0$ known (most common) | loss resistance $\times$ capacitive susceptance |
| $Q=R_p\sqrt{C/L}=R_p/R_0$ | when comparing "$R_p$ against the characteristic impedance" | how large the loss resistance is relative to $R_0=\sqrt{L/C}$ |
| $Q=R_p/(\omega_0 L)$ | $L$, $R_p$ known | loss resistance relative to inductive reactance |

## Step 2: the energy definition $Q=\omega_0\dfrac{\text{儲存能量}}{\text{耗散功率}}$, proved consistent with Step 1

The most physical, most field-agnostic definition of $Q$ is the energy definition:

$$
Q=\omega_0\,\frac{E_{stored}}{P_{diss}}=2\pi\,\frac{\text{每週期儲存的能量}}{\text{每週期耗散的能量}}.
$$

- **Meaning**: $Q/(2\pi)$ = stored energy / energy dissipated per cycle. The higher the $Q$, the smaller the fraction $2\pi/Q$ of the stored energy leaked per oscillation cycle. Hence "$Q$ is roughly the number of radians for a free oscillation to decay to $1/e$" (more precisely: the energy envelope is $e^{-\omega_0 t/Q}$; see below).
- **Unit check**: $\omega_0 E/P=(\text{rad/s})(\text{J})/(\text{W})=(\text{rad/s})(\text{J})/(\text{J/s})=$ dimensionless (rad) ✓.

**Proof that it equals Step 1's $\omega_0 R_p C$.** At resonance, let the voltage across the tank be $v(t)=V_p\cos\omega_0 t$.

(1) **Stored energy**: at resonance the energy swaps entirely between $L$ and $C$; the total stored energy is conserved and equals the peak capacitor energy (at the voltage peak, all the energy is in $C$):

$$
E_{stored}=\frac{1}{2}C V_p^2.
$$

- Conservation check: capacitor energy $\tfrac12 C v^2=\tfrac12 C V_p^2\cos^2\omega_0 t$; inductor energy $\tfrac12 L i_L^2$, where $i_L=\tfrac1L\int v\,dt=\tfrac{V_p}{\omega_0 L}\sin\omega_0 t$, so the inductor energy $=\tfrac12 L\tfrac{V_p^2}{\omega_0^2 L^2}\sin^2\omega_0 t=\tfrac12\tfrac{V_p^2}{\omega_0^2 L}\sin^2\omega_0 t$. Using $\omega_0^2 L=1/C$, this becomes $\tfrac12 C V_p^2\sin^2\omega_0 t$. The sum $=\tfrac12 C V_p^2(\cos^2+\sin^2)=\tfrac12 C V_p^2$ — **indeed conserved** ✓.

(2) **Dissipated power**: only $R_p$ dissipates; the average power (mean square of a sinusoid = half the peak squared):

$$
P_{diss}=\frac{\overline{v^2}}{R_p}=\frac{V_p^2/2}{R_p}=\frac{V_p^2}{2R_p}.
$$

(3) **Substitute into the energy definition**:

$$
Q=\omega_0\frac{E_{stored}}{P_{diss}}=\omega_0\cdot\frac{\tfrac12 C V_p^2}{\,V_p^2/(2R_p)\,}=\omega_0\cdot\frac{\tfrac12 C V_p^2\cdot 2R_p}{V_p^2}=\omega_0 R_p C.
$$

- $V_p^2$ and the factors $\tfrac12,2$ all cancel, **landing exactly back on Step 1's $\omega_0 R_p C$** ✓. The energy definition and the circuit definition are the same $Q$ — no coincidence: both measure the same thing, the fraction of stored energy leaked per radian.
- **Unit check**: $\omega_0\cdot\dfrac{[\text{F}][\text{V}^2]}{[\text{V}^2]/[\Omega]}=(\text{rad/s})[\text{F}][\Omega]=(\text{rad/s})[\text{s}]=$ dimensionless ✓.

**The free-decay rate falls out as a bonus (for the "$Q$ = so many radians" intuition)**: with no active core replenishing energy, the tank dissipates $P_{diss}=\omega_0 E/Q$ per second, i.e. $\dfrac{dE}{dt}=-\dfrac{\omega_0}{Q}E$, whose solution is

$$
E(t)=E_0\,e^{-\omega_0 t/Q}\quad\Rightarrow\quad v(t)\ \text{包絡}\ \propto e^{-\omega_0 t/(2Q)}.
$$

- **Reading**: energy decay time constant $\tau_E=Q/\omega_0$; oscillation-amplitude decay time constant $2Q/\omega_0$. For a $Q=100$, 5 GHz tank ($\omega_0=2\pi\times5\times10^9$), the free amplitude-decay constant is about $2\times100/(2\pi\times5\times10^9)\approx6.4$ ns, roughly 32 cycles — **this is why a real oscillator must have an active core continuously restoring energy, or it stops within a few tens of cycles**. Which brings us to Step 3.

## Step 3: the active core supplies $-R$ to cancel $R_p$ — and $R_p$ is precisely the source of the $4kT/R_p$ thermal noise

Step 2 showed: as long as $R_p$ is there, the oscillation decays as $e^{-\omega_0 t/(2Q)}$. To sustain steady oscillation, the oscillator's **active core (e.g., the negative conductance provided by a cross-coupled differential pair)** must **replenish, cycle by cycle, the energy that $R_p$ leaks**. The cleanest view: the active core presents a **negative resistance $-R$** (negative conductance $-G_m$) across the tank, in parallel with $R_p$.

$$
\frac{1}{R_{tank}}=\frac{1}{R_p}-G_m,\qquad \text{起振條件}:\ G_m\ge\frac{1}{R_p}\ \big(\text{即 } -R\le -R_p\big).
$$

- **Physical meaning**: positive resistance absorbs energy; negative resistance supplies it. When the active core's negative conductance $G_m$ exactly equals $R_p$'s conductance $1/R_p$, the total loss is zero and the oscillation holds constant amplitude (the Barkhausen start-up boundary). In practice, $G_m$ is designed slightly larger than $1/R_p$ (loop gain $>1$) to guarantee start-up, and nonlinear saturation then pulls the effective $G_m$ back to exact cancellation — the circuit-level incarnation of the limit-cycle amplitude-restoring mechanism described in [oscillator_phase](/02_foundations/oscillator_phase).
- **Unit check**: $G_m$ and $1/R_p$ are both in siemens (S) ✓.
- **Key clarification**: what the active core cancels is $R_p$'s **deterministic energy loss** (keeping the oscillation from decaying). It **does not — and cannot — cancel the random thermal noise that $R_p$ brings**. That is the point of the next paragraph, and the bridge from this whole page to phase noise.

**$R_p$ is the physical source of the tank thermal-noise current $4kT/R_p$.** Any dissipative resistance (including the equivalent loss $R_p$) is necessarily accompanied by thermal noise, per the Johnson–Nyquist theorem. A parallel resistance is most conveniently represented by its **Norton-equivalent noise current source**, with single-sided PSD:

$$
\frac{\overline{i_{n,R}^2}}{\Delta f}=\frac{4kT}{R_p}.
$$

- **Physics used**: the fluctuation–dissipation theorem — where there is dissipation, there is fluctuation. The resistor thermal-noise voltage PSD is $4kTR_p$ (covered in [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter)); converting to a parallel Norton current source means dividing by $R_p^2$: $\overline{i_n^2}/\Delta f=(4kTR_p)/R_p^2=4kT/R_p$.
- **Unit check**: $[4kT/R_p]=\text{J}/\Omega=(\text{V·A·s})/(\text{V/A})=\text{A}^2\text{s}=\text{A}^2/\text{Hz}$ ✓ (single-sided current PSD, consistent with the spec's notation of $\overline{i_n^2}/\Delta f$ in A²/Hz).
- **The deep point**: you **cannot cancel this noise with $-R$ as well**. The active core's $-R$ cancels $R_p$'s loss term on the "energy balance" ledger; but the random $4kT/R_p$ current that $R_p$ injects on the "fluctuation" ledger is sustained — equally amplified — by the very energy the active core pumps back in. So **the tank loss $R_p$ is simultaneously the source of two things: it forces you to add an active core to restore energy, and it hands you an unavoidable baseline thermal-noise floor**. This is the physical root tying $Q$ to phase noise. (The active core's own devices add still more noise — that is the topic of [device_noise_mapping](/06_design_insights/device_noise_mapping); this page covers only the tank's own $4kT/R_p$.)

**Expressing $R_p$ in terms of $Q$** (to hook into phase noise next): from Step 1, $R_p=Q/(\omega_0 C)=Q\,\omega_0 L=Q\,R_0$, so at the same capacitance/frequency,

$$
\frac{4kT}{R_p}=\frac{4kT\,\omega_0 C}{Q}\quad\Rightarrow\quad \overline{i_{n,R}^2}/\Delta f\ \propto\ \frac{1}{Q}.
$$

- **Reading**: higher $Q$ → larger $R_p$ → smaller tank-injected thermal-noise current PSD ($\propto 1/Q$). This is the first layer of "high $Q$ → low phase noise" (the noise source shrinks); the "narrow-band / steep-slope" effect of Step 2 is the second layer. Stack the two and you get the next step.

## Step 4: connecting $Q$ to phase noise — narrow band, steep phase slope, and the equivalence with $\Gamma_{rms}/q_{max}$

**(a) High $Q$ = narrow bandwidth = steep phase slope.** The standard relation between $Q$ and the 3-dB bandwidth:

$$
Q=\frac{\omega_0}{\Delta\omega_{3\mathrm{dB}}}\quad\Leftrightarrow\quad \Delta\omega_{3\mathrm{dB}}=\frac{\omega_0}{Q}.
$$

- **Derivation sketch**: the parallel-RLC impedance is $Z(\omega)=\big(\tfrac{1}{R_p}+j\omega C+\tfrac{1}{j\omega L}\big)^{-1}$; expanding to first order near $\omega_0$ with $\omega=\omega_0+\Delta\omega$, the susceptance part is $\approx j\,2C\Delta\omega$, giving $Z\approx R_p/(1+j\,2Q\Delta\omega/\omega_0)$. $|Z|$ drops to $1/\sqrt2$ of the peak (−3 dB) when $2Q\Delta\omega/\omega_0=1$, i.e. half-bandwidth $\Delta\omega=\omega_0/(2Q)$, full bandwidth $\omega_0/Q$ ✓.
- **Phase slope**: the phase of the above is $\angle Z=-\arctan(2Q\Delta\omega/\omega_0)$, whose slope with respect to $\omega$ at $\omega_0$ is $\dfrac{d\angle Z}{d\omega}\big|_{\omega_0}=-\dfrac{2Q}{\omega_0}$. **The higher the $Q$, the steeper the phase-vs-frequency slope.**
- **Physical meaning (why a steep phase slope = low phase noise)**: the oscillation locks to the frequency where "the total loop phase shift = 0." If noise tries to push the phase away from 0, the tank's steep phase slope applies a large "frequency restoring force" pulling it back to $\omega_0$ — the steeper the phase slope $d\phi/d\omega$, the smaller the frequency (and hence long-term phase) offset that a given phase perturbation corresponds to. The tank acts like a very stiff spring clamping the oscillation frequency at $\omega_0$. This is precisely the physical origin of the Leeson shaping term $\big(\tfrac{\omega_0}{2Q\Delta\omega}\big)^2$ ([derivation_leeson](/99_appendix/derivation_leeson), Step 2).

**(b) $1/Q^2$ scaling (Leeson).** **Stack** (a)'s narrow-band shaping on top of Step 3's $1/Q$ noise source, then run it through the autonomous oscillator's phase integration ($1/\Delta\omega^2$): the $Q$ dependence of phase noise lands at $1/Q^2$:

$$
\mathcal{L}(\Delta\omega)\ \propto\ \Big(\frac{\omega_0}{2Q\,\Delta\omega}\Big)^2\ \propto\ \frac{1}{Q^2}.
$$

- **Reading**: doubling $Q$ → phase noise improves by $10\log_{10}(2^2)=6.02$ dB. This is the **same inverse-square law** as [tank_swing](/06_design_insights/tank_swing)'s "double $q_{max}$ → −6 dB" — $Q$ and $q_{max}$ are two independent levers that each "pay off quadratically" toward low phase noise.
- **Note**: the shaping expression $\big(\tfrac{\omega_0}{2Q\Delta\omega}\big)^2$ belongs to the Leeson model (**external literature, not among the five source PDFs**; see [derivation_leeson](/99_appendix/derivation_leeson)).

**(c) Q ↔ Γrms/qmax equivalence (this site's core correspondence).** [derivation_leeson](/99_appendix/derivation_leeson) (Step 5, comparison table) asserts: Leeson's $\dfrac{1}{2Q}$ and the ISF's $\dfrac{\Gamma_{rms}}{q_{max}}$ describe **the same thing** — "the efficiency of converting tank/device noise into phase skirts." Putting the two $1/f^2$ results side by side makes it clear:

| Model | $1/f^2$ phase skirt | "noise → phase" efficiency factor | Source |
|---|---|---|---|
| Leeson (external, not among the five PDFs) | $\propto\big(\dfrac{\omega_0}{2Q\,\Delta\omega}\big)^2$ | $\dfrac{1}{2Q}$ (high $Q$ → low efficiency → less noise) | [E1] Leeson 1966 |
| ISF ([P1], within the five PDFs) | $\dfrac{\Gamma_{rms}^2}{q_{max}^2}\cdot\dfrac{\overline{i_n^2}/\Delta f}{4\Delta\omega^2}$ | $\dfrac{\Gamma_{rms}}{q_{max}}$ (small → less noise) | [P1] Eq.(21), p.185 |

The correspondence:

$$
\frac{1}{2Q}\ \longleftrightarrow\ \frac{\Gamma_{rms}}{q_{max}}\times(\text{載波/雜訊功率正規化}).
$$

- **How to read it**: **high $Q$ ⟺ low $\Gamma_{rms}/q_{max}$ ⟺ low phase noise.** Both are the ratio of "how much phase the same lump of noise buys."
- **Why the ISF is more general**: $Q$ is an LC-tank concept (you need a resonant energy-storage element to even have a $Q$); **a ring oscillator has no high-$Q$ tank — no $Q$ at all — yet it still has $\Gamma_{rms}$ and $q_{max}$**, so [P1]'s $\Gamma_{rms}/q_{max}$ holds for rings just as well, while Leeson's $1/(2Q)$ fails for rings (see [lc_vs_ring](/06_design_insights/lc_vs_ring)). $Q$ is the incarnation of $\Gamma_{rms}/q_{max}$ in the special case "a resonant tank exists." That is the full meaning of the $Q\leftrightarrow\Gamma_{rms}/q_{max}$ equivalence claimed in [derivation_leeson](/99_appendix/derivation_leeson).

## Numerical example (building intuition)

> **Example ($Q$, $R_p$, and thermal-noise floor of a 5 GHz LC tank)**: take $L=1$ nH, $C=1.013$ pF (tuned so $f_0=5$ GHz), tank parallel loss $R_p=314\ \Omega$, $T=300$ K. Find $Q$, the 3-dB bandwidth, and the tank thermal-noise current PSD.

**(1) Resonant frequency**:

$$
\omega_0=\frac{1}{\sqrt{LC}}=\frac{1}{\sqrt{10^{-9}\times1.013\times10^{-12}}}=\frac{1}{\sqrt{1.013\times10^{-21}}}\approx3.142\times10^{10}\ \text{rad/s},
$$

i.e. $f_0=\omega_0/(2\pi)\approx5.00$ GHz ✓.

**(2) $Q$ (via $R_p/(\omega_0 L)$, cross-checked against $\omega_0 R_p C$)**:

$$
Q=\frac{R_p}{\omega_0 L}=\frac{314}{3.142\times10^{10}\times10^{-9}}=\frac{314}{31.42}\approx10.0.
$$

Cross-check: $\omega_0 R_p C=3.142\times10^{10}\times314\times1.013\times10^{-12}\approx9.99$ ✓ (the two forms agree). Characteristic impedance $R_0=\sqrt{L/C}=\sqrt{10^{-9}/1.013\times10^{-12}}\approx31.4\ \Omega$, so $Q=R_p/R_0=314/31.4=10.0$ ✓ (all three forms agree).

**(3) 3-dB bandwidth**: $\Delta\omega_{3\mathrm{dB}}=\omega_0/Q=3.142\times10^{10}/10=3.142\times10^9$ rad/s, i.e. $\Delta f_{3\mathrm{dB}}=f_0/Q=500$ MHz. $Q=10$ is typical for an on-chip inductor — a bandwidth of a full 500 MHz, a resonance that is not sharp at all; this also foreshadows Step 5's on-chip $Q$ ceiling.

**(4) Tank thermal-noise current PSD**:

$$
\frac{4kT}{R_p}=\frac{4\times1.38\times10^{-23}\times300}{314}=\frac{1.656\times10^{-20}}{314}\approx5.27\times10^{-23}\ \text{A}^2/\text{Hz}.
$$

- **Dimension check**: $\dfrac{[\text{J/K}][\text{K}]}{[\Omega]}=\dfrac{\text{J}}{\Omega}=\dfrac{\text{V·A·s}}{\text{V/A}}=\text{A}^2\text{·s}=\text{A}^2/\text{Hz}$ ✓.
- **Feel for the number**: this $5.27\times10^{-23}$ A²/Hz is the "tank-only, best-case" noise-current floor. Plugging it into [P1] Eq.(21) as $\overline{i_n^2}/\Delta f$ (with $q_{max}=1$ pC, $\Gamma_{rms}=0.5$) estimates an ideal phase-noise bound — real circuits are worse due to active-core device noise, cyclostationarity, and flicker (see [device_noise_mapping](/06_design_insights/device_noise_mapping)). Raising $Q$ from 10 to 20 (doubling $R_p$ to 628 Ω) cuts this noise-current floor in half outright ($\propto 1/Q$), and phase noise gains again.

**One-shot Python check**:

```python
import numpy as np
L, C, Rp, T, k = 1e-9, 1.013e-12, 314.0, 300.0, 1.380649e-23
w0 = 1/np.sqrt(L*C)
Q_1 = w0*Rp*C            # ω0 Rp C
Q_2 = Rp*np.sqrt(C/L)    # Rp√(C/L)
Q_3 = Rp/(w0*L)          # Rp/(ω0 L)
in2 = 4*k*T/Rp           # tank thermal-noise current PSD (A^2/Hz)
print(f"f0={w0/2/np.pi/1e9:.2f}GHz  Q={Q_1:.2f},{Q_2:.2f},{Q_3:.2f}  "
      f"BW={w0/Q_1/2/np.pi/1e6:.0f}MHz  in2={in2:.2e} A^2/Hz")
# -> f0=5.00GHz  Q=9.99,9.99,9.99  BW=500MHz  in2=5.27e-23 A^2/Hz
```

(The RLC/Q/thermal-noise formulas in this example are all standard textbook material — external, not among the five source PDFs; how $q_{max}$, $\Gamma_{rms}$, and Eq.(21) hook up is covered in [tank_swing](/06_design_insights/tank_swing) and [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise).)

## Step 5: the practical ceiling — on-chip inductor Q and parasitics

In theory you could keep raising $Q$ by making $R_p$ large, but in a silicon process $Q$ hits a hard ceiling, and the causes almost all trace back to the inductor and parasitics:

| Limiting source | Why it suppresses $Q$ | Typical magnitude / consequence |
|---|---|---|
| spiral-inductor metal series resistance $R_s$ | finite metal conductivity + skin effect / proximity effect raise $R_s$ at high frequency; the series $R_s$ converted to parallel, $R_p\approx Q_L^2 R_s$, is capped | on-chip inductor unloaded $Q$ is often only **5–15** (~20 in advanced nodes); only discrete/MEMS reach the hundreds |
| substrate loss | the silicon substrate conducts: magnetically induced eddy currents + capacitive coupling leak energy into the substrate | worst at high frequency; drags $Q$ down further |
| capacitor / varactor loss | the varactor (voltage-controlled capacitor used to tune $f_0$) has series resistance and finite $Q_C$ | the wider the tuning range, the larger the varactor's share and the more it drags down the tank $Q$ |
| external loading (loaded $Q$) | the buffer / next stage effectively parallels in an $R_{ext}$, so $Q_L<Q_0$ (Step 1) | the heavier the measurement or drive loading, the lower the effective $Q$ → worse phase noise |
| parasitic capacitance | wiring/device parasitics $C_{par}$ parallel into the tank, eating the usable $C$ tuning range and possibly adding extra loss | limits the maximum $f_0$ and the swing |

- **Design implication**: because on-chip $Q$ is stuck at ~10–20, LC-oscillator phase-noise improvements often come **not from raising $Q$ (there is little headroom) but from enlarging the swing to raise $q_{max}$** — exactly the theme of [tank_swing](/06_design_insights/tank_swing). The design knob "raising tank $Q$ is nearly-free swing" (at the same $I_{bias}$, larger $R_p$ → larger swing $\approx\tfrac{4}{\pi}I_{bias}R_p$) has its upper limit locked by this inductor-$Q$ ceiling.
- **Why rings do not rely on $Q$**: a ring oscillator has no resonant tank at all (no $Q$); it uses the number of stages $N$ and per-stage current/swing as levers instead — another reason the ISF's $\Gamma_{rms}/q_{max}$ framework (which needs no $Q$) is more general than Leeson (see [lc_vs_ring](/06_design_insights/lc_vs_ring)).

> **Honesty note**: this section's typical inductor-$Q$ values (5–20), skin/proximity effects, substrate loss, and varactor $Q$ are all **standard RFIC design knowledge (external, not among the five source PDFs; e.g., Lee, *CMOS RFICs*; Razavi, *RF Microelectronics*; Niknejad's inductor work)**. Exact numbers vary widely across process generations; only order-of-magnitude feel is given here. TODO: to cite a specific process's inductor-$Q$ curves, consult that process's documentation.

## Applicability and failure conditions

| Condition | When it holds (the $Q$ concept applies cleanly) | What happens when it fails |
|---|---|---|
| a resonant tank exists (LC, crystal, MEMS) | $Q=\omega_0 R_p C$ and the other forms hold; $1/Q^2$ scaling applies | **ring/relaxation has no resonance → no $Q$**; use $\Gamma_{rms}/q_{max}$ instead ([lc_vs_ring](/06_design_insights/lc_vs_ring)) |
| high $Q$ (narrow band), $\Delta\omega\ll\omega_0/(2Q)$ | the first-order expansion $Z\approx R_p/(1+j2Q\Delta\omega/\omega_0)$ and Lorentzian shaping are accurate | at low $Q$ (wide band) the first-order approximation degrades; use the full $Z(\omega)$ |
| losses lumpable into a single parallel $R_p$ | the three $Q$ forms are equivalent; a single $4kT/R_p$ noise source | distributed losses / multiple noise sources need separate models (substrate and varactor each with their own $Q$) |
| linear, small perturbation | $Q$ is a constant; the energy definition holds | under large signals the active core's strong nonlinearity makes the effective impedance time-varying (cyclostationary; see [effective_isf](/03_isf_core_theory/effective_isf)) |
| loaded vs unloaded kept distinct | loaded $Q$ determines phase noise; unloaded $Q$ for inductor design | conflating the two overestimates $Q$ and underestimates phase noise |

## Key takeaways

- The parallel-RLC $Q$ has four equivalent forms: $Q=\omega_0 R_p C=R_p\sqrt{C/L}=R_p/(\omega_0 L)=R_p/R_0$ ($R_0=\sqrt{L/C}$); **in parallel, $R_p$ sits in the numerator — large $R_p$ → high $Q$**.
- The energy definition $Q=\omega_0\,E_{stored}/P_{diss}$ agrees exactly with the above (substituting $v=V_p\cos\omega_0 t$ yields $\omega_0 R_p C$; $V_p^2$ cancels entirely).
- Without an active core the energy decays as $\propto e^{-\omega_0 t/Q}$; the active core uses **$-R$ (negative conductance $G_m\ge1/R_p$) to cancel $R_p$'s energy loss**, but **cannot cancel $R_p$'s thermal noise**.
- $R_p$ is the physical source of the tank thermal-noise current $4kT/R_p$ (single-sided PSD, A²/Hz); $R_p=Q\,R_0$, hence $4kT/R_p\propto 1/Q$.
- $Q=\omega_0/\Delta\omega_{3\mathrm{dB}}$: high $Q$ → narrow band → steep phase slope $-2Q/\omega_0$ → frequency clamped → phase noise $\propto1/Q^2$ (−6 dB per doubling of $Q$; Leeson, external, not among the five source PDFs).
- **$Q\leftrightarrow\Gamma_{rms}/q_{max}$**: Leeson's $1/(2Q)$ and [P1] Eq.(21)'s $\Gamma_{rms}/q_{max}$ are the same "noise → phase" efficiency; high $Q$ = low $\Gamma_{rms}/q_{max}$ = low phase noise. The ISF version also holds for rings, which have no $Q$.
- Example: $L=1$ nH, $C=1.013$ pF, $R_p=314\ \Omega$ → $f_0=5$ GHz, $Q=10$, $\Delta f_{3\mathrm{dB}}=500$ MHz, $4kT/R_p\approx5.3\times10^{-23}$ A²/Hz.
- Practical ceiling: on-chip spiral-inductor $Q$ is only ~5–20 (metal $R_s$, skin/proximity, substrate loss, varactor), so LC phase-noise reduction usually shifts to enlarging the swing instead ([tank_swing](/06_design_insights/tank_swing)).
- Sources: RLC/$Q$/$4kTR$ are standard textbook material (**external literature, not among the five source PDFs**); the $1/Q^2$ shaping is Leeson's (external); $\Gamma_{rms}/q_{max}$ and Eq.(21) are [P1] (within the five PDFs, verified verbatim).

## Further reading

- Why phase has no restoring force, and how $-R$ maps to limit-cycle amplitude restoration: [oscillator_phase](/02_foundations/oscillator_phase)
- How $Q$ enters the Leeson model; the full $Q\leftrightarrow\Gamma_{rms}/q_{max}$ comparison: [derivation_leeson](/99_appendix/derivation_leeson)
- The other quadratic lever, $q_{max}$ (swing), and the consequences of the on-chip $Q$ ceiling: [tank_swing](/06_design_insights/tank_swing)
- Why a ring with no $Q$ can still use the ISF framework: [lc_vs_ring](/06_design_insights/lc_vs_ring)
- The signature $1/f^2$ result and how $4kT/R_p$ enters Eq.(21): [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)
- Fundamentals of resistor thermal noise $4kTR$: [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter)
- Site-wide symbols and units: [Notation](/00_overview/notation)
