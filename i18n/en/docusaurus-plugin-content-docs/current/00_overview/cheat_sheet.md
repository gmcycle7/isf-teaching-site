---
title: Cheat Sheet
description: "One-page quick reference: core formulas, canonical numbers, unit conversions, design knobs, the five papers. Skim it before an exam or a design review."
---

> 🌐 English translation (β). Most other pages are currently in Traditional Chinese — they will show in Chinese until translated.

# Cheat Sheet

The most frequently used formulas, numbers and knobs of the whole site, condensed onto
one page. Every entry links back to its full derivation page.

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

## The five papers in one line each

- **[P1]** Hajimiri–Lee 1998: the ISF theory itself (the oscillator is LTV).
- **[P2]** 1999: ISF applied to rings — closed-form jitter/PN, $N$-independence.
- **[P3]** Hong 2019 I: ISF generalizes Adler → generalized injection locking.
- **[P4]** Hong 2019 II: the APF (amplitude counterpart of the ISF), $\tau_0=2Q/\omega_0$, frequency division.
- **[P5]** a sense amplifier paper, **unrelated to the ISF** (honestly labeled).

Full cross-reference: [paper_summary_table](/01_paper_map/paper_summary_table), [equation_index](/01_paper_map/equation_index).
