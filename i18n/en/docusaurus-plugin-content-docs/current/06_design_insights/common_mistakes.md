---
title: "Common Mistakes Showroom: 12 Real-World Landmines"
description: 12 real, verifiable common mistakes in phase-noise / jitter work — κ² mistaken for D, SSB /4 vs /2 mixed up, single-sideband PSD plugged into the wrong jitter kernel, ΔV/slope intuition inverting the ISF, corner confusion, 8/(3γ) misremembered, forgetting the ×2 in an integral, treating the 1/f² divergence as physical, DJ_pp plugged into the TJ formula, RBW smearing out close-in noise, ÷2 mistaken for halving the jitter in seconds, applying √N to flicker — each with a physical explanation, the correct version, and an on-site reference.
---

> **β**: This English translation is in beta — the Traditional-Chinese original is the authoritative version.

# Common Mistakes Showroom: 12 Real-World Landmines

> Prerequisites: [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) · [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter) | Next: [exercises](/06_design_insights/exercises) · [cheat_sheet](/00_overview/cheat_sheet)

This page does not teach new formulas. It lays out 12 mistakes that **actually happen**
in phase noise / jitter work and that cost you a factor of
**2, 3 dB, or $\sqrt2$** when they do — several of which this site itself made during
drafting and review, then fixed by simulation adjudication (we leave the correction
record honestly on each page). Every entry follows the same format:

**❌ Wrong claim/practice → 💥 Why it's wrong (physics) → ✅ Correct version → 📍 On-site reference**.

40 years of hard-won lesson: the most expensive mistakes in this line of work are not
failures to derive something, but **dropping a factor of 2 when swapping conventions**,
or **forcing LTI intuition onto an LTV system**. Look at the summary table first, then
work through each entry.

| # | Landmine | Error size | Antidote page |
|---|---|---|---|
| 1 | Treating $\kappa^2$ as Demir's convention $D$ | Linewidth $\times2$ | [diffusion_dictionary](/03_isf_core_theory/diffusion_dictionary) |
| 2 | Mixing SSB $/4$ with time-domain $/2$ ($-148$ vs $-145$) | 3 dB; back-solved $\kappa$ off by $\sqrt2$ | [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) |
| 3 | Single-sideband $S_\phi$ plugged into the coefficient-8 jitter kernel | Variance $\times2$, jitter $\times\sqrt2$ | [jitter_kernels](/02_foundations/jitter_kernels) |
| 4 | Using $\Delta V/$slope intuition to infer ISF direction | Sign flipped, false divergence at the peak | [lti_vs_ltv](/02_foundations/lti_vs_ltv) |
| 5 | Treating the device $1/f$ corner as the $1/f^3$ corner | Off by 3–300× in frequency in this example | [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion) |
| 6 | Ring FOM misremembered as $8/(3\gamma)$ | 1.76 dB (long channel) | [fom_limit](/06_design_insights/fom_limit) |
| 7 | Forgetting $\times2$ in the dBc/Hz integral, or shifting $f_1$ carelessly | $\sqrt2$; $\sqrt{10}$ per decade of $f_1$ | [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter) |
| 8 | Treating the $\Delta f\to0$ divergence as physical | Qualitatively wrong (reality is Lorentzian) | [lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth) |
| 9 | Feeding $\mathrm{DJ}_{pp}$ directly into the TJ formula | Pessimistic by 0.84 ps in this example | [dj_dual_dirac](/06_design_insights/dj_dual_dirac) |
| 10 | RBW too wide when measuring close-in | High by 2.5 dB in this example (and can be worse) | [measurement_and_spurs](/06_design_insights/measurement_and_spurs) |
| 11 | Assuming jitter (in seconds) also halves after ÷2 | The time value **does not change by a single fs** | [clock_chain_budget](/06_design_insights/clock_chain_budget) |
| 12 | Applying the white-noise $\sqrt N$ accumulation law to flicker | Underestimates by ~3× at $N=10$ | [jitter_kernels](/02_foundations/jitter_kernels) |

---

## 1. Treating κ² as D — linewidth comes out 2× too large

**❌ Wrong practice**: compute the phase-variance growth rate
$\kappa^2=\dfrac{\Gamma_{rms}^2}{2q_{max}^2}\dfrac{\overline{i_n^2}}{\Delta f}$ ([P2] Eq.(11)/(12), p.793),
call this number **directly** the diffusion constant $D$, then plug it into Demir's
linewidth formula $\Delta f_{3\mathrm{dB}}=D/\pi$. (This site's v3 spec made exactly
this mistake; v5 fixed it by Monte-Carlo adjudication.)

**💥 Why it's wrong**: the literature has two definitions of $D$ — the rate convention
$\mathrm{Var}[\Delta\phi]=D\vert t\vert$ (in which $D=\kappa^2$), and the
Demir/laser convention $\mathrm{Var}[\Delta\phi]=2D\vert t\vert$ (in which
$D=\kappa^2/2$). $\Delta f_{3\mathrm{dB}}=D/\pi$ is the formula for **the latter**;
plugging in the former's value overstates the linewidth by $2\times$.

**✅ Correct version**: first ask whether the other party's $\mathrm{Var}$ expression
has **that factor of 2** before converting conventions. The unambiguous way to write
it is entirely in terms of $\kappa^2$:

$$
\Delta f_{3\mathrm{dB}}=\frac{\kappa^2}{2\pi}\qquad[\text{Hz}]
$$

Canonical Example B ($\Gamma_{rms}=0.5$, $q_{max}=1$ pC, $S_i=10^{-24}$ A²/Hz):
$\kappa^2=0.125$ rad²/s → correct linewidth **19.9 mHz**; the wrong version gives 39.8 mHz.
A single lab_23 simulation extracting all four channels (variance slope 0.1252 rad²/s,
linewidth fit 20.0 mHz) sides with 19.9 mHz.
Dimension check: $\text{rad}^2/\text{s}\div2\pi=\text{Hz}$ ✓ (rad is dimensionless).

**📍 On-site reference**: [diffusion_dictionary](/03_isf_core_theory/diffusion_dictionary)
(item-by-item reconciliation of Suits 2/3 and the lab_23 adjudication),
[lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth).

## 2. Mixing up −148 and −145 — the 3 dB between SSB /4 and time-domain /2

**❌ Wrong practice**: for the same oscillator, one page states
$\mathcal{L}(1\,\text{MHz})=-148$ dBc/Hz, another states $-145$, and they cross-reference
each other without labeling the convention; or the $/4$-convention number from
[P1] Eq.(21) is plugged into the back-solving formula
$\kappa=2\pi\Delta f\sqrt{\mathcal{L}_{lin}}$, which expects the $/2$ convention.

**💥 Why it's wrong**: [P1] Eq.(21), p.185 uses SSB (single-sideband) bookkeeping, with
denominator $4\Delta\omega^2$ (its summation form, Eq.(19), corresponds to
$8q_{max}^2\Delta\omega^2$); the clean time-domain derivation for small-angle PM gives
$\mathcal{L}=\tfrac12S_\phi$, with denominator $2\Delta\omega^2$ — the two differ by
$10\log_{10}2\approx3$ dB, a well-known convention dispute in the literature, **not**
an arithmetic error by either side.

**✅ Correct version**: know both faces of Example B: $/4$ gives $-148.0$, $/2$ gives
$-145.0$ dBc/Hz. Any reported number **must be labeled with its convention**;
back-solving $\kappa$ ([P2] Eq.(50), p.803 route) expects the $/2$ convention —
substituting $-145$ gives $\kappa=0.354$ rad/$\sqrt{\text{s}}$ ✓, mistakenly
substituting $-148$ gives only $0.25$ (short by $\sqrt2$).
Scaling ($\Gamma_{rms}^2/q_{max}^2$, $-20$ dB/dec) is identical between the two conventions.

**📍 On-site reference**: [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)
(factor-of-2 teaching note), [diffusion_dictionary](/03_isf_core_theory/diffusion_dictionary) (Suit 4),
[jitter_kernels](/02_foundations/jitter_kernels) (Section 4.5's back-solving trap).

## 3. Single-sided/double-sided PSD plugged into the wrong jitter kernel — 8 vs 4's √2

**❌ Wrong practice**: take the single-sideband spectrum $S_\phi=2\times10^{\mathcal{L}/10}$
from a measured $\mathcal{L}$, then plug it into the literature's period-jitter formula
$\sigma^2_{\Delta\phi}=\dfrac{8}{\omega_0^2}\displaystyle\int_0^\infty S_\phi\sin^2(\pi f\tau)\,df$
([P2] Eq.(49), p.803, taken literally).

**💥 Why it's wrong**: the $R_\phi(\tau)=\int_{-\infty}^{\infty}S_\phi e^{j2\pi f\tau}df$
defined in [P2] Eq.(48) is a **double-sided** spectrum; the coefficient-8 formula
is matched to a double-sided spectrum. A single-sideband spectrum (the kind you get from
a datasheet or from $\mathcal{L}$) has already folded the double-sided power into 2×
the density, so pairing it with the coefficient-8 formula **double-counts a factor of 2**
— variance $\times2$, jitter $\times\sqrt2$.

**✅ Correct version**: pick one convention and stay with it end to end. With a
single-sideband $S_\phi$ and $\int_0^\infty$, the N-period kernel is

$$
\sigma_P^2(N)=\frac{1}{\omega_0^2}\int_0^\infty S_\phi(f)\,4\sin^2(\pi fNT)\,df
$$

($8S_\phi^{DS}\sin^2=4S_\phi^{OS}\sin^2$ — numerically identical). For the canonical
white-noise oscillator ($\kappa^2=0.125$ rad²/s, $f_0=5$ GHz): correct $\sigma_P=0.1592$ fs;
the wrong version gives 0.2251 fs. lab_24 computes it three different ways with three
different bookkeeping conventions and all three print 0.1592 fs.

**📍 On-site reference**: [jitter_kernels](/02_foundations/jitter_kernels) (Step 0
comparison table, [P2] Eq.(48)/(49) verified-verbatim note, lab_24 Monte-Carlo).

## 4. Using ΔV/slope intuition to infer ISF direction — LTI intuition crashes on an LTV system

**❌ Wrong practice**: apply the comparator intuition
$\Delta t=\Delta V/(\mathrm{d}V/\mathrm{d}t)$ and claim that "injecting positive charge
pushes the voltage up, so the phase always leads (or always lags)"; or extend this to
"the smaller the slope, the more sensitive, so a sinusoidal oscillator is most vulnerable
to noise at its **peak**." (An early version of this site's lti_vs_ltv page had the
direction backwards; it has since been corrected.)

**💥 Why it's wrong**: an oscillator is an LTV (linear time-variant) system. The sign of
$\Delta\phi$ is set by the **tangential projection** of the voltage jump onto the limit
cycle, which **flips sign** with injection phase; at the peak, $\Delta V$ is almost
entirely a radial (amplitude) component, which the amplitude restoring force absorbs —
the true sensitivity there is **0**, not the infinity that $1/$slope suggests.

**✅ Correct version**: for an ideal LC oscillator ($V=V_{max}\cos\theta$), the ISF is
$\Gamma(\theta)=-\sin\theta$ ([P1] Sec. III; $\Delta\phi=\Gamma\,\Delta q/q_{max}$).
Look up the direction directly: rising zero-crossing ($\theta=3\pi/2$) $\Gamma=+1$ →
phase **leads**; falling zero-crossing ($\theta=\pi/2$) $\Gamma=-1$ → phase **lags**;
peak/trough $\Gamma=0$ → pure amplitude change. Numerical feel (Example A): a 1 fC
injection with $q_{max}=1$ pC, $f_0=5$ GHz gives $\vert\Delta\phi\vert=10^{-3}$ rad
$=31.8$ fs at the zero-crossing, and 0 fs at the peak. The 1-D waveform-shift check
$\delta=\Delta V/(\mathrm{d}V/\mathrm{d}t)$ agrees with the ISF **only at the
zero-crossing**; it breaks down moving toward the peak — exactly where the amplitude
channel takes over.

**📍 On-site reference**: [lti_vs_ltv](/02_foundations/lti_vs_ltv) (direction table and
projection argument), [impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift),
[waveform_slope](/06_design_insights/waveform_slope) (where slope intuition **does**
apply: driven threshold-crossing circuits).

## 5. Treating a device's 1/f corner as its 1/f³ corner

**❌ Wrong claim**: "This transistor's flicker corner is at 1 MHz, so the phase noise's
$1/f^3$ region also extends out to 1 MHz offset."

**💥 Why it's wrong**: the efficiency of flicker upconversion is set by the DC term
$c_0$ of the ISF, while the white-noise floor is set by $\Gamma_{rms}$ — so the
intersection of the two regions (the $1/f^3$ corner) is **rescaled by waveform
symmetry**, not a copy of the device corner. [P1] specifically emphasizes that this
overturns the old myth that "the two corners are equal."

**✅ Correct version**: [P1] Eq.(24), p.185:

$$
\Delta\omega_{1/f^3}=\omega_{1/f}\cdot\frac{c_0^2}{2\Gamma_{rms}^2}\approx\omega_{1/f}\left(\frac{c_0}{c_1}\right)^2
$$

With a device corner at 1 MHz and $\Gamma_{rms}=0.5$: an asymmetric waveform
($c_0=0.4$) → corner at **320 kHz**; symmetrizing to $c_0=0.04$ → **3.2 kHz**. Same
device, corner differs by 100× — the $1/f^3$ corner is a **design variable**
(symmetry), not a process constant.
Dimension check: frequency × dimensionless ratio = frequency ✓.

**📍 On-site reference**: [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)
(Examples E/F are exactly these two numbers), [symmetry](/06_design_insights/symmetry).

## 6. Ring FOM prefactor misremembered as 8/(3γ) — γ counted twice

**❌ Wrong practice**: write [P2]'s white-noise phase-noise limit for a ring as
$\mathcal{L}=\dfrac{8}{3\gamma}\dfrac{kT}{P}\dfrac{V_{DD}}{V_{char}}\Big(\dfrac{f_0}{\Delta f}\Big)^2$
(putting the channel thermal-noise coefficient $\gamma$ in the denominator).

**💥 Why it's wrong**: the prefactor in [P2] Eq.(23), p.796 is $8/(3\eta)$, where
$\eta$ is the **stage-delay proportionality constant** ([P2] Eq.(14), $\approx1$,
waveform/delay bookkeeping) and has nothing to do with noise; $\gamma$ only enters
through $V_{char}=\Delta V/\gamma$. Writing $8/(3\gamma)$ counts $\gamma$ twice.

**✅ Correct version**:

$$
\mathcal{L}_{lin}=\frac{8}{3\eta}\cdot\frac{kT}{P}\cdot\frac{V_{DD}}{V_{char}}\cdot\left(\frac{f_0}{\Delta f}\right)^{2},\qquad V_{char}=\frac{\Delta V}{\gamma}
$$

For a long-channel device with $\gamma=2/3$, $\eta=1$, the misremembered formula
overstates the noise by $10\log_{10}\!\big(4/(8/3)\big)=1.76$ dB; more insidiously, when
$\gamma=1$ the two formulas coincide exactly, hiding the error. The $V_T=0$ ceiling
$F_{eff}\ge16\gamma/(3\eta)$ ([P2] Eq.(25)) is where the $\gamma$ that genuinely comes
from $V_{char}$ shows up. (This site's v3 spec corrected this coefficient against the
original [P2] PDF, p.796.)

**📍 On-site reference**: [fom_limit](/06_design_insights/fom_limit) (Step 2, with a
step-by-step derivation and the ceiling), [paper_002 deep dive](/05_paper_deep_dives/paper_002_jitter_phase_noise_ring).

## 7. Computing jitter from a dBc/Hz integral: forgetting ×2, or mislabeling the integration range

**❌ Wrong practice**: compute rms jitter directly as
$\sigma_\phi^2=\int10^{\mathcal{L}/10}df$ (forgetting the $\times2$ in
$S_\phi=2\times10^{\mathcal{L}/10}$); or report "jitter = xx fs" without stating the
integration band, so others using a different $f_1$ can't reconcile the numbers.

**💥 Why it's wrong**: $\mathcal{L}\approx\tfrac12S_\phi$ (small-angle PM: each sideband
only carries half the power), so missing the ×2 → half the variance, jitter low by
$\sqrt2$. And the integral of a $1/f^2$ spectrum is **dominated by the lower limit
$f_1$** ($\int_{f_1} df/f^2\propto1/f_1$) — every decade $f_1$ drops, jitter rises by
$\sqrt{10}$.

**✅ Correct version**: the four-step chain
$\mathcal{L}\xrightarrow{\times2,\ \text{de-dB}}S_\phi\xrightarrow{\int_{f_1}^{f_2}}\sigma_\phi^2\xrightarrow{\sqrt{\ }}\sigma_\phi\xrightarrow{\div\,2\pi f_0}\sigma_t$,
and **always attach $[f_1,f_2]$**. Canonical Example C (5 GHz, $-100$ dBc/Hz@1 MHz,
$1/f^2$, integrated 1–100 MHz): correct **447.9 fs**; forgetting $\times2$ → 316.7 fs;
moving $f_1$ to 100 kHz → 1422.8 fs ($\times\sqrt{10}$).
Dimension check: $\text{rad}\div(\text{rad/s})=\text{s}$ ✓.

**📍 On-site reference**: [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter)
(Example C step-by-step), [lab_08](/04_simulation_labs/lab_08_jitter_integration).

## 8. Treating L's divergence at Δf→0 as physical — "infinite power near the carrier" does not exist

**❌ Wrong claim**: "Eq.(21) is $1/\Delta\omega^2$, so phase noise grows without bound
as offset shrinks — power is infinite at $\Delta f\to0$"; or seeing an instrument fail
to show the $-20$ dB/dec slope at very small offsets and suspecting the measurement is
broken.

**💥 Why it's wrong**: $1/\Delta\omega^2$ comes from **linearization** (small-angle
approximation), and $\Delta f\to0$ corresponds to long time intervals, where the random
phase walk has already gone far beyond $\gg1$ rad — exactly where the approximation
breaks down. The real carrier spectrum is **Lorentzian**: it flattens near the carrier,
has a finite peak, and conserves total power (equal to the carrier power).

**✅ Correct version**: $1/f^2$ is just the far asymptote of a Lorentzian at
$\Delta f\gg\Delta f_{3\mathrm{dB}}$; the knee is at
$\Delta f_{3\mathrm{dB}}=\kappa^2/2\pi$. Canonical Example B: 19.9 mHz (almost
unmeasurable, so in practice the $1/f^2$ region "looks like" it goes all the way down);
a datasheet-grade $-100$ dBc/Hz@1 MHz oscillator has a knee at 628 Hz — genuinely
visible when measuring at low offset. Divergence is not physics; it's a signal that the
approximation has failed.

**📍 On-site reference**: [lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth)
(full mechanism and power conservation), [beyond_lorentzian](/03_isf_core_theory/beyond_lorentzian),
[diffusion_dictionary](/03_isf_core_theory/diffusion_dictionary) (Suit 3).

## 9. Plugging DJ_pp directly into the TJ formula — you should use DJ_δδ

**❌ Wrong practice**: measure (or compute) the actual peak-to-peak value of
deterministic jitter, $\mathrm{DJ}_{pp}$, and substitute it directly into the industry
extrapolation formula $\mathrm{TJ}(\mathrm{BER})=\mathrm{DJ}+2Q^{-1}(\mathrm{BER})\,\sigma$.

**💥 Why it's wrong**: the dual-Dirac model's $\mathrm{DJ}_{\delta\delta}$ is a **model
parameter fitted from the Q-scale tail**, and mathematically it must satisfy
$\mathrm{DJ}_{\delta\delta}\le\mathrm{DJ}_{pp}$ (near its extremes the DJ distribution
has only finite probability mass, so the deep tail is a "discounted Gaussian"); this
"intentional underreporting" is precisely the mechanism that makes the BER extrapolation
fit the true tail.

**✅ Correct version**: $\mathrm{TJ}(\mathrm{BER})=\mathrm{DJ}_{\delta\delta}+2Q^{-1}(\mathrm{BER})\sigma$,
where $2Q^{-1}=14.07$ at BER $=10^{-12}$. lab_31 (sinusoidal DJ, $A=2$ ps, RJ
$\sigma=1$ ps): $\mathrm{DJ}_{pp}=4.0$ ps but the fitted $\mathrm{DJ}_{\delta\delta}=3.16$ ps;
forcing in $\mathrm{DJ}_{pp}$ gives TJ $=18.07$ ps, **0.84 ps more pessimistic** than the
exact bathtub value of 17.23 ps — throwing away margin for nothing. The reverse
direction is also wrong: $\mathrm{DJ}_{\delta\delta}$ is not a physical peak-to-peak
value, so don't use it to plot waveform extrema. Always state the fit window when
reporting (lab_31: the deeper the fit window, the closer $\mathrm{DJ}_{\delta\delta}$
gets to, but never exceeds, $\mathrm{DJ}_{pp}$: 3.07/3.16/3.27 ps).

**📍 On-site reference**: [dj_dual_dirac](/06_design_insights/dj_dual_dirac) (Steps 6/7:
derivation plus the proof that "underreporting is intentional"),
[serdes_clocking_connection](/06_design_insights/serdes_clocking_connection).

## 10. RBW set too wide when measuring close-in — smearing out the −30 dB/dec skirt

**❌ Wrong practice**: when measuring near-carrier phase noise with a spectrum analyzer
direct method, use a filter with RBW (resolution bandwidth) $=1$ kHz at 1 kHz offset to
read dBc/Hz quickly; or normalize per-Hz using the nominal RBW instead of the ENBW.

**💥 Why it's wrong**: a dBc/Hz reading is "the average density inside the RBW filter
window." In the $1/f^3$ region, the density varies by tens of dB within one window, and
the average is dominated by the side closer to the carrier — the reading is biased
high, and the steep skirt gets smeared out; when the RBW is large enough that the
window edge touches the carrier, carrier power leaks straight in and you read the
filter shape, not the DUT.

**✅ Correct version**: for close-in measurements, keep RBW $\ll\Delta f$ (conservatively
below $\Delta f/10$). An honest numerical feel (averaging the $1/f^3$ density across the
window and comparing to the true value at $\Delta f=1$ kHz): RBW $=1$ kHz reads
**2.5 dB** high, RBW $=100$ Hz only 0.02 dB (see the code at the end of this page; this
doesn't even account for carrier leakage — real conditions are only worse). Normalize
per-Hz using **ENBW** (equivalent noise bandwidth), not the nominal RBW, and remember
the log-detector's $+2.5$ dB correction (a **different mechanism** from the 2.5 dB
window-averaging bias above — the matching numeric value is pure coincidence) — this is
standard spectrum-analyzer measurement knowledge (external literature, not among the
five source PDFs; see the measurement page's Method A, which cites Keysight/Agilent
AN-1303). The true near-carrier flattening is the Lorentzian (Mistake 8) — you must
rule out the RBW artifact before claiming to have seen it.

**📍 On-site reference**: [measurement_and_spurs](/06_design_insights/measurement_and_spurs)
(Method A's ENBW normalization, the "re-weight by changing RBW" spur-identification test).

## 11. Assuming jitter (in seconds) also halves after ÷2 — confusing phase in dB with absolute time

**❌ Wrong claim**: "A ÷2 frequency divider improves phase noise by 6 dB, so rms jitter
(in fs) also halves (or shrinks by $\sqrt2$)."

**💥 Why it's wrong**: an ideal divider is edge-picking — it **copies** the input edge's
time position verbatim, without moving it by a single fs. What changes is the
"exchange rate": the same time-domain error, spread over a period that is now $N$
times longer, converts to a smaller **phase angle** (rad), which is why
$\mathcal{L}$ drops by $20\log_{10}N$.

**✅ Correct version**: work it through honestly. $\phi_{out}=\phi_{in}/N$ (the phase
definition of division), so $\sigma_{\phi,out}=\sigma_{\phi,in}/N$ (the rad value truly
shrinks); but $f_{0,out}=f_{0,in}/N$, and substituting into spec formula 17:

$$
\sigma_{t,out}=\frac{\sigma_{\phi,out}}{2\pi f_{0,out}}=\frac{\sigma_{\phi,in}/N}{2\pi f_{0,in}/N}=\frac{\sigma_{\phi,in}}{2\pi f_{0,in}}=\sigma_{t,in}
$$

The two $N$'s cancel — **jitter measured in seconds is an invariant under ideal
×N/÷N**. A worked chain (5 GHz divided by 2 to 2.5 GHz, same integration band):
22.5 fs → 22.5 fs, while $\sigma_\phi$ does halve (0.706 → 0.353 mrad). What ÷2 saves
is "fraction of the UI" (the UI got longer), not the time value; an ADC aperture or an
absolute timing budget cares about seconds, and gains nothing at all.
Dimension check: $\text{rad}\div(\text{rad/s})=\text{s}$, independent of $N$ ✓.

**📍 On-site reference**: [clock_chain_budget](/06_design_insights/clock_chain_budget)
(Rule 2 and Step 5's "conserved quantity"), [adc_aperture_jitter](/06_design_insights/adc_aperture_jitter).

## 12. Applying the white-noise √N accumulation law to flicker noise

**❌ Wrong practice**: measure the period jitter $\sigma_P(1)$, then extrapolate the
accumulated jitter after $N$ periods using $\sigma(N)=\sigma_P(1)\sqrt N$ — regardless
of what the spectrum actually looks like.

**💥 Why it's wrong**: the $\sqrt N$ law is a property of white-FM random walks
(independent increments, [P2] Eq.(8)). When flicker ($1/f^3$) dominates, adjacent
increments are **strongly correlated**, and the growth law is approximately
$\propto N$ ([P2] Eq.(9) and the slope-1 region of Fig. 4) — extrapolating with
$\sqrt N$ **systematically underestimates** jitter over long intervals.

**✅ Correct version**: first check which mechanism dominates near
$f\sim1/(2NT)$. White-noise region: $\sigma_{\Delta\phi}=\kappa\sqrt{NT}$; flicker region:
$\sigma^2_{\Delta\phi}=4\pi^2b_3(NT)^2\big[\tfrac32-\gamma_E-\ln(2\pi NTf_l)\big]$
($\gamma_E=0.5772$ is the Euler–Mascheroni constant; nearly $\propto N$, and with a
logarithmic dependence on the low-frequency cutoff $f_l$ — always attach $f_l$ when
reporting a number). Numerical picture (lab_24, $T=200$ ps, $f_l=100$ Hz):
$\sigma(N{=}10)/\sigma(N{=}1)$ is $\sqrt{10}=3.16$ for white noise vs $9.29$ for
flicker — nearly 3× apart. Quick sanity check: only the white-noise region satisfies
$\sigma_{c2c}=\sqrt2\,\sigma_P$; if that relation doesn't hold, don't use $\sqrt N$.

**📍 On-site reference**: [jitter_kernels](/02_foundations/jitter_kernels) (Step 5's
closed-form flicker expression and the log-band caveat), [lab_03](/04_simulation_labs/lab_03_ring_oscillator_toy_model),
[allan_variance](/02_foundations/allan_variance) (the ADEV version of the same story:
white FM $\tau^{-1/2}$ vs flicker FM $\tau^0$).

---

## Common root cause: three factor-of-2 families + one LTI habit

Of the 12 landmines, 7 (1, 2, 3, 7, 9's $2Q^{-1}$, 11, 12) are fundamentally
**bookkeeping-convention** issues, grouped into three families (see
[diffusion_dictionary](/03_isf_core_theory/diffusion_dictionary) for details):

1. **Single-sided vs double-sided PSD**: the $\delta$-strength $S_i/2$, the single-sideband
   $2\kappa^2$, the 8 vs 4 in the jitter kernel.
2. **$\mathrm{Var}=D\vert t\vert$ vs $2D\vert t\vert$**: $\kappa^2=D_{\text{A}}=2D_{\text{B}}$.
3. **SSB $/2$ vs $/4$**: the 3 dB between $-145$ and $-148$.

The other 4 (4, 5, 8, and part of 10) are cases of **applying LTI/linearization
intuition where it no longer holds**: slope intuition colliding with amplitude
restoration, device-corner intuition colliding with $c_0$ upconversion, the $1/f^2$
line colliding with the large-angle regime of a random walk, narrowband-density
intuition colliding with wide-RBW averaging. There is only one defense: **ask, for
every number, "which convention is this? does the approximation still hold here?"**
— then reconcile it with a one-line Python check.

## One-shot reconciliation: verification code for every number on this page

Below, every number from the 12 landmines that can be verified in one line is
recomputed (run with `PYTHONPATH=. python3 <this-file>` from the project root; the DJ
numbers in Mistake 9 are produced by `simulations/lab_31_dual_dirac.py`, see
[dj_dual_dirac](/06_design_insights/dj_dual_dirac)):

```python
import numpy as np
from simulations.common.noise_utils import leeson_one_over_f2, integrate_rms_jitter

# --- Mistake 1: κ² mistaken for D (linewidth 2×) ---
GRMS, QMAX, SI = 0.5, 1e-12, 1e-24
k2 = GRMS**2 * SI / (2 * QMAX**2)                 # [P2] Eq.(11)/(12)
print(round(k2, 3))                               # -> 0.125 (κ², rad²/s)
print(round(k2 / (2*np.pi) * 1e3, 1))             # -> 19.9 (correct FWHM, mHz)
print(round(k2 / np.pi * 1e3, 1))                 # -> 39.8 (κ² plugged into D/π, the 2x wrong value)

# --- Mistake 2: SSB /4 vs time-domain /2 (3 dB) ---
dw = 2 * np.pi * 1e6
print(round(10*np.log10(GRMS**2/QMAX**2 * SI/(4*dw**2)), 1))  # -> -148.0 ([P1] Eq.(21) /4)
print(round(10*np.log10(GRMS**2/QMAX**2 * SI/(2*dw**2)), 1))  # -> -145.0 (time-domain /2)

# --- Mistake 3: single-sideband spectrum plugged into coefficient-8 kernel (x√2) ---
f0, T = 5e9, 2e-10
sigP = np.sqrt(k2 * T) / (2*np.pi*f0)
print(round(sigP*1e15, 4))                        # -> 0.1592 (correct period jitter, fs)
print(round(sigP*np.sqrt(2)*1e15, 4))             # -> 0.2251 (x√2 wrong value, fs)

# --- Mistake 5: 1/f³ corner != device corner (Eq.24, device corner=1 MHz) ---
print(round(1e6 * 0.4**2 / (2*GRMS**2) / 1e3, 1))   # -> 320.0 (c0=0.4, kHz)
print(round(1e6 * 0.04**2 / (2*GRMS**2) / 1e3, 1))  # -> 3.2 (c0=0.04, kHz)

# --- Mistake 6: 8/(3γ) vs 8/(3η) (γ=2/3, η=1) ---
print(round(10*np.log10((8/(3*(2/3))) / (8/3)), 2))  # -> 1.76 (dB, excess from misremembering)

# --- Mistake 7: forgetting integral x2, or shifting f1 carelessly ---
f = np.logspace(3, 9, 400001)
L = leeson_one_over_f2(f, L_ref_dbc=-100.0, f_ref=1e6)
st, _ = integrate_rms_jitter(f, L, f0=5e9, fmin=1e6, fmax=1e8)
print(round(st*1e15, 1))                          # -> 447.9 (correct, fs; Example C)
print(round(st/np.sqrt(2)*1e15, 1))               # -> 316.7 (forgot x2, fs)
st2, _ = integrate_rms_jitter(f, L, f0=5e9, fmin=1e5, fmax=1e8)
print(round(st2*1e15, 1))                         # -> 1422.8 (f1 moved to 100 kHz, fs)

# --- Mistake 10: RBW bias on the 1/f³ skirt reading at offset=1 kHz ---
d = 1e3
bias = lambda rbw: 10*np.log10(d**3/(2*rbw)*(1/(d-rbw/2)**2 - 1/(d+rbw/2)**2))
print(round(bias(1e3), 2))                        # -> 2.5 (RBW=1 kHz, dB high)
print(round(bias(1e2), 2))                        # -> 0.02 (RBW=100 Hz, dB)

# --- Mistake 11: dB improves by 6 dB after ÷2, time value unchanged ---
f = np.logspace(4, 8, 20001)
L5G = np.where(f <= 1e6, -126.02, -148.0 - 20*np.log10(f/1e6))
st5, sp5 = integrate_rms_jitter(f, L5G, f0=5e9, fmin=1e4, fmax=1e8)
st25, sp25 = integrate_rms_jitter(f, L5G - 6.02, f0=2.5e9, fmin=1e4, fmax=1e8)
print(round(st5*1e15, 1), round(st25*1e15, 1))    # -> 22.5 22.5 (fs, before/after division)
print(round(sp5/sp25, 2))                         # -> 2.0 (phase in rad does halve)

# --- Mistake 12: flicker's N growth law ≈ N (not √N) ---
gEM, fl = 0.5772156649, 100.0
br = lambda N: 1.5 - gEM - np.log(2*np.pi*N*T*fl)
print(round(10*np.sqrt(br(10)/br(1)), 2))         # -> 9.29 (white noise should be √10=3.16)
```

(In Mistake 10, `bias` is the closed form for "the average of the $1/f^3$ density
across the RBW window, divided by the true value at the window center":
$\overline{S}=\frac{1}{\mathrm{RBW}}\int b/f^3\,df=\frac{b}{2\,\mathrm{RBW}}\big(f_{lo}^{-2}-f_{hi}^{-2}\big)$,
a teaching toy calculation that does not include carrier leakage or detector effects.)

## Key takeaways

- Reconcile before switching conventions: **single-sided vs double-sided**,
  **$\mathrm{Var}=D\vert t\vert$ vs $2D\vert t\vert$**, **SSB $/2$ vs $/4$** — these
  three factor-of-2 families account for most of the landmines.
- The ISF's direction and magnitude come from the **tangential projection on the limit
  cycle**, not $\Delta V/$slope; the peak belongs to the amplitude channel ($\Gamma=0$).
- The two corners are different things: the $1/f^3$ corner
  $=\omega_{1/f}\,c_0^2/(2\Gamma_{rms}^2)$ can be pushed far below the device corner by
  symmetry (300× lower in this example at $c_0=0.04$: 1 MHz → 3.2 kHz).
- The ring FOM prefactor is $8/(3\eta)$; $\gamma$ only lives inside $V_{char}=\Delta V/\gamma$.
- Jitter integration: $\times2$, label the band ($f_1$ dominates), $\div\,2\pi f_0$;
  under ideal ×N/÷N, **the time value is unchanged** — only the dB exchange rate changes.
- The $\Delta f\to0$ divergence is a linearization artifact — the real spectrum is
  Lorentzian, and total power is conserved.
- TJ extrapolation uses $\mathrm{DJ}_{\delta\delta}$ (a model parameter, intentionally
  underreported), not $\mathrm{DJ}_{pp}$.
- Close-in measurement: RBW $\ll\Delta f$, normalize with ENBW, rule out instrument
  artifacts before discussing physics.
- When flicker dominates, the accumulation law is $\approx N$ (not $\sqrt N$), with a
  logarithmic dependence on $f_l$ — always state the condition when reporting a number.

## Further reading

- Site-wide factor-of-2 reconciliation table: [diffusion_dictionary](/03_isf_core_theory/diffusion_dictionary)
- Full derivation of $/4$ vs $/2$: [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)
- Jitter kernel and [P2] Eq.(49) verified verbatim: [jitter_kernels](/02_foundations/jitter_kernels)
- The $\mathcal{L}\to\sigma_t$ four-step chain and Example C: [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter)
- The truth near the carrier: [lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth)
- The four rules of clock-chain bookkeeping: [clock_chain_budget](/06_design_insights/clock_chain_budget)
- Measurement methods and spur identification: [measurement_and_spurs](/06_design_insights/measurement_and_spurs)
- Exercises to turn concepts into intuition: [exercises](/06_design_insights/exercises)
