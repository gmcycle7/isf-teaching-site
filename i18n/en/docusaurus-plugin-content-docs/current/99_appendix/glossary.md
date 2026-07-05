---
title: Chinese–English Glossary
description: Chinese–English pairing of ISF-related terminology, each with a one-line Chinese intuition and a link to the source page on the site.
---

> **β**: This English translation is in beta — the Traditional-Chinese original is the authoritative version.

# Chinese–English Glossary

> **See also**: [notation](/00_overview/notation) (rigorous symbols and units), [math_identities](/99_appendix/math_identities) (math toolbox), [references](/99_appendix/references) (source codes [P1]–[P5], external [E1]–[E4])

The biggest friction when reading English papers alongside Chinese teaching pages is "one concept, two languages." This page pairs the site's terminology **Chinese–English**,
each with **one line of Chinese intuition** (not a rigorous definition, just "get the feel first") plus the **page it comes from**. Click through for depth.

> **How to use this page**: when you hit an unfamiliar term on some page, come back here, scan a one-liner, then decide whether to click through to the source page for detail.
> For rigorous symbols and units, cross-reference [notation](/00_overview/notation). Terms marked **(external)** mean they are **not
> among the five downloaded PDFs**, supplemented from standard literature.

---

## Core ISF terminology

| English | Chinese | One-line intuition | Source page |
|---|---|---|---|
| **ISF (Impulse Sensitivity Function)** | 脈衝敏感度函數 | The oscillator's "phase-sensitivity weighting" to noise — tells you "kick it at this phase of the waveform, and this much phase results." Dimensionless, $2\pi$-periodic. | [isf_definition](/03_isf_core_theory/isf_definition) |
| **excess phase** | 多餘相位 $\phi(t)$ | The deviation beyond the ideal phase $\omega_0 t$; both phase noise and jitter live here. | [impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift) |
| **phase noise** | 相位雜訊 | Random jitter of the oscillator signal's phase, appearing in the frequency domain as skirts on either side of the carrier. | [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) |
| **timing jitter** | 時間抖動 | The time-domain statement of the same thing: the random error of when an edge actually occurs relative to ideal. | [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter) |
| **phase perturbation** | 相位擾動 | The component of noise that pushes the state point "tangent to the limit cycle"; **no restoring force**, it persists forever. | [phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise) |
| **amplitude perturbation** | 振幅擾動 | The component of noise that pushes the state point "radially"; a restoring mechanism pulls it back, **does not persist**. | [phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise) |
| **limit cycle** | 極限環 | The closed trajectory the oscillator circles in steady state in state-space; phase = how far along the cycle, amplitude = how far off the cycle. | [oscillator_phase](/02_foundations/oscillator_phase) |

---

## System and noise properties

| English | Chinese | One-line intuition | Source page |
|---|---|---|---|
| **LTI (Linear Time-Invariant)** | 線性非時變 | Impulse response depends only on "how long ago" $t-\tau$; the oscillator's response to noise is **not** LTI. | [math_identities](/99_appendix/math_identities) |
| **LTV (Linear Time-Variant)** | 線性時變 | Impulse response also depends on "when you kick it" $\tau$ — the same impulse has different effect at different phases, which is exactly the spirit of the ISF. | [convolution_derivation](/03_isf_core_theory/convolution_derivation) |
| **cyclostationary noise** | 週期穩態雜訊 | The noise strength itself varies periodically with the oscillation period (the device does not leak noise at every instant equally). | [effective_isf](/03_isf_core_theory/effective_isf) |
| **noise-modulating function (NMF)** $\alpha(\omega_0 t)$ | 雜訊調變函數 | A periodic function with $0\le\alpha\le1$ describing "when the device is leaking noise"; multiplied by the ISF gives the effective ISF. | [effective_isf](/03_isf_core_theory/effective_isf) |
| **white noise** | 白噪 | Noise whose PSD is frequency-independent (autocorrelation is a delta); converted by the ISF integrator into $1/f^2$ phase noise. | [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) |
| **flicker noise (1/f noise)** | 閃爍雜訊／$1/f$ 雜訊 | Device noise with large low-frequency energy; only upconverted through the ISF's $c_0$ into close-in $1/f^3$ phase noise. | [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion) |
| **upconversion** | 上轉（頻率搬移） | The ISF acts like a mixer, moving device noise at low frequency (or near $n\omega_0$) up to near the carrier as phase noise. | [fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf) |

---

## Fourier and statistical quantities

| English | Chinese | One-line intuition | Source page |
|---|---|---|---|
| **rms / effective ISF** | rms ISF $\Gamma_{rms}$ / 有效 ISF $\Gamma_{eff}$ | $\Gamma_{rms}$ is the rms of the ISF, directly setting the size of $1/f^2$ phase noise; $\Gamma_{eff}=\Gamma\cdot\alpha$ folds in cyclostationarity. | [rms_isf](/03_isf_core_theory/rms_isf) |
| **$q_{max}$** | 最大電荷擺幅 | The nodal charge swing $=C\cdot V_{max}$, used to normalize the ISF; larger means lower phase noise. | [impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift) |
| **$c_0$ (DC ISF coefficient)** | ISF 的 DC 係數 | The key controlling $1/f$ upconversion; the ISF's DC **value** $=c_0/2$. For a symmetric waveform $c_0\approx0$. | [symmetry](/06_design_insights/symmetry) |
| **Fourier series / coefficients** $c_n,\theta_n$ | 傅立葉級數／係數 | Decomposes the $2\pi$-periodic ISF into DC plus harmonics; the $n$-th harmonic moves noise near $n\omega_0$. | [fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf) |
| **PSD (Power Spectral Density)** | 功率譜密度 | Noise power per unit bandwidth; $S_i$ (A²/Hz), $S_\phi$ (rad²/Hz). Integrating over frequency gives variance. | [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter) |
| **SSB phase noise** $\mathcal{L}(\Delta f)$ | 單邊帶相位雜訊 | Phase-noise power relative to the carrier, in a single sideband, per Hz; $\approx\frac12 S_\phi$. | [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter) |
| **dBc/Hz** | 分貝（相對載波）每赫茲 | The unit of $\mathcal{L}$: "c" = relative to carrier, "/Hz" = per unit bandwidth, taking $10\log_{10}$. | [math_identities](/99_appendix/math_identities) |

---

## Oscillator types and advanced concepts

| English | Chinese | One-line intuition | Source page |
|---|---|---|---|
| **ring oscillator** | 環形振盪器 | $N$ inverter stages in a ring; ISF is concentrated at the transition, $\Gamma_{rms}\propto N^{-3/2}$. | [lab_03](/04_simulation_labs/lab_03_ring_oscillator_toy_model) |
| **LC oscillator** | LC 振盪器 | Tank resonance, near-sinusoidal waveform; ideal ISF $=-\sin\theta$. | [lab_02](/04_simulation_labs/lab_02_lc_oscillator_toy_model) |
| **accumulated jitter** | 累積（長期）jitter | An open-loop oscillator has no absolute time reference, so its error grows like a random walk $\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$. | [lab_03](/04_simulation_labs/lab_03_ring_oscillator_toy_model) |
| **injection locking / pulling** | 注入鎖定／拉扯 | An injected external signal "pulls" the oscillator's frequency toward it; the same ISF also governs this phenomenon (generalized Adler). | [paper_003_injection_locking_part1](/05_paper_deep_dives/paper_003_injection_locking_part1) |
| **APF (Amplitude Perturbation Function)** $\Lambda(\phi)$ | 振幅擾動函數 | What the ISF is to phase, the APF is to amplitude; unit 1/A. Orthogonal (in quadrature) to the ISF in an ideal LC. | [paper_004_injection_locking_part2](/05_paper_deep_dives/paper_004_injection_locking_part2) |
| **Adler's equation** | Adler 方程 | The first-order differential equation describing the injection-locked phase difference (1946); the ISF generalizes it to arbitrary waveforms. | [paper_003_injection_locking_part1](/05_paper_deep_dives/paper_003_injection_locking_part1) |

---

## Rigorous mathematical foundations (external literature)

| English | Chinese | One-line intuition | Source page |
|---|---|---|---|
| **PPV (Perturbation Projection Vector)** | 擾動投影向量 **(external)** | The rigorous generalization of the ISF: the vector projecting a perturbation onto the phase direction; corresponds to the theory of Demir et al. 2000. **Not among the five source PDFs.** | [effective_isf](/03_isf_core_theory/effective_isf) |
| **adjoint method** | 伴隨法 **(external)** | A numerical method for computing the PPV/ISF from the periodic steady-state solution (solving the adjoint system). **Not among the five source PDFs.** | [effective_isf](/03_isf_core_theory/effective_isf) |
| **Floquet theory** | Floquet 理論 **(external)** | Stability theory for linear systems with periodic coefficients; gives the mathematical foundation of the PPV. **Not among the five source PDFs.** | [effective_isf](/03_isf_core_theory/effective_isf) |
| **Wiener–Khinchin theorem** | 維納–辛欽定理 **(external)** | The PSD is the Fourier transform of the autocorrelation function; connects time-domain and frequency-domain noise. A standard stochastic-process theorem. | [math_identities](/99_appendix/math_identities) |
| **Leeson model** | Leeson 模型 **(external)** | The 1966 empirical phase-noise model; the ISF theory subsumes it as a special case. **Not among the five source PDFs.** | [references](/99_appendix/references) |

---

## One-line reminders (the pairs most often confused)

- **phase noise vs timing jitter**: the same thing, the former in the frequency domain (dBc/Hz), the latter in the time domain (fs);
  interconvert via $\sigma_t=\sigma_\phi/(2\pi f_0)$.
- **phase perturbation vs amplitude perturbation**: phase **stays**, amplitude **gets pulled back** — which is why phase noise is the star of the show.
- **LTI vs LTV**: the difference is whether the impulse response depends on the absolute time $\tau$; the oscillator is LTV.
- **$c_0$ vs the $1/f^3$ corner**: $c_0$ determines whether flicker upconverts at all; the $1/f^3$ corner $=\omega_{1/f}(c_0/c_1)^2$,
  **is not equal to** the device's $\omega_{1/f}$.
- **device $1/f$ corner $\omega_{1/f}$ vs phase-noise $1/f^3$ corner $\Delta\omega_{1/f^3}$**: two different things,
  do not confuse them (see [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)).

## Further reading

- Rigorous symbols and units: [notation](/00_overview/notation)
- Math toolbox: [math_identities](/99_appendix/math_identities)
- Full literature list and citation conventions: [references](/99_appendix/references)
- Equation index: [equation_index](/01_paper_map/equation_index)
