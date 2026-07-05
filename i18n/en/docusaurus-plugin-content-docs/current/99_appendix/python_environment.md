---
title: Python 環境與模擬程式庫 Python Environment
description: How to set up the environment (Python 3.12, numpy/scipy/matplotlib, CJK font Heiti TC), directory layout, running run_all_sims.py, an overview of the common module and its functions, and reproducibility via fixed rng seed.
---

> **β**: This English translation is in beta — the Traditional-Chinese original is the authoritative version.

# Python 環境與模擬程式庫 Python Environment

> **See also**: [notation](/00_overview/notation) (symbol conventions for function arguments), the simulation lab pages (e.g. [lab_01](/04_simulation_labs/lab_01_sinusoidal_oscillator)) reference the `common/` functions here | to regenerate all figures: `python scripts/run_all_sims.py`

Every figure on this site is produced with a Python **pedagogical toy model**
(not transistor-level). This page covers: how to set up the environment, what the directory layout
looks like, how to regenerate all figures with one command, and what each module and function in
`common/` does. All function names correspond to **actual existing** code, and can be imported
directly to verify.

> **Design philosophy**: the simulations aren't meant to "look like a real circuit" — they exist to
> **turn formulas into numbers and plots you can touch**.
> Each lab reduces one ISF formula to the smallest runnable program, with a fixed random seed so
> results are **fully reproducible**.

---

## 1. Setting up the environment

Requires **Python 3.12**; only three packages are needed:

```python
# Recommended: use a virtual environment
# python3.12 -m venv .venv && source .venv/bin/activate
# Then install:
#   pip install numpy scipy matplotlib
```

| Package | Recommended version | Purpose |
|---|---|---|
| `numpy` | 1.26+ | vectorized numerics, FFT, random number generation |
| `scipy` | 1.11+ | `scipy.signal.welch` (PSD estimation), integration, interpolation |
| `matplotlib` | 3.8+ | render figures to `static/figures/` |

**Why only three packages**: dependencies are kept deliberately minimal, so anyone can install
everything with one line on a clean Python 3.12 install and reproduce every figure with one
command. No deep-learning framework or circuit simulator (SPICE, etc.) is used — again, this is a
toy model.

---

## 2. CJK font (Heiti TC)

Figures carry Chinese labels (axis names, legends); matplotlib's default font doesn't cover Chinese
and renders "tofu boxes" instead. This site uses macOS's built-in **Heiti TC (黑體-繁)**:

```python
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Heiti TC"     # Traditional Chinese font (built into macOS)
plt.rcParams["axes.unicode_minus"] = False    # avoid minus sign turning into a box
```

- **`axes.unicode_minus=False`** is critical: matplotlib defaults to the Unicode minus sign
  U+2212, which many fonts lack the glyph for, turning the minus sign in "$-100$ dBc/Hz" into a
  box; setting it to `False` switches to the ASCII hyphen and fixes this.
- **Non-macOS platforms**: replace `"Heiti TC"` with a CJK font available on your system (e.g.
  `"Noto Sans CJK TC"` on Linux, `"Microsoft JhengHei"` on Windows). `TODO: manual verification
  needed` — adjust the cross-platform font name per your system's actual `fc-list` output.

---

## 3. Directory layout

```python
# simulations/
#   common/
#     isf_utils.py            # ISF shape, Fourier decomposition, impulse->phase
#     noise_utils.py          # noise generation, PSD, jitter integration, dBc/Hz
#     oscillator_models.py    # toy oscillator, ISF extraction, ring edge times
#   lab_01_sinusoidal_oscillator.py
#   lab_02_lc_oscillator_isf.py
#   lab_03_ring_oscillator_toy_model.py
#   lab_04_impulse_injection_sweep.py
#   lab_05_fourier_decomposition.py
#   lab_06_white_noise_phase_noise.py
#   lab_07_flicker_upconversion.py
#   lab_08_jitter_integration.py
# scripts/
#   run_all_sims.py           # regenerate all lab figures with one command
# static/figures/             # generated .png files (site references them as /figures/<name>.png)
```

- **`common/`** holds reusable core functions, shared across labs; **each lab** is responsible only
  for "setting parameters, calling common, plotting." This way each formula is implemented once,
  and any lab that changes parameters uses the same authoritative implementation.
- **Figure output** always lands in `static/figures/`; site pages reference it with
  `![alt](/figures/<name>.png)` (see the figure list in [authoring spec section 4]).

---

## 4. Regenerate all figures with one command

```python
# Run from the project root:
#   python scripts/run_all_sims.py
```

`scripts/run_all_sims.py` runs the `main()` / `fig_*()` of lab_01 through lab_08 in sequence,
regenerating all 14 PNGs into `static/figures/`. To reproduce any figure on the site, this one
command suffices. The script and function behind each figure:

| Figure file | script | function |
|---|---|---|
| `limit_cycle_phase_amplitude.png` | `lab_01_sinusoidal_oscillator.py` | `fig_limit_cycle` |
| `waveform_with_impulse_markers.png` | `lab_01_sinusoidal_oscillator.py` | `fig_impulse_markers` |
| `lc_waveform_and_isf.png` | `lab_02_lc_oscillator_isf.py` | `main` |
| `ring_oscillator_timing_noise_accumulation.png` | `lab_03_ring_oscillator_toy_model.py` | `fig_accumulation` |
| `lc_vs_ring_isf_comparison.png` | `lab_03_ring_oscillator_toy_model.py` | `fig_lc_vs_ring_isf` |
| `sinusoidal_impulse_phase_sweep.png` | `lab_04_impulse_injection_sweep.py` | `fig_isf_sweep` |
| `isf_impulse_sweep_sinusoidal.png` | `lab_04_impulse_injection_sweep.py` | `fig_isf_sweep` |
| `lti_vs_ltv_impulse_response.png` | `lab_04_impulse_injection_sweep.py` | `fig_lti_vs_ltv` |
| `isf_fourier_reconstruction.png` | `lab_05_fourier_decomposition.py` | `fig_reconstruction` |
| `isf_fourier_coefficients.png` | `lab_05_fourier_decomposition.py` | `fig_coefficients` |
| `symmetric_vs_asymmetric_isf_c0.png` | `lab_05_fourier_decomposition.py` | `fig_symmetric_vs_asymmetric` |
| `white_noise_phase_noise_psd.png` | `lab_06_white_noise_phase_noise.py` | `main` |
| `flicker_upconversion_symmetric_vs_asymmetric.png` | `lab_07_flicker_upconversion.py` | `main` |
| `phase_noise_to_jitter_integration.png` | `lab_08_jitter_integration.py` | `main` |

---

## 5. Overview of `common/` modules and functions

The function names and signatures below are taken from section 5 of the authoring spec; they are
**actual existing** APIs — do not fabricate other functions.

### 5.1 `simulations/common/isf_utils.py` — ISF shape and phase conversion

| Function | What it does | Corresponding formula |
|---|---|---|
| `wrap_phase` | wrap phase into $[-\pi,\pi]$ or $[0,2\pi)$ | — |
| `gamma_symmetric` | ISF of a symmetric waveform ($c_0\approx0$) | [P1] Eq.(12) |
| `gamma_asymmetric(alpha)` | asymmetric ISF ($c_0\neq0$, $\alpha$ controls the degree of asymmetry) | flicker upconversion |
| `gamma_lc_ideal` | ISF of an ideal LC, $=-\sin\theta$ | $\Gamma=-\sin\theta$ |
| `gamma_triangular(n_stages)` | triangular ISF of a ring (sensitivity concentrated at the transition) | [P2] Fig. 5 |
| `impulse_to_phase_step(dq, gamma, qmax)` | $\Delta\phi=\Gamma\,\Delta q/q_{max}$ | [P1] Eq.(10)/(11) |
| `integrate_phase_from_noise(t, i, gamma_vals, qmax)` | integrate a noise current into phase | [P1] Eq.(11) |
| `apply_isf_weighting(t, i, gamma_func, qmax, omega0)` | weight noise by $\Gamma(\omega_0 t)$ | [P1] Eq.(11) |
| `compute_fourier_coefficients(theta, gamma, n_harmonics)` | returns `(a0, a, b, c, phase)` | [P1] Eq.(12) |
| `reconstruct_from_fourier` | reconstruct $\Gamma$ from $c_n,\theta_n$ | [P1] Eq.(12) |
| `gamma_rms(theta, gamma)` | numerically compute $\Gamma_{rms}$ | [P1] Eq.(20) |
| `effective_isf(gamma, alpha)` | $\Gamma_{eff}=\Gamma\cdot\alpha$ (cyclostationary) | [P1] cyclostationary section |

Corresponding pages: [isf_definition](/03_isf_core_theory/isf_definition),
[fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf),
[effective_isf](/03_isf_core_theory/effective_isf).

### 5.2 `simulations/common/noise_utils.py` — noise, PSD, jitter

| Function | What it does | Corresponding formula |
|---|---|---|
| `white_noise(n, psd, fs, rng)` | generate a white-noise sequence (given single-sided PSD) | $S_i=\overline{i_n^2}/\Delta f$ |
| `flicker_noise(n, fs, k_flicker, ...)` | generate $1/f$ flicker noise | [P1] Eq.(22) |
| `estimate_psd(x, fs, nperseg)` | estimate PSD via Welch's method | Wiener–Khinchin |
| `phase_psd_to_l_dbc_per_hz(s_phi)` | $\mathcal{L}=10\log_{10}(\tfrac12 S_\phi)$ | $\mathcal{L}\approx\frac12 S_\phi$ |
| `phase_to_time_error(phi, f0)` | $\Delta t=\Delta\phi/(2\pi f_0)$ | spec Eq.(17) |
| `integrate_rms_jitter(f, l_dbc, f0, fmin, fmax)` | returns `(sigma_t, sigma_phi)` | spec Eq.(18)/(19) |
| `leeson_one_over_f2(f, Lref, fref)` | generate a $1/f^2$ skirt shape | Leeson (for comparison) |

Corresponding pages: [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter),
[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise),
[numerical_feeling](/04_simulation_labs/numerical_feeling).

### 5.3 `simulations/common/oscillator_models.py` — toy oscillators and ISF extraction

| Function | What it does | Corresponding page |
|---|---|---|
| `sinusoidal_oscillator` | simplest sinusoidal oscillator (builds limit-cycle intuition) | [lab_01](/04_simulation_labs/lab_01_sinusoidal_oscillator) |
| `simulate_lc(...)` | toy LC oscillator state-space simulation | [lab_02](/04_simulation_labs/lab_02_lc_oscillator_toy_model) |
| `excess_phase` | extract excess phase $\phi(t)$ from a waveform | [P1] Eq.(1) |
| `extract_isf_by_injection(...)` | inject a small charge at different phases, measure the phase jump, **back out the ISF** | [lab_04](/04_simulation_labs/lab_04_impulse_injection_sweep) |
| `ring_edge_times` | compute the timing of each edge in a ring | [lab_03](/04_simulation_labs/lab_03_ring_oscillator_toy_model) |
| `accumulated_jitter_curve` | generate a $\sigma_{\Delta t}$ vs $\Delta t$ curve | [P2] Eq.(8) |
| `phase_to_time` | phase → time (edge position) | spec Eq.(17) |

> All of these are **toy / conceptual models** (toy model, not transistor-level). What they
> reproduce is the **behavior and scaling of the formulas**, not precise numerical values of a real
> transistor circuit.

---

## 6. Reproducibility (fixed rng seed)

Every lab that uses randomness (white noise, flicker, jitter accumulation) uses **NumPy's modern
random generator with a fixed seed**, so that anyone re-running it gets a **bit-identical** figure:

```python
import numpy as np
rng = np.random.default_rng(seed=12345)   # fixed seed -> fully reproducible
i_n = white_noise(n=2**16, psd=1e-24, fs=fs, rng=rng)   # pass in the same rng
```

- **Why `default_rng(seed)` instead of the legacy `np.random.seed`**: the modern `Generator`
  object-based API passes random state **explicitly** (`rng` as an argument into functions),
  avoiding global state being silently mutated elsewhere — this is best practice for
  reproducibility.
- **Sanity check**: with a fixed seed, the numerically integrated jitter in
  [lab_08](/04_simulation_labs/lab_08_jitter_integration) settles stably near the analytical values
  $\sigma_t=447.9$ fs, $\sigma_\phi=14.07$ mrad (canonical example C), fully consistent with theory.
- **To see different realizations**: change the seed (e.g. `default_rng(1)`, `default_rng(2)`) to
  see the Monte-Carlo spread; but the figures pinned on the site always use the fixed seed.

---

## 7. One-line worked check (turning a formula into a number)

Chaining together everything above, the snippet below needs no lab script at all — using only
`common/` it reproduces canonical example A
($q_{max}=1$ pC, $\Delta q=1$ fC, $\Gamma=0.5$, $f_0=5$ GHz):

```python
from simulations.common.isf_utils import impulse_to_phase_step
from simulations.common.noise_utils import phase_to_time_error

dphi = impulse_to_phase_step(delta_q=1e-15, gamma_value=0.5, qmax=1e-12)
dt   = phase_to_time_error(dphi, f0=5e9)
print(dphi, "rad", dt * 1e15, "fs")   # -> 0.0005 rad  15.92 fs
```

This gives $\Delta\phi=5\times10^{-4}$ rad, $\Delta t=15.9$ fs, consistent with
[impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift) (example A).

---

## 8. 📓 Download Jupyter notebooks

The seven mainline labs each have a corresponding Jupyter notebook (interactive notebook, runnable
cell-by-cell with parameters you can change and re-run) available for direct download, to play with
the formulas offline as numbers and figures:

| Notebook (click to download .ipynb) | Contents | Corresponding page |
|---|---|---|
| [lab_01_sinusoidal_oscillator](/notebooks/lab_01_sinusoidal_oscillator.ipynb) | limit cycle, phase (tangential) vs amplitude (radial) perturbation, impulse injection timing | [lab_01](/04_simulation_labs/lab_01_sinusoidal_oscillator) |
| [lab_05_fourier_isf](/notebooks/lab_05_fourier_isf.ipynb) | ISF Fourier coefficients $c_n$, Parseval verification, $c_0$ and symmetry | [lab_05](/04_simulation_labs/lab_05_isf_fourier_coefficients) |
| [lab_06_white_noise_phase_noise](/notebooks/lab_06_white_noise_phase_noise.ipynb) | end-to-end white noise $\to$ $1/f^2$ phase noise simulation vs theoretical line | [lab_06](/04_simulation_labs/lab_06_white_noise_phase_noise) |
| [lab_08_jitter_integration](/notebooks/lab_08_jitter_integration.ipynb) | integrating $\mathcal{L}(f)$ into rms jitter (canonical example C) | [lab_08](/04_simulation_labs/lab_08_jitter_integration) |
| [lab_18_lorentzian](/notebooks/lab_18_lorentzian.ipynb) | phase random walk $\to$ carrier Lorentzian lineshape and 3-dB linewidth | [lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth) |
| [lab_22_capstone_lc_end_to_end](/notebooks/lab_22_capstone_lc_end_to_end.ipynb) | full ideal-LC chain: $\Gamma\to\Gamma_{rms}\to S_\phi\to$ linewidth $\to\sigma_t\to$ BER | [capstone](/03_isf_core_theory/capstone_lc_end_to_end) |
| [lab_24_jitter_kernels](/notebooks/lab_24_jitter_kernels.ipynb) | TIE / period / cycle-to-cycle: three jitter weighting kernels + Monte-Carlo verification | [jitter_kernels](/02_foundations/jitter_kernels) |

**How to run it**: the notebook imports modules from `simulations/common`, so you first need to
`git clone https://github.com/gmcycle7/isf-teaching-site.git`, and then run the downloaded .ipynb
from anywhere within the repo directory tree (each notebook's setup cell automatically searches
parent directories for `simulations/common` and adds it to `sys.path`). Dependencies are the same
as in section 1, `pip install numpy scipy matplotlib`, plus `pip install jupyter`, then open with
`jupyter lab`.

> **Honesty note**: these notebooks are **generated snapshots** that `scripts/make_notebooks.py`
> automatically produces from the corresponding `simulations/lab_*.py` — they are not hand-written;
> the authoritative version is always the lab script in the repo. After a lab is updated, running
> `python scripts/make_notebooks.py` regenerates all notebooks.
> There are exactly two deliberate differences from the original script: `savefig` is replaced with
> inline display within the notebook (not written to `static/figures/`), and the path setup is
> handled by the setup cell automatically locating the repo root
> (the original script uses `__file__` for this).

## Key takeaways

- Python 3.12 + `numpy`/`scipy`/`matplotlib`; use `Heiti TC` for CJK and disable `unicode_minus`.
- The three `common/` modules (`isf_utils`, `noise_utils`, `oscillator_models`) hold the
  authoritative implementation; each lab only sets parameters.
- `python scripts/run_all_sims.py` regenerates all 14 figures into `static/figures/` in one command.
- Everything is a toy model; a fixed `default_rng(seed)` guarantees bit-identical reproducibility.
- The seven mainline labs have downloadable Jupyter notebooks (section 8), automatically produced
  as generated snapshots by `scripts/make_notebooks.py`.

## Further reading

- Numerical intuition and sanity checks: [numerical_feeling](/04_simulation_labs/numerical_feeling)
- Math toolbox: [math_identities](/99_appendix/math_identities)
- Glossary: [glossary](/99_appendix/glossary)
- Equation index: [equation_index](/01_paper_map/equation_index)
