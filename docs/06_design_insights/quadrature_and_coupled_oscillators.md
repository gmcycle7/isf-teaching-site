---
title: Quadrature 產生與 coupled-oscillator phase noise
description: 三種 quadrature（I/Q 正交）產生法（parallel/series coupled QVCO、divide-by-2 ILFD、RC-CR polyphase）的 phase-noise 代價；coupled QVCO 的 coupling-strength vs I/Q phase-error vs phase-noise 三角權衡；coupled pair 的 common-mode / differential-mode 雜訊相關性與 ~3 dB；最後把耦合注入接回 [P3] 的 ISF／廣義 Adler 機制。進階頁。
---

# Quadrature 產生與 coupled-oscillator phase noise

> **本頁定位（先講清楚）**：這是一頁**進階（advanced）**設計頁。它把「怎麼生出一對相位差
> $90^\circ$ 的時脈（**quadrature**，正交，即 I/Q）」這個 SerDes／收發機天天要面對的需求，
> 放回本站既有的 **ISF + 廣義 Adler** 機器裡解釋。**前置（prerequisite）**：先讀懂
> [P1] 的 ISF（[isf_definition](/03_isf_core_theory/isf_definition)、[effective_isf](/03_isf_core_theory/effective_isf)）、
> [P3] 的廣義 Adler 注入鎖定（[paper_003](/05_paper_deep_dives/paper_003_injection_locking_part1)），
> 以及 [P4] 的 ILFD／頻率除法（[paper_004](/05_paper_deep_dives/paper_004_injection_locking_part2)）。
> 沒讀過這三頁，本頁的公式會看起來像憑空冒出來。

**quadrature（正交，相位差 $90^\circ$ 的一對訊號 I 與 Q）** 是現代收發機的基本元件：image-reject
mixer（鏡像抑制混頻器）、單邊帶調變、half-rate（半速率）SerDes 的 4 相取樣、CDR 的相位偵測，
全都要一對乾淨、相位誤差小的 I/Q。問題是：**產生 quadrature 本身要付 phase-noise 的代價**，而且
不同產生法的代價結構完全不同。這頁要回答：

> **這頁要回答什麼**：(1) 三種主流 quadrature 產生法各自的 **phase-noise 代價**長什麼樣？
> (2) coupled QVCO（耦合正交壓控振盪器）裡，**coupling strength（耦合強度）↔ I/Q phase error
> （正交相位誤差）↔ phase noise** 為什麼是個三角權衡（trade-off）？(3) 耦合的那一對振盪器，
> 它們的雜訊是 **common-mode（共模）還是 differential-mode（差模）相關**，這如何決定那個有名的
> **$\sim 3$ dB**？(4) 怎麼把「耦合注入」這件事**嚴格接回 [P3] 的 ISF／廣義 Adler**？

> **物理直覺（先講結論）**：耦合 QVCO 就是「**兩個振盪器互相做 injection locking**」——A 的輸出
> 注入 B、B 的輸出注入 A。一旦你這樣看，本站 [P3] 的整套機器立刻就能用：耦合電流 $i_{c}$ 看到的是
> 一個有效 ISF $\tilde\Gamma$，它透過 $\tilde\Gamma$ 的諧波 $c_n$ 把對方的相位「拉」過來，鎖定動態
> 服從廣義 Adler 方程（[P3] Eq.(30)）。耦合越強，兩者相位越被綁死（phase error 越小），但耦合
> device 本身也注入額外雜訊、又把頻率拉離 tank 共振點——這就是三角權衡的來源。

---

## 1. 三種 quadrature 產生法與它們的 phase-noise 代價

先把三條路擺在一起。每條路的「代價」都不一樣，理解差異比記結論重要。

### (a) Coupled QVCO（耦合正交 VCO）

兩個相同的 LC VCO，用一對 **coupling transistor（耦合電晶體）** 把 A 的輸出注入 B、B 的輸出
（反相）注入 A，強迫兩者鎖在固定 $90^\circ$ 相位差。

```mermaid
flowchart LR
  OSCA["VCO A  (I 相)"] -- "coupling i_c  (注入 B)" --> OSCB["VCO B  (Q 相)"]
  OSCB -- "coupling i_c  (反相注入 A)" --> OSCA
```

- **怎麼生 quadrature**：兩個振盪器在「總迴路相位 $=0$」的約束下，被耦合方式強迫成 $90^\circ$（推導見第 4 節，這是 [P3] 廣義 Adler 在「互注入」情形的穩態解）。
- **phase-noise 代價**：理論上**可以比單顆好**——兩顆相同 VCO 的差動／反相耦合會讓**不相關**的
  雜訊部分平均掉（$\sim 3$ dB 的潛在好處，第 3 節）；但**耦合 device 自身的雜訊**會打進來，且
  強耦合把頻率拉離 tank peak、降低有效 $Q$，反而抬高 phase noise。**net 是好是壞，取決於耦合強度**
  （第 2 節的三角權衡）。

### (b) Divide-by-2（÷2）from a $2f_0$ source（ILFD／靜態除頻器）

跑一顆 $2f_0$ 的振盪器，再除以 2。一個 master-slave 觸發器除頻器天生輸出兩個相位差 $90^\circ$
的時脈（因為 $\div 2$ 把一個輸入週期映成輸出半週期 $=90^\circ$）；或用 **ILFD（injection-locked
frequency divider，注入鎖定除頻器）**——把 $2f_0$ 注入一顆 $f_0$ 振盪器，靠 ISF 的**第 2 諧波**鎖定
到 $f_0$（這正是 [paper_004](/05_paper_deep_dives/paper_004_injection_locking_part2) 講的
ILFD，subharmonic locking）。

- **怎麼生 quadrature**：$\div 2$ 的兩個互補輸出（或差動 ÷2 的四個節點）天然相差 $90^\circ$，
  **正交精度由電路對稱性決定，與 tank 失諧無關**——這是它相對 QVCO 的最大優點。
- **phase-noise 代價**：**理想 $\div N$ 把相位雜訊改善 $20\log_{10}N$ dB**。理由：除頻把相位除以
  $N$，相位誤差也除以 $N$，相位功率（$\propto\phi^2$）除以 $N^2$：

$$
\mathcal{L}_{out}(\Delta f)=\mathcal{L}_{2f_0}(\Delta f)-20\log_{10}N
$$

  對 $\div 2$ 即 $-20\log_{10}2=-6.02$ dB。**但**這只算了「源」的雜訊；你還得**先做出一顆乾淨的
  $2f_0$ 振盪器**（高頻 VCO 通常 $Q$ 較低、$q_{max}$ 較小、本身就比較吵），而除頻器（尤其 CML
  latch）自己也加 noise floor。**淨好處要把「$-6$ dB 改善」與「$2f_0$ 源變吵 + 除頻器 noise」相減**。
  此式為標準頻率合成結果（**外部文獻，非本站 5 篇 PDF**），但其物理根據——相位被除以 $N$——
  與本站 [P1] 的相位定義一致；ILFD 的鎖定機制則是 [P4] 的 subharmonic injection locking。

> **dimension／量級 check**：$2f_0=10$ GHz 的源若 $\mathcal{L}(1\text{MHz})=-110$ dBc/Hz，
> 理想 $\div 2$ 得 $5$ GHz、$\mathcal{L}=-116$ dBc/Hz。但若那顆 10 GHz VCO 的 $\Gamma_{rms}/q_{max}$
> 比一顆直接做 5 GHz 的 VCO 差了 6 dB 以上，$\div 2$ 反而沒賺到——這是實務上常見的陷阱。

### (c) RC-CR polyphase filter（多相濾波器）

純被動：一個 RC 低通給一路（相位 $-45^\circ$）、一個 CR 高通給另一路（相位 $+45^\circ$），在
$\omega=1/RC$ 處兩路差 $90^\circ$。多級串接（polyphase）可拓寬頻寬。

- **怎麼生 quadrature**：被動相移，$90^\circ$ 由 $R$、$C$ 匹配決定；不需要第二顆振盪器。
- **phase-noise 代價**：**被動網路不產生新的 phase noise**（理論上），但它有兩個代價：(1)
  **插入損耗（insertion loss）**——每級 RC-CR 衰減 $\sim 3$ dB，要補一級 buffer，buffer 的
  thermal noise 變成 **additive noise**（加成雜訊，劣化 SNR、抬高遠端 noise floor）；(2)
  **正交精度對 $R$、$C$ 的絕對值與頻率敏感**——偏離 $1/RC$ 就有 I/Q 相位與振幅誤差，要靠多級
  與校正。它**不改 close-in（近載波）的 $1/f^2$、$1/f^3$ phase noise**（那是 PLL／VCO 決定的），
  只在**遠端**因 buffer 加成雜訊抬一點 floor。

### 三法對照

| 維度 | coupled QVCO | $\div 2$（ILFD/static） | RC-CR polyphase |
|---|---|---|---|
| 正交來源 | 耦合強迫 $90^\circ$ | $\div 2$ 天然 $90^\circ$ | 被動相移 $\pm45^\circ$ |
| 正交精度受誰決定 | tank 失諧 + 耦合對稱 | 電路對稱（**與失諧無關**） | $R,C$ 匹配 + 頻率 |
| close-in PN | 可比單顆好或壞（看耦合） | $-20\log_{10}N$（**減去源變吵**） | 不改（VCO 決定） |
| 額外雜訊源 | 耦合 device | 高頻源 + 除頻器 | buffer additive noise |
| 主要陷阱 | 強耦合拉頻、$Q$ 降 | $2f_0$ 源天生較吵 | 插損 + 頻寬窄 |
| 接回本站機制 | [P3] 廣義 Adler（第 4 節） | [P4] ILFD（subharmonic） | 純線性網路（與 ISF 無關） |

> 三法的**定性比較與設計取捨**屬振盪器設計常識（**外部文獻，非本站 5 篇 PDF**；標準參考如
> Razavi 收發機教材、Behbahani polyphase 1999）。其中 ILFD 的鎖定動態與 $\div 2$ 的 subharmonic
> injection 機制**嚴格屬於 [P4]**（見 [paper_004](/05_paper_deep_dives/paper_004_injection_locking_part2)）；
> $\div N$ 的 $20\log_{10}N$ 改善是標準頻率合成結果。

---

## 2. Coupled QVCO：coupling strength ↔ I/Q phase error ↔ phase noise

這是 QVCO 設計的**核心三角權衡**。先定義耦合強度，再說明三者怎麼互相拉扯。

### 耦合強度 $m$ 的定義

設每顆 VCO 的核心（−$G_m$）跨導讓它自己起振、提供電流 $I_{core}$；耦合電晶體把對方的訊號
注入本顆，注入電流幅度 $I_{c}$。定義**耦合係數（coupling factor）**

$$
m\equiv\frac{I_{c}}{I_{core}}
$$

$m$ 是無因次的「耦合相對核心有多強」。$m\to 0$ 兩顆解耦、各跑各的；$m$ 大則強綁。

### 三者的拉扯（physics）

**(i) coupling ↑ → I/Q phase error ↓**：耦合提供把兩顆「拉回 $90^\circ$」的恢復力。任何讓兩顆
本徵頻率不同的失配（mismatch，$L$、$C$、$g_m$ 的製程偏差）都會試圖把相位差推離 $90^\circ$；
耦合越強，恢復力越大，殘留相位誤差越小。直覺與量級（**外部文獻，QVCO 標準結果**）：

$$
\Delta\phi_{IQ}\ \approx\ \frac{Q}{m}\,\frac{\Delta\omega_0}{\omega_0}\quad\text{（量級，耦合 }m\text{ 越強誤差越小；}Q\text{ 越大誤差越大）}
$$

其中 $\Delta\omega_0/\omega_0$ 是兩顆 tank 的相對失諧（由失配造成）。等價寫法 $\Delta\phi_{IQ}\approx\Delta\omega_0/\omega_L$，
其中 $\omega_L=\dfrac{m\,\omega_0}{2Q}$ 是互注入的 Adler lock range（[P3] Eq.(35) 形式；外部 QVCO 文獻）。
直覺：耦合越強（$m$ 大）lock range 越寬、恢復力越大，殘留 I/Q 誤差越小；但 tank 越尖（$Q$ 大）
lock range 越**窄**，同樣失配反而**更難**被拉回 $90^\circ$，I/Q 相位誤差**越大**。

> **數值例（量級）**：取 $m=0.3$、$Q=10$、tank 失配 $\Delta\omega_0/\omega_0=0.1\%$，則
> $$
> \Delta\phi_{IQ}\approx\frac{Q}{m}\,\frac{\Delta\omega_0}{\omega_0}=\frac{10}{0.3}\times0.001\approx0.033\ \text{rad}\approx1.9^\circ.
> $$
> 也就是高 $Q$（$Q=10$）的尖 tank，即使失配壓到 $0.1\%$，$m\sim0.3$ 的耦合也只能把 I/Q 誤差
> 收到約 $1.9^\circ$；要再小就得**加強耦合**（$m$ 大）或**降失配**（$\Delta\omega_0/\omega_0$ 小）。
> 單位檢查：$\dfrac{(\text{無因次})}{(\text{無因次})}\times(\text{無因次})=$ 無因次 $=$ rad ✓。
> 反過來看，要做到 $0.5^\circ\approx8.7\times10^{-3}$ rad 以內（同樣 $\Delta\omega_0/\omega_0=0.1\%$），需 $Q/m\lesssim 8.7$，
> 即 $m\gtrsim Q/8.7\approx1.15$——對 $Q=10$ 的 tank 這意味著相當強的耦合，這正是「高 $Q$ QVCO 反而更吃耦合強度」的定量界。

**(ii) coupling ↑ → phase noise ↑（兩個機制）**：

- **耦合 device 自身注入雜訊**：耦合電晶體和核心 device 一樣有 thermal／flicker noise，它**直接打在
  tank 節點**上、看到一個有效 ISF，貢獻額外的 phase noise（第 4 節用 ISF 量化）。耦合越強（耦合
  device 越大、電流越大），這份雜訊越大。
- **耦合把振盪頻率拉離 tank peak、降低有效 $Q$**：耦合注入是一股與 tank 電壓**不同相位**的電流，
  振盪器必須偏離 tank 共振頻率才能讓總迴路相位 $=0$（這是 injection pulling 的穩態）。偏離共振
  → tank 在工作頻率的相位斜率（即有效 $Q$）變小 → 由 Leeson／ISF，phase noise $\propto 1/Q^2$
  抬高。**這是強耦合 QVCO 的主要 phase-noise 懲罰**。

**(iii) net trade-off**：所以 QVCO 設計是在「**夠強的耦合壓低 I/Q phase error**」與「**過強的耦合
抬高 phase noise**」之間找甜蜜點。實務經驗（**外部文獻**）：存在一個最佳 $m$（典型 $m\sim 0.2\!-\!0.5$
量級，視拓樸），太小則 I/Q error 與失鎖風險大，太大則 phase noise 被有效 $Q$ 降低主導。

### parallel vs series coupling（兩種接法的差別）

| | **parallel coupling** | **series coupling** |
|---|---|---|
| 耦合 device 怎麼接 | 與核心 −$G_m$ device **並聯**接到 tank 節點 | **串接**在核心 device 與 tail 之間 |
| 電流分配 | 耦合與核心**爭同一個 tank 節點電流** | 耦合電流流經核心，**共用偏流** |
| phase-noise 直覺 | 耦合 device 直接加 noise；頻率拉移較大 | 耦合不另耗電流、頻率拉移較小 → 一般 **PN 較佳** |
| 代價 | 較吵但設計簡單 | headroom（電壓裕度）較緊、設計較難 |

> **series coupling 通常 phase noise 較好**：因為耦合不另開一條注 tank 的吵電流支路、頻率拉移
> 較小、有效 $Q$ 保留較多。這是 QVCO 文獻的核心結論之一（**外部文獻，非本站 5 篇 PDF**；
> 標準參考如 Andreani QVCO 系列、Romanò *parallel vs series QVCO*）。本站不重畫其電路圖。

> **設計旋鈕（coupled QVCO）**：
> 1. **耦合強度 $m$**：折衷 I/Q error（要 $m$ 大）與 phase noise（要 $m$ 小）→ 取中間最佳值。
> 2. **耦合接法**：series 一般優於 parallel（頻率拉移小、不另耗流）。
> 3. **降耦合 device 雜訊**：耦合電晶體用大尺寸、低 $g_m$／低 flicker，減少它注入的 $\Gamma_{rms}$。
> 4. **降失配**：好的 layout、共質心（common-centroid）→ 同樣 $m$ 下 I/Q error 更小，可用較弱耦合。

---

## 3. 雜訊相關性：common-mode vs differential-mode 與 ~3 dB

QVCO 是「兩顆相同振盪器」，所以必須分清楚**哪些雜訊在兩顆之間相關、哪些不相關**——這決定那個
有名的 $\sim 3$ dB 到底是賺還是賠。

### 兩種雜訊的記帳

把第二顆（Q）想成第一顆（I）的「複製品」。對 I/Q 兩路各自的 phase noise 功率：

- **differential-mode / 不相關雜訊**（每顆 VCO 核心 device 自己的 thermal noise，兩顆**獨立**）：
  兩顆的相位雜訊**不相關**。當你把兩顆**強耦合綁成同一個振盪系統**，輸出的相位由兩顆**共同**決定
  ——兩份不相關功率平均，輸出 phase noise 比**單顆**低 $\sim 3$ dB（$10\log_{10}2$）。這是
  QVCO「用兩顆換 3 dB」的理論好處。

$$
\mathcal{L}_{QVCO}\ \approx\ \mathcal{L}_{single}-10\log_{10}2\ =\ \mathcal{L}_{single}-3.01\ \text{dB}\quad\text{（僅就不相關核心雜訊而言）}
$$

- **common-mode / 相關雜訊**（同時打在兩顆、或耦合路徑共用的雜訊，例如共用 tail、共用 bias、
  耦合 device）：兩顆的擾動**完全相關**，平均**不會**降低它——相關功率不享受 $\sqrt{N}$ 平均。
  這份雜訊**抵銷掉部分 3 dB 好處**。

### 帳要怎麼算（關鍵 caveat）

> **$\sim 3$ dB 的誠實版本**：「兩顆 → $-3$ dB」只對**不相關**雜訊成立，且**前提是耦合 device 不另
> 引進可觀的相關雜訊、也不把有效 $Q$ 拉低**。實務上：
> 1. 核心 device 的不相關 thermal noise：享受 $-3$ dB ✓。
> 2. 耦合 device 注入的雜訊：是**新增**的、且常**相關**（共用耦合路徑）→ 抵銷部分好處。
> 3. 有效 $Q$ 因耦合拉頻而降：phase noise $\propto 1/Q^2$ 抬高 → 再吃掉一些。
>
> **所以真實 QVCO 不一定比單顆好 3 dB，可能只好 1–2 dB，甚至在強耦合下更差**。$\sim 3$ dB 是
> 「兩顆不相關源平均」的**上限**，不是保證值（**外部文獻，非本站 5 篇 PDF**）。

> **記帳口訣**：**相關 ↔ 振幅相加（總功率 $\propto N^2$，相對單源不下降）→ 不享受平均；
> 不相關 ↔ 功率相加（總功率 $\propto N$）→ 享受 $-10\log_{10}N$。** 這跟第 1 節 $\div N$ 改善 $20\log_{10}N$（相位被除以 $N$，是
> deterministic 的相關縮放）是同一套相關性記帳邏輯的兩面。

---

## 4. 把耦合注入接回 ISF / 廣義 Adler（[P3]）

這是本頁的數學核心：**耦合 QVCO 的鎖定動態，就是 [P3] 的廣義 Adler 方程套在「互注入」上**。
我們不另造新理論，直接把本站
[paper_003](/05_paper_deep_dives/paper_003_injection_locking_part1) 的式子拿來用。

### 第 1 步：耦合電流看到的有效 ISF

從 A 注入 B 的耦合電流 $i_{c}(t)$，和任何注入電流一樣，透過**有單位 ISF**
$\tilde\Gamma(x)=\Gamma(x)/q_{max}$（單位 rad/C，[P3] Eq.(26), p.2113）推動 B 的相位。也就是說，
耦合注入**不是什麼特別的東西**——它看到的就是 B 這顆振盪器在注入節點的有效 $\tilde\Gamma$，並透過
$\tilde\Gamma$ 的傅立葉諧波 $c_n$（[P1] Eq.(12)）把對方的訊號「收」進來：諧波對齊得越好，耦合
（鎖定）越有效。

耦合 device 自身的雜訊 $i_{c,n}(t)$ 也走**同一條** $\tilde\Gamma$，所以它對 phase noise 的貢獻就是
[P1] 那套：$\mathcal{L}\propto\Gamma_{rms}^2/q_{max}^2$（[P1] Eq.(21), p.185，把 $\Gamma$ 換成耦合注入
看到的有效 ISF）。**這就是第 2 節「耦合 device 注入額外雜訊」的量化出口**。

### 第 2 步：互注入的廣義 Adler

把 B 對 A 的注入也寫上。對振盪器 A，相對相位 $\theta_A=\phi_A-\phi_{ref}$ 服從 **[P3] 的時間平均
廣義 Adler 方程**（[P3] Eq.(30), p.2113，平均項前為**加號**）：

$$
\frac{d\theta_A}{dt}=(\omega_{0,A}-\omega_{ref})+\frac{1}{T}\int_{T}\tilde\Gamma\big(\omega_{ref}t+\theta_A\big)\,i_{c,B\to A}(t)\,dt
$$

其中 $i_{c,B\to A}$ 是 B 注入 A 的耦合電流（正比於 B 的輸出 $\propto\cos(\omega_{ref}t+\theta_B)$）。
對 B 對稱地寫一條。**重點**：耦合 QVCO 不過是**兩條這樣的 Adler 方程互相耦合**——A 的方程裡
出現 $\theta_B$、B 的方程裡出現 $\theta_A$。整理成 [P3] 的 **lock characteristic** 形式
（[P3] Eq.(33), p.2114）：

$$
\frac{d\theta_A}{dt}=(\omega_{0,A}-\omega_{ref})+\Omega(\theta_A-\theta_B)
$$

$\Omega(\cdot)$ 即耦合造成的平均頻率偏移隨**相對相位差**的函數（耦合越強，$\Omega$ 的值域越寬，
鎖定越牢）。

### 第 3 步：穩態解 → 為什麼是 $90^\circ$

QVCO 的耦合方式（A 同相注入 B、B **反相**注入 A，差一個負號）使得穩態
（$d\theta_A/dt=d\theta_B/dt=0$、兩顆同頻）下，兩條 Adler 方程**只能在相位差**

$$
\theta_A-\theta_B=\pm 90^\circ
$$

時自洽——正號或負號（I 領先或落後 Q）是兩個對稱的穩定解之一，由起振瞬間決定。**$90^\circ$ 不是
湊出來的，是互注入 Adler 方程的穩態約束**。任何 tank 失諧（$\omega_{0,A}\ne\omega_{0,B}$）會把這個
$90^\circ$ 推偏一點，偏多少由 $\Omega$ 的斜率（即耦合強度）抵抗——這正是第 2 節
$\Delta\phi_{IQ}\propto Q/m$ 的微分方程版本。

> **量級／dimension check**：$\Omega(\theta)$ 與 $(\omega_0-\omega_{ref})$ 同單位 rad/s ✓。
> 耦合強 → $\Omega$ 值域寬 → 同樣失諧 $(\omega_{0,A}-\omega_{0,B})$ 只需很小的相位偏移就能
> 由 $\Omega(\theta_A-\theta_B)$ 補回 → I/Q 誤差小。耦合弱 → $\Omega$ 窄 → 失諧一大就無解（失鎖，
> 兩顆不再同頻、相位週期滑動，這就是 [P3] 講的 injection **pulling**）。

### 第 4 步：把三件事縫成一張圖

| 設計現象（第 2、3 節） | 對應的 [P3]／ISF 量 |
|---|---|
| 耦合強度 $m$ | $\Omega(\theta)$ 的值域寬度（= lock range；[P3] Eq.(33)） |
| I/Q phase error 隨失配 | 失諧除以 $\Omega$ 斜率（耦合強 → 斜率陡 → 誤差小） |
| 耦合 device 額外 phase noise | 耦合注入看到的有效 $\Gamma_{rms}$ 經 [P1] Eq.(21) |
| 強耦合拉頻、$Q$ 降 | 穩態 $\theta^\*\ne 0$ → 工作頻率偏離 tank peak |
| $90^\circ$ 自然出現 | 反相互注入 Adler 方程的穩態約束 |

**一句話**：coupled QVCO ＝ 兩顆振盪器用 [P3] 的廣義 Adler 互相鎖定；耦合電流走的是
[P1] 的 ISF，所以「鎖定（quadrature）」與「額外 phase noise」其實是**同一個 $\tilde\Gamma$ 的兩面**
——和 [P3] 講「同一個 ISF 既算 phase noise、也算 injection locking」完全一致。

---

## 適用與失效條件

| 條件 | 成立時 | 失效時會怎樣 |
|---|---|---|
| 弱～中耦合、相位線性 | 廣義 Adler（[P3] Eq.(30)）成立、$90^\circ$ 穩態解存在 | 強耦合 → 振幅調變（要 [P4] APF）、ISF 本身被改 |
| 兩顆 VCO 近乎相同、失配小 | I/Q error $\propto Q/m$、$\sim 3$ dB 上限可逼近 | 大失配 → I/Q error 大、甚至失鎖（pulling） |
| 耦合 device 雜訊／相關性可忽略 | $-3$ dB（不相關核心雜訊平均）成立 | 耦合/共用雜訊相關 → 抵銷 3 dB、可能更差 |
| 工作頻率仍近 tank peak | 有效 $Q$ 保留、PN 不被 $1/Q^2$ 懲罰 | 強耦合拉頻 → 有效 $Q$ 降、close-in PN 抬高 |
| $\div 2$ 源乾淨 | $-20\log_{10}N$ 改善淨賺 | $2f_0$ 源太吵 / 除頻器 noise → 改善被吃光 |

---

## 重點回顧

- **三種 quadrature 產生法的代價結構不同**：coupled QVCO 的代價是耦合 device 雜訊 + 拉頻降 $Q$（淨值看耦合強度）；
  $\div 2$（ILFD）理想改善 $-20\log_{10}N$，但要先有乾淨的 $2f_0$ 源；RC-CR polyphase 不產生新 close-in PN，
  代價是插損 + buffer additive noise + 頻寬窄。
- **coupled QVCO 的三角權衡**：coupling ↑ → I/Q phase error ↓（恢復力強），但 phase noise ↑（耦合 device 注雜訊 +
  拉頻降有效 $Q$）→ 存在最佳耦合強度 $m$。**series coupling 一般優於 parallel**（頻率拉移小、不另耗流）。
- **$\sim 3$ dB 是上限不是保證**：只有**不相關**的核心 device 雜訊享受 $-10\log_{10}2$；耦合/共用雜訊是**相關**的，
  抵銷部分好處；拉頻降 $Q$ 再吃掉一些 → 真實 QVCO 常只好 1–2 dB，強耦合下甚至更差。
- **接回 [P3]**：耦合 QVCO ＝ 兩條互注入的**廣義 Adler 方程**（[P3] Eq.(30), p.2113）；耦合電流走
  有單位 ISF $\tilde\Gamma=\Gamma/q_{max}$（[P3] Eq.(26)），$90^\circ$ 是反相互注入的穩態約束，
  lock range ＝ $\Omega(\theta)$ 值域（[P3] Eq.(33)）。鎖定與額外 phase noise 是同一個 $\tilde\Gamma$ 的兩面。
- **誠實標註**：QVCO 的拓樸比較、$\Delta\phi_{IQ}$ 量級式、$\sim 3$ dB、parallel/series 結論皆為
  **外部文獻（非本站 5 篇 PDF）**；其鎖定動態嚴格繫於 [P3]，$\div 2$/ILFD 的 subharmonic 機制嚴格繫於 [P4]。

## 延伸閱讀

- 廣義 Adler／注入鎖定（本頁鎖定動態的來源）：[paper_003](/05_paper_deep_dives/paper_003_injection_locking_part1)（[P3] Eq.(30)）
- ILFD／頻率除法／subharmonic locking（$\div 2$ 那一路）：[paper_004](/05_paper_deep_dives/paper_004_injection_locking_part2)
- quadrature 怎麼用到 SerDes（half-rate 取樣、CDR 相位偵測）：[serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)
- 有效 ISF $\Gamma_{eff}=\Gamma\cdot\alpha$（耦合注入看到的 ISF）：[effective_isf](/03_isf_core_theory/effective_isf)
- 真實拓樸的 ISF（cross-coupled LC VCO 的 tank/tail noise）：[real_oscillator_topologies](/06_design_insights/real_oscillator_topologies)
- 相位 vs 振幅雜訊的幾何（為何強耦合要看振幅）：[phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise)

## 外部文獻（不在下載的 5 篇 PDF 內）

- **[E-Andreani-QVCO]** P. Andreani, A. Bonfanti, L. Romanò, C. Samori, *"Analysis and Design of a 1.8-GHz
  CMOS LC Quadrature VCO,"* IEEE J. Solid-State Circuits, vol. 37, no. 12, pp. 1737–1747, Dec. 2002.
  （QVCO 的 coupling-strength vs phase-noise vs I/Q error 三角權衡之權威分析；本頁第 2、3 節之依據。
  卷期/頁碼已查證。）
- **[E-Romano-QVCO]** L. Romanò, S. Levantino, C. Samori, A. L. Lacaita, *"Multiphase LC Oscillators,"*
  IEEE Trans. Circuits Syst. I, vol. 53, no. 7, pp. 1579–1588, Jul. 2006（及相關 parallel-vs-series
  QVCO 文獻）。（parallel vs series coupling 的 phase-noise 比較依據。卷期/頁碼已查證。）
- **[E-Behbahani-PPF]** F. Behbahani, Y. Kishigami, J. Leete, A. A. Abidi, *"CMOS Mixers and Polyphase
  Filters for Large Image Rejection,"* IEEE JSSC, vol. 36, no. 6, pp. 873–887, Jun. 2001.
  （RC-CR polyphase filter 的設計與插損／頻寬權衡依據。卷期/頁碼已查證。）
- **$\div N$ 改善 $20\log_{10}N$ dB**：標準頻率合成結果（見任何 PLL／frequency synthesis 教材，
  如 Razavi *RF Microelectronics*）。**不在 5 篇 PDF 內**；其物理根據（相位被除以 $N$）與本站 [P1]
  相位定義一致。
