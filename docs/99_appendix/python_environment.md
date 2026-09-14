---
title: Python 環境與模擬程式庫 Python Environment
description: 如何建環境（Python 3.12、numpy/scipy/matplotlib、CJK 字型自動偵測）、目錄結構、跑 run_all_sims.py、common 七模組與函式一覽、固定 rng seed 的 reproducibility。
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

## 2. CJK 字型（自動偵測，非寫死）

圖上有中文標籤（軸名、圖例），matplotlib 預設字型不含中文會出現「豆腐方塊」。本站**不是**寫死
單一字型名稱，而是在 `simulations/common/plot_utils.py` 用 `matplotlib.font_manager` 掃描機器上
**實際安裝**的字型，依偏好清單挑第一個存在的（`import` 在 `plot_utils.py:24`，掃描／挑選邏輯在
`plot_utils.py:26–29`）：

```python
import matplotlib.font_manager as _fm

_available = {f.name for f in _fm.fontManager.ttflist}
_cjk_prefs = ["Heiti TC", "Arial Unicode MS", "STHeiti", "Hiragino Sans GB",
              "Songti SC", "PingFang TC"]
_cjk_font = next((f for f in _cjk_prefs if f in _available), None)

plt.rcParams["font.family"] = ([_cjk_font] if _cjk_font else []) + ["DejaVu Sans", "sans-serif"]
plt.rcParams["axes.unicode_minus"] = False
```

- **`_available`**：`_fm.fontManager.ttflist` 是 matplotlib 啟動時掃到的所有已安裝字型物件；
  取 `.name` 集合起來，就是「這台機器實際有的字型名稱」。
- **`_cjk_prefs`**：6 個常見 macOS 中文字型的優先順序清單（Heiti TC、Arial Unicode MS、
  STHeiti、Hiragino Sans GB、Songti SC、PingFang TC）。`_cjk_font = next(...)` 依序挑
  **第一個「在偏好清單裡、且這台機器真的有」**的字型；六個都沒有就回傳 `None`。
- **優雅降級（不是寫死 Heiti TC）**：`([_cjk_font] if _cjk_font else [])` 在找不到任何 CJK 字型
  時變成空列表，`font.family` 就只剩 `["DejaVu Sans", "sans-serif"]`——matplotlib 內建、
  不含 CJK glyph 的字型；此時圖仍會**正常產生**（不會噴例外），只是中文標籤會變成方塊。
- **`axes.unicode_minus=False`** 仍然關鍵：matplotlib 預設用 Unicode 減號 U+2212，很多字型缺這個
  glyph，會讓「$-100$ dBc/Hz」的負號變方塊；設成 `False` 改用 ASCII 連字號就正常。
- **非 macOS 平台**：`_cjk_prefs` 目前只列了 6 個 macOS 字型；在 Linux／Windows 上要讓中文標籤
  正常顯示，把系統實際有的 CJK 字型（如 Linux 的 `Noto Sans CJK TC`、Windows 的
  `Microsoft JhengHei`）加進 `_cjk_prefs` 清單最前面即可——探測邏輯會自動挑到它，不需要改
  任何其他程式碼。

---

## 3. 目錄結構

```python
# simulations/
#   common/
#     isf_utils.py            # ISF 形狀、傅立葉、impulse->phase
#     noise_utils.py          # 噪訊產生、PSD、jitter 積分、dBc/Hz
#     oscillator_models.py    # toy 振盪器、ISF 萃取、ring edge times
#     pll_utils.py            # type-II PLL/CDR loop transfer（H_lp/H_hp）、loop 設計
#     serdes_utils.py         # SerDes eye/BER（Q 函式、bathtub、眼圖 traces）
#     signal_utils.py         # 通用訊號工具（time axis、Hilbert phase、zero-crossing、jitter 核）
#     plot_utils.py           # 存圖到 static/figures/、CJK 字型自動偵測（見第 2 節）
#   lab_01_sinusoidal_oscillator.py
#   lab_02_lc_toy_model.py
#   lab_03_ring_toy_model.py
#   lab_04_impulse_sweep.py
#   lab_05_fourier_isf.py
#   lab_06_white_noise_phase_noise.py
#   lab_07_flicker_noise.py
#   lab_08_jitter_integration.py
#   …共 52 個 lab_*.py / fig_*.py（42 個 lab_*、10 個 fig_*），完整清單見 figure_index
# scripts/
#   run_all_sims.py           # 一鍵重跑全部 lab_*.py + fig_*.py，產生所有圖
# static/figures/             # 產出的 .png（網站用 /figures/<name>.png 引用）
```

- **`common/`** 放可重用的核心函式，各 lab 共用；**各 lab** 只負責「擺參數、呼叫 common、出圖」。
  這樣公式只實作一次，任何 lab 改參數都用同一份權威實作。`common/` 目前共 **7 個模組**
  （`isf_utils`、`noise_utils`、`oscillator_models`、`pll_utils`、`serdes_utils`、
  `signal_utils`、`plot_utils`），第 5 節逐一列出函式簽章。
- **圖的輸出**一律落在 `static/figures/`，網站頁面用 `![alt](/figures/<name>.png)` 引用
  （見 [authoring spec 第 4 節] 的圖表清單）。

---

## 4. 一鍵重跑全部圖

```python
# 在專案根目錄執行：
#   python scripts/run_all_sims.py
```

`scripts/run_all_sims.py` 用 `glob.glob` 抓齊 `simulations/lab_*.py` 與 `simulations/fig_*.py`
（`scripts/run_all_sims.py:24–25`），依序在各自的 subprocess 中執行，把全部圖重新產生到
`static/figures/`；某一支腳本失敗不會中斷其他腳本，最後印出成敗總表。目前共
**52 支**腳本（42 個 `lab_*.py` + 10 個 `fig_*.py`）→ **60 張** PNG。要重現網站上的任何一張圖，
這一行就夠。

下表是 **lab_01–08 示範子集**（8 個最基礎的 lab，對應第 7 節一行驗算與 canonical 例 A/B/C）；
完整 52 支腳本 × 60 張圖的對照見 [figure_index](/01_paper_map/figure_index)。

| 圖檔 | script | function |
|---|---|---|
| `limit_cycle_phase_amplitude.png` | `lab_01_sinusoidal_oscillator.py` | `fig_limit_cycle` |
| `waveform_with_impulse_markers.png` | `lab_01_sinusoidal_oscillator.py` | `fig_impulse_markers` |
| `lc_waveform_and_isf.png` | `lab_02_lc_toy_model.py` | `main` |
| `ring_oscillator_timing_noise_accumulation.png` | `lab_03_ring_toy_model.py` | `fig_accumulation` |
| `lc_vs_ring_isf_comparison.png` | `lab_03_ring_toy_model.py` | `fig_lc_vs_ring_isf` |
| `sinusoidal_impulse_phase_sweep.png` | `lab_04_impulse_sweep.py` | `fig_isf_sweep` |
| `isf_impulse_sweep_sinusoidal.png` | `lab_04_impulse_sweep.py` | `fig_isf_sweep` |
| `lti_vs_ltv_impulse_response.png` | `lab_04_impulse_sweep.py` | `fig_lti_vs_ltv` |
| `isf_fourier_reconstruction.png` | `lab_05_fourier_isf.py` | `fig_reconstruction` |
| `isf_fourier_coefficients.png` | `lab_05_fourier_isf.py` | `fig_coefficients` |
| `symmetric_vs_asymmetric_isf_c0.png` | `lab_05_fourier_isf.py` | `fig_symmetric_vs_asymmetric` |
| `white_noise_phase_noise_psd.png` | `lab_06_white_noise_phase_noise.py` | `main` |
| `flicker_upconversion_symmetric_vs_asymmetric.png` | `lab_07_flicker_noise.py` | `main` |
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

### 5.4 `simulations/common/pll_utils.py` —— type-II PLL/CDR loop transfer

| 函式 | 簽章 | 做什麼 | 對應公式 |
|---|---|---|---|
| `loop_natural_freq` | `loop_natural_freq(fn_hz)` | $\omega_n=2\pi f_n$（Hz→rad/s 的小工具） | — |
| `H_lowpass_mag2` | `H_lowpass_mag2(f, fn_hz, zeta=0.707)` | $\lvert H_{lp}(j2\pi f)\rvert^2$（reference→output） | 規範 10.2 PLL 公式 |
| `H_highpass_mag2` | `H_highpass_mag2(f, fn_hz, zeta=0.707)` | $\lvert H_{hp}\rvert^2=\lvert1-H_{lp}\rvert^2$（VCO→output） | 規範 10.2 PLL 公式 |
| `shape_output_phase_noise` | `shape_output_phase_noise(f, S_ref, S_vco, fn_hz, zeta=0.707)` | $S_{out}=S_{ref}\lvert H_{lp}\rvert^2+S_{vco}\lvert H_{hp}\rvert^2$，回傳 `(S_out, S_ref_shaped, S_vco_shaped)` | 規範 10.3 PLL 雜訊預算 |
| `design_type2` | `design_type2(fn, zeta, N, Kvco, Icp)` | charge-pump type-II 2nd-order loop 的 $(R,C)$ 反推（`Kvco` 站內慣例為 **Hz/V**，函式內部乘 $2\pi$） | 開迴路 $G(s)=\omega_n^2(1+sRC)/s^2$ |

對應頁：[pll_noise_budget](/06_design_insights/pll_noise_budget)、
[pll_cdr_jitter_transfer](/04_simulation_labs/lab_13_pll_cdr_transfer)、
[cdr_bang_bang_jtol](/06_design_insights/cdr_bang_bang_jtol)。

### 5.5 `simulations/common/serdes_utils.py` —— SerDes 眼圖與 BER

| 函式 | 簽章 | 做什麼 | 對應公式 |
|---|---|---|---|
| `Q` | `Q(x)` | 高斯尾機率 $Q(x)=\tfrac12\,\mathrm{erfc}(x/\sqrt2)$ | 規範 10.2 SerDes BER |
| `ber_bathtub` | `ber_bathtub(t_offsets, sigma_t, ui)` | RJ-only 的取樣時刻 vs BER（浴缸曲線），$\text{BER}(t)=\tfrac12[Q(\tfrac{UI/2-t}{\sigma_t})+Q(\tfrac{UI/2+t}{\sigma_t})]$，回傳值下限裁到 $10^{-300}$ 方便取 log | 規範 10.2 SerDes BER |
| `eye_traces` | `eye_traces(sigma_t, ui, n_traces=400, n_pts=200, rng=None)` | 產生疊圖用的 NRZ 眼圖 traces（每條 trace 的 edge 加 $N(0,\sigma_t)$ 抖動），回傳 `(t_axis, traces)` | 眼圖視覺化（僅 RJ，無 ISI/DJ） |

對應頁：[serdes_eye_ber_bathtub](/04_simulation_labs/lab_12_serdes_eye_ber)。

### 5.6 `simulations/common/signal_utils.py` —— 通用訊號工具

| 函式 | 簽章 | 做什麼 | 對應公式 |
|---|---|---|---|
| `time_axis` | `time_axis(fs, duration)` | $[0,\text{duration})$、取樣率 $f_s$ 的均勻時間向量，回傳 `(t, dt)` | — |
| `instantaneous_phase` | `instantaneous_phase(x, analytic=True)` | 用 Hilbert transform（解析訊號）估瞬時（已展開）相位 | [P1] Eq.(1) 的數值萃取 |
| `zero_crossings_rising` | `zero_crossings_rising(x, t)` | 內插求上升零交越時刻 | ring edge 偵測 |
| `period_jitter` | `period_jitter(edge_times, T_nominal)` | period jitter：$T_k-T_{nominal}$ | 規範第 2 節 period jitter 定義 |
| `cycle_to_cycle_jitter` | `cycle_to_cycle_jitter(edge_times)` | cycle-to-cycle jitter：$T_{k+1}-T_k$ | 規範第 2 節 cycle-to-cycle 定義 |
| `db10` | `db10(x)` | $10\log_{10}x$（含下限避免 $-\infty$） | — |
| `db20` | `db20(x)` | $20\log_{10}\lvert x\rvert$（含下限避免 $-\infty$） | — |

對應頁：[jitter_kernels](/02_foundations/jitter_kernels)、
[psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter)。

### 5.7 `simulations/common/plot_utils.py` —— 存圖與 CJK 字型

| 函式 | 簽章 | 做什麼 |
|---|---|---|
| `figure_path` | `figure_path(name)` | 回傳 `static/figures/<name>` 的絕對路徑（自動補 `.png`、確保目錄存在） |
| `savefig` | `savefig(fig, name, verbose=True)` | 把 `fig` 存到 `figure_path(name)`、`plt.close(fig)`、印出相對路徑 |

模組載入時即執行第 2 節說明的 CJK 字型自動偵測（`_cjk_prefs` → `_cjk_font` → 設定
`plt.rcParams["font.family"]`），所有 lab/fig script 只要 `from simulations.common.plot_utils
import savefig` 就會套用同一套字型與版面風格（`figure.dpi=120`、`axes.grid=True` 等）。

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

---

## 8. 📓 下載 Jupyter notebooks

七個主線 lab 有對應的 Jupyter notebook（互動式筆記本，可一格一格執行、改參數重跑）
可直接下載，離線把公式玩成數字與圖：

| Notebook（點擊下載 .ipynb） | 內容 | 對應頁面 |
|---|---|---|
| [lab_01_sinusoidal_oscillator](/notebooks/lab_01_sinusoidal_oscillator.ipynb) | limit cycle、phase（切向）vs amplitude（徑向）擾動、impulse 注入時機 | [lab_01](/04_simulation_labs/lab_01_sinusoidal_oscillator) |
| [lab_05_fourier_isf](/notebooks/lab_05_fourier_isf.ipynb) | ISF 傅立葉係數 $c_n$、Parseval 驗證、$c_0$ 與對稱性 | [lab_05](/04_simulation_labs/lab_05_isf_fourier_coefficients) |
| [lab_06_white_noise_phase_noise](/notebooks/lab_06_white_noise_phase_noise.ipynb) | 白噪 $\to$ $1/f^2$ phase noise 端到端模擬 vs 理論線 | [lab_06](/04_simulation_labs/lab_06_white_noise_phase_noise) |
| [lab_08_jitter_integration](/notebooks/lab_08_jitter_integration.ipynb) | $\mathcal{L}(f)$ 積分成 rms jitter（canonical 例 C） | [lab_08](/04_simulation_labs/lab_08_jitter_integration) |
| [lab_18_lorentzian](/notebooks/lab_18_lorentzian.ipynb) | 相位 random walk $\to$ 載波 Lorentzian 線形與 3-dB 線寬 | [lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth) |
| [lab_22_capstone_lc_end_to_end](/notebooks/lab_22_capstone_lc_end_to_end.ipynb) | 理想 LC 全鏈：$\Gamma\to\Gamma_{rms}\to S_\phi\to$ 線寬 $\to\sigma_t\to$ BER | [capstone](/03_isf_core_theory/capstone_lc_end_to_end) |
| [lab_24_jitter_kernels](/notebooks/lab_24_jitter_kernels.ipynb) | TIE／period／cycle-to-cycle 三種 jitter 權重核 + Monte-Carlo 驗證 | [jitter_kernels](/02_foundations/jitter_kernels) |

**怎麼跑**：notebook 會 import `simulations/common` 的模組，所以要先
`git clone https://github.com/gmcycle7/isf-teaching-site.git`，並把下載的 .ipynb 放在
repo 目錄樹內任何位置執行（每本 notebook 的 setup cell 會自動往上層目錄尋找
`simulations/common` 並加入 `sys.path`）。相依套件同第 1 節的
`pip install numpy scipy matplotlib`，再加上 `pip install jupyter` 後用
`jupyter lab` 開啟即可。

> **誠實註記**：這些 notebook 是 `scripts/make_notebooks.py` 從對應的
> `simulations/lab_*.py` **自動產生的快照**（generated snapshot），不是手寫檔——
> 權威版本永遠是 repo 裡的 lab script；lab 更新後執行
> `python scripts/make_notebooks.py` 會重新產生全部 notebook。
> 與原 script 只有兩處刻意差異：`savefig` 改成 notebook 內 inline 顯示
> （不寫入 `static/figures/`）、路徑設定由 setup cell 自動尋找 repo root
> （原 script 用 `__file__` 定位）。

## 重點回顧

- Python 3.12 + `numpy`/`scipy`/`matplotlib`，CJK 字型用 `plot_utils.py` 的 `_cjk_prefs` 清單
  自動偵測（找不到就降級為 `DejaVu Sans`），並關閉 `unicode_minus`。
- `common/` 七模組（`isf_utils`、`noise_utils`、`oscillator_models`、`pll_utils`、`serdes_utils`、
  `signal_utils`、`plot_utils`）放權威實作；各 lab 只擺參數。
- `python scripts/run_all_sims.py` 一鍵重產全部 **60 張**圖到 `static/figures/`
  （來自 52 支 `lab_*.py`/`fig_*.py`）。
- 全部是 toy model；用固定 `default_rng(seed)` 保證逐位元可重現。
- 七個主線 lab 有可下載的 Jupyter notebook（第 8 節），由 `scripts/make_notebooks.py`
  自動產生（generated snapshot）。

## 延伸閱讀

- 數值口算與驗算：[numerical_feeling](/04_simulation_labs/numerical_feeling)
- 數學工具箱：[math_identities](/99_appendix/math_identities)
- 詞彙表：[glossary](/99_appendix/glossary)
- 公式索引：[equation_index](/01_paper_map/equation_index)
