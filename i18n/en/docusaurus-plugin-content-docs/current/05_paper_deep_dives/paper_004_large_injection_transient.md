---
title: "[P4] Large-Injection LC Model and Transient Behavior (Sec. III-E/F, V Leftovers)"
description: "Hong–Hajimiri 2019 Part II leftovers, taught: how Mirzaei's Generalized Adler equation ([P4] Eq.(7)–(9)) grows out of ISF/(1+A) (Eq.(13), (21)–(22), (27)); the exact transient of the sinusoidal Adler equation in one line — the tan half-angle turns the in-lock tanh (Eq.(31)–(32)) and the out-of-lock tan (Eq.(33)–(34)) into the two signs of one quadratic; closed-form lock time and its edge divergence (lab_36's 4.435 reproduced digit for digit); the APF-driven amplitude transient (dip→overshoot→settle) and Table I's slope recipe (τ_p×(1+a)); a closed-form beat frequency for large-injection pulling (site derivation) and the k=0/k=2 comb lines raised by AM. All four lab_41 panels checked against numbers."
---

> **β**: This English translation is in beta — the Traditional-Chinese original is the authoritative version.

# [P4] Large-Injection LC Model and Transient Behavior: Exact Pull-In Solution, Lock Time, APF Amplitude Transient, and Pulling Spectrum

> **Prerequisites**: [paper_004](/05_paper_deep_dives/paper_004_injection_locking_part2) (APF definition [P4] Eq.(18)–(22), ISF/APF quadrature Eq.(26), augmented Adler Eq.(27)), [lab_36](/04_simulation_labs/lab_36_lock_acquisition) (the $R$-form exact solution of the in-lock Adler equation, critical slowing, cycle slips), [injection_locking_noise](/06_design_insights/injection_locking_noise) (Part A first-order PLL, Part B beat frequency $\omega_b$ and the one-sided comb), [phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise) (amplitude recovery with $\tau_0=2Q/\omega_0$, OU process) | **Next**: the M:N / ILFD part of [paper_004](/05_paper_deep_dives/paper_004_injection_locking_part2), lab_37 (`simulations/lab_37_ilfd_lock.py`, documented inside the paper_004 page), [quadrature_and_coupled_oscillators](/06_design_insights/quadrature_and_coupled_oscillators).

[paper_004](/05_paper_deep_dives/paper_004_injection_locking_part2) already covered the **APF** (amplitude
perturbation function) definition of [P4], the ideal-LC ISF/APF quadrature, and M:N sub-/super-harmonic locking.
This page collects what is left of [P4] **Sec. III-E/F (the large-injection LC model) and Sec. V (transient behavior)**
and teaches it:

> **What this page answers**:
> 1. Why is the "amplitude-aware Adler" — Mirzaei's **Generalized Adler's equation** ([P4] Eq.(8)) — exactly the
>    $\tilde\Gamma/(1+A)$ model of [P4] (Eq.(13), (27))? In the large-injection lock range $\omega_L=\omega_{L0}/\sqrt{1-a^2}$
>    (Eq.(9), (23)), is $a$ equal to $I_{inj}/I_{osc}$ or to $I_{inj}/I_{max}$? Why does the model become "unbounded" for $a\ge1$?
> 2. Where does the **exact transient solution** of the sinusoidal Adler equation come from? Why do the $\tanh$ of [P4] Eq.(31)
>    (in lock) and the $\tan$ of Eq.(33) (out of lock) look alike?
> 3. **How long does locking take**? Is there a closed form? Why does an oscillator near the lock-range edge lock, but
>    extremely slowly? What is the recipe behind the asterisk in [P4] Table I, "$\tau_p$ from the slope of the lock characteristic"?
> 4. What does the **amplitude** do during acquisition? How does the APF turn the phase transient into an amplitude dip/overshoot?
>    When does the quasi-static assumption fail?
> 5. Out of lock (pulling), is the large-injection **beat frequency** still $\sqrt{\Delta\omega^2-\omega_L^2}$? What does AM do to the
>    pulling spectrum ("ISF + APF" vs "ISF Only" in [P4] Fig. 14(c))?

> **Physical intuition (conclusions first)**: the injected current simultaneously "pushes the phase" (ISF, tangential) and
> "changes the amplitude" (APF, radial). Once the amplitude changes, the ISF **scales inversely** with it
> ($\tilde\Gamma_{LC}=\tilde\Gamma/(1+A)$: a larger swing means the same charge pushes the phase less). That single feedback turns
> Adler's $\sin\theta$ into $\sin\theta/(1+a\cos\theta)$ — when the injection is in phase with the oscillation ($\theta\approx0$)
> the amplitude is inflated, the restoring force **weakens**, and locking is **slow**; in anti-phase ($\theta\approx\pm\pi$) the
> amplitude is drained, the restoring force **strengthens**, and the lock characteristic is pulled up — so the lock range is
> stretched from $\omega_{L0}$ to $\omega_{L0}/\sqrt{1-a^2}$, and diverges as $a\to1$ through the nonphysical "zero amplitude"
> solution. As for the transient: after the tan half-angle substitution the sinusoidal Adler equation leaves a single
> **quadratic**; flipping the sign of its discriminant turns the in-lock $\tanh$ (exponential convergence at rate $\omega_p$) into
> the out-of-lock $\tan$ (periodic slipping at the beat frequency $\omega_b$) — the same Pythagorean root
> $\sqrt{\lvert\omega_L^2-\Delta\omega^2\rvert}$.

> **Scope of this page**: advanced deep-dive ([P4] leftovers), **not a core teaching chapter**. Everything marked "✓ verified" below
> was checked word for word against the magnified original PDF: [P4] Eq.(5)–(9) and the Sec. III-B $\tau_0=2Q/\omega_0$ (p.2123),
> Eq.(13) (p.2124), Eq.(20)–(22) and footnote 7 (p.2126), Eq.(23) and the empirical $\theta\in[-110^\circ,110^\circ]$ restriction
> (p.2127), Eq.(24)–(27) and the Fig. 8 caption (p.2128), Eq.(31)–(34), Table I and its asterisk note (p.2130), the Fig. 13 / Fig. 14
> captions, Table II and the amplitude-conscious waveform (p.2131–2132), Eq.(35)–(38) (p.2132). Parts that are **derived on this
> site and not in [P4]** are labeled explicitly: the step-by-step derivation of Eq.(31)/(33) ([P4] only writes "one can show that
> [29]"), the closed-form beat frequency for large-injection pulling (Sec. 5.2), and the first-order amplitude-lag model (Sec. 4.3).
> External references are always flagged "(external reference, not among the site's 5 PDFs)" with the source checked word for
> word in [P4]'s bibliography.

## 0. Notation and Convention Bookkeeping (pin down the 2s and the signs first)

| Quantity | This site | [P4] | Bookkeeping |
|---|---|---|---|
| Detuning | $\Delta\omega\equiv\omega_0-\omega_{inj}$ | $\Delta\omega\equiv\omega_{inj}/N-\omega_0$ (p.2130) | Overall sign differs; every result on this page depends only on $\Delta\omega^2$ or states the branch explicitly |
| ISF-only half lock range | $\omega_{L0}\equiv\dfrac{I_{inj}}{2q_{max,0}}$ | $\omega_L=\tfrac12 I_{inj}\lvert\tilde\Gamma_1\rvert$, ideal LC $\lvert\tilde\Gamma_1\rvert=1/q_{max,0}$ (Eq.(26)) | That $\tfrac12$ is the **product-to-sum $\tfrac12$** ([P3] Eq.(34)–(35), p.2114, verified on this site in injection_locking_noise); unrelated to the SSB $/4$ vs time-domain $/2$ phase-noise convention |
| Large-injection half lock range | $\omega_L\equiv\omega_{L0}/\sqrt{1-a^2}$ | Eq.(9) = Eq.(23) at $\beta=90^\circ$ | Whenever this page writes $\omega_L$ it means the **APF-corrected** value; ISF-only is always $\omega_{L0}$ |
| Injection strength (LC-specific) | $a\equiv\dfrac{I_{inj}}{I_{osc}}$ | $\tfrac12 I_{inj}\lvert\Delta_1\rvert=\tfrac12\tau_0\dfrac{I_{inj}}{q_{max,0}}$ | Identity $\omega_0 q_{max,0}=Q\,I_{osc}$ (p.2124) ⟹ $a=\tau_0\,\omega_{L0}$ (exact) |
| Linearity validity | $I_{inj}/I_{max}$, $I_{max}\equiv\omega_0 q_{max,0}$ | footnote 11, p.2130; Eq.(35), p.2132 | $I_{osc}=I_{max}/Q$ (p.2132): **two different normalizations** — $I_{max}$ governs whether first-order linearity holds, $I_{osc}$ governs how large the LC amplitude effect is |
| Amplitude memory time | $\tau_0=2Q/\omega_0$ [s] | Sec. III-B, p.2123; Eq.(25), p.2128 | This is the **amplitude** time constant; the energy time constant is $Q/\omega_0$ (a factor of 2, see [tank_Q](/02_foundations/tank_Q_and_energy_restoration)) |
| Shifted phase | $\psi\equiv\theta+\pi/2$ | $N\tilde\theta\equiv N\theta+\angle\tilde\Gamma_N-\angle I_{inj}$ | Ideal LC, cosine injection, $N=1$: $\angle\tilde\Gamma_1=90^\circ$, $\angle I_{inj}=0$ ⟹ $\tilde\theta=\theta+\pi/2=\psi$ |

Except for the end of Sec. 2, this page takes $N=1$ (fundamental injection) throughout. **Generic dimension check**:
$[\omega_{L0}]=[\text{A}]/[\text{C}]=[\text{C/s}]/[\text{C}]=\text{rad/s}$ ✓ (rad is dimensionless); $[a]=[\text{s}]\cdot[\text{rad/s}]=$ dimensionless ✓.

## 1. The Paper's Text: Passages Newly Verified for This Unit (verbatim transcription)

### 1.1 Existing models: Adler and Mirzaei's Generalized Adler ([P4] Sec. III-A, p.2123 ✓)

Adler's equation ([P4] Eq.(5)) and the tank $Q$ (Eq.(6)):

$$
\frac{d\theta}{dt}=\omega_0-\omega_{inj}-\frac{\omega_0}{2Q}\frac{I_{inj}}{I_{osc}}\sin\theta,\qquad
Q=\frac{R_P}{\omega_0 L}=R_P\,\omega_0 C
$$

[P4] (p.2123): "A powerful improvement to Adler's equation was derived by Mirzaei *et al.* [11], where they forgo
the assumption of a weak injection signal. ... the oscillation amplitude under injection is roughly given by"

$$
V_{osc}=(I_{osc}+I_{inj}\cos\theta)\,R_P\qquad\text{([P4] Eq.(7))}
$$

"which leads to an augmented differential equation for the oscillator's phase:"

$$
\frac{d\theta}{dt}=\omega_0-\omega_{inj}-\frac{\omega_0}{2Q}\,\frac{I_{inj}\sin\theta}{I_{osc}+I_{inj}\cos\theta}\qquad\text{([P4] Eq.(8))}
$$

"The lock range associated with (8) was derived independently by a number of authors [9]–[12] to be"

$$
\omega_L=\frac{\omega_0}{2Q}\frac{I_{inj}}{I_{osc}}\,\frac{1}{\sqrt{1-\dfrac{I_{inj}^2}{I_{osc}^2}}}\qquad\text{([P4] Eq.(9))}
$$

[P4] immediately lists three limitations of this model (p.2123): it only handles sinusoidal injections; $Q$ and $I_{osc}$ are hard
to determine accurately because of parasitics, and modern integrated oscillators may not be modeled by the circuit of Fig. 1 at
all; and the predicted lock range is **symmetric**, "which is not always the case [8], [12]". The Sec. III-B thought experiment
on the same page states the amplitude time constant explicitly: "we assume that any excess amplitude decays exponentially with
a time constant of $\tau_0=2Q/\omega_0$ in between successive injections due to the energetics of the oscillator."

### 1.2 Effective ISF inversely dependent on amplitude, and the augmented pulling equation ([P4] Sec. III-C/E, p.2124 and p.2126 ✓)

$$
\tilde\Gamma_{LC}=\frac{\tilde\Gamma}{1+A}\qquad\text{([P4] Eq.(13), p.2124)}
$$

The physics in the text of p.2124: "the oscillation amplitude controls the slope of the waveform (for a fixed oscillation
frequency), and a steeper waveform corresponds to a proportionally smaller phase shift from the same injection of charge."
Footnote 4 is honest: this inverse relationship holds **exactly only when the state variables are mutually orthogonal (no
AM-to-PM)**, which LC and Bose oscillators satisfy.

Amplitude deviation ([P4] Eq.(20), p.2126) and the augmented pulling equation (Eq.(21)):

$$
A=\frac{1}{T_{inj}}\int_{T_{inj}}\Delta\big(\omega_{inj}t+\theta\big)\,i_{inj}(t)\,dt
$$

$$
\frac{d\theta}{dt}=\omega_0-\omega_{inj}+\frac{\dfrac{1}{T_{inj}}\displaystyle\int_{T_{inj}}\tilde\Gamma\big(\omega_{inj}t+\theta\big)\,i_{inj}(t)\,dt}{1+\dfrac{1}{T_{inj}}\displaystyle\int_{T_{inj}}\Delta\big(\omega_{inj}t+\theta\big)\,i_{inj}(t)\,dt}
$$

[P4] calls this a "quasi-nonlinear" model: the nonlinearity hides only in the **division** of ISF by APF; each remains linear in the
injection current. For a sinusoidal injection $i_{inj}=I_{inj}\cos(\omega_{inj}t)$ only the fundamental survives (Eq.(22), p.2126;
footnote 7: the ISF/APF of an ideal LC are pure sinusoids, the remaining harmonics are "effectively *filtered out*"):

$$
\frac{d\theta}{dt}=\omega_0-\omega_{inj}+\frac{\tfrac12 I_{inj}\lvert\tilde\Gamma_1\rvert\cos(\theta+\angle\tilde\Gamma_1)}{1+\tfrac12 I_{inj}\lvert\Delta_1\rvert\cos(\theta+\angle\Delta_1)}
$$

### 1.3 Asymmetric lock range and the "unboundedness" of the model ([P4] Eq.(23), p.2127 ✓)

$$
\omega_L^{\pm}=\frac{\tfrac12 I_{inj}\lvert\tilde\Gamma_1\rvert}{\tfrac12 I_{inj}\lvert\Delta_1\rvert\cos\beta\pm\sqrt{1-\big(\tfrac12 I_{inj}\lvert\Delta_1\rvert\sin\beta\big)^2}},\qquad
\beta\equiv\angle\tilde\Gamma_1-\angle\Delta_1
$$

Text (p.2127): "This lock range is generally asymmetric, meaning $\omega_L^+\ne-\omega_L^-$. ... Only in the specific case of
the ISF and the APF being in perfect quadrature with respect to each other ($\beta=\pm\pi/2$) is the lock range symmetric."
And the most important warning on this page: "the lock characteristic from (22) is no longer bounded for all $\theta$ when
$I_{inj}\lvert\Delta_1\rvert\ge2$, resulting in an infinite lock range [i.e., (23) no longer holds]. Physically, this is because
the fractional amplitude change $A$ is able to dip below $-1$ for certain values of $\theta$, corresponding to the nonphysical
scenario of an oscillation amplitude which is zero or negative." Remedy: "roughly restricting $\theta\in[-110^\circ,110^\circ]$
for very large injection amplitudes usually results in reliable estimates of the lock range." (Footnote 8: Generalized Adler
(8) and [9]–[12] likewise predict an infinite lock range when $I_{inj}\ge I_{osc}$.)

### 1.4 Ideal LC: from ISF/APF back to Generalized Adler ([P4] Sec. III-F, p.2128 ✓)

$$
\tilde\Gamma(\varphi)=-\frac{1}{q_{max,0}}\sin\varphi,\qquad\tilde\Lambda(\varphi)=\frac{1}{q_{max,0}}\cos\varphi\qquad\text{(Eq.(24))}
$$

$$
d(t,\varphi)=e^{-t/\tau_0},\quad\tau_0=\frac{2Q}{\omega_0},\quad\int_0^\infty d\,dt=\tau_0\ \Longrightarrow\ \Delta(\varphi)=\tau_0\,\tilde\Lambda(\varphi)\qquad\text{(Eq.(25))}
$$

$$
\tilde\Gamma_1=\frac{1}{q_{max,0}}\angle90^\circ,\qquad\Delta_1=\frac{\tau_0}{q_{max,0}}\angle0\qquad\text{(Eq.(26))}
$$

$$
\frac{d\theta}{dt}=\omega_0-\omega_{inj}-\frac{\tfrac12\dfrac{I_{inj}}{q_{max,0}}\sin\theta}{1+\tfrac12\tau_0\dfrac{I_{inj}}{q_{max,0}}\cos\theta}\qquad\text{(Eq.(27))}
$$

The closing sentence: "Finally, if we use the identity $\omega_0 q_{max,0}=QI_{osc}$ shown in Fig. 2(a) ... to eliminate the maximum
charge swing $q_{max,0}$, we arrive at Generalized Adler's equation (8)." **Check**: $\tfrac12\tau_0 I_{inj}/q_{max,0}=\tfrac12\cdot\dfrac{2Q}{\omega_0}\cdot\dfrac{I_{inj}}{q_{max,0}}=\dfrac{Q\,I_{inj}}{\omega_0 q_{max,0}}=\dfrac{I_{inj}}{I_{osc}}=a$ ✓,
$\tfrac12 I_{inj}/q_{max,0}=\dfrac{\omega_0}{2Q}\dfrac{I_{inj}}{I_{osc}}=\omega_{L0}$ ✓ — Eq.(27) equals Eq.(8) term by term.
Physical reading: the amplitude Mirzaei guessed as $V_{osc}=(I_{osc}+I_{inj}\cos\theta)R_P$ is, in the [P4] framework, the APF
fundamental $A=a\cos\theta$.

The Fig. 8 caption (p.2128 ✓) supplies the real numbers used for the Table I reconstruction on this page: "Injection amplitudes of
$I_{inj}=0.75$ mA and $I_{inj}=1.5$ mA, respectively, for a CMOS differential *LC* oscillator with tank parameters $L=6$ nH,
$C=4.15$ pF, and $Q=15$ and biased at $I_{tail}=1$ mA, resulting in $I_{osc}=(4/\pi)$ mA and $2/\lvert\Delta_1\rvert=1.25$ mA.
(c) Bipolar Colpitts oscillator shown in Fig. 6 subjected to an injection amplitude of $I_{inj}=7.5$ mA." Two sentences on the same
page are kept for Sec. 4: "the stable mode must feature a negative lock characteristic slope, which also corresponds to the
larger oscillation amplitude"; and the model's limit — "the deviation between theory and simulation near the center of the
oscillation amplitude plot for larger injection strengths ... occurs since nonlinear amplitude restoring effects, which are not
captured by the APF, are more prominent at larger oscillation amplitudes."

### 1.5 Sec. V-A Pull-In Process (p.2130 ✓)

Setup in the text: "Suppose the injection is *within* the lock range ($\lvert\Delta\omega\rvert\lt\omega_L$) and $\theta_0$ denotes
the locked phase; i.e., $\Delta\omega\equiv\omega_{inj}/N-\omega_0=\Omega(\theta_0)$. Then one can show that [29]"

$$
\tan\!\left(\frac{N\tilde\theta}{2}\right)=\tan\!\left(\frac{N\tilde\theta_0}{2}\right)\tanh\!\left(\frac{\omega_p t+\phi_0}{2}\right)\qquad\text{([P4] Eq.(31))}
$$

"where we denoted $N\tilde\theta\equiv N\theta+\angle\tilde\Gamma_N-\angle I_{inj}$ out of convenience, $\phi_0$ is set by
initial conditions, and $\omega_p:=-\Omega'(\theta_0)$ is the *pull-in frequency*. As time persists and $\theta$
approaches $\theta_0$, the difference between them $\hat\theta$ approaches $\hat\theta\propto e^{-\omega_p t}$. (See
[1, Sec. V-F].)" The Pythagorean relationship:

$$
\omega_p=N\sqrt{\omega_L^{\,2}-\Delta\omega^2}\qquad\text{([P4] Eq.(32))}
$$

**Table I (p.2130 ✓) THEORETICAL AND SIMULATED PULL-IN TIME CONSTANTS**:

| | Fig. 13(a) | Fig. 13(b) | Fig. 13(c) |
|---|---|---|---|
| Simulated $\tau_p/T_{inj}$ | $1/0.1667=6$ | $1/0.5358=1.87$ | $1/0.0590=16.9$ |
| Theoretical $\tau_p/T_{inj}$ | 5.95 | 1.79 | $17.4^{*}$ |

Asterisk note (verbatim): "$^*$To incorporate the APF into our prediction, we calculated $\tau_p$ directly from the slope of the
theoretical lock characteristic instead of from (32)." Fig. 13 caption: (a) 1-GHz 17-stage ring locked to a 1-GHz 1.5-mA
sinusoidal injection; (b) same ring, 1-GHz 5-mA; (c) 1-GHz CMOS differential *LC* locked to a 1-GHz 0.5-mA injection.
The fitted curves of the three panels are $y=0.9983e^{-0.1667x}$, $1.0001e^{-0.5358x}$, $0.9988e^{-0.0590x}$ ($R^2=1.0000$), with
"Number of Cycles" on the horizontal axis. $\tau_p\equiv1/\omega_p$.

### 1.6 Sec. V-B Spectrum of an Injection-Pulled Oscillator (p.2130–2132 ✓)

"If the injection is *outside* the lock range ($\lvert\Delta\omega\rvert\gt\omega_L$), then one can show that [29]"

$$
\tan\!\left(\frac{N\tilde\theta}{2}\right)=-\frac{1}{N}\frac{\omega_b}{\omega_L+\Delta\omega}\tan\!\left(\frac{\omega_b t+\phi_0}{2}\right)\qquad\text{([P4] Eq.(33))}
$$

$$
\omega_b:=N\sqrt{\Delta\omega^2-\omega_L^{\,2}}\qquad\text{([P4] Eq.(34))}
$$

"The tangent function has a period of $\pi$, and so $\theta(t)$ is periodic with the beat frequency $\omega_b$ (hence
its name). Thus, elementary phase modulation theory tells us that the distance between adjacent sidebands is
$\omega_b$." And: "The tone at one edge of the spectrum always occurs right at the injection frequency."

**Table II (p.2132 ✓) THEORETICAL AND SIMULATED BEAT FREQUENCIES**: Fig. 14(a) simulated $f_b=30.4$ MHz, theoretical
$f_b=\sqrt{\Delta f^2-f_L^{\,2}}=30.6$ MHz; Fig. 14(b) $6.8$ vs $6.6$ MHz. Fig. 14 caption: (a) 1-GHz 17-stage ring pulled by a
1.04-GHz 1.5-mA sinusoidal injection; (b) same ring, 0.97-GHz 1.5-mA; (c) 1-GHz bipolar Colpitts pulled by a 0.7-GHz 7.5-mA
sinusoidal injection. p.2131: "the oscillator shown in Fig. 14(b) is on the cusp of being locked—the injection is only 0.7 MHz
below the lower edge of the lock range. To account for amplitude modulation in the *LC* oscillator example of Fig. 14(c), we
solved the pulling equation of (21) and assumed the following amplitude-conscious form for the oscillation voltage:
$v_{osc}(t)\propto[1+A(t)]\cdot\cos[\omega_{inj}t+\theta(t)]$. As we can see, incorporating the APF into the analysis improves the
model's accuracy dramatically."

### 1.7 Sec. VI Injection Compliance (p.2132 ✓, only the three equations relevant here)

$$
\eta_N:=\frac{2\omega_L/\omega_0}{I_{inj}/I_{max}}\ \text{(Eq.(35))},\qquad
\eta_N=q_{max,0}\lvert\tilde\Gamma_N\rvert\ \text{(Eq.(36))},\qquad
\eta_{LC}:=\frac{2\omega_L/\omega_0}{I_{inj}/I_{osc}}=\frac{q_{max,0}}{Q}\lvert\tilde\Gamma_1\rvert\ \text{(Eq.(38))}
$$

**Convention flag**: $\eta$ uses the **two-sided** lock range $2\omega_L$ ("fractional, two-sided, sinusoidal lock range"); the
$\omega_L$ on this page is the half-width. The paper's qualitative conclusion for LC: "for the same power consumption, an *LC*
oscillator with a higher tank $Q$ has a narrower lock range" (Table III: $\eta_{LC}=0.212$ CMOS diff., $0.533$ NMOS-only diff.,
$0.325$ MOS Colpitts). For an ideal LC, $\eta_{LC}=q_{max,0}\cdot(1/q_{max,0})/Q=1/Q$ — the canonical $Q=10$ gives $0.1$; the
measured CMOS differential LC ($Q=15$) reads 0.212, three times larger than $1/Q=0.067$ — evidence that the real ISF magnitude
exceeds $1/q_{max,0}$ (non-sinusoidal waveform, smaller effective $q_{max}$ at the injection node); [P4] does not decompose this
further and neither does this site guess.

## 2. Teaching (1): The Exact Transient of the Sinusoidal Adler Equation — One Quadratic, Two Signs

For Eq.(31) and (33), [P4] only writes "one can show that [29]" ([29] is Hong's Ph.D. dissertation, external reference, see the end
of the page). Here we derive from scratch, and **derive both at once**. Ideal LC, cosine injection, $N=1$, site convention (Sec. 0):

$$
\frac{d\theta}{dt}=\Delta\omega-\omega_{L0}\sin\theta,\qquad\Delta\omega=\omega_0-\omega_{inj}\ [\text{rad/s}].
$$

**Step 1 (shift the lock characteristic into an even function)**: let $\psi\equiv\theta+\pi/2$ (= the $\tilde\theta$ of [P4], Sec. 0),
$\sin\theta=-\cos\psi$:

$$
\frac{d\psi}{dt}=\Delta\omega+\omega_{L0}\cos\psi .
$$

Locked point $\cos\psi_0=-\Delta\omega/\omega_{L0}$; linearization $d(\delta\psi)/dt=-\omega_{L0}\sin\psi_0\,\delta\psi$, stable branch
$\sin\psi_0\gt0$, i.e. $\psi_0\in(0,\pi)$. **Units**: rad/s = rad/s + (rad/s)·dimensionless ✓.

**Step 2 (Weierstrass half-angle substitution, as in lab_36 / injection_locking_noise)**: $u\equiv\tan(\psi/2)$,
$\cos\psi=\dfrac{1-u^2}{1+u^2}$, $\dfrac{d\psi}{dt}=\dfrac{2}{1+u^2}\dfrac{du}{dt}$. Substitute and multiply both sides by $(1+u^2)$:

$$
2\frac{du}{dt}=\Delta\omega\,(1+u^2)+\omega_{L0}(1-u^2)
=\underbrace{(\omega_{L0}+\Delta\omega)}_{\gt0}-\underbrace{(\omega_{L0}-\Delta\omega)}_{\text{the sign decides everything}}\,u^2 .
$$

This is the pivot of the whole page: the right-hand side is a **quadratic** in $u$, and the sign of the $u^2$ coefficient
$(\omega_{L0}-\Delta\omega)$ decides whether the solution is a $\tanh$ or a $\tan$. ($\Delta\omega\ge0$ without loss of generality;
$\Delta\omega\lt0$ follows from the symmetry $\theta\to-\theta$, i.e. $\psi\to\pi-\psi$.)

**Step 3A (in lock, $0\le\Delta\omega\lt\omega_{L0}$ → $\tanh$)**: let $u_0^2\equiv\dfrac{\omega_{L0}+\Delta\omega}{\omega_{L0}-\Delta\omega}$,
so that $2\dot u=(\omega_{L0}-\Delta\omega)(u_0^2-u^2)$. By the half-angle identity $\tan^2(\psi_0/2)=\dfrac{1-\cos\psi_0}{1+\cos\psi_0}=\dfrac{1+\Delta\omega/\omega_{L0}}{1-\Delta\omega/\omega_{L0}}=u_0^2$ — so $u_0=\tan(\psi_0/2)$ **is the half-angle tangent of the locked
point**. Separate variables, $\displaystyle\int\frac{du}{u_0^2-u^2}=\frac{1}{u_0}\operatorname{artanh}\frac{u}{u_0}$ ($\lvert u\rvert\lt u_0$):

$$
\frac{2}{u_0}\operatorname{artanh}\frac{u}{u_0}=(\omega_{L0}-\Delta\omega)\,t+C
\ \Longrightarrow\
u=u_0\tanh\!\Big(\frac{(\omega_{L0}-\Delta\omega)\,u_0\,t+\phi_0}{2}\Big).
$$

And $(\omega_{L0}-\Delta\omega)\,u_0=\sqrt{(\omega_{L0}-\Delta\omega)(\omega_{L0}+\Delta\omega)}=\sqrt{\omega_{L0}^2-\Delta\omega^2}\equiv\omega_p$.
Written back in $\psi=\tilde\theta$:

$$
\boxed{\ \tan\frac{\tilde\theta}{2}=\tan\frac{\tilde\theta_0}{2}\,\tanh\!\Big(\frac{\omega_p t+\phi_0}{2}\Big),\qquad\omega_p=\sqrt{\omega_{L0}^2-\Delta\omega^2}\ }
$$

— **word for word [P4] Eq.(31)–(32) ($N=1$)**. Also $\omega_p=\omega_{L0}\sin\psi_0=-\Omega'(\theta_0)$ ($\Omega=\omega_{L0}\cos\psi$,
$\Omega'=-\omega_{L0}\sin\psi_0$), matching [P4]'s definition $\omega_p:=-\Omega'(\theta_0)$ ✓. **Units**: $[\omega_p t]=$
(rad/s)(s) = dimensionless ✓; the $/2$ inside the $\tanh$ and the half angle in $u=\tan(\psi/2)$ are **the same 2** (bookkeeping,
not physics): $\tanh(z/2)\to1$ at rate $e^{-z}$, hence $\hat\theta\propto e^{-\omega_p t}$ and the decay rate is $\omega_p$, not
$\omega_p/2$.

**Step 3B (out of lock, $\Delta\omega\gt\omega_{L0}$ → $\tan$)**: now $\omega_{L0}-\Delta\omega\lt0$; write
$2\dot u=(\Delta\omega-\omega_{L0})(u^2+b^2)$, $b^2\equiv\dfrac{\Delta\omega+\omega_{L0}}{\Delta\omega-\omega_{L0}}\gt0$.
$\displaystyle\int\frac{du}{u^2+b^2}=\frac1b\arctan\frac ub$:

$$
u=b\tan\!\Big(\frac{(\Delta\omega-\omega_{L0})\,b\,t+\phi_0}{2}\Big),\qquad
(\Delta\omega-\omega_{L0})\,b=\sqrt{\Delta\omega^2-\omega_{L0}^2}\equiv\omega_b,\qquad
b=\frac{\omega_b}{\Delta\omega-\omega_{L0}}.
$$

Converting to [P4]'s sign $\Delta\omega_{[P4]}=-\Delta\omega$: $b=\dfrac{\omega_b}{-\Delta\omega_{[P4]}-\omega_{L0}}=-\dfrac{\omega_b}{\omega_L+\Delta\omega_{[P4]}}$ —
**word for word [P4] Eq.(33)–(34) ($N=1$)** ✓. The $\tan$ has period $\pi$ ⟹ $u$ (hence $\psi$ mod $2\pi$) has period $2\pi/\omega_b$:
$\theta$ advances by $2\pi$ per beat, which is [P4]'s "$\theta(t)$ is periodic with the beat frequency".

**How the two branches relate**: $b^2=-u_0^2$ — the same expression $\dfrac{\omega_{L0}+\Delta\omega}{\omega_{L0}-\Delta\omega}$, positive in
lock (real roots $\pm u_0$ = stable / unstable locked points), negative out of lock (no real root, $\dot u$ always positive, never
stops). lab_36's $R$-form $R(\theta)=R(\theta_0)e^{-\omega_c t}$ and the $\tanh$ form here are interchangeable through the identity
$x=x_0\tanh z\Leftrightarrow\dfrac{x-x_0}{x+x_0}=-e^{-2z}$ (written out in lab_36 Step 2); the $\tanh$ branch only covers initial
conditions on the arc $(-\psi_0,\psi_0)$ (containing the peak of $\Omega$), while a start on the other arc takes the $\coth$ branch
with the same decay rate. **Numerical verification (lab_41)**: $r_0=\Delta\omega/\omega_{L0}=0.5$, $\theta(0)=0$, the Eq.(31) closed form
and RK4 differ by at most $2.16\times10^{-14}$ rad over the whole trajectory; the Eq.(33) closed form at $r_0=2.276$ differs by at most
$3.32\times10^{-7}$ rad over 427 beats (floating-point unwrapping accumulation).

**Generalization to the $N$-th superharmonic** (the general form of [P4] Sec. V): Eq.(30) gives $\Omega(\theta)=\omega_L\cos(N\tilde\theta)$,
$d(N\tilde\theta)/dt=N\big[-\Delta\omega_{[P4]}+\omega_L\cos(N\tilde\theta)\big]$ — replace every $(\omega_{L0},\Delta\omega)$ above by
$(N\omega_L,N\Delta\omega)$ and $\psi\to N\tilde\theta$, and immediately $\omega_p=N\sqrt{\omega_L^2-\Delta\omega^2}$,
$\omega_b=N\sqrt{\Delta\omega^2-\omega_L^2}$, and the coefficient $-\dfrac{N\sqrt{\cdot}}{N(\omega_L+\Delta\omega)}=-\dfrac1N\dfrac{\omega_b}{\omega_L+\Delta\omega}$ ✓ —
every $N$ in Eq.(31)–(34) falls into place.

## 3. Teaching (2): Closed-Form Lock (Pull-In) Time and the Edge Divergence

### 3.1 Inverting Eq.(31) for time

Invert the $\tanh$: $t(u)=\dfrac{2}{\omega_p}\Big[\operatorname{artanh}\dfrac{u}{u_0}-\operatorname{artanh}\dfrac{u(0)}{u_0}\Big]$.
Define "locked" as $\theta$ entering $\theta_{ss}-\varepsilon$ (this site and lab_36 both use $\varepsilon=0.01$ rad):

$$
\boxed{\ T_{lock}=\frac{2}{\omega_p}\left[\operatorname{artanh}\frac{\tan\frac{\psi_0-\varepsilon}{2}}{\tan\frac{\psi_0}{2}}-\operatorname{artanh}\frac{\tan\frac{\psi(0)}{2}}{\tan\frac{\psi_0}{2}}\right]\ }\qquad[\text{s}]
$$

**Units**: $\operatorname{artanh}$ is dimensionless, $2/\omega_p$ is in s ✓. **Asymptotic expansion** ($\varepsilon\ll1$):
$\dfrac{\tan((\psi_0-\varepsilon)/2)}{\tan(\psi_0/2)}\approx1-\dfrac{\varepsilon}{\sin\psi_0}$, and
$\operatorname{artanh}(1-\delta)\approx\tfrac12\ln\dfrac{2}{\delta}$, so

$$
T_{lock}\approx\frac{1}{\omega_p}\left[\ln\frac{2\sin\psi_0}{\varepsilon}-2\operatorname{artanh}\frac{u(0)}{u_0}\right]
=\tau_p\cdot\big[\text{a few }\ln\big],\qquad\tau_p\equiv\frac1{\omega_p}.
$$

$1/\omega_p$ is the protagonist; the start and the threshold only enter logarithmically — consistent with lab_36. **Numbers**:
$r_0=0.5$ ($\theta_{ss}=30^\circ$, $\psi_0=120^\circ$, $u_0=\tan60^\circ=\sqrt3$, $u(0)=\tan45^\circ=1$), $\varepsilon=0.01$: exact closed
form $\omega_{L0}T_{lock}=4.435$, RK4 measurement $4.435$, **and lab_36's independent $R$-form value is also 4.435** — three routes
agree; the asymptotic formula gives 4.431 (0.1% off, the $O(\delta)$ dropped in the $\operatorname{artanh}(1-\delta)$ expansion).

### 3.2 Divergence at the edge (critical slowing)

$\omega_p=\omega_{L0}\sqrt{1-r^2}$; as $r=\Delta\omega/\omega_{L0}\to1$, $\omega_p\approx\sqrt2\,\omega_{L0}\sqrt{1-r}\to0$ and
$T_{lock}\propto(1-r)^{-1/2}\to\infty$: the locked point $\psi_0$ and the unstable point $-\psi_0$ merge at $\psi=0$ (saddle-node), and
the slope of the restoring force vanishes. lab_36 measured $\omega_{L0}T_{lock}$ growing from 4.435 ($r=0.5$) to 22.913 ($r=0.99$); the
three $\tau_p$ of [P4] Table I are tests of this very $e^{-\omega_p t}$ ($R^2=1.0000$). **Canonical scale** (this page: $I_{inj}=1.5$ mA,
$q_{max}=1$ pC ⟹ $f_{L0}=119.4$ MHz): $T_{lock}=4.435/\omega_{L0}=5.913$ ns = 29.6 periods at 5 GHz for $r_0=0.5$; on lab_36's $f_L=5$ MHz
scale it is 141.2 ns (706 periods) — the same dimensionless 4.435, differing only by $1/\omega_{L0}$.

### 3.3 Large-injection correction: the "slope recipe" behind Table I's asterisk

The augmented model $\dot\theta=\Delta\omega-\omega_{L0}\,g(\theta)$, $g(\theta)\equiv\dfrac{\sin\theta}{1+a\cos\theta}$, has no $\tanh$
closed form as neat as Eq.(31), but [P4]'s definition $\omega_p:=-\Omega'(\theta_0)$ applies directly — exactly what the Table I
asterisk note does. Step by step:

$$
g'(\theta)=\frac{\cos\theta\,(1+a\cos\theta)+a\sin^2\theta}{(1+a\cos\theta)^2}=\frac{\cos\theta+a}{(1+a\cos\theta)^2}
\ \Longrightarrow\
\boxed{\ \omega_p^{APF}=\omega_{L0}\,\frac{\cos\theta_0+a}{(1+a\cos\theta_0)^2}\ },\qquad
\frac{\sin\theta_0}{1+a\cos\theta_0}=\frac{\Delta\omega}{\omega_{L0}} .
$$

Three things one reads off immediately:

1. **Stable branch and lock-range edge**: $g'\gt0\Leftrightarrow\cos\theta_0\gt-a$; the maximum of $g$ is at $\cos\theta_{max}=-a$,
   $g_{max}=\dfrac{\sqrt{1-a^2}}{1-a^2}=\dfrac{1}{\sqrt{1-a^2}}$ ⟹ $\omega_L=\omega_{L0}/\sqrt{1-a^2}$ — [P4] Eq.(9) = Eq.(23) at
   $\beta=90^\circ$ ✓ (lab_41 numerics: $\max_\theta g=1.13811$ vs $1/\sqrt{1-a^2}=1.13811$). As $a\to1$, $\theta_{max}\to180^\circ$ and
   $1+a\cos\theta_{max}\to0$: the nonphysical zero-amplitude solution, i.e. the "unboundedness" of Sec. 1.3 (lab_41: for $a=1.2$ the
   denominator crosses zero at $146.4^\circ$).
2. **Slower by $(1+a)$ at band centre**: $\Delta\omega=0\Rightarrow\theta_0=0$, $\omega_p^{APF}=\omega_{L0}\dfrac{1+a}{(1+a)^2}=\dfrac{\omega_{L0}}{1+a}$,
   $\tau_p^{APF}=(1+a)\,\tau_p^{ISF}$. Physics: in-phase injection inflates the amplitude to $1+a$, the effective ISF shrinks to
   $1/(1+a)$ (Eq.(13)), and the slope of the restoring force loses a factor $(1+a)$. Canonical: $\tau_p^{ISF}=1/\omega_{L0}=1.333$ ns →
   $\tau_p^{APF}=1.970$ ns (9.8 periods).
3. **The locked phase moves outward at the same detuning**: at $r_0=0.5$, ISF-only $\theta_{ss}=30.00^\circ$, $\omega_p/\omega_{L0}=0.8660$;
   augmented $\theta_0=42.53^\circ$, $\omega_p^{APF}/\omega_{L0}=0.6645$ (1.30 times slower), locked amplitude $1+a\cos\theta_0=1.3519$.
   RK4-fitted decay rate / formula: $1.0046$ (ISF), $1.0006$ (APF) — the linearized rate is the whole-trajectory rate (the same
   statement as $R^2=1.0000$ in [P4] Fig. 13).

**Ideal-LC reconstruction of Table I(c) (an estimate, not an exact reproduction)**: with the Fig. 8 caption's $Q=15$, $f_0=1$ GHz,
$I_{osc}=(4/\pi)$ mA, $I_{inj}=0.5$ mA, $\tfrac12 I_{inj}\lvert\Delta_1\rvert=0.5/1.25=0.40=a$, the identity $q_{max,0}=QI_{osc}/\omega_0=3.04$ pC
gives $\omega_{L0}=I_{inj}/(2q_{max,0})$, ISF-only $\tau_p/T_{inj}=f_0/\omega_{L0}=12.2$, and multiplying by $(1+a)$ gives **17.0** — [P4]'s
slope recipe gives 17.4, the circuit simulation 16.9. The 2% gap comes from our use of the ideal-LC $\lvert\tilde\Gamma_1\rvert=1/q_{max,0}$
and $I_{osc}$ to back out $q_{max,0}$, whereas [P4] used the ISF/APF actually extracted from that circuit (its $2/\lvert\Delta_1\rvert=1.25$ mA
is itself 2% below $I_{osc}=1.273$ mA). The point is not 17.0 vs 17.4 but that **without the APF one gets only 12.2**: Table I(c)'s
asterisk is direct evidence of the APF stretching the pull-in time by 40%.

## 4. Teaching (3): The Amplitude Transient During Acquisition (APF-Driven)

### 4.1 Quasi-static amplitude: $A(t)=a\cos\theta(t)$

For an ideal LC under sinusoidal injection (Eq.(26)), [P4] Eq.(20) is simply $A=\tfrac12 I_{inj}\lvert\Delta_1\rvert\cos(\theta+\angle\Delta_1)=a\cos\theta$.
It is an **algebraic** relation — the amplitude follows $\theta$ instantaneously (quasi-static). Combined with the amplitude-conscious
waveform of p.2131:

$$
v_{osc}(t)\propto\big[1+a\cos\theta(t)\big]\cos\big[\omega_{inj}t+\theta(t)\big].
$$

**Physics**: at $\theta=0$ the injection current is in phase with the oscillation voltage → power is pumped into the tank → amplitude
$1+a$; at $\theta=\pm\pi$ anti-phase → power is drained → $1-a$; at $\theta=\pm\pi/2$ quadrature → the phase is pushed but the amplitude is
untouched (the time-domain version of the ISF/APF quadrature). **Units**: $a$ dimensionless, $A$ a relative amplitude deviation ✓.

### 4.2 Two amplitudes per detuning: the stable one is the larger

In lock, $\dfrac{\sin\theta_0}{1+a\cos\theta_0}=\dfrac{\Delta\omega}{\omega_{L0}}$ has **two roots** for $\lvert\Delta\omega\rvert\lt\omega_L$
([P4] p.2128: "two mathematical solutions for the phase $\theta$ and therefore also two possible oscillation amplitudes"); the stable root
lies on the branch $\cos\theta_0\gt-a$ (Sec. 3.3, item 1), with amplitude $1+a\cos\theta_0\gt1-a^2$ — this is the closed loop of solid
(stable, large-amplitude) and dashed (unstable, small-amplitude) curves in the bottom row of Fig. 8, and the solid/dashed lines of
lab_41 panel (c) are the same thing projected onto the lock characteristic.

### 4.3 Transient: dip → overshoot → settle, and when quasi-static fails

Insert the $\theta(t)$ of Sec. 2 into $A=a\cos\theta$: if, when the injection is switched on, $\theta(0)$ lies on the half circle with
$\cos\theta\lt0$ (anti-phase injection), the amplitude first drops **below** free-running (dip); as $\theta$ sweeps through $0$ the amplitude
shoots up to $1+a$ (overshoot); finally it settles at $1+a\cos\theta_0$. lab_41 (b) uses $\theta(0)=-2$ rad, $r_0=0.5$: the quasi-static $A$
starts at $-0.1987$, peaks at $+0.4775$ ($=a$, at $\omega_{L0}t=1.97$), and ends at $+0.3519$, an overshoot of $0.1256$.

**The premise of quasi-static** is that the amplitude follows the phase "instantly" — but [P4]'s own APF definition Eq.(19) is the
**time integral** of the decay function (Fig. 5(c): "the APF is equal to the area under the amplitude deviation impulse response"),
with $d(t)=e^{-t/\tau_0}$ for an ideal LC. So the amplitude is really the "drive $a\cos\theta(t)$" passed through a first-order low-pass
with time constant $\tau_0$. **Site extension (not in [P4], labeled illustrative)**:

$$
\tau_0\frac{dA}{dt}=a\cos\theta(t)-A,\qquad
\tau_0\,\omega_{L0}=a\ \Longrightarrow\ a\,\frac{dA}{d\tau}=a\cos\theta-A\quad(\tau\equiv\omega_{L0}t).
$$

The derivation is one step: $A(t)=\displaystyle\int_0^\infty\frac{a\cos\theta(t-\tau')}{\tau_0}e^{-\tau'/\tau_0}\,d\tau'$ (period-average
Eq.(17) with $D=\tilde\Lambda\,d$ over the fundamental; what remains is the convolution of the slow envelope with $d/\tau_0$, normalized so
that a constant $\theta$ returns Eq.(20)'s $A=a\cos\theta$); differentiate. **Units**: $[\tau_0\dot A]=$ s·(1/s) = dimensionless ✓.
**Quasi-static criterion**: the phase-transient rate $\omega_p$ against the amplitude memory $1/\tau_0$ —
$\omega_p\tau_0=a\,\omega_p/\omega_{L0}\le a$. Canonical $a=0.4775$, $r_0=0.5$: $\omega_p\tau_0=0.317$ — not small. The lagged version in
lab_41 (b): the dip only reaches $-0.0443$ (start $A(0)=0$: injection just switched on, amplitude not yet responding), peak $+0.4577$, peak
delayed by $0.885$ ns, the same final value $+0.3519$, and an essentially unchanged phase trajectory (both models at $0.74223$ rad at
$\omega_{L0}t=24$). Conclusion: **steady state and lock range are unaffected by the lag, but the height and timing of the transient amplitude
peak are smeared by $\tau_0$**; for $a\ll1$ (weak injection) quasi-static is exact, while as $a\to1$ even quasi-static itself is in trouble
(the unboundedness of Sec. 1.3). [P4] p.2128 further notes that **nonlinear amplitude restoring** (outside the linear APF model) is more
prominent at large amplitudes — the second ceiling of the model on this page.

## 5. Teaching (4): Large-Injection Pulling — Beat Frequency and Comb Lines Raised by AM

### 5.1 The ISF-only comb (review, already on the site)

[injection_locking_noise](/06_design_insights/injection_locking_noise) Part B derived $\omega_b=\sqrt{\Delta\omega^2-\omega_{L0}^2}$, comb lines
at $\omega_{inj}+k\omega_b$, $k=0$ exactly at the injection frequency, **strictly one-sided** and geometrically decaying (ratio
$\omega_{L0}/(\Delta\omega+\omega_b)$, external reference Armand 1969). The ISF-only curve of lab_41 (d) verifies it again: at $r=2.276$,
$\omega_b/\omega_{L0}=2.0448$ (Eq.(34)), measured $2.0448$; geometric ratio $0.2314$ ⟹ $-12.71$ dB per line, measured $k_2-k_1=-12.71$,
$k_3-k_2=-12.71$ dB; mirror line $-117.9$ dB (numerical zero).

### 5.2 The large-injection beat frequency: a site closed form ([P4] gives none)

[P4] Eq.(34) holds only for ISF-only (or, generally, a purely sinusoidal lock characteristic); Fig. 14(c) for the LC was drawn by
solving Eq.(21) numerically. The beat frequency of the augmented model can be integrated exactly. Dimensionless
$r\equiv\Delta\omega/\omega_{L0}$, $\tau=\omega_{L0}t$:

$$
\frac{d\theta}{d\tau}=r-\frac{\sin\theta}{1+a\cos\theta}
\ \Longrightarrow\
\omega_{L0}T_b=\oint\frac{(1+a\cos\theta)\,d\theta}{r+ra\cos\theta-\sin\theta}\equiv\oint\frac{(1+a\cos\theta)\,d\theta}{D(\theta)} .
$$

**Step 1 (write the denominator as a single cosine)**: $ra\cos\theta-\sin\theta=R\cos(\theta+\delta)$, $R^2=1+r^2a^2$, $\tan\delta=1/(ra)$.
Out of lock ⟺ $D\gt0$ everywhere ⟺ $r\gt R$ ⟺ $r^2(1-a^2)\gt1$ ⟺ $\Delta\omega\gt\omega_{L0}/\sqrt{1-a^2}=\omega_L$ ✓ (self-consistent with Eq.(9)).

**Step 2 (split the numerator into $D$, $D'$ and a constant)**: solve $1+a\cos\theta=p\,D+q\,D'+s$, $D'=-ra\sin\theta-\cos\theta$.
Comparing the $\sin\theta$, $\cos\theta$ and constant coefficients: $0=-p-qra$, $a=pra-q$, $1=pr+s$ ⟹

$$
p=\frac{ra^2}{R^2},\qquad q=-\frac{a}{R^2},\qquad s=\frac{1}{R^2}.
$$

(Check: $pD+qD'+s=\dfrac{(r^2a^2+1)+a\cos\theta\,(r^2a^2+1)}{R^2}=1+a\cos\theta$ ✓.)

**Step 3 (integrate the three pieces around one turn)**: $\oint p\,d\theta=2\pi p$; $\oint q\,D'/D\,d\theta=q\big[\ln D\big]_0^{2\pi}=0$
($D\gt0$ and periodic); $\oint\dfrac{s\,d\theta}{r+R\cos(\theta+\delta)}=\dfrac{2\pi s}{\sqrt{r^2-R^2}}$ (standard integral, $r\gt R$). Total:

$$
\omega_{L0}T_b=\frac{2\pi}{R^2}\Big[ra^2+\frac1S\Big],\quad S\equiv\sqrt{r^2-R^2}=\sqrt{r^2(1-a^2)-1}
\ \Longrightarrow\
\boxed{\ \frac{\omega_b^{APF}}{\omega_{L0}}=\frac{R^2\,S}{1+ra^2S}\ }
$$

**Units**: $r,a,R,S$ all dimensionless, $\omega_b^{APF}$ in units of $\omega_{L0}$ ✓. **Two limits**: $a\to0$: $R\to1$, $S\to\sqrt{r^2-1}$ ⟹
back to Eq.(34) ✓; $S\to0$ ($\Delta\omega\to\omega_L^+$) ⟹ $\omega_b^{APF}\to0$: critical slowing happens at the **correct** (augmented) edge ✓.
**Numbers ($\Delta\omega=2\omega_L$, $r=2.2762$)**: closed form $1.9896$, RK4 measurement $1.9897$ (ratio $1.0000$); the "naive" recipe of
plugging Eq.(9)'s $\omega_L$ into Eq.(34), $\sqrt{r^2-1/(1-a^2)}=1.9713$, is 0.9% off — small at this $a$, but **it is not the correct
formula** (the error grows with $a$). Real units: $\Delta f=271.7$ MHz, $f_b^{ISF}=244.1$ MHz, $f_b^{APF}=237.5$ MHz.

### 5.3 What AM does to the spectrum: $k=0$ and $k=2$ raised, one-sidedness breached

The complex envelope relative to $\omega_{inj}$ (the amplitude-conscious form of p.2131):

$$
\big[1+a\cos\theta\big]e^{j\theta}=e^{j\theta}+\frac a2+\frac a2\,e^{j2\theta}.
$$

(The $\tfrac a2$ is the $\tfrac12$ of $\cos\theta=\tfrac12(e^{j\theta}+e^{-j\theta})$ — expansion bookkeeping.) Spectral meaning of the three
terms: $e^{j\theta}$ is the pure phase comb; $\tfrac a2$ is **DC** — exactly at $\omega_{inj}$ ($k=0$), raising the line [P4] describes as the
"tone at one edge ... right at the injection frequency"; $\tfrac a2e^{j2\theta}$ is the doubled phase, feeding mainly $k\ge2$. lab_41 (d)
($\Delta\omega=2\omega_L$) computes the Fourier coefficients exactly over an integer number of beats:

| Line (relative to the $k=1$ main line) | ISF-only | ISF+APF | Change |
|---|---|---|---|
| $k=0$ ($\omega_{inj}$) | $-12.23$ dB | $-9.82$ dB | $\times1.299$ ($+2.3$ dB) |
| $k=2$ | $-12.71$ dB | $-9.08$ dB | $\times1.494$ ($+3.5$ dB) |
| $k=3$ | $-25.42$ dB | $-19.31$ dB | slower geometric decay |
| $k=-1$ (mirror side) | $-117.9$ dB (numerical zero) | $-30.4$ dB | **one-sidedness breached** |

Attribution of the mirror line: taking $e^{j\theta_{APF}(t)}$ alone (without the AM factor) gives $k=-1$ at $-29.7$ dB — the breach comes from
the augmented model's $\theta(t)$ **no longer being of Adler/Riccati type** (the Möbius one-sidedness argument fails), not from the AM factor
itself. This agrees with the message of [P4] Fig. 14(c) (only ISF+APF matches the circuit simulation), but remember it is a prediction
**within the quasi-static ISF+APF model**, not transistor-level.

**Table II reconstruction (pure arithmetic, ✓)**: back out $f_L$ from [P4]'s theoretical $f_b=\sqrt{\Delta f^2-f_L^2}$: (a) $\sqrt{40^2-30.6^2}=25.8$ MHz,
(b) $\sqrt{30^2-6.6^2}=29.3$ MHz ⟹ $\Delta f-f_L=0.7$ MHz — exactly p.2131's "only 0.7 MHz below the lower edge" ✓. A side reading: the same
17-stage ring, the same 1.5 mA, 25.8 MHz on the upper side vs 29.3 MHz on the lower side — a numerical version of [P4]'s statement that
non-LC lock ranges are generally asymmetric (backed out from [P4]'s theoretical values, not measured on this site).

## 6. Worked Example (canonical numbers, one line per check)

Given $f_0=5$ GHz, $q_{max,0}=1$ pC, $Q=10$, a sinusoidal injection $I_{inj}=1.5$ mA (this page's representative "large injection").

1. **Two normalizations**: $I_{max}=\omega_0q_{max,0}=2\pi\cdot5\times10^9\cdot10^{-12}=31.42$ mA; $I_{osc}=I_{max}/Q=3.142$ mA;
   $a=I_{inj}/I_{osc}=0.4775$, $I_{inj}/I_{max}=0.048$ — linearity valid (4.8%), but the LC amplitude effect is large (48%).
   Dimension check: (rad/s)·C = C/s = A ✓.
2. **Lock range**: $\omega_{L0}=I_{inj}/(2q_{max,0})=1.5\times10^{-3}/(2\times10^{-12})=7.5\times10^8$ rad/s ⟹ $f_{L0}=119.37$ MHz;
   $\omega_L=\omega_{L0}/\sqrt{1-a^2}=7.5\times10^8/0.8786=8.536\times10^8$ rad/s ⟹ $f_L=135.85$ MHz (stretched by 13.8%).
3. **Amplitude memory**: $\tau_0=2Q/\omega_0=0.6366$ ns; check the identity $\tau_0\omega_{L0}=0.4775=a$ ✓.
4. **In lock at $\Delta\omega=0.5\,\omega_{L0}$ ($\Delta f=59.7$ MHz)**: ISF-only $\theta_{ss}=30.0^\circ$, $\omega_p=0.866\,\omega_{L0}$
   ⟹ $\tau_p=1.540$ ns; augmented $\theta_0=42.53^\circ$, $\omega_p^{APF}=0.6645\,\omega_{L0}$ ⟹ $\tau_p^{APF}=2.007$ ns.
   Lock time ($\theta(0)=0\to\theta_{ss}-0.01$): $\omega_{L0}T_{lock}=4.435$ ⟹ $5.913$ ns = 29.6 periods.
5. **Band centre**: $\tau_p^{ISF}=1/\omega_{L0}=1.333$ ns, $\tau_p^{APF}=(1+a)/\omega_{L0}=1.970$ ns.
6. **Out of lock at $\Delta\omega=2\omega_L$ ($\Delta f=271.7$ MHz)**: $f_b^{ISF}=244.1$, $f_b^{APF}=237.5$, naive formula $235.3$ MHz.

```python
import numpy as np
from scipy.optimize import brentq
f0, qmax, Q, Iinj = 5e9, 1e-12, 10.0, 1.5e-3       # [Hz], [C], [-], [A]
w0 = 2 * np.pi * f0                                # [rad/s]
Imax = w0 * qmax                                   # [A]  I_max := w0*q_max,0  ([P4] fn.11, p.2130)
Iosc = Imax / Q                                    # [A]  I_osc = I_max/Q      ([P4] p.2132; w0*q_max,0 = Q*I_osc, p.2124)
a = Iinj / Iosc                                    # [-]  = (1/2)*tau0*Iinj/qmax = (1/2)*Iinj*|Delta_1|
print(round(Imax * 1e3, 2), round(Iosc * 1e3, 4), round(a, 4))          # -> 31.42 3.1416 0.4775
wL0 = Iinj / (2 * qmax)                            # [rad/s] ISF-only half lock range ([P3] Eq.(34)-(35))
wL = wL0 / np.sqrt(1 - a ** 2)                     # [rad/s] [P4] Eq.(9) = Eq.(23) at beta = 90 deg
print(round(wL0 / 2 / np.pi / 1e6, 2), round(wL / 2 / np.pi / 1e6, 2))  # -> 119.37 135.85
tau0 = 2 * Q / w0                                  # [s]  [P4] Sec. III-B, p.2123
print(round(tau0 * 1e9, 4), round(tau0 * wL0, 4))                         # -> 0.6366 0.4775
# (i) pull-in at Dw = 0.5*wL0: ISF-only [P4] Eq.(32) vs augmented slope recipe ([P4] Table I footnote)
r0 = 0.5
th_ss = np.arcsin(r0)                              # [rad] ISF-only locked phase
wp_isf = np.sqrt(1 - r0 ** 2)                      # [wL0] Eq.(32), N = 1
g = lambda th: np.sin(th) / (1 + a * np.cos(th)) - r0
th0 = brentq(g, -np.arccos(-a), np.arccos(-a))     # [rad] augmented locked phase (stable branch cos th + a > 0)
wp_apf = (np.cos(th0) + a) / (1 + a * np.cos(th0)) ** 2                 # [wL0] -Omega'(theta_0)/wL0
print(round(np.degrees(th_ss), 2), round(wp_isf, 4), round(np.degrees(th0), 2), round(wp_apf, 4))  # -> 30.0 0.866 42.53 0.6645
# (ii) lock time theta(0)=0 -> theta_ss - 0.01 rad from [P4] Eq.(31) (psi = theta + pi/2, alpha = tan(psi0/2))
eps = 0.01
psi0 = th_ss + np.pi / 2
alpha = np.tan(psi0 / 2)
T = (2 / wp_isf) * (np.arctanh(np.tan((psi0 - eps) / 2) / alpha) - np.arctanh(np.tan(np.pi / 4) / alpha))
print(round(T, 3), round(T / wL0 * 1e9, 3), round(T / wL0 * f0, 1))     # -> 4.435 5.913 29.6
print(round(1 / wL0 * 1e9, 3), round((1 + a) / wL0 * 1e9, 3))           # -> 1.333 1.97
# (iii) pulled at Dw = 2*wL: beat frequency, ISF-only Eq.(34) vs augmented closed form vs naive
r = 2 * wL / wL0
wb_isf = np.sqrt(r ** 2 - 1)                       # [wL0] [P4] Eq.(34), N = 1
R2 = 1 + (r * a) ** 2                              # [-]
S = np.sqrt(r ** 2 * (1 - a ** 2) - 1)             # [-]  -> 0 exactly at the augmented lock edge Dw = wL
wb_apf = R2 * S / (1 + r * a ** 2 * S)             # [wL0] site derivation (Sec. 5.2)
wb_naive = np.sqrt(r ** 2 - (wL / wL0) ** 2)       # [wL0] Eq.(34) with Eq.(9)'s wL plugged in
print(round(wb_isf * wL0 / 2 / np.pi / 1e6, 1), round(wb_apf * wL0 / 2 / np.pi / 1e6, 1),
      round(wb_naive * wL0 / 2 / np.pi / 1e6, 1))                        # -> 244.1 237.5 235.3
```

## 7. lab_41: Four Faces of the Large-Injection LC Model (simulation and figure)

### 7.1 Model (dimensionless $\tau=\omega_{L0}t$; the ideal-LC dynamics depend only on $r=\Delta\omega/\omega_{L0}$ and $a$)

$$
\text{ISF-only: }\ \frac{d\theta}{d\tau}=r-\sin\theta;\qquad
\text{ISF+APF ([P4] Eq.(27)): }\ \frac{d\theta}{d\tau}=r-\frac{\sin\theta}{1+A},\ A=a\cos\theta;\qquad
\text{lagged (site): }\ a\frac{dA}{d\tau}=a\cos\theta-A .
$$

Fixed-step RK4; (a) $d\tau=0.002$, $\tau_{max}=24$; (d) $d\tau=0.01$, $2^{17}$ steps (≈427 beats), spectral lines taken as Fourier
coefficients over an integer number of beats (no leakage / scalloping), plotted with a Hann window and 4× zero padding.

### 7.2 Parameter table

| Parameter | Value | Unit | Source / note |
|---|---|---|---|
| $f_0$ | 5 | GHz | canonical |
| $q_{max,0}$ | 1 | pC | canonical |
| $Q$ | 10 | — | canonical ([tank_Q](/02_foundations/tank_Q_and_energy_restoration), phase_vs_amplitude_noise §5.6) |
| $I_{inj}$ | 1.5 | mA | representative "large injection" |
| $I_{max}=\omega_0q_{max,0}$ | 31.42 | mA | [P4] fn.11 |
| $I_{osc}=I_{max}/Q$ | 3.142 | mA | [P4] p.2132 |
| $a=I_{inj}/I_{osc}$ | 0.4775 | — | $=\tau_0\omega_{L0}$ |
| $\omega_{L0}$ / $f_{L0}$ | $7.5\times10^8$ / 119.37 | rad/s / MHz | ISF-only |
| $\omega_L$ / $f_L$ | $8.536\times10^8$ / 135.85 | rad/s / MHz | Eq.(9) |
| $\tau_0=2Q/\omega_0$ | 0.6366 | ns | 3.18 periods |
| Detuning in (a)(b) | $r_0=0.5$ | — | $\Delta f=59.7$ MHz |
| Detuning in (d) | $\Delta\omega=2\omega_L$ ($r=2.2762$) | — | $\Delta f=271.7$ MHz |
| Lock threshold $\varepsilon$ | 0.01 | rad | as in lab_36 |

### 7.3 Unit table

| Quantity | Unit | Note |
|---|---|---|
| $\theta,\psi,\varepsilon$ | rad | relative phase |
| $\Delta\omega,\omega_{L0},\omega_L,\omega_p,\omega_b$ | rad/s | normalized to $\omega_{L0}$ in the figure |
| $a,A,r,R,S$ | — | dimensionless |
| $\tau_0,\tau_p,T_{lock},T_b$ | s | ns in panel (b) |
| Spectrum | dB | relative to the $k=1$ main-line power |

### 7.4 Figure

![lab_41: (a) normalized phase deviation during acquisition (semilog) — ISF-only RK4, the [P4] Eq.(31) tanh closed form (circles), e^(−ω_p t) (dashed), and the slower ISF+APF pull-in; (b) amplitude 1+A(t) during acquisition: quasi-static vs first-order lag, θ(t) on the right axis; (c) large-injection lock characteristic sinθ/(1+a cosθ) for a=0/0.477/0.9 and the unbounded a=1.2; (d) pulled spectrum (Δω=2ω_L): the ISF-only one-sided comb vs ISF+APF with raised k=0, k=2 and an emerging mirror line](/figures/large_injection_transient.png)

### 7.5 How to read it

- **(a)**: vertical axis $\lvert\hat\theta(t)\rvert/\lvert\hat\theta(0)\rvert$ (the same kind of plot as [P4] Fig. 13), horizontal axis
  $\omega_{L0}t$. The blue line (ISF-only RK4) is completely covered by the circles (Eq.(31) closed form) and the dashed $e^{-\omega_pt}$,
  $\omega_p=0.866\,\omega_{L0}$; the red line (ISF+APF) has slope $0.6645$ — the $-\Omega'(\theta_0)$ of Table I's asterisk recipe. Both are
  straight lines: the linearized rate is the whole-trajectory rate.
- **(b)**: horizontal axis in real ns. Orange (quasi-static) starts at $0.80$, shoots to $1.4775$, falls back to $1.3519$ (black dotted);
  green (lagged) starts at $1.0$ (injection just on), peaks at $1.4577$ and 0.885 ns later; purple (right axis) $\theta$ climbs from
  $-115^\circ$ to $42.5^\circ$. The gray dashed line at $1.0$ is free-running.
- **(c)**: $\Delta\omega/\omega_{L0}=\sin\theta/(1+a\cos\theta)$. Solid = stable ($\cos\theta+a\gt0$), dashed = unstable; dotted lines are the
  respective edges $1/\sqrt{1-a^2}$ ($a=0$: 1; $0.477$: 1.138; $0.9$: 2.294). $a=1.2$ is drawn only for $\lvert\theta\rvert\le110^\circ$ (the
  empirical restriction of [P4] p.2127); its denominator crosses zero at $146.4^\circ$ and the curve is unbounded. Note that for $a\gt0$ the
  curve is depressed on the $\theta\lt0$ side and first depressed, then pulled up on the $\theta\gt0$ side: "in-phase weakens, anti-phase
  strengthens".
- **(d)**: horizontal axis $(\omega-\omega_{inj})/\omega_b$ (each with its own $\omega_b$), vertical axis relative to $k=1$. Blue (ISF-only): nothing
  at $k\lt0$, $-12.71$ dB per line for $k\ge2$; red (ISF+APF): $k=0$ up by 2.3 dB, $k=2$ up by 3.5 dB, and a $-30$ dB mirror line appears at $k=-1$.

### 7.6 Check numbers (`PYTHONPATH=. python3 simulations/lab_41_large_injection_transient.py`, 1.7 s on one machine)

```bash
# -> 0.4775  a = I_inj/I_osc ; tau0*omega_L0 = 0.4775 (= a, identity)
# -> 119.37 / 135.85 MHz  f_L0 (ISF-only) / f_L (Eq.9), ratio 1.1381 = 1/sqrt(1-a^2)
# -> 1.00000  edge check: max_theta sin/(1+a cos) over 1/sqrt(1-a^2)
# -> 2.16e-14 rad  (a) Eq.(31) closed form vs RK4, max deviation over the whole trajectory
# -> 4.435 / 4.435  (a) omega_L0*T_lock closed form / RK4 (lab_36 independent value 4.435)
# -> 0.8660 / 0.8700  (a) ISF-only omega_p/omega_L0: Eq.(32) / RK4 fit (ratio 1.0046)
# -> 42.53 deg, 0.6645 / 0.6649  (a) augmented theta_0, omega_p/omega_L0: slope recipe / RK4 fit (ratio 1.0006)
# -> 1.4775  (a) Dw=0: tau_p(APF)/tau_p(ISF) = 1+a ; 1.333 ns -> 1.970 ns = 9.8 cycles
# -> 17.0  (a) Table I(c) ideal-LC reconstruction of tau_p/T_inj (paper 17.4*, simulated 16.9; ISF-only gives only 12.2)
# -> -0.1987 / +0.4775 / +0.3519  (b) quasi-static A_min / A_max / A_final (overshoot 0.1256)
# -> -0.0443 / +0.4577 / +0.3519  (b) lagged A_min / A_max / A_final; peak delayed 0.885 ns; omega_p*tau0 = 0.317
# -> 3.32e-07 rad  (d) Eq.(33) closed form vs RK4, 427 beats
# -> 2.0448 / 2.0441  (d) ISF-only omega_b/omega_L0: Eq.(34) / measured
# -> 1.9896 / 1.9897 / 1.9713  (d) augmented omega_b/omega_L0: site closed form / measured / naive
# -> 244.1 / 237.5 MHz  (d) f_b ISF-only / augmented (Df = 271.7 MHz)
# -> 25.8 / 29.3 / 0.7 MHz  (d) Table II reconstruction f_L(a) / f_L(b) / Df-f_L(b)
# -> -12.23 -12.71 -25.42 -117.9  (d) ISF-only comb lines k0 k2 k3 mirror [dB rel. k1]
# -> -9.82 -9.08 -19.31 -30.4  (d) ISF+APF comb lines k0 k2 k3 mirror [dB rel. k1]
# -> 0.2314 / -12.71  (d) geometric ratio omega_L0/(Dw+omega_b) / per-line step dB (measured k2-k1 -12.71, k3-k2 -12.71)
# -> 1.299 / 1.494  (d) amplitude ratio (ISF+APF)/(ISF-only) of the k0, k2 lines
# -> -29.7  (d) mirror line dB of e^{j theta_APF} alone (no AM): the breach comes from theta(t), not from the AM factor
```

Full script: `simulations/lab_41_large_injection_transient.py` (depends on `savefig` from `simulations/common/plot_utils.py` and
`scipy.optimize.brentq`; deterministic, no seed). **Limitations**: pedagogical toy (ideal-LC ISF/APF, not transistor-level); both the
quasi-static APF and the first-order lag are linear amplitude models (no nonlinear restoring); (d) computes line amplitudes over
integer-beat windows, and the $-117.9$ dB mirror line is the floating-point floor.

## 8. Applicability / Failure Conditions and Honest Scope

| Condition | When it holds | When it fails |
|---|---|---|
| First-order linearity ($I_{inj}\ll I_{max}=\omega_0q_{max,0}$, [P4] fn.11) | ISF and APF each linear in the injection | Strong injection: the ISF/APF themselves deform with injection ([P4] Sec. III-E calls the model quasi-nonlinear — it captures only the division) |
| $a=I_{inj}/I_{osc}\lt1$ | Eq.(9)/(23) bounded, lock characteristic has an extremum | $a\ge1$: $1+A$ can reach zero, lock range unbounded (nonphysical); [P4] empirical cap $\theta\in[-110^\circ,110^\circ]$ |
| Ideal LC: pure-sine ISF/APF, $\beta=90^\circ$ | Eq.(27) = Generalized Adler (8), symmetric lock range, $\tanh$ / $\tan$ closed forms | Real LC: $\beta\ne90^\circ$ ⟹ asymmetric (Eq.(23)), Eq.(31)/(33) need the general $N\tilde\theta$ form; non-LC oscillators: the Sec. 2 derivation still holds for a purely sinusoidal lock characteristic, but $\tilde\Gamma_{LC}=\tilde\Gamma/(1+A)$ is exact only for oscillators with orthogonal state variables (fn.4) |
| Quasi-static amplitude ($\omega_p\tau_0=a\,\omega_p/\omega_{L0}\ll1$) | $A=a\cos\theta(t)$ holds pointwise | $a$ not small: the amplitude lags, the peak is smeared (Sec. 4.3 lag model, illustrative); steady state unaffected |
| Linear amplitude restoring ($d=e^{-t/\tau_0}$) | APF integral equals $\tau_0\tilde\Lambda$ | Large amplitude: nonlinear amplitude restoring ([P4] p.2128 admits the APF does not capture it; the centre deviation in Fig. 8) |
| Deterministic, noiseless | All of this page | With noise: in-lock shaping / cycle slips in injection_locking_noise Part A and lab_36 Part b; [P4] p.2130 defers "phase noise via the pulling equation" to [29, Ch. 7] (external) |

**What remains external and is not done on this site**: (i) [P4]'s original derivation of Eq.(31)/(33) is in Hong's Ph.D. dissertation
[29] (this site proves them itself in Sec. 2); (ii) the original Generalized Adler derivation by Mirzaei et al. [11] and the lock-range
derivations of [9], [10], [12] (this site uses only Eq.(7)–(9) as restated by [P4]); (iii) the geometric closed form of the pulling comb
(Armand 1969); (iv) nonlinear amplitude restoring, AM-to-PM, and circuit-level (Spectre / PDK) verification — beyond this site's Level-1
equation-level model; the circuit-simulation values in Tables I/II can only be quoted, not reproduced.

## What to remember

- **Generalized Adler = ISF/(1+A)**: [P4] Eq.(27) equals Eq.(8) term by term; the bridge is the identity $\omega_0q_{max,0}=QI_{osc}$ and
  $a=I_{inj}/I_{osc}=\tfrac12\tau_0I_{inj}/q_{max,0}=\tau_0\omega_{L0}$; lock range $\omega_{L0}/\sqrt{1-a^2}$ (Eq.(9) = Eq.(23) at
  $\beta=90^\circ$); unbounded for $a\ge1$ = the nonphysical zero-amplitude solution. **$I_{max}$ governs linearity, $I_{osc}$ governs the
  amplitude effect** — two different normalizations.
- **One quadratic, two signs**: $2\dot u=(\omega_{L0}+\Delta\omega)-(\omega_{L0}-\Delta\omega)u^2$, $u=\tan(\tilde\theta/2)$. In lock →
  $\tanh$ at rate $\omega_p=\sqrt{\omega_{L0}^2-\Delta\omega^2}$ (Eq.(31)–(32)); out of lock → $\tan$ at beat frequency $\omega_b=\sqrt{\Delta\omega^2-\omega_{L0}^2}$
  (Eq.(33)–(34)). The $/2$ in the $\tanh$ is half-angle bookkeeping; the decay rate is still $\omega_p$.
- **Lock time**: $T_{lock}=\dfrac{2}{\omega_p}[\operatorname{artanh}-\operatorname{artanh}]\approx\tau_p[\ln(2\sin\psi_0/\varepsilon)+\dots]$;
  $r_0=0.5$, $\varepsilon=0.01$ gives $\omega_{L0}T=4.435$ (identical to lab_36 digit for digit); diverges $\propto(1-r)^{-1/2}$ at the edge.
- **The APF slows pull-in**: $\omega_p^{APF}=\omega_{L0}(\cos\theta_0+a)/(1+a\cos\theta_0)^2$ (the slope recipe of Table I's asterisk); at band
  centre $\tau_p\times(1+a)$; the ideal-LC reconstruction of Table I(c) gives 17.0 (paper 17.4 / 16.9; only 12.2 without the APF).
- **Amplitude transient**: $A=a\cos\theta(t)$ ⟹ dip → overshoot (to $1+a$) → settle at $1+a\cos\theta_0$; the stable solution is the large
  amplitude; quasi-static criterion $\omega_p\tau_0\ll1$, 0.317 in the canonical case — the lag smears the peak without changing the steady state.
- **Large-injection pulling**: closed-form beat frequency $\omega_b^{APF}/\omega_{L0}=R^2S/(1+ra^2S)$ (site derivation; returns to Eq.(34) as
  $a\to0$, $S\to0$ at the augmented edge); the AM factor $=e^{j\theta}+\tfrac a2+\tfrac a2e^{j2\theta}$ raises $k=0$ ($\times1.30$) and $k=2$
  ($\times1.49$), and the $-30$ dB mirror line comes from the non-Adler $\theta(t)$ — the mechanism behind "ISF + APF" in [P4] Fig. 14(c).

## Further reading

- [paper_004](/05_paper_deep_dives/paper_004_injection_locking_part2): APF definition, quadrature, the origin of Eq.(27), and M:N / ILFD — the first half of this page.
- [lab_36](/04_simulation_labs/lab_36_lock_acquisition): the $R$-form of the same in-lock exact solution, critical slowing swept in $r$ to 0.99, and cycle slips with noise.
- [injection_locking_noise](/06_design_insights/injection_locking_noise): Part A in-lock noise shaping (the corner is $\omega_p$), Part B beat frequency and the one-sided comb (Armand), injection waveform design.
- [phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise): amplitude recovery with $\tau_0=2Q/\omega_0$, the OU process and the flat-topped Lorentzian — the noise version of this page's lag model.
- [paper_003](/05_paper_deep_dives/paper_003_injection_locking_part1): generalized Adler, the lock characteristic, and the original definition $\omega_p:=-\Omega'(\theta_0)$ ([P3] Eq.(38)–(40)).
- [tank_Q](/02_foundations/tank_Q_and_energy_restoration): $Q$, $2Q/\omega_0$ vs $Q/\omega_0$, and where the canonical $Q=10$ comes from.
- lab_37 (`simulations/lab_37_ilfd_lock.py`, documented inside the [paper_004](/05_paper_deep_dives/paper_004_injection_locking_part2) page): how the $N$ enters Eq.(31)–(34) when $N\ne1$ (out-of-lock drift rate $\omega_b/N$).

### External references (not among the 5 downloaded PDFs; citations taken verbatim from [P4]'s bibliography, p.2138)

- **[P4]-[11]** A. Mirzaei, M. E. Heidari, R. Bagheri, S. Chehrazi, and A. A. Abidi, *"The quadrature LC oscillator: A complete
  portrait based on injection locking,"* IEEE J. Solid-State Circuits, vol. 42, no. 9, pp. 1916–1932, Sep. 2007.
  (Original source of Generalized Adler's equation and of $V_{osc}=(I_{osc}+I_{inj}\cos\theta)R_P$.)
- **[P4]-[9]** L. J. Paciorek, *"Injection locking of oscillators,"* Proc. IEEE, vol. 53, no. 11, pp. 1723–1727, Nov. 1965;
  **[P4]-[10]** B. Razavi, *"A study of injection locking and pulling in oscillators,"* IEEE J. Solid-State Circuits, vol. 39,
  no. 9, pp. 1415–1424, Sep. 2004; **[P4]-[12]** B. Hong and A. Hajimiri, *"A phasor-based analysis of sinusoidal injection
  locking in LC and ring oscillators,"* IEEE Trans. Circuits Syst. I, Reg. Papers, vol. 66, no. 1, pp. 355–368, Jan. 2019.
  (The [9]–[12] that [P4] p.2123 credits with "independently" deriving Eq.(9).)
- **[P4]-[29]** B. Hong, *"Periodically disturbed oscillators,"* Ph.D. dissertation, Dept. Elect. Eng., California Inst.
  Technol., Pasadena, CA, USA, 2018. doi: 10.7907/W0A7-4258. (Original derivation of Eq.(31), (33); Ch. 7 on phase noise via the pulling equation.)
- **[E-Armand]** M. Armand, *"On the Output Spectrum of Unlocked Driven Oscillators,"* Proc. IEEE, vol. 57, no. 5, pp. 798–799,
  May 1969. (One-sided geometric closed form of the ISF-only pulling comb; already listed in injection_locking_noise.)
