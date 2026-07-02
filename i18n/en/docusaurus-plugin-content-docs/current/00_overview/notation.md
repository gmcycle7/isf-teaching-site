---
title: Unified Notation Table
description: Site-wide consistent symbols, units, and the symbol correspondence across the papers.
---

# Unified Notation Table

:::info β English translation
This page is a **β (beta) English translation** of the Traditional-Chinese original at the same path. The zh-Hant version is authoritative. All mathematics, units, citations ([P1]–[P4]), and links are kept identical to the original.
:::

Different papers write the same thing with different symbols. This page **unifies** them; every later chapter follows this table.
If you encounter a different convention in one of the papers, come back here to cross-reference.

> **How to use this page**: skim it once to get acquainted; when actually reading the derivations, come back and look up any symbol you do not recognize.
> Every quantity is labeled with its **unit** — doing a dimension check is the fastest way to catch mistakes.

## Main symbols

| Symbol | Meaning (intuition) | Unit | Used in | Notes |
|---|---|---|---|---|
| $t$ | time | s | all | — |
| $\tau$ | injection instant of the noise/impulse | s | [P1] | the ISF's argument is the injection phase $\omega_0\tau$ |
| $T$ | oscillation period $T=1/f_0$ | s | all | — |
| $\omega_0$ | oscillation angular frequency $=2\pi f_0$ | rad/s | all | — |
| $f_0$ | oscillation (carrier) frequency | Hz | all | e.g. 5 GHz |
| $\phi(t)$ | excess phase (the deviation beyond the ideal phase) | rad | [P1][P2] | phase noise / jitter lives here |
| $\Delta\phi$ | phase step / phase error | rad | all | the jump caused by one impulse |
| $A(t)$ | instantaneous amplitude | V or normalized | [P1][P4] | perturbations get pulled back (see [P4] APF) |
| $\Gamma(\omega_0\tau)$ | **ISF**, the oscillator's "phase sensitivity" to noise; dimensionless, $2\pi$-periodic | — | [P1] | not the noise itself, but a weighting function |
| $q_{max}$ | maximum node charge swing $=C\cdot V_{max}$ | C | [P1] | used for normalization; the larger it is, the lower the phase noise |
| $\Delta q$ | injected charge $=\int i\,dt$ | C | [P1] | e.g. 1 fC |
| $i_n(t)$ | noise current | A | [P1][P2] | the noise source injected into the node |
| $\overline{i_n^2}/\Delta f$ | current-noise power spectral density (single-sided) | A²/Hz | [P1] | white: independent of frequency |
| $S_i(f)$ | current-noise PSD | A²/Hz | all | another way of writing the same thing |
| $S_\phi(f)$ | phase PSD (single-sided) | rad²/Hz | all | integrating over $f$ gives $\sigma_\phi^2$ |
| $\mathcal{L}(\Delta f)$ | SSB phase noise (single-sideband phase noise) | dBc/Hz | all | $\approx\frac12 S_\phi$ |
| $\Delta f,\ \Delta\omega$ | offset frequency (how far from the carrier) | Hz, rad/s | all | $\Delta\omega=2\pi\Delta f$ |
| $c_0$ | DC Fourier coefficient of the ISF (DC value $=c_0/2$) | — | [P1] | the key to 1/f upconversion |
| $c_n,\ \theta_n$ | amplitude / phase of the ISF's $n$-th harmonic | — | [P1] | moves noise near $n\omega_0$ onto the carrier |
| $\Gamma_{rms}$ | rms value of the ISF | — | [P1][P2] | sets the magnitude of the 1/f² phase noise |
| $\Gamma_{eff}$ | effective ISF (including cyclostationarity) | — | [P1] | $\Gamma_{eff}=\Gamma\cdot\alpha$ |
| $\alpha(\omega_0 t)$ | noise-modulating function (NMF): when the device is "leaking noise" | — | [P1] | $0\le\alpha\le1$, periodic |
| $\sigma_t$ | rms timing jitter | s | [P2] | what SerDes cares about most |
| $\sigma_\phi$ | rms phase | rad | all | $\sigma_t=\sigma_\phi/(2\pi f_0)$ |
| $\kappa$ | proportionality constant of ring accumulated jitter | $\sqrt{\mathrm{s}}$ | [P2] | $\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$ |
| $\omega_{1/f}$ | the device's 1/f-noise corner | rad/s | [P1] | note: ≠ the phase-noise 1/f³ corner |
| $N$ | number of ring-oscillator stages | — | [P2] | $\Gamma_{rms}\propto N^{-3/4}$ |
| $Q$ | tank quality factor | — | [P1] | appears in the Leeson comparison |
| $\eta$ | proportionality constant in the ring frequency / FOM | — | [P2] | $f_0=1/(2N\tau_D)$ |

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
| amplitude counterpart of phase sensitivity | (see [P4]) APF $\tilde\Lambda$ | [P4] amplitude perturbation function; ideal LC fundamental $\tilde\Lambda_1=\frac{\tau_0}{q_{max}}\angle0°$, in quadrature with the ISF; $\tau_0=2Q/\omega_0$ |
| dimensioned ISF | $\tilde\Gamma=\Gamma/q_{max}$ | [P3] Eq.(26): Hong uses the dimensioned version (rad/C); this site's core uses the dimensionless $\Gamma$ |
| phase equation (injection) | generalized Adler | [P3] Eq.(30),(33): $\frac{d\theta}{dt}=(\omega_0-\omega_{inj})+\Omega(\theta)$, $\Omega=\langle\tilde\Gamma\,i_{inj}\rangle$ |
| PPV / adjoint / Floquet | — | **not in these 5 PDFs**; external literature (Demir et al.), see [effective_isf](/03_isf_core_theory/effective_isf) |

> **Notation trap**: $c_0$ is the Fourier **coefficient**, while the DC **value** of the ISF is $c_0/2$ (see Eq.(12)).
> This factor is an easy source of error when computing the 1/f³ corner (Eq.(24)); later chapters will keep reminding you.
