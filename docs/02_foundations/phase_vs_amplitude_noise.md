---
title: Phase noise 為何重要、amplitude noise 為何被抑制
description: 用 ISF（相位敏感度）與 [P4] 的 APF（振幅敏感度，單位 1/A）說明為何相位雜訊會累積而振幅雜訊會衰減；ISF 與 APF 在理想 LC 為 quadrature；附 AM-PM 簡述。
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

## 重點回顧

- 通訊與時脈系統在意的抖動 **= 相位的事**；相位無恢復力 → 累積 → $1/f^2$、$1/f^3$ 裙擺。
- 振幅有恢復力 → 擾動指數衰減（amplitude decay function $d(t-\tau)\to 0$）→ 方差有界、被抑制。
- **APF $\Lambda(\omega_0\tau)$（單位 $\mathrm{A^{-1}}$）是 ISF 在振幅域的對應物**；相位核是
  階梯 $u$、振幅核是 脈衝×衰減。
- 理想 LC：$\Gamma\propto-\sin\theta$（切向）與 $\Lambda\propto\cos\theta$（徑向）**互為
  quadrature（差 90°）**——[P4] Fig. 5, p.2126。
- **AM–PM** 是振幅雜訊漏回相位的後門：$\partial\omega/\partial A\neq 0$ 時要當心。
- 例 A：1 fC 注零交越 → 31.8 fs 永久 jitter；注波峰 → ~0 永久影響。
- 來源：[P4]（APF / amplitude decay / quadrature，Sec. III-D、Fig. 5, p.2126，部分標
  TODO 待核）；相位側來自 [P1] Eqs.(1),(10)。

## 延伸閱讀

- 上游幾何（切向 vs 徑向）：[oscillator_phase](/02_foundations/oscillator_phase)
- 相位敏感度的精確推導：[從 impulse 到 phase shift 的推導](/03_isf_core_theory/impulse_to_phase_shift)
- 為何敏感度是週期時變的：[LTI vs LTV](/02_foundations/lti_vs_ltv)
- $c_0$ 如何把 $1/f$ 上轉（與 AM–PM 並列的另一機制）：[flicker_upconversion](/03_isf_core_theory/flicker_noise_upconversion)
- 全站符號（APF $\Lambda$ 已登錄）：[統一符號表 Notation](/00_overview/notation)
