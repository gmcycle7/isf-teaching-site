---
title: 五篇論文速覽 Paper Summary Table
description: 五篇來源論文一頁速覽——貢獻、關鍵公式、關鍵圖、我們拿它來教什麼，外加教學角度的分工。
---

# 五篇論文速覽 Paper Summary Table

來源資料夾共 **5 個 PDF**。這頁用一張表把它們一眼看完，再用**教學角度**整理它們的分工：
哪篇是 ISF 核心、哪篇延伸到 ring、哪篇講 injection、哪篇其實**離題**，以及哪些公式
其實是同一件事的不同寫法、哪些符號定義不同需要統一。

> **誠實聲明（先講）**：這 5 篇裡，4 篇是 Hajimiri 系列的 oscillator phase noise／
> injection 論文，**1 篇（`Hajimiri_ISCS_98.pdf` = [P5]）其實是 cross-coupled
> sense amplifier 論文、與 ISF 無關**，本站只當邊角註解。另外，常被一起講的
> **PPV / adjoint / PSS / PNoise / Floquet** 其實**沒有**任何一篇專屬論文在這 5 個 PDF
> 內——它們屬外部文獻，誠實標註於下。

## 一頁總表

資料取自 `extracted/paper_metadata.json`。引用字串依站內規範逐字使用（見 [references](/99_appendix/references)）。

| Paper | Year | Main Contribution | Key Equations | Key Figures | What We Use It For |
|---|---|---|---|---|---|
| **[P1]** Hajimiri & Lee, *A General Theory of Phase Noise in Electrical Oscillators*, IEEE JSSC 33(2):179–194 (`general.pdf`, paper_001) | 1998 | 建立振盪器對 noise 的 **LTV / ISF** 理論：引入 $\Gamma(\omega_0\tau)$ 與 $q_{max}$ normalization，導出 $1/f^2$、$1/f^3$ 的封閉式與設計法則（大 $q_{max}$、小 $\Gamma_{rms}$、波形對稱壓 $c_0$）。 | Eq.(1) 輸出分解；(9) $\Delta V=\Delta q/C$；(10)(11) ISF 脈衝響應與卷積；(12) 傅立葉級數；(19)(20) 求和與 Parseval；**(21)** $1/f^2$ 招牌式；(22)(23)(24) flicker $1/f^3$ 與 corner | Fig. 4（peak vs ZC 注入）、Fig. 6（$\Delta\phi$–$\Delta q$ 線性）、Fig. 7（LC/ring ISF 形狀）、Fig. 8（$n\omega_0$→carrier 降頻）、Fig. 11/12（$1/f^3,1/f^2$,floor 全景與 corner） | **ISF 核心基礎**——全站 02/03 章與大部分 lab 的理論來源。 |
| **[P2]** Hajimiri, Limotyrakis & Lee, *Jitter and Phase Noise in Ring Oscillators*, IEEE JSSC 34(6):790–804 (`jitter_ring.pdf`, paper_002) | 1999 | 把 ISF 套到 ring oscillator：jitter／phase noise 封閉式、$\Gamma_{rms}\propto N^{-3/4}$ scaling、「固定功率與頻率下 ring phase noise 幾乎與級數 $N$ 無關」、rise/fall 對稱如何壓 $1/f$ 上轉。 | (8) 累積 jitter $\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$；(11)(12) $\kappa^2\propto\Gamma_{rms}^2/q_{max}^2\cdot\overline{i_n^2}/\Delta f$；(15) $f_0=1/(2N\tau_D)$；(16) $\Gamma_{rms}\propto N^{-3/4}$；text result $\mathcal{L}\vert _{1/f^2}\approx\frac{8}{3\eta}\,\frac{V_{DD}}{V_{char}}\,\frac{kT}{P}(\omega_0/\Delta\omega)^2$（$\eta$ 為級延遲比例常數 Eq.14，$\approx 1$；$\gamma$ 僅透過 $V_{char}=\Delta V/\gamma$ 進入） | Fig. 5（ring 單級 ISF）、Fig. 8（$\Gamma_{rms}$ vs $N$）、Fig. 17（phase noise vs 對稱控制電壓，最小值在對稱點） | **ring oscillator 延伸**——06 章 lc_vs_ring、symmetry，與 lab_03。 |
| **[P3]** B. Hong & A. Hajimiri, *Injection Locking and Pulling…Part I: Time-Synchronous Modeling and Injection Waveform Design*, IEEE JSSC 54(8):2109–2121 (`BHongGenTheor-I_JSSC2019_Postprint.pdf`, paper_003) | 2019 | 用 ISF 建立 **time-synchronous** injection locking/pulling 模型，把 Adler 1946 推廣到**任意振盪器與任意注入波形**：單一一階（廣義 Adler）方程預測 lock range、locked phase、模態穩定性。 | 經典 Adler $\dot\phi=-\omega_L\sin\phi+\Delta\omega_{inj}$；廣義 Adler（時間平均）$\dot\theta=\omega_0-\omega_{inj}-\frac{1}{q_{max}}\langle\Gamma(\omega_{inj}t+\theta)\,i_{inj}\rangle$ = Eq.(30)（本站 $\Gamma$ 取與 [P3] 相反的符號慣例，故平均項前為 $-$；數值等價，原 PDF Eq.(30) 為 $+$）；sinusoidal lock range $\omega_L=\tfrac{1}{2}I_{inj}\vert\tilde\Gamma_1\vert$ = Eq.(35)，p.2114（已核實） | Fig. 1–3（time-synchronous 注入模型與 ISF 表述） | **injection locking 進階 deep-dive**（05 章，選修）；示範同一個 $\Gamma$ 延伸出 phase noise 以外的用途。 |
| **[P4]** B. Hong & A. Hajimiri, *…Part II: Amplitude Modulation in LC Oscillators, Transient Behavior, and Frequency Division*, IEEE JSSC 54(8):2122–2139 (`BHongGenTheor-II_JSSC2019_Postprint.pdf`, paper_004) | 2019 | 引入 **APF（amplitude perturbation function）**——ISF 的振幅版類比（單位 $\mathrm{A^{-1}}$）：處理注入下的 amplitude modulation、暫態 locking、injection-locked frequency division。理想 LC 中 ISF 與 APF 正交。 | APF 定義 $\Delta(\phi):=\int_0^\infty D(\tau,\phi)\,d\tau$（單位 $\mathrm{A^{-1}}$）= Eq.(19)，p.2126（分解 $D=\tilde\Lambda(\phi)\,d(\tau,\phi)$ = Eq.(18)；理想 LC 正交 = Eq.(26)，p.2128，已核實） | Fig. 5，p.2126（瞬時電荷注入對振盪器的影響：ISF／excess phase／振幅衰減／APF；理想 LC 中 ISF 與 APF 正交） | **APF / 進階 deep-dive**（05 章，選修）；02 章 phase_vs_amplitude_noise 借它說明「為何振幅 noise 會衰減」。 |
| **[P5]** A. Hajimiri & R. Heald, *Design Issues in Cross-Coupled Inverter Sense Amplifier*, Proc. IEEE ISCAS 1998 (`Hajimiri_ISCS_98.pdf`, paper_005) | 1998 | cross-coupled-inverter sense amplifier 的解析設計（regeneration 速度、mismatch offset、FOM）。**與 ISF／phase noise 完全無關**，只因在來源資料夾且作者相同而被收入。 | 無（off-topic，公式未轉錄）`TODO: equations not transcribed because off-topic` | 無 | **邊角註解**——誠實說明 mislabeled；唯一概念連結是 cross-coupled-pair 的 regeneration／正回授機制與 latch/LC 振盪共通。 |

⚠️ = `manual_verification_needed = true`，確切常數／形式仍需對照原始 PDF。詳見
[claims_cross_reference](/01_paper_map/claims_cross_reference) 與
[equation_index](/01_paper_map/equation_index)。

---

## 教學角度：誰負責教什麼

### 哪篇是 ISF 核心基礎

**[P1]** 是整站的地基。LTV/ISF 的所有概念——$\Gamma(\omega_0\tau)$、$q_{max}$
normalization、卷積式相位響應、傅立葉降頻、$1/f^2$/$1/f^3$ 封閉式——全部出自這裡。
02 章（foundations）與 03 章（isf core theory）幾乎逐節對應 [P1] 第 III–IV 節，
lab_01/02/04/05/06/07 都在重現 [P1] 的圖與公式。

### 哪篇延伸到 ring

**[P2]** 把 [P1] 的通用理論落到 **ring oscillator**：同一組 $\Gamma_{rms}^2/q_{max}^2$
邏輯給出累積 jitter（claim **C6**）、$\Gamma_{rms}\propto N^{-3/4}$（claim **C8**），
與「固定功率/頻率下 ring phase noise 幾乎與 $N$ 無關」（claim **C7**）。06 章
[lc_vs_ring](/06_design_insights/lc_vs_ring)、[symmetry](/06_design_insights/symmetry)
與 [lab_03](/04_simulation_labs/lab_03_ring_oscillator_toy_model) 用它。

### 哪篇關於 adjoint / PPV / PSS / PNoise / simulation

**老實說：這 5 篇裡沒有任何一篇是專門講 PPV/adjoint/PSS/PNoise 的。**

- **PPV（perturbation projection vector，擾動投影向量）／adjoint method／Floquet
  theory** 是 ISF 背後嚴謹的數學基礎，但它們來自**更廣的文獻**（如
  Demir–Mehrotra–Roychowdhury 2000、Kaertner），**不在下載的 5 篇 PDF 內**。本站把它們
  當**標準外部文獻**補充，明確標註於 [effective_isf](/03_isf_core_theory/effective_isf)
  （對應 claim **C13**）。
- **PSS（periodic steady-state）／PNoise** 是商用模擬器（如 SpectreRF）萃取 ISF／
  phase noise 的數值方法，同樣**不是這 5 篇的任何一篇**的主題；本站只在概念上引用，
  不宣稱出自下載 PDF。
- 與「simulation」最相關的，反而是 [P1] 自己提到「實際電路要靠 transient impulse
  response 或 adjoint/PSS 萃取 ISF」這個**limitation**——也就是說，模擬萃取被**提及**，
  但沒有專屬論文。本站的所有 lab 都是**教學用 toy model（非 transistor-level）**，
  用 Python 重現概念，不是真實 PSS/PNoise 流程。

### 哪篇修正／批判／補充前人

**[P1] 取代 Leeson 的經驗式。** Leeson 1966 的 $\mathcal{L}$ 表達式（含 $2FkT/P_s$、
$(\omega_0/2Q\Delta\omega)^2$、$1+\omega_{1/f^3}/|\Delta\omega|$）是**經驗擬合**：它能畫出
$1/f^3$、$1/f^2$、floor 三段，但 $F$（noise factor）與 $1/f^3$ corner 都是**事後填的
fitting 參數**，沒有從第一原理算出。[P1] 的貢獻正是：用 ISF 從第一原理**算出**這三段，
並指出 **$1/f^3$ corner 不是 device 的 $1/f$ corner**，而是 $\omega_{1/f}(c_0/c_1)^2$
（[P1] Eq.(24)，claim **C5**）——這是對 Leeson 經驗模型的關鍵修正。Leeson 式本身
**不是**下載的 5 篇 PDF 之一，本站只當對照（見
[equation_index](/01_paper_map/equation_index) 第 19 列，標 reference ⚠️）。

此外 **[P3]** 補充/推廣 **Adler 1946** 的 injection locking 方程；**[P4]** 補上 [P1]/[P3]
缺的**振幅維度**（APF）。Adler 與 Leeson 的原始論文都**不在**這 5 個 PDF 內。

### 哪些公式在不同 paper 是同一件事、不同寫法

| 概念 | [P1] 寫法 | 其他論文寫法 | 統一說明 |
|---|---|---|---|
| 相位敏感度 | $\Gamma(\omega_0\tau)$（ISF） | [P2] 沿用 $\Gamma$；[P3] 寫成 $\Gamma(\theta+\phi)$ 放進注入內積 | 同一個 $\Gamma$，[P3] 只是把它當 injection 的加權核 |
| 相位演化 | $\phi(t)=\frac{1}{q_{max}}\int\Gamma i_n\,d\tau$（Eq.11，noise 視角） | [P3] $\dot\phi=\Delta\omega-\frac{1}{q_{max}}\langle\Gamma i_{inj}\rangle$（injection 視角） | 同一條 LTV 相位方程，一個源是 random noise、一個源是 deterministic injection |
| $1/f^2$ phase noise | Eq.(21) $\propto\Gamma_{rms}^2/q_{max}^2$ | [P2] $\kappa^2\propto\Gamma_{rms}^2/q_{max}^2$（jitter 版） | 同一個 $\Gamma_{rms}^2/q_{max}^2$ 比例，phase noise 與累積 jitter 是同一物理（claim **C3**=**C6** 同源） |
| 敏感度的兩個方向 | 只有相位版 $\Gamma$ | [P4] 加上振幅版 APF $\Lambda$ | $\Gamma$（切向/相位）與 $\Lambda$（徑向/振幅）是 limit cycle 上正交的兩個投影 |

### 哪些符號定義不同、需要統一

不同論文對同一量用不同記號，本站一律以 [notation](/00_overview/notation) 為準：

- **offset 頻率**：[P1] 多用 $\Delta\omega$（rad/s），datasheet/SerDes 用 $\Delta f$（Hz）；
  本站兩者並用，$\Delta\omega=2\pi\Delta f$。
- **ISF 的 DC**：注意 $c_0$ 是傅立葉**係數**，ISF 的 DC**值**是 $c_0/2$（Eq.(12)）——
  算 $1/f^3$ corner（Eq.(24)）時極易出錯，本站反覆提醒。
- **振幅敏感度**：[P4] 的 APF 寫 $\Lambda(\phi)$、單位 $\mathrm{A^{-1}}$，與 ISF 的無因次
  $\Gamma$ **量綱不同**，不可混用。
- **PPV/adjoint/Floquet**：本站不在主幹用其專屬記號（如 Demir 的 $v_1^T(t)$），
  只在 [effective_isf](/03_isf_core_theory/effective_isf) 以外部文獻形式提及。

完整符號對照（含「各論文寫法／備註」一欄）見
[notation 的「各論文符號對照」段](/00_overview/notation)。

## 重點回顧

- **[P1]** = ISF 核心；**[P2]** = ring 延伸；**[P3]/[P4]** = injection locking / APF 進階；
  **[P5]** = sense amplifier，**與 ISF 無關**（誠實標註）。
- **沒有**任何一篇是專屬 PPV/adjoint/PSS/PNoise 論文；那些屬**外部文獻**（如 Demir 2000）。
- [P1] 從第一原理**取代 Leeson 經驗式**，並修正「$1/f^3$ corner ≠ device $1/f$ corner」。
- 不同論文的 $\Gamma$、相位方程、$\Gamma_{rms}^2/q_{max}^2$ 常是同一件事的不同視角；
  符號一律以 [notation](/00_overview/notation) 統一。

## 延伸閱讀

- 每條公式 → 推導頁 → 來源：[equation_index](/01_paper_map/equation_index)
- 每張圖的 script／公式／來源：[figure_index](/01_paper_map/figure_index)
- 教學主張交叉索引（C1–C13）：[claims_cross_reference](/01_paper_map/claims_cross_reference)
- 逐篇精讀：[paper deep dives](/05_paper_deep_dives/)
- 為何來源含一篇 off-topic PDF：[build_report](/00_overview/build_report)
