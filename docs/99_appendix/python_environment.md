---
title: Python 環境與模擬程式庫 Python Environment
description: 如何建環境（Python 3.12、numpy/scipy/matplotlib、CJK 字型 Heiti TC）、目錄結構、跑 run_all_sims.py、common 模組與函式一覽、固定 rng seed 的 reproducibility。
---

# Python 環境與模擬程式庫 Python Environment

> **See also**：[notation](/00_overview/notation)（函式參數對應的符號）、各模擬 lab 頁（如 [lab_01](/04_simulation_labs/lab_01_sinusoidal_oscillator)）會引用這裡的 `common/` 函式｜跑全部圖：`python scripts/run_all_sims.py`

本站所有圖都是用 Python 的**教學用 toy model**（pedagogical toy model，非 transistor-level）
跑出來的。這頁告訴你：怎麼把環境建起來、目錄長什麼樣、一鍵重跑全部圖、以及 `common/`
裡每個模組與函式在做什麼。所有函式名稱都對應**真實存在**的程式碼，可以直接 import 來驗算。

> **設計哲學**：模擬不是為了「像真電路」，而是為了**把公式變成可以動手摸的數字與圖**。
> 每個 lab 都把一條 ISF 公式拆成最小可跑的程式，固定亂數種子讓結果**完全可重現**。

---

## 1. 建環境

需要 **Python 3.12**，三個套件即可：

```python
# 建議用虛擬環境
# python3.12 -m venv .venv && source .venv/bin/activate
# 然後安裝：
#   pip install numpy scipy matplotlib
```

| 套件 | 版本建議 | 用途 |
|---|---|---|
| `numpy` | 1.26+ | 向量化數值運算、FFT、亂數 |
| `scipy` | 1.11+ | `scipy.signal.welch`（PSD 估計）、積分、插值 |
| `matplotlib` | 3.8+ | 出圖到 `static/figures/` |

**為什麼只要三個套件**：刻意保持最小相依，讓任何人都能在乾淨的 Python 3.12 上一行裝完、
一鍵重現所有圖。沒有用到深度學習框架或電路模擬器（SPICE 等）——再次強調，這是 toy model。

---

## 2. CJK 字型（Heiti TC）

圖上有中文標籤（軸名、圖例），matplotlib 預設字型不含中文會出現「豆腐方塊」。本站在 macOS 上
用系統內建的 **Heiti TC（黑體-繁）**：

```python
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Heiti TC"     # 繁體中文字型 (macOS 內建)
plt.rcParams["axes.unicode_minus"] = False    # 避免負號變方塊
```

- **`axes.unicode_minus=False`** 很關鍵：matplotlib 預設用 Unicode 減號 U+2212，很多字型缺這個
  glyph，會讓「$-100$ dBc/Hz」的負號變方塊；設成 `False` 改用 ASCII 連字號就正常。
- **非 macOS 平台**：把 `"Heiti TC"` 換成系統有的 CJK 字型（如 Linux 的 `"Noto Sans CJK TC"`、
  Windows 的 `"Microsoft JhengHei"`）。`TODO: manual verification needed` —— 跨平台字型名稱請依
  實際系統 `fc-list` 結果調整。

---

## 3. 目錄結構

```python
# simulations/
#   common/
#     isf_utils.py            # ISF 形狀、傅立葉、impulse->phase
#     noise_utils.py          # 噪訊產生、PSD、jitter 積分、dBc/Hz
#     oscillator_models.py    # toy 振盪器、ISF 萃取、ring edge times
#   lab_01_sinusoidal_oscillator.py
#   lab_02_lc_oscillator_isf.py
#   lab_03_ring_oscillator_toy_model.py
#   lab_04_impulse_injection_sweep.py
#   lab_05_fourier_decomposition.py
#   lab_06_white_noise_phase_noise.py
#   lab_07_flicker_upconversion.py
#   lab_08_jitter_integration.py
# scripts/
#   run_all_sims.py           # 一鍵重跑全部 lab，產生所有圖
# static/figures/             # 產出的 .png（網站用 /figures/<name>.png 引用）
```

- **`common/`** 放可重用的核心函式，三個 lab 共用；**各 lab** 只負責「擺參數、呼叫 common、出圖」。
  這樣公式只實作一次，任何 lab 改參數都用同一份權威實作。
- **圖的輸出**一律落在 `static/figures/`，網站頁面用 `![alt](/figures/<name>.png)` 引用
  （見 [authoring spec 第 4 節] 的圖表清單）。

---

## 4. 一鍵重跑全部圖

```python
# 在專案根目錄執行：
#   python scripts/run_all_sims.py
```

`scripts/run_all_sims.py` 會依序跑 lab_01 ~ lab_08 的 `main()` / `fig_*()`，把全部 14 張 PNG
重新產生到 `static/figures/`。要重現網站上的任何一張圖，這一行就夠。各圖對應的 script 與函式：

| 圖檔 | script | function |
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

## 5. `common/` 模組與函式一覽

以下函式名稱與簽名取自作者規範第 5 節，是**真實存在**的 API，請勿杜撰其他函式。

### 5.1 `simulations/common/isf_utils.py` —— ISF 的形狀與相位轉換

| 函式 | 做什麼 | 對應公式 |
|---|---|---|
| `wrap_phase` | 把相位包進 $[-\pi,\pi]$ 或 $[0,2\pi)$ | — |
| `gamma_symmetric` | 對稱波形的 ISF（$c_0\approx0$） | [P1] Eq.(12) |
| `gamma_asymmetric(alpha)` | 不對稱 ISF（$c_0\neq0$，$\alpha$ 控制不對稱度） | flicker upconversion |
| `gamma_lc_ideal` | 理想 LC 的 ISF $=-\sin\theta$ | $\Gamma=-\sin\theta$ |
| `gamma_triangular(n_stages)` | ring 的三角形 ISF（敏感度集中在 transition） | [P2] Fig. 5 |
| `impulse_to_phase_step(dq, gamma, qmax)` | $\Delta\phi=\Gamma\,\Delta q/q_{max}$ | [P1] Eq.(10)/(11) |
| `integrate_phase_from_noise(t, i, gamma_vals, qmax)` | 把 noise 電流積分成相位 | [P1] Eq.(11) |
| `apply_isf_weighting(t, i, gamma_func, qmax, omega0)` | 對 noise 乘上 $\Gamma(\omega_0 t)$ 的權重 | [P1] Eq.(11) |
| `compute_fourier_coefficients(theta, gamma, n_harmonics)` | 回傳 `(a0, a, b, c, phase)` | [P1] Eq.(12) |
| `reconstruct_from_fourier` | 由 $c_n,\theta_n$ 重建 $\Gamma$ | [P1] Eq.(12) |
| `gamma_rms(theta, gamma)` | 數值算 $\Gamma_{rms}$ | [P1] Eq.(20) |
| `effective_isf(gamma, alpha)` | $\Gamma_{eff}=\Gamma\cdot\alpha$（cyclostationary） | [P1] cyclostationary 節 |

對應頁：[isf_definition](/03_isf_core_theory/isf_definition)、
[fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf)、
[effective_isf](/03_isf_core_theory/effective_isf)。

### 5.2 `simulations/common/noise_utils.py` —— 噪訊、PSD、jitter

| 函式 | 做什麼 | 對應公式 |
|---|---|---|
| `white_noise(n, psd, fs, rng)` | 產生白噪序列（指定單邊 PSD） | $S_i=\overline{i_n^2}/\Delta f$ |
| `flicker_noise(n, fs, k_flicker, ...)` | 產生 $1/f$ flicker 噪訊 | [P1] Eq.(22) |
| `estimate_psd(x, fs, nperseg)` | 用 Welch 法估 PSD | Wiener–Khinchin |
| `phase_psd_to_l_dbc_per_hz(s_phi)` | $\mathcal{L}=10\log_{10}(\tfrac12 S_\phi)$ | $\mathcal{L}\approx\frac12 S_\phi$ |
| `phase_to_time_error(phi, f0)` | $\Delta t=\Delta\phi/(2\pi f_0)$ | spec Eq.(17) |
| `integrate_rms_jitter(f, l_dbc, f0, fmin, fmax)` | 回傳 `(sigma_t, sigma_phi)` | spec Eq.(18)/(19) |
| `leeson_one_over_f2(f, Lref, fref)` | 產生 $1/f^2$ skirt 形狀 | Leeson（對照用） |

對應頁：[psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter)、
[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)、
[numerical_feeling](/04_simulation_labs/numerical_feeling)。

### 5.3 `simulations/common/oscillator_models.py` —— toy 振盪器與 ISF 萃取

| 函式 | 做什麼 | 對應頁 |
|---|---|---|
| `sinusoidal_oscillator` | 最簡正弦振盪器（建立 limit cycle 直覺） | [lab_01](/04_simulation_labs/lab_01_sinusoidal_oscillator) |
| `simulate_lc(...)` | toy LC 振盪器 state-space 模擬 | [lab_02](/04_simulation_labs/lab_02_lc_oscillator_toy_model) |
| `excess_phase` | 從波形萃取 excess phase $\phi(t)$ | [P1] Eq.(1) |
| `extract_isf_by_injection(...)` | 在不同相位注入小電荷、量相位跳變，**反推 ISF** | [lab_04](/04_simulation_labs/lab_04_impulse_injection_sweep) |
| `ring_edge_times` | 算 ring 各 edge 的時刻 | [lab_03](/04_simulation_labs/lab_03_ring_oscillator_toy_model) |
| `accumulated_jitter_curve` | 產生 $\sigma_{\Delta t}$ vs $\Delta t$ 曲線 | [P2] Eq.(8) |
| `phase_to_time` | 相位 → 時間（edge 位置） | spec Eq.(17) |

> 全部都是 **toy / 概念模型**（toy model，非 transistor-level）。它們重現的是**公式的行為與
> scaling**，不是真實電晶體電路的精確數值。

---

## 6. Reproducibility（固定 rng seed）

所有用到亂數的 lab（白噪、flicker、jitter 累積）都用 **NumPy 的新式亂數產生器並固定 seed**，
讓任何人重跑都得到**逐位元相同**的圖：

```python
import numpy as np
rng = np.random.default_rng(seed=12345)   # 固定種子 -> 完全可重現
i_n = white_noise(n=2**16, psd=1e-24, fs=fs, rng=rng)   # 傳入同一個 rng
```

- **為什麼用 `default_rng(seed)` 而不是舊的 `np.random.seed`**：新式 `Generator` 物件式 API
  讓亂數狀態**顯式傳遞**（`rng` 當參數丟進函式），避免全域狀態被別處偷改，是 reproducibility 的
  最佳實務。
- **驗證手感**：固定 seed 後，[lab_08](/04_simulation_labs/lab_08_jitter_integration) 的數值積分
  jitter 會穩定落在解析值 $\sigma_t=447.9$ fs、$\sigma_\phi=14.07$ mrad（canonical 例 C）附近，
  與理論完全一致。
- **想看不同實現**：改 seed（如 `default_rng(1)`、`default_rng(2)`）可看 Monte-Carlo 抖動範圍；
  但網站上釘住的圖一律用固定 seed。

---

## 7. 一行驗算示範（把公式變數字）

把前面的環境串起來，下面這段不需要任何 lab script，只靠 `common/` 就能重現 canonical 例 A
（$q_{max}=1$ pC、$\Delta q=1$ fC、$\Gamma=0.5$、$f_0=5$ GHz）：

```python
from simulations.common.isf_utils import impulse_to_phase_step
from simulations.common.noise_utils import phase_to_time_error

dphi = impulse_to_phase_step(delta_q=1e-15, gamma_value=0.5, qmax=1e-12)
dt   = phase_to_time_error(dphi, f0=5e9)
print(dphi, "rad", dt * 1e15, "fs")   # -> 0.0005 rad  15.92 fs
```

得到 $\Delta\phi=5\times10^{-4}$ rad、$\Delta t=15.9$ fs，與
[impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift)（例 A）一致。

## 重點回顧

- Python 3.12 + `numpy`/`scipy`/`matplotlib`，CJK 用 `Heiti TC` 並關閉 `unicode_minus`。
- `common/` 三模組（`isf_utils`、`noise_utils`、`oscillator_models`）放權威實作；各 lab 只擺參數。
- `python scripts/run_all_sims.py` 一鍵重產 14 張圖到 `static/figures/`。
- 全部是 toy model；用固定 `default_rng(seed)` 保證逐位元可重現。

## 延伸閱讀

- 數值口算與驗算：[numerical_feeling](/04_simulation_labs/numerical_feeling)
- 數學工具箱：[math_identities](/99_appendix/math_identities)
- 詞彙表：[glossary](/99_appendix/glossary)
- 公式索引：[equation_index](/01_paper_map/equation_index)
