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
| **APF (Amplitude Perturbation Function)** $\Delta(\phi)$ | 振幅擾動函數 | What the ISF is to phase, the APF is to amplitude; unit 1/A. Orthogonal (in quadrature) to the ISF in an ideal LC. | [paper_004_injection_locking_part2](/05_paper_deep_dives/paper_004_injection_locking_part2) |
| **Adler's equation** | Adler 方程 | The first-order differential equation describing the injection-locked phase difference (1946); the ISF generalizes it to arbitrary waveforms. | [paper_003_injection_locking_part1](/05_paper_deep_dives/paper_003_injection_locking_part1) |

---

## Injection Locking & Measurement

| English | Chinese | One-line intuition | Source page |
|---|---|---|---|
| **realignment factor** $\beta$ | 重新對齊係數 | The linearized gain telling you how much each injected pulse "pulls back" the phase; sets the discrete-loop stability range $0<\beta<2$ and the noise-shaping corner $\approx\beta f_{ref}/2\pi$. | [subharmonic_injection](/06_design_insights/subharmonic_injection) |
| **impulse-train locking** | 脈衝列鎖定 | When injection is a periodic pulse train (not a continuous sinusoid), the lock range is set by the interaction between the pulse's $N$-th harmonic amplitude and the ISF's fundamental — the core mechanism of subharmonic injection. | [subharmonic_injection](/06_design_insights/subharmonic_injection) |
| **washboard potential** (tilted washboard) | 傾斜搓衣板位能 | Rewrites the Adler equation as a particle rolling in a tilted periodic potential $U(\theta)$; locking = rolling into the nearest well, a cycle slip = thermal noise kicking the particle over the neighboring barrier. | [lab_36](/04_simulation_labs/lab_36_lock_acquisition) |
| **ILFD (Injection-Locked Frequency Divider)** | 注入鎖定除頻器 | Not a digital division circuit at all — it's simply an oscillator already running at $f_0=f_{inj}/N$, locked via the ISF's $N$-th harmonic. | [injection_locked_division](/06_design_insights/injection_locked_division) |
| **dual-Dirac model** | 雙 Dirac 模型 | The industry-standard approximation: any bounded-shape DJ is modeled as two Dirac deltas (split left/right), combined with the Gaussian RJ's $Q$-function tail integral to get $\text{TJ(BER)}$. | [dj_dual_dirac](/06_design_insights/dj_dual_dirac) |
| **ADEV / Allan deviation** | 亞倫偏差 | The time-domain stability metric used by the clock/frequency-standards community: the square root of the two-sample variance; its log–log slope tells white/flicker/random-walk FM noise types apart at a glance. | [allan_variance](/02_foundations/allan_variance) |
| **sub-sampling PLL** | 次取樣鎖相環 | Uses the reference edge to directly sample the VCO sinusoid as the phase detector; the divider disappears entirely from the noise path, so charge-pump noise is no longer amplified by $\times N^2$. | [sampling_pll](/06_design_insights/sampling_pll) |
| **Lorentzian linewidth** | 洛倫茲線寬 | The autocorrelation of a phase random walk decays exponentially; Wiener–Khinchin turns that into a finite-height, finite-width bell-shaped spectrum — $1/f^2$ is just its far-from-center asymptote. | [lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth) |
| **cycle slip / Kramers escape** | 週期滑動／克拉默逃逸 | The rare event where noise kicks the locked phase a full turn ($2\pi$) over the washboard barrier; the escape rate follows the Kramers formula (external literature). | [lab_36](/04_simulation_labs/lab_36_lock_acquisition) |
| **cross-correlation measurement** | 交叉相關量測法 | Correlates two independent measurement channels so their uncorrelated instrument floors are suppressed by $1/\sqrt{M}$, yielding a cleaner $\mathcal{L}(f)$ than a single channel. | [measurement_and_spurs](/06_design_insights/measurement_and_spurs) |
| **polyphase filter** | 多相濾波器 | An RC-CR network that produces a $90^\circ$ phase shift at $\omega=1/RC$ to generate I/Q; cascading stages widens the bandwidth, and it does not actively generate new close-in phase noise. | [quadrature_and_coupled_oscillators](/06_design_insights/quadrature_and_coupled_oscillators) |
| **FOM / FOM$_{jitter}$** | 品質指標／jitter 版品質指標 | FOM combines $\mathcal{L}$, $(f_0/\Delta f)^2$, and $P$ into a single number comparable across topologies, with a theoretical ceiling $173.8-10\log_{10}F_{eff}$; FOM$_{jitter}$ replaces $\mathcal{L}$ with the raw $\sigma_t$. | [fom_limit](/06_design_insights/fom_limit) / [pll_noise_budget](/06_design_insights/pll_noise_budget) |
| **$K_{push}$** (supply pushing) | 電源推移係數 | How much the oscillation frequency is pushed per 1 V of supply variation ($\partial f_0/\partial V_{DD}$), mathematically exactly parallel to $K_{VCO}$; ideally zero. | [varactor_tuning_supply_pushing](/06_design_insights/varactor_tuning_supply_pushing) |
| **TDC (Time-to-Digital Converter)** | 時間數位轉換器 | Quantizes the time difference between two edges into an integer; the finite resolution $\Delta t_{res}$ becomes the ADPLL's in-band quantization noise. | [adpll_tdc_dco](/06_design_insights/adpll_tdc_dco) |
| **DCO (Digitally Controlled Oscillator)** | 數位控制振盪器 | Tunes frequency with a bank of switched capacitors rather than a continuous varactor voltage; the finite frequency resolution $\Delta f_{res}$ becomes out-of-band quantization noise. | [adpll_tdc_dco](/06_design_insights/adpll_tdc_dco) |
| **JTOL (jitter tolerance)** | 抖動容忍度 | The spec curve $(\text{UI}-\text{TJ}_{eye})/\lvert1-H(f)\rvert$ describing how much input jitter a CDR loop can track before eating into the eye margin, with different slopes at low/mid/high frequency. | [cdr_bang_bang_jtol](/06_design_insights/cdr_bang_bang_jtol) |
| **BBPD / Alexander PD** | 二元（bang-bang）相位偵測器 | A phase detector that outputs only early/late $\text{sign}(\Delta t)$ with no linear gain; the loop bandwidth is in fact set by the jitter's rms value. | [cdr_bang_bang_jtol](/06_design_insights/cdr_bang_bang_jtol) |
| **FOM$_T$** (tuning-range-normalized FOM) | 調諧範圍正規化品質指標 | Adds a $20\log_{10}(\text{TR}\%/10)$ correction to FOM so a wide-tuning-range design is not penalized for having "the same FOM"; an external empirical convention, not an identity. | [design_recipe](/06_design_insights/design_recipe) |
| **design recipe** (spec-driven design) | 規格驅動設計配方 | The 7-step standard flow that works backward from a spec ($\mathcal{L}$, $P$, tuning range) to topology choice, tank component values, and bias current. | [design_recipe](/06_design_insights/design_recipe) |

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
