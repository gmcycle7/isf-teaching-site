---
title: 數學工具箱 Math Identities
description: 本站推導反覆用到的數學工具——傅立葉級數/Parseval、LTV 卷積、Wiener–Khinchin、dB 換算、積分器響應、small-angle PM、三角恆等式、random walk variance——每條附簡短證明與用到它的頁。
---

# 數學工具箱 Math Identities

> **See also**：[notation](/00_overview/notation)（權威符號與單位）、[glossary](/99_appendix/glossary)（中英術語直覺）、[convolution_derivation](/03_isf_core_theory/convolution_derivation)（LTV 卷積用到本頁工具）、[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)（Parseval/積分器響應的應用場）

ISF 理論看起來很「電路」，但骨架其實是幾條標準的數學工具反覆組合。這頁把它們集中起來，
給每條一個**簡短證明或出處**，並標明**站內哪一頁用到它**。讀推導卡住時回來查，
比硬背公式有用。

> **怎麼用這頁**：每一節先給「一句話它在說什麼」，再給「為什麼成立」（證明或出處），
> 最後給「站內用在哪」。所有量都帶單位——做 dimension check（因次檢查）永遠是抓錯最快的方法。

---

## 1. 傅立葉級數與 Parseval（ISF 的諧波分解）

**一句話**：任何 $2\pi$ 週期的實函數可以拆成 DC 加一串諧波；它的「總能量」等於各諧波能量之和。
這就是把 ISF $\Gamma(\omega_0\tau)$ 拆成 $c_0,c_1,c_2,\dots$ 的數學依據。

ISF 是無因次、$2\pi$ 週期的函數，寫成餘弦級數（[P1] Eq.(12), p.183）：

$$
\Gamma(\omega_0\tau)=\frac{c_0}{2}+\sum_{n=1}^{\infty}c_n\cos(n\omega_0\tau+\theta_n)
$$

把自變數記成 $x=\omega_0\tau$。**Parseval 關係**（[P1] Eq.(20), p.185）：

$$
\sum_{n=0}^{\infty}c_n^2=\frac{1}{\pi}\int_0^{2\pi}|\Gamma(x)|^2\,dx=2\,\Gamma_{rms}^2
$$

**為什麼成立（簡短證明）**：把級數平方後對 $0$ 到 $2\pi$ 積分。不同諧波的餘弦互相正交，

$$
\int_0^{2\pi}\cos(mx+\theta_m)\cos(nx+\theta_n)\,dx=\pi\,\delta_{mn}\quad(m,n\ge1),
$$

所以交叉項全部消掉，只剩各自的平方項：每個 $c_n\cos(\cdot)$ 項貢獻 $c_n^2\cdot\pi$，DC 項
$\left(\frac{c_0}{2}\right)^2$ 貢獻 $\left(\frac{c_0}{2}\right)^2\cdot 2\pi=\frac{c_0^2}{2}\pi$。
兩邊除以 $\pi$ 得 $\sum_{n=1}^{\infty}c_n^2+\frac{c_0^2}{2}$。Hajimiri–Lee 把 DC 項記成
$\frac{c_0^2}{2}$（注意 $n=0$ 那一項在求和裡只算半個），整理後恰是上式的形式。

**rms 的定義一致性檢查**：$\Gamma_{rms}^2=\frac{1}{2\pi}\int_0^{2\pi}|\Gamma(x)|^2\,dx$
（rms 就是「均方根」，先平方、取平均、再開根）。把它代進 Parseval 右邊：
$\frac{1}{\pi}\int=2\cdot\frac{1}{2\pi}\int=2\Gamma_{rms}^2$ ✓。

**數值手感**：理想 LC 的 $\Gamma(\theta)=-\sin\theta$，只有 $c_1=1$（其餘為 0）。
$\Gamma_{rms}^2=\frac{1}{2\pi}\int_0^{2\pi}\sin^2\theta\,d\theta=\frac12$，所以 $\Gamma_{rms}=1/\sqrt2\approx0.707$；
Parseval 右邊 $2\times\frac12=1=c_1^2$ ✓。

**站內用到**：[fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf)（把 ISF 分諧波、
解釋 $n\omega_0$ 附近 noise 如何下轉）、[rms_isf](/03_isf_core_theory/rms_isf)、
[lab_05](/04_simulation_labs/lab_05_isf_fourier_coefficients)（數值驗證 $\sum c_n^2=2\Gamma_{rms}^2$）。

---

## 2. 卷積與 LTI／LTV 的差別（為什麼振盪器是「時變」）

**一句話**：LTI（線性非時變）系統的脈衝響應只看「相隔多久」$t-\tau$；LTV（線性時變）系統
還要看「在什麼時刻踢」$\tau$。振盪器對 noise 是 LTV，這是 ISF 理論的核心。

LTI 的疊加是標準卷積：

$$
y(t)=\int_{-\infty}^{\infty}h(t-\tau)\,x(\tau)\,d\tau .
$$

- **核心特徵**：$h$ 只依賴差值 $t-\tau$（time-invariant）。輸入延遲，輸出原樣延遲。

振盪器的 excess-phase 脈衝響應卻是（[P1] Eq.(10), p.182）：

$$
h_\phi(t,\tau)=\frac{\Gamma(\omega_0\tau)}{q_{max}}\,u(t-\tau).
$$

它**同時**依賴 $\tau$（透過 $\Gamma(\omega_0\tau)$——踢在波形哪個相位）與 $t-\tau$
（透過 step $u(t-\tau)$——踢完之後永久保留）。把所有過去 noise 疊起來（[P1] Eq.(11), p.182）：

$$
\phi(t)=\int_{-\infty}^{\infty}h_\phi(t,\tau)\,i_n(\tau)\,d\tau=\frac{1}{q_{max}}\int_{-\infty}^{t}\Gamma(\omega_0\tau)\,i_n(\tau)\,d\tau .
$$

**為什麼是 LTV 而非 LTI**：因為 $\Gamma(\omega_0\tau)$ 是注入**絕對時刻**的週期函數。同一顆 impulse，
在波峰踢（$\Gamma\approx0$）幾乎不改相位，在 zero crossing 踢（$|\Gamma|$ 最大）改最多。
這正是 [P1] Sec. III 的主張 C1：「振盪器對 noise 是 linear time-variant，不是 LTI。」

**單位檢查**：$h_\phi$ 的單位是 $1/\text{C}$（$\Gamma$ 無因次、$q_{max}$ 是 C、$u$ 無因次），
$\int h_\phi\, i_n\, d\tau$ 的單位 $=(1/\text{C})\cdot\text{A}\cdot\text{s}=(1/\text{C})\cdot\text{C}=$ 無因次 $=$ rad ✓。

**站內用到**：[impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift)、
[convolution_derivation](/03_isf_core_theory/convolution_derivation)、
[lab_04](/04_simulation_labs/lab_04_impulse_injection_sweep)（`lti_vs_ltv_impulse_response.png`：
LTI 的階高固定、LTV 的階高隨注入相位變）。

---

## 3. 積分器的頻率響應 $1/(j\omega)$（為什麼白噪 → 1/f² 相位雜訊）

**一句話**：相位是 noise 電流「積分」出來的（Eq.(11) 的上限是 $t$）；積分器在頻域是
$1/(j\omega)$，功率上是 $1/\omega^2$。這就是 $-20$ dB/dec 斜率的來源。

理想積分器 $y(t)=\int_{-\infty}^{t}x(\tau)\,d\tau$，對單頻 $x(t)=e^{j\omega t}$：

$$
\int^{t}e^{j\omega\tau}\,d\tau=\frac{1}{j\omega}e^{j\omega t}\;\Rightarrow\;H(j\omega)=\frac{1}{j\omega}.
$$

- **幅度**：$|H(j\omega)|=1/\omega$。**功率（PSD 乘子）**：$|H|^2=1/\omega^2$。
- **dB 斜率**：$10\log_{10}(1/\omega^2)=-20\log_{10}\omega$，每十倍頻 $-20$ dB——就是 phase noise 的
  $1/f^2$ 區斜率。

**接到 ISF**：把 $\Gamma$ 的 rms 當成等效增益，noise 電流 PSD $S_i$ 經「乘 $\Gamma_{rms}/q_{max}$
再積分」得到 phase PSD：

$$
S_\phi(\Delta\omega)=\frac{\Gamma_{rms}^2}{q_{max}^2}\cdot\frac{S_i}{\Delta\omega^2}.
$$

- **單位檢查**（用 $\text{C}=\text{A}\cdot\text{s}$）：

$$
\frac{1}{\text{C}^2}\cdot\frac{\text{A}^2/\text{Hz}}{(\text{rad/s})^2}=\frac{\text{A}^2/\text{Hz}}{\text{C}^2\cdot\text{s}^{-2}}=\frac{\text{A}^2/\text{Hz}}{\text{A}^2}=\frac{1}{\text{Hz}}=\text{rad}^2/\text{Hz}\ \checkmark
$$

**factor-of-2 註記**：用上式（時域乾淨推導）得 $\mathcal{L}=\frac12 S_\phi$，對應分母 $2\Delta\omega^2$；
而 [P1] Eq.(21), p.185 寫成 $4\Delta\omega^2$。差的 2 倍是 SSB 記帳慣例，是文獻著名小爭議，
**不影響** $\Gamma_{rms}^2/q_{max}^2$ scaling 與 $-20$ dB/dec 斜率。詳見
[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)。

**站內用到**：[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)、
[lab_06](/04_simulation_labs/lab_06_white_noise_phase_noise)。

---

## 4. 隨機過程的 PSD 與 Wiener–Khinchin 定理

**一句話**：一個平穩隨機過程的「功率譜密度」（PSD）是它「自相關函數」的傅立葉轉換。
這條把時域的 noise（自相關）與頻域的 noise（PSD）連起來，是所有 phase noise 計算的地基。

對平穩隨機過程 $x(t)$，自相關 $R_x(\tau)=\langle x(t)\,x(t+\tau)\rangle$。
**Wiener–Khinchin 定理**：

$$
S_x(\omega)=\int_{-\infty}^{\infty}R_x(\tau)\,e^{-j\omega\tau}\,d\tau .
$$

- **白噪特例**：$R_x(\tau)=\frac{N_0}{2}\delta(\tau)$（不同時刻完全不相關）$\Rightarrow S_x(\omega)=\frac{N_0}{2}$
  （與頻率無關，「白」就是這個意思）。本站用單邊 PSD $S_i=\overline{i_n^2}/\Delta f$（A²/Hz）。
- **variance（總功率）**：

$$
\sigma_x^2=R_x(0)=\frac{1}{2\pi}\int_{-\infty}^{\infty}S_x(\omega)\,d\omega=\int_0^{\infty}S_x^{(1\text{-side})}(f)\,df .
$$

這就是 phase variance 公式 $\sigma_\phi^2=\int_{f_1}^{f_2}S_\phi(f)\,df$ 的出處：phase variance
是 phase PSD 對頻率的積分（[P1] 使用慣例；標準隨機程序結果）。

**單位檢查**：$S_\phi$ 是 rad²/Hz，$\int S_\phi\, df$ 的單位 $=\text{rad}^2/\text{Hz}\cdot\text{Hz}=\text{rad}^2$ ✓。

**外部出處**：Wiener–Khinchin 是標準隨機程序定理（**不在下載的 5 篇 PDF 內**，屬通用教科書內容，
例如 Papoulis；[P1] 直接使用其結論）。

**站內用到**：[psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter)、
[stochastic_processes_recap](/02_foundations/stochastic_noise_basics)、
[lab_06](/04_simulation_labs/lab_06_white_noise_phase_noise)（用 Welch 法估 PSD）、
[lab_08](/04_simulation_labs/lab_08_jitter_integration)（積分 PSD 得 jitter）。

---

## 5. $10\log_{10}$ / dB 與 dBc/Hz 換算

**一句話**：dB 是「功率比的對數刻度」；dBc/Hz 是「相對 carrier 功率、每 Hz 頻寬」的相位雜訊單位。
記住「$\times10$ 功率 $=+10$ dB、$\times2$ 功率 $\approx+3$ dB」就夠用。

定義（功率比）：

$$
X_{\text{dB}}=10\log_{10}\!\left(\frac{P}{P_{ref}}\right).
$$

- **電壓/幅度比**：因為功率 $\propto$ 幅度$^2$，所以 $X_{\text{dB}}=20\log_{10}(V/V_{ref})$
  （多了一個 2）。
- **反向換算**：$P/P_{ref}=10^{X_{\text{dB}}/10}$。
- **SSB phase noise** $\mathcal{L}(\Delta f)$ 的單位是 dBc/Hz：「c」= relative to carrier，
  「/Hz」= 每單位頻寬。它與 phase PSD 的關係（小角近似，見第 6 節）：

$$
\mathcal{L}(\Delta f)\approx\frac12 S_\phi(\Delta f)\quad\Longrightarrow\quad
\mathcal{L}_{\text{dBc/Hz}}=10\log_{10}\!\left(\tfrac12 S_\phi\right),\;\;
S_\phi=2\cdot10^{\mathcal{L}_{\text{dBc/Hz}}/10}\ \text{rad}^2/\text{Hz}.
$$

**數值手感（canonical 例 C）**：$\mathcal{L}=-100$ dBc/Hz $\Rightarrow 10^{-100/10}=10^{-10}$，
$S_\phi=2\times10^{-10}$ rad²/Hz。功率好 10 倍（$-110$ dBc/Hz）= 幅度（rms）好 $\sqrt{10}\approx3.16$ 倍。

**常用換算表**：

| 功率比 | dB | 電壓比 | 直覺 |
|---|---|---|---|
| $\times2$ | $+3.01$ dB | $\times\sqrt2$ | 加一倍功率 |
| $\times10$ | $+10$ dB | $\times\sqrt{10}\approx3.16$ | 一個數量級 |
| $\times100$ | $+20$ dB | $\times10$ | 兩個數量級 |
| $\times\tfrac12$ | $-3.01$ dB | $\times1/\sqrt2$ | 砍半 |

**站內用到**：[psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter)、
[numerical_feeling](/04_simulation_labs/numerical_feeling)（Example 3 全套換算）、
[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)。

---

## 6. Small-angle PM 近似（$\mathcal{L}\approx\frac12 S_\phi$ 的由來）

**一句話**：相位抖動很小時，相位調變的單邊帶功率約等於相位 PSD 的一半。這是把「相位 PSD」
換成「資料表上的 dBc/Hz」的橋。

考慮被相位調變的 carrier：$v(t)=A\cos\!\big(\omega_0 t+\phi(t)\big)$。當 $|\phi(t)|\ll1$ rad
（small-angle，小角），用三角展開並近似 $\cos\phi\approx1$、$\sin\phi\approx\phi$：

$$
v(t)=A\big[\cos\omega_0 t\cos\phi-\sin\omega_0 t\sin\phi\big]\approx A\cos\omega_0 t-A\,\phi(t)\sin\omega_0 t .
$$

- 第一項是純 carrier；第二項 $-A\,\phi(t)\sin\omega_0 t$ 是「相位 sideband」——把基頻的 $\phi(t)$
  搬到 carrier 兩側。
- 對單一 offset 頻率 $\Delta f$ 的相位分量，sideband 功率正比於 $\phi$ 的功率；換算到**單邊帶**
  （SSB，single-sideband）相對 carrier 的密度，得

$$
\mathcal{L}(\Delta f)\approx\frac12 S_\phi(\Delta f).
$$

那個 $\frac12$ 來自「總相位功率平分到上、下兩個 sideband」的記帳。

**適用條件（重要）**：只在 $\sigma_\phi\ll1$ rad 成立。若積分頻寬太寬使 $\sigma_\phi$ 接近或超過 1 rad，
這個近似失效（carrier 會被「散掉」），要用更完整的處理。canonical 例 C 的 $\sigma_\phi=14.07$ mrad
$\ll1$，安全。

**站內用到**：[psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter)、
[numerical_feeling](/04_simulation_labs/numerical_feeling)、Eq.(16) of the spec（$\mathcal{L}\approx\frac12 S_\phi$）。

---

## 7. 三角恆等式（推導 Eq.(15)–(18) 時的工作馬）

**一句話**：把「ISF 的某條諧波」乘上「注入單音」並對時間積分時，會用到積化和差，
把乘積拆成慢項（生存）與快項（積分後消失）。

注入單音 $i(t)=I_0\cos(\Delta\omega\,t)$ 靠近 DC 時，phase response（[P1] Eq.(13), p.183 的 $c_0$ 項）
要算 $\int^{t}I_0\cos(\Delta\omega\,\tau)\,d\tau=\dfrac{I_0\sin(\Delta\omega\,t)}{\Delta\omega}$，
直接得 [P1] Eq.(15), p.183：

$$
\phi(t)\approx\frac{I_0\,c_0\sin(\Delta\omega\,t)}{2q_{max}\,\Delta\omega}.
$$

當單音靠近 $n\omega_0$ 時要用**積化和差**：

$$
\cos(n\omega_0\tau+\theta_n)\cos\big((n\omega_0+\Delta\omega)\tau\big)
=\frac12\cos\big((2n\omega_0+\Delta\omega)\tau+\theta_n\big)+\frac12\cos\big(\Delta\omega\,\tau-\theta_n\big).
$$

- 第一項頻率 $\approx2n\omega_0$（快），積分後幅度 $\propto1/(2n\omega_0)$，極小、忽略。
- 第二項頻率 $\Delta\omega$（慢、近 DC），積分後幅度 $\propto1/\Delta\omega$，生存。

只留慢項並積分，得 [P1] Eq.(16)/(17), p.183：

$$
\phi(t)\approx\frac{I_0\,c_n\sin(\Delta\omega\,t)}{2q_{max}\,\Delta\omega}.
$$

那個 $\frac12$ 就是積化和差掉出來的。**物理意義**：ISF 第 $n$ 條諧波像個 mixer（混頻器），
把 $n\omega_0$ 附近的 noise「下轉」到 carrier 附近的低頻相位調變——這是 phase noise 的頻率搬移圖像。

**常用恆等式速查**：

| 恆等式 | 用途 |
|---|---|
| $\cos A\cos B=\tfrac12[\cos(A-B)+\cos(A+B)]$ | 分離慢/快項（Eq.16/17） |
| $\sin^2\theta=\tfrac12(1-\cos2\theta)$ | 算 $\Gamma_{rms}$（$-\sin$ 的 rms=$1/\sqrt2$） |
| $\int^{t}\cos(\omega\tau)d\tau=\sin(\omega t)/\omega$ | 積分器 $1/\omega$（Eq.15） |

**站內用到**：[fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf)、
[convolution_derivation](/03_isf_core_theory/convolution_derivation)、第 1 節 Parseval 的正交性。

---

## 8. Random walk variance（累積 jitter 的 $\sqrt{\Delta t}$ 律）

**一句話**：開環振盪器沒有絕對時間參考，每個週期的相位誤差像「醉漢走路」一樣獨立累加；
誤差的**變異數**線性成長，所以**標準差**按 $\sqrt{\Delta t}$ 成長。

設每個週期注入一個獨立、零均值、變異數 $\sigma_1^2$ 的相位誤差 $\delta_k$（白噪在一週期內積分的結果）。
經過 $M$ 個週期後總相位誤差 $\Phi_M=\sum_{k=1}^{M}\delta_k$。因為各 $\delta_k$ **獨立**，
變異數可加（互相關項期望值為 0）：

$$
\mathrm{Var}(\Phi_M)=\sum_{k=1}^{M}\mathrm{Var}(\delta_k)=M\,\sigma_1^2 .
$$

- 量測區間 $\Delta t=M\cdot T$，所以 $M=\Delta t/T$，$\mathrm{Var}(\Phi_M)=\dfrac{\sigma_1^2}{T}\,\Delta t\propto\Delta t$。
- 換成時間 jitter（$\sigma_t=\sigma_\phi/(2\pi f_0)$）並開根號：

$$
\sigma_{\Delta t}=\kappa\,\sqrt{\Delta t}\qquad([P2]\ \text{Eq.}(10),\ \text{p.793}).
$$

$\kappa$ 是每個元件的比例常數，單位 $\sqrt{\text{s}}$；它由同一個 $\Gamma_{rms}^2/q_{max}^2$ 比值決定
（[P2] Eq.(12), p.793：$\kappa=\frac{\Gamma_{rms}}{q_{max}}\sqrt{\tfrac12\tfrac{\overline{i_n^2}}{\Delta f}}$，已核實）。

**關鍵直覺**：variance（功率）線性增長，標準差（rms）開根號增長。這是 random walk（隨機漫步）的
招牌；只要相位誤差**獨立累加且無恢復力**就會出現（對比：有 PLL 鎖定就有恢復力，jitter 會被壓住，
不再無上界成長）。對應主張 C6。

**數值手感**：若相隔 1000 個週期（5 GHz 下 $\Delta t=200$ ns），$\sigma_{\Delta t}$ 是相隔 10 個週期
（$\Delta t=2$ ns）的 $\sqrt{1000/10}=\sqrt{100}=10$ 倍——區間長 100 倍，jitter 只大 10 倍。

**站內用到**：[lab_03](/04_simulation_labs/lab_03_ring_oscillator_toy_model)
（`ring_oscillator_timing_noise_accumulation.png`：$\sigma_{\Delta t}=\sigma\sqrt{\Delta N}$ 隨機漫步）、
[psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter)、
[serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)。

---

## 速查總表

| 工具 | 核心式 | 站內主要用途 |
|---|---|---|
| 傅立葉/Parseval | $\sum c_n^2=2\Gamma_{rms}^2$ | ISF 諧波分解、$\Gamma_{rms}$ |
| LTV 卷積 | $\phi=\frac{1}{q_{max}}\int^{t}\Gamma\,i_n\,d\tau$ | 相位疊加、LTV vs LTI |
| 積分器 $1/(j\omega)$ | $\vert H\vert ^2=1/\omega^2$ | 白噪 → $1/f^2$（$-20$ dB/dec） |
| Wiener–Khinchin | $S_x=\mathcal{F}\{R_x\}$ | PSD ↔ 自相關、variance |
| dB / dBc/Hz | $X_{\text{dB}}=10\log_{10}(P/P_{ref})$ | 單位換算 |
| small-angle PM | $\mathcal{L}\approx\frac12 S_\phi$ | dBc/Hz ↔ phase PSD |
| 積化和差 | $\cos A\cos B=\tfrac12[\cdots]$ | Eq.(15)–(18) 混頻 |
| random walk | $\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$ | 累積 jitter |

## 延伸閱讀

- 符號與單位總表：[notation](/00_overview/notation)
- 隨機程序複習：[stochastic_processes_recap](/02_foundations/stochastic_noise_basics)
- 數值口算練習：[numerical_feeling](/04_simulation_labs/numerical_feeling)
- 公式索引（每條 → 推導頁 → 來源）：[equation_index](/01_paper_map/equation_index)
- 完整文獻清單：[references](/99_appendix/references)
