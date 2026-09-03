---
title: Cheat Sheet
description: "One-page quick reference: core formulas, canonical numbers, unit conversions, design knobs, the five papers, plus a v5–v8 quick-reference block (jitter kernels, kappa/D/linewidth dictionary, App.B closed forms, M:N locking, PLL peaking, FOM, SerDes). Skim it before an exam or a design review."
---

> **β**: This English translation is in beta — the Traditional-Chinese original is the authoritative version.

# Cheat Sheet

The most frequently used formulas, numbers and knobs of the whole site, condensed onto
one page. Every entry links back to its full derivation page.

> 🖨 **Print / save as PDF**: press `Cmd+P` (macOS) or `Ctrl+P` (Windows/Linux) in a
> desktop browser to save **this page** as a PDF or send it straight to a printer — this
> works on every page of the site, not just the cheat sheet. The navbar, sidebar,
> right-hand table of contents, and footer hide themselves automatically; the controls
> on interactive widgets (sliders, buttons) hide too, but whatever SVG plot a widget is
> currently showing stays in the printout. Collapsed `<details>` blocks (e.g. the
> worked solutions in [exercises](/02_foundations/exercises)) do **not** auto-expand —
> open every ▸ in the browser first if you need them on paper.

## Core formulas (all verified against the original PDFs)

| Topic | Formula | Source |
|---|---|---|
| ISF operational definition | $\Delta\phi=\dfrac{\Gamma(\omega_0\tau)}{q_{max}}\Delta q$ | [P1] Eq.(10)(11) → [impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift) |
| LTV phase response | $\phi(t)=\dfrac{1}{q_{max}}\displaystyle\int_{-\infty}^{t}\Gamma(\omega_0\tau)\,i_n(\tau)\,d\tau$ | [P1] Eq.(11) → [convolution](/03_isf_core_theory/convolution_derivation) |
| ISF Fourier | $\Gamma=\dfrac{c_0}{2}+\sum_n c_n\cos(n\omega_0\tau+\theta_n)$ | [P1] Eq.(12) → [fourier](/03_isf_core_theory/fourier_series_of_isf) |
| Parseval / rms | $\sum_{n=0}^\infty c_n^2=2\Gamma_{rms}^2$ | [P1] Eq.(20) → [rms_isf](/03_isf_core_theory/rms_isf) |
| White noise 1/f² | $\mathcal{L}=10\log_{10}\!\Big(\dfrac{\Gamma_{rms}^2}{q_{max}^2}\dfrac{\overline{i_n^2}/\Delta f}{4\,\Delta\omega^2}\Big)$ | [P1] Eq.(21) → [white_noise](/03_isf_core_theory/white_noise_to_phase_noise) |
| Flicker 1/f³ | $\mathcal{L}=10\log_{10}\!\Big(\dfrac{c_0^2}{q_{max}^2}\dfrac{\overline{i_n^2}/\Delta f}{8\,\Delta\omega^2}\dfrac{\omega_{1/f}}{\Delta\omega}\Big)$ | [P1] Eq.(23) → [flicker](/03_isf_core_theory/flicker_noise_upconversion) |
| 1/f³ corner | $\Delta\omega_{1/f^3}=\omega_{1/f}\dfrac{c_0^2}{2\Gamma_{rms}^2}$ | [P1] Eq.(24) |
| SSB↔PSD | $\mathcal{L}(\Delta f)\approx\tfrac12 S_\phi(\Delta f)$ | [psd](/02_foundations/psd_phase_noise_jitter) |
| phase→time | $\Delta t=\dfrac{\Delta\phi}{2\pi f_0}$ | standard |
| rms jitter | $\sigma_t=\dfrac{1}{2\pi f_0}\sqrt{\displaystyle\int_{f_1}^{f_2}S_\phi\,df}$ | [serdes](/06_design_insights/serdes_clocking_connection) |
| Accumulated jitter | $\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$, $\kappa=\dfrac{\Gamma_{rms}}{q_{max}}\sqrt{\tfrac12\tfrac{\overline{i_n^2}}{\Delta f}}$ | [P2] Eq.(8)(12) |
| Ring frequency | $f_0=\dfrac{1}{2N\tau_D}$ | [P2] Eq.(15) |
| Ring $\Gamma_{rms}$ | $\Gamma_{rms}=\sqrt{\dfrac{2\pi^2}{3\eta^3}}\;\dfrac{1}{N^{1.5}}\Rightarrow\Gamma_{rms}\propto N^{-3/2}$ (at $\eta=0.75$, $\approx4/N^{1.5}$, the solid line in [P2] Fig.8; the radical covers only the constant) | [P2] Eq.(16) |
| Ring FOM | $\mathcal{L}=\dfrac{8}{3\eta}\dfrac{kT}{P}\dfrac{V_{DD}}{V_{char}}\Big(\dfrac{f_0}{\Delta f}\Big)^2$ (no $N$!) | [P2] Eq.(23) |
| Generalized Adler | $\dfrac{d\theta}{dt}=(\omega_0-\omega_{inj})+\Omega(\theta)$, $\Omega=\langle\tilde\Gamma\,i_{inj}\rangle$ | [P3] Eq.(30)(33) |
| APF / amplitude decay | $\tau_0=\dfrac{2Q}{\omega_{osc}}$, $\tilde\Lambda_1=\dfrac{\tau_0}{q_{max}}\angle0°$ (in quadrature with the ISF) | [P4] Eq.(25)(26) |

## Canonical numbers (consistent site-wide)

| Example | Setup | Result |
|---|---|---|
| A: impulse→time | $q_{max}=1$ pC, $\Delta q=1$ fC, $\Gamma=0.5$, $f_0=5$ GHz | $\Delta\phi=5\times10^{-4}$ rad, $\Delta t=15.9$ fs |
| B: white-noise $\mathcal{L}$ | $\Gamma_{rms}=0.5$, $q_{max}=1$ pC, $S_i=10^{-24}$ A²/Hz, $\Delta f=1$ MHz | $\mathcal{L}=-148$ dBc/Hz |
| C: jitter integral | $\mathcal{L}(1\text{MHz})=-100$ dBc/Hz, 1/f², 1→100 MHz, 5 GHz | $\sigma_t=447.9$ fs |
| Ring FOM | $\gamma=2/3$, $V_{DD}/V_{char}=3$, $P=1$ mW, others as above | $\mathcal{L}\approx-91$ dBc/Hz |

> Want to sweep the parameters yourself? Use the [interactive calculator](/04_simulation_labs/interactive_calculator).

## Conversion anchors at 5 GHz

- $1$ mrad $\approx 32$ fs; $1$ rad $\approx 31.8$ ps; period $=200$ ps.
- dBc/Hz → linear: $10^{\mathcal{L}/10}$; $S_\phi=2\times$ linear.
- $2\times q_{max}$ or $\tfrac12\Gamma_{rms}$ → $\mathcal{L}$ drops by **6 dB**.

## Design knobs (to lower phase noise)

| To lower | Knob | Why |
|---|---|---|
| 1/f² (white noise) | ↑ $q_{max}$ (swing/energy), ↓ $\Gamma_{rms}$ | $\mathcal{L}\propto\Gamma_{rms}^2/q_{max}^2$ |
| 1/f³ (close-in) | make the waveform **symmetric** → ↓ $c_0$ | corner $\propto c_0^2/\Gamma_{rms}^2$ |
| Jitter (time domain) | same as above (same $\Gamma_{rms}^2/q_{max}^2$); or lock in a PLL/CDR | $\kappa\propto\Gamma_{rms}/q_{max}$ |
| Where noise is injected | avoid phases where $\lvert\Gamma\rvert$ is large (small slope) | cyclostationary $\Gamma_{eff}=\Gamma\alpha$ |

## v5–v8 quick reference (jitter kernels / κ↔D↔linewidth / App.B / M:N locking / PLL / FOM / SerDes)

Rule for this block: every entry is copied verbatim from its source page, convention flags included. The link is the single source of truth for the derivation.

### Jitter kernels (three kernels + white-FM closed form) — [jitter_kernels](/02_foundations/jitter_kernels)

| Kernel | Formula (one-sided $S_\phi$, $\int_0^\infty$ convention) | White-FM closed form |
|---|---|---|
| TIE (0th order) | $\sigma_{TIE}^2=\dfrac{1}{\omega_0^2}\displaystyle\int_{f_1}^{f_2}S_\phi\,df$ | — |
| N-period (1st-order difference) | $\sigma_P^2(N)=\dfrac{1}{\omega_0^2}\displaystyle\int_0^\infty S_\phi\,4\sin^2(\pi fNT)\,df$ | $=\kappa^2NT$ (exact match to [P2] Eq.(8)) |
| Cycle-to-cycle (2nd-order difference) | $\sigma_{c2c}^2=\dfrac{1}{\omega_0^2}\displaystyle\int_0^\infty S_\phi\,16\sin^4(\pi fT)\,df$ | $=2\kappa^2T\Rightarrow\sigma_{c2c}=\sqrt2\,\sigma_P(1)$ |

> The prefactor is $1/\omega_0^2$, **not** $2/\omega_0^2$ (that 2 belongs to the double-sided-spectrum or $\mathcal{L}=\tfrac12S_\phi$ bookkeeping).

### κ↔D↔linewidth↔ADEV↔$S_\phi$ dictionary (with the 19.9/39.8 mHz canonical numbers) — [diffusion_dictionary](/03_isf_core_theory/diffusion_dictionary)

Lead quantity: $\kappa^2=\dfrac{\Gamma_{rms}^2}{2q_{max}^2}\dfrac{\overline{i_n^2}}{\Delta f}$ ([P2] Eq.(11)/(12)); canonical ($\Gamma_{rms}=0.5$) gives $\kappa^2=0.125$ rad²/s, true LC ($\Gamma_{rms}=1/\sqrt2$) gives $0.25$.

| "Outfit" | Formula | Canonical value |
|---|---|---|
| $\kappa$ (phase) / $\kappa_t$ (time) | $\sigma_{\Delta\phi}=\kappa\sqrt{\Delta t}$; $\kappa_t=\kappa/\omega_0$ | $\kappa=0.354$ rad/$\sqrt{\text{s}}$ |
| $D$ convention A / B | $\mathrm{Var}=D_{A}\vert t\vert=2D_{B}\vert t\vert\Rightarrow D_{A}=\kappa^2,\ D_{B}=\kappa^2/2$ | $0.125$ / $0.0625$ |
| Lorentzian 3-dB linewidth | $\Delta f_{3\mathrm{dB}}=\kappa^2/(2\pi)$ | **19.9 mHz** (true LC **39.8 mHz**) |
| $S_\phi$ coefficient (one-sided) | $S_\phi=2\kappa^2/(2\pi f)^2$ | $b_{-2}=6.33\times10^{-3}$ rad²·Hz |
| White-FM ADEV | $\sigma_y(\tau)=\kappa/(2\pi f_0\sqrt\tau)$ | $1.13\times10^{-11}$@1s (5 GHz) |

> Three factor-of-2 families to settle before you convert: one-sided vs double-sided PSD, $\mathrm{Var}=D\vert t\vert$ vs $2D\vert t\vert$, and SSB $/2$ vs $/4$.

### App.B closed forms: $\Gamma_{rms}(A,N)$, $c_0$, corner — [asymmetric_isf_closed_form](/03_isf_core_theory/asymmetric_isf_closed_form)

$$
\Gamma_{rms}^2=\frac{2\pi^2}{3\eta^3}\frac{1}{N^3}\left[4\frac{1+A^3}{(1+A)^3}\right],\quad
\Gamma_{dc}=\frac{2\pi}{\eta^2}\frac{1}{N^2}\left(\frac{1-A}{1+A}\right),\quad c_0=2\Gamma_{dc}
$$

$$
f_{1/f^3}=f_{1/f}\cdot\frac{3}{2\eta N}\cdot\frac{(1-A)^2}{1-A+A^2}\qquad([\text{P2}]\ \text{Eq.}(52)\text{–}(57),\ \text{p.803})
$$

$A\equiv f'_{rise}/f'_{fall}$; $A=1$ degenerates exactly to [P2] Eq.(16) ($\Gamma_{rms}\propto N^{-1.5}$); the corner is quadratically flat at $A=1$, symmetric under $A\to1/A$, and $\propto1/N$. Convention flag: this corner is the [P2] Eq.(7)/(57) value; [P1] Eq.(24) (substituting $c_0=2\Gamma_{dc}$) $=2\times$ this value.

### [P1] appendix: $\Gamma=f'/(f'^2+f''^2)$ — [isf_from_waveform](/03_isf_core_theory/isf_from_waveform)

$$
\Gamma(x)=\frac{f'}{f'^{\,2}+f''^{\,2}}\qquad([\text{P1}]\ \text{Eq.}(37),\ \text{p.193})
$$

Substituting $f=\cos x$: the denominator $\sin^2+\cos^2=1$, giving $\Gamma=-\sin x$ exactly, and it stays bounded at the waveform peak (this is what resolves the $1/\text{slope}$ heuristic's divergence). Ranking of the three methods: A direct impulse injection (most accurate) → B this closed form (one period of waveform suffices) → C slope approximation $\Gamma=f'/f_{max}'^2$ (cheapest, ring-specific, Eq.(38)).

### Injection-locked noise shaping corner $=\omega_L\cos\theta_{ss}$ — [injection_locking_noise](/06_design_insights/injection_locking_noise) Part A

$$
\omega_c\equiv\omega_L\cos\theta_{ss}=\sqrt{\omega_L^2-\Delta\omega^2}\qquad([\text{P3}]\ \text{Eq.}(40)\text{'s pull-in frequency})
$$

At lock center ($\Delta\omega=0$) the corner is widest; at the lock edge ($\Delta\omega\to\omega_L$), $\cos\theta_{ss}\to0$ and the high-pass suppression of the oscillator's own noise **disappears entirely**. (First-order-PLL picture: own noise is high-passed, reference noise is low-passed.)

### Optimal injection waveform $\omega_L^*=I_{rms}\tilde\Gamma_{rms}$ — [injection_locking_noise](/06_design_insights/injection_locking_noise), final section

For a fixed $I_{rms}\equiv\sqrt{\langle i_{inj}^2\rangle}$, Cauchy–Schwarz gives the lock-range upper bound ([P3] Eq.(43)–(45), pp.2119–2120):

$$
\omega_L^*=I_{rms}\,\tilde\Gamma_{rms},\qquad i_{inj,0}^*(x)=\pm\frac{I_{rms}}{\tilde\Gamma_{rms}}\tilde\Gamma(x)
$$

Equality holds iff the injection waveform matches the ISF's shape (matched filter). Pure-sinusoid ISF: sinusoidal injection is already optimal (gain 1). Ring narrow-pulse ISF: gain $\approx\sqrt{\eta N/3}$ ($\approx2.06$ at $N=17$, matching [P3] Fig.19's "almost doubled").

### M:N subharmonic locking / ILFD: $\lvert\tilde\Gamma_N\rvert$ — [paper_004](/05_paper_deep_dives/paper_004_injection_locking_part2)

When locked at $M\omega_{inj}=N\omega_{osc}$ ($M=1$ is the ÷$N$ ILFD case), the half lock range rides on only the $N$-th ISF harmonic ([P4] Eq.(28)–(30), p.2129, verified):

$$
\Omega(\theta)=\frac12 I_{inj}\lvert\tilde\Gamma_N\rvert\cos(N\theta+\angle\tilde\Gamma_N)\ \Rightarrow\
\omega_L=\frac12 I_{inj}\lvert\tilde\Gamma_N\rvert=\frac{I_{inj}\,c_N}{2\,q_{max}}
$$

A half-wave-symmetric ISF ($c_2=c_4=\cdots=0$) means ÷2 cannot lock at first order — the same differential-node symmetry that's good news for phase noise is bad news for ILFD (fix: switch to the tail node to pick up $c_2$).

### Subharmonic multiplication (×N, ILCM): $\omega_L$, $\beta$, corner — [subharmonic_injection](/06_design_insights/subharmonic_injection)

The other half of the duality: at $N=1$, locking is carried by the injection waveform's own $N$-th harmonic (not the ISF's). Canonical: $f_0=5$ GHz, $q_{max}=1$ pC, $N=20$ ($f_{ref}=250$ MHz), $q_{inj}=50$ fC.

| Quantity | Formula | Canonical value |
|---|---|---|
| Multiplier lock range | $\omega_L=\tfrac12\vert I_N\vert\vert\tilde\Gamma_1\vert$ (impulse train: $\Delta\omega_L=\dfrac{q_{inj}}{q_{max}}\cdot\dfrac{f_0}{N}$) | $f_L=1.989$ MHz |
| Realignment factor | $\beta\equiv-q_{inj}\tilde\Gamma'(\theta_{ss})$ (stable for $0\lt\beta\lt2$, converges in $\approx1/\beta$ injections) | $0.0498$ |
| Noise corner | $f_c\approx\beta f_{ref}/2\pi$ (= $\Delta f_L$ at lock center) | $2.09$ MHz |

### ADEV floor: $\sqrt{2\ln2\cdot h_{-1}}$ — [allan_variance](/02_foundations/allan_variance)

$$
\sigma_{y,\text{floor}}=\sqrt{2\ln2\cdot h_{-1}}\approx1.1774\sqrt{h_{-1}}\qquad(\text{flicker FM, the }\tau\text{-independent floor})
$$

Canonical (with a $1/f^3$ corner of $3.2$ kHz): floor $\approx1.06\times10^{-9}$ (1.1 ppb); knee $\tau_{knee}=0.3607/f_c\approx113\ \mu$s (where the white-FM $\tau^{-1/2}$ segment meets the floor).

### PLL peaking: $\zeta=0.707\to2.09$ dB — [pll_noise_budget](/06_design_insights/pll_noise_budget), supplementary derivation

A type-II loop with a zero always peaks: $f_{pk}=f_n\sqrt{2/(s+1)}$, $s=\sqrt{1+1/\zeta^4}$ (golden-ratio easter egg: at $\zeta=1/\sqrt2$ the peak value $=\varphi=1.618$).

| $\zeta$ | $f_{pk}/f_n$ | Peaking (dB) | Phase margin |
|---|---|---|---|
| 0.707 | 0.786 | **2.09** | 65.5° |
| 1.0 | 0.707 | 1.25 | 76.3° |

Cascading 20 SONET regenerator stages: $20\times2.09=41.8$ dB, which is why specs cap peaking at the **0.1 dB** level per stage.

### FOM $=173.8-10\log_{10}F_{eff}$ — [fom_limit](/06_design_insights/fom_limit)

$$
\mathrm{FOM}=173.8\ \text{dB}-10\log_{10}F_{eff}\qquad(T=300\ \text{K, paired with }1\cdot kT\text{, not }2kT)
$$

Ring ceiling ($\gamma=2/3,\eta=1$): $F_{eff,min}=32/9\Rightarrow\mathrm{FOM}_{max}^{ring}=168.32$ dB; the LC ceiling rises with $Q$ ($F_{eff}\propto1/Q^2$).

### Aperture SNR: $-20\log_{10}(2\pi f_{in}\sigma_t)$ — [adc_aperture_jitter](/06_design_insights/adc_aperture_jitter)

$$
\text{SNR}_{jitter}=-20\log_{10}(2\pi f_{in}\sigma_t)\ \text{dB},\qquad \text{ENOB}=\frac{\text{SNR}-1.76}{6.02}\ \text{bit}
$$

Canonical $\sigma_t=447.9$ fs: at $f_{in}=f_0=5$ GHz, $2\pi f_{in}\sigma_t=\sigma_\phi=14.07$ mrad $\Rightarrow$ SNR $=37.0$ dB (carried over directly from example C).

### TJ $=\mathrm{DJ}_{\delta\delta}+2Q^{-1}(\mathrm{BER})\sigma$ — [dj_dual_dirac](/06_design_insights/dj_dual_dirac)

$$
\mathrm{TJ}(\mathrm{BER})=\mathrm{DJ}_{\delta\delta}+2\,Q^{-1}(\mathrm{BER})\,\sigma
$$

At BER$=10^{-12}$, $Q^{-1}=7.034$, so $\mathrm{TJ}=\mathrm{DJ}_{\delta\delta}+14.07\,\sigma$. DJ does not change with BER (bounded, paid once); the RJ term grows only slowly as BER tightens ($10^{-12}\to10^{-15}$: $14.07\sigma\to15.88\sigma$).

### ×N / ÷N / buffer bookkeeping — [clock_chain_budget](/06_design_insights/clock_chain_budget)

| Element | Phase relation | $\mathcal{L}(f)$ bookkeeping |
|---|---|---|
| Ideal ×N multiplication | $\phi_{out}=N\phi_{in}$ | $\mathcal{L}+20\log_{10}N$ |
| Ideal ÷N division | $\phi_{out}=\phi_{in}/N$ | $\mathcal{L}-20\log_{10}N$ |
| Through a PLL (×N) | in-band tracks ref, out-of-band tracks VCO | $N^2S_{ref}\lvert H_{lp}\rvert^2+S_{vco}\lvert H_{hp}\rvert^2$ |
| Buffer/divider additive floor | $\phi_{out}=\phi_{in}+\phi_{add}$ (uncorrelated) | $\mathcal{L}_{out}=10\log_{10}(10^{\mathcal{L}_{in}/10}+10^{\mathcal{L}_{buf}/10})$ (**convert to linear, add, then convert back to dB**) |

Conserved quantity: under ideal ×N/÷N, **the time-domain $\sigma_t$ (in seconds) never changes** — only the $\mathcal{L}$/rad bookkeeping does.

### $K_{push}$ path: $S_\phi=K^2S_v/\Delta f^2$ — [varactor_tuning_supply_pushing](/06_design_insights/varactor_tuning_supply_pushing)

$$
K_{VCO}\equiv\frac{\partial f_0}{\partial V_{tune}},\quad K_{push}\equiv\frac{\partial f_0}{\partial V_{DD}},\qquad
S_\phi(\Delta f)=\frac{K_{VCO}^2\,S_v(\Delta f)}{\Delta f^2}\ \ (\text{the supply version is identical, with }K_{VCO}\to K_{push},\ S_v\to S_{v,DD})
$$

Side by side with the ISF white-noise result: both have a $\Delta\omega^2$/$\Delta f^2$ integrator in the denominator, differing only in what feeds it ($\Gamma_{rms}/q_{max}$ vs $2\pi K_{VCO}$). White tune/supply noise $\to 1/f^2$; $1/f$ tune/supply noise $\to 1/f^3$ (parallel to the device $c_0$ mechanism). lab_38 gives a first-principles measurement of $K_{push}$ (ratio to $\beta$ of 1.002).

## The five papers in one line each

- **[P1]** Hajimiri–Lee 1998: the ISF theory itself (the oscillator is LTV).
- **[P2]** 1999: ISF applied to rings — closed-form jitter/PN, $N$-independence.
- **[P3]** Hong 2019 I: ISF generalizes Adler → generalized injection locking.
- **[P4]** Hong 2019 II: the APF (amplitude counterpart of the ISF), $\tau_0=2Q/\omega_0$, frequency division.
- **[P5]** a sense amplifier paper, **unrelated to the ISF** (honestly labeled).

Full cross-reference: [paper_summary_table](/01_paper_map/paper_summary_table), [equation_index](/01_paper_map/equation_index).
