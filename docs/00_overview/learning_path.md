---
title: 循序學習路徑 Learning Path
description: 九步循序學習路徑，每步含目標、要讀的頁、先備、預期收穫，並給快速與完整兩條路線。
---

# 循序學習路徑 Learning Path

這頁把首頁的九個步驟展開成一條**可以照著走**的學習路徑。每一步告訴你：

- **要達成什麼**（這步的學習目標）；
- **讀哪幾頁**（按順序）；
- **先備**（沒有這個會卡住）；
- **預期收穫**（讀完應該能做什麼）。

最後給兩條路線：**快速路線**（一個下午抓到 ISF 主幹）與**完整路線**
（每條公式自己重推一遍、每個 lab 自己跑一遍）。

> **怎麼用這頁**：第一次學請走「完整路線」，每讀完一步就回來打勾。回頭複習時走
> 「快速路線」即可。看到 `TODO:` 表示該處仍需人工對照原始 PDF；看到「toy model」
> 表示那是**教學用簡化模型，非 transistor-level**。

## 先把這三頁當「字典」

開始之前，先把這三頁放在手邊，遇到不懂的符號或論文出處隨時回查：

- [notation](/00_overview/notation) — 統一符號表（全站符號、單位、各論文對照）。
- [paper_summary_table](/01_paper_map/paper_summary_table) — 五篇論文一頁速覽（誰負責什麼）。
- [equation_index](/01_paper_map/equation_index) — 每條公式 → 推導頁 → 來源。

**隨手查**（不確定符號／公式／英文術語時，照下表跳頁；卡關時優先回這四頁）：

| 想查什麼 | 去哪頁 |
|---|---|
| 公式一頁打包、canonical 數值例 A/B/C | [速查表 Cheat Sheet](/00_overview/cheat_sheet) |
| 某個符號的意義與單位（如 $\Gamma_{rms}$、$q_{max}$、$c_0$） | [統一符號表 Notation](/00_overview/notation) |
| 某個英文術語的中文直覺（如 ISF、cyclostationary、limit cycle） | [中英對照詞彙表 Glossary](/99_appendix/glossary) |
| 某條公式出自哪篇論文哪個 Eq.、在哪頁推導 | [公式推導索引 Equation Index](/01_paper_map/equation_index) |

---

## 第 1 步：振盪器的「相位」到底是什麼 {#step-1}

- **要達成什麼**：建立 limit cycle（極限環，振盪器穩態走的閉合軌跡）的幾何圖像，
  分清楚**相位**（沿環的切向，無恢復力）與**振幅**（離環的徑向，有恢復力）。
- **讀哪幾頁**：[oscillator_phase](/02_foundations/oscillator_phase) →
  [phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise)。
- **先備**：二維狀態空間、相平面、RLC 振盪的基本圖像。
- **預期收穫**：能解釋「為什麼擾動沿切向會永久留下、沿徑向會被拉回」，這正是
  claim **C2**（見 [claims_cross_reference](/01_paper_map/claims_cross_reference)）。

## 第 2 步：noise 是小擾動，振盪器對它是 LTV 而非 LTI {#step-2}

- **要達成什麼**：理解振盪器對 noise 是 **LTV（linear time-variant，線性時變）**——
  同一顆 impulse 在不同相位注入，造成的相位偏移**不同**；不像 LTI 系統只看 $t-\tau$。
- **讀哪幾頁**：[lti_vs_ltv](/02_foundations/lti_vs_ltv)。
- **先備**：第 1 步；線性系統、脈衝響應、卷積。
- **預期收穫**：能畫出 LTI 的 $h(t-\tau)$ 與 LTV 的 $h_\phi(t,\tau)$ 之差別，
  對應圖 `lti_vs_ltv_impulse_response.png`。這就是 claim **C1**。

## 第 3 步：ISF 的操作型定義（impulse → phase） {#step-3}

- **要達成什麼**：從電容 $q=Cv$ 一路推到 ISF 的操作型定義
  $\Delta\phi=\Gamma(\omega_0\tau)\,\Delta q/q_{max}$（[P1] Eq.(9)–(11), p.182），
  並理解 $\Gamma$ 為何無因次、為何 $2\pi$ 週期。
- **讀哪幾頁**：[impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift) →
  [isf_definition](/03_isf_core_theory/isf_definition)。
- **先備**：第 1、2 步；電容關係、單位換算。
- **預期收穫**：能做 canonical 例 A 的口算——$q_{max}=1$ pC、$\Delta q=1$ fC、
  $\Gamma=0.5$、$f_0=5$ GHz 時 $\Delta\phi=5\times10^{-4}$ rad、$\Delta t=15.9$ fs。

## 第 4 步：從單一 impulse 到任意 noise（卷積） {#step-4}

- **要達成什麼**：用疊加把單一相位步階推廣成 LTV 卷積
  $\phi(t)=\frac{1}{q_{max}}\int_{-\infty}^{t}\Gamma(\omega_0\tau)\,i_n(\tau)\,d\tau$
  （[P1] Eq.(11), p.182），看懂積分上限 $t$（記憶）為何造成相位**累積**。
- **讀哪幾頁**：[convolution_derivation](/03_isf_core_theory/convolution_derivation)。
- **先備**：第 3 步；卷積、積分。
- **預期收穫**：能解釋「相位是 noise 的積分器」，為第 5 步的 $1/f^2$ 斜率鋪路。

## 第 5 步：白噪 → $1/f^2$，flicker → $1/f^3$ {#step-5}

- **要達成什麼**：推出招牌結果 $\mathcal{L}\propto\Gamma_{rms}^2/q_{max}^2$
  （[P1] Eq.(21), p.185，claim **C3**），以及 flicker 只透過 ISF 的 DC 項 $c_0$
  上轉成 $1/f^3$（[P1] Eq.(23)(24), claim **C4/C5**）。
- **讀哪幾頁**：[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) →
  [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)。
- **先備**：第 4 步；PSD、Parseval。
- **預期收穫**：能做 canonical 例 B——同一組數值用 Eq.(21) 算出 $\mathcal{L}=-148.0$
  dBc/Hz；並理解 spec 第 3 節提到的**著名 factor-of-2** SSB 記帳爭議。

## 第 6 步：ISF 的傅立葉觀點（$c_0$、$c_n$、upconversion） {#step-6}

- **要達成什麼**：把 ISF 展開成傅立葉級數 $\Gamma=\frac{c_0}{2}+\sum c_n\cos(n\omega_0\tau+\theta_n)$
  （[P1] Eq.(12), p.183），理解每個 $c_n$ 把 $n\omega_0$ 附近的 noise「降頻」搬到 carrier，
  以及 $\sum c_n^2=2\Gamma_{rms}^2$（Parseval，[P1] Eq.(20)）。
- **讀哪幾頁**：[fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf) →
  [rms_isf](/03_isf_core_theory/rms_isf)。
- **先備**：第 5 步；傅立葉級數。
- **預期收穫**：能說出「對稱波形 → $c_0\approx0$ → 抑制 $1/f^3$」這個設計鐵則的數學根據。

## 第 7 步：模擬 lab，建立數值手感 {#step-7}

- **要達成什麼**：把前面的公式**親手跑一遍**、看圖、對數字，把 rad、fs、dBc/Hz、
  jitter 之間的換算練成反射。
- **讀哪幾頁**：先 [numerical_feeling](/04_simulation_labs/numerical_feeling)（三個必做口算），
  再依序 [lab_01](/04_simulation_labs/lab_01_sinusoidal_oscillator)、
  [lab_02](/04_simulation_labs/lab_02_lc_oscillator_toy_model)、
  [lab_04](/04_simulation_labs/lab_04_impulse_injection_sweep)、
  [lab_05](/04_simulation_labs/lab_05_isf_fourier_coefficients)、
  [lab_06](/04_simulation_labs/lab_06_white_noise_phase_noise)、
  [lab_07](/04_simulation_labs/lab_07_flicker_noise_upconversion)、
  [lab_08](/04_simulation_labs/lab_08_jitter_integration)。
- **先備**：第 3–6 步；一點 Python/NumPy。
- **預期收穫**：能用 `simulations/common/` 的函式一行驗證 canonical 例 A/B/C；
  每張圖都能追溯到 [figure_index](/01_paper_map/figure_index) 的 script 與公式。

## 第 8 步：設計 takeaways（symmetry、swing、slope） {#step-8}

- **要達成什麼**：把公式翻成**設計旋鈕**——拉大 $q_{max}$、壓低 $\Gamma_{rms}$、
  強制波形對稱以壓 $c_0$；並理解 ring 的 $\Gamma_{rms}\propto N^{-3/4}$ 與
  「固定功率/頻率下 ring phase noise 幾乎與級數 $N$ 無關」（claim **C7/C8**）。
- **讀哪幾頁**：[symmetry](/06_design_insights/symmetry) →
  [lc_vs_ring](/06_design_insights/lc_vs_ring)。
- **先備**：第 5、6 步。
- **預期收穫**：拿到一顆振盪器規格，能說出「先動哪個旋鈕」。

## 第 9 步：接到 SerDes clocking（jitter、eye、PLL/CDR） {#step-9}

- **要達成什麼**：把 phase noise 積分成 rms jitter，連到 SerDes 的 eye 閉合與 BER。
- **讀哪幾頁**：[psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter) →
  [serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)。
- **先備**：第 5、7 步（尤其 lab_08）。
- **預期收穫**：能做 canonical 例 C——$f_0=5$ GHz、$\mathcal{L}(1\text{MHz})=-100$
  dBc/Hz、$1/f^2$、積 1→100 MHz $\Rightarrow\sigma_\phi=14.07$ mrad、$\sigma_t=447.9$ fs，
  並知道積分被**下限**主導。

---

## 進階（選修）：injection locking 與 APF

主幹學完後，若想看 ISF 如何延伸到 phase noise 以外：

- [paper_003_injection_locking_part1](/05_paper_deep_dives/paper_003_injection_locking_part1)
  ——同一個 ISF 給出廣義 Adler 方程（claim **C10**，[P3]）。
- [paper_004_injection_locking_part2](/05_paper_deep_dives/paper_004_injection_locking_part2)
  ——振幅版的 APF（amplitude perturbation function，claim **C11**，[P4]）。
- [effective_isf](/03_isf_core_theory/effective_isf) ——cyclostationary 修正
  $\Gamma_{eff}=\Gamma\cdot\alpha$（claim **C9**），以及 PPV/adjoint/Floquet 的**外部**
  數學基礎（claim **C13**，**不在這 5 篇 PDF 內**，以標準文獻補充）。

---

## 兩條路線

### 快速路線（約一個下午，抓主幹）

目標是「看懂 ISF 是什麼、它如何決定 phase noise」。**不**自己重推、**不**自己跑模擬：

1. [oscillator_phase](/02_foundations/oscillator_phase)（只看 limit cycle 與相位／振幅圖像）
2. [lti_vs_ltv](/02_foundations/lti_vs_ltv)（看 LTV 的核心結論與圖）
3. [impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift)（記住操作型定義 + 例 A）
4. [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)（記住 Eq.(21) 與例 B）
5. [fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf)（$c_0$ 抑制 $1/f^3$ 的直覺）
6. [numerical_feeling](/04_simulation_labs/numerical_feeling)（三個口算）
7. [serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)（jitter 與 eye 的結論）

讀完你應能回答：什麼是 ISF、為何 LTV、$\mathcal{L}\propto\Gamma_{rms}^2/q_{max}^2$、
對稱性為何重要、phase noise 怎麼變 jitter。

### 完整路線（每步自己重推 + 自己跑 lab）

照上面**第 1 步到第 9 步**順序，**每條公式蓋住答案自己重推一遍**，
**每個 lab 自己 `python scripts/run_all_sims.py` 跑一遍**對圖對數字，最後再讀進階三頁。
建議節奏：

| 階段 | 步驟 | 重點交付（自我檢核） |
|---|---|---|
| 幾何直覺 | 1–2 | 能畫 limit cycle、能說 LTV vs LTI 差別 |
| ISF 核心 | 3–6 | 能重推 Eq.(9)→(11)→(12)→(20)→(21)→(24) |
| 動手 | 7 | 能重現例 A/B/C 的數字，誤差量級對得上 |
| 設計 | 8–9 | 能列設計旋鈕、能把 $\mathcal{L}$ 積成 $\sigma_t$ |
| 進階 | 選修 | 能說 injection/APF/PPV 如何沿用同一個 $\Gamma$ |

## 重點回顧

- 九步主幹：相位幾何 → LTV → ISF 定義 → 卷積 → 白噪/flicker → 傅立葉 → lab → 設計 → SerDes。
- 隨手查四頁（卡關時優先回查）：[cheat_sheet](/00_overview/cheat_sheet)、
  [notation](/00_overview/notation)、[glossary](/99_appendix/glossary)、
  [equation_index](/01_paper_map/equation_index)（見本頁開頭「隨手查」表）。
- 快速路線抓主幹；完整路線重推每式、跑每個 lab。
- 進階 injection/APF/PPV 為選修；PPV/adjoint **不在 5 篇 PDF 內**，屬外部文獻。

## 延伸閱讀

- 五篇論文的分工：[paper_summary_table](/01_paper_map/paper_summary_table)
- 每張圖的來源：[figure_index](/01_paper_map/figure_index)
- 教學主張的交叉索引：[claims_cross_reference](/01_paper_map/claims_cross_reference)
- 為何來源含一篇 off-topic PDF：[build_report](/00_overview/build_report)
