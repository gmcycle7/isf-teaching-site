---
title: Unified Notation Table
description: Site-wide consistent symbols, units, and the symbol correspondence across the papers.
---

# Unified Notation Table

> **β**: This English translation is in beta — the Traditional-Chinese original is the authoritative version.

Different papers write the same thing with different symbols. This page **unifies** them; every later chapter follows this table.
If you encounter a different convention in one of the papers, come back here to cross-reference.

> **How to use this page**: skim it once to get acquainted; when actually reading the derivations, come back and look up any symbol you do not recognize.
> Every quantity is labeled with its **unit** — doing a dimension check is the fastest way to catch mistakes.

## Main symbols

| Symbol | Meaning (intuition) | Unit | Used in | Notes |
|---|---|---|---|---|
| $t$ | time | s | all | — |
| $\tau$ | injection instant of the noise/impulse | s | [P1] | the ISF's argument is the injection phase $\omega_0\tau$; **collision note**: this page also has $\tau_0$ (amplitude memory time / jitter averaging window, three meanings — see the disambiguation below) and the Allan $\sigma_y(\tau)$ (averaging time) — similar letters, different physics |
| $T$ | oscillation period $T=1/f_0$ | s | all | — |
| $\omega_0$ | oscillation angular frequency $=2\pi f_0$ | rad/s | all | — |
| $f_0$ | oscillation (carrier) frequency | Hz | all | e.g. 5 GHz |
| $\phi(t)$ | excess phase (the deviation beyond the ideal phase) | rad | [P1][P2] | phase noise / jitter lives here |
| $\Delta\phi$ | phase step / phase error | rad | all | the jump caused by one impulse |
| $A(t)$ | instantaneous amplitude | V or normalized | [P1][P4] | perturbations get pulled back (see [P4] APF) |
| $\Gamma(\omega_0\tau)$ | **ISF**, the oscillator's "phase sensitivity" to noise; dimensionless, $2\pi$-periodic | — | [P1] | not the noise itself, but a weighting function; **collision note**: capital $\Gamma$ (ISF) looks like — but is unrelated to — lowercase $\gamma$ (MOSFET thermal-noise coefficient; see the new row below) |
| $\tilde\Lambda(\phi)$ | **amplitude ISF** (charge-normalized): the **initial** fractional amplitude change $D(0,\phi)$ caused by a unit impulse of charge injected at phase $\phi$ | 1/C | [P4] | [P4] Eq.(18),(24); the tilde denotes charge normalization (as in $\tilde\Gamma=\Gamma/q_{max}$); ideal LC $\tilde\Lambda=\cos\phi/q_{max}$; the $\Lambda\equiv q_{max}\tilde\Lambda$ of [P4] footnote 6 is the dimensionless version of its ref. [28], not used on this site |
| $\Delta(\phi)$ | **APF** (amplitude perturbation function) $=\int_0^\infty D\,d\tau=\tilde\Lambda\int_0^\infty d\,d\tau$; ideal LC $=\tau_0\tilde\Lambda$ | 1/A | [P4] | [P4] Eq.(19),(25); the APF itself carries **no tilde**; fundamental $\Delta_1=\frac{\tau_0}{q_{max}}\angle0°$ (Eq.(26)); a function $\Delta(\cdot)$ with an argument — not to be confused with the difference prefix in $\Delta q$, $\Delta\omega$ |
| $q_{max}$ | maximum node charge swing $=C\cdot V_{max}$ | C | [P1] | used for normalization; the larger it is, the lower the phase noise |
| $\Delta q$ | injected charge $=\int i\,dt$ | C | [P1] | e.g. 1 fC |
| $i_n(t)$ | noise current | A | [P1][P2] | the noise source injected into the node |
| $\overline{i_n^2}/\Delta f$ | current-noise power spectral density (single-sided) | A²/Hz | [P1] | white: independent of frequency |
| $S_i(f)$ | current-noise PSD | A²/Hz | all | another way of writing the same thing |
| $S_\phi(f)$ | phase PSD (single-sided) | rad²/Hz | all | integrating over $f$ gives $\sigma_\phi^2$ |
| $\mathcal{L}(\Delta f)$ | SSB phase noise (single-sideband phase noise) | dBc/Hz | all | $\approx\frac12 S_\phi$; the papers themselves usually write $\mathcal{L}\{\Delta\omega\}$ or $\mathcal{L}\{\Delta f\}$ (curly braces — see spec Sec. 3, Eq.(19)–(23)), while this site's pages mostly use $\mathcal{L}(\Delta f)$ (parentheses) — **the same SSB quantity**; $\Delta\omega=2\pi\Delta f$ is just the argument conversion, so no site-wide symbol replacement is done |
| $\Delta f,\ \Delta\omega$ | offset frequency (how far from the carrier) | Hz, rad/s | phase-noise pages | $\Delta\omega=2\pi\Delta f$; **this is the phase-noise/PSD-context definition**. The injection-locking cluster (injection_locking_noise, lab_36, paper_004_large_injection_transient, subharmonic_injection, interactive_calculator) instead uses $\Delta\omega$ for **detuning** — see the "$\Delta\omega$ (injection)" row below and the disambiguation section |
| $\Delta\omega$ (injection, detuning) | frequency difference between the oscillator and the injected signal | rad/s | [P3][P4] and the injection-locking pages | This site's convention is $\Delta\omega\equiv\omega_0-\omega_{inj}$ (used consistently by injection_locking_noise and lab_36); [P3]/[P4] themselves are not internally consistent on the sign ([P3] before Eq.(9) uses $\omega_{inj}-\omega_0$; [P4] p.2130 uses $\omega_{inj}/N-\omega_0$; subharmonic_injection separately writes $\Delta\omega_0$) — **every site result depends only on $\Delta\omega^2$ or writes the branch explicitly**, so the sign difference never affects the physics; lock condition $\lvert\Delta\omega\rvert\le\omega_L$ |
| $c_0$ | DC Fourier coefficient of the ISF (DC value $=c_0/2$) | — | [P1] | the key to 1/f upconversion |
| $c_n,\ \theta_n$ | amplitude / phase of the ISF's $n$-th harmonic | — | [P1] | moves noise near $n\omega_0$ onto the carrier |
| $\Gamma_{rms}$ | rms value of the ISF | — | [P1][P2] | sets the magnitude of the 1/f² phase noise |
| $\Gamma_{eff}$ | effective ISF (including cyclostationarity) | — | [P1] | $\Gamma_{eff}=\Gamma\cdot\alpha$ |
| $\alpha(\omega_0 t)$ | noise-modulating function (NMF): when the device is "leaking noise" | — | [P1] | $0\le\alpha\le1$, periodic; **overload warning**: fourier_series_of_isf.md's toy model `gamma_asymmetric` separately uses a scalar $\alpha$ for the ISF's DC offset ($\Gamma=\cos\theta+\alpha$, $c_0=2\alpha$), and the Allan-variance page also writes $\alpha$ for the power-law noise exponent ($S_y(f)=h_\alpha f^\alpha$, $-2\le\alpha\le2$) — **the NMF function, the toy DC-offset scalar, and the Allan power-law exponent share a letter but are otherwise unrelated**; see the disambiguation below |
| $\sigma_t$ | rms timing jitter | s | [P2] | what SerDes cares about most |
| $\sigma_\phi$ | rms phase | rad | all | $\sigma_t=\sigma_\phi/(2\pi f_0)$ |
| $\kappa$ | proportionality constant of ring accumulated jitter | $\sqrt{\mathrm{s}}$ | [P2] | $\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$ |
| $\omega_{1/f}$ | the device's 1/f-noise corner | rad/s | [P1] | note: ≠ the phase-noise 1/f³ corner |
| $N$ | number of ring-oscillator stages | — | [P2] | $\Gamma_{rms}\propto N^{-3/2}$; **overload warning**: the injection-division / subharmonic cluster ([P4] $M{:}N$, subharmonic_injection, injection_locked_division) separately uses $N$ for a **frequency ratio** ($\div N$ or $\times N$, $\omega_{inj}\approx N\omega_0$), and jitter_kernels.md's $\tau_0=NT$ uses $N$ for a **number of periods** — three different contexts, see the disambiguation below |
| $Q$ | tank quality factor | — | [P1] | appears in the Leeson comparison |
| $\eta$ | proportionality constant in the ring frequency / FOM | — | [P2] | $f_0=1/(2N\tau_D)$ |
| $\tilde\Gamma=\Gamma/q_{max}$ | dimensioned ISF (charge-normalized) | rad/C | [P3] | $\tilde\Gamma(x)\equiv\Gamma(x)/q_{max}$ ([P3] Eq.(26)); tilde = charge normalization, same convention as $\tilde\Lambda=\Lambda/q_{max}$ (see the amplitude-ISF row above); this site's core material keeps the dimensionless $\Gamma$, while the injection-locking pages switch to $\tilde\Gamma$ |
| $\omega_L,\ \omega_L^{\pm}$ | (half) lock range | rad/s | [P3][P4] | sinusoidal injection: $\omega_L=\tfrac12 I_{inj}\lvert\tilde\Gamma_1\rvert$ ([P3] Eq.(35), p.2114); ideal LC $=I_{inj}/(2q_{max})$; lock condition $\lvert\Delta\omega\rvert\le\omega_L$; canonical $f_L=\omega_L/2\pi=5$ MHz (injection_locking_noise example); generally asymmetric, $\omega_L^+\ne-\omega_L^-$ ([P4] Eq.(23)) |
| $I_{inj},\ i_{inj}(t)$ | amplitude / instantaneous waveform of the injection current | A | [P3] | $i_{inj}(t)$ appears in the time-synchronous averaging integral $\Omega(\theta)=\frac{1}{T_{inj}}\int_{T_{inj}}\tilde\Gamma\,i_{inj}\,dt$ ([P3] Eq.(30), p.2113); for sinusoidal injection $I_{inj}$ is its amplitude |
| $q_{inj}$ | charge in one injected pulse | C | [P3] | [P3] Sec. IV, p.2112 (the impulse-train thought experiment); canonical 50 fC (5% of $q_{max}$; see the injection_locking_noise worked example) |
| $\omega_{inj}$ | angular frequency of the injected signal | rad/s | [P3][P4] | its difference from $\omega_0$ is the detuning — see the $\Delta\omega$ (injection) row above |
| $\theta(t),\ \theta_{ss}$ | oscillator's phase relative to the injection / its steady-state value | rad | [P3] | coordinate change $\theta=\phi-\omega_{inj}t$ ([P3] Eq.(4): $\phi(t)\equiv\omega_{inj}t+\theta(t)$); locked steady state $\sin\theta_{ss}=\Delta\omega/\omega_L$, stable branch $\cos\theta_{ss}\gt0$; **shares an axis with the ISF's argument $\omega_0\tau$ above, but is unrelated to the Fourier phase $\theta_n$ in the $c_n,\theta_n$ row** |
| $\Omega(\theta)$ | lock characteristic (the injection-induced mean frequency shift, as a function of $\theta$) | rad/s | [P3] | [P3] Eq.(33), p.2114: $\Omega(\theta)=\dfrac{1}{T_{inj}}\displaystyle\int_{T_{inj}}\tilde\Gamma(\omega_{inj}t+\theta)\,i_{inj}(t)\,dt$; the lock range is the width of its range |
| $a$ | LC injection-strength ratio | — | [P4] | $a\equiv I_{inj}/I_{osc}$ ([P4] Eq.(8), Mirzaei's Generalized Adler); large-injection $\omega_L=\omega_{L0}/\sqrt{1-a^2}$; under the identity $\omega_0 q_{max}=Q\,I_{osc}$, $a=\tau_0\,\omega_{L0}$ (exact) |
| $M$ | (context-dependent — see the disambiguation below) | — | [P4] and the measurement page | [P4] Eq.(28)–(30), p.2129's $M{:}N$ subharmonic-locking ratio ($M=1$ is division); measurement_and_spurs.md's cross-correlation **averaging count** — same letter, unrelated meaning |
| $\beta$ (realignment factor) | the fraction of phase error one pulse pulls back | — | this site's / ILCM convention | $\beta\equiv-q_{inj}\,\tilde\Gamma'(\theta_{ss})$ (defined in subharmonic_injection.md, **not a [P3]/[P4] paper symbol**); stable for $0\lt\beta\lt2$; continuous limit $\omega_c=\beta/T_{inj}$ (see the $\omega_c$ disambiguation below); **unrelated to the $\beta_{[P4]}$ below, the FM modulation index $\beta$ (varactor page), and the MOS $\beta$ (lab_32 square-law gain factor) — four different meanings** |
| $\beta_{[P4]}$ | phase difference between the ISF fundamental and the APF fundamental | rad | [P4] | $\beta\equiv\angle\tilde\Gamma_1-\angle\Delta_1$ ([P4] Eq.(23), p.2127); ideal LC: $\angle\tilde\Gamma_1=90°,\ \angle\Delta_1=0°\Rightarrow\beta_{[P4]}=90°$ (quadrature); determines whether the large-injection lock range is symmetric ($\beta_{[P4]}=\pm90°$ gives symmetry — see the discussion following [P4] Eq.(23)) |
| $\gamma$ | MOSFET channel thermal-noise coefficient | — | [P2] | $\overline{i_n^2}=4kT\gamma g_m$; long-channel $\gamma=2/3$; **$\gamma\ne\Gamma$ (ISF, above), $\gamma\ne$ the Euler–Mascheroni constant** (noted separately where 99_appendix uses the latter); the ring-FOM ([P2] Eq.(23)) leading coefficient is $8/(3\eta)$ — $\gamma$ enters only through $V_{char}=\Delta V/\gamma$ below |
| $\Delta V$ | differential-pair linearizing voltage swing | V | [P2] | long-channel $\Delta V=V_{GS}-V_T$; short-channel $\Delta V=E_cL$ ([P2] p.796) |
| $V_{char}$ | characteristic voltage in the ring FOM | V | [P2] | $V_{char}=\Delta V/\gamma$; appears in the $V_{DD}/V_{char}$ term of [P2] Eq.(23) |
| $F_{eff}$ | topology noise factor (the variable part of the FOM ceiling) | — | this site (fom_limit.md, an external FOM convention) | $\mathrm{FOM}=173.8-10\log_{10}F_{eff}$ dB (300 K); the constant $173.8=-10\log_{10}(kT\cdot1\,\text{Hz}/1\,\text{mW})$ corresponds to $1\cdot kT$ (**not** $2kT$, which would give $170.8$); ring $F_{eff}\ge3.6$ (ceiling 168.3 dB), LC $F_{eff}\propto1/Q^2$ |
| $K_{VCO}$ | VCO tuning gain | Hz/V (or rad/s/V) | this site (varactor_tuning_supply_pushing.md) | $K_{VCO}\equiv\partial f_0/\partial V_{tune}$; worked example 50 MHz/V |
| $K_{push}$ | supply-pushing gain | Hz/V | this site | $K_{push}\equiv\partial f_0/\partial V_{DD}$; lab_38 (Level-1 MOS ring, first-principles measurement) measures 2.936 GHz/V |
| $H_{lp}(f),\ H_{hp}(f)$ | PLL closed-loop low-pass / high-pass transfer functions | — | this site (pll_noise_budget.md) | $S_{out}=(S_{ref}N^2+S_{cp})\lvert H_{lp}\rvert^2+S_{vco}\lvert H_{hp}\rvert^2$; type-II second order, parameterized by $\omega_n,\zeta$ (see the $\omega_n/f_n$ and $\zeta$ disambiguation below) |
| $S_{ref},\ S_{vco},\ S_{cp}$ | PSDs of the PLL's individual noise sources (reference / VCO / charge pump) | rad²/Hz | this site | three statistically independent sources whose power sums into $S_{out}$ (row above) |
| $D$ (this site's convention B) | phase-diffusion coefficient | rad²/s | this site / external literature (Demir 2000) | $D=\kappa^2/2=\Gamma_{rms}^2 S_i/(4q_{max}^2)$, canonical $0.0625$ (diffusion_dictionary.md, spec Sec. 11.2, v5); paired with $\mathrm{Var}[\Delta\phi]=2D\lvert t\rvert$; 3-dB linewidth $\Delta f_{3dB}=D/\pi=\kappa^2/2\pi\approx19.9$ mHz (true LC: $39.8$ mHz); **$\ne$ [P4]'s $D(\tau,\phi)$** (the amplitude perturbation quantity — see the $\tilde\Lambda$ row above) |
| $\sigma_y(\tau),\ h_\alpha$ | Allan deviation / frequency-metrology power-law noise coefficient | dimensionless / depends on $\alpha$ | external literature (IEEE 1139, not one of this site's 5 PDFs) | $S_y(f)=h_\alpha f^\alpha$, $\alpha=-2,\dots,+2$; here $\tau$ is the **averaging time (gate time)** — it collides in name with, but is unrelated to, the ISF's injection instant $\tau$ above (see that row's note) |
| RJ/DJ/TJ | random / deterministic / total jitter | s | SerDes industry convention (dj_dual_dirac.md) | dual-Dirac extrapolation: $\mathrm{TJ}(\mathrm{BER})=\mathrm{DJ}_{\delta\delta}+2\,Q^{-1}(\mathrm{BER})\,\mathrm{RJ}_{rms}$; $\mathrm{RJ}_{rms}=\sigma_t$ (row above); at BER $=10^{-12}$ the multiplier $2Q^{-1}=14.07$ |

## Overloaded symbols (same symbol, different meaning by context)

The following symbols mean different physical quantities on **different pages**; each page's own definition governs there — this section only flags what not to confuse it with.

**$\omega_c$ (three meanings, none of them the 1/f³ corner $\omega_{1/f^3}$)**:
1. **AM / amplitude-decay corner** (phase_vs_amplitude_noise.md): $\omega_c=1/\tau_0=\omega_0/2Q$ — the bandwidth of the tank's amplitude restoration.
2. **Injection-locking pull-in frequency** (injection_locking_noise.md, i.e. the native result of [P3] Eq.(40)): $\omega_c=\omega_L\cos\theta_{ss}=\sqrt{\omega_L^2-\Delta\omega^2}$ — strongest at the center of the lock range, vanishing at the edges; discrete version $\omega_c=\beta/T_{inj}$ (subharmonic_injection.md).
3. **PLL open-loop crossover frequency** (a passing usage in pll_noise_budget.md): a loop-filter design bandwidth metric, unrelated to the first two.

**$\tau_0$ (three meanings)**:
1. **Amplitude memory time** ([P4] Sec. III-B, Eq.(25)): $\tau_0=2Q/\omega_{osc}$, the time constant of the LC amplitude decay $e^{-t/\tau_0}$.
2. **Jitter averaging window** (jitter_kernels.md): $\tau_0=NT$, the observation window accumulating $N$ periods ($T$ = oscillation period).
3. **Impulse injection instant** (convolution_derivation.md's degeneracy check): a single impulse lands at $\tau_0$, $\phi(t)=\Gamma(\omega_0\tau_0)\Delta q/q_{max}$ — this is really just a special case of the $\tau$ row above, which happens to be labeled $\tau_0$ there.

**$\zeta$ (two meanings)**:
1. **PLL damping ratio** (pll_noise_budget.md): $\zeta\gt0$; this site's worked design takes near-critical $\zeta=0.707$; controls the peaking of $H_{lp}/H_{hp}$.
2. **[P2] Fig.16's quadratic-term coefficient for accumulated jitter** (jitter_kernels.md, Step 5b): $\sigma(\Delta t)=\sqrt{\kappa^2\Delta t+\zeta^2\Delta t^2}$, dimensionless in the time version (this site has verified the printed value $2.5\text{e}5$ is missing a minus sign, and corrected it to $\zeta=2.5\times10^{-5}$); the phase version is $\zeta_\phi=\omega_0\zeta$ (rad/s).

**$\omega_n,\ f_n$ (PLL natural frequency, this site's PLL-teaching convention, not a symbol from the 5 PDFs)**: the central metric of the loop bandwidth; the type-II second-order peaking closed form peaks at $2.09$ dB at $\zeta=0.707$, located at $f_{pk}=0.786\,f_n$ (pll_noise_budget.md, verified by `# ->`: `0.707: closed 0.7862/2.0903 dB`).

**$\alpha$ (three meanings, all distinct from the NMF $\alpha(\omega_0t)$ in the main table above)**: the NMF function (main table above, $0\le\alpha\le1$, periodic); fourier_series_of_isf.md's toy model's **scalar** DC offset ($\Gamma=\cos\theta+\alpha$, $c_0=2\alpha$); the Allan-variance page's power-law **exponent** ($S_y=h_\alpha f^\alpha$). Same letter, completely different domains and physical meaning — check the page context first.

**$N$ (three meanings)**: [P2]'s ring stage count ($\Gamma_{rms}\propto N^{-3/2}$); the injection-division/subharmonic cluster's frequency ratio ($\omega_{inj}\approx N\omega_0$, $\div N$ or $\times N$); jitter_kernels.md's accumulated period count ($\tau_0=NT$).

**$M$ (two meanings)**: [P4]'s $M{:}N$ subharmonic-locking ratio ($M=1$ is division; see injection_locked_division.md); measurement_and_spurs.md's cross-correlation averaging count (the floor converges as $1/\sqrt{M}$).

## The four "dialects" of jitter

Many people lump all jitter together, when in fact the measured quantities differ:

| Name | Definition | Intuition |
|---|---|---|
| **period jitter** | $T_k-T$ (a single period vs. nominal) | how long/short this beat is |
| **cycle-to-cycle jitter** | $T_{k+1}-T_k$ (difference between two adjacent beats) | how fast the beat changes from one to the next |
| **accumulated / long-term jitter** | timing error between two edges separated by $\Delta t$, $\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$ | an open-loop oscillator drifts further the longer it runs |
| **random jitter (RJ)** | Gaussian, unbounded; described by $\sigma$ | what SerDes BER uses to estimate eye closure |

See [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter) and
[serdes_clocking_connection](/06_design_insights/serdes_clocking_connection) for details.

## Symbol correspondence across the papers (where unification is needed)

| Concept | This site's symbol | Papers' notation / remarks |
|---|---|---|
| ISF | $\Gamma(\omega_0\tau)$ | [P1][P2] use $\Gamma$; some later literature uses $h$ or "ISF" |
| maximum charge | $q_{max}$ | [P1] $q_{max}=C_{node}V_{max}$; in rings it corresponds to the per-stage node charge |
| offset frequency | $\Delta\omega$ or $\Delta f$ | [P1] mostly uses $\Delta\omega$; datasheets use $\Delta f$ (Hz) |
| amplitude counterpart of phase sensitivity | amplitude ISF $\tilde\Lambda$ (1/C) / APF $\Delta=\tau_0\tilde\Lambda$ (1/A, ideal LC) | [P4] Eq.(18),(24): $\tilde\Lambda(\phi)=D(0,\phi)$, the tilde denotes charge normalization; Eq.(19),(25): APF $\Delta(\phi)=\int_0^\infty D\,d\tau$, **no tilde** ([P4] footnote 6, p.2126: $\Lambda\equiv q_{max}\tilde\Lambda$ is the dimensionless amplitude ISF of [28]); ideal-LC fundamentals $\tilde\Gamma_1=\frac{1}{q_{max}}\angle90°$, $\Delta_1=\frac{\tau_0}{q_{max}}\angle0°$ (Eq.(26), p.2128), in quadrature; $\tau_0=2Q/\omega_0$ |
| dimensioned ISF | $\tilde\Gamma=\Gamma/q_{max}$ | [P3] Eq.(26): Hong uses the dimensioned version (rad/C); this site's core uses the dimensionless $\Gamma$ |
| phase equation (injection) | generalized Adler | [P3] Eq.(30),(33): $\frac{d\theta}{dt}=(\omega_0-\omega_{inj})+\Omega(\theta)$, $\Omega=\langle\tilde\Gamma\,i_{inj}\rangle$ |
| PPV / adjoint / Floquet | — | **not in these 5 PDFs**; external literature (Demir et al.), see [effective_isf](/03_isf_core_theory/effective_isf) |

> **Notation trap**: $c_0$ is the Fourier **coefficient**, while the DC **value** of the ISF is $c_0/2$ (see Eq.(12)).
> This factor is an easy source of error when computing the 1/f³ corner (Eq.(24)); later chapters will keep reminding you.
