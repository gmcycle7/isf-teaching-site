---
title: 相位雜訊量測與 spur
description: 量 L(f) 的三種方法（spectrum analyzer 直接法、PLL/delay-line frequency discriminator、cross-correlation）、確定性 spur 與隨機 phase noise 的分辨與成因對策，以及如何讀一張真實 PN 圖、從 1/f³/1/f²/floor 三段反推設計訊息。
---

# 相位雜訊量測與 spur

> **先備**：[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)（$\mathcal{L}\approx\tfrac12 S_\phi$、$1/f^2$ 中段，反推 $S_i$ 用得到）、[fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf)（spur 經 ISF 第 $n$ 諧波 $c_n$ 下變頻的機制）、[symmetry](/06_design_insights/symmetry)（$1/f^3$ corner 反推 $c_0/c_1$ 對稱性）｜ **接下來**：[real_oscillator_topologies](/06_design_insights/real_oscillator_topologies)、[lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth)

前面幾章把 phase noise（相位雜訊）從 ISF 一路推到 $\mathcal{L}(\Delta f)$（SSB phase noise，單邊帶相位雜訊，單位 dBc/Hz），都是「理論預測」。這頁回到實驗台前，回答三個量測現場一定會碰到的問題：

1. **怎麼量 $\mathcal{L}(f)$**？三種主流方法——spectrum analyzer（頻譜分析儀，SA）直接法、PLL/delay-line frequency discriminator（鑑頻器去載波）、**cross-correlation（互相關，兩條獨立通道相關把儀器本底開根號降低）**——各自的原理、優缺點、適用範圍。
2. **spur（spurious tone，確定性邊帶）和隨機 phase noise 怎麼分辨**？一個是離散 tone（單位 dBc，**不是** /Hz），一個是連續譜（/Hz）。它們在頻譜上長得不一樣、成因不同、對策也不同。
3. **怎麼讀一張真實的 PN 圖**？把 $1/f^3$、$1/f^2$、floor 三段、各 corner、spur 標出來，再**反推設計訊息**。

> **物理直覺（先講結論）**：量 phase noise 的本質困難是——**待測物（DUT）的相位抖動極小**（離載波 1 MHz 處常在 $-100$ 到 $-150$ dBc/Hz），而你手上的儀器**自己也會抖**。所以所有方法都在做同一件事：**想辦法把載波那根又高又乾淨的大訊號「拿掉」，只留下旁邊微弱的雜訊裙邊**，並且**讓量測系統自己的本底（noise floor）比 DUT 還低**。三種方法就是三種「拿掉載波 + 壓低本底」的工程手段。
>
> **誠實聲明**：本頁的**量測儀器架構與標準**（PN spectrum analyzer、delay-line/PLL discriminator、cross-correlation analyzer，如 Keysight E5052B、R&S FSWP、Holzworth 等）屬**外部工程文獻與儀器手冊，不在本站下載的 5 篇 PDF 內**。本頁用標準量測理論補充，並把每個結果接回 [P1] 的 ISF 框架。涉及的物理（去載波、PSD 估計、相關平均）皆為通用 DSP/通訊知識；具體儀器型號僅作舉例。

---

## 第 1 部分：量 $\mathcal{L}(f)$ 的三種方法

先把要量的東西寫清楚。把振盪器輸出寫成

$$
v(t)=V_0\,\big[1+a(t)\big]\cos\!\big(\omega_0 t+\phi(t)\big),
$$

其中 $a(t)$ 是 AM noise（振幅雜訊）、$\phi(t)$ 是 PM noise（相位雜訊，本站主角）。我們要的是相位部分的單邊功率譜

$$
\mathcal{L}(\Delta f)\approx\tfrac12 S_\phi(\Delta f)\quad[\text{dBc/Hz}],
$$

（小角近似，規範 Eq.16；見 [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)）。三種方法差在「如何從 $v(t)$ 把 $\phi(t)$ 乾淨地分離出來、且不被儀器本身的相位雜訊污染」。

### 方法 A：spectrum analyzer 直接法

**原理**：直接把 DUT 接上頻譜分析儀，看載波 $f_0$ 旁邊的功率譜裙邊。在 offset $\Delta f$、解析頻寬 $\text{RBW}$ 下量到的邊帶功率 $P_{SSB}(\Delta f)$，相對載波功率 $P_{carrier}$，歸一到 1 Hz：

$$
\mathcal{L}(\Delta f)=10\log_{10}\!\left(\frac{P_{SSB}(\Delta f)}{P_{carrier}}\right)-10\log_{10}(\text{ENBW}/1\,\text{Hz})\ +\ 2.5\,\text{dB}.
$$

- 第一項是「邊帶比載波低幾 dB」（dBc）。
- 第二項把量測頻寬歸一到 per-Hz（用等效雜訊頻寬 ENBW 而非標稱 RBW；例如 ENBW $\approx1$ kHz 要減 $10\log_{10}1000=30$ dB）。
- $+2.5$ dB 是常見的修正：log 檢波器配 video/sample 平均對高斯雜訊**低估約 $2.5$ dB**（Rayleigh-log 偏差），故須「**加回**」約 $2.5$ dB 才回到真實雜訊功率（外部文獻：Keysight/Agilent AN-1303 頻譜分析基礎）。**這是 toy/illustrative 的近似**，實機由儀器內建 PN 量測模式自動補。

**單位檢查**：$10\log_{10}(\text{無因次 W/W})-10\log_{10}(\text{Hz})=\text{dBc}-\text{dB(Hz)}=\text{dBc/Hz}$ ✓。

**優點**：

- 設定最快，一台 SA 就能做；同時看得到 spur（離散 tone）與寬頻雜訊全貌。

**致命缺點——SA 自己的相位雜訊**：

- 你量到的不是 DUT 的 $S_\phi^{DUT}$，而是 DUT 與 SA 本地振盪器（LO）相位雜訊**之和**：
  

$$
S_\phi^{meas}(\Delta f)=S_\phi^{DUT}(\Delta f)+S_\phi^{SA\,LO}(\Delta f).
$$

  只要 DUT 比 SA 的 LO 乾淨，量到的就是 SA 自己——**你量的是儀器，不是 DUT**。
- 此外 SA 量到的是 AM+PM 的總和；近載波通常 PM 主導，但要分離 AM/PM 它做不到。

**適用範圍**：DUT 相位雜訊**明顯比 SA 的 LO 差**（例如量一顆 noisy 的自由運行 ring VCO）、或只需快速看 spur 與大致裙邊形狀時。**不適合**量低雜訊參考源（OCXO、低噪 PLL），因為會撞到 SA 本底。

### 方法 B：PLL / delay-line frequency discriminator（去載波法）

直接法的問題是「載波那根大訊號還在，旁邊小雜訊被儀器動態範圍與 LO 雜訊壓住」。**去載波（carrier suppression）**的想法：先把載波那根 $\cos(\omega_0 t)$ 用相位偵測器抵銷掉，只把 $\phi(t)$ 變成**基頻電壓**送進低頻 FFT 分析儀（它的本底遠低於 RF SA）。有兩種去載波法：

#### B-1：PLL（phase-locked loop）法——用乾淨參考鎖相

把 DUT 與一顆**更乾淨的參考源**送進 mixer（混頻器當相位偵測器），用 PLL 讓兩者鎖在 $90^\circ$（quadrature，正交）。在 quadrature 下 mixer 輸出對相位差是線性的：

$$
v_{out}(t)=K_\phi\,\big[\phi_{DUT}(t)-\phi_{ref}(t)\big],
$$

$K_\phi$ 是相位偵測增益（V/rad）。PLL 環路頻寬設得很低，使得在關心的 offset 上 $\phi_{ref}$ 被環路追掉、只剩 DUT 的相位起伏轉成電壓。對 $v_{out}$ 做 FFT、除以 $K_\phi^2$ 得 $S_\phi^{DUT}$。

- **優點**：本底可以做到非常低（受限於參考源、mixer、基頻放大器），是測**低雜訊源**的金標準之一；天然只測 PM（mixer 在 quadrature 對 AM 不敏感）。
- **缺點**：需要一顆**比 DUT 更乾淨的參考源**（最大痛點）；要鎖相，DUT 要夠穩；PLL 環路頻寬以下的近載波 offset 會被環路吃掉，要做環路轉移修正。

#### B-2：delay-line（延遲線）frequency discriminator——把自己當參考

當你**找不到更乾淨的參考源**（例如量一顆本身就是頂尖低噪的 source）時，用 DUT **自己延遲一段** $\tau_d$ 當參考。把訊號分兩路，一路經延遲線 $\tau_d$、一路經移相器調到 quadrature，送進 mixer。延遲把**頻率起伏**轉成相位差，mixer 解出來。其轉移函數（把頻率雜訊 $S_{\Delta f}$ 變成輸出）為

$$
\big|H(\Delta f)\big|^2=\big(2\pi\tau_d\big)^2\,\operatorname{sinc}^2(\Delta f\,\tau_d),\qquad \operatorname{sinc}(x)=\frac{\sin(\pi x)}{\pi x},
$$

這裡 $H$ 把**頻率起伏** $\delta f$ 映成輸出。鑑頻器感測的是頻率起伏，而頻率是相位的微分，故頻率譜與相位譜的橋接關係為 $S_{\delta f}(\Delta f)=\Delta f^2\,S_\phi(\Delta f)$（每多一次微分在頻域多一個 $\Delta f$ 因子）。把它代回，等於在分母多出一個 $\Delta f^2$（即 $(2\pi\tau_d)^2\to(2\pi\,\Delta f\,\tau_d)^2$），

於是

$$
S_\phi(\Delta f)=\frac{S_{v}(\Delta f)}{K_\phi^2\,(2\pi\,\Delta f\,\tau_d)^2\,\operatorname{sinc}^2(\Delta f\,\tau_d)}.
$$

- **物理意義**：延遲線把**頻率鑑別**（discriminator）成相位，靈敏度 $\propto\tau_d$——延遲越長越靈敏。
- **缺點**：靈敏度 $\propto\tau_d$，但 $\operatorname{sinc}$ 在 $\Delta f=k/\tau_d$ 有**零點（null）**——延遲太長，可用 offset 範圍變窄、且零點處盲掉；延遲線本身有損耗（衰減訊號、抬高本底）。是「靈敏度 vs 頻率覆蓋」的取捨。
- **優點**：**不需要外部參考源**，自給自足；適合量本身極乾淨、找不到更好參考的 source。

**單位檢查（delay-line）**：$S_v$ 是 $\text{V}^2/\text{Hz}$，除以 $K_\phi^2$（$\text{V}^2/\text{rad}^2$）得 $\text{rad}^2/\text{Hz}$；分母 $(2\pi\Delta f\tau_d)^2$ 無因次，整體 $\text{rad}^2/\text{Hz}=S_\phi$ ✓。

### 方法 C：cross-correlation（互相關）——把不相關的儀器本底開根號降低

這是現代商用 PN analyzer（如 E5052B、FSWP、Holzworth）的看家本領，**不在 5 篇 PDF 內**，屬外部儀器文獻。它解決 B 法的根本限制：**量測通道自己的本底**。

**核心想法**：把同一顆 DUT 的訊號**分成兩路**，各自接**一條完全獨立**的去載波 + 量測通道（各有自己的參考源/mixer/放大器，本底互不相關）。兩路輸出分別是

$$
y_1(t)=\phi_{DUT}(t)+n_1(t),\qquad y_2(t)=\phi_{DUT}(t)+n_2(t),
$$

其中 $\phi_{DUT}$ 是**兩路共有**的 DUT 相位（相關），$n_1,n_2$ 是各通道**獨立**的儀器本底（不相關）。對兩路做**互功率譜**（cross-spectrum）$S_{y_1 y_2}=\langle Y_1 Y_2^*\rangle$ 並平均 $M$ 次：

$$
S_{y_1 y_2}(\Delta f)=\underbrace{S_{\phi\phi}(\Delta f)}_{\text{相關，留下}}+\underbrace{\frac{1}{\sqrt{M}}\big(\text{不相關本底項}\big)}_{\text{隨平均次數開根號下降}}.
$$

- **關鍵物理**：DUT 相位在兩路**相關**，互相關裡**同相累加**、保留全額；兩路的儀器本底**不相關**，互相關裡是隨機相位、平均 $M$ 段後以 **$1/\sqrt{M}$** 收斂下去（每 10 倍平均，本底降 $5$ dB，即 $10\log_{10}\sqrt{10}=5$ dB）。
- **能降多少**：相對單通道本底，可額外降

$$
\Delta_{floor}=5\log_{10}M\ \text{[dB]}\quad(\text{每 }\times10\text{ 平均降 }5\text{ dB}).
$$

  要降 $20$ dB 需 $M=10^4$ 次平均；降到極限後受限於**通道間殘餘相關**（共用的供電、參考分配、熱）與量測時間。

**優點**：本底可壓到**比任何單一參考源還低**——量得到世界級低噪源；同一架構可同時分離 AM 與 PM。
**缺點**：要**兩套**獨立硬體，貴；近載波要大量平均、**量測時間長**（$M$ 大）；殘餘相關設定上限。
**適用範圍**：量**最低雜訊**的 source（OCXO、低噪合成器、整合 PLL），需要逼近物理極限本底時的首選。

### 三法比較表

| 方法 | 去載波手段 | 需外部參考？ | 本底（相對）| 主要限制 | 最適合 |
|---|---|---|---|---|---|
| A. SA 直接法 | 無（直接看裙邊）| 否 | 高（=SA 自身 LO）| 量到 SA 自己；不分 AM/PM | 快速看 spur／高噪 DUT |
| B-1. PLL 鎖相 | mixer + PLL 鎖 quadrature | **要更乾淨參考** | 低 | 受參考源限制；近載波被環路吃 | 低噪源（有好參考時）|
| B-2. delay-line | 自延遲 $\tau_d$ 當參考 | 否（自參考）| 中–低 | $\operatorname{sinc}$ 零點、延遲損耗 | 無更好參考的乾淨源 |
| C. cross-correlation | 兩路各去載波 + 互相關 | 視架構（常用內參）| **最低（$\propto1/\sqrt{M}$）** | 貴、慢、殘餘相關設限 | 世界級低噪源 |

> **一句話記住**：A 法量的是「DUT 與儀器的和」；B 法用去載波把儀器 LO 換成**一顆好參考**或**自己的延遲**；C 法承認「每條通道都有本底」，但用**兩條獨立通道相關**把不相關的本底**開根號殺掉**。

---

## 第 2 部分：spur（確定性邊帶）vs 隨機 phase noise

量到的 PN 圖上常見**兩種完全不同的東西**疊在一起，新手最容易混淆。先把定義釘死：

| 項目 | 隨機 phase noise | spur（spurious tone）|
|---|---|---|
| 本質 | 隨機過程（stochastic）| 確定性弦波（deterministic tone）|
| 頻譜外觀 | **連續**裙邊（continuous skirt）| 離散**單根尖峰**（discrete spike）|
| 單位 | **/Hz**（dBc/Hz，功率密度）| **dBc**（總功率比，**無 /Hz**）|
| 隨 RBW | 量到的 dBc/Hz **不隨 RBW 變**（已歸一）| 尖峰高度（dBc）**不隨 RBW 變**；但「看起來」隨 RBW 變寬窄 |
| 成因 | 元件熱雜訊／flicker，經 ISF 上轉 | 參考洩漏、電源漣波、外部注入等**週期性**干擾 |
| 對策 | 改 ISF 對稱性、加大 $q_{max}$、降 device noise | 找出干擾源、隔離/濾波/屏蔽 |

### 2.1 為什麼單位天差地別：密度 vs 總功率

**隨機 PN 是功率密度**：相位是連續隨機過程，功率攤在頻率軸上，每 Hz 有多少功率才有意義——所以是 dBc/**Hz**。你把量測頻寬 RBW 加倍，量到的雜訊功率也加倍，**歸一到 per-Hz 後數字不變**。

**spur 是離散 tone 的總功率**：一根確定性弦波的全部功率集中在單一頻率，理論上頻寬為零。它的「密度」是無限大（沒意義），所以只報**相對載波的總功率 dBc**，**不帶 /Hz**。RBW 變大不會改變它的 dBc 值（功率全在那一根），只是看起來「胖」一點。

> **量測陷阱**：在 PN analyzer 上，背景連續譜以 dBc/Hz 畫，但 spur 若也照「當前 RBW 的密度」畫，會隨你選的 RBW 上下浮動——**這是假象**。正確做法是儀器把 spur 用 dBc（積分總功率）單獨標記。判別準則：**把 RBW 改一個檔位再量一次——隨機 PN 的 dBc/Hz 數字不動，spur 的「dBc/Hz 讀數」會變（因為它不是密度）。** 數字會變的就是 spur。

### 2.2 spur 的典型成因與對策

| spur 頻率位置 | 典型成因 | 物理機制（連 ISF）| 對策 |
|---|---|---|---|
| $f_{ref}$ 與其諧波（reference spur）| PLL 參考洩漏、charge-pump 不匹配、PFD 死區 | 參考頻率的週期性擾動經 ISF 第 $n$ 諧波上轉到載波旁 | 降 CP 漏電/不匹配、優化 PFD、加強 loop filter 抑制 |
| 電源漣波頻率（如 $50/60$ Hz、開關電源 $\sim$ 數百 kHz）| supply/ground 上的週期漣波耦合進 tank/tail | 週期供電擾動 → ISF 的 $c_0/c_n$ 上轉 | 穩壓/LDO 去耦、版圖隔離、降 PSRR 敏感度 |
| 鄰近強訊號頻率 | 外部 RF 注入、injection pulling | 注入訊號把振盪器拉動（見 injection locking）| 屏蔽、隔離、加大 tank $Q$ 抗拉 |
| 數位時脈／其諧波 | 數位 aggressor 經基板/電源耦合 | 週期數位 edge 經 ISF 上轉 | 基板環、分離電源域、時序錯開 |

**連回 ISF 的關鍵洞見**：一個落在 $n\omega_0+\Delta\omega$（接近第 $n$ 諧波）的**確定性**注入單音，會被 ISF 的第 $n$ 個傅立葉係數 $c_n$ **下變頻**到載波旁 $\Delta\omega$ 處，造成一根 spur（[P1] Eq.(16/17), p.183 的單音版，見 [fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf)）：

$$
\phi(t)\approx\frac{I_0\,c_n\sin(\Delta\omega t)}{2q_{max}\,\Delta\omega}.
$$

- 這和隨機 PN **用的是同一條 ISF 機制**——差別只在「來源是確定性單音（→spur）還是白噪（→連續譜）」。
- **設計訊息**：若某根 spur 落在第 $n$ 諧波附近，把 ISF 的 $c_n$ 壓低（改波形對稱性）就能同時壓那根 spur；和降隨機 PN 是同一組旋鈕。

### 2.3 在頻譜上怎麼分辨（操作型流程）

1. **看形狀**：連續裙邊 = 隨機 PN；孤立尖峰 = spur。
2. **改 RBW 重量**：dBc/Hz 不動的是 PN；讀數隨 RBW 變的是 spur。
3. **看可重複性**：spur 頻率固定（鎖在 $f_{ref}$、漣波頻率…），開關周邊設備（電源、鄰近發射源）spur 會跟著動/消失；隨機 PN 是 DUT 本質、關不掉。
4. **量積分功率**：對一根 spur 積分得固定 dBc（與 RBW 無關）；對 PN 積分得 jitter（見 [numerical_feeling](/04_simulation_labs/numerical_feeling)）。

---

## 第 3 部分：怎麼讀一張真實的 PN 圖

把前兩部分整合：拿到一張 $\mathcal{L}(\Delta f)$ 對 offset（log–log）的圖，怎麼**讀出設計訊息**。一張典型自由運行振盪器的 PN 圖由**三段斜率**與若干 spur 組成。

### 3.1 三段斜率與兩個 corner

| 區段 | 斜率 | 物理來源 | 對應公式 |
|---|---|---|---|
| close-in（最靠載波）| $-30$ dB/dec（$1/f^3$）| device flicker（$1/f$）noise 經 **$c_0$**（ISF 直流不對稱）上轉 | [P1] Eq.(23), p.185 |
| mid（中段）| $-20$ dB/dec（$1/f^2$）| 白噪經相位積分器 $1/\omega^2$ | [P1] Eq.(21), p.185 |
| floor（最遠）| $0$ dB/dec（平）| 量測系統/buffer 的白色雜訊本底 | — |

兩個轉折：

- **$1/f^3$ corner** $\Delta f_{1/f^3}$：$1/f^3$ 與 $1/f^2$ 交會點。由 [P1] Eq.(24), p.185：

$$
\Delta\omega_{1/f^3}=\omega_{1/f}\cdot\frac{c_0^2}{2\,\Gamma_{rms}^2}\approx\omega_{1/f}\left(\frac{c_0}{c_1}\right)^2.
$$

  **它反映 ISF 的對稱性**：$c_0$（ISF 直流分量）越小（波形越對稱），corner 越往載波靠、$1/f^3$ 區越窄——這是「為什麼追求對稱波形」的量化依據（見 [symmetry](/06_design_insights/symmetry)）。
- **noise floor corner** $\Delta f_{floor}$：$1/f^2$ 與平底交會點。它**多半是量測系統或輸出 buffer 的本底**，不一定是振盪器本質——讀圖時要先確認 floor 是 DUT 還是儀器（用第 1 部分的 cross-correlation 可把儀器 floor 壓下去，才看得到 DUT 真實 floor）。

### 3.2 反推設計訊息（讀圖 checklist）

- **$1/f^3$ 區的高度與寬度** → device flicker 大小（$\omega_{1/f}$）與 ISF 對稱性（$c_0$）。close-in 太差 → 換低 flicker 元件、做對稱波形/版圖、用 tail filter 壓 $c_0$。
- **$1/f^2$ 區的高度** → $\Gamma_{rms}^2/q_{max}^2 \cdot S_i$。太高 → 加大 swing（$q_{max}$）、降 device 白噪、壓 $\Gamma_{rms}$（見 [tank_swing](/06_design_insights/tank_swing)）。$1/f^2$ 區每 decade 改善 20 dB 是物理定律，斜率不對就要懷疑量錯了。
- **floor 高度** → 確認是 DUT 還是儀器。若是 buffer，加大載波功率或換低噪 buffer。
- **spur** → 逐根對位：$f_{ref}$？漣波？注入？分別用第 2.2 表對策。

> **這張 PN 圖的全貌**和 Leeson 模型、ISF 模型畫出來是同一個三段折線——本站 [derivation_leeson](/99_appendix/derivation_leeson) 與 [leeson_vs_isf 圖](/figures/leeson_vs_isf_overlay.png) 把兩模型疊在一起，三段（$1/f^3$、$1/f^2$、floor）與 corner 完全對得上。差別只在 ISF 把每段的常數用 $\Gamma_{rms}$、$c_0$、$q_{max}$ 解釋清楚，而 Leeson 用經驗的 $Q$、$F$。

![Leeson 與 ISF 三段折線疊圖：1/f³、1/f²、floor 與 corner 對應](/figures/leeson_vs_isf_overlay.png)

下面這張白噪→$1/f^2$ 的模擬譜，就是上圖中段 $-20$ dB/dec 那一段被單獨量出來的樣子（toy 模型，見 [lab_06](/04_simulation_labs/lab_06_white_noise_phase_noise)）：

![白噪經 ISF 與相位積分後得到的 1/f² phase noise PSD](/figures/white_noise_phase_noise_psd.png)

---

## 數值例子：由圖讀數反推設計（worked examples）

下面兩題用嚴格格式：**題目（給圖上讀數）→ 逐步代入（帶單位）→ 結果 → dimension check → 一行 Python 驗證**。沿用第 8 節 canonical 數值（$q_{max}=1$ pC、$\Gamma_{rms}=0.5$、$f_0=5$ GHz）。

> **例 1（由 $1/f^2$ 讀數反推等效白噪 $S_i$）**：在一張 PN 圖上量到中段（$1/f^2$ 區）$\mathcal{L}(1\,\text{MHz})=-148.0$ dBc/Hz。已知 $q_{max}=1$ pC、$\Gamma_{rms}=0.5$。反推等效白噪電流 PSD $S_i=\overline{i_n^2}/\Delta f$。

**逐步代入**（反解 [P1] Eq.(21), p.185）：

1. 把 dBc/Hz 轉回 linear：$10^{\mathcal{L}/10}=10^{-14.8}=1.585\times10^{-15}$（無因次 per-Hz）。
2. offset 角頻率：$\Delta\omega=2\pi\times10^{6}=6.283\times10^{6}$ rad/s，$\Delta\omega^2=3.948\times10^{13}$ rad²/s²。
3. Eq.(21) 是 $\mathcal{L}=\dfrac{\Gamma_{rms}^2}{q_{max}^2}\cdot\dfrac{S_i}{4\Delta\omega^2}$，反解

$$
S_i=\mathcal{L}_{lin}\cdot\frac{4\,\Delta\omega^2\,q_{max}^2}{\Gamma_{rms}^2}.
$$

4. 代入：$S_i=1.585\times10^{-15}\times\dfrac{4\times3.948\times10^{13}\times(10^{-12})^2}{0.25}$
   $=1.585\times10^{-15}\times\dfrac{1.579\times10^{14}\times10^{-24}}{0.25}=1.585\times10^{-15}\times6.317\times10^{-10}\approx1.0\times10^{-24}$。

**結果**：$S_i\approx1.0\times10^{-24}\ \text{A}^2/\text{Hz}$——正好回到 canonical 例 B 的輸入值（自洽）。

**Dimension check**：$\mathcal{L}_{lin}$（per-Hz $=$ s）$\times\dfrac{(\text{rad/s})^2\cdot\text{C}^2}{1}=\text{s}\cdot\dfrac{\text{C}^2}{\text{s}^2}=\dfrac{\text{C}^2}{\text{s}}=\dfrac{(\text{A}\cdot\text{s})^2}{\text{s}}=\text{A}^2\cdot\text{s}=\text{A}^2/\text{Hz}$ ✓。

```python
import numpy as np
L_dbc, gamma_rms, qmax = -148.0, 0.5, 1e-12
dw = 2*np.pi*1e6
Si = 10**(L_dbc/10) * (4*dw**2*qmax**2) / gamma_rms**2
print(f"{Si:.3e} A^2/Hz")   # -> 1.000e-24 A^2/Hz
```

> **例 2（由 $1/f^3$ corner 反推 ISF 對稱性 $c_0/c_1$）**：圖上量到 device flicker corner $f_{1/f}=1\,\text{MHz}$（$\omega_{1/f}=2\pi\times10^6$），而 PN 圖上 $1/f^3$ 與 $1/f^2$ 的交會 corner 出現在 $\Delta f_{1/f^3}=100\,\text{kHz}$。反推 ISF 的 $c_0/c_1$ 比，評估波形對稱性。

**逐步代入**（用 [P1] Eq.(24), p.185 的近似 $\Delta\omega_{1/f^3}\approx\omega_{1/f}(c_0/c_1)^2$）：

1. 反解：$\left(\dfrac{c_0}{c_1}\right)^2=\dfrac{\Delta\omega_{1/f^3}}{\omega_{1/f}}=\dfrac{2\pi\times10^5}{2\pi\times10^6}=\dfrac{10^5}{10^6}=0.1$。
2. 開根號：$\dfrac{c_0}{c_1}=\sqrt{0.1}\approx0.316$。

**結果**：$c_0/c_1\approx0.32$——ISF 的直流分量約為一次諧波的三分之一，屬「中度對稱」。

**反推的設計訊息**：$c_0\neq0$ 表示波形/版圖**仍有不對稱**，仍有可觀 $1/f^3$ 上轉。若把波形做更對稱使 $c_0$ 再降 $\times0.3$（$c_0/c_1\to0.1$），corner 從 $100$ kHz 降到 $\Delta f_{1/f^3}=\omega_{1/f}(0.1)^2=1\,\text{MHz}\times0.01=10\,\text{kHz}$——**close-in $1/f^3$ 區縮小 10 倍**，近載波雜訊大幅改善（見 [symmetry](/06_design_insights/symmetry)、[flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)）。

**Dimension check**：$\Delta\omega_{1/f^3}/\omega_{1/f}$ 為 rad/s ÷ rad/s $=$ 無因次；$(c_0/c_1)^2$ 也無因次 ✓。

```python
import numpy as np
w_1f = 2*np.pi*1e6           # device flicker corner
dw_1f3 = 2*np.pi*1e5         # 1/f^3 corner read off the plot
c0_over_c1 = np.sqrt(dw_1f3/w_1f)
print(round(c0_over_c1, 3))  # -> 0.316
```

---

## 適用與失效條件

| 條件 | 成立時 | 失效時會怎樣 |
|---|---|---|
| 量測系統本底 $\ll$ DUT 雜訊 | 量到的是 DUT | 量到儀器自己（SA 直接法最易踩）→ 改用 PLL/cross-correlation |
| 小角 PM（$\phi\ll1$ rad）| $\mathcal{L}\approx\tfrac12 S_\phi$ | 大相位起伏要用嚴格 PM 譜，近載波 Lorentzian（見 [lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth)）|
| 雜訊源為穩態白色/flicker | 三段折線乾淨 | cyclostationary、注入拉動會破壞乾淨折線 |
| spur 為確定性週期源 | dBc 固定、可逐根對位 | 隨機叢發/間歇干擾不易用 dBc 描述 |
| floor 是 DUT 本質 | floor 反映 buffer/source | 多半是儀器 floor，需 cross-correlation 才看得到真 floor |

## 與哪些 paper／公式對應

- spur 的下變頻機制（單音版）：[P1] Eq.(16/17), p.183（見 [fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf)）。
- $1/f^2$ 中段：[P1] Eq.(21), p.185；$1/f^3$ close-in：[P1] Eq.(23), p.185；$1/f^3$ corner：[P1] Eq.(24), p.185。
- $\mathcal{L}\approx\tfrac12 S_\phi$（小角 PM）：規範 Eq.16。
- 三段折線全貌與 Leeson 對照：[derivation_leeson](/99_appendix/derivation_leeson)、[E1] Leeson 1966（**不在 5 篇 PDF 內**）。
- **量測儀器/標準（SA、delay-line/PLL discriminator、cross-correlation analyzer）屬外部工程文獻與儀器手冊，不在下載的 5 篇 PDF 內**；本頁用標準量測理論補充。

## 重點回顧

- 量 $\mathcal{L}(f)$ 的本質：**拿掉載波 + 壓低系統本底**。SA 直接法量到「DUT＋儀器」；PLL/delay-line 用去載波把儀器換成好參考或自延遲；**cross-correlation 用兩條獨立通道相關，把不相關的本底以 $1/\sqrt{M}$ 殺掉**（每 ×10 平均降 5 dB）。
- **spur** 是確定性離散 tone（單位 **dBc**，不隨 RBW 變密度）；**隨機 PN** 是連續譜（**dBc/Hz**）。分辨：改 RBW 重量、看可重複性、開關周邊設備。
- spur 成因：參考洩漏、電源漣波、外部注入；經 ISF 第 $n$ 諧波 $c_n$ 下變頻到載波旁；對策是隔離/濾波/屏蔽 + 壓 $c_n$。
- 讀 PN 圖：$1/f^3$（flicker 經 $c_0$）／$1/f^2$（白噪經積分器）／floor（多為儀器/buffer），加兩個 corner。反推 $S_i$、$c_0/c_1$、device flicker，得設計旋鈕。
- 數值例：$-148$ dBc/Hz @ 1 MHz 反推 $S_i\approx10^{-24}$ A²/Hz；$1/f^3$ corner $100$ kHz（flicker corner 1 MHz）反推 $c_0/c_1\approx0.32$。

## 延伸閱讀

- $\mathcal{L}$ 與 $S_\phi$、白噪 $1/f^2$ 推導：[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)
- spur 的下變頻機制（ISF 諧波）：[fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf)
- close-in $1/f^3$ 與對稱性：[flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)、[symmetry](/06_design_insights/symmetry)
- 加大 swing 壓 $1/f^2$：[tank_swing](/06_design_insights/tank_swing)
- 把 $\mathcal{L}$ 積回 jitter：[numerical_feeling](/04_simulation_labs/numerical_feeling)
- 三段折線與 Leeson 對照：[derivation_leeson](/99_appendix/derivation_leeson)
- 近載波 Lorentzian（$1/f^2$ 發散的真相）：[lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth)
