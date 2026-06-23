---
title: "[P3] Injection Locking & Pulling — Part I (Time-Synchronous Modeling)"
description: Hong–Hajimiri 2019 Part I 精讀：ISF-based time-synchronous model、廣義 Adler 方程、lock range、injection waveform design（進階，核心公式已對照 [P3] 原文核實）。
---

# A General Theory of Injection Locking and Pulling in Electrical Oscillators—Part I

> **先備**：[paper_001](/05_paper_deep_dives/paper_001_general_theory_phase_noise)（[P1] 的 ISF 定義與 Eq.(11) 相位推力）、[fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf)（ISF 的傅立葉諧波 $c_n$） ｜ **接下來**：[paper_004](/05_paper_deep_dives/paper_004_injection_locking_part2)（Part II：APF 振幅、transient、frequency division）。

這是**進階**篇。它把 [P1] 的 ISF 從「自由振盪器的 phase noise」延伸到「振盪器被外部訊號注入
時的 injection locking／pulling（注入鎖定／拉扯）」。核心結果：一個用 ISF 寫成的**單一一階微分
方程**（廣義 Adler 方程）就能預測 lock range（鎖定範圍）、鎖定相位與穩定性，對**任意**振盪器
拓樸與**任意**注入波形都成立——並由此導出「怎麼設計注入波形把 lock range 做到最大」。

> **本頁定位**：進階 deep-dive，**不是核心教學章節**。核心公式（廣義 Adler Eq.(26)、(28)–(30)、
> (33)、(35)）已對照 [P3] 原始 PDF 核實。先確定你已讀懂 [P1] 的 ISF（[paper_001](/05_paper_deep_dives/paper_001_general_theory_phase_noise)）再讀這裡。

## Citation

> **[P3]** B. Hong and A. Hajimiri, *"A General Theory of Injection Locking and Pulling in
> Electrical Oscillators—Part I: Time-Synchronous Modeling and Injection Waveform Design,"*
> IEEE J. Solid-State Circuits, vol. 54, no. 8, pp. 2109–2121, Aug. 2019.
> （檔案 `BHongGenTheor-I_JSSC2019_Postprint.pdf`，paper_003）

## One-sentence contribution

同一個 ISF $\Gamma$ 不只算 phase noise，也能寫出一個 topology-independent 的廣義 Adler 方程，
預測任意振盪器、任意注入波形下的 lock range、鎖定相位與穩定性，並指出如何設計注入波形來放大
lock range（claim C10）。

## Why this paper matters

**injection locking** 是指：一個振盪器被一個頻率接近自身的外部訊號注入時，會「跟著外部訊號
同步」——相位、頻率被外部拉住。當頻率差太大跟不上時，相位週期性滑動，產生不想要的 spurs，這
叫 **injection pulling**。這現象在 PLL、clock distribution、quadrature 產生、frequency division
裡到處都是，既被利用也被害怕。

1946 年 **Adler** 用一條一階相位方程描述 LC 振盪器在**弱、正弦、近自由頻率**注入下的行為。
[P3] 指出 Adler 方程的五大限制（只適用弱注入、只適用 LC、假設正弦注入、需要難以準確量測的
$Q$ 與 $I_{osc}$、且預測對稱 lock range），然後用 ISF 把它**徹底推廣**：

- 用 $\Gamma$ 取代「只對 LC 成立」的 $Q$／$I_{osc}$ 參數——任何能萃取出 ISF 的振盪器都適用。
- 允許**任意注入波形**（不只正弦），於是可以**設計**注入波形使 lock range 最大。
- 自然產生**不對稱 lock range**（真實電路常見，Adler 抓不到）。
- 涵蓋 subharmonic／superharmonic locking（注入頻率在 $\omega_0/m$ 或 $m\omega_0$ 附近）。

## Main assumptions

照 paper_metadata（paper_003.assumptions）：

1. **振盪器 autonomy 與週期時變**（與 ISF 同一基礎）。
2. 注入（擾動）透過 ISF 映射到相位；振幅留到 Part II（APF）處理。
3. **time-synchronous averaging**：在一個週期上做時間同步平均。

> **物理直覺**：phase noise 把擾動換成隨機 noise；injection 把擾動換成一個**確定的、週期性的
> 注入電流 $i_{inj}$**。同一台「ISF 加權後積分」的機器，輸入從隨機變確定，輸出就從統計量
> （$\Gamma_{rms}$、PSD）變成確定的相位動態（鎖定／滑動）。

## Key equations

### 經典 Adler 方程（基準線）

**Original formula**（[P3] Sec. III（SURVEY OF EXISTING MODELS）, 約 p.2111，對照原文 Eq.(15)）：

$$
\frac{d\theta}{dt}=\omega_0-\omega_{inj}-\frac{\omega_0}{2Q}\frac{I_{inj}}{I_{osc}}\sin\theta
$$

寫成規範第 3 節的簡化形式（$\omega_L\equiv\dfrac{\omega_0}{2Q}\dfrac{I_{inj}}{I_{osc}}$、
$\Delta\omega_{inj}\equiv\omega_0-\omega_{inj}$）：

$$
\frac{d\phi}{dt}=-\omega_L\sin\phi+\Delta\omega_{inj}
$$

**Meaning**：注入鎖定的相位差 $\theta$（或 $\phi$）滿足一條一階非線性 ODE。$\omega_L$ 是
（半）lock range。**鎖定**＝存在穩態解 $d\theta/dt=0$，要求 $|\Delta\omega_{inj}|\le\omega_L$。

**Step-by-step（[P3] 對 LC 的簡化推導摘要）**：把注入電流寫成 phasor
$i_{inj}=I_{inj}e^{j\omega_{inj}t}$，對 LC tank 寫 KCL（注入電流要供應 tank 偏離共振時的
無功電流），在弱注入（$I_{inj}\ll I_{osc}$）與慢相位（$|d\theta/dt|\ll\omega_{inj}$）近似下取
實部，即得上式。穩態解給出 lock characteristic 與**對稱** lock range
$\omega_L=\dfrac{\omega_0}{2Q}\dfrac{I_{inj}}{I_{osc}}$。

**Numerical example**：$f_0=5$ GHz、$Q=10$、$I_{inj}/I_{osc}=0.1$。半 lock range

$$
\omega_L=\frac{\omega_0}{2Q}\frac{I_{inj}}{I_{osc}}=\frac{2\pi\times5\times10^{9}}{2\times10}\times0.1=1.57\times10^{8}\ \text{rad/s},
$$

換成頻率 $f_L=\omega_L/2\pi\approx25$ MHz。手感：lock range 隨注入強度線性增加、隨 $Q$ 反比
下降（高 $Q$ 的 LC 比較「固執」、不容易被拉走）。

> **註**：經典 Adler 為標準結果（[P3] Sec. III, p.2111 回顧 Adler [20]）；本頁採通用簡化記法。
> 下一節的**廣義 Adler** 已對照原始 PDF 逐字核實。

### 廣義 Adler 方程 / lock characteristic（本篇核心，已對照原始 PDF 核實 ✓）

[P3] 先把 Hajimiri 的**無因次** ISF $\Gamma$ 換成**有單位**的版本（[P3] Eq.(26), p.2113）：

$$
\tilde\Gamma(x)\equiv\frac{\Gamma(x)}{q_{max}}\qquad[\text{單位 rad/C}]
$$

於是注入電流對相位的瞬時推力，以及換到相對相位 $\theta=\phi-\omega_{inj}t$ 的座標（[P3] Eq.(28)–(29), p.2113）：

$$
\frac{d\phi}{dt}=\tilde\Gamma(\phi)\,i_{inj}(t)
\;\xrightarrow{\ \theta=\phi-\omega_{inj}t\ }\;
\frac{d\theta}{dt}=(\omega_0-\omega_{inj})+\tilde\Gamma(\omega_{inj}t+\theta)\,i_{inj}(t)
$$

對「快變的一個注入週期」做時間同步平均（$\theta$ 慢變視為常數），得 **time-averaged 廣義 Adler 方程**（[P3] Eq.(30), p.2113）：

$$
\frac{d\theta}{dt}=(\omega_0-\omega_{inj})+\frac{1}{T_{inj}}\int_{T_{inj}}\tilde\Gamma(\omega_{inj}t+\theta)\,i_{inj}(t)\,dt
$$

整理成 lock characteristic 形式（[P3] Eq.(33), p.2114）：

$$
\frac{d\theta}{dt}=(\omega_0-\omega_{inj})+\Omega(\theta),\qquad
\boxed{\ \Omega(\theta)=\frac{1}{T_{inj}}\int_{T_{inj}}\tilde\Gamma(\omega_{inj}t+\theta)\,i_{inj}(t)\,dt\ }
$$

其中 $\Omega(\theta)$ 稱為 **lock characteristic**（[P3] Eq.(33), p.2114）：注入造成的平均頻率偏移隨相位差 $\theta$ 的函數。注意平均項前為 **加號**（與 [P3] Eq.(30) 同號慣例）。

**Meaning**：一條一階 ODE，由**有單位 ISF $\tilde\Gamma=\Gamma/q_{max}$** 與**注入波形 $i_{inj}$** 組成，
預測任意振盪器、任意注入波形下的行為（claim C10）。**鎖定**＝存在 $\theta^\*$ 使
$\omega_{inj}-\omega_0=\Omega(\theta^\*)$；lock range ＝ $\Omega(\theta)$ 的值域寬度；**穩定性**由 $d\Omega/d\theta$ 的符號決定。

**正弦注入退化回經典 Adler（[P3] Eq.(34)–(35)）**：若注入為單音 $i_{inj}=I_{inj}\cos\omega_{inj}t$，
只有 ISF 基波 $\tilde\Gamma_1$ 存活：

$$
\Omega(\theta)=\tfrac12 I_{inj}\,\lvert\tilde\Gamma_1\rvert\cos(\theta+\angle\tilde\Gamma_1),
\qquad
\omega_L=\tfrac12 I_{inj}\,\lvert\tilde\Gamma_1\rvert
$$

半 lock range $\omega_L=\frac12 I_{inj}\lvert\tilde\Gamma_1\rvert$（[P3] Eq.(35)）——$\Omega\propto\cos\theta$ 對稱於 0，正是經典 Adler。

**為何一般不對稱**：任意注入時 $\Omega(\theta)$ 含**多個諧波**，值域不再對稱於 0，於是
$\omega_L^+\ne-\omega_L^-$——真實電路常見、Adler 抓不到的不對稱。

**Injection waveform design**：lock range ＝ $\Omega(\theta)$ 的值域寬度，把注入波形 $i_{inj}$ 的諧波
**對齊 ISF $\tilde\Gamma$ 的諧波**（讓內積更大）就能放大 lock range——比「只能加大注入電流」多一個自由度（波形形狀）。

> **已核實**：$\tilde\Gamma=\Gamma/q_{max}$（Eq.26）、pulling 方程 Eq.(28)–(30)、lock characteristic
> Eq.(33)、正弦退化 Eq.(34)、lock range Eq.(35) 皆已對照 [P3] p.2113–2114 原始 PDF 渲染逐字確認。

### lock range = $\Omega(\theta)$ 的值域（toy 圖示）

把 lock characteristic $\Omega(\theta)$ 直接照 [P3] Eq.(33) 的時間同步平均積分畫出來，就能一眼看懂
「lock range ＝ $\Omega(\theta)$ 的值域寬度、邊緣 ＝ $\Omega(\theta)$ 的 max/min」這句話：

![lock characteristic Ω(θ)：左為正弦注入（Γ̃=−sinθ/q_max）給出乾淨餘弦、對稱於 0（ω_L⁺=−ω_L⁻，經典 Adler）；右為諧波豐富注入給出不對稱 Ω，使 ω_L⁺≠−ω_L⁻，三角形/倒三角標出 lock range 上下邊緣。toy model，[P3] Eq.(33)。](/figures/lock_characteristic_omega.png)

- **左 (a) 正弦注入**：單音 $i_{inj}=I_{inj}\cos\omega_{inj}t$ 注入 ideal-LC ISF $\tilde\Gamma=-\sin\theta/q_{max}$。
  只有 ISF 基波存活（Eq.(34)），$\Omega(\theta)$ 是乾淨餘弦、對稱於 0，邊緣
  $\pm\omega_L=\pm\tfrac12 I_{inj}\lvert\tilde\Gamma_1\rvert$（此 toy 值 $=\pm0.50$ rad/s，正是 Eq.(35)）——這就是經典 Adler。
- **右 (b) 諧波豐富注入**：注入帶基波＋刻意定相的二次諧波、ISF 也含二次諧波。多個諧波同時貢獻，
  $\Omega(\theta)$ **不對稱於 0**：上邊緣 $\omega_L^+=+0.56$、下邊緣 $\omega_L^-=-0.63$ rad/s
  （$\omega_L^+\ne-\omega_L^-$）——真實電路常見、Adler 抓不到的不對稱 lock range。

**怎麼讀**：要鎖定，需 $\omega_{inj}-\omega_0=\Omega(\theta^\*)$ 有解；可達的 $\omega_{inj}-\omega_0$ 範圍正是
$\Omega$ 曲線的值域（兩條水平虛線之間）。把注入波形諧波對齊 ISF 諧波（讓 Eq.(33) 的內積更大）就能把這條曲線
撐高、放大 lock range——比「只能加大 $I_{inj}$」多一個自由度（波形形狀）。

> **toy model 聲明**：這是 pedagogical toy model，**非 transistor-level**。ideal-LC 的 $\Gamma=-\sin\theta$ 為嚴格結果；
> 諧波豐富的 ISF 與被設計的注入波形僅為**示意**，只用來暴露不對稱機制。$\Omega(\theta)$ 由 Eq.(33) 的時間平均積分數值算出。
> 完整 script：`simulations/fig_lock_characteristic.py`（產生 `static/figures/lock_characteristic_omega.png`）。

## Key figures

| 論文圖 | 頁 | 內容 | 教學用途 |
|---|---|---|---|
| Fig. 6 | 2113 | block diagram：注入電流的諧波被 ISF 的諧波**濾波**，形成 lock characteristic | 說明 $\Omega(\theta)$ 為何只留下對齊的諧波 |
| Fig. 7 | 2114 | lock characteristic 的**時域**圖：上/下邊緣與 free-running 三種情形的 ISF×injection 面積 | 直覺看 lock range = 每週期淨面積的極值 |

> 本站**刻意不重畫** [P3] 的 Fig. 6／Fig. 7 這兩張進階圖（無對應 transistor-level toy 模擬）；
> 以上頁碼/內容已對照 [P3] 原文。上方 Key equations 內的 $\Omega(\theta)$ 圖是**獨立的 toy 示意**
> （只示範「lock range ＝ $\Omega(\theta)$ 值域」這個概念），**不是** Fig. 6／Fig. 7 的重畫。

## Design insights

- **lock range 可設計**：lock range ＝ $\langle\Gamma\,i_{inj}\rangle$ 隨 $\phi$ 的值域寬度。
  把注入波形 $i_{inj}$ 的諧波對齊 ISF $\Gamma$ 的諧波（讓內積更大），就能放大 lock range——這比
  「只能加大注入電流」多了一個自由度（波形形狀）。
- **拓樸無關**：只要能萃取出 ISF，ring、LC、relaxation 都適用同一條方程；不必再去量難測的
  $Q$ 與 $I_{osc}$。
- **subharmonic／superharmonic locking**：注入頻率在 $\omega_0/m$ 或 $m\omega_0$ 附近時，是
  $\Gamma$ 的對應諧波在做平均——這直接連到 [P4] 的 frequency division（ILFD）。
- **pulling 是同一條方程的另一面**：當 $|\Delta\omega| > $ lock range，$d\phi/dt$ 不為零、相位
  週期性滑動，產生 pulling spurs。設計時要確保工作頻率落在 lock range 內。

## Limitations

照 paper_metadata（paper_003.limitations）：

- **Part I 只談相位**；振幅調變留到 Part II（APF，[P4]）。
- 依賴**準確萃取的 ISF**——ISF 不準，預測就不準。
- 本站把它當**進階 deep-dive，非核心教學章節**；核心廣義 Adler 公式已對照 [P3] 原文核實。

## Relationship to other papers

- **[P1]** 提供 ISF $\Gamma$ 與 Eq.(11) 的相位推力，是本篇的數學起點。
- **[P2]** 提供 ring 的 ISF，與本篇的 ring 注入（及 [P4] 的 ILFD）相連。
- **[P4]** 是直接續集：補上振幅（APF）、transient pulling 與 frequency division，見
  [paper_004](/05_paper_deep_dives/paper_004_injection_locking_part2)。
- 廣義 Adler 方程列在 [equation_index](/01_paper_map/equation_index) 第 20 條（[P3] Eq.(30)/(33)/(35)）。

## What to remember

- **同一個 ISF 既算 phase noise，也算 injection locking**——輸入從隨機 noise 換成確定的
  $i_{inj}$（claim C10）。
- **廣義 Adler 方程**：$\dfrac{d\theta}{dt}=(\omega_0-\omega_{inj})+\dfrac{1}{T_{inj}}\displaystyle\int_{T_{inj}}\tilde\Gamma(\omega_{inj}t+\theta)\,i_{inj}(t)\,dt$（[P3] Eq.(30), p.2113，平均項前為 **加號**）。
- **鎖定** = 存在穩態解 / $|\omega_0-\omega_{inj}|\le\omega_L$；**lock range** = lock characteristic $\Omega(\theta)$ 的值域寬度；正弦注入時 $\omega_L=\tfrac12 I_{inj}\lvert\tilde\Gamma_1\rvert$（[P3] Eq.(35), p.2114）。
- 比 Adler 強在：拓樸無關、任意波形、不對稱 lock range、可設計波形放大 lock range。
- 本頁屬**進階**；核心公式（Eq.26、28–30、33、35）已對照 [P3] p.2113–2114 原始 PDF 核實。

## 延伸閱讀

- 本篇的數學起點 ISF $\Gamma$：[paper_001](/05_paper_deep_dives/paper_001_general_theory_phase_noise)（[P1]）。
- ISF 的傅立葉諧波 $c_n$（為何只有對齊的諧波在 $\Omega(\theta)$ 存活）：[fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf)。
- 直接續集 Part II（APF 振幅、transient pulling、frequency division）：[paper_004](/05_paper_deep_dives/paper_004_injection_locking_part2)（[P4]）。
- 廣義 Adler 在公式索引的位置：[equation_index](/01_paper_map/equation_index)（第 20 條，[P3] Eq.(30)/(33)/(35)）。
- 進階篇在整體路徑中的定位（選修）：[learning_path](/00_overview/learning_path)。
- 五篇論文分工速覽：[paper_summary_table](/01_paper_map/paper_summary_table)。
