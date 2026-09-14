---
title: "[P2] Jitter and Phase Noise in Ring Oscillators"
description: "Hajimiri–Limotyrakis–Lee 1999 deep dive: accumulated jitter, Γrms∝N^(-3/2), N-independence (verified), symmetry, and Fig.17."
---

> **β**: This English translation is in beta — the Traditional-Chinese original is the authoritative version.

# Jitter and Phase Noise in Ring Oscillators

> **Prerequisites (recommended reading order)**: first digest [paper_001](/05_paper_deep_dives/paper_001_general_theory_phase_noise) (ISF, $\Gamma_{rms}^2/q_{max}^2$, the symmetry rule) — every conclusion on this page is [P1]'s ISF applied to the ring. For the time-/frequency-domain language of jitter see [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter).

[P2] applies the ISF framework of [P1] **to the ring oscillator**. It answers three very practical
questions: (1) how does the long-term jitter of a free-running ring grow with time? (2) what effect
does the number of stages $N$ have on phase noise? (3) why does waveform symmetry suppress close-in
noise? The answers are, respectively, $\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$,
$\Gamma_{rms}\propto N^{-3/2}$ (with "nearly $N$-independent at fixed power and frequency"), and the symmetry experiment of Fig. 17.

## Citation

> **[P2]** A. Hajimiri, S. Limotyrakis, and T. H. Lee, *"Jitter and Phase Noise in Ring
> Oscillators,"* IEEE J. Solid-State Circuits, vol. 34, no. 6, pp. 790–804, Jun. 1999.
> (file `jitter_ring.pdf`, paper_002)

## One-sentence contribution

Applying [P1]'s ISF to the ring oscillator yields closed forms for jitter and phase noise, the
$\Gamma_{rms}\propto N^{-3/2}$ scaling, and the counter-intuitive conclusion that "at fixed $f_0$
and power, the phase noise/jitter of a single-ended ring is nearly independent of the number of
stages $N$" (claim C7, C8).

## Why this paper matters

An LC oscillator needs an inductor — large area, hard to integrate; **a ring oscillator is all
inverters: small area, easy to integrate, wide tuning range** — the most common VCO in PLLs/CDRs.
But a ring's phase noise is usually much worse than an LC's — [P2] uses the ISF to explain
**why**, and gives actionable design rules:

- It ties the ring's jitter to **the same $\Gamma_{rms}^2/q_{max}^2$ ratio as phase noise** (claim C6),
  unifying "time-domain jitter" and "frequency-domain phase noise" under the ISF framework.
- It settles a commonly misunderstood question: "does adding more stages $N$ to a ring make it
  better?" Under the constraint of fixed power and frequency the answer is "**almost no
  difference**" (claim C7) — more stages shrink $\Gamma_{rms}$, but each stage's swing shrinks and
  there are more devices; the effects cancel.
- It confirms [P1]'s symmetry rule with measurements (Fig. 17): tuning the control voltage to the
  point of symmetric rise/fall produces a **minimum** in phase noise (claim C4).

## Main assumptions

Per paper_metadata (paper_002.assumptions):

1. The same LTV/ISF small-perturbation assumptions as [P1].
2. Per-stage device noise is white (plus a 1/f component handled via symmetry).
3. Identical stages; delay and noise add independently at every transition.

> **Physical intuition**: nearly all of a ring's energy is injected in the instant of a transition
> (edge flip), so its ISF is not the smooth $-\sin$ of an LC but a set of **sharp peaks concentrated
> at the transitions** ([P2] Fig. 5). The sensitive spots — where a kick hurts phase the most — sit
> on those peaks. The more stages, the smaller the fraction of the full period a single transition
> occupies, and the smaller the rms ISF.

## Key equations

### Eq.(8): accumulated jitter (the random-walk fingerprint)

**Original formula** ([P2] Eq.(8), p.792; κ from Eq.(12), p.793):

$$
\sigma_{\Delta t}=\kappa\sqrt{\Delta t}
$$

**Meaning**: for two edges of a free-running oscillator separated by $\Delta t$, the standard
deviation of the timing error is **proportional to $\sqrt{\Delta t}$** — the **random-walk
fingerprint** of an oscillator with "no absolute time reference" (claim C6). $\kappa$ is a
device-dependent proportionality constant with units of $\sqrt{\text{s}}$.

**Step-by-step derivation**: each transition injects an independent, zero-mean timing perturbation
with variance $\sigma_{step}^2$. Over $\Delta t$ there are about $M=\Delta t/T$ transitions;
independent quantities add in variance:

$$
\begin{aligned}
\sigma_{\Delta t}^2 &= M\,\sigma_{step}^2 = \frac{\Delta t}{T}\,\sigma_{step}^2 \\
\Rightarrow\quad \sigma_{\Delta t} &= \underbrace{\frac{\sigma_{step}}{\sqrt{T}}}_{\equiv\,\kappa}\sqrt{\Delta t}=\kappa\sqrt{\Delta t}.
\end{aligned}
$$

**Dimension check**: $\kappa$ is $\sqrt{\text{s}}$ and $\sqrt{\Delta t}$ is $\sqrt{\text{s}}$;
their product is $\text{s}$ ✓. Cross-check against [P1] in the frequency domain:
$\sigma_{\Delta t}\propto\sqrt{\Delta t}$ corresponds to 1/f² phase noise (the two are the
time-/frequency-domain faces of the same thing).

**Numerical example**: the toy ring sets per-edge $\sigma_{step}=50$ fs (see the parameters of
`ring_oscillator_timing_noise_accumulation.png`). Accumulated jitter over $\Delta t=1$ µs (about
5000 periods at $f_0=5$ GHz): first find $\kappa$. With $T=200$ ps,
$\kappa=50\text{fs}/\sqrt{200\text{ps}}=50\times10^{-15}/\sqrt{2\times10^{-10}}=3.54\times10^{-9}\ \sqrt{\text{s}}$,
so $\sigma_{\Delta t}=3.54\times10^{-9}\times\sqrt{10^{-6}}=3.54\ \text{ps}$. Intuition: the longer the separation, the larger the drift — but it grows only slowly, as $\sqrt{\Delta t}$.

**Python verification**:

```python
import numpy as np
from simulations.common.oscillator_models import accumulated_jitter_curve

# toy random walk: each edge adds an independent 50 fs timing perturbation
lags, sigma = accumulated_jitter_curve(f0=5e9, sigma_edge=50e-15, max_lag_periods=500, n_trials=2000)
# expect sigma(lag) ~ sigma_edge * sqrt(lag) -> log-log slope 0.5
slope = np.polyfit(np.log(lags[1:]), np.log(sigma[1:]), 1)[0]
print(round(slope, 2))  # -> 0.50
```

The full toy derivation is in [lab_03_ring_oscillator_toy_model](/04_simulation_labs/lab_03_ring_oscillator_toy_model)
(**pedagogical toy model, not transistor-level**).

### Eq.(11)–(12): the jitter constant κ and its relation to the ISF (verified ✓)

**Original formula** ([P2] Eq.(11)–(12), p.793, proportionality):

$$
\kappa^2\;\propto\;\frac{\Gamma_{rms}^2}{q_{max}^2}\cdot\frac{\overline{i_n^2}}{\Delta f}
$$

**Meaning**: the jitter proportionality constant $\kappa$ is set by **exactly the same
$\Gamma_{rms}^2/q_{max}^2$ ratio as phase noise** (claim C6). This ties time-domain jitter and
frequency-domain phase noise to the same ISF quantity: the knobs that lower phase noise lower
jitter as well.

> **Verified**: [P2] Eq.(12), p.793 gives $\kappa=\frac{\Gamma_{rms}}{q_{max}}\sqrt{\tfrac12\tfrac{\overline{i_n^2}}{\Delta f}}$ (verified verbatim against the original PDF rendering);
> it shares the same $\Gamma_{rms}^2/q_{max}^2$ ratio with phase noise (claim C6).

### Eq.(14): ring frequency vs number of stages

**Original formula** ([P2] Eq.(14), p.794):

$$
f_0=\frac{1}{2N\tau_D}
$$

**Meaning**: an $N$-stage ring with per-stage delay $\tau_D$ oscillates at this frequency. **The
factor of 2** comes from the signal having to travel around the ring **twice** per period (one lap
inverts; a second lap returns it in phase) to complete one full cycle.

**Dimension check**: $1/(N\cdot\text{s})=\text{Hz}$ ✓ ($N$ dimensionless).

**Numerical example**: for a 5-stage ring at $f_0=5$ GHz, the per-stage delay is
$\tau_D=1/(2\times5\times5\times10^9)=2\times10^{-11}\ \text{s}=20$ ps. Doubling to $N=10$
while keeping 5 GHz halves the per-stage delay to 10 ps — this is exactly where "at fixed
frequency, larger $N$ forces faster, smaller-swing stages" comes from, leading into the
N-independence below.

### Eq.(16): rms-ISF scaling with the number of stages (re-verified in v7 ✓)

**Original formula** ([P2] Eq.(16), p.794; the radical covers only the constant term):

$$
\Gamma_{rms}=\sqrt{\dfrac{2\pi^2}{3\eta^3}}\;\dfrac{1}{N^{1.5}}
$$

where $\eta$ is the frequency proportionality constant (Eq.(14)–(15): $\hat t_D=\eta/f_{max}$, $2\pi=2N\eta/f_{max}$);
at $\eta=0.75$, $\sqrt{2\pi^2/(3\times0.75^3)}\approx3.95\approx4$, i.e. $\Gamma_{rms}\approx4/N^{1.5}$,
which is the solid line in [P2] Fig. 8 — the radical covers only the constant, and $1/N^{1.5}$ sits outside it.

**Meaning**: **$\Gamma_{rms}\propto N^{-3/2}$** (i.e. $\Gamma_{rms}^2\propto N^{-3}$).
Intuition: with more stages, each transition occupies a narrower "sensitive window" of the $2\pi$ period and the peaks get shorter, so the rms naturally shrinks.

> **[P2] Eq.(16), p.794 (re-verified in v7: the radical covers only the constant, $\Gamma_{rms}\propto N^{-3/2}$;
> triple-confirmed by the prose's $4/N^{1.5}$@$\eta=0.75$ and App.B Eq.(55). v3 had misread this as $N^{-3/4}$)**:
> three independent lines of evidence — (1) the paper's own text (p.794, the paragraph after Eq.16) states
> "the $1/N^{1.5}$ dependence of $\Gamma_{rms}$"; (2) the $\eta=0.75$ numerical anchor: the text says
> "solid line = $\Gamma_{rms}\approx4/N^{1.5}$, obtained from (16) for $\eta=0.75$", and
> $\sqrt{2\pi^2/(3\times0.75^3)}=3.95\approx4$ ✓ (if $N^{1.5}$ were inside the radical this would give
> $4/N^{0.75}$, contradicting the text); (3) independent algebra in App.B Eq.(52)+(54) (p.803):
> $\Gamma_{rms}^2=(1/3\pi)(1/f'_{rise})^3(1+A^3)$, $2\pi=\eta N(1+A)/f'_{rise}$, which combine to give
> $\Gamma_{rms}^2=(2\pi^2/3\eta^3)\cdot[4(1+A^3)/(1+A)^3]\cdot N^{-3}$; at $A=1$ the bracket equals 1, so
> $\Gamma_{rms}^2\propto N^{-3}\Rightarrow\Gamma_{rms}\propto N^{-3/2}$ ✓. All three point to $N^{-3/2}$;
> there is no real "formula-vs-text" inconsistency — it was a prior misreading of the radical's scope.

### Eq.(23): ring white-noise phase-noise FOM and N-independence (prefactor corrected to 8/(3η) and verified)

**Original formula** ([P2] Eq.(23), p.796; the $V_T=0$ lower bound is Eq.(25)):

$$
\mathcal{L}\{\Delta f\}=\frac{8}{3\eta}\cdot\frac{kT}{P}\cdot\frac{V_{DD}}{V_{char}}\cdot\left(\frac{f_0}{\Delta f}\right)^2
\qquad\Big(\min_{V_T=0}:\ \frac{16\gamma}{3\eta}\cdot\frac{kT}{P}\cdot\frac{f_0^2}{\Delta f^2}\Big)
$$

where $\gamma$ is the MOSFET channel thermal-noise coefficient ($2/3$ long-channel, larger for
short-channel), $V_{char}$ is the device's **characteristic voltage** (long-channel
$\approx\Delta V/\gamma$), $P$ is the power dissipation (Eq.(21): $P=2\eta N V_{DD}q_{max}f_0$),
and the per-stage noise is given by Eq.(17),(18) $\overline{i_n^2}/\Delta f=4kT\gamma\mu C_{ox}(W/L)\Delta V$.

**Meaning**: ring white-noise phase noise collapses into a figure of merit — only $kT/P$, the
voltage ratio $V_{DD}/V_{char}$, and $(f_0/\Delta f)^2$ appear. **Key conclusion (claim C7): $N$
is entirely absent from Eq.(23) — at fixed $f_0$ and power $P$, the phase noise of a single-ended
ring is independent of the number of stages $N$.**

**Why N-independent**: microscopically, raising $N$ lowers $\Gamma_{rms}$ (Eq.16) but
simultaneously lowers each stage's swing $q_{max}$ and adds more noisy stages; [P2] shows these
effects cancel exactly at fixed $P$, $f_0$, so Eq.(23) contains no $N$. Hence "how many stages
should my ring have" is not decided by phase noise, but by phase margin, tuning range, area,
quadrature needs, and other considerations.

> **Correction note (v3)**: the prefactor of [P2] Eq.(23) is $8/(3\eta)$ ($\eta$ being the
> stage-delay proportionality constant of Eq.14, $\approx1$); $\gamma$ enters only through
> $V_{char}=\Delta V/\gamma$. (v2 mistakenly changed it to $8/(3\gamma)$ and mislabeled it
> "verified verbatim"; v3 corrected it against the original PDF p.796.) The $V_T=0$ lower bound is
> accordingly corrected to $16\gamma/(3\eta)$. $\gamma$ (noise coefficient) and $\eta$ (frequency
> proportionality constant, Eq.14) are different quantities — do not confuse them.

### Eq.(27)–(30): short-channel velocity-saturation current/noise model and $V_{char}=E_cL/\gamma$ (verified ✓)

**Original formulas** ([P2] Sec. V-A, p.796, verified verbatim against a render of the original PDF):

The drain current of a short-channel device is governed by **velocity saturation** (the field is so high that the carrier velocity no longer rises with it) (Eq.(27)):

$$
I_D=\frac{\mu C_{ox}}{2}\,W\,E_c\,\Delta V
$$

where $E_c$ is the **critical electric field**, defined in the paper as the field at which the carrier velocity drops to half the value expected from the low-field mobility.
Combining Eq.(27) with Eq.(17) gives the drain-current noise of a short-channel MOS device (Eq.(28)):

$$
\frac{\overline{i_n^2}}{\Delta f}=8kT\,\frac{\gamma I_D}{E_cL}
$$

The oscillation frequency (Eq.(29), as printed):

$$
f_0=\frac{1}{2Nt_D}=\frac{1}{\eta N(t_r+t_f)}=\frac{\mu_{eff}W_{eff}C_{ox}\Delta V^2}{8\eta NLq_{max}}
$$

Re-running the Eq.(23)/(24) derivation with (28) and (29), the paper states that one obtains **the same** phase-noise and jitter expressions, except for a new $V_{char}$ (Eq.(30)):

$$
V_{char}=\frac{E_cL}{\gamma}
$$

and notes that the result is larger than the long-channel case by a factor $\gamma\Delta V/E_cL$ (p.796), adding verbatim: "Again, note the absence of any dependency on the number of stages." — **N-independence survives in the short-channel branch**.

**Step-by-step derivation of Eq.(28)** (the same move this site uses to go from Eq.(17) to Eq.(18)):

1. Eq.(17) (p.795): $\overline{i_n^2}/\Delta f=4kT\gamma g_{d0}=4kT\gamma\,\mu C_{ox}(W/L)\Delta V$. The paper states explicitly that this holds in both long- and short-channel regimes as long as the right $\gamma$ is used ($2/3$ long-channel, "typically two to three times greater" short-channel).
2. Solve Eq.(27) for $\mu C_{ox}W\Delta V=2I_D/E_c$.
3. Substitute:

$$
\frac{\overline{i_n^2}}{\Delta f}=4kT\gamma\cdot\frac{1}{L}\cdot\underbrace{\mu C_{ox}W\Delta V}_{=\,2I_D/E_c}=\frac{8kT\gamma I_D}{E_cL}\quad\checkmark
$$

**Dimension check**: $kT$ is J $=$ V·A·s, $I_D$ is A, $E_cL$ is (V/m)·m $=$ V; hence $8kT\gamma I_D/(E_cL)=$ V·A·s·A/V $=$ A²·s $=$ A²/Hz ✓.

**Physical meaning**: in the long-channel case $g_{d0}\propto(W/L)\Delta V$, so the noise rises linearly with overdrive; once velocity-saturated, the current is only linear in $\Delta V$ (Eq.(27)) and the effective $g_{d0}=2I_D/(E_cL)$ — the noise is **directly proportional to the current and inversely proportional to $E_cL$**. $E_cL$ is a "voltage": the voltage scale needed to push carriers to saturation velocity over a channel of length $L$; for the 0.25 µm process, $E_c\approx4\times10^6$ V/m gives $E_cL=1.0$ V (the numbers [P2] uses for oscillator number 3 on p.799).

**Step-by-step derivation of Eq.(30)** (supplied by this site; it also shows why $N$ still cancels):

1. $N$ identical noise sources, one per node, so the total phase noise is $N$ times Eq.(6); insert Eq.(16) $\Gamma_{rms}^2=2\pi^2/(3\eta^3N^3)$ and Eq.(28):

$$
\mathcal{L}\{\Delta f\}=N\cdot\frac{2\pi^2}{3\eta^3N^3}\cdot\frac{1}{8\pi^2\Delta f^2}\cdot\frac{8kT\gamma I_D/(E_cL)}{q_{max}^2}=\frac{2kT\gamma\,I_D}{3\eta^3N^2\,E_cL\,\Delta f^2\,q_{max}^2}
$$

> **Convention flag**: the denominator of [P2] Eq.(6) (p.792, verified verbatim) is $8\pi^2f_{off}^2=2\Delta\omega^2$, i.e. this site's $\mathcal{L}_{/2}=\kappa^2/\Delta\omega^2$ family of [diffusion_dictionary](/03_isf_core_theory/diffusion_dictionary) — **3 dB above** the $4\Delta\omega^2$ ($\mathcal{L}_{/4}$) in the denominator of [P1] Eq.(21). This section and the "Measured validation" section below keep the books exactly as Eq.(6) is printed, which is why they reproduce the paper's numbers digit for digit; switching to [P1] Eq.(21) would lower every absolute value by $3$ dB while leaving every scaling and the $N$-independence untouched.

2. **Stage delay**: during a transition $I_D$ charges the node to $q_{max}$, so $t_r\approx t_f\approx q_{max}/I_D$ and $f_0=1/(\eta N(t_r+t_f))\approx I_D/(2\eta Nq_{max})$ — the single-ended twin of Eq.(32) (differential, charged by $I_{tail}$); solve for $I_D=2\eta Nq_{max}f_0$.
3. **Power**: Eq.(21) $P=2\eta NV_{DD}q_{max}f_0\Rightarrow q_{max}=P/(2\eta NV_{DD}f_0)$.
4. Back into step 1 (first $I_D$, then $q_{max}$):

$$
\mathcal{L}\{\Delta f\}=\frac{2kT\gamma\cdot2\eta Nq_{max}f_0}{3\eta^3N^2E_cL\Delta f^2q_{max}^2}=\frac{4kT\gamma f_0}{3\eta^2N\,E_cL\,\Delta f^2\,q_{max}}=\frac{4kT\gamma f_0\cdot2\eta NV_{DD}f_0}{3\eta^2N\,E_cL\,\Delta f^2\,P}=\frac{8}{3\eta}\cdot\frac{kT}{P}\cdot\frac{V_{DD}}{E_cL/\gamma}\cdot\frac{f_0^2}{\Delta f^2}
$$

which is exactly Eq.(23) with $V_{char}=E_cL/\gamma$ (Eq.(30)) ✓. **Exponent bookkeeping** (fixed $P$, $f_0$): $q_{max}\propto1/N$, while $I_D=2\eta Nq_{max}f_0=P/V_{DD}$ is $N$-independent; hence $N^{+1}\cdot N^{-3}\cdot N^{0}\cdot N^{+2}=N^0$ (from the source count, $\Gamma_{rms}^2$, $S_i\propto I_D$, and $1/q_{max}^2$ respectively) — exactly the same cancellation as in the long-channel branch.

> **A note on Eq.(29) as printed (this site's reading; to be verified)**: the last term of Eq.(29) on p.796 is **verbatim identical** to Eq.(22) (p.795) ($\mu_{eff}W_{eff}C_{ox}\Delta V^2/(8\eta NLq_{max})$, still containing $\Delta V^2/L$); if one really substitutes that last term together with Eq.(28), the prefactor comes out as $16/(3\eta)$ instead of the $8/(3\eta)$ printed in Eq.(23), and Eq.(30) does not follow. This site's derivation uses only the first two equalities of Eq.(29) ($f_0=1/(\eta N(t_r+t_f))$) plus $t_r\approx q_{max}/I_D$; that route simultaneously reproduces the printed $8/(3\eta)$ of Eq.(23), the $E_cL/\gamma$ of Eq.(30), and the Table I Pred.(23) value for oscillator number 3 (see below). With Eq.(27) substituted, the short-channel frequency should read $f_0\approx\mu_{eff}W_{eff}C_{ox}E_c\Delta V/(4\eta Nq_{max})$ (no $L$, and $\Delta V$ only to the first power). Whichever form is used, as long as $I_D$ comes from Eq.(27), $N$ cancels and Eq.(30) is unchanged.

**Numerical example (with the paper's numbers for oscillator number 3, p.799)**: $E_c=4\times10^6$ V/m, $\gamma=2.5$, $L=0.25$ µm, simulated mid-transition current $I_D=3.47$ mA, $kT$ at $300$ K:

- Eq.(28): $8\times4.14\times10^{-21}\times2.5\times3.47\times10^{-3}/(4\times10^6\times0.25\times10^{-6})=2.87\times10^{-22}$ A²/Hz (the paper prints $2.87\times10^{-22}$ ✓).
- Eq.(30): $V_{char}=E_cL/\gamma=1.0/2.5=0.4$ V.
- **Long- vs short-channel degradation ratio**: the paper only gives the factor $\gamma\Delta V/E_cL$. If the long-channel $V_{char}=\Delta V/\gamma$ is used with the same $\gamma$ on both sides, the algebraic ratio is $(\Delta V/\gamma)/(E_cL/\gamma)=\Delta V/(E_cL)$, with no $\gamma$; this site reads the extra $\gamma$ in the printed factor as the ratio $\gamma_S/\gamma_L$ (to be verified) — p.795 states that the short-channel $\gamma$ is "typically two to three times greater", and in practice the difference comes mostly from $\gamma$ itself. Taking $\Delta V=V_{DD}/2-V_T$ and **assuming** $V_T=0.5$ V (the paper does not print $V_T$ for the 0.25 µm process; to be verified) gives $\Delta V=0.75$ V: long-channel $V_{char}=\Delta V/\gamma_L=0.75/(2/3)=1.125$ V, short-channel $0.4$ V, ratio $2.81$, i.e. **$+4.5$ dB**; velocity saturation alone (same $\gamma$) gives a ratio of only $0.75$ (slightly better, in fact) — what really penalizes the short-channel device is $\gamma\approx2.5$, not $E_c$.
- **Convention flag**: this section introduces no new 2/4/SSB factor; all SSB bookkeeping lives in Eq.(6)/(23) (see the flag above).

**Python verification**:

```python
import numpy as np
k, T = 1.380649e-23, 300.0
kT = k*T                                   # J
Ec, L, gam_s, gam_l = 4e6, 0.25e-6, 2.5, 2/3   # [P2] p.799 numbers for oscillator #3; long-channel gamma = 2/3
ID = 3.47e-3                                # A, simulated mid-transition drain current (#3)
Si_28 = 8*kT*gam_s*ID/(Ec*L)                # [P2] Eq.(28)
Vchar_s = Ec*L/gam_s                        # [P2] Eq.(30)
print(f"{Si_28:.2e}")                       # -> 2.87e-22  A^2/Hz (paper prints 2.87e-22)
print(round(Vchar_s, 3))                    # -> 0.4  V
# short vs long channel: paper prints the factor gamma*dV/(Ec*L) (p.796); the site reads it with two gammas
VT = 0.5                                    # V, ASSUMED (the paper does not print V_T for the 0.25 um process)
dV = 2.5/2 - VT                             # gate overdrive at mid-transition, [P2] p.795
Vchar_l = dV/gam_l
ratio = Vchar_l/Vchar_s                     # = (gam_s/gam_l)*dV/(Ec*L)
print(round(Vchar_l,3), round(ratio,2), round(10*np.log10(ratio),1))   # -> 1.125 2.81 4.5
print(round(dV/(Ec*L),2))                   # -> 0.75  same-gamma ratio dV/(Ec L)
# N-independence check: N x Eq.(6) with Eq.(16),(28) under P = 2*eta*N*VDD*qmax*f0 and f0 = ID/(2*eta*N*qmax)
def L_short(N, P=25e-3, f0=1.33e9, VDD=2.5, eta=0.75, df=1e6):
    qmax = P/(2*eta*N*VDD*f0); ID = 2*eta*N*qmax*f0
    G2 = 2*np.pi**2/(3*eta**3*N**3)
    Si = 8*kT*gam_s*ID/(Ec*L)
    return 10*np.log10(N*G2*Si/(8*np.pi**2*df**2*qmax**2))
Ls = [round(float(L_short(N)),2) for N in (3,5,7,11,19)]
L23 = 10*np.log10(8/(3*0.75)*kT/25e-3*2.5/Vchar_s*(1.33e9/1e6)**2)
print(Ls, round(L23,2))   # -> [-111.86, -111.86, -111.86, -111.86, -111.86] -111.86   dBc/Hz (identical for N = 3..19 and equal to Eq.(23))
```

**Applicability and failure conditions**: Eq.(27) is a first-order fully-velocity-saturated model (valid only for $\Delta V\gg E_cL$; oscillator number 3 has $\Delta V\approx0.75$ V against $E_cL=1.0$ V, which is really only the transition region, yet the paper applies it directly); the value of $\gamma$ (2–3) is itself empirical and bias-dependent; Eq.(28) counts channel thermal noise only — no gate resistance, substrate, or induced-gate noise. For the measured comparison see "Measured validation" below.

### Eq.(31)–(35): differential-ring phase noise — with an explicit $N$ (verified ✓)

**Original formulas** ([P2] Sec. V-B, p.796, verified verbatim against a render of the original PDF):

Power (Eq.(31)) and frequency (Eq.(32)):

$$
P=N\,I_{tail}\,V_{DD}
\qquad\qquad
f_0=\frac{1}{2Nt_D}\approx\frac{1}{2\eta N t_r}\approx\frac{I_{tail}}{2\eta N q_{max}}
$$

Noise on each single-ended node (Eq.(33); two shares — differential transistor + load resistor
$R_L$ — with $V_{char}=(V_{GS}-V_T)/\gamma$ for a balanced long-channel stage, $E_cL/\gamma$
short-channel):

$$
\frac{\overline{i_n^2}}{\Delta f}=\left(\frac{\overline{i_n^2}}{\Delta f}\right)_{N}+\left(\frac{\overline{i_n^2}}{\Delta f}\right)_{Load}=4kT\,I_{tail}\left(\frac{1}{V_{char}}+\frac{1}{R_L I_{tail}}\right)
$$

The ring has $2N$ nodes (two outputs per stage), and the total phase noise is $2N$ times the
single-source value (p.796, verbatim: "The phase noise and jitter due to all $2N$ noise sources is
$2N$ times the value given by (6) and (12)." — this 2 is a **node count**, not the SSB convention's
2). Combined with the $\Gamma_{rms}$ of Eq.(16), it collapses into (Eq.(34)/(35); $\mathcal{L}$ is
the paper's $L\{\Delta f\}$):

$$
\mathcal{L}_{min}\{\Delta f\}=\frac{8}{3\eta}\cdot N\cdot\frac{kT}{P}\cdot\left(\frac{V_{DD}}{V_{char}}+\frac{V_{DD}}{R_L I_{tail}}\right)\cdot\frac{f_0^2}{\Delta f^2}
$$

$$
\kappa_{min}=\sqrt{\frac{8}{3\eta}}\cdot\sqrt{N\cdot\frac{kT}{P}\cdot\left(\frac{V_{DD}}{V_{char}}+\frac{V_{DD}}{R_L I_{tail}}\right)}
$$

The paper states verbatim that both are "valid in both long- and short-channel regimes of operation
with the right choice of $V_{char}$"; a bipolar differential ring's shot + load noise (Eq.(36),
p.797) folds back into **the same two equations** with $V_{char}=4kT/q_e$.

**Meaning**: only two differences from single-ended Eq.(23) — **an explicit $N$**, and an extra
load share $V_{DD}/(R_L I_{tail})$ in the bracket. At fixed $f_0$ and $P$, a differential ring's
phase noise **degrades with $N$** ($\Delta\mathcal{L}=10\log_{10}(N_2/N_1)$; for jitter,
$\kappa_{min}\propto\sqrt N$) — the lost other half of N-independence.

**Why the $N$ appears** (exponent bookkeeping, fixed $P$, $f_0$, fixed swing): $P=NI_{tail}V_{DD}$
is a **static** bookkeeping (unlike Eq.(21), it is not tied to $f_0$), so fixed $P$ forces
$I_{tail}\propto1/N$; Eq.(32) then forces $q_{max}=I_{tail}/(2\eta Nf_0)\propto1/N^2$ (p.797,
verbatim: "…reduce the swing, and hence $q_{max}$, by a factor of $1/N^2$"). Hence
$2N\cdot\Gamma_{rms}^2\cdot S_i/q_{max}^2\propto N\cdot N^{-3}\cdot N^{-1}\cdot N^{4}=N^{+1}$.
Full term-by-term table and worked example:
[lc_vs_ring Step 2b](/06_design_insights/lc_vs_ring).

> **[P2]'s conclusion sentence (pp.796–797, verbatim)**: "Note that, in contrast with the
> single-ended ring oscillator, a differential oscillator does exhibit a phase noise and jitter
> dependency on the number of stages, with the phase noise degrading as the number of stages
> increases for a given frequency and power dissipation."

**Numerical example**: $f_0=5$ GHz, $\Delta f=1$ MHz, $kT=4.0\times10^{-21}$ J, $P=1$ mW,
$\eta\approx1$, $V_{DD}/V_{char}=3$, $V_{DD}/(R_LI_{tail})=2$ (fixed swing): $N=4$ gives
$-82.7$ dBc/Hz, $N=12$ gives $-78.0$ dBc/Hz, $\Delta\mathcal{L}=10\log_{10}3=+4.77$ dB; and
$\kappa_{min}$ grows by $\times\sqrt3\approx1.732$. (The absolute values inherit [P2]'s SSB
bookkeeping, the same family as the 4 in the denominator of [P1] Eq.(21); the time-domain $/2$
convention shifts everything by $+3$ dB. $\Delta\mathcal{L}$ is a difference, **identical under
both conventions**.)

**Python verification**:

```python
import numpy as np
def L_ring_diff(N, kT, P, f0, df, eta=1.0, vdd_vchar=3.0, vdd_swing=2.0):  # [P2] Eq.(34)
    return 10*np.log10(8/(3*eta) * N * (kT/P) * (vdd_vchar + vdd_swing) * (f0/df)**2)
L4  = L_ring_diff(4,  4.0e-21, 1e-3, 5e9, 1e6)
L12 = L_ring_diff(12, 4.0e-21, 1e-3, 5e9, 1e6)
print(round(L4,1), round(L12,1), round(L12-L4,2))   # -> -82.7 -78.0 4.77
```

**One-line design rule**: single-ended = $N$-free (Eq.23); differential = **fewest stages wins**
(Eq.34, $+3.01$ dB per doubling) — the lower bound on $N$ is set by phase margin /
quadrature / multiphase needs, so do not add more. Tail-source noise near $f_0$ "surprisingly"
does not enter the phase noise (p.796); what enters is its low-frequency noise (the symmetry path)
and its noise near even harmonics (filterable with an LC).

## Key figures

| Paper figure | Page | Content | Site counterpart | Note |
|---|---|---|---|---|
| Fig. 5 | 793 | Overlaid ISFs at the same frequency for different stage counts $N$ (3/5/15) | scaling intuition ($\Gamma_{rms}\propto N^{-3/2}$) | ✓ |
| Fig. 6 | 793 | Approximate waveform and ISF of one single-ended ring stage (energy concentrated at the transition) | toy triangular ISF (lab_03) | ✓ |
| Fig. 8 | 794 | rms ISF vs $N$ for rings of different stage counts; the solid line is Eq.(16) at $\eta=0.75$, $\Gamma_{rms}\approx4/N^{1.5}$ | scaling argument for `lc_vs_ring_isf_comparison.png` | ✓ |
| Fig. 9 | 795 | rms ISF vs $N$ for **differential** rings under three constraint scenarios (fixed power/fixed swing, fixed power/fixed $R_L$, fixed tail current/fixed $R_L$) | empirical support that Eq.(16)'s scaling carries over to differential rings (a premise of the Eq.(34) derivation) | ✓ |
| Fig. 12 / Tables I–III | 799–800 | The three ring stage circuits (inverter-chain / current-starved / differential) and 26 measured $\mathcal{L}(1\,\text{MHz})$ values compared with Eq.(6)/(23)/(34) | "Measured validation" section (table transcription + recomputation of oscillators 3 and 12) | ✓ |
| Fig. 16 | 802 | rms jitter vs $\Delta T$ (log–log) of differential ring 12: the $\sqrt{\Delta T}$ segment fits $\kappa=6.18\times10^{-9}\ \sqrt{\text{s}}$, turning to slope 1 after roughly $10^{-8}$–$10^{-7}$ s ($\zeta=2.5\times10^5$) | measured closed loop of Eq.(8)/(12)/(35)/(50) (Worked example 2) | ✓ |
| **Fig. 17** | 802 | phase noise vs the symmetry (control) voltage, with a **minimum** at the symmetric point | direct experimental support for the symmetry design rule | ✓ |

**Fig. 17 is the smoking gun for the symmetry rule**: sweep the control voltage; at the point where
the PMOS pull-up current = NMOS pull-down current and the waveform is symmetric, $c_0$ is squeezed
to its minimum, 1/f³ upconversion is suppressed, and the phase noise shows a **bowl bottom**. This
directly verifies [P1] Eq.(24) (claim C4).

This site compares LC ($-\sin$) and ring (triangular ISF, peaks shrinking with $N$) with a toy
model — **not transistor-level**:

![ISF comparison of LC vs ring (toy)](/figures/lc_vs_ring_isf_comparison.png)
![Ring accumulated jitter growing as √Δt over time (toy)](/figures/ring_oscillator_timing_noise_accumulation.png)

## Measured validation (Sec. VIII, pp.798–802)

The most underrated section of [P2]: it uses **26 fabricated rings** (three topologies, two processes — 2 µm 5 V and 0.25 µm 2.5 V — from 115 MHz to 5.5 GHz)
to compare Eq.(6)/(23)/(34) with the measured $\mathcal{L}(1\,\text{MHz})$ device by device, and Fig. 16 to compare Eq.(8)/(12)/(35) with measured jitter.
Measurement systems (p.798): HP 8563E, RDL NTS-1000A, HP E5500 (phase noise); Tektronix CSA 803A (jitter). The offset is fixed at 1 MHz to maximize the measurement dynamic range.
The three tables below were transcribed cell by cell from renders of the original PDF (pp.799–800); $W/L$ in µm/µm, phase noise in dBc/Hz at 1 MHz offset.

> **Honesty note**: the OCR in `extracted/raw_text/jitter_ring.txt` lost all three tables and every intermediate number of the oscillator-3 and oscillator-12 examples; the tables and the paper's printed intermediates in this section ($2.87\times10^{-22}$, $179.5$ fC, $50.3$ fC, $4.14\times10^{-23}$, $8.28\times10^{-24}$, $4.97\times10^{-23}$, $-113.0$, $-95.5$, $-95.4$) were read from the rendered pages and then **recomputed by this site** in the Python below — values that agree digit for digit are marked ✓; this is not a verbatim transcription.
>
> **Convention flag**: every "Pred.(6)" column and every recomputation here uses [P2] Eq.(6) as printed, $\mathcal{L}=\Gamma_{rms}^2/(8\pi^2\Delta f^2)\cdot(\overline{i_n^2}/\Delta f)/q_{max}^2$ — the denominator $8\pi^2\Delta f^2=2\Delta\omega^2$ is this site's $\mathcal{L}_{/2}$ family, 3 dB above the $4\Delta\omega^2$ of [P1] Eq.(21) (see the flag in the Eq.(27)–(30) section).

### Table I (p.799): inverter-chain rings (Fig. 12(a), no tuning)

| Index | $N$ | NMOS $W/L$ | PMOS $W/L$ | $V_{DD}$ (V) | $I_{sup}$ (mA) | $f_0$ | Pred. (23) | Pred. (6) | Meas. |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 5 | 3/2 | 5/2 | 5.0 | 0.3 | 232 MHz | −119.9 | −117.7 | −118.5 |
| 2 | 11 | 4/2 | 6/2 | 5.0 | 0.5 | 115 MHz | −127.2 | −126.4 | −126.0 |
| 3 | 19 | 10/0.25 | 20/0.25 | 2.5 | 10 | 1.33 GHz | −111.8 | −113.0 | −111.5 |

Oscillators 1 and 2 are in the 2 µm 5 V process (long-channel, Eq.(18) noise); oscillator 3 is in the 0.25 µm 2.5 V process (short-channel, Eq.(28) noise). Both predictions (the FOM form Eq.(23) and the term-by-term $N\times$Eq.(6)) land within ±2 dB of the measurement.

### Table II (p.799): current-starved inverter-chain rings (Fig. 12(b), all 0.25 µm 2.5 V)

The design intent is **fixed frequency and power, sweeping only $N$** (frequency set by channel length, power by width); Nbias is tied to $V_{DD}$ and Pbias to 0 V.

| Index | $N$ | inv N/P $W/L$ | tail N/P $W/L$ | $I_{sup}$ (mA) | $f_0$ (MHz) | Pred. (23) | Pred. (6) | Meas. |
|---|---|---|---|---|---|---|---|---|
| 4 | 3 | 35/0.53, 70/0.53 | 28/0.53, 56/0.53 | 2.34 | 751 | −113.8 | −116.6 | −114.0 |
| 5 | 5 | 21/0.39, 42/0.39 | 23/0.39, 46/0.39 | 2.51 | 850 | −111.7 | −111.9 | −112.6 |
| 6 | 7 | 14/0.36, 28/0.36 | 36.8/0.36, 73.5/0.36 | 2.49 | 931 | −110.5 | −110.4 | −111.7 |
| 7 | 9 | 12.6/0.32, 25.2/0.32 | 28/0.32, 56/0.32 | 2.73 | 932 | −110.4 | −113.5 | −112.5 |
| 8 | 11 | 10.5/0.32, 21/0.32 | 146/0.32, 291/0.32 | 2.65 | 869 | −110.9 | −110.1 | −112.2 |
| 9 | 15 | 9.1/0.28, 18.2/0.28 | 146/0.28, 291/0.28 | 2.8 | 929 | −110.0 | −110.7 | −112.3 |
| 10 | 17 | 7.4/0.25, 12.6/0.25 | 25.2/0.28, 50.4/0.28 | 3.8 | 898 | −111.2 | −109.4 | −112.0 |
| 11 | 19 | 6.3/0.25, 12.6/0.25 | 56/0.25, 112/0.25 | 3.9 | 959 | −110.6 | −110.1 | −110.9 |

**This table is the measured evidence for claim C7 (N-independence)**: as $N$ goes from 3 to 19 ($6.3\times$), the measured $\mathcal{L}$ stays between $-114.0$ and $-110.9$; normalizing every row to 900 MHz and 6.25 mW with the $f_0^2/P$ of Eq.(23) leaves a total spread of only **3.2 dB** (recomputed by this site, Python below) — if $\Gamma_{rms}^2\propto N^{-3}$ acted alone, $N=3\to19$ would differ by $10\log_{10}(19^3/3^3)=24.0$ dB. Oscillator 4 (3 stages) is slightly better, which the paper attributes to the lower frequency and longer channel (smaller $\gamma$). Oscillator 7 is the device used in the Fig. 17 symmetry-voltage experiment.

### Table III (p.800): differential rings (Fig. 12(c), all 0.25 µm 2.5 V, unsilicided poly $R_L$)

| Index | $N$ | $W/L$ | $R_L$ (Ω) | $I_{tail}$ (mA) | $P_{tot}$ (mW) | $f_{max}$ | Tuning | Pred. (34) | Pred. (6) | Meas. |
|---|---|---|---|---|---|---|---|---|---|---|
| 12 | 4 | 4.2/0.25 | 2k | 1 | 10 | 2.81 GHz | 34% | −95.4 | −95.5 | −95.2 |
| 13 | 4 | 8.4/0.25 | 1k | 2 | 20 | 4.47 GHz | 42% | −95.1 | −94.0 | −94.3 |
| 14 | 4 | 16.8/0.25 | 500 | 4 | 40 | 3.89 GHz | 44% | −98.5 | −97.2 | −97.4 |
| 15 | 4 | 33.6/0.25 | 250 | 8 | 80 | 5.43 GHz | 25% | −98.7 | −99.6 | −98.5 |
| 16 | 4 | 8.4/0.25 | 2k | 1 | 10 | 2.87 GHz | 37% | −95.2 | −96.6 | −93.8 |
| 17 | 4 | 16.8/0.25 | 1k | 2 | 20 | 3.39 GHz | 45% | −96.7 | −97.9 | −96.8 |
| 18 | 4 | 33.6/0.25 | 500 | 4 | 40 | 5.33 GHz | 32% | −95.8 | −97.2 | −95.3 |
| 19 | 4 | 16.8/0.25 | 2k | 1 | 10 | 1.75 GHz | 73% | −99.5 | −97.5 | −95.2 |
| 20 | 4 | 33.6/0.25 | 1k | 2 | 20 | 2.24 GHz | 58% | −100.3 | −100.3 | −99.0 |
| 21 | 4 | 33.6/0.25 | 2k | 1 | 10 | 1.27 GHz | 67% | −104.4 | −101.8 | −100.2 |
| 22 | 4 | 67.2/0.25 | 1k | 2 | 20 | 1.19 GHz | 76% | −105.8 | −102.6 | −100.2 |
| 23 | 4 | 33.6/0.25 | 2k | 1 | 10 | 1.53 GHz | N/A | −100.6 | −98.9 | −97.3 |
| 24 | 6 | 13.4/0.25 | 3k | 0.67 | 10 | 859 MHz | 58% | −103.9 | −106.0 | −104.3 |
| 25 | 8 | 6.7/0.25 | 4k | 0.5 | 10 | 731 MHz | 74% | −104.1 | −106.3 | −106.2 |
| 26 | 12 | 4.2/0.25 | 6k | 0.33 | 10 | 447 MHz | 52% | −106.6 | −110.4 | −109.5 |

Why poly resistors as loads (p.799): they make the node waveform closer to the step response of an RC network — more symmetric — which suppresses 1/f upconversion (the symmetry rule in practice).
Oscillators 12/24/25/26 share **$P=10$ mW and $R_LI_{tail}=2$ V** (fixed power / fixed swing, exactly the "+" scenario of Fig. 9): normalized to 2.81 GHz, the measurements are $-95.2/-94.0/-94.5/-93.5$ ($N=4/6/8/12$), while Eq.(34) predicts $+10\log_{10}(N/4)=0/1.8/3.0/4.8$ dB — **the direction agrees (more stages is worse for a differential ring)**, but the measured slope is gentler; this is the measured face of the explicit $N$ in Eq.(34).

### Worked example 1: oscillator 3 (single-ended, Eq.(28)→(6)→(23); recomputed by this site ✓)

The paper's procedure (p.799): the simulated mid-transition drain current $I_D=3.47$ mA, $E_c=4\times10^6$ V/m and $\gamma=2.5$ go into Eq.(28); $C_{total}=71.8$ fF; one noise source per node, so the total phase noise is $N$ times Eq.(6).

1. Eq.(28): $\overline{i_n^2}/\Delta f=8kT\gamma I_D/(E_cL)=2.87\times10^{-22}$ A²/Hz (paper ✓).
2. $q_{max}=C_{total}V_{DD}=71.8\text{ fF}\times2.5\text{ V}=179.5$ fC (paper ✓; full-swing node charge).
3. Eq.(16): $\Gamma_{rms}^2=2\pi^2/(3\eta^3N^3)$, $N=19$; the paper does not print the $\eta$ used for oscillator 3, so this site sweeps $\eta=0.75$ (the Fig. 8 solid-line value) and $0.9$ (the value used for oscillator 12).
4. $N\times$Eq.(6): $\mathcal{L}=N\Gamma_{rms}^2/(8\pi^2\Delta f^2)\cdot(\overline{i_n^2}/\Delta f)/q_{max}^2$; $\eta=0.75$ gives $-113.1$ dBc/Hz (paper $-113.0$, a 0.1 dB difference).
5. Eq.(23): $P=V_{DD}I_{sup}=25$ mW, $V_{char}=E_cL/\gamma=0.4$ V, $f_0=1.33$ GHz; $\eta=0.75$ gives $-111.9$ (paper $-111.8$). Measured: $-111.5$.

**Dimension check** (step 4): $\Gamma_{rms}^2$ is dimensionless; $1/(\text{Hz}^2)\times(\text{A}^2/\text{Hz})/\text{C}^2=\text{A}^2/(\text{Hz}^3\text{C}^2)=(\text{C}^2/\text{s}^2)\cdot\text{s}^3/\text{C}^2=\text{s}=1/\text{Hz}$ ✓ (the "/Hz" of dBc/Hz).

```python
import numpy as np
k, T = 1.380649e-23, 300.0; kT = k*T
# ---- oscillator #3 ([P2] Table I row 3, p.799): single-ended inverter chain, 0.25 um / 2.5 V
N, VDD, Isup, f0, df = 19, 2.5, 10e-3, 1.33e9, 1e6
Ec, Lch, gam, ID = 4e6, 0.25e-6, 2.5, 3.47e-3
Ctot = 71.8e-15
Si = 8*kT*gam*ID/(Ec*Lch)                       # Eq.(28)
qmax = Ctot*VDD                                 # full-swing node charge
print(f"{Si:.2e} {qmax*1e15:.1f}")             # -> 2.87e-22 179.5   A^2/Hz, fC (paper prints 2.87e-22, 179.5 fC)
def L6_times_N(N, Si, qmax, eta):               # N x Eq.(6), Gamma_rms from Eq.(16)
    G2 = 2*np.pi**2/(3*eta**3*N**3)
    return 10*np.log10(N*G2/(8*np.pi**2*df**2)*Si/qmax**2)
def L23(P, Vchar, eta):                         # Eq.(23), Vchar = Ec*L/gamma (Eq.30)
    return 10*np.log10(8/(3*eta)*kT/P*VDD/Vchar*(f0/df)**2)
Vchar = Ec*Lch/gam
for eta in (0.75, 0.9):
    print(eta, round(L6_times_N(N, Si, qmax, eta),1), round(L23(VDD*Isup, Vchar, eta),1))
# -> 0.75 -113.1 -111.9   (paper Table I: Pred.(6) -113.0, Pred.(23) -111.8, Meas. -111.5)
# -> 0.9 -115.5 -112.7
```

### Worked example 2: oscillator 12 (differential, Eq.(28)+(33)→(6), Eq.(34), jitter Eq.(12)/(35); recomputed by this site ✓)

The paper's procedure (pp.800–801): in the balanced state each node has $C_{total}=41.6$ fF and a simulated swing of $1.208$ V; each differential-pair NMOS carries $I_{tail}/2=0.5$ mA and its noise is given by Eq.(28); load resistor $4kT/R_L$; one source on each of the $2N$ nodes; $\eta=0.9$.

1. $q_{max}=41.6\text{ fF}\times1.208\text{ V}=50.3$ fC (paper ✓).
2. NMOS: $8kT\gamma I_D/(E_cL)=4.14\times10^{-23}$; $R_L=2$ kΩ: $4kT/R_L=8.28\times10^{-24}$; total $4.97\times10^{-23}$ A²/Hz (all three ✓). These are the two shares of Eq.(33): $4kTI_{tail}(1/V_{char}+1/(R_LI_{tail}))$ with $V_{char}=0.4$ V.
3. $2N\times$Eq.(6) ($N=4$, $\eta=0.9$): $-95.5$ dBc/Hz (paper ✓).
4. Eq.(34): $P=NV_{DD}I_{tail}=10$ mW, $V_{DD}/V_{char}=6.25$, $V_{DD}/(R_LI_{tail})=1.25$, $f_0=2.81$ GHz: $-95.4$ (paper ✓). Measured: $-95.2$.
5. **Jitter**: p.801 prints the Fig. 16 best fit $\kappa=6.18\times10^{-9}\ \sqrt{\text{s}}$, with Eq.(12) and Eq.(35) giving $5.95\times10^{-9}$ and $6.07\times10^{-9}\ \sqrt{\text{s}}$ respectively. This site's recomputation: Eq.(35) gives $6.07\times10^{-9}$ ✓; Eq.(12) (**as printed on p.793**, with $\omega_0$ in the denominator and the noise powers of the $2N$ sources added) gives $5.97\times10^{-9}$ (0.3% from the paper, within the rounding of the paper's intermediates; this site cannot tell which step it comes from); inverting the measured $-95.2$ dBc/Hz through Eq.(50) (p.803) $\kappa=(\Delta f/f_0)\sqrt{\mathcal{L}_{lin}}$ gives $6.18\times10^{-9}$ — **digit for digit** the Fig. 16 fit, the measured closed loop of "frequency-domain phase noise and time-domain jitter share one $\Gamma_{rms}^2/q_{max}^2$" (claim C6). **Dimension check**: $(\text{Hz}/\text{Hz})\cdot\sqrt{1/\text{Hz}}=\sqrt{\text{s}}$ ✓. Fig. 16 (p.802) turns to slope 1 between roughly $10^{-8}$ and $10^{-7}$ s ($\sigma\propto\Delta T$, fitted $\zeta=2.5\times10^5$ on the plot), which the paper attributes to device 1/f noise (end of Sec. VI).

> **Convention flag (the two outfits of κ)**: the printed [P2] Eq.(12), $\kappa=\dfrac{\Gamma_{rms}}{q_{max}\omega_0}\sqrt{\tfrac12\dfrac{\overline{i_n^2}}{\Delta f}}$, has $\omega_0$ in the denominator and units of $\sqrt{\text{s}}$ (time domain, matching the $\sigma_{\Delta t}$ of Eq.(8)); the $\kappa^2=\Gamma_{rms}^2S_i/(2q_{max}^2)$ of this site's [diffusion_dictionary](/03_isf_core_theory/diffusion_dictionary) is the phase version of Eq.(11) (rad²/s). They differ by $\omega_0$: $\kappa_t=\kappa_\phi/\omega_0$. Here $\omega_0=2\pi\times2.81$ GHz.

```python
import numpy as np
k, T = 1.380649e-23, 300.0; kT = k*T
# ---- oscillator #12 ([P2] Table III row 1, p.800): 4-stage differential, R_L = 2 kOhm, I_tail = 1 mA
N, VDD, Itail, RL, f0, df, eta = 4, 2.5, 1e-3, 2e3, 2.81e9, 1e6, 0.9
Ec, Lch, gam = 4e6, 0.25e-6, 2.5
Ctot, swing = 41.6e-15, 1.208
qmax = Ctot*swing
ID = Itail/2                                    # balanced: half the tail current
Si_N = 8*kT*gam*ID/(Ec*Lch)                     # Eq.(28), one differential-pair NMOS
Si_R = 4*kT/RL                                  # load resistor
Si = Si_N + Si_R
print(f"{qmax*1e15:.1f} {Si_N:.2e} {Si_R:.2e} {Si:.2e}")   # -> 50.3 4.14e-23 8.28e-24 4.97e-23   fC, A^2/Hz (paper prints 50.3, 4.14e-23, 8.28e-24, 4.97e-23)
G2 = 2*np.pi**2/(3*eta**3*N**3)                 # Eq.(16)
L6 = 10*np.log10(2*N*G2/(8*np.pi**2*df**2)*Si/qmax**2)     # 2N x Eq.(6)
P = N*VDD*Itail                                 # Eq.(31)
Vchar = Ec*Lch/gam                              # Eq.(30)
L34 = 10*np.log10(8/(3*eta)*N*kT/P*(VDD/Vchar + VDD/(RL*Itail))*(f0/df)**2)   # Eq.(34)
print(round(P*1e3,1), round(L6,1), round(L34,1))   # -> 10.0 -95.5 -95.4   mW, dBc/Hz (paper: -95.5, -95.4; Meas. -95.2)
# jitter: Eq.(12) as printed on p.793 carries omega_0 (kappa in sqrt(s)); 2N sources add in power
w0 = 2*np.pi*f0
k12 = np.sqrt(G2)/(qmax*w0)*np.sqrt(0.5*2*N*Si)
k35 = np.sqrt(8/(3*eta))*np.sqrt(N*kT/P*(VDD/Vchar + VDD/(RL*Itail)))          # Eq.(35)
k50 = df/f0*10**(-95.2/20)                       # Eq.(50) from the MEASURED -95.2 dBc/Hz
print(f"{k12:.2e} {k35:.2e} {k50:.2e}")          # -> 5.97e-09 6.07e-09 6.18e-09   sqrt(s) (paper p.801: 5.95e-9, 6.07e-9; Fig.16 measured fit 6.18e-9)
```

### This site's addition: Table II/III normalized against $N$ (recomputed by this site)

```python
import numpy as np
# [P2] Table II (current-starved single-ended, all 0.25 um / 2.5 V, p.799): N -> (I_sup mA, f0 MHz, measured L(1 MHz) dBc/Hz)
tab2 = {3:(2.34,751,-114.0), 5:(2.51,850,-112.6), 7:(2.49,931,-111.7), 9:(2.73,932,-112.5),
        11:(2.65,869,-112.2), 15:(2.8,929,-112.3), 17:(3.8,898,-112.0), 19:(3.9,959,-110.9)}
# normalise each row to f0 = 900 MHz, P = 2.5 V x 2.5 mA = 6.25 mW with L ~ f0^2/P (Eq.23)
norm = np.array([L - 20*np.log10(f/900) + 10*np.log10(2.5*I/6.25) for N,(I,f,L) in tab2.items()])
print(round(norm.min(),1), round(norm.max(),1), round(norm.max()-norm.min(),1))   # -> -112.7 -109.5 3.2   dBc/Hz (total spread after normalisation, N = 3..19, only 3.2 dB)
print(round(10*np.log10(19**3/3**3),1))   # -> 24.0  dB (what Gamma_rms^2 ~ N^-3 alone would predict for N = 3 -> 19)
# [P2] Table III rows 12/24/25/26 (p.800): P = 10 mW and R_L*I_tail = 2 V for all four -> Eq.(34) bracket fixed
tab3 = {4:(2810,-95.4,-95.2), 6:(859,-103.9,-104.3), 8:(731,-104.1,-106.2), 12:(447,-106.6,-109.5)}  # N: (f_max MHz, Pred.(34), Meas.)
for N,(f,Lp,Lm) in tab3.items():
    s = 20*np.log10(2810/f)
    print(N, round(Lp+s,1), round(Lm+s,1), round(10*np.log10(N/4),1))
# -> 4 -95.4 -95.2 0.0
# -> 6 -93.6 -94.0 1.8
# -> 8 -92.4 -94.5 3.0
# -> 12 -90.6 -93.5 4.8   (N, normalised Pred.(34), normalised Meas., Eq.(34)'s 10log(N/4); units dBc/Hz, dB)
```

**Applicability and failure conditions (when reading the three tables)**: (i) the predictions count white noise only (Eq.(6)/(23)/(34)); at 1 MHz offset these rings are already in the 1/f² region, hence the agreement; close-in (1/f³) belongs to Fig. 17 and symmetry. (ii) Eq.(23)/(34) assume symmetric waveforms and ignore supply/substrate and tail-source noise, so they are **lower bounds** (p.796); most measurements land within ±2 dB of the prediction, a few (the low-frequency Table III devices, oscillators 19–23) measure 4–6 dB above it. (iii) $\eta$, $I_D$, $C_{total}$ and the swing all come from circuit simulation and the paper does not print all of them (this site back-fits $\eta=0.75$ for oscillator 3). (iv) The $\sqrt{\Delta T}$ segment of the jitter only lasts to roughly $10^{-8}$–$10^{-7}$ s, after which 1/f takes over with slope 1; a SerDes integration that crosses that point needs the two-segment treatment (see [jitter_kernels](/02_foundations/jitter_kernels)).

## Design insights

- **Jitter and phase noise share one origin**: lowering $\Gamma_{rms}^2/q_{max}^2$ lowers both; do
  not treat long-term jitter and close-in phase noise as two separate problems.
- **Adding stages is not a phase-noise cure**: for single-ended rings at fixed $f_0$, $P$ the phase
  noise is nearly independent of $N$ (conclusion verified); **differential rings want even fewer
  stages** — Eq.(34) contains an explicit $N$, costing $+3.01$ dB per doubling at fixed $f_0$, $P$.
  The real reasons to add stages are quadrature/multi-phase outputs, tuning range, and phase margin.
- **Symmetry is the master knob for close-in noise**: tune the rise/fall to be symmetric (e.g. the
  control voltage of Fig. 17) to suppress $c_0$ and push the 1/f³ corner far out. Differential
  rings are usually more symmetric than single-ended ones.
- **The steeper the transition, the better**: the energy is concentrated at the transitions; the
  higher the slope, the larger $q_{max}$ and the relatively smaller $\Gamma_{rms}$.

Design-side summaries in [lc_vs_ring](/06_design_insights/lc_vs_ring) and [symmetry](/06_design_insights/symmetry);
the SerDes view is in [serdes_clocking_connection](/06_design_insights/serdes_clocking_connection).

## Limitations

Per paper_metadata (paper_002.limitations):

- Toy/first-order: short-channel effects and detailed device noise are approximate.
- **The N-independence conclusion** holds only for **single-ended** rings, at fixed power, fixed frequency, and for the specific noise model ([P2] Sec.V, Eq.(23)/(25), p.796, verified, claim C7); a differential ring instead contains an explicit $N$ (Eq.(34), p.796, verified).
- Substrate/supply noise is treated separately and qualitatively.

## Relationship to other papers

- **[P1]** is the foundation: this page's jitter $\kappa$, $\Gamma_{rms}$, and symmetry all use
  [P1]'s ISF and Eq.(21)/(24).
- **[P3]/[P4]** also use the ring as a vehicle ([P4]'s ILFD/prescaler is an inverter-chain ring),
  extending the ISF from phase noise to injection.
- **[P5]** is unrelated to this page; but latch-based/differential ring start-up also relies on
  cross-coupled positive feedback (the corner-case bridge of claim C12).

## Further reading / companion teaching pages

| Which block of this page | Companion teaching page | What that page adds |
|---|---|---|
| The LC ($-\sin$) vs ring (transition-concentrated) ISF comparison and the N-scaling argument | [lc_vs_ring](/06_design_insights/lc_vs_ring) | The $\Gamma_{rms}$, $q_{max}$, and phase-noise trade-offs of the two topologies organized into a design table |
| The random walk behind Eq.(8) accumulated jitter $\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$ | [lab_03_ring_oscillator_toy_model](/04_simulation_labs/lab_03_ring_oscillator_toy_model) | A runnable toy model: add an independent perturbation per edge; the log-log slope verifies $\sqrt{\Delta t}$ (**pedagogical toy, not transistor-level**) |
| The Fig. 17 phase-noise bowl at the symmetric point, $c_0$, and the 1/f³ corner | [symmetry](/06_design_insights/symmetry) | how rise/fall symmetry suppresses $c_0$, differential vs single-ended, design knobs |

> **How to read**: this page is the story of "how the paper applies [P1] to the ring"; to watch jitter grow as $\sqrt{\Delta t}$ hands-on, go back to lab_03; to turn the conclusions into topology selection, go back to lc_vs_ring and symmetry. For the SerDes view see also [serdes_clocking_connection](/06_design_insights/serdes_clocking_connection).

## What to remember

- **Accumulated jitter $\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$**: the random-walk fingerprint of a free-running oscillator ([P2] Eq.(8), p.792).
- $\kappa$ is set by **the same $\Gamma_{rms}^2/q_{max}^2$ as phase noise** ([P2] Eq.16/23, verified).
- **$\Gamma_{rms}\propto N^{-3/2}$** ([P2] Eq.(16), p.794, re-verified in v7: the radical covers only the
  constant, triple-confirmed by the prose's $4/N^{1.5}$@$\eta=0.75$ and App.B Eq.(55)); yet at fixed $f_0$, $P$ the phase noise is
  **nearly independent of $N$** (no $N$ in [P2] Eq.(23), claim C7, verified).
- **Differential rings are the opposite**: [P2] Eq.(34), p.796 contains an explicit $N$
  ($q_{max}\propto1/N^2$, verbatim on p.797); at fixed $f_0$, $P$ the phase noise degrades as
  $10\log_{10}N$ ($N=4\to12$ costs $+4.77$ dB); differential designs use the fewest necessary stages.
- **Fig. 17**: the phase-noise bowl bottom at the symmetric point — the smoking gun for the symmetry rule (claim C4).
- **Short-channel branch**: [P2] Eq.(27)–(30), p.796 replaces the $V_{char}$ of Eq.(23) by $E_cL/\gamma$ (oscillator 3: $0.4$ V), leaving N-independence intact; **Sec. VIII validates with 26 fabricated rings** — oscillator 3 recomputed via Eq.(28)→$N\times$Eq.(6) gives $-113.1$ (paper $-113.0$, measured $-111.5$), oscillator 12 via Eq.(34) gives $-95.4$ (measured $-95.2$), and inverting the measured phase noise gives $\kappa=6.18\times10^{-9}\ \sqrt{\text{s}}$, digit for digit the Fig. 16 fit.
- Rings integrate better than LC but usually have worse phase noise; this page shows where the knobs are.
