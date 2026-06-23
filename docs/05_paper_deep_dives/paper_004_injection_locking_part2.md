---
title: "[P4] Injection Locking & Pulling — Part II (APF / Frequency Division)"
description: Hong–Hajimiri 2019 Part II 精讀：APF（振幅版 ISF，單位 1/A，[P4] Eq.(18)–(22)）、ISF/APF quadrature（Eq.(26)）、amplitude modulation、ILFD/頻率除法（ILFD 細節屬進階）。
---

# A General Theory of Injection Locking and Pulling in Electrical Oscillators—Part II

> **先備知識（建議先讀）**：[paper_001](/05_paper_deep_dives/paper_001_general_theory_phase_noise)（ISF $\Gamma$ 是切向投影）→ [phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise)（為何振幅被拉回、相位累積）→ [paper_003](/05_paper_deep_dives/paper_003_injection_locking_part1)（phase-only 廣義 Adler）。本頁屬**進階**，APF 是 ISF 在徑向的對偶。

[P3] 只談相位；本篇（Part II，**進階**）補上**振幅**這一維。它引入 **APF（Amplitude
Perturbation Function，振幅擾動函數）** $\Lambda(\phi)$——這是「振幅版的 ISF」，單位 $1/\text{A}$
——並用它解釋 LC 振盪器在注入下的 amplitude modulation（振幅調變）、transient（暫態）鎖定行為，
以及 **injection-locked frequency division（注入鎖定頻率除法，ILFD）**。對 ideal LC，ISF 與 APF
**互相正交（quadrature）**。

> **本頁定位**：進階 deep-dive，**非核心教學章節**。APF 的定義式（[P4] Eq.(18)–(22), p.2126）與 ideal-LC
> quadrature（Eq.(26), p.2128）已對照原文核實；ILFD 細節仍偏進階。先讀 [P1]（ISF）與
> [P3](/05_paper_deep_dives/paper_003_injection_locking_part1)（phase-only injection）再讀這裡。

## Citation

> **[P4]** B. Hong and A. Hajimiri, *"A General Theory of Injection Locking and Pulling in
> Electrical Oscillators—Part II: Amplitude Modulation in LC Oscillators, Transient Behavior,
> and Frequency Division,"* IEEE J. Solid-State Circuits, vol. 54, no. 8, pp. 2122–2139,
> Aug. 2019.（檔案 `BHongGenTheor-II_JSSC2019_Postprint.pdf`，paper_004）

## One-sentence contribution

定義振幅版的 ISF——APF $\Lambda(\phi)$（單位 $1/\text{A}$）——把 [P3] 的相位框架補成
phase + amplitude 完整模型，解釋注入下的振幅調變、暫態鎖定與 ILFD 頻率除法；對 ideal LC，ISF
與 APF 互成 quadrature（claim C11）。

## Why this paper matters

[P1] 與 [P3] 都假設「振幅擾動會被拉回、可以忽略」。這個假設在 phase noise 與弱注入時很好，但在
**強注入、暫態、或頻率除法**時就不夠了——這時振幅會被明顯調變，相位與振幅互相耦合。Part II 補上
這一維：

- **APF 是振幅的 ISF**：ISF $\Gamma$ 把注入電荷投影到 limit cycle 的**切向**（相位）；APF
  $\Lambda$ 把它投影到**徑向**（振幅）。兩者合起來才是擾動的完整投影。
- **ISF 與 APF 在 ideal LC 互成 quadrature**（差 90°）：相位最敏感的時刻（zero-crossing），
  振幅最不敏感；振幅最敏感的時刻（波峰），相位最不敏感。這正是
  [phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise) 講「為何振幅噪聲會衰減」
  的數學版本。
- **frequency division（ILFD）**：把一個 $N$ 倍頻的訊號注入振盪器，讓它鎖定在 $1/N$ 子諧波，
  就得到一個低功耗的除頻器。Part II 用 ISF/APF 框架設計這種除頻器，並做出可切換除數的
  dual-modulus prescaler（雙模除頻器）。

## Main assumptions

照 paper_metadata（paper_004.assumptions）：

1. 建立在 Part I 的 time-synchronous ISF 模型之上。
2. 振幅動態以一階方式用 **APF 與 amplitude decay function（振幅衰減函數）** 捕捉。
3. amplitude-modulation 結果聚焦在 **LC 振盪器**。

> **物理直覺（2-D 投影）**：一顆注入電荷 $\Delta q$ 把狀態點推一下。把這推力分解到 limit
> cycle 的兩個正交方向——切向（相位，永久留）用 $\Gamma$ 量、徑向（振幅，會被拉回）用 $\Lambda$
> 量。phase noise 只關心切向；injection 的完整動態兩者都要。

## Key equations

### APF 定義與 amplitude decay function（已對照原始 PDF 核實 ✓）

APF $\tilde\Lambda$ 是 Part I 有單位 ISF $\tilde\Gamma=\Gamma/q_{max}$ 的**振幅類比**：一顆注入電流脈衝
投影到 limit cycle **徑向（振幅）方向**的權重。[P4] 把振幅擾動分解成 APF 與衰減的乘積
$D(\tau,\phi)=\tilde\Lambda(\phi)\,d(\tau,\phi)$（[P4] Eq.(18), p.2126），並定義 **APF**
$\Delta(\phi):=\int_0^\infty D(\tau,\phi)\,d\tau$（[P4] Eq.(19), p.2126，單位 $1/\text{A}$）。和相位不同，振幅擾動會衰減——
ideal-LC 的 **amplitude decay function（振幅衰減函數）**（在 ideal-LC 一節 [P4] p.2127–2128）為：

$$
d(t,\phi)=e^{-t/\tau_0},\qquad \int_0^\infty d(t,\phi)\,dt=\tau_0=\frac{2Q}{\omega_{osc}}
$$

**關鍵物理（gem）**：振幅的「記憶時間」是 $\tau_0=2Q/\omega_{osc}$——高 $Q$ 的 LC 振幅恢復**慢**（$\tau_0$ 大），
但**終究會恢復**（指數衰減回 limit cycle）；相位則沒有這種恢復力（脈衝響應是 unit step，記憶無限長）。
這正是「為何振幅噪聲被抑制、相位噪聲累積」（claim C2）的**量化版本**。對 ideal LC，APF 與 decay 的關係為
$\Delta(\phi)=\tau_0\,\tilde\Lambda(\phi)$。

**對照表（ISF vs APF）**：

| 量 | 投影方向 | 符號 | 擾動命運 |
|---|---|---|---|
| ISF | 切向（phase） | $\tilde\Gamma=\Gamma/q_{max}$ | 永久累積（脈衝響應 = unit step） |
| APF | 徑向（amplitude） | $\tilde\Lambda$ | 以 $e^{-t/\tau_0}$、$\tau_0=2Q/\omega_{osc}$ 衰減回 limit cycle |

> **已核實**：APF 分解 $D(\tau,\phi)=\tilde\Lambda(\phi)\,d(\tau,\phi)$（[P4] Eq.(18), p.2126）、APF 定義
> $\Delta(\phi)=\int_0^\infty D\,d\tau$（[P4] Eq.(19), p.2126，單位 $1/\text{A}$），以及 ideal-LC 的 decay function
> $e^{-t/\tau_0}$、$\tau_0=2Q/\omega_{osc}$（[P4] ideal-LC 一節 p.2127–2128），皆對照原始 PDF 渲染逐字確認。

### ISF 與 APF 的 quadrature（ideal LC，已核實 ✓）

ideal LC 的 ISF 與 APF **基波**（[P4] Eq.(26), p.2128）：

$$
\tilde\Gamma_1=\frac{1}{q_{max}}\,\angle 90^\circ,\qquad
\tilde\Lambda_1=\frac{\tau_0}{q_{max}}\,\angle 0^\circ
$$

兩者相位差正好 **$90^\circ$（quadrature）**（claim C11）。物理意義：在 zero-crossing 注入幾乎純改相位
（$\tilde\Gamma$ 大、$\tilde\Lambda$ 小）；在波峰注入幾乎純改振幅（$\tilde\Lambda$ 大、$\tilde\Gamma$ 小）。
注意 APF 基波比 ISF 多一個 $\tau_0$ 因子——**高 $Q$ 時振幅效應（$\propto\tau_0=2Q/\omega_0$）反而更顯著**，
這也是為何 LC 注入鎖定常伴隨可觀的 amplitude modulation。

**amplitude-corrected Adler（augmented pulling，ideal-LC 特例 [P4] Eq.(27), p.2128）**：把 ISF 與 APF
一起代入。一般正弦注入的形式是 [P4] Eq.(22), p.2126（帶 $+$ 號與 $\cos(\theta+\angle\tilde\Gamma_1)/\cos(\theta+\angle\tilde\Lambda_1)$ 的相位偏移項）；
再把 ideal-LC 的 quadrature 角 $\angle 90^\circ/\angle 0$（Eq.(26)）代入 Eq.(22)，正弦注入下的相位方程化簡成

$$
\frac{d\theta}{dt}=(\omega_0-\omega_{inj})-\frac{\tfrac12\,(I_{inj}/q_{max})\sin\theta}{1+\tfrac12\,(I_{inj}\tau_0/q_{max})\cos\theta}
$$

分母那一項就是 APF 帶來的 **amplitude modulation 修正**；Part I 的純相位 Adler 是分母 $=1$ 的特例。

> **已核實**：$\tilde\Gamma_1,\tilde\Lambda_1$ 的 quadrature（[P4] Eq.(26), p.2128；sin/cos 形式見 Eq.(24)）
> 與上方顯示的 amplitude-corrected Adler——即 **ideal-LC 特例 [P4] Eq.(27), p.2128**（由 Eq.(26) 的 $\angle 90^\circ/\angle 0$ 代入一般式 Eq.(22), p.2126 得到，帶 $-$ 號、$\sin\theta$ 分子與 $\tau_0$ 因子）——皆對照原始 PDF 渲染逐字確認。

### amplitude modulation 與 frequency division（ILFD）

**Meaning**：把 APF 展成傅立葉級數後，可算出注入波形如何被「濾」成 amplitude modulation
（[P4] Sec. III-D 文字）。在 **ILFD** 裡，把頻率 $\approx N\omega_0$ 的訊號注入，靠 ISF/APF 的
第 $N$ 諧波鎖定到 $\omega_0$，達成 ÷$N$。Part II 並做出可在兩個除數間切換的 **dual-modulus
prescaler**（用 single-ended inverter-chain ring，靠 quadrature 注入方案分配級數）。

**Numerical example（÷2 的直覺）**：注入 $2f_0$ 的訊號，振盪器鎖定在 $f_0$，輸出頻率＝輸入的
一半。若輸入 10 GHz，輸出 5 GHz。lock range 此時由 ISF/APF 的**第 2 諧波**與注入波形的內積決定
（連回 [P3] 的廣義 Adler，只是換成 subharmonic 那一諧波在做平均）。具體級數分配與除數切換見
[P4] Sec. VIII（dual-modulus prescaler，p.2135 起；schematic Fig.19、Table VIII、Fig.21 在 p.2137）。

## Key figures

| 論文圖 | 頁 | 內容 | 教學用途 |
|---|---|---|---|
| Fig. 5 | 2126 | characterizing 注入電荷瞬間對振盪器的影響：ISF／excess phase、amplitude decay function、及 ISF 與 APF 的 quadrature 關係（已核實） | 連結相位（ISF）與振幅（APF）敏感度的最佳單圖 |

這張圖是「為何振幅噪聲會衰減、相位噪聲不會」的最佳視覺：APF 對應的擾動會被 amplitude decay
function 拉回，ISF 對應的相位擾動則永久留下。本站在
[phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise) 用這個概念（toy 對照圖
`limit_cycle_phase_amplitude.png`，**非 transistor-level**）。

> **已核實**：此圖為 [P4] Fig. 5, p.2126，標題「Characterizing the effect that an instantaneous injection of
> charge has on an oscillator」，已對照原始 PDF 渲染確認。（Fig. 3 p.2124 是 impulse-train↔sinusoid 等價、Fig. 6
> p.2127 是 bipolar Colpitts 範例，皆非此圖。）

![limit cycle：切向=相位（持續）、徑向=振幅（被拉回）（toy）](/figures/limit_cycle_phase_amplitude.png)

## Design insights

- **強注入／暫態要看振幅**：弱注入時忽略 APF 沒問題；強注入、暫態鎖定、頻率除法時，振幅調變
  不可忽略，必須 ISF + APF 一起算。
- **quadrature 是設計工具**：想純調相位就在相位敏感點（ISF 極值）注入；想做振幅鍵控／AM 就在
  振幅敏感點（APF 極值）注入。
- **ILFD 是低功耗除頻器**：相較 latch-based／CML divider 在高頻耗電大，ILFD 用注入鎖定除頻，
  功耗低；用 ISF/APF 的第 $N$ 諧波設計除數與 lock range。
- **dual-modulus prescaler**：靠 quadrature 注入方案在同一條 inverter-chain ring 上切換除數，
  省功耗。

## Limitations

照 paper_metadata（paper_004.limitations）：

- 強非線性、超出一階 APF 的效應只被部分捕捉。
- 對本站核心 ISF phase-noise 目標而言屬**進階／邊陲**。
- APF 的確切方程（[P4] Eq.(18)–(22), p.2126；quadrature Eq.(26), p.2128）已對照原文核實（claim C11）。

## Relationship to other papers

- **[P3]** 是直接前傳：本篇用 Part I 的 time-synchronous ISF 模型，補上振幅（APF）。
- **[P1]** 提供 ISF $\Gamma$；APF 是其在徑向的對偶。ideal LC 的 $\Gamma=-\sin$ 也出現在本站
  [isf_definition](/03_isf_core_theory/isf_definition)。
- **[P2]** 提供 ring 的 ISF；本篇的 ILFD/prescaler 就用 inverter-chain ring 實作。
- **[P5]** 與本頁無關（sense amplifier）；但 LC／latch 振盪器的起振同樣靠 cross-coupled 正回授
  （claim C12 的邊角橋樑）。
- APF 列在 [equation_index](/01_paper_map/equation_index) 第 21 條（本頁已對照 [P4] Eq.(18)–(22) 核實）；相位／振幅幾何見
  [phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise)。

## 延伸閱讀 / 對應教學頁

| 本頁的哪一塊 | 對應教學頁 | 那頁多給你什麼 |
|---|---|---|
| 注入相位決定 $\Gamma$／$\Lambda$ 的有效權重（cyclostationary 觀念） | [effective_isf](/03_isf_core_theory/effective_isf) | $\Gamma_{eff}=\Gamma\cdot\alpha$、bias-dependent 熱雜訊 NMF、switching-pair worked example |
| 注入相位如何改變有效 ISF（數值手感） | [lab_14_cyclostationary_isf](/04_simulation_labs/lab_14_cyclostationary_isf) | 可跑的 toy：noise 注入相位 $\to$ $\Gamma_{eff,rms}$（**pedagogical toy，非 transistor-level**） |
| ISF／APF 的 quadrature、injection locking 的耦合振盪器 | [quadrature_and_coupled_oscillators](/06_design_insights/quadrature_and_coupled_oscillators) | quadrature 注入、coupled-oscillator 的相位關係與設計 |

> **怎麼讀**：本頁把 [P3] 的相位框架補成 phase + amplitude；想理解「為何注入相位（或 noise 注入相位）會改變有效敏感度」，effective_isf 與 lab_14 是同一個 cyclostationary 觀念的理論與動手版本；想看 quadrature 如何變成可用的設計工具，回 quadrature_and_coupled_oscillators。相位／振幅幾何另見 [phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise)。

## What to remember

- **APF = 振幅版 ISF**，單位 $1/\text{A}$；ISF 投影到切向（相位），APF 投影到徑向（振幅）。
- **ideal LC：ISF 與 APF 互成 quadrature（差 $90°$）**——相位最敏感時振幅最不敏感，反之亦然
  （claim C11）。
- **相位永久累積、振幅被 decay function 拉回**——這就是「只追相位」在 phase noise 成立的根據。
- **ILFD**：注入 $N\omega_0$ 鎖定到 $\omega_0$ 得 ÷$N$ 低功耗除頻器；dual-modulus prescaler 可
  切換除數。
- 本頁屬**進階**；APF 確切式（[P4] Eq.(18)–(22), p.2126；quadrature Eq.(26), p.2128）已對照原文核實，ILFD 細節仍偏進階。
