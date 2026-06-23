---
title: 參考文獻 References
description: 5 篇 PDF 完整引用 [P1]-[P5]，加外部補充文獻（Leeson 1966、Demir PPV 2000、Kaertner——標明不在下載資料夾），並說明引用慣例與待人工核對的 TODO。
---

# 參考文獻 References

> **See also**：[glossary](/99_appendix/glossary)（術語直覺）、[equation_index](/01_paper_map/equation_index)（公式↔頁碼索引）、外部文獻用在 [derivation_leeson](/99_appendix/derivation_leeson)（[E1]）與 [derivation_floquet_ppv](/99_appendix/derivation_floquet_ppv)（[E2]、[E3]）

本站所有公式與結論都標了來源。這頁集中列出：**(A)** 下載資料夾裡的 5 篇 PDF（站內引用代號
`[P1]`–`[P5]`，引用字串逐字採自作者規範第 1 節），**(B)** 教學上會提到、但**不在下載資料夾**的
外部補充文獻，以及 **(C)** 引用慣例與需要人工核對的 TODO 清單。

> **誠實原則**：[P1]–[P4] 的公式皆已對照原始 PDF 渲染**逐字核實**；外部文獻 [E1]–[E4]（標 **不在
> 下載的 5 篇 PDF 內**）的卷期/頁碼/DOI 已用網路查證，但其論文內部公式只作背景。[P5] 與 ISF 無關。

---

## A. 核心文獻（下載資料夾內的 5 篇 PDF）

### [P1] — ISF 理論的奠基論文

A. Hajimiri and T. H. Lee, *"A General Theory of Phase Noise in Electrical Oscillators,"*
IEEE J. Solid-State Circuits, vol. 33, no. 2, pp. 179–194, Feb. 1998.
（檔案 `general.pdf`，`paper_001`）

- **一句話貢獻**：建立振盪器對 noise 是 **LTV（線性時變）** 而非 LTI 的觀點，提出 ISF
  $\Gamma(\omega_0\tau)$ 與 $q_{max}$ normalization，導出 $1/f^2$、$1/f^3$ 的封閉式與設計法則。
- **本站用到**：[impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift)、
  [isf_definition](/03_isf_core_theory/isf_definition)、
  [convolution_derivation](/03_isf_core_theory/convolution_derivation)、
  [fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf)、
  [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)、
  [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)。
- **關鍵式**：Eqs.(1),(9),(10),(11),(12),(13),(15)–(24)，pp.181–185（見 [equation_index](/01_paper_map/equation_index)）。

### [P2] — ring oscillator 的延伸

A. Hajimiri, S. Limotyrakis, and T. H. Lee, *"Jitter and Phase Noise in Ring Oscillators,"*
IEEE J. Solid-State Circuits, vol. 34, no. 6, pp. 790–804, Jun. 1999.
（檔案 `jitter_ring.pdf`，`paper_002`）

- **一句話貢獻**：把 ISF 框架套到 ring oscillator，給出 jitter／phase noise 封閉式、
  $\Gamma_{rms}\propto N^{-3/4}$ scaling，以及「固定功率與頻率下 single-ended ring 相位雜訊
  幾乎與級數 $N$ 無關」的結論。
- **本站用到**：[lab_03](/04_simulation_labs/lab_03_ring_oscillator_toy_model)、
  [lc_vs_ring](/06_design_insights/lc_vs_ring)、[symmetry](/06_design_insights/symmetry)。
- **關鍵式（已核實）**：Eq.(8) $\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$ p.792、Eq.(12) $\kappa=\frac{\Gamma_{rms}}{q_{max}}\sqrt{\tfrac12\tfrac{\overline{i_n^2}}{\Delta f}}$ p.793、
  Eq.(14) $f_0=1/(2N\tau_D)$、Eq.(16) $\Gamma_{rms}=\sqrt{\tfrac{2\pi^2}{3\eta^3}\tfrac{1}{N^{1.5}}}$ p.794、
  Eq.(23) FOM $\frac{8}{3\eta}\frac{kT}{P}\frac{V_{DD}}{V_{char}}(f_0/\Delta f)^2$ p.796（$\eta$ 為級延遲比例常數 Eq.(14)，$\approx 1$；$\gamma$ 僅透過 $V_{char}=\Delta V/\gamma$ 進入。v2 曾誤改前置係數為 $8/(3\gamma)$，v3 已對照原始 PDF p.796 更正）。

### [P3] — injection locking（進階）

B. Hong and A. Hajimiri, *"A General Theory of Injection Locking and Pulling in Electrical
Oscillators—Part I: Time-Synchronous Modeling and Injection Waveform Design,"*
IEEE J. Solid-State Circuits, vol. 54, no. 8, pp. 2109–2121, Aug. 2019.
（檔案 `BHongGenTheor-I_JSSC2019_Postprint.pdf`，`paper_003`）

- **一句話貢獻**：用 ISF 建立 time-synchronous 的 injection locking/pulling 理論，
  把 Adler 1946 推廣到任意振盪器與任意注入波形。
- **本站用到**：[paper_003_injection_locking_part1](/05_paper_deep_dives/paper_003_injection_locking_part1)。
- **關鍵式（已核實）**：$\tilde\Gamma=\Gamma/q_{max}$（Eq.26）、廣義 Adler
  $\frac{d\theta}{dt}=(\omega_0-\omega_{inj})+\Omega(\theta)$、$\Omega(\theta)=\frac{1}{T_{osc}}\int\tilde\Gamma(\omega_0 t+\theta)i_{inj}\,dt$（Eq.33）、
  lock range $\omega_L=\frac12 I_{inj}\lvert\tilde\Gamma_1\rvert$（Eq.35），pp.2113–2114。

### [P4] — APF / 進階

B. Hong and A. Hajimiri, *"...Part II: Amplitude Modulation in LC Oscillators, Transient
Behavior, and Frequency Division,"* IEEE J. Solid-State Circuits, vol. 54, no. 8,
pp. 2122–2139, Aug. 2019.
（檔案 `BHongGenTheor-II_JSSC2019_Postprint.pdf`，`paper_004`）

- **一句話貢獻**：提出 **APF（Amplitude Perturbation Function，振幅擾動函數）**——ISF 在振幅域的
  對應物（單位 1/A），處理 LC 振盪器在注入下的振幅調變、暫態鎖定與注入鎖定除頻。
- **本站用到**：[paper_004_injection_locking_part2](/05_paper_deep_dives/paper_004_injection_locking_part2)、
  [phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise)（用其 ISF/APF 正交圖說明振幅擾動為何衰減）。
- **關鍵式（已核實）**：APF 分解 $D(\tau,\phi)=\tilde\Lambda(\phi)\,d(\tau,\phi)$（Eq.18）、APF 定義
  $\Delta(\phi):=\int_0^\infty D\,d\tau$（單位 1/A，Eq.19）、振幅變化（Eq.20）、augmented pulling equation
  （Eq.21，正弦形式 Eq.22）皆在 Fig.5, p.2126；ideal-LC quadrature（ISF 基波 $\angle90°$、APF 基波 $\angle0°$）
  $\tilde\Gamma_1=\frac{1}{q_{max}}\angle90°$、$\tilde\Lambda_1=\frac{\tau_0}{q_{max}}\angle0°$（Eq.26），p.2128；
  amplitude decay $d(t,\phi)=e^{-t/\tau_0}$、$\tau_0=2Q/\omega_{osc}$ 在同一 ideal-LC 段 p.2127–2128。

### [P5] — 與 ISF 無關（誠實註記）

A. Hajimiri and R. Heald, *"Design Issues in Cross-Coupled Inverter Sense Amplifier,"*
Proc. IEEE ISCAS, 1998.
（檔案 `Hajimiri_ISCS_98.pdf`，`paper_005`）

- **誠實說明**：這是一篇 **cross-coupled-inverter sense amplifier（交叉耦合反相器感測放大器）**
  的論文，主題是 regeneration 速度與 mismatch offset，**與 oscillator phase noise / ISF 無關**。
  它出現在下載資料夾只因為**同作者（Hajimiri）**。
- **唯一概念連結**：cross-coupled-pair 的 **regeneration / 正回授** 機制，也是 latch 型與 LC 振盪器
  起振的底層機制——本站僅以此當作邊角註解，不從它取任何 ISF 公式（對應主張 C12）。
- **關鍵式**：`TODO: equations not transcribed because this PDF is unrelated to ISF/phase noise.`

---

## B. 外部補充文獻（**不在下載的 5 篇 PDF 內**）

以下文獻在教學上會被提到，但**不在下載資料夾**。**卷期／頁碼／DOI 已用網路查證**；但本站對這些
論文**內部**的公式只作背景說明、未逐字重推。

### [E1] Leeson 1966 — 經驗相位雜訊模型（對照用）

D. B. Leeson, *"A Simple Model of Feedback Oscillator Noise Spectrum,"*
Proc. IEEE, vol. 54, no. 2, pp. 329–330, Feb. 1966. **DOI: 10.1109/PROC.1966.4682**。

- **角色**：ISF 理論之前最廣用的**經驗** phase noise 模型；[P1] 引言把它當作「ISF 理論所涵蓋
  並超越的特例」。對照與推導見 [derivation_leeson](/99_appendix/derivation_leeson)：

$$
\mathcal{L}(\Delta\omega)=10\log_{10}\!\left[\frac{2FkT}{P_s}\left(1+\left(\frac{\omega_0}{2Q\,\Delta\omega}\right)^2\right)\left(1+\frac{\omega_{1/f^3}}{|\Delta\omega|}\right)\right].
$$

- **狀態**：卷期/頁碼/DOI **已查證**；$F$（noise figure）為經驗擬合參數（依版本略異），本站當對照用。

### [E2] Demir–Mehrotra–Roychowdhury 2000 — PPV（嚴謹化 ISF）

A. Demir, A. Mehrotra, and J. Roychowdhury, *"Phase Noise in Oscillators: A Unifying Theory
and Numerical Methods for Characterization,"* IEEE Trans. Circuits Syst. I: Fundam. Theory
Appl., vol. 47, no. 5, pp. 655–674, May 2000. **DOI: 10.1109/81.847872**。

- **角色**：用 **PPV（Perturbation Projection Vector，擾動投影向量）** 與非線性相位方程，給 ISF
  一個嚴謹的數學基礎（PPV 即 Floquet 第一主向量，可由 adjoint 數值求出）。背景式：
  $\dot{\phi}(t)=v_1^T(t)\,B(t)\,\xi(t)$。
- **狀態**：卷期/頁碼/DOI **已查證**；PPV 框架詳見 [derivation_floquet_ppv](/99_appendix/derivation_floquet_ppv)。

### [E3] Kärtner 1990 — 振盪器雜訊的擾動分析（背景）

F. X. Kärtner, *"Analysis of White and $f^{-\alpha}$ Noise in Oscillators,"*
Int. J. Circuit Theory Appl., vol. 18, no. 5, pp. 485–519, 1990. **DOI: 10.1002/cta.4490180505**。

- **角色**：早於 [P1] 的振盪器雜訊擾動分析之一，常與 Demir 一起被列為「ISF/PPV 的數學前驅」。
- **狀態**：卷期/頁碼/DOI **已查證**；本站僅作背景提及。

### [E4] Adler 1946 — injection locking 的原始論文（[P3] 推廣的對象）

R. Adler, *"A Study of Locking Phenomena in Oscillators,"* Proc. IRE, vol. 34, no. 6,
pp. 351–357, Jun. 1946. **DOI: 10.1109/JRPROC.1946.229930**。（再刊於 Proc. IEEE, vol. 61, no. 10, pp. 1380–1385, Oct. 1973。）

- **角色**：經典 Adler 方程的原始來源；[P3] 把它推廣到任意振盪器／任意注入波形。
- **狀態**：卷期/頁碼 **已查證**；經典與廣義 Adler 式見
  [paper_003](/05_paper_deep_dives/paper_003_injection_locking_part1)。

### [E5] Zadeh 1950 — 線性時變系統的頻域分析（HTM 的源頭）

L. A. Zadeh, *"Frequency Analysis of Variable Networks,"* Proc. IRE, vol. 38, no. 3,
pp. 291–299, Mar. 1950. **DOI: 10.1109/JRPROC.1950.231083**。

- **角色**：定義時變傳函 $H(f,t)$（system function），是 harmonic transfer matrix 與
  「ISF 是相位輸出對各諧波的轉換向量」這個嚴格 LTV 觀點的源頭。
- **狀態**：卷期/頁碼/DOI **已查證**；框架見 [ltv_htm](/99_appendix/ltv_htm)（**不在 5 篇 PDF 內**）。

---

## C. 引用慣例

1. **站內引用格式**：行內用 `[P1] Eq.(21), p.185` 這種寫法；每個來自論文的定義／公式／結論／figure
   都標來源（見作者規範第 1 節）。
2. **代號**：核心 5 篇用 `[P1]`–`[P5]`（對應 `paper_001`–`paper_005`）；外部補充用 `[E1]`–`[E3]`，
   且一律附「**不在下載的 5 篇 PDF 內**」字樣。
3. **LaTeX 來源**：[P1] 的公式 LaTeX 已對照 PDF 渲染頁確認（`manual_verification_needed=false`）；
   [P2]–[P4] 的部分常數／形式標 ⚠️，見下方 TODO。
4. **單位與符號**：一律對照 [notation](/00_overview/notation)，全站一致。

---

## D. 待人工核對 TODO 清單

經 v3 更新後，**[P1] 全部、[P2] ring 常數（Eq.8/12/14/16/17/21/23，其中 Eq.(23) 前置係數於 v3 由誤寫的
$8/(3\gamma)$ 更正為 $8/(3\eta)$ 並重新核實）、[P3] 廣義 Adler（Eq.26/30/33/34/35）、
[P4] APF（正確編號為 Eq.(18)–(22) + Fig.5, p.2126；ideal-LC quadrature Eq.(26), p.2128）皆已對照原始
PDF 渲染逐字核實**；外部文獻 [E1]–[E4] 的**卷期/頁碼/DOI 已用網路查證**。剩餘僅以下次要項目：

| 項目 | 內容 | 出處 | 性質 |
|---|---|---|---|
| 已核實 | [P2] Fig.17（phase noise vs 對稱電壓，y 軸 = $1/f^3$ corner frequency，於對稱點急降） | p.802 | 次要（圖細節，已核實） |
| `TODO` | [P4] dual-modulus prescaler 的級數分配細節 | Sec. VIII, p.2135 | 次要（進階電路） |
| 註記 | [E1]–[E4] 論文**內部**公式只作背景、未逐字重推（卷期/DOI 已查證） | 外部 | 背景 |
| 註記 | [P5] sense-amplifier 公式刻意未轉錄（與 ISF 無關） | — | 誠實標註 |

> **factor-of-2 提醒**：[P1] Eq.(21) 的分母寫 $4\Delta\omega^2$，而時域乾淨推導得 $2\Delta\omega^2$，
> 差的 2 倍是 SSB 記帳慣例（文獻著名小爭議），**不是** 引用錯誤；詳見
> [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)。

## 延伸閱讀

- 公式 → 推導頁 → 來源：[equation_index](/01_paper_map/equation_index)
- 主張與交叉引用：[claims_cross_reference](/01_paper_map/claims_cross_reference)
- 詞彙表：[glossary](/99_appendix/glossary)
- 數學工具箱：[math_identities](/99_appendix/math_identities)
