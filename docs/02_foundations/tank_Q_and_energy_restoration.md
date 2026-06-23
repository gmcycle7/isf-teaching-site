---
title: Tank Q 與能量恢復
description: 從並聯 RLC tank 乾淨推出品質因數 Q——三種等價寫法（R_p√(C/L)、ω0 R_p C、R_p/(ω0 L)）與能量定義 Q=ω0·儲能/耗能；說明 active core 必須補 −R 抵消 tank 損耗 R_p，而那個 R_p 正是 4kT/R_p 熱雜訊電流的物理來源；連到 phase noise（高 Q → 窄帶 → 陡相位斜率）與 Q↔Γrms/qmax 的對應，以及 on-chip inductor Q 的實務天花板。RLC/Q 為標準教科書內容（外部，非本站 5 篇 PDF）。
---

# Tank Q 與能量恢復

「品質因數 $Q$（quality factor，諧振有多『尖』、每週期能量被耗掉多少的指標）」這個量幾乎在本站每一頁都出現：Leeson 模型寫成 $\dfrac{1}{2Q}$（[derivation_leeson](/99_appendix/derivation_leeson)）、LC vs ring 的比較靠它（[lc_vs_ring](/06_design_insights/lc_vs_ring)）、tank swing 的取捨也要它（[tank_swing](/06_design_insights/tank_swing)）。可是它在那些頁裡**都被當成已知量直接用，從來沒有從電路被乾淨推出來過**。這一頁就把這個洞補上：從最基本的並聯 RLC tank 出發，把 $Q$ 的三種等價寫法與能量定義一步步推出來，再說明它如何接到 active core 的 $-R$、tank 熱雜訊 $4kT/R_p$，以及最後如何決定 phase noise。

> **物理直覺（先講結論）**：tank（諧振槽，$L$ 與 $C$ 來回交換能量的儲能元件）就像一個鐘擺。$Q$ 衡量「這個鐘擺有多不願意停下來」——它每振盪一個 radian，相對於儲存的能量只漏掉一小撮給損耗電阻 $R_p$。$Q$ 越高，諧振峰越尖、頻寬越窄、相位對頻率的斜率越陡。把 noise 想成想把振盪頻率推歪的力：$Q$ 越高，tank 越「咬死」在 $\omega_0$、越不肯被推歪，於是同一坨 noise 換來的 phase noise 越小。這就是為什麼低 phase noise 設計的第一句口號永遠是「把 $Q$ 做高」。

這頁要回答三件事：

1. $Q$ 到底是什麼？為什麼 $Q=R_p\sqrt{C/L}=\omega_0 R_p C=R_p/(\omega_0 L)$ 三種寫法等價，又為什麼它等於 $\omega_0\times$（儲能/耗能功率）？
2. 真實 tank 一定有損耗 $R_p$，振盪會衰減——active core 怎麼用 $-R$ 把它補回來？而那個被補掉的 $R_p$，為什麼正是 tank 熱雜訊 $4kT/R_p$ 的源頭？
3. $Q$ 怎麼接到 phase noise？為什麼「高 $Q$ → 窄帶 → 陡相位斜率 → 每單位 offset 的 noise 更少」，而這跟 ISF 的 $\Gamma_{rms}/q_{max}$ 是同一回事？

> **誠實聲明（請先讀）**：本頁的 **RLC tank、$Q$ 的定義與三種等價寫法、$4kTR$ 熱雜訊**都是**標準電路學/微波工程教科書內容（外部，非本站下載的 5 篇 PDF）**，例如 Razavi《RF Microelectronics》、Pozar《Microwave Engineering》、Lee《The Design of CMOS RFICs》。本站不重新發明這些常數，只把它們乾淨推一遍，並接到 5 篇 PDF 內已核的 ISF 結果（[P1] Eq.(21) 等）。凡是接到 [P1]/[P2] 的地方都有標明 paper id + equation。

## 第 1 步：並聯 RLC tank 與 $Q$ 的三種等價寫法

最基本的 LC 振盪器 tank 是一個**並聯 RLC**：電感 $L$、電容 $C$、以及一個並聯損耗電阻 $R_p$（把所有 tank 損耗——inductor 串聯電阻、capacitor 介質損耗、輻射——全部等效成這一個並聯電阻）。

先定義諧振角頻率。並聯 LC 在某個頻率讓電感與電容的電納（susceptance）相消、阻抗純電阻、能量在 $L$ 與 $C$ 之間完全來回交換：

$$
\omega_0=\frac{1}{\sqrt{LC}}.
$$

- **用到的物理**：電感阻抗 $j\omega L$、電容阻抗 $1/(j\omega C)$。並聯時電納相加 $\dfrac{1}{j\omega L}+j\omega C=j\big(\omega C-\dfrac{1}{\omega L}\big)$，令括號為零即得 $\omega_0^2=1/(LC)$。
- **單位檢查**：$[\sqrt{LC}]=\sqrt{\text{H}\cdot\text{F}}=\sqrt{(\text{V·s/A})(\text{A·s/V})}=\sqrt{\text{s}^2}=\text{s}$，所以 $1/\sqrt{LC}$ 是 rad/s ✓。

**unloaded（無載）vs loaded（有載）$Q$ 的區別先講清楚**：

- **unloaded $Q$（$Q_0$，無載品質因數）**：只算 tank 自身損耗（$R_p$ 純粹是 tank 元件的損耗）時的 $Q$。這是 tank 元件本身的「品質」。
- **loaded $Q$（$Q_L$，有載品質因數）**：把外部負載（接出去的電路、量測儀器、buffer 輸入阻抗）也並進來後的 $Q$。外部負載相當於再並一個電阻 $R_{ext}$，總並聯電阻 $R_p\parallel R_{ext}$ 比 $R_p$ 小，所以 $Q_L<Q_0$。
- 兩者關係：$\dfrac{1}{Q_L}=\dfrac{1}{Q_0}+\dfrac{1}{Q_{ext}}$（電導相加 → $Q$ 倒數相加，因為 $Q\propto R_p\propto 1/G$）。本頁推導與決定 phase noise 的，**主要是 loaded $Q$（振盪器實際看到的）**；但設計 inductor 時關心的是 unloaded $Q$。下文除非特別說明，$Q$ 指振盪迴路實際的有效（loaded）$Q$。

現在推 $Q$。並聯 RLC 的 $Q$ 的**電路定義**是「諧振時，電抗元件（$L$ 或 $C$）儲存的能量流，相對於電阻 $R_p$ 耗散的速率」。最方便的等價代數定義是：諧振時電容（或電感）的電納大小對電導的比值

$$
Q=\frac{|B_C(\omega_0)|}{G}=\frac{\omega_0 C}{1/R_p}=\omega_0 R_p C.
$$

- **用到的物理**：並聯 RLC 中，電導 $G=1/R_p$ 是唯一耗能元件；電容電納 $B_C=\omega_0 C$ 量「無功電流」有多大。$Q$ 就是無功電流 / 有功電流的比。
- **單位檢查**：$[\omega_0 R_p C]=(\text{rad/s})(\Omega)(\text{F})=(\text{1/s})(\text{V/A})(\text{A·s/V})=$ 無因次 ✓。

把 $\omega_0=1/\sqrt{LC}$ 代進去，得到第二種寫法：

$$
Q=\omega_0 R_p C=\frac{R_p C}{\sqrt{LC}}=R_p\sqrt{\frac{C^2}{LC}}=R_p\sqrt{\frac{C}{L}}.
$$

- **代數每一步**：$\omega_0 C=C/\sqrt{LC}=\sqrt{C^2/(LC)}=\sqrt{C/L}$，乘上 $R_p$ 即得。
- **單位檢查**：$\sqrt{C/L}=\sqrt{\text{F/H}}=\sqrt{(\text{A·s/V})/(\text{V·s/A})}=\sqrt{\text{A}^2/\text{V}^2}=\text{A/V}=1/\Omega$，乘 $R_p$（$\Omega$）→ 無因次 ✓。$\sqrt{L/C}$ 這個量有電阻的單位，叫 tank 的**特性阻抗（characteristic impedance）** $R_0=\sqrt{L/C}$，所以也可寫成 $Q=R_p/R_0$——「並聯損耗電阻相對特性阻抗有多大」。

第三種寫法用 $\omega_0=1/\sqrt{LC}$ 把 $C$ 換成 $L$。因為諧振時電感電納大小等於電容電納大小（$\omega_0 L$ 與 $1/(\omega_0 C)$ 互為倒數），所以同一個比值也可寫成電導 $\times$ 電感電抗的倒數：

$$
Q=\omega_0 R_p C=\frac{R_p}{\omega_0 L}.
$$

- **代數驗證**：$\omega_0 R_p C\cdot\omega_0 L=\omega_0^2 LC\,R_p=R_p$（因 $\omega_0^2 LC=1$），兩邊除以 $\omega_0 L$ 即得 $\omega_0 R_p C=R_p/(\omega_0 L)$ ✓。
- **單位檢查**：$R_p/(\omega_0 L)=\Omega/[(\text{rad/s})(\text{H})]=\Omega/\Omega=$ 無因次 ✓。

**三式等價，集中收在這裡（全站之後直接引用）**：

$$
Q=\omega_0 R_p C=R_p\sqrt{\frac{C}{L}}=\frac{R_p}{\omega_0 L}=\frac{R_p}{R_0},\qquad R_0\equiv\sqrt{\frac{L}{C}}.
$$

- **物理讀法（極重要）**：注意 $R_p$ 在分子。**並聯 tank 裡，$R_p$ 越大、$Q$ 越高**（並聯時大電阻 = 小損耗電導 = 漏得少）。這跟串聯 RLC 直覺相反（串聯 $Q=\omega_0 L/R_s$，$R_s$ 在分母），初學最容易弄反——本站振盪器一律用**並聯**模型，記住「並聯：$R_p$ 大 → $Q$ 高」。

| 寫法 | 適合什麼時候用 | 一句話讀法 |
|---|---|---|
| $Q=\omega_0 R_p C$ | 已知 $C$、$R_p$、$\omega_0$（最常見） | 損耗電阻 $\times$ 電容電納 |
| $Q=R_p\sqrt{C/L}=R_p/R_0$ | 想看「$R_p$ 相對特性阻抗」 | 損耗電阻相對 $R_0=\sqrt{L/C}$ 有多大 |
| $Q=R_p/(\omega_0 L)$ | 已知 $L$、$R_p$ 時 | 損耗電阻相對電感電抗 |

## 第 2 步：能量定義 $Q=\omega_0\dfrac{\text{儲存能量}}{\text{耗散功率}}$，並證明與第 1 步一致

$Q$ 最物理、最跨領域通用的定義是能量定義：

$$
Q=\omega_0\,\frac{E_{stored}}{P_{diss}}=2\pi\,\frac{\text{每週期儲存的能量}}{\text{每週期耗散的能量}}.
$$

- **意義**：$Q/(2\pi)$ = 儲能 / 每週期耗能。$Q$ 越高，每振盪一圈只漏掉儲能的一小撮 $2\pi/Q$。所以「$Q$ 等於振盪自由衰減到 $1/e$ 大約需要的 radian 數」（更精確：能量包絡 $e^{-\omega_0 t/Q}$，見下）。
- **單位檢查**：$\omega_0 E/P=(\text{rad/s})(\text{J})/(\text{W})=(\text{rad/s})(\text{J})/(\text{J/s})=$ 無因次（rad）✓。

**證明它等於第 1 步的 $\omega_0 R_p C$**。在諧振時，tank 兩端的電壓設為 $v(t)=V_p\cos\omega_0 t$。

(1) **儲存能量**：諧振時能量在 $L$、$C$ 間完全來回交換，總儲能守恆且等於電容能量的峰值（電壓峰值時能量全在 $C$）：

$$
E_{stored}=\frac{1}{2}C V_p^2.
$$

- 檢查守恆：電容能量 $\tfrac12 C v^2=\tfrac12 C V_p^2\cos^2\omega_0 t$，電感能量 $\tfrac12 L i_L^2$；其中 $i_L=\tfrac1L\int v\,dt=\tfrac{V_p}{\omega_0 L}\sin\omega_0 t$，故電感能量 $=\tfrac12 L\tfrac{V_p^2}{\omega_0^2 L^2}\sin^2\omega_0 t=\tfrac12\tfrac{V_p^2}{\omega_0^2 L}\sin^2\omega_0 t$。用 $\omega_0^2 L=1/C$，得 $\tfrac12 C V_p^2\sin^2\omega_0 t$。兩者相加 $=\tfrac12 C V_p^2(\cos^2+\sin^2)=\tfrac12 C V_p^2$，**確實守恆** ✓。

(2) **耗散功率**：只有 $R_p$ 耗能，平均功率（正弦的均方 = 峰值平方的一半）：

$$
P_{diss}=\frac{\overline{v^2}}{R_p}=\frac{V_p^2/2}{R_p}=\frac{V_p^2}{2R_p}.
$$

(3) **代入能量定義**：

$$
Q=\omega_0\frac{E_{stored}}{P_{diss}}=\omega_0\cdot\frac{\tfrac12 C V_p^2}{\,V_p^2/(2R_p)\,}=\omega_0\cdot\frac{\tfrac12 C V_p^2\cdot 2R_p}{V_p^2}=\omega_0 R_p C.
$$

- $V_p^2$ 與因子 $\tfrac12,2$ 全約掉，**精確回到第 1 步的 $\omega_0 R_p C$** ✓。能量定義與電路定義是同一個 $Q$，這不是巧合——兩者都在量同一件事：每 radian 漏掉儲能的比例。
- **單位檢查**：$\omega_0\cdot\dfrac{[\text{F}][\text{V}^2]}{[\text{V}^2]/[\Omega]}=(\text{rad/s})[\text{F}][\Omega]=(\text{rad/s})[\text{s}]=$ 無因次 ✓。

**順帶推出自由衰減率（給「$Q$=幾個 radian」直覺）**：tank 沒有 active core 補能時，每秒耗散 $P_{diss}=\omega_0 E/Q$，即 $\dfrac{dE}{dt}=-\dfrac{\omega_0}{Q}E$，解得

$$
E(t)=E_0\,e^{-\omega_0 t/Q}\quad\Rightarrow\quad v(t)\ \text{包絡}\ \propto e^{-\omega_0 t/(2Q)}.
$$

- **讀法**：能量衰減時間常數 $\tau_E=Q/\omega_0$，振盪振幅衰減時間常數 $2Q/\omega_0$。$Q=100$ 的 5 GHz tank（$\omega_0=2\pi\times5\times10^9$）振幅自由衰減常數約 $2\times100/(2\pi\times5\times10^9)\approx6.4$ ns，約 32 個週期——**這就是為什麼真實振盪器一定要 active core 持續補能，否則幾十個週期就停**。這帶我們到第 3 步。

## 第 3 步：active core 補 $-R$ 抵消 $R_p$，而 $R_p$ 正是 $4kT/R_p$ 熱雜訊的源頭

第 2 步說明了：只要有 $R_p$，振盪就會以 $e^{-\omega_0 t/(2Q)}$ 衰減。要維持穩定振盪，振盪器的 **active core（主動核心，例如 cross-coupled 差動對提供的負電導）** 必須把 $R_p$ 漏掉的能量**逐週期補回來**。最乾淨的看法：active core 在 tank 兩端呈現一個**負電阻 $-R$**（負電導 $-G_m$），與 $R_p$ 並聯。

$$
\frac{1}{R_{tank}}=\frac{1}{R_p}-G_m,\qquad \text{起振條件}:\ G_m\ge\frac{1}{R_p}\ \big(\text{即 } -R\le -R_p\big).
$$

- **物理意義**：正電阻吸能、負電阻供能。當 active core 的負電導 $G_m$ 剛好等於 $R_p$ 的電導 $1/R_p$，總損耗為零，振盪維持等幅（Barkhausen 起振邊界）。實務上設計 $G_m$ 略大於 $1/R_p$（loop gain $>1$）保證能起振，再靠非線性飽和把有效 $G_m$ 拉回到剛好抵消——這就是 [oscillator_phase](/02_foundations/oscillator_phase) 講的 limit cycle 的振幅恢復機制在電路層的化身。
- **單位檢查**：$G_m$ 與 $1/R_p$ 都是西門子（S）✓。
- **關鍵釐清**：active core 抵消的是 $R_p$ 的**確定性能量損耗**（讓振盪不衰減）。它**不會、也不能消掉 $R_p$ 帶來的隨機熱雜訊**——這是下一段的重點，也是整頁與 phase noise 接軌的橋。

**$R_p$ 是 tank 熱雜訊電流 $4kT/R_p$ 的物理來源。** 任何耗能電阻（包括等效損耗 $R_p$）依 Johnson–Nyquist 定理一定伴隨熱雜訊。並聯電阻最方便用**諾頓等效的雜訊電流源**表示，其單邊 PSD：

$$
\frac{\overline{i_{n,R}^2}}{\Delta f}=\frac{4kT}{R_p}.
$$

- **用到的物理**：fluctuation–dissipation（漲落–耗散）定理——有耗散就有漲落。電阻熱雜訊電壓 PSD 是 $4kTR_p$（[psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter) 有講），換成並聯諾頓電流源就是除以 $R_p^2$：$\overline{i_n^2}/\Delta f=(4kTR_p)/R_p^2=4kT/R_p$。
- **單位檢查**：$[4kT/R_p]=\text{J}/\Omega=(\text{V·A·s})/(\text{V/A})=\text{A}^2\text{s}=\text{A}^2/\text{Hz}$ ✓（單邊電流 PSD，符合規範 notation 的 $\overline{i_n^2}/\Delta f$ 單位 A²/Hz）。
- **深刻之處**：你**沒辦法用 $-R$ 把這個雜訊也消掉**。active core 的 $-R$ 抵消的是 $R_p$ 在「能量平衡」帳上的損耗項；但 $R_p$ 在「漲落」帳上注入的 $4kT/R_p$ 隨機電流，被 active core 補進來的能量同等放大維持。所以**tank 損耗 $R_p$ 同時是兩件事的源頭：它讓你需要 active core 補能，也讓你拿到一個無法迴避的基礎熱雜訊地板**。這正是把 $Q$ 與 phase noise 綁在一起的物理根。（active core 自己的 device 還會再加雜訊——那是 [device_noise_mapping](/06_design_insights/device_noise_mapping) 的主題；本頁只談 tank 本身的 $4kT/R_p$。）

**把 $R_p$ 用 $Q$ 表達**（之後好接 phase noise）：由第 1 步 $R_p=Q/(\omega_0 C)=Q\,\omega_0 L=Q\,R_0$，所以同樣電容/頻率下，

$$
\frac{4kT}{R_p}=\frac{4kT\,\omega_0 C}{Q}\quad\Rightarrow\quad \overline{i_{n,R}^2}/\Delta f\ \propto\ \frac{1}{Q}.
$$

- **讀法**：$Q$ 越高 → $R_p$ 越大 → tank 注入的熱雜訊電流 PSD 越小（$\propto 1/Q$）。這是「高 $Q$ → 低 phase noise」的第一層原因（雜訊源變小）；第 2 步的「窄帶/陡斜率」是第二層。兩層疊起來就是下一步。

## 第 4 步：把 $Q$ 接到 phase noise——窄帶、陡相位斜率、與 $\Gamma_{rms}/q_{max}$ 的等價

**(a) 高 $Q$ = 窄帶寬 = 陡相位斜率。** $Q$ 與 3-dB 頻寬的標準關係：

$$
Q=\frac{\omega_0}{\Delta\omega_{3\mathrm{dB}}}\quad\Leftrightarrow\quad \Delta\omega_{3\mathrm{dB}}=\frac{\omega_0}{Q}.
$$

- **推導要點**：並聯 RLC 阻抗 $Z(\omega)=\big(\tfrac{1}{R_p}+j\omega C+\tfrac{1}{j\omega L}\big)^{-1}$，在 $\omega_0$ 附近用 $\omega=\omega_0+\Delta\omega$ 一階展開，電納部分 $\approx j\,2C\Delta\omega$，得 $Z\approx R_p/(1+j\,2Q\Delta\omega/\omega_0)$。$|Z|$ 掉到峰值 $1/\sqrt2$（−3 dB）發生在 $2Q\Delta\omega/\omega_0=1$，即半頻寬 $\Delta\omega=\omega_0/(2Q)$，全頻寬 $\omega_0/Q$ ✓。
- **相位斜率**：上式相位 $\angle Z=-\arctan(2Q\Delta\omega/\omega_0)$，在 $\omega_0$ 處對 $\omega$ 的斜率 $\dfrac{d\angle Z}{d\omega}\big|_{\omega_0}=-\dfrac{2Q}{\omega_0}$。**$Q$ 越高，相位對頻率的斜率越陡**。
- **物理意義（為什麼陡相位斜率 = 低 phase noise）**：振盪鎖在「迴路總相移 = 0」的頻率。若 noise 想把相位推離 0，tank 的陡相位斜率會用一個很大的「頻率回復力」把它拉回 $\omega_0$——相位斜率 $d\phi/d\omega$ 越陡，同樣的相位擾動只對應越小的頻率（進而越小的長期相位）偏移。tank 像一個很硬的彈簧把振盪頻率咬死在 $\omega_0$。這正是 Leeson 模型 $\big(\tfrac{\omega_0}{2Q\Delta\omega}\big)^2$ 整形項的物理來源（[derivation_leeson](/99_appendix/derivation_leeson) 第 2 步）。

**(b) $1/Q^2$ scaling（Leeson）。** 把 (a) 的窄帶整形與第 3 步的 $1/Q$ 雜訊源**疊起來**，再經自治振盪器的相位積分（$1/\Delta\omega^2$），phase noise 的 $Q$ 依賴落在 $1/Q^2$：

$$
\mathcal{L}(\Delta\omega)\ \propto\ \Big(\frac{\omega_0}{2Q\,\Delta\omega}\Big)^2\ \propto\ \frac{1}{Q^2}.
$$

- **讀法**：$Q$ 加倍 → phase noise 改善 $10\log_{10}(2^2)=6.02$ dB。這跟 [tank_swing](/06_design_insights/tank_swing) 的「$q_{max}$ 加倍 → −6 dB」是**同一種平方反比**——$Q$ 與 $q_{max}$ 是兩個獨立但都「平方進帳」的低 phase noise 槓桿。
- **註**：$\big(\tfrac{\omega_0}{2Q\Delta\omega}\big)^2$ 這條整形式屬 Leeson 模型（**外部文獻，非本站 5 篇 PDF**，見 [derivation_leeson](/99_appendix/derivation_leeson)）。

**(c) Q ↔ Γrms/qmax 等價（本站核心對應）。** [derivation_leeson](/99_appendix/derivation_leeson)（第 5 步、對照表）斷言：Leeson 的 $\dfrac{1}{2Q}$ 和 ISF 的 $\dfrac{\Gamma_{rms}}{q_{max}}$ 描述**同一件事**——「把 tank/device 雜訊轉成相位裙帶的效率」。把兩個 $1/f^2$ 結果擺在一起看就清楚：

| 模型 | $1/f^2$ 相位裙帶 | 「雜訊→相位」效率因子 | 來源 |
|---|---|---|---|
| Leeson（外部，非 5 篇 PDF） | $\propto\big(\dfrac{\omega_0}{2Q\,\Delta\omega}\big)^2$ | $\dfrac{1}{2Q}$（$Q$ 高 → 效率低 → 雜訊少） | [E1] Leeson 1966 |
| ISF（[P1]，5 篇 PDF 內） | $\dfrac{\Gamma_{rms}^2}{q_{max}^2}\cdot\dfrac{\overline{i_n^2}/\Delta f}{4\Delta\omega^2}$ | $\dfrac{\Gamma_{rms}}{q_{max}}$（小 → 雜訊少） | [P1] Eq.(21), p.185 |

對應關係：

$$
\frac{1}{2Q}\ \longleftrightarrow\ \frac{\Gamma_{rms}}{q_{max}}\times(\text{載波/雜訊功率正規化}).
$$

- **怎麼讀**：**高 $Q$ ⟺ 低 $\Gamma_{rms}/q_{max}$ ⟺ 低 phase noise**。兩者都是「同一坨雜訊換來多少相位」的比例。
- **ISF 為什麼更一般**：$Q$ 是 LC tank 的概念（要有諧振儲能元件才有 $Q$）；**ring oscillator 沒有高 $Q$ tank、根本沒有 $Q$ 可言，但仍然有 $\Gamma_{rms}$ 與 $q_{max}$**，所以 [P1] 的 $\Gamma_{rms}/q_{max}$ 對 ring 一樣成立，而 Leeson 的 $1/(2Q)$ 對 ring 失效（見 [lc_vs_ring](/06_design_insights/lc_vs_ring)）。$Q$ 是 $\Gamma_{rms}/q_{max}$ 在「有諧振 tank」這個特例下的化身。這就是 [derivation_leeson](/99_appendix/derivation_leeson) 主張的 $Q\leftrightarrow\Gamma_{rms}/q_{max}$ 等價的完整意思。

## 數值例子（建立手感）

> **例（5 GHz LC tank 的 $Q$、$R_p$、熱雜訊地板）**：取 $L=1$ nH、$C=1.013$ pF（湊 $f_0=5$ GHz）、tank 並聯損耗 $R_p=314\ \Omega$、$T=300$ K。求 $Q$、3-dB 頻寬、tank 熱雜訊電流 PSD。

**(1) 諧振頻率**：

$$
\omega_0=\frac{1}{\sqrt{LC}}=\frac{1}{\sqrt{10^{-9}\times1.013\times10^{-12}}}=\frac{1}{\sqrt{1.013\times10^{-21}}}\approx3.142\times10^{10}\ \text{rad/s},
$$

即 $f_0=\omega_0/(2\pi)\approx5.00$ GHz ✓。

**(2) $Q$（用 $R_p/(\omega_0 L)$，也對照 $\omega_0 R_p C$）**：

$$
Q=\frac{R_p}{\omega_0 L}=\frac{314}{3.142\times10^{10}\times10^{-9}}=\frac{314}{31.42}\approx10.0.
$$

對照 $\omega_0 R_p C=3.142\times10^{10}\times314\times1.013\times10^{-12}\approx9.99$ ✓（兩寫法一致）。特性阻抗 $R_0=\sqrt{L/C}=\sqrt{10^{-9}/1.013\times10^{-12}}\approx31.4\ \Omega$，故 $Q=R_p/R_0=314/31.4=10.0$ ✓（三寫法全一致）。

**(3) 3-dB 頻寬**：$\Delta\omega_{3\mathrm{dB}}=\omega_0/Q=3.142\times10^{10}/10=3.142\times10^9$ rad/s，即 $\Delta f_{3\mathrm{dB}}=f_0/Q=500$ MHz。$Q=10$ 是 on-chip inductor 的典型值——頻寬高達 500 MHz，諧振一點都不尖，這也預告了第 5 步的 on-chip $Q$ 天花板問題。

**(4) tank 熱雜訊電流 PSD**：

$$
\frac{4kT}{R_p}=\frac{4\times1.38\times10^{-23}\times300}{314}=\frac{1.656\times10^{-20}}{314}\approx5.27\times10^{-23}\ \text{A}^2/\text{Hz}.
$$

- **Dimension check**：$\dfrac{[\text{J/K}][\text{K}]}{[\Omega]}=\dfrac{\text{J}}{\Omega}=\dfrac{\text{V·A·s}}{\text{V/A}}=\text{A}^2\text{·s}=\text{A}^2/\text{Hz}$ ✓。
- **手感**：這 $5.27\times10^{-23}$ A²/Hz 就是「只有 tank、最理想」的雜訊電流地板。把它當 [P1] Eq.(21) 的 $\overline{i_n^2}/\Delta f$（配 $q_{max}=1$ pC、$\Gamma_{rms}=0.5$）可估出一個理想 phase noise 上限——真實電路因 active core device 雜訊、cyclostationary、flicker 會更高（見 [device_noise_mapping](/06_design_insights/device_noise_mapping)）。若把 $Q$ 從 10 提到 20（$R_p$ 加倍到 628 Ω），這個雜訊電流地板直接砍半（$\propto 1/Q$），phase noise 再得益。

**一行 Python 驗證**：

```python
import numpy as np
L, C, Rp, T, k = 1e-9, 1.013e-12, 314.0, 300.0, 1.380649e-23
w0 = 1/np.sqrt(L*C)
Q_1 = w0*Rp*C            # ω0 Rp C
Q_2 = Rp*np.sqrt(C/L)    # Rp√(C/L)
Q_3 = Rp/(w0*L)          # Rp/(ω0 L)
in2 = 4*k*T/Rp           # tank 熱雜訊電流 PSD (A^2/Hz)
print(f"f0={w0/2/np.pi/1e9:.2f}GHz  Q={Q_1:.2f},{Q_2:.2f},{Q_3:.2f}  "
      f"BW={w0/Q_1/2/np.pi/1e6:.0f}MHz  in2={in2:.2e} A^2/Hz")
# -> f0=5.00GHz  Q=9.99,9.99,9.99  BW=500MHz  in2=5.27e-23 A^2/Hz
```

（本例的 RLC/Q/熱雜訊公式均為標準教科書內容，外部、非 5 篇 PDF；$q_{max}$、$\Gamma_{rms}$ 與 Eq.(21) 的接法見 [tank_swing](/06_design_insights/tank_swing)、[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)。）

## 第 5 步：實務天花板——on-chip inductor Q 與寄生

理論上把 $R_p$ 做大就能無限提 $Q$，但矽製程裡 $Q$ 有硬天花板，原因幾乎都出在 inductor 與寄生：

| 限制來源 | 為什麼壓 $Q$ | 典型量級／後果 |
|---|---|---|
| spiral inductor 金屬串聯電阻 $R_s$ | 金屬有限電導 + skin effect / proximity effect 使高頻 $R_s$ 上升；串聯 $R_s$ 折算到並聯 $R_p\approx Q_L^2 R_s$ 有上限 | on-chip inductor unloaded $Q$ 常只有 **5～15**（先進製程到 ~20）；discrete/MEMS 才上百 |
| 基板損耗（substrate loss） | 矽基板導電，磁場感應渦流 + 電容耦合漏電到基板耗能 | 高頻尤甚，進一步拉低 $Q$ |
| capacitor / varactor 損耗 | varactor（壓控電容，用來調 $f_0$）的串聯電阻與有限 $Q_C$ | 調諧範圍越寬，varactor 佔比越大，tank $Q$ 越被它拖累 |
| 外部負載（loaded $Q$） | buffer/下級電路並進來等效並一個 $R_{ext}$，$Q_L<Q_0$（第 1 步） | 量測或驅動越重，有效 $Q$ 越低 → phase noise 越差 |
| 寄生電容 | 走線/device 寄生 $C_{par}$ 並進 tank，吃掉可用的 $C$ 調諧範圍、也可能引入額外損耗 | 限制最高 $f_0$ 與 swing |

- **設計含意**：因為 on-chip $Q$ 卡在 ~10–20，LC 振盪器的 phase noise 改善常常**不是靠提 $Q$（提不太動），而是靠加大 swing 提 $q_{max}$**——這正是 [tank_swing](/06_design_insights/tank_swing) 的主軸。「提高 tank $Q$ 是接近免費的 swing」那條 design knob（同 $I_{bias}$ 下 $R_p$ 大 → swing $\approx\tfrac{4}{\pi}I_{bias}R_p$ 大），其上限就被這裡的 inductor $Q$ 天花板鎖死。
- **為什麼 ring 不靠 $Q$**：ring oscillator 完全沒有諧振 tank（沒有 $Q$），改用級數 $N$、每級電流/swing 當槓桿——這也是為什麼 ISF 的 $\Gamma_{rms}/q_{max}$ 框架（不需要 $Q$）比 Leeson 通用（見 [lc_vs_ring](/06_design_insights/lc_vs_ring)）。

> **誠實標註**：本節的 inductor $Q$ 典型值（5～20）、skin/proximity effect、substrate loss、varactor $Q$ 都是**標準 RFIC 設計知識（外部，非本站 5 篇 PDF；如 Lee《CMOS RFICs》、Razavi《RF Microelectronics》、Niknejad 的 inductor 著作）**。確切數字依製程世代差異很大，這裡只給量級手感。TODO: 若要引用特定製程的 inductor $Q$ 曲線請查該製程文件。

## 適用與失效條件

| 條件 | 成立時（$Q$ 概念乾淨適用） | 失效時會怎樣 |
|---|---|---|
| 存在諧振 tank（LC、crystal、MEMS） | $Q=\omega_0 R_p C$ 等三式成立、$1/Q^2$ scaling 適用 | **ring/relaxation 無諧振 → 沒有 $Q$**，改用 $\Gamma_{rms}/q_{max}$（[lc_vs_ring](/06_design_insights/lc_vs_ring)） |
| 高 $Q$（窄帶）、$\Delta\omega\ll\omega_0/(2Q)$ | 一階展開 $Z\approx R_p/(1+j2Q\Delta\omega/\omega_0)$、Lorentzian 整形準 | 低 $Q$（寬帶）一階近似失準，需用完整 $Z(\omega)$ |
| 損耗集中可等效成單一並聯 $R_p$ | 三種 $Q$ 寫法等價、$4kT/R_p$ 單一雜訊源 | 分佈損耗/多個雜訊源要分別建模（substrate、varactor 各自的 $Q$） |
| 線性、小擾動 | $Q$ 是常數、能量定義成立 | 大訊號下 active core 強非線性使有效阻抗時變（cyclostationary，見 [effective_isf](/03_isf_core_theory/effective_isf)） |
| loaded vs unloaded 分清楚 | 決定 phase noise 用 loaded $Q$；設計 inductor 用 unloaded $Q$ | 混用兩者會高估 $Q$、低估 phase noise |

## 重點回顧

- 並聯 RLC 的 $Q$ 有四個等價寫法：$Q=\omega_0 R_p C=R_p\sqrt{C/L}=R_p/(\omega_0 L)=R_p/R_0$（$R_0=\sqrt{L/C}$），**並聯時 $R_p$ 在分子——$R_p$ 大 → $Q$ 高**。
- 能量定義 $Q=\omega_0\,E_{stored}/P_{diss}$ 與上式精確一致（代 $v=V_p\cos\omega_0 t$ 推得 $\omega_0 R_p C$，$V_p^2$ 全約掉）。
- 無 active core 時能量 $\propto e^{-\omega_0 t/Q}$ 衰減；active core 用 **$-R$（負電導 $G_m\ge1/R_p$）抵消 $R_p$ 的能量損耗**，但**消不掉 $R_p$ 的熱雜訊**。
- $R_p$ 是 tank 熱雜訊電流 $4kT/R_p$（單邊 PSD，A²/Hz）的物理源頭；$R_p=Q\,R_0$，故 $4kT/R_p\propto 1/Q$。
- $Q=\omega_0/\Delta\omega_{3\mathrm{dB}}$：高 $Q$ → 窄帶 → 相位斜率 $-2Q/\omega_0$ 陡 → 頻率被咬死 → phase noise $\propto1/Q^2$（−6 dB/$Q$ 加倍，Leeson；外部、非 5 篇 PDF）。
- **$Q\leftrightarrow\Gamma_{rms}/q_{max}$**：Leeson 的 $1/(2Q)$ 與 [P1] Eq.(21) 的 $\Gamma_{rms}/q_{max}$ 是同一個「雜訊→相位」效率；高 $Q$ = 低 $\Gamma_{rms}/q_{max}$ = 低 phase noise。ISF 版對無 $Q$ 的 ring 也成立。
- 例：$L=1$ nH、$C=1.013$ pF、$R_p=314\ \Omega$ → $f_0=5$ GHz、$Q=10$、$\Delta f_{3\mathrm{dB}}=500$ MHz、$4kT/R_p\approx5.3\times10^{-23}$ A²/Hz。
- 實務天花板：on-chip spiral inductor $Q$ 僅 ~5–20（金屬 $R_s$、skin/proximity、substrate loss、varactor），所以 LC 降 phase noise 常改靠加大 swing（[tank_swing](/06_design_insights/tank_swing)）。
- 來源：RLC/$Q$/$4kTR$ 為標準教科書內容（**外部，非本站 5 篇 PDF**）；$1/Q^2$ 整形屬 Leeson（外部）；$\Gamma_{rms}/q_{max}$ 與 Eq.(21) 為 [P1]（5 篇 PDF 內、已核）。

## 延伸閱讀

- 為何相位無恢復力、$-R$ 對應 limit cycle 振幅恢復：[oscillator_phase](/02_foundations/oscillator_phase)
- $Q$ 如何進 Leeson 模型、$Q\leftrightarrow\Gamma_{rms}/q_{max}$ 完整對照：[derivation_leeson](/99_appendix/derivation_leeson)
- 另一個平方槓桿 $q_{max}$（swing）、on-chip $Q$ 天花板的後果：[tank_swing](/06_design_insights/tank_swing)
- 沒有 $Q$ 的 ring 為何仍能用 ISF 框架：[lc_vs_ring](/06_design_insights/lc_vs_ring)
- 招牌 $1/f^2$ 結果與 $4kT/R_p$ 如何進 Eq.(21)：[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)
- 電阻熱雜訊 $4kTR$ 的基礎：[psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter)
- 全站符號與單位：[統一符號表 Notation](/00_overview/notation)
