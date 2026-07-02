---
title: Phase noise 為何重要、amplitude noise 為何被抑制
description: 用 ISF（相位敏感度）與 [P4] 的 APF（振幅敏感度，單位 1/A）說明為何相位雜訊會累積而振幅雜訊會衰減；ISF 與 APF 在理想 LC 為 quadrature；附 AM-PM 簡述；並以 OU 過程推出振幅雜訊的完整頻譜（平頂 Lorentzian，轉角 f0/2Q）。
---

# Phase noise 為何重要、amplitude noise 為何被抑制

> 先備：[oscillator_phase](/02_foundations/oscillator_phase) · [統一符號表](/00_overview/notation) ｜ 接下來：[lti_vs_ltv](/02_foundations/lti_vs_ltv)

上一頁 [oscillator_phase](/02_foundations/oscillator_phase) 用幾何說明了：noise 對振盪器的
擾動可以拆成**切向（相位）**與**徑向（振幅）**兩個分量。這一頁要回答兩個工程上最實際的問題：

1. **為什麼我們幾乎只擔心 phase noise（相位雜訊），而不太擔心 amplitude noise（振幅雜訊）？**
2. **「振幅擾動會被拉回」這件事，能不能像 ISF 一樣寫成一個敏感度函數？**

答案的關鍵字是 **APF（Amplitude Perturbation Function，振幅擾動函數）**——這是 [P4] 引入的、
ISF 在振幅域的對應物。

> **物理直覺（先講結論）**：limit cycle 在兩個方向的「穩定性」完全不同。**徑向（振幅）方向
> 有恢復力**（負的 Floquet 指數），擾動指數衰減回環上，所以振幅雜訊被振盪器自己壓掉；
> **切向（相位）方向沒有恢復力**（零 Floquet 指數），擾動永久累積，所以相位雜訊一路漫步、
> 沒有上界。同一顆 noise 電流，注入後分給相位的那一份留下、分給振幅的那一份被吃掉——
> ISF $\Gamma$ 描述「分給相位多少」，APF $\Lambda$ 描述「分給振幅多少」。

## 1. 為什麼相位雜訊重要

把振盪器輸出寫成標準分解（[P1] Eq.(1), p.181）：

$$
V_{out}(t)=A(t)\,f\!\big(\omega_0 t+\phi(t)\big).
$$

這裡 $A(t)$ 是瞬時振幅、$\phi(t)$ 是 excess phase（多餘相位，理想相位之外的偏差），$f$ 是
週期穩態波形。雜訊就藏在 $A(t)$ 與 $\phi(t)$ 這兩個調變裡。它們對「時鐘品質」的衝擊不對稱：

- **相位雜訊直接變成 timing jitter**：時脈電路在乎的是「邊緣什麼時候跨過門檻」。那個時刻
  由相位決定：$\Delta t=\Delta\phi/(2\pi f_0)$。相位抖動 = 邊緣時間抖動 = SerDes 眼圖閉合、
  取樣時刻錯位。
- **相位誤差會累積、無上界**：因為相位沒有恢復力（上一頁第 3 步），$\phi(t)$ 做 random walk，
  方差隨時間增長。在頻域呈現為載波旁邊高高的 $1/f^2$（與更靠內的 $1/f^3$）裙擺。這是
  振盪器頻譜不是一根理想 delta、而是有寬度的根本原因。
- **振幅誤差有界、且大多打不進門檻判斷**：振幅在門檻附近的影響，多半又轉回時間誤差
  （見下面 AM–PM），但純振幅起伏本身會被恢復力壓掉，且接收端常用限幅／比較器，對振幅不敏感。

**一句話**：對通訊與時脈系統，**抖動（timing jitter）= 相位的事**。所以整套 Hajimiri–Lee
理論把焦點全押在 $\phi(t)$ 上，先把振幅自由度「合理地丟掉」——下一節解釋為什麼能丟。

## 2. 振幅擾動為何會衰減：APF 與 amplitude decay function

ISF 把「注入電荷 → 相位偏移」寫成（[P1] Eq.(10), p.182）

$$
\Delta\phi=\frac{\Gamma(\omega_0\tau)}{q_{max}}\,\Delta q.
$$

[P4] 對**振幅**做了完全平行的事，定義 **APF $\Lambda(\phi)$（amplitude perturbation
function）**：同一顆注入電流脈衝，投影到 limit cycle 的**徑向**方向，造成多少瞬時振幅偏差。
概念式（[P4] Sec. III-D，APF 定義在 p.2127 附近）：

$$
\Delta A_0\;\propto\;\Lambda(\omega_0\tau)\,\Delta q \quad\Longleftrightarrow\quad \text{APF 是 ISF 的振幅域對應物}.
$$

- **單位**：[P4] 給的 APF 單位是 **$\mathrm{A^{-1}}$（1/安培）**——它把「注入電流」映到「振幅
  的相對偏差」。對照 ISF $\Gamma$ 無因次：兩者結構平行、但歸一化方式不同。
- **關鍵差別——命運不同**：相位偏差用一個 **unit step** $u(t-\tau)$ 表示（永久保持，[P1]
  Eq.(10)）；振幅偏差則乘上一個**衰減函數（amplitude decay function）**，隨時間指數鬆弛回零。
  概念上：

$$
\underbrace{h_\phi(t,\tau)=\frac{\Gamma(\omega_0\tau)}{q_{max}}\,u(t-\tau)}_{\text{相位：階梯，永久}}\qquad\text{vs}\qquad \underbrace{h_A(t,\tau)\;\propto\;\Lambda(\omega_0\tau)\,d(t-\tau)}_{\text{振幅：脈衝}\times\text{衰減,}\;d\to 0}.
$$

  這裡 $d(t-\tau)$ 是 amplitude decay function（振幅衰減函數）。**[P4] Sec. III-F, p.2128（緊接 Eq.(25) 之前的正文）給出確切閉式**
  （已對照原始 PDF 渲染核實；注意 Eq.(25) 本身是 $\Lambda(\phi)=\tau_0\,\tilde\Lambda(\phi)$，APF = $\tau_0$ × 振幅 ISF，而下式的衰減閉式是其前的正文）：

$$
d(t,\phi)=e^{-t/\tau_0},\qquad \tau_0=\frac{2Q}{\omega_{osc}}
$$

  也就是 $\tau_A=\tau_0=2Q/\omega_{osc}$——**振幅的恢復時間常數正比於 $Q$**。直覺：高 $Q$ 的 LC 振幅恢復
  得**慢**（$\tau_0$ 大），但**終究會恢復**（指數衰減）；相位則沒有這個恢復力（unit step，記憶無限長）。
  這就是「為何振幅雜訊有界、相位雜訊發散」最量化的一句話。

> **已核實**：$d(t,\phi)=e^{-t/\tau_0}$、$\tau_0=2Q/\omega_{osc}$ 出自 [P4] Sec. III-F, p.2128 的正文（緊接 Eq.(25) 之前的未編號式；Eq.(25) 本身是 APF 關係 $\Lambda(\phi)=\tau_0\,\tilde\Lambda(\phi)$）。
> （更一般振盪器的衰減率屬 Floquet／PPV 框架，**不在下載的 5 篇 PDF 內**，見 [derivation_floquet_ppv](/99_appendix/derivation_floquet_ppv)。）

- **為何「衰減」就等於「被抑制」**：把振幅雜訊想成對 $h_A$ 做卷積。因為 $d(t-\tau)$ 可積、
  會歸零，過去的振幅擾動**不會累加**，輸出振幅方差收斂到一個**有限**值（一個有恢復力的
  一階低通系統的穩態方差）。反觀相位卷積用的是 $u(t-\tau)$（不可積、不歸零），方差**發散**
  ——這就是 phase noise 累積、amplitude noise 不累積的數學分水嶺。

把 ISF 與 APF 對照成一張表，把整頁濃縮成一格一格：

| 量 | 投影方向 | 敏感度函數 | 脈衝響應核 | 長期命運 | 對 jitter 的影響 |
|---|---|---|---|---|---|
| **相位** $\phi$ | 切向（沿環） | ISF $\Gamma(\omega_0\tau)$，無因次 | $\dfrac{\Gamma}{q_{max}}u(t-\tau)$（階梯） | **累積／發散** | 直接：$\Delta t=\Delta\phi/2\pi f_0$ |
| **振幅** $A$ | 徑向（垂直環） | APF $\Lambda(\omega_0\tau)$，單位 $\mathrm{A^{-1}}$ | $\Lambda\cdot d(t-\tau)$（脈衝×衰減） | **衰減／有界** | 間接，多經 AM–PM |

## 3. 理想 LC：ISF 與 APF 為 quadrature（正交，差 90°）

[P4] Fig. 5, p.2126 同時畫了理想 LC 振盪器的 **ISF、APF、amplitude decay function 與三者關係**，
最漂亮的結論是：

> **在理想 LC 振盪器，ISF 與 APF 互為 quadrature（相差 90°）。**

這完全符合上一頁的幾何：切向與徑向在圓上**處處互相垂直**。理想 LC 的 ISF 是
$\Gamma(\theta)=-\sin\theta$（在零交越最大、在峰值為零）；那麼徑向敏感度（APF）就應該在
**峰值最大、零交越為零**，也就是長得像 $\cos$：

$$
\Gamma_{LC}(\theta)=-\sin\theta\quad\text{（切向）},\qquad \Lambda_{LC}(\theta)\;\propto\;\cos\theta\quad\text{（徑向，與}\Gamma\text{正交）}.
$$

- **物理意義**：在**波峰**踢（$\theta=0$）→ $\Gamma=0$、$\Lambda$ 最大 → **純改振幅**
  （會被吃掉）。在**零交越**踢（$\theta=\pi/2$）→ $|\Gamma|$ 最大、$\Lambda=0$ → **純改相位**
  （永久留著）。這正是上一頁那張
  [waveform_with_impulse_markers](/figures/waveform_with_impulse_markers.png) 的紅／綠標記。
- **單位檢查 / dimension**：$\Gamma$ 無因次、$\Lambda$ 單位 $\mathrm{A^{-1}}$；quadrature 講的是
  **相位（角度）關係**，不是量綱相等。差 90° 指的是兩個敏感度函數作為 $\theta$ 的週期函數，
  傅立葉上一個是 $\sin$、一個是 $\cos$。

> **已核實（[P4] Eq.(26), p.2128）**：上式 $\Lambda_{LC}\propto\cos\theta$
> 的**比例常數**與 APF 的精確歸一化需從 PDF Fig. 5, p.2126 核對。本頁只主張「quadrature（正交）」
> 這個定性關係（[P4] 明確陳述），不寫死振幅常數。

## 4. AM–PM 簡述：振幅雜訊「漏」回相位的後門

如果振幅擾動會被吃掉，為什麼設計上還是要在意它？因為有一條後門叫 **AM–PM conversion
（振幅調變轉相位調變，amplitude-to-phase conversion）**：

- **機制**：真實振盪器的有效振盪頻率會**隨振幅而變**（例如非線性電容 $C(V)$ 隨擺幅變、
  或 tank 的有效相位隨振幅偏移）。於是「振幅起伏 $\Delta A$」經由 $\dfrac{\partial\omega}{\partial A}$
  漏進「相位／頻率起伏」，再被相位的無恢復力特性**永久累積**。
- **後果**：原本應該被壓掉的振幅雜訊，透過 AM–PM 變成了**長壽的相位雜訊**——尤其把
  device 的 $1/f$ 振幅起伏上轉成 close-in（靠近載波）相位雜訊，惡化 $1/f^3$ 區。
- **設計含意**：(i) 讓 $\partial\omega/\partial A\to 0$（例如在電容曲線的平坦點偏壓、加 AM 抑制／
  限幅）；(ii) 在 quadrature 觀念下，把主要 noise 注入安排在「徑向最不敏感」的相位也有幫助。
  詳細的 AM–PM 與 amplitude modulation 分析是 [P4] 的主軸（**進階**，本站只給直覺）。

- **與本站其它頁的接點**：AM–PM 是「為什麼真實 $1/f^3$ 比純 $c_0$ 機制更高」的常見原因之一；
  純粹由 ISF 的 $c_0$ 上轉 $1/f$ 的機制見
  [flicker_upconversion](/03_isf_core_theory/flicker_noise_upconversion) 與 [P1] Eq.(23)–(24)。

## 數值例子（建立手感）

> **例 A 改編**：$q_{max}=1$ pC、$\Delta q=1$ fC、$f_0=5$ GHz，比較注在 zero crossing
> （$\Gamma=-1$，純相位）與注在 peak（$\Gamma\approx 0$，純振幅）的長期後果。

**注在零交越**（$\theta=\pi/2$，$\Gamma=-\sin(\pi/2)=-1$）：

$$
\Delta\phi=\frac{|\Gamma|\,\Delta q}{q_{max}}=\frac{1\times10^{-15}}{10^{-12}}=1\times10^{-3}\ \text{rad}\ \Rightarrow\ \Delta t=\frac{10^{-3}}{2\pi\times5\times10^{9}}\approx31.8\ \text{fs（永久保留）}.
$$

**注在波峰**（$\theta=0$，$\Gamma\approx 0$）：$\Delta\phi\approx 0$，能量幾乎全進振幅；
振幅偏差 $\Delta A$ 在幾個 $\tau_A$（振幅恢復時間常數）後鬆弛回零，**對相位無永久影響**
（除非有 AM–PM 後門）。

- **Dimension check**：$[\text{rad}]/[\text{rad/s}]=[\text{s}]$ ✓。
- **手感**：同一顆 1 fC，注入相位差 90° 就是「31.8 fs 永久 jitter」與「~0 永久影響」的差別。
  這把「為什麼相位敏感度（ISF）形狀如此重要」講得很實在——把噪聲源安排在相位最不敏感
  （$\Gamma$ 小）的相位，等於免費降相位雜訊。

## 適用與失效條件

| 條件 | 成立時 | 失效時會怎樣 |
|---|---|---|
| 有振幅恢復（穩定 limit cycle） | 振幅雜訊衰減、可只追蹤相位 | 弱恢復／高 Q 慢恢復時振幅雜訊壽命變長，不可忽略 |
| AM–PM 可忽略（$\partial\omega/\partial A\approx 0$） | 「丟掉振幅」近似良好 | 強 AM–PM 時振幅雜訊上轉成相位雜訊，需用 [P4] APF 框架 |
| 小訊號擾動 | $\Gamma,\Lambda$ 可線性投影 | 大注入下 ISF/APF 本身被改變、非線性混疊 |
| 理想 LC 對稱 | $\Gamma\perp\Lambda$（quadrature）成立 | 非對稱波形 / ring 時 quadrature 只是近似 |

## 5. 振幅雜訊的頻譜：OU 過程與平頂 Lorentzian

第 2 節說的是**單一顆** kick 的命運：振幅偏差以 $d(t)=e^{-t/\tau_0}$、$\tau_0=2Q/\omega_{osc}$
衰減（[P4] Sec. III-F, p.2128，本站已核實）。但真實的雜訊不是單一顆 kick，而是**連續不斷的
白噪電流**。這一節把「單一 kick 衰減」升級成「連續驅動下的穩態頻譜」，回答兩個問題：

1. **振幅雜訊的完整頻譜 $S_a(\omega)$ 長什麼樣？**（答案：一個「平頂 Lorentzian」，
   轉角在 $\omega_0/2Q$。）
2. **為什麼量測到的振盪器頻譜在遠離載波處會「變平」？** 除了儀器底線之外，還有第二個
   物理原因——AM 平頂。

> **物理直覺（先講結論）**：白噪 = 密集的隨機小 kick 串流。相位側每顆 kick 永久保留
> （unit step）→ 疊加成 random walk → 頻譜 $\propto 1/\omega^2$ 一路到底。振幅側每顆 kick
> 帶著 $e^{-t/\tau_0}$ 的「保鮮期」→ 疊加後只有「最近 $\tau_0$ 內」的 kick 還活著 → 方差有限、
> 頻譜在 $\omega \lt 1/\tau_0$ 處**平掉**。觀察頻率高於 $1/\tau_0$（時間尺度短於 $\tau_0$）時
> 恢復力來不及作用，振幅看起來也像自由積分器——所以高頻端 AM 與 PM 的頻譜**形狀相同**。

### 5.1 從單一 kick 到連續驅動：Langevin / OU 方程式

把第 2 節的振幅動力學線性化（小擾動）：恢復力把振幅偏差以速率 $1/\tau_0$ 拉回、白噪連續
推它。定義 $a(t)\equiv \Delta A/A_0$ 為**相對振幅偏差**（無因次，這樣才能與 $\phi$ [rad]
公平比較），其隨機微分方程（Langevin 方程）是：

$$
da=-\frac{a}{\tau_0}\,dt+\sqrt{c}\,dW(t).
$$

逐項的物理意義與單位：

- $-\dfrac{a}{\tau_0}dt$：**恢復力項**——振幅控制（限幅、非線性飽和）的線性化，正是 [P4]
  單一 kick 衰減 $d(t)=e^{-t/\tau_0}$ 的微分形式。$[a/\tau_0]\cdot[dt]=(1/\text{s})\cdot\text{s}$
  ×無因次 = 無因次 ✓。$\tau_0=2Q/\omega_0$ [s]（[P4] Sec. III-F, p.2128，已核實）。
- $\sqrt{c}\,dW$：**白噪驅動**。$W(t)$ 是標準 Wiener 過程，$\mathrm{Var}[dW]=dt$，
  $[dW]=\sqrt{\text{s}}$；$c$ 是驅動強度，$[c]=1/\text{s}$（若 $a$ 無因次），
  故 $[\sqrt{c}\,dW]=\sqrt{1/\text{s}}\cdot\sqrt{\text{s}}=$ 無因次 ✓。
- **相位方程 = 同一條、拿掉恢復力項**：$d\phi=\sqrt{c}\,dW$（$[c]=\text{rad}^2/\text{s}$）。
  這就是「同一顆白噪源、兩種命運」的最小數學模型。

這種「指數恢復 + 白噪驅動」的過程叫 **Ornstein–Uhlenbeck（OU）過程**。

> **誠實標註**：OU 過程與下面的解法是**標準隨機過程數學**（外部文獻，非本站 5 篇 PDF）：
> G. E. Uhlenbeck and L. S. Ornstein, "On the Theory of the Brownian Motion," *Physical
> Review*, vol. 36, pp. 823–841, 1930。本站來自論文的部分只有**衰減時間常數**
> $\tau_0=2Q/\omega_0$（[P4] Sec. III-F, p.2128，已核實）；把它接上 OU 是教學上的標準組裝。

### 5.2 解 OU：自相關與有限方差（逐步）

**Step 1：積分因子解 SDE。** 對 $e^{t/\tau_0}a$ 微分：

$$
d\!\left(e^{t/\tau_0}a\right)=e^{t/\tau_0}\left(da+\frac{a}{\tau_0}dt\right)=e^{t/\tau_0}\sqrt{c}\,dW,
$$

兩邊從 $-\infty$ 積到 $t$（穩態：初始條件早已衰減光）：

$$
a(t)=\sqrt{c}\int_{-\infty}^{t}e^{-(t-s)/\tau_0}\,dW(s).
$$

**物理意義**：現在的振幅偏差 = 過去每一顆 kick（$dW(s)$）各自乘上自己的衰減
$e^{-(t-s)/\tau_0}$ 之後疊加——這正是第 2 節 [P4] 的 $d(t)$ 對雜訊做卷積的結果，
和相位側 $\phi(t)=\sqrt{c}\int^t dW$（每顆 kick 權重恆為 1）成鮮明對比。

**Step 2：自相關。** 用「不同時刻的 $dW$ 不相關、$\mathrm{E}[dW^2]=ds$」
（Itô isometry，標準結果），對 $\tau\ge 0$：

$$
\begin{aligned}
R_a(\tau)&\equiv \mathrm{E}[a(t)\,a(t+\tau)]
=c\int_{-\infty}^{t}e^{-(t-s)/\tau_0}\,e^{-(t+\tau-s)/\tau_0}\,ds\\
&=c\,e^{-\tau/\tau_0}\int_{-\infty}^{t}e^{-2(t-s)/\tau_0}\,ds
=c\,e^{-\tau/\tau_0}\cdot\frac{\tau_0}{2}
\qquad(\text{代 }u=t-s,\ \int_0^\infty e^{-2u/\tau_0}du=\tfrac{\tau_0}{2}),
\end{aligned}
$$

$$
\boxed{\ R_a(\tau)=\frac{c\,\tau_0}{2}\,e^{-\lvert\tau\rvert/\tau_0}\ }
$$

**Step 3：方差有限。** $\mathrm{Var}[a]=R_a(0)=c\tau_0/2$。
單位：$(1/\text{s})\cdot\text{s}=$ 無因次 ✓（$a^2$）。對照相位：
$\mathrm{Var}[\phi(t)]=c\,t$ **隨時間線性發散**（random walk，見
[lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth) 的 $2D\lvert t\rvert$，
對應 $c=2D$）。**方差「有限 vs 發散」就是第 2 節「衰減核 vs 階梯核」的穩態版本。**

### 5.3 Wiener–Khinchin → 平頂 Lorentzian（逐步積分）

平穩過程的 PSD 是自相關的傅立葉變換（Wiener–Khinchin，標準結果）。先算
$e^{-\lvert\tau\rvert/\tau_0}$ 的變換（跟 Lorentzian 線寬頁同一招，把絕對值拆兩半）：

$$
\int_{-\infty}^{\infty}e^{-\lvert\tau\rvert/\tau_0}e^{-j\omega\tau}\,d\tau
=\frac{1}{1/\tau_0+j\omega}+\frac{1}{1/\tau_0-j\omega}
=\frac{2/\tau_0}{1/\tau_0^2+\omega^2}
=\frac{2\tau_0}{1+\omega^2\tau_0^2}.
$$

乘上 $R_a$ 的前置係數 $c\tau_0/2$：

$$
\boxed{\ S_a(\omega)=\frac{c\,\tau_0^2}{1+\omega^2\tau_0^2}\ }\qquad\left[\frac{1}{\text{Hz}}\right]
$$

- **慣例（factor-of-2 紀律）**：本節全程用**雙邊（two-sided）PSD**（$\pm\infty$ 積分、
  反變換帶 $1/2\pi$）。模擬用的 `scipy.signal.welch` 回傳**單邊** = 2×雙邊，所以 lab_28
  圖上的理論線是 $2c/\omega^2$ 與 $2c\tau_0^2/(1+\omega^2\tau_0^2)$。**轉角頻率、
  交叉頻率、PM/AM 比值都是「比出來的」，對單邊/雙邊、$\mathcal{L}=S_\phi/2$ 或 /4
  慣例完全不敏感**——只有 dBc/Hz 絕對值才需要指明慣例（見 5.6）。
- **單位檢查**：$[c\tau_0^2]=(1/\text{s})\cdot\text{s}^2=\text{s}=1/\text{Hz}$ ✓
  （無因次量的 PSD）。
- **兩個極限（形狀）**：
  - $\omega\tau_0\ll 1$（低頻）：$S_a\to c\tau_0^2$，**平頂**。恢復力來得及把方差鎖住。
  - $\omega\tau_0\gg 1$（高頻）：$S_a\to c/\omega^2$，**跟自由積分器一模一樣**。
    時間尺度短於 $\tau_0$ 時恢復力根本來不及動作。
- **轉角（corner）**：兩漸近線相交於
  $$
  \omega_c=\frac{1}{\tau_0}=\frac{\omega_0}{2Q}\ \ [\text{rad/s}]
  \qquad\Longleftrightarrow\qquad
  f_c=\frac{\omega_c}{2\pi}=\frac{f_0}{2Q}\ \ [\text{Hz}],
  $$
  在轉角處 $S_a=c\tau_0^2/2$（比平頂低 3 dB）。**Hz 形式請記 $f_c=f_0/2Q$**。
- **功率守恆自檢**：$\dfrac{1}{2\pi}\displaystyle\int_{-\infty}^{\infty}
  \frac{c\tau_0^2\,d\omega}{1+\omega^2\tau_0^2}=\frac{c\tau_0^2}{2\pi}\cdot\frac{\pi}{\tau_0}
  =\frac{c\tau_0}{2}=\mathrm{Var}[a]$ ✓（積分公式
  $\int d\omega/(1+\omega^2\tau_0^2)=\pi/\tau_0$）。

這個形狀叫**平頂 Lorentzian**：跟 [lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth)
頁載波線形 $D/(D^2+\Delta\omega^2)$ 是同一族函數，但**物理主角不同**——那邊是「相位
random walk 造成的**載波**線形」（轉角 $=D$，很窄）；這邊是「振幅恢復力造成的 **AM 雜訊**
頻譜」（轉角 $=\omega_0/2Q$，很寬）。

### 5.4 對照相位：沒有恢復力，$1/\omega^2$ 一路到底

同一顆白噪源驅動相位：$d\phi=\sqrt{c}\,dW$，即 $\phi$ 是白噪的積分。積分器
$\lvert H(j\omega)\rvert^2=1/\omega^2$ 作用在雙邊位準 $c$ 的白噪上：

$$
S_\phi(\omega)=\frac{c}{\omega^2}\qquad\left[\frac{\text{rad}^2}{\text{Hz}}\right].
$$

一格一格對照（表內 $\lvert\cdot\rvert$ 為絕對值）：

| | 相位 $\phi$ | 振幅 $a$ |
|---|---|---|
| 方程式 | $d\phi=\sqrt{c}\,dW$ | $da=-(a/\tau_0)dt+\sqrt{c}\,dW$ |
| 恢復力 | 無（零 Floquet 指數） | $-a/\tau_0$，$\tau_0=2Q/\omega_0$（[P4]） |
| 平穩？ | 否（random walk） | 是（OU） |
| 方差 | $c\,t$，發散 | $c\tau_0/2$，有限 |
| 頻譜（雙邊） | $c/\omega^2$ | $c\tau_0^2/(1+\omega^2\tau_0^2)$ |
| 近 DC | 發散（實際被 Lorentzian 線形取代） | 平頂 $c\tau_0^2$ |
| 遠端 $\omega\tau_0\gg1$ | $c/\omega^2$ | $c/\omega^2$（**相同！**） |

由兩式直接相除得一條好用的恆等式（等驅動）：

$$
\frac{S_a(\omega)}{S_\phi(\omega)}=\frac{\omega^2\tau_0^2}{1+\omega^2\tau_0^2}\ \le\ 1,
$$

在 $\omega=\omega_c$ 時比值 $=1/2$（差 3 dB）、$\omega=10\,\omega_c$ 時 $=100/101=0.990$。
**等驅動下 AM 頻譜處處低於 PM、但在遠端趨近相等。**

### 5.5 量測總邊帶 = PM + AM：頻譜為何在底線「之前」就變平

頻譜分析儀（SA）看到的載波旁邊帶是 **PM 與 AM 的總和**。AM 的邊帶記帳與
[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) 的 PM
小角推導完全平行：取 $x(t)=[1+a(t)]\cos\omega_0 t$、$a(t)=a_p\cos\omega_m t$（$a_p\ll1$）：

$$
x(t)=\cos\omega_0 t+\frac{a_p}{2}\cos\big((\omega_0+\omega_m)t\big)+\frac{a_p}{2}\cos\big((\omega_0-\omega_m)t\big),
$$

每個邊帶相對載波的功率 $=(a_p/2)^2$；而 $a$ 的功率密度給 $S_a=a_p^2/2$，故每邊帶密度
$=S_a/2$——**跟 PM 的 $\mathcal{L}\approx S_\phi/2$ 一模一樣的係數**（同一慣例下）。
差別只在**符號**：AM 上下邊帶同號、PM 反號（$-\tfrac{\phi_p}{2}\cos(\omega_0-\omega_m)t
+\tfrac{\phi_p}{2}\cos(\omega_0+\omega_m)t$）。功率上 SA 分不出來；
用 quadrature mixer 的鑑相法天然拒斥 AM（見
[measurement_and_spurs](/06_design_insights/measurement_and_spurs)）。於是：

$$
\mathcal{L}_{tot}(\Delta f)\approx\frac{S_\phi(\Delta f)+S_a(\Delta f)}{2}\qquad(\text{同一 }/2\text{ 慣例；比較 PM/AM 只需比 }S_\phi\text{ vs }S_a).
$$

**情況一：等驅動（$c_a=c_\phi=c$）。** 在理想 LC 這是自然基準：切向/徑向投影分別為
$-\sin\theta$ 與 $\cos\theta$（[P4] Eq.(26), p.2128 的 quadrature，已核實；歸一化常數
本頁沿第 3 節立場不寫死），兩者 rms 相同。此時：

- PM skirt 漸近線 $c/\omega^2$ 與 AM 平頂 $c\tau_0^2$ 相交於
  $c/\omega^2=c\tau_0^2\Rightarrow\omega=1/\tau_0=\omega_c$——**漸近線交點恰好就是轉角**。
- 實際曲線**永不相交**（上面比值 $\le1$）；遠端 AM 貢獻最多把總邊帶抬高
  $10\log_{10}2\approx3$ dB。

**情況二：AM 驅動較強（$R\equiv c_a/c_\phi \gt 1$）。** 真實電路常見：偏壓/尾流雜訊、
弱限幅都會把 AM 驅動推高。交叉條件三行推完：

$$
\frac{c_\phi}{\omega^2}=\frac{R\,c_\phi\,\tau_0^2}{1+\omega^2\tau_0^2}
\;\Longrightarrow\;1+\omega^2\tau_0^2=R\,\omega^2\tau_0^2
\;\Longrightarrow\;\boxed{\ \omega_x=\frac{\omega_c}{\sqrt{R-1}}\ \Longleftrightarrow\ f_x=\frac{f_c}{\sqrt{R-1}}\ }
$$

（$R\to1^+$ 時 $f_x\to\infty$，與「等驅動永不相交」一致 ✓；$R\le1$ 無解。）
在 $f_x \lt \Delta f \lt f_c$ 之間 **AM 平頂高於 PM skirt**：量測頻譜先按 $-20$ dB/dec
下降、在 $f_x$ 拐平、平到 $f_c$ 之後才恢復 $-20$ dB/dec（此時已是 AM 主導）。這個
「肩膀（pedestal）」發生在儀器底線**之上、之前**——這就是**量測頻譜遠端變平的第二個
原因**（第一個是加性/儀器底線；近載波的變平則是另一回事——Lorentzian 線形，見
[lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth)）。

### 5.6 數值例子（$Q=10$、$f_0=5$ GHz，接 canonical 例 B）

**(a) 振幅恢復時間常數**：

$$
\tau_0=\frac{2Q}{\omega_0}=\frac{2\times10}{2\pi\times5\times10^9\ \text{rad/s}}=6.366\times10^{-10}\ \text{s}=0.637\ \text{ns}.
$$

Dimension check：無因次 ÷ (rad/s) = s ✓（rad 無因次）。5 GHz 週期 $T=0.2$ ns，
所以振幅擾動大約「活」3 個週期左右。

**(b) AM 轉角**：$f_c=f_0/2Q=5\times10^9/20=250$ MHz（$\omega_c=1.571\times10^9$ rad/s）。
$Q$ 越高、轉角越低、平頂越往載波靠。

**(c) 等驅動交叉**：$f_x=f_c=250$ MHz（漸近線交點；實際曲線只在遠端趨近、AM 最多 +3 dB）。

**(d) $R=10$**：$f_x=250/\sqrt{9}=83.3$ MHz。

**(e) dBc/Hz 圖像**（錨定例 B：$\mathcal{L}(1\ \text{MHz})=-148$ dBc/Hz，
[P1] Eq.(21), p.185 的 SSB /4 慣例；若用時域 /2 慣例錨 $-145$，下列 dBc/Hz 一律 +3 dB，
**交叉/轉角頻率不變**）：

- PM skirt 外插到 250 MHz：$-148-20\log_{10}(250)=-195.96$ dBc/Hz。
- 設 AM 驅動比 PM 強 40 dB（$R=10^4$，示意值）：AM 平頂 $=-195.96+40=-155.96$ dBc/Hz、
  交叉 $f_x=250\ \text{MHz}/\sqrt{10^4-1}\approx2.50$ MHz。
- 儀器底線 $-170$ dBc/Hz 要到 $\Delta f=10^{(170-148)/20}=12.6$ MHz 才會接住 PM skirt——
  但 AM 平頂在 **2.5 MHz** 就先接手了：**頻譜在底線之前就變平**。

一行一驗證（自含，`# ->` 為實際執行輸出）：

```python
import numpy as np
f0, Q = 5e9, 10.0                       # [Hz], [-]
omega0 = 2 * np.pi * f0                 # [rad/s]
tau0 = 2 * Q / omega0                   # [s]  [P4] Sec. III-F, p.2128
print(round(tau0 * 1e9, 4))             # -> 0.6366
fc = f0 / (2 * Q)                       # [Hz] = 1/(2 pi tau0)
print(round(fc / 1e6, 1))               # -> 250.0
c = 0.5                                 # 共同白噪驅動（雙邊位準）[1/s]
print("{:.3e}".format(c * tau0 / 2))    # -> 1.592e-10
print("{:.3e}".format(2 * c * tau0**2)) # -> 4.053e-19
print(round(fc / np.sqrt(10 - 1) / 1e6, 2))    # -> 83.33
L_pm_250M = -148 - 20 * np.log10(250.0)        # [dBc/Hz] SSB /4 錨
print(round(L_pm_250M, 2))              # -> -195.96
print(round(L_pm_250M + 40, 2))         # -> -155.96
print(round(fc / np.sqrt(1e4 - 1) / 1e6, 2))   # -> 2.5
```

（第 3、4 個輸出分別是 $\mathrm{Var}[a]=c\tau_0/2$ 與單邊平頂 $2c\tau_0^2$
[1/Hz]，供對照下方模擬。）

### 5.7 模擬驗證：lab_28（同一顆白噪源、兩種命運）

`simulations/lab_28_am_noise.py` 用**同一條**白噪序列（seed 28）同時驅動：
(i) Wiener 相位 $\phi=\sqrt{c}\sum dW$；(ii) OU 振幅（精確離散化
$a_{k+1}=e^{-dt/\tau_0}a_k+\sigma_{step}\,\xi_k$，$\sigma_{step}^2=\tfrac{c\tau_0}{2}(1-e^{-2dt/\tau_0})$）；
(iii) 驅動 ×10 的 OU（$R=10$）。參數表：

| 參數 | 值 | 單位 | 說明 |
|---|---|---|---|
| $f_0$ | $5\times10^9$ | Hz | canonical |
| $Q$ | 10 | — | 低 Q on-chip LC 量級 |
| $\tau_0$ | 0.6366 | ns | $2Q/\omega_0$（[P4]） |
| $c$ | 0.5 | rad²/s（$\phi$）；1/s（$a$） | 共同驅動；$c=2D\Rightarrow D=0.25$ rad²/s（toy 值；true-LC canonical 為 $c=\kappa^2=0.25$、$D=0.125$，v5） |
| $f_s$ | $20\times10^9$ | Hz | $\gg f_c$ |
| $N$ | $2^{22}$ | — | $T=210\ \mu$s $\gg\tau_0$ |

實際執行輸出（節錄，`# ->` 與程式列印逐行對齊）：

```text
tau0 [ns]                    = 0.6366      # -> 0.6366
f_c = f0/(2Q) [MHz]          = 250.0       # -> 250.0
Var[a] theory c*tau0/2       = 1.592e-10   # -> 1.592e-10
Var[a] simulated             = 1.587e-10   # -> 1.587e-10
tau0 from R_a(tau)=e^-1 [ns] = 0.6353      # -> 0.6353
AM plateau theory 2c*tau0^2  = 4.053e-19   # -> 4.053e-19
AM plateau simulated         = 4.102e-19   # -> 4.102e-19
AM corner measured [MHz]     = 239.9       # -> 239.9
S_a/S_phi @ 2.5 GHz theory   = 0.990       # -> 0.990
S_a/S_phi @ 2.5 GHz sim      = 0.991       # -> 0.991
equal-drive asymptote cross  = 250.0 MHz   # -> 250.0
R=10 crossover theory [MHz]  = 83.33       # -> 83.33
R=10 crossover sim [MHz]     = 83.31       # -> 83.31
```

![OU 振幅雜訊頻譜與 Wiener 相位對照；右：AM 平頂使量測頻譜在底線之前變平](/figures/am_noise_spectrum.png)

**如何解讀**：

- **左圖**：藍（$S_\phi$）沿 $-20$ dB/dec 一路到底；橘（等驅動 $S_a$）在低頻鎖成平頂
  （量測 $4.10\times10^{-19}$ /Hz vs 理論 $4.05\times10^{-19}$）、在 $f_c=250$ MHz 拐彎
  （量測 $-3$ dB 點 239.9 MHz，偏低約 4%——welch 分段平均 + 平滑造成，屬估計偏差非物理）、
  高頻端與 $S_\phi$ 重合（2.5 GHz 處比值 0.991 vs 理論 0.990）。綠（$R=10$）在
  **83.3 MHz**（量測 83.31，理論 83.33）穿越 PM skirt。
- **時域對照**：從自相關量到的衰減常數 0.6353 ns ≈ 理論 0.6366 ns——這直接驗證了
  [P4] 的 $d(t)=e^{-t/\tau_0}$ 在連續驅動下仍然是頻譜的骨架。
- **右圖**（理論示意，錨定例 B）：黑色總邊帶在 2.5 MHz 拐平、$-156$ dBc/Hz 平台一路到
  250 MHz、再恢復 $-20$ dB/dec；紅點線（$-170$ dBc/Hz 底線）在更下面——**平坦不是底線
  造成的**。
- **誠實註記**：(i) 左圖 $\gtrsim3$ GHz 處模擬略高於理論線，是離散化（$\omega\,dt$ 不再
  $\ll1$）與混疊的 artifact，非物理。(ii) $R=40$ dB 是**示意**參數——實際的 AM/PM 驅動比
  由拓樸決定（尾流、偏壓、限幅強度）；等驅動時 AM 對總邊帶最多貢獻 +3 dB。(iii) 本模擬是
  基頻等效 toy model（直接模擬 $a,\phi$ 兩個慢變數），非 transistor-level。

### 5.8 本節的適用與失效條件

| 條件 | 成立時 | 失效時會怎樣 |
|---|---|---|
| 小擾動線性化（$\lvert a\rvert\ll1$） | OU 模型成立 | 大擾動進入非線性限幅，頻譜偏離 Lorentzian |
| 單一振幅衰減模態、$\tau_0=2Q/\omega_0$ | 轉角就在 $f_0/2Q$ | 非 LC 拓樸／多模態時衰減率不同（一般情形屬 Floquet 框架，非本站 5 篇 PDF） |
| 白噪驅動 | 平頂是平的 | flicker AM 會在平頂內再疊 $1/f$ 上升 |
| 忽略 AM–PM（第 4 節） | AM 與 PM 各走各的 | AM 經 $\partial\omega/\partial A$ 漏進 PM，close-in 惡化 |
| SA 量測（AM+PM 都收） | 5.5 的總邊帶公式適用 | 鑑相法量測時 AM 被拒斥，看不到 AM 平頂 |

## 重點回顧

- 通訊與時脈系統在意的抖動 **= 相位的事**；相位無恢復力 → 累積 → $1/f^2$、$1/f^3$ 裙擺。
- 振幅有恢復力 → 擾動指數衰減（amplitude decay function $d(t-\tau)\to 0$）→ 方差有界、被抑制。
- **APF $\Lambda(\omega_0\tau)$（單位 $\mathrm{A^{-1}}$）是 ISF 在振幅域的對應物**；相位核是
  階梯 $u$、振幅核是 脈衝×衰減。
- 理想 LC：$\Gamma\propto-\sin\theta$（切向）與 $\Lambda\propto\cos\theta$（徑向）**互為
  quadrature（差 90°）**——[P4] Fig. 5, p.2126。
- **AM–PM** 是振幅雜訊漏回相位的後門：$\partial\omega/\partial A\neq 0$ 時要當心。
- 例 A：1 fC 注零交越 → 31.8 fs 永久 jitter；注波峰 → ~0 永久影響。
- **白噪連續驅動 + 指數恢復（[P4] $\tau_0=2Q/\omega_0$）＝ OU 過程**：
  $S_a=c\tau_0^2/(1+\omega^2\tau_0^2)$——平頂 Lorentzian，轉角 $f_c=f_0/2Q$
  （$Q=10$、5 GHz → $\tau_0=0.64$ ns、$f_c=250$ MHz）；相位無恢復力 → $c/\omega^2$ 一路到底。
- **量測頻譜遠端變平的第二個原因是 AM 平頂**（第一個是儀器/加性底線）：等驅動時漸近線
  交點恰在 $f_c$、AM 最多 +3 dB；AM 驅動較強（$R\gt1$）時交叉 $f_x=f_c/\sqrt{R-1}$，
  例：$R=10\to83.3$ MHz。SA 量到 AM+PM、鑑相法拒斥 AM。
- 來源：[P4]（APF / amplitude decay / quadrature，Sec. III-D–E、Fig. 5, p.2126，已核實）；相位側來自 [P1] Eqs.(1),(10)；OU 過程為標準隨機過程數學（外部文獻 Uhlenbeck–Ornstein 1930）。

## 延伸閱讀

- 上游幾何（切向 vs 徑向）：[oscillator_phase](/02_foundations/oscillator_phase)
- 相位敏感度的精確推導：[從 impulse 到 phase shift 的推導](/03_isf_core_theory/impulse_to_phase_shift)
- 為何敏感度是週期時變的：[LTI vs LTV](/02_foundations/lti_vs_ltv)
- $c_0$ 如何把 $1/f$ 上轉（與 AM–PM 並列的另一機制）：[flicker_upconversion](/03_isf_core_theory/flicker_noise_upconversion)
- 近載波的另一種「變平」（相位 random walk → Lorentzian 線形）：[lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth)
- 量測上如何分離 AM/PM（SA vs 鑑相法 vs cross-correlation）：[measurement_and_spurs](/06_design_insights/measurement_and_spurs)
- 全站符號（APF $\Lambda$ 已登錄）：[統一符號表 Notation](/00_overview/notation)
